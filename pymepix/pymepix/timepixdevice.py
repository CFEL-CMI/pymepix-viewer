##############################################################################
##
# This file is part of Pymepix
#
# https://arxiv.org/abs/1905.07999
#
#
# Pymepix is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pymepix is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pymepix.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import numpy as np
from pymepix.SPIDR.spidrdevice import SpidrDevice
from pymepix.SPIDR.error import PymePixException
from pymepix.timepixdef import *
from pymepix.config import TimepixConfig, SophyConfig, DefaultConfig
# from .config.sophyconfig import SophyConfig
from pymepix.core.log import Logger
from pymepix.processing.acquisition import PixelPipeline
from multiprocessing.sharedctypes import Value
import time
import threading


class ConfigClassException(Exception):
    pass


class BadPixelFormat(Exception):
    pass


class TimepixDevice(Logger):
    """ Provides high level control of a timepix/medipix object



    """

    def update_timer(self):
        """Heartbeat thread"""
        self.info('Heartbeat thread starting')
        while self._run_timer:
            while self._pause_timer and self._run_timer:
                time.sleep(1.0)
                continue

            self._timer_lsb, self._timer_msb = self._device.timer
            self._timer = (self._timer_msb & 0xFFFFFFFF) << 32 | (self._timer_lsb & 0xFFFFFFFF)
            self._longtime.value = self._timer
            self.debug(
                f'Reading heartbeat LSB: {self._timer_lsb} MSB: {self._timer_msb} TIMER: {self._timer} {self._timer * 25e-9} ')
            time.sleep(1.0)

    def __init__(self, spidr_device, data_queue):

        self._device = spidr_device
        Logger.__init__(self, 'Timepix ' + self.devIdToString())
        self._data_queue = data_queue
        self._udp_address = (self._device.ipAddrDest, self._device.serverPort)
        self.info('UDP Address is {}:{}'.format(*self._udp_address))
        self._pixel_offset_coords = (0, 0)
        # TODO: this doesn't work, it makes the spot round and the tof appear at 10ms
        # self._device.reset()
        # self._device.reinitDevice()

        self._longtime = Value('L', 0)
        self.setupAcquisition(PixelPipeline)

        # TODO: this doesn't work
        self._initDACS()

        self._event_callback = None

        self._run_timer = True
        self._pause_timer = False

        self._config_class = SophyConfig

        self.setEthernetFilter(0xFFFF)

        # Start the timer thread
        self._timer_thread = threading.Thread(target=self.update_timer)
        self._timer_thread.daemon = True
        self._timer_thread.start()
        self.pauseHeartbeat()
        self._acq_running = False

    def setupAcquisition(self, acquisition_klass, *args, **kwargs):
        self.info('Setting up acquisition class')
        self._acquisition_pipeline = acquisition_klass(self._data_queue, self._udp_address, self._longtime, *args,
                                                       **kwargs)

    def _initDACS(self):
        # TODO: where does the 5 in the pixel threshold mask come from???
        # self.getDeviceConfig()

        self.setConfigClass(DefaultConfig)
        # TODO: these settings are not the same as from SoPhy yet
        # self.loadConfig()
        # self.setConfigClass(SophyConfig)

        self.getDeviceConfig()

    def setConfigClass(self, klass):
        if issubclass(klass, TimepixConfig):
            self._config_class = klass
        else:
            raise ConfigClassException

    def loadConfig(self, *args, **kwargs):
        """Loads dac settings from the Config class

        """

        config = self._config_class(*args, **kwargs)

        for name, code, value in config.dacCodes():
            self.info(f'Setting DAC {name}: {value}')
            self.setDac(code, value)
            # time.sleep(0.5)

        # TODO: this doesn't work for now
        # if config.thresholdPixels() is not None:
        #    self.pixelThreshold = config.thresholdPixels()

        # if config.maskPixels() is not None:
        #    self.pixelMask = config.maskPixels()

        # self.uploadPixels()
        # self.refreshPixels()

        # print(self.pixelThreshold)

    def setupDevice(self):
        """Sets up valid paramters for acquisition

        This will be manual when other acquisition parameters are working

        """
        self.debug('Setting up acqusition')
        self.polarity = Polarity.Positive
        self.debug('Polarity set to {}'.format(Polarity(self.polarity)))
        self.operationMode = OperationMode.ToAandToT
        self.debug('OperationMode set to {}'.format(OperationMode(self.operationMode)))
        self.grayCounter = GrayCounter.Enable
        self.debug('GrayCounter set to {}'.format(GrayCounter(self.grayCounter)))
        self.superPixel = SuperPixel.Enable
        self.debug('SuperPixel set to {}'.format(SuperPixel(self.superPixel)))
        # TODO: PLL
        # 0x11E -> 00 0001 0001 1110
        # SoPhy ->            1 1110
        # PLL configuration: 40 MHz on pixel matrix
        pll_cfg = 0x01E | 0x100  # 40 MHz, 16 clock phases
        self._device.pllConfig = pll_cfg
        # self._device.setTpPeriodPhase(10,0)
        # self._device.tpNumber = 1
        # self._device.columnTestPulseRegister

    def getDeviceConfig(self):
        '''
        extract current timepix device configuration
        :return: none
        '''

        pass
        print(f"pixel threshold: {self.pixelThreshold}")
        print(f"pixel mask: {self.pixelMask}")
        print(f"polarity: {self.polarity}")
        print(f"operation mode: {self.operationMode}")
        print(f"gray counter: {self.grayCounter}")
        print(f"super pixel: {self.superPixel}")
        print(f"time overflow: {self.timerOverflowControl}")
        print(f"Ibias DiscS1 off: {self.Ibias_DiscS1_OFF}")
        print(f"Ibias DiscS1 on: {self.Ibias_DiscS1_ON}")
        print(f"Ibias DiscS2 off: {self.Ibias_DiscS2_OFF}")
        print(f"Ibias DiscS2 on: {self.Ibias_DiscS2_ON}")
        print(f"Ibias preamp off: {self.Ibias_Preamp_OFF}")
        print(f"Ibias preamp on: {self.Ibias_Preamp_ON}")
        print(f"V preamp NCAS: {self.VPreamp_NCAS}")
        print(f"Ibias Ikrum: {self.Ibias_Ikrum}")
        print(f"Vfbk: {self.Vfbk}")
        print(f"Vthreashold coarse: {self.Vthreshold_coarse}")
        print(f"Vthreashold fine: {self.Vthreshold_fine}")
        print(f"Ibias pixel DAC: {self.Ibias_PixelDAC}")
        print(f"Ibias TP buffer in: {self.Ibias_TPbufferIn}")
        print(f"Ibias TP buffer out: {self.Ibias_TPbufferOut}")
        print(f"VTP coarse: {self.VTP_coarse}")
        print(f"VTP fine: {self.VTP_fine}")
        print(f'PLL config: {bin(self._device.pllConfig)}')
        '''
        import h5py
        import time
        with h5py.File(f'{time.strftime("%Y%m%d-%H%M%S_TimePixSettings.hdf5")}', 'w') as f:
            f.create_dataset('pixel threshold', data=self.pixelThreshold)
            f.create_dataset('pixel mask', data=self.pixelMask)
            f.create_dataset('polarity', data=self.polarity)
            f.create_dataset('operation mode', data=self.operationMode)
            f.create_dataset('gray counter', data=self.grayCounter)
            f.create_dataset('super pixel', data=self.superPixel)
            f.create_dataset('time overflow', data=self.timerOverflowControl)
            f.create_dataset('Ibias DiscS1 off', data=self.Ibias_DiscS1_OFF)
            f.create_dataset('Ibias DiscS1 on', data=self.Ibias_DiscS1_ON)
            f.create_dataset('Ibias DiscS2 off', data=self.Ibias_DiscS2_OFF)
            f.create_dataset('Ibias DiscS2 on', data=self.Ibias_DiscS2_ON)
            f.create_dataset('Ibias preamp off', data=self.Ibias_Preamp_OFF)
            f.create_dataset('Ibias preamp on', data=self.Ibias_Preamp_ON)
            f.create_dataset('V preamp NCAS', data=self.VPreamp_NCAS)
            f.create_dataset('Ibias Ikrum', data=self.Ibias_Ikrum)
            f.create_dataset('Vfbk', data=self.Vfbk)
            f.create_dataset('Vthreashold coarse', data=self.Vthreshold_coarse)
            f.create_dataset('Vthreashold fine', data=self.Vthreshold_fine)
            f.create_dataset('Ibias pixel DAC', data=self.Ibias_PixelDAC)
            f.create_dataset('Ibias TP buffer in', data=self.Ibias_TPbufferIn)
            f.create_dataset('Ibias TP buffer out', data=self.Ibias_TPbufferOut)
            f.create_dataset('VTP coarse', data=self.VTP_coarse)
            f.create_dataset('VTP fine', data=self.VTP_fine)
            f.create_dataset('PLL config', data=self._device.pllConfig)
        '''

    @property
    def acquisition(self):
        """Returns the acquisition object

        Can be used to set parameters in the acqusition directly for example,
        to setup TOF calculation when using a :class:`PixelPipeline`

        >>> tpx.acqusition.enableEvents
        False
        >>> tpx.acquistion.enableEvents = True

        """
        return self._acquisition_pipeline

    def pauseHeartbeat(self):
        self._pause_timer = True

    def resumeHeartbeat(self):
        self._pause_timer = False

    def devIdToString(self):
        """Converts device ID into readable string

        Returns
        --------
        str
            Device string identifier

        """
        devId = self._device.deviceId
        waferno = (devId >> 8) & 0xFFF
        id_y = (devId >> 4) & 0xF
        id_x = (devId >> 0) & 0xF
        return "W{:04d}_{}{:02d}".format(waferno, chr(ord('A') + id_x - 1), id_y)

    @property
    def deviceName(self):
        return self.devIdToString()

    def setEthernetFilter(self, eth_filter):
        """Sets the packet filter, usually set to 0xFFFF to all all packets"""
        eth_mask, cpu_mask = self._device.headerFilter
        eth_mask = eth_filter
        self._device.setHeaderFilter(eth_mask, cpu_mask)
        eth_mask, cpu_mask = self._device.headerFilter
        self.info('Dev: {} eth_mask :{:8X} cpu_mask: {:8X}'.format(self._device.deviceId, eth_mask, cpu_mask))

    def resetPixels(self):
        """Clears pixel configuration"""
        self._device.clearPixelConfig()
        self._device.resetPixels()

    @property
    def pixelThreshold(self):
        """Threshold set for timepix device

        Parameters
        ----------
        value : :obj:`numpy.array` of :obj:`int`
            256x256 uint8 threshold to set locally


        Returns
        -----------
        :obj:`numpy.array` of :obj:`int` or :obj:`None`:
            Locally stored threshold  matrix

        """
        # self._device.getPixelConfig()
        return self._device._pixel_threshold

    @pixelThreshold.setter
    def pixelThreshold(self, value):
        self._device._pixel_threshold = value

    @property
    def pixelMask(self):
        """Pixel mask set for timepix device

        Parameters
        ----------
        value : :obj:`numpy.array` of :obj:`int`
            256x256 uint8 threshold mask to set locally


        Returns
        -----------
        :obj:`numpy.array` of :obj:`int` or :obj:`None`:
            Locally stored pixel mask matrix


        """
        # self._device.getPixelConfig()
        return self._device._pixel_mask

    @pixelMask.setter
    def pixelMask(self, value):
        self._device._pixel_mask = value

    @property
    def pixelTest(self):
        """Pixel test set for timepix device

        Parameters
        ----------
        value : :obj:`numpy.array` of :obj:`int`
            256x256 uint8 pixel test to set locally


        Returns
        -----------
        :obj:`numpy.array` of :obj:`int` or :obj:`None`:
            Locally stored pixel test matrix


        """
        # self._device.getPixelConfig()
        return self._device._pixel_test

    @pixelTest.setter
    def pixelTest(self, value):
        self._device._pixel_test = value

    def uploadPixels(self):
        """Uploads local pixel configuration to timepix"""
        self._device.uploadPixelConfig()

    def refreshPixels(self):
        """Loads timepix pixel configuration to local array"""
        self._device.getPixelConfig()

    def start(self):
        self.stop()
        self.info('Beginning acquisition')
        self.resumeHeartbeat()
        if self._acquisition_pipeline is not None:
            self._acquisition_pipeline.start()
            self._acq_running = True

    def stop(self):

        if self._acq_running:
            self.info('Stopping acquisition')
            if self._acquisition_pipeline is not None:
                self._acquisition_pipeline.stop()
            self.pauseHeartbeat()
            self._acq_running = False

    # -----General Configuration-------
    @property
    def polarity(self):
        return Polarity(self._device.genConfig & 0x1)

    @polarity.setter
    def polarity(self, value):
        gen_config = self._device.genConfig
        self._device.genConfig = (gen_config & ~1) | value

    @property
    def operationMode(self):
        return OperationMode(self._device.genConfig & OperationMode.Mask)

    @operationMode.setter
    def operationMode(self, value):
        gen_config = self._device.genConfig
        self._device.genConfig = (gen_config & ~OperationMode.Mask) | (value)

    @property
    def grayCounter(self):
        return GrayCounter(self._device.genConfig & GrayCounter.Mask)

    @grayCounter.setter
    def grayCounter(self, value):
        gen_config = self._device.genConfig
        self._device.genConfig = (gen_config & ~GrayCounter.Mask) | (value)

    @property
    def testPulse(self):
        return TestPulse(self._device.genConfig & TestPulse.Mask)

    @testPulse.setter
    def testPulse(self, value):
        gen_config = self._device.genConfig
        self._device.genConfig = (gen_config & ~TestPulse.Mask) | (value)

    @property
    def superPixel(self):
        return SuperPixel(self._device.genConfig & SuperPixel.Mask)

    @superPixel.setter
    def superPixel(self, value):
        gen_config = self._device.genConfig
        self._device.genConfig = (gen_config & ~SuperPixel.Mask) | (value)

    @property
    def timerOverflowControl(self):
        return TimerOverflow(self._device.genConfig & TimerOverflow.Mask)

    @timerOverflowControl.setter
    def timerOverflowControl(self, value):
        gen_config = self._device.genConfig
        self._device.genConfig = (gen_config & ~TimerOverflow.Mask) | (value)

    @property
    def testPulseDigitalAnalog(self):
        return TestPulseDigAnalog(self._device.genConfig & TestPulseDigAnalog.Mask)

    @testPulseDigitalAnalog.setter
    def testPulseDigitalAnalog(self, value):
        gen_config = self._device.genConfig
        self._device.genConfig = (gen_config & ~TestPulseDigAnalog.Mask) | (value)

    @property
    def testPulseGeneratorSource(self):
        return TestPulseGenerator(self._device.genConfig & TestPulseGenerator.Mask)

    @testPulseGeneratorSource.setter
    def testPulseGeneratorSource(self, value):
        gen_config = self._device.genConfig
        self._device.genConfig = (gen_config & ~TestPulseGenerator.Mask) | (value)

    @property
    def timeOfArrivalClock(self):
        return TimeofArrivalClock(self._device.genConfig & TimeofArrivalClock.Mask)

    @timeOfArrivalClock.setter
    def timeOfArrivalClock(self, value):
        gen_config = self._device.genConfig
        self._device.genConfig = (gen_config & ~TimeofArrivalClock.Mask) | (value)

    @property
    def Ibias_Preamp_ON(self):
        """nanoAmps"""
        value = self._device.getDac(DacRegisterCodes.Ibias_Preamp_ON)
        return ((value & 0xFF) * 20.0)

    @Ibias_Preamp_ON.setter
    def Ibias_Preamp_ON(self, value):
        """nanoAmps"""
        nA = value
        nAint = int(nA / 20.0)
        self._device.setDac(DacRegisterCodes.Ibias_Preamp_ON, nAint & 0xFF)

    @property
    def Ibias_Preamp_OFF(self):
        """nanoAmps"""
        value = self._device.getDac(DacRegisterCodes.Ibias_Preamp_OFF)
        return ((value & 0xF) * 20.0)

    @Ibias_Preamp_OFF.setter
    def Ibias_Preamp_OFF(self, value):
        """nanoAmps"""
        nA = value
        nAint = int(nA / 20.0)
        self._device.setDac(DacRegisterCodes.Ibias_Preamp_OFF, nAint & 0xF)

    @property
    def VPreamp_NCAS(self):
        """Volts"""
        value = self._device.getDac(DacRegisterCodes.VPreamp_NCAS)
        return ((value & 0xFF) * 5.0) / 1000.0

    @VPreamp_NCAS.setter
    def VPreamp_NCAS(self, value):
        """Volts"""
        n = value * 1000.0
        nint = int(n / 5.0)
        self._device.setDac(DacRegisterCodes.VPreamp_NCAS, nint & 0xFF)

    @property
    def Ibias_Ikrum(self):
        """
        Bias current, affects the pulse shaping and has effect on gain. The higher the current, the shorter shaping, but lower gain.
        Unit=nA"""
        value = self._device.getDac(DacRegisterCodes.Ibias_Ikrum)
        return ((value & 0xFF) * 240.0) / 1000.0

    @Ibias_Ikrum.setter
    def Ibias_Ikrum(self, value):
        """nA"""
        n = value * 1000.0
        nint = int(n / 240.0)
        self._device.setDac(DacRegisterCodes.Ibias_Ikrum, nint & 0xFF)

    @property
    def Vfbk(self):
        """V"""
        value = self._device.getDac(DacRegisterCodes.Vfbk)
        return ((value & 0xFF) * 5.0) / 1000.0

    @Vfbk.setter
    def Vfbk(self, value):
        """V"""
        n = value * 1000.0
        nint = int(n / 5.0)
        self._device.setDac(DacRegisterCodes.Vfbk, nint & 0xFF)

    @property
    def Vthreshold_fine(self):
        """mV"""
        value = self._device.getDac(DacRegisterCodes.Vthreshold_fine)
        return ((value & 0x1FF) * 500.0) / 1000.0

    @Vthreshold_fine.setter
    def Vthreshold_fine(self, value):
        """mV"""
        n = value * 1000.0
        nint = int(n / 500.0)
        self._device.setDac(DacRegisterCodes.Vthreshold_fine, nint & 0x1FF)

    @property
    def Vthreshold_coarse(self):
        """V"""
        value = self._device.getDac(DacRegisterCodes.Vthreshold_coarse)
        return ((value & 0xF) * 80.0) / 1000.0

    @Vthreshold_coarse.setter
    def Vthreshold_coarse(self, value):
        """V"""
        n = value * 1000.0
        nint = int(n / 80.0)
        self._device.setDac(DacRegisterCodes.Vthreshold_coarse, nint & 0xF)

    @property
    def Ibias_DiscS1_ON(self):
        """uA"""
        value = self._device.getDac(DacRegisterCodes.Ibias_DiscS1_ON)
        return ((value & 0xFF) * 20.0) / 1000.0

    @Ibias_DiscS1_ON.setter
    def Ibias_DiscS1_ON(self, value):
        """uA"""
        n = value * 1000.0
        nint = int(n / 20.0)
        self._device.setDac(DacRegisterCodes.Ibias_DiscS1_ON, nint & 0xFF)

    @property
    def Ibias_DiscS1_OFF(self):
        """nA"""
        value = self._device.getDac(DacRegisterCodes.Ibias_DiscS1_OFF)
        return ((value & 0xF) * 20.0)

    @Ibias_DiscS1_OFF.setter
    def Ibias_DiscS1_OFF(self, value):
        """nA"""
        n = value
        nint = int(n / 20.0)
        self._device.setDac(DacRegisterCodes.Ibias_DiscS1_OFF, nint & 0xF)

    @property
    def Ibias_DiscS2_ON(self):
        """uA"""
        value = self._device.getDac(DacRegisterCodes.Ibias_DiscS2_ON)
        return ((value & 0xFF) * 13.0) / 1000.0

    @Ibias_DiscS2_ON.setter
    def Ibias_DiscS2_ON(self, value):
        """uA"""
        n = value * 1000.0
        nint = int(n / 13.0)
        self._device.setDac(DacRegisterCodes.Ibias_DiscS2_ON, nint & 0xFF)

    @property
    def Ibias_DiscS2_OFF(self):
        """nA"""
        value = self._device.getDac(DacRegisterCodes.Ibias_DiscS2_OFF)
        return ((value & 0xF) * 13.0)

    @Ibias_DiscS2_OFF.setter
    def Ibias_DiscS2_OFF(self, value):
        """nA"""
        n = value
        nint = int(n / 13.0)
        self._device.setDac(DacRegisterCodes.Ibias_DiscS2_OFF, nint & 0xF)

    @property
    def Ibias_PixelDAC(self):
        """nA"""
        value = self._device.getDac(DacRegisterCodes.Ibias_PixelDAC)
        return ((value & 0xFF) * 1.08)

    @Ibias_PixelDAC.setter
    def Ibias_PixelDAC(self, value):
        """nA"""
        n = value
        nint = int(n / 1.08)
        self._device.setDac(DacRegisterCodes.Ibias_PixelDAC, nint & 0xFF)

    @property
    def Ibias_TPbufferIn(self):
        """uA"""
        value = self._device.getDac(DacRegisterCodes.Ibias_TPbufferIn)
        return ((value & 0xFF) * 40.0) / 1000.0

    @Ibias_TPbufferIn.setter
    def Ibias_TPbufferIn(self, value):
        """uA"""
        n = value * 1000.0
        nint = int(n / 40.0)
        self._device.setDac(DacRegisterCodes.Ibias_TPbufferIn, nint & 0xFF)

    @property
    def Ibias_TPbufferOut(self):
        """uA"""
        value = self._device.getDac(DacRegisterCodes.Ibias_TPbufferOut)
        return float((value & 0xFF))

    @Ibias_TPbufferOut.setter
    def Ibias_TPbufferOut(self, value):
        """uA"""
        n = value
        nint = int(n)
        self._device.setDac(DacRegisterCodes.Ibias_TPbufferOut, nint & 0xFF)

    @property
    def VTP_coarse(self):
        """V"""
        value = self._device.getDac(DacRegisterCodes.VTP_coarse) * 5
        return float((value & 0xFF)) / 1000.0

    @VTP_coarse.setter
    def VTP_coarse(self, value):
        """V"""
        n = value * 1000.0
        nint = int(n / 5.0)
        self._device.setDac(DacRegisterCodes.VTP_coarse, nint & 0xFF)

    @property
    def VTP_fine(self):
        """V"""
        # TODO: multiply by 2.5 and typecast to int for bit operation isn't good...
        value = int(self._device.getDac(DacRegisterCodes.VTP_fine) * 2.5)
        return float((value & 0x1FF)) / 1000.0

    @VTP_fine.setter
    def VTP_fine(self, value):
        """V"""
        n = value * 1000.0
        nint = int(n / 2.5)
        self._device.setDac(DacRegisterCodes.VTP_fine, nint & 0x1FF)

    def setDac(self, code, value):
        """Sets the DAC parameter using codes

        Parameters
        ----------
        code: :obj:`int`
            DAC code to set

        value: :obj:`int`
            value to set
        """
        self._device.setDac(code, value)


def main():
    import logging
    from .SPIDR.spidrcontroller import SPIDRController
    from .SPIDR.spidrdefs import SpidrShutterMode
    from multiprocessing import Queue
    logging.basicConfig(level=logging.INFO)
    end_queue = Queue()

    def get_queue_thread(queue):
        while True:
            value = queue.get()
            print(value)
            if value is None:
                break

    t = threading.Thread(target=get_queue_thread, args=(end_queue,))
    t.daemon = True
    t.start()

    spidr = SPIDRController(('192.168.1.10', 50000))

    timepix = TimepixDevice(spidr[0], end_queue)
    timepix.loadSophyConfig('/Users/alrefaie/Documents/repos/libtimepix/config/eq-norm-50V.spx')

    # spidr.shutterTriggerMode = SpidrShutterMode.Auto
    spidr.disableExternalRefClock()
    TdcEnable = 0x0000
    spidr.setSpidrReg(0x2B8, TdcEnable)
    spidr.enableDecoders(True)
    spidr.resetTimers()
    spidr.restartTimers()

    spidr.datadrivenReadout()
    timepix.setupDevice()

    spidr.openShutter()
    timepix.start()
    time.sleep(4.0)
    timepix.stop()
    logging.info('DONE')
    spidr.closeShutter()


if __name__ == "__main__":
    main()

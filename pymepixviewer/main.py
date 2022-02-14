#!/usr/bin/env python3
##############################################################################
##
# This file is part of pymepixviewer
#
# https://arxiv.org/abs/1905.07999
#
#
# pymepixviewer is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pymepixviewer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pymepixviewer.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import os
import logging
import platform
import time
import argparse

import numpy as np
import zmq
import socket
import pymepix
import pymepix.config.load_config as cfg
from pymepix.config.sophyconfig import SophyConfig
from pymepix.processing import MessageType
from pymepix.processing.acquisition import CentroidPipeline

# force to load PyQt5 for systems where PyQt4 is still installed
from PyQt5 import QtWidgets, QtCore, QtGui

from pymepixviewer.core.datatypes import ViewerMode
from pymepixviewer.dialogs.postprocessing import PostProcessing
from pymepixviewer.panels.blobview import BlobView
from pymepixviewer.panels.daqconfig import DaqConfigPanel
from pymepixviewer.panels.editpixelmaskpanel import EditPixelMaskPanel
from pymepixviewer.panels.timeofflight import TimeOfFlightPanel
from pymepixviewer.panels.timepixsetupplotspanel import TimepixSetupPlotsPanel
from pymepixviewer.ui.mainui import Ui_MainWindow


logger = logging.getLogger(__name__)

QUEUE_SIZE_WARNING_LIMIT = 30
QUEUE_SIZE_WARNING_TEXT = "The queue size has passed the warning size of {} packages with {} packages in the queue. The data can not be processed at the rate of arrival. Please consider increasing the number of processes allocated to the centroiding, reducing the data frequency or increase the packages skipped for live processing. The current queue size can be checked in the processing tab. <b>This can have a significant impact on the recorded data! Possible loss of data!</b>"


class GenericThread(QtCore.QThread):
    def __init__(self, function, *args, **kwargs):
        QtCore.QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        self.wait()

    def run(self):
        self.function(*self.args, **self.kwargs)
        return


class PymepixDAQ(QtWidgets.QMainWindow, Ui_MainWindow):
    displayNow = QtCore.pyqtSignal()
    onRaw = QtCore.pyqtSignal(object)
    onPixelToA = QtCore.pyqtSignal(object)
    onPixelToF = QtCore.pyqtSignal(object)
    onCentroid = QtCore.pyqtSignal(object)
    clearNow = QtCore.pyqtSignal()
    modeChange = QtCore.pyqtSignal(object)
    updateStatusSignal = QtCore.pyqtSignal(object)

    fineThresholdUpdate = QtCore.pyqtSignal(float)
    coarseThresholdUpdate = QtCore.pyqtSignal(float)

    start_acq_sig = QtCore.pyqtSignal()
    stop_acq_sig = QtCore.pyqtSignal()

    show_slow_processing_warning_sig = QtCore.pyqtSignal(int)

    def statusUdate(self):
        logger.info("Starting status update thread")

        while True:
            fpga = self._timepix._spidr.fpgaTemperature
            local = self._timepix._spidr.localTemperature
            remote = self._timepix._spidr.remoteTemperature
            chipSpeed = self._timepix._spidr.chipboardFanSpeed
            spidrSpeed = self._timepix._spidr.spidrFanSpeed
            longtime = self._timepix._timepix_devices[0]._longtime.value * 25e-9

            self.updatePacketProcessorOutputQueueSize()

            self.updateStatusSignal.emit(
                f"T_(FPGA)={fpga}, T_(loc)={local}, T_(remote)={remote}, Fan(chip)={chipSpeed}, Fan(SPIDR)={spidrSpeed}, Longtime={longtime:.2f}"
            )
            # self.statusbar.showMessage(, 5000)
            time.sleep(5)

    def api_server(self):
        """Function to provide a simple remote interface for the GUI using ZMQ"""
        self.rest_sock = self.ctx.socket(zmq.REP)
        self.rest_sock.connect("tcp://localhost:9033")
        logger.info(f"API server bind on {socket.gethostbyname(socket.gethostname())}:9033")

        run_server = True
        while run_server:
            request = self.rest_sock.recv_json()
            command = request["command"]
            logger.debug(f"API server: {command} command")

            if command == "PATH":
                if request["parameters"]["path"] != None:
                    logger.debug(
                        f"API server: Changing path to {request['parameters']['path']}"
                    )
                    self._config_panel.acqtab.path_name.setText(request["parameters"]["path"])
                path = self._config_panel.acqtab.path_name.text()
                response = {"result": path}
                self.rest_sock.send_json(response)
            elif command == "PREFIX":
                if request["parameters"]["prefix"] != None:
                    logger.debug(
                        f"API server: Changing prefix to {request['parameters']['prefix']}"
                    )
                    self._config_panel.acqtab.file_prefix.setText(
                        request["parameters"]["prefix"]
                    )
                prefix = self._config_panel.acqtab.file_prefix.text()
                response = {"result": prefix}
                self.rest_sock.send_json(response)
            elif command == "START_ACQUISITION":
                self.start_acq_sig.emit()
                response = {"result": "STARTED_ACQUISITION"}
                self.rest_sock.send_json(response)
            elif command == "STOP_ACQUISITION":
                self.stop_acq_sig.emit()
                response = {"result": "STOPPED_ACQUISITION"}
                self.rest_sock.send_json(response)
            elif command == "GET_ROI_SUM":
                histogram_sums = []
                for i in range(self._tof_panel._roi_model.rootItem.childCount()):
                    roi = self._tof_panel._roi_model.rootItem.child(i)
                    histogram_sums.append(int(roi.roi_sum))
                response = {"result": histogram_sums}
                self.rest_sock.send_json(response)
            else:
                self.updateStatusSignal.emit(f"API server recieved unknown command {command}")
                logger.warning(f'API server recieved unknown command "{command}"')
                response = {"result": "UNKNOWN_COMMAND"}
                self.rest_sock.send_json(response)

    def __init__(self, parent=None):
        super(PymepixDAQ, self).__init__(parent)
        self.setupUi(self)

        QtCore.QCoreApplication.setOrganizationName("CFEL-CMI")
        QtCore.QCoreApplication.setOrganizationDomain("controlled-molecule-imaging.org")
        QtCore.QCoreApplication.setApplicationName("Pymepix Viewer")

        self.queue_size_warning_displayed = False

        self._current_mode = ViewerMode.TOA
        self.setupWindow()

        self._view_widgets = {}

        self._event_max = -1
        self._current_event_count = 0

        self.setCentralWidget(None)

        self._display_rate = 1 / 5
        self._frame_time = -1.0
        self._last_frame = 0.0
        self._last_update = 0
        self.connectSignals()
        self.startupTimepix(timepix_ip)

        # Initialize SoPhy configuration manually, because the corresponding signal is connected after initialization of the LineEdit.
        # This will load the selected SoPhy configuration file into the camera
        self.__load_sophy_config_file(self._config_panel.acqtab.sophy_config.text())
        self._config_panel.proctab.read_settings()

        self.onModeChange(ViewerMode.TOA)
        self._statusUpdate.start()

        self.ctx = zmq.Context.instance()
        self._api_server.start()

    def closeEvent(self, event):
        sock = self.ctx.socket(zmq.PUSH)
        sock.connect("tcp://127.0.0.1:9033")
        sock.send_string("STOP API SERVER")
        time.sleep(0.5)
        sock.close()

        super(QtGui.QMainWindow, self).closeEvent(event)

    def switchToMode(self):
        self._timepix.stop()
        if self._current_mode is ViewerMode.TOA:
            # self._timepix[0].setupAcquisition(pymepix.processing.PixelPipeline)
            self.__get_packet_processor().handle_events = False
            logger.info(
                "Switch to TOA mode, {}".format(
                    self.__get_packet_processor().handle_events
                )
            )
        elif self._current_mode is ViewerMode.TOF:
            # self._timepix[0].setupAcquisition(pymepix.processing.PixelPipeline)
            self.__get_packet_processor().handle_events = True
            logger.info(
                "Switch to TOF mode, {}".format(
                    self.__get_packet_processor().handle_events
                )
            )
        elif self._current_mode is ViewerMode.Centroid:
            # self._timepix[0].setupAcquisition(pymepix.processing.CentroidPipeline)
            self.__get_packet_processor().handle_events = True
            logger.info(
                "Switch to Centroid mode, {}".format(
                    self.__get_packet_processor().handle_events
                )
            )

        time.sleep(2.0)
        self._timepix.start()

    def startupTimepix(self, timepix_ip):

        self._timepix = pymepix.PymepixConnection(
            (timepix_ip, 50000), pipeline_class=CentroidPipeline
        )
        self._timepix.dataCallback = self.onData

        if len(self._timepix) == 0:
            logger.error("NO TIMEPIX DEVICES DETECTED")
            quit()

        logging.getLogger("pymepix").setLevel(logging.INFO)

        logger.info(
            "Fine: {} Coarse: {}".format(
                self._timepix[0].Vthreshold_fine, self._timepix[0].Vthreshold_coarse
            )
        )

        self.coarseThresholdUpdate.emit(self._timepix[0].Vthreshold_coarse)
        self.fineThresholdUpdate.emit(self._timepix[0].Vthreshold_fine)

        self._timepix.start()

    def onClose(self):
        self._timepix.stop()

    def setFineThreshold(self, value):
        self._timepix[0].Vthreshold_fine = value

    def setCoarseThreshold(self, value):
        self._timepix[0].Vthreshold_coarse = value

    def setEventWindow(self, event_window_min, event_window_max):
        logger.info(
            "Setting Event window {} {}".format(event_window_min, event_window_max)
        )
        self.__get_packet_processor().event_window = (
            event_window_min,
            event_window_max,
        )

    def setTriggersProcessed(self, triggers_processed):
        logger.info("Setting centroid skip {}".format(triggers_processed))
        self.__get_centroid_calculator().triggers_processed = triggers_processed

    def setNumberProcesses(self, number_processes):
        logger.info("Setting number of blob processes {}".format(number_processes))
        self._timepix.stop()
        self._timepix[0].acquisition.numBlobProcesses = number_processes
        self._timepix.start()

    def setEpsilon(self, epsilon):
        logger.info("Setting epsilon {}".format(epsilon))
        self.__get_centroid_calculator().epsilon = epsilon

    def setMinSamples(self, min_samples):
        logger.info("Setting samples {}".format(min_samples))
        self.__get_centroid_calculator().min_samples = min_samples

    def setTotThreshold(self, tot_threshold):
        logger.info("Setting Tot threshold {}".format(tot_threshold))
        self.__get_centroid_calculator().tot_threshold = tot_threshold

    def __get_centroid_calculator(self):
        return self._timepix[0].acquisition.centroid_calculator

    def __get_packet_processor(self):
        return self._timepix[0].acquisition.packet_processor

    def startPacketProcessorOutputQueueSizeTimer(self):
        queue_size_update_timer = QtCore.QTimer()
        queue_size_update_timer.timeout.connect(
            self.updatePacketProcessorOutputQueueSize
        )
        queue_size_update_timer.start(500)

    def updatePacketProcessorOutputQueueSize(self):
        queue_size = -1
        if (
            platform.system() != "Darwin"
        ):  # qsize does not work for MacOS, see: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue.qsize
            packet_processor = self._timepix[0].acquisition.getStage(2)
            queue_size = packet_processor.outputQueue.qsize()
        self._config_panel.proctab.queue_size_changed.emit(queue_size)
        if (
            queue_size > QUEUE_SIZE_WARNING_LIMIT
            and not self.queue_size_warning_displayed
        ):
            self.show_slow_processing_warning_sig.emit(queue_size)
            self.queue_size_warning_displayed = True
        elif (
            queue_size < QUEUE_SIZE_WARNING_LIMIT and self.queue_size_warning_displayed
        ):
            self.queue_size_warning_displayed = False

    def show_slow_processing_warning(self, queue_size):
        QtGui.QMessageBox.warning(
            self,
            "Slow processing - Centroiding lags behind.",
            QUEUE_SIZE_WARNING_TEXT.format(QUEUE_SIZE_WARNING_LIMIT, queue_size),
        )

    def startPacketProcessorOutputQueueSizeTimer(self):
        queue_size_update_timer = QtCore.QTimer()
        queue_size_update_timer.timeout.connect(self.updatePacketProcessorOutputQueueSize)
        queue_size_update_timer.start(500)

    def show_slow_processing_warning(self, queue_size):
        QtGui.QMessageBox.warning(
            self, "Slow processing - Centroiding lags behind.", 
            QUEUE_SIZE_WARNING_TEXT.format(QUEUE_SIZE_WARNING_LIMIT, queue_size)
        )

    def connectSignals(self):
        self.actionLaunchPostProcessing.triggered.connect(self.launchPostProcessing)
        self.actionTimepixSetupPlotsPanel.triggered.connect(
            self.launchTimepixSetupPlotsPanel
        )

        self.editPixelMask.setDisabled(
            True
        )  # Disabled until a configuration file has been loaded
        self.editPixelMask.triggered.connect(self.launchEditPixelMask)

        self._config_panel.viewtab.updateRateChange.connect(self.onDisplayUpdate)
        self._config_panel.viewtab.eventCountChange.connect(self.onEventCountUpdate)
        self._config_panel.viewtab.frameTimeChange.connect(self.onFrameTimeUpdate)
        self._config_panel.acqtab.biasVoltageChange.connect(self.onBiasVoltageUpdate)
        self._config_panel.acqtab.sophy_config.textChanged.connect(
            self.__load_sophy_config_file
        )

        self._config_panel.acqtab.fine_threshold.editingFinished.connect(
            lambda: self.setFineThreshold(
                self._config_panel.acqtab.fine_threshold.value()
            )
        )
        self._config_panel.acqtab.coarse_threshold.editingFinished.connect(
            lambda: self.setCoarseThreshold(
                self._config_panel.acqtab.coarse_threshold.value()
            )
        )

        self.fineThresholdUpdate.connect(
            self._config_panel.acqtab.fine_threshold.setValue
        )
        self.coarseThresholdUpdate.connect(
            self._config_panel.acqtab.coarse_threshold.setValue
        )
        self._config_panel.viewtab.modeChange.connect(self.onModeChange)
        self.displayNow.connect(self._tof_panel.displayTof)
        self.onPixelToF.connect(self._tof_panel.onEvent)
        self.onCentroid.connect(self._tof_panel.onBlob)
        self.clearNow.connect(self._tof_panel.clearTof)
        self._tof_panel.roiUpdate.connect(self.onRoiChange)
        self._tof_panel.displayRoi.connect(self.addViewWidget)

        self.displayNow.connect(self._overview_panel.plotData)

        self.onPixelToA.connect(self._overview_panel.onToA)
        self.onPixelToF.connect(self._overview_panel.onEvent)
        self.onCentroid.connect(self._overview_panel.onCentroid)
        self.clearNow.connect(self._overview_panel.clearData)
        self.modeChange.connect(self._overview_panel.modeChange)

        self._config_panel.start_acq.clicked.connect(self.start_recording)
        self._config_panel.end_acq.clicked.connect(self.stop_recording)

        self._config_panel.viewtab.resetPlots.connect(self.clearNow.emit)
        self._config_panel.proctab.eventWindowChanged.connect(self.setEventWindow)

        self._config_panel.proctab.numberProcessesChanged.connect(
            self.setNumberProcesses
        )
        self._config_panel.proctab.triggersProcessedChanged.connect(
            self.setTriggersProcessed
        )
        self._config_panel.proctab.triggersProcessedChanged.connect(
            self._overview_panel.setTriggersProcessed
        )
        self._config_panel.proctab.epsilonChanged.connect(self.setEpsilon)
        self._config_panel.proctab.samplesChanged.connect(self.setMinSamples)
        self._config_panel.proctab.totThresholdChanged.connect(self.setTotThreshold)

        self.onRaw.connect(self._config_panel.fileSaver.onRaw)
        self.onPixelToA.connect(self._config_panel.fileSaver.onToa)
        self.onPixelToF.connect(self._config_panel.fileSaver.onTof)
        self.onCentroid.connect(self._config_panel.fileSaver.onCentroid)

        self._statusUpdate = GenericThread(self.statusUdate)
        self.updateStatusSignal.connect(
            lambda msg: self.statusbar.showMessage(msg, 5000)
        )

        self.start_acq_sig.connect(self.start_recording)
        self.stop_acq_sig.connect(self.stop_recording)

        self.show_slow_processing_warning_sig.connect(self.show_slow_processing_warning)

        self._api_server = GenericThread(self.api_server)

    def launchPostProcessing(self):
        self._timepix.stop()
        dialog = PostProcessing()
        dialog.exec_()
        self._timepix.start()

    def launchEditPixelMask(self):
        panel = EditPixelMaskPanel(self._timepix[0].config, self)

        self.onPixelToA.connect(panel.onToaData)
        self.onPixelToF.connect(panel.onTofData)
        self.onCentroid.connect(panel.onCentroidData)

        panel.onCloseEvent.connect(self.__load_sophy_config)

        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, panel)
        panel.setFloating(True)

    def launchTimepixSetupPlotsPanel(self):
        self._timepix_setup_plots_panel = TimepixSetupPlotsPanel(self)
        self.onCentroid.connect(self._timepix_setup_plots_panel.on_centroid)
        self.onPixelToF.connect(self._timepix_setup_plots_panel.on_event)
        self.addDockWidget(
            QtCore.Qt.RightDockWidgetArea, self._timepix_setup_plots_panel
        )
        self._timepix_setup_plots_panel.setFloating(True)

    def onBiasVoltageUpdate(self, value):
        logger.info("Bias Voltage changed to {} V".format(value))
        self._timepix.biasVoltage = value

    def onDisplayUpdate(self, value):
        logger.info("Display rate changed to {} s".format(value))
        self._display_rate = value

    def onEventCountUpdate(self, value):
        self._event_max = value
        self._current_event_count = 0

    def onFrameTimeUpdate(self, value):
        logger.info("Frame time set to {} s".format(value))
        self._frame_time = value

    def onModeChange(self, value):
        logger.info("Viewer mode changed to {}".format(value))
        self._current_mode = value
        if self._current_mode is ViewerMode.TOA:
            # Hide TOF panel
            self._dock_tof.hide()
            for k, view in self._view_widgets.items():
                view.hide()

        elif self._current_mode in (
            ViewerMode.TOF,
            ViewerMode.Centroid,
        ):
            # Show it
            self._dock_tof.show()
            for k, view in self._view_widgets.items():
                view.show()
        self.switchToMode()

        self.modeChange.emit(value)

    def onData(self, data_type, event):

        # if self._event_max != -1 and self._current_event_count > self._event_max:
        #     self.clearNow.emit()
        #     self._current_event_count = 0

        # event_shots = event[4]
        check_update = time.time()

        # if data_type in (MessageType.PixelData,):
        #     self.clearNow.emit()

        if self._current_mode is ViewerMode.TOA:
            if (
                self._frame_time >= 0
                and (check_update - self._last_frame) > self._frame_time
            ):
                self.clearNow.emit()
                self._last_frame = time.time()

        if self._current_mode in (
            ViewerMode.TOF,
            ViewerMode.Centroid,
        ) and data_type in (
            MessageType.EventData,
            MessageType.CentroidData,
        ):
            event_shots = event[0]

            if self._event_max != -1 and self._current_event_count > self._event_max:
                self.clearNow.emit()
                self._current_event_count = 0

            try:
                num_events = event_shots.max() - event_shots.min() + 1
            except ValueError:
                logger.warning("Events has no identity {}".format(event_shots))
                return
            self._current_event_count += num_events

        if data_type is MessageType.RawData:
            self.onRaw.emit(event)
        elif data_type is MessageType.PixelData:
            logger.debug("RAW: {}".format(event))
            self.onPixelToA.emit(event)
        elif data_type is MessageType.EventData:
            logger.debug("TOF: {}".format(event))
            self.onPixelToF.emit(event)
        elif data_type is MessageType.CentroidData:
            logger.debug("CENTROID: {}".format(event))
            self.onCentroid.emit(event)

        # if data_type in (MessageType.PixelData,):
        #     self.displayNow.emit()

        if (check_update - self._last_update) > self._display_rate:
            self.displayNow.emit()
            # self.displayNow.emit()
            self._last_update = time.time()

    def start_recording(self):
        self.clearNow.emit()
        path = self._config_panel.acqtab.path_name.text()
        if len(path) == 0:
            path = "./"  # for raw2disk to recognise it as a filename
        fName = f"{self._config_panel.acqtab.file_prefix.text()}"
        self._fileName = os.path.join(path, fName)
        path = self._config_panel.acqtab.get_path()

        self._timepix._spidr.resetTimers()
        self._timepix._spidr.restartTimers()
        time.sleep(1)  # give camera time to reset timers

        self._timepix._timepix_devices[0].start_recording(path)

        # setup GUI
        self._config_panel.start_acq.setStyleSheet("QPushButton {color: red;}")
        self._config_panel.start_acq.setEnabled(False)
        self._config_panel.end_acq.setEnabled(True)
        self._config_panel.start_acq.setText("Recording")
        self._config_panel._in_acq = True
        self._config_panel._elapsed_time.restart()

    def stop_recording(self):
        self._timepix._timepix_devices[0].stop_recording()

        # update GUI
        self._config_panel.start_acq.setStyleSheet("QPushButton {color: black;}")
        self._config_panel.start_acq.setEnabled(True)
        self._config_panel.end_acq.setEnabled(False)
        self._config_panel.start_acq.setText("Start Recording")
        self._config_panel._in_acq = False

    def addViewWidget(self, name, start, end):
        if name in self._view_widgets:
            QtGui.QMessageBox.warning(
                self, "Roi name", "Roi display of name '{}' already exists".format(name)
            )
            return
        else:
            dock_view = QtGui.QDockWidget("Display {}".format(name), self)
            blob_view = BlobView(
                start=start, end=end, parent=self, current_mode=self._current_mode
            )
            dock_view.setWidget(blob_view)
            self._view_widgets[name] = dock_view
            self.displayNow.connect(blob_view.plotData)
            self.onPixelToA.connect(blob_view.onToA)
            self.onPixelToF.connect(blob_view.onEvent)
            self.onCentroid.connect(blob_view.onCentroid)
            self.clearNow.connect(blob_view.clearData)
            self.modeChange.connect(blob_view.modeChange)
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock_view)

    def __load_sophy_config(self, config: SophyConfig):
        self.__load_sophy_config_file(config.filename)

    def __load_sophy_config_file(self, config_filename):
        if config_filename is not None and config_filename != "":
            self._timepix.stop()

            try:
                self._timepix[0].setConfigClass(pymepix.config.SophyConfig)
                self._timepix[0].loadConfig(config_filename)
                self.editPixelMask.setDisabled(False)
            except FileNotFoundError:
                QtGui.QMessageBox.warning(
                    None,
                    "Sophy config file not found",
                    f"File with name {config_filename} not found",
                    QtGui.QMessageBox.Ok,
                    QtGui.QMessageBox.Ok,
                )

            self.coarseThresholdUpdate.emit(self._timepix[0].Vthreshold_coarse)
            self.fineThresholdUpdate.emit(self._timepix[0].Vthreshold_fine)

            self._timepix.start()

            self.clearNow.emit()

    def onRoiChange(self, name, start, end):
        logger.debug("ROICHANGE", name, start, end)
        if name in self._view_widgets:
            logger.debug("FOUND WIDGET", name, start, end)
            self._view_widgets[name].widget().onRegionChange(start, end)
        else:
            logger.debug(
                "Widget for {} does not exist",
            )

    def setupWindow(self):
        self._tof_panel = TimeOfFlightPanel()
        self._config_panel = DaqConfigPanel()
        self._overview_panel = BlobView()
        self._dock_tof = QtWidgets.QDockWidget("Time of Flight", self)
        self._dock_tof.setFeatures(
            QtWidgets.QDockWidget.DockWidgetMovable
            | QtWidgets.QDockWidget.DockWidgetFloatable
        )
        self._dock_tof.setWidget(self._tof_panel)
        self._dock_config = QtWidgets.QDockWidget("Daq Configuration", self)
        self._dock_config.setFeatures(
            QtWidgets.QDockWidget.DockWidgetMovable
            | QtWidgets.QDockWidget.DockWidgetFloatable
        )
        self._dock_config.setWidget(self._config_panel)
        self._dock_overview = QtWidgets.QDockWidget("Overview", self)
        self._dock_overview.setFeatures(
            QtWidgets.QDockWidget.DockWidgetMovable
            | QtWidgets.QDockWidget.DockWidgetFloatable
        )
        self._dock_overview.setWidget(self._overview_panel)

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self._dock_tof)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self._dock_config)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self._dock_overview)


def main():
    parser = argparse.ArgumentParser(description="Pymepix Viewer Application")

    parser.add_argument(
        "-i",
        "--ip",
        dest="ip",
        type=str,
        default=cfg.default_cfg["timepix"]["tpx_ip"],
        help="IP address of Timepix",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    app = QtWidgets.QApplication([])

    config = PymepixDAQ(args.ip)
    app.lastWindowClosed.connect(config.onClose)
    config.show()

    app.exec_()


if __name__ == "__main__":
    main()

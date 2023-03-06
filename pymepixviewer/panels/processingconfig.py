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
from functools import partial

from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

from .ui.processingconfigui import Ui_Form

"""Conversion factor from the GUI input (µs) to match actual data given in seconds """
EVENT_WINDOW_FACTOR = 1e6


class ProcessingConfig(QtWidgets.QWidget, Ui_Form):
    eventWindowChanged = QtCore.pyqtSignal(float, float)
    totThresholdChanged = QtCore.pyqtSignal(int)
    triggersProcessedChanged = QtCore.pyqtSignal(int)
    numberProcessesChanged = QtCore.pyqtSignal(int)
    samplesChanged = QtCore.pyqtSignal(int)
    epsilonChanged = QtCore.pyqtSignal(float)
    queue_size_changed = QtCore.pyqtSignal(int)
    cs_minSamples_changed = QtCore.pyqtSignal(int)
    cs_maxToFdist_changed = QtCore.pyqtSignal(float)
    cs_ToToffset_changed = QtCore.pyqtSignal(float)
    clustering_changed_signal = QtCore.pyqtSignal(bool)

    dbscan_centroiding = True

    def __init__(self, parent=None):
        super(ProcessingConfig, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)

        self.setupLines()
        self.setupSignals()

    def setupLines(self):
        self.min_event_window.setValidator(QtGui.QDoubleValidator(self))
        self.max_event_window.setValidator(QtGui.QDoubleValidator(self))
        self.number_processes.setValidator(QtGui.QIntValidator(self))

    def init_event_window(self, event_window):
        min_event_window, max_event_window = event_window
        self.min_event_window.setText(f"{(min_event_window * EVENT_WINDOW_FACTOR):.2f}")
        self.max_event_window.setText(f"{(max_event_window * EVENT_WINDOW_FACTOR):.2f}")

    def tofEventWindow(self):
        min_value = float(self.min_event_window.text()) / EVENT_WINDOW_FACTOR
        self.__save_setting("mineventwindow", min_value)
        max_value = float(self.max_event_window.text()) / EVENT_WINDOW_FACTOR
        self.__save_setting("maxeventwindow", max_value)
        self.eventWindowChanged.emit(min_value, max_value)

    def __number_processes_enter_pressed(self):
        number_of_processes = int(self.number_processes.text())
        self.__save_setting("number_processes", number_of_processes)
        self.numberProcessesChanged.emit(number_of_processes)

    def centroiding_changed(self):
        if self.dbscan_centroiding:
            self.dbscan_group.setChecked(False)
            self.cstream_group.setChecked(True)
            self.dbscan_centroiding = False
            self.clustering_changed_signal.emit(False)
        else:
            self.dbscan_group.setChecked(True)
            self.cstream_group.setChecked(False)
            self.dbscan_centroiding = True
            self.clustering_changed_signal.emit(True)

    def setupSignals(self):
        # Configuration entries for packet processor
        self.min_event_window.returnPressed.connect(self.tofEventWindow)
        self.max_event_window.returnPressed.connect(self.tofEventWindow)

        self.dbscan_group.clicked.connect(self.centroiding_changed)
        self.cstream_group.clicked.connect(self.centroiding_changed)

        # Configuration entries for centroiding
        self.triggers_processed.valueChanged[int].connect(
            self.triggersProcessedChanged.emit
        )
        self.triggers_processed.valueChanged[int].connect(
            partial(self.__save_setting, "triggers_processed")
        )
        self.min_samples.valueChanged[int].connect(self.samplesChanged.emit)
        self.min_samples.valueChanged[int].connect(
            partial(self.__save_setting, "min_samples")
        )
        self.epsilon.valueChanged[float].connect(self.epsilonChanged.emit)
        self.epsilon.valueChanged[float].connect(
            partial(self.__save_setting, "epsilon")
        )
        self.tot_threshold.valueChanged[int].connect(self.totThresholdChanged.emit)
        self.tot_threshold.valueChanged[int].connect(
            partial(self.__save_setting, "tot_threshold")
        )

        self.cstream_tot_offset.valueChanged[float].connect(self.cs_ToToffset_changed.emit)
        self.cstream_tot_offset.valueChanged[float].connect(
            partial(self.__save_setting, "cstream_tot_offset")
        )

        self.cstream_max_tof_dist.valueChanged[float].connect(self.cs_maxToFdist_changed.emit)
        self.cstream_max_tof_dist.valueChanged[float].connect(
            partial(self.__save_setting, "cstream_max_tof_dist")
        )

        self.cstream_min_samples.valueChanged[int].connect(self.cs_minSamples_changed.emit)
        self.cstream_min_samples.valueChanged[int].connect(
            partial(self.__save_setting, "cstream_min_samples")
        )

        self.number_processes.returnPressed.connect(
            self.__number_processes_enter_pressed
        )

        self.queue_size_changed.connect(self.lcd_queue_size.display)


    def read_settings(self):
        """Read settings using QSettings. This method has to be called after all signals are connected to gurantee
        accordance among the values."""
        settings = QtCore.QSettings()

        settings.beginGroup("processingconfig")
        triggers_processed = settings.value("triggers_processed", 1, type=int)
        self.triggers_processed.setValue(triggers_processed)
        min_samples = settings.value("min_samples", 3, type=int)
        self.min_samples.setValue(min_samples)
        epsilon = settings.value("epsilon", 2.0, type=float)
        self.epsilon.setValue(epsilon)
        tot_threshold = settings.value("tot_threshold", 0, type=int)
        self.tot_threshold.setValue(tot_threshold)

        cstream_min_samples = settings.value("cstream_min_samples", 3, type=int)
        self.cstream_min_samples.setValue(cstream_min_samples)
        cstream_max_tof_dist = settings.value("cstream_max_tof_dist", 5e-8, type=float)
        self.cstream_max_tof_dist.setValue(cstream_max_tof_dist)
        cstream_tot_offset = settings.value("cstream_tot_offset", 0.5, type=float)
        self.cstream_tot_offset.setValue(cstream_tot_offset)

        number_processes = settings.value("number_processes", 4, type=str)
        self.number_processes.setText(number_processes)
        self.number_processes.returnPressed.emit()

        event_window = settings.value(
            "mineventwindow", 0.0, type=float
        ), settings.value("maxeventwindow", 10_000 / EVENT_WINDOW_FACTOR, type=float)
        self.init_event_window(event_window)
        settings.endGroup()

    def __save_setting(self, key, value):
        settings = QtCore.QSettings()

        settings.beginGroup("processingconfig")
        settings.setValue(key, value)
        settings.endGroup()

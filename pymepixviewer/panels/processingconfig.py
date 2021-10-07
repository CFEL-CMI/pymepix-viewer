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

from pyqtgraph.Qt import QtCore, QtGui

from .ui.processingconfigui import Ui_Form


EVENT_WINDOW_FACTOR = 1E6


class ProcessingConfig(QtGui.QWidget, Ui_Form):
    eventWindowChanged = QtCore.pyqtSignal(float, float)
    totThresholdChanged = QtCore.pyqtSignal(int)
    triggersProcessedChanged = QtCore.pyqtSignal(int)
    numberProcessesChanged = QtCore.pyqtSignal(int)
    samplesChanged = QtCore.pyqtSignal(int)
    epsilonChanged = QtCore.pyqtSignal(float)
    queue_size_changed = QtCore.pyqtSignal(int)

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
        self.min_event_window.setText(f'{(min_event_window * EVENT_WINDOW_FACTOR):.2f}')
        self.max_event_window.setText(f'{(max_event_window * EVENT_WINDOW_FACTOR):.2f}')

    def tofEventWindow(self):
        min_value = float(self.min_event_window.text()) / EVENT_WINDOW_FACTOR
        self.__save_setting('mineventwindow', min_value)
        max_value = float(self.max_event_window.text()) / EVENT_WINDOW_FACTOR
        self.__save_setting('maxeventwindow', max_value)
        self.eventWindowChanged.emit(min_value, max_value)

    def __number_processes_enter_pressed(self):
        number_of_processes = int(self.number_processes.text())
        self.__save_setting('number_processes', number_of_processes)
        self.numberProcessesChanged.emit(number_of_processes)
        
    def setupSignals(self):
        # Configuration entries for packet processor
        self.min_event_window.returnPressed.connect(self.tofEventWindow)
        self.max_event_window.returnPressed.connect(self.tofEventWindow)
        
        # Configuration entries for centroiding
        self.triggers_processed.valueChanged[int].connect(self.triggersProcessedChanged.emit)
        self.triggers_processed.valueChanged[int].connect(partial(self.__save_setting, 'triggers_processed'))
        self.min_samples.valueChanged[int].connect(self.samplesChanged.emit)
        self.min_samples.valueChanged[int].connect(partial(self.__save_setting, 'min_samples'))
        self.epsilon.valueChanged[float].connect(self.epsilonChanged.emit)
        self.epsilon.valueChanged[float].connect(partial(self.__save_setting, 'epsilon'))
        self.tot_threshold.valueChanged[int].connect(self.totThresholdChanged.emit)
        self.tot_threshold.valueChanged[int].connect(partial(self.__save_setting, 'tot_threshold'))
        self.number_processes.returnPressed.connect(self.__number_processes_enter_pressed)

        self.queue_size_changed.connect(self.lcd_queue_size.display)

    def read_settings(self):
        """ Read settings using QSettings. This method has to be called after all signals are connected to gurantee
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

        number_processes = settings.value("number_processes", 4, type=str)
        self.number_processes.setText(number_processes)
        self.number_processes.returnPressed.emit()

        event_window = settings.value("mineventwindow", 0.0, type=float), settings.value("maxeventwindow", 10_000 / EVENT_WINDOW_FACTOR, type=float)
        self.init_event_window(event_window)
        settings.endGroup()

    def __save_setting(self, key, value):
        settings = QtCore.QSettings()

        settings.beginGroup("processingconfig")
        settings.setValue(key, value)
        settings.endGroup()


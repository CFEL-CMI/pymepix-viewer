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

from pyqtgraph.Qt import QtCore, QtGui

from .ui.processingconfigui import Ui_Form


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
        self.min_event_window.setValidator(QtGui.QIntValidator(self))
        self.max_event_window.setValidator(QtGui.QDoubleValidator(self))
        self.number_processes.setValidator(QtGui.QIntValidator(self))

    def tofEventWindow(self):
        min_value = float(self.min_event_window.text()) * 1E-6
        max_value = float(self.max_event_window.text()) * 1E-6
        self.eventWindowChanged.emit(min_value, max_value)

    def __number_processes_enter_pressed(self):
        self.numberProcessesChanged.emit(int(self.number_processes.text()))
        
    def setupSignals(self):
        # Configuration entries for packet processor
        # TODO: Fix those!!!
        self.min_event_window.returnPressed.connect(self.tofEventWindow)
        self.max_event_window.returnPressed.connect(self.tofEventWindow)
        
        # Configuration entries for centroiding
        self.triggers_processed.valueChanged[int].connect(self.triggersProcessedChanged.emit)
        self.min_samples.valueChanged[int].connect(self.samplesChanged.emit)
        self.epsilon.valueChanged[float].connect(self.epsilonChanged.emit)
        self.tot_threshold.valueChanged[int].connect(self.totThresholdChanged.emit)
        self.number_processes.returnPressed.connect(self.__number_processes_enter_pressed)

        self.queue_size_changed.connect(self.lcd_queue_size.display)


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
import logging
import os
import threading
import time
from threading import Thread

from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

from .ui.daqcontrolui import Ui_Form

class DaqControlPanel(QtWidgets.QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(DaqControlPanel, self).__init__(parent)

        self.setupUi(self)

        self._in_acq = False

        self._elapsed_time_thread = QtCore.QTimer()
        self._elapsed_time = QtCore.QElapsedTimer()
        self._elapsed_time_thread.timeout.connect(self.updateTimer)
        self._elapsed_time_thread.start(1000)


    def updateTimer(self):
        if self._in_acq:
            seconds = self._elapsed_time.elapsed() / 1000
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)

            self.elapsed_time_s.display(int(round(s)))
            self.elapsed_time_m.display(int(round(m)))
            self.elapsed_time_h.display(h)
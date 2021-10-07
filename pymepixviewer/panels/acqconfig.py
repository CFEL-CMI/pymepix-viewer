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

import glob
import logging
import os
import time
from functools import partial

import numpy as np
from pyqtgraph.Qt import QtCore, QtGui

from ..core.datatypes import ViewerMode
from .ui.acqconfigui import Ui_Form

logger = logging.getLogger(__name__)


class AcquisitionConfig(QtGui.QWidget, Ui_Form):

    biasVoltageChange = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(AcquisitionConfig, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)

        self._current_mode = ViewerMode.TOA
        self.connectSignals()

        self.__read_settings()

    def connectSignals(self):
        self.openpath.clicked.connect(self.openPath)
        self.open_sophy_config.clicked.connect(self.on_open_sophy_config)
        self.bias_voltage.valueChanged[int].connect(self.biasVoltageChange.emit)
        self.path_name.textChanged.connect(partial(self.__save_setting, "path"))
        self.file_prefix.textChanged.connect(partial(self.__save_setting, "prefix"))
        self.sophy_config.textChanged.connect(
            partial(self.__save_setting, "sophyconfig")
        )

        self.path_name.textChanged.connect(self.__updateFileIndex)
        self.file_prefix.textChanged.connect(self.__updateFileIndex)

    @staticmethod
    def __determine_current_file_index(path):
        files = np.sort(glob.glob(f"{path}*.raw"))
        if len(files) > 0:
            index = int(files[-1].split("_")[-2]) + 1
        else:
            index = 0
        return index

    def __determine_current_path(self):
        directory = self.path_name.text()
        if len(directory) == 0:
            directory = "./"  # for raw2disk to recognise it as a filename
        return os.path.join(directory, self.file_prefix.text())

    def __updateFileIndex(self, _text):
        index = self.__determine_current_file_index(self.__determine_current_path())
        self.startIndex.display(index)

    def get_path(self):
        path = self.__determine_current_path()
        index = self.__determine_current_file_index(path)

        path = f'{path}_{index:04d}_{time.strftime("%Y%m%d-%H%M")}.raw'
        self.startIndex.display(index)
        return path

    def openPath(self):
        directory = QtGui.QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            self.path_name.text(),
            QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks,
        )

        self.path_name.setText(directory)

    def on_open_sophy_config(self):
        config_file = QtGui.QFileDialog.getOpenFileName(
            self, "Select SoPhy configuration file", "/home", "SoPhy File (*.spx)"
        )[0]
        self.sophy_config.setText(config_file)

    def __read_settings(self):
        settings = QtCore.QSettings()

        settings.beginGroup("acqconfig")
        path = settings.value("path")
        self.path_name.setText(path)
        prefix = settings.value("prefix")
        self.file_prefix.setText(prefix)
        config_file = settings.value("sophyconfig")
        self.sophy_config.setText(config_file)
        settings.endGroup()

    def __save_setting(self, key, value):
        settings = QtCore.QSettings()

        settings.beginGroup("acqconfig")
        settings.setValue(key, value)
        settings.endGroup()

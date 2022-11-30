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
from pathlib import Path
from threading import Thread

import numpy as np
import pymepix as pymepix
from pyqtgraph.Qt import QtGui

from .ui.postprocessingui import Ui_Dialog

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

FILE_SEPARATOR = ";"
OUTPUT_FILE_EXTENSION = "hdf5"


class PostProcessing(QtGui.QDialog, Ui_Dialog):
    """
    User interface to access the post-processing functionality of pymepix. The UI allows the user to enter all the required
    parameters and to start the processing. The processing transforms raw data into processed HDF5 files, which provide also
    additional information like centroids.
    """

    def __init__(self, parent=None,
            cs_sensor_size=256,
            cs_min_cluster_size=3,
            cs_max_dist_tof=5e-8,
            cs_tot_offset=0.5,
            tot_threshold=25,
            epsilon=2,
            min_samples=3,
            triggers_processed=1,
            chunk_size_limit=6_500
    ):
        super(PostProcessing, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)

        self.processing_is_running = False
        self._close_allowed = True

        self.pushButtonBrowseInputFiles.clicked.connect(self.onBrowseInputFiles)
        self.pushButtonBrowseTimeWalkFile.clicked.connect(self.onBrowseTimeWalkFile)
        self.pushButtonBrowseTimeWalkFileCentroided.clicked.connect(
            self.onBrowseTimeWalkFileCentroided
        )
        self.pushButtonBrowseOutputDirectory.clicked.connect(
            self.onBrowseOutputDirectory
        )

        self.pushButtonStartProcessing.clicked.connect(self.onStartProcessing)

        #self.dbscan_rbutton
        #self.cstream_rbutton

        self.cs_sensor_size = cs_sensor_size
        self.cs_min_cluster_size = cs_min_cluster_size
        self.cs_max_dist_tof = cs_max_dist_tof
        self.cs_tot_offset = cs_tot_offset

        self.tot_threshold = tot_threshold
        self.epsilon = epsilon
        self.min_samples = min_samples
        self.triggers_processed = triggers_processed
        self.chunk_size_limit = chunk_size_limit

        integer_regex_validator = QRegExpValidator(QRegExp("[0-9]*"))
        float_regex_validator = QRegExpValidator(QRegExp("[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?"))

        self.lineEdit_cs_sensor_size.setValidator(integer_regex_validator);
        self.lineEdit_cs_min_cluster_size.setValidator(integer_regex_validator);
        self.lineEdit_cs_max_dist_tof.setValidator(float_regex_validator);
        self.lineEdit_cs_tot_offset.setValidator(float_regex_validator);

        self.lineEdit_tot_threshold.setValidator(integer_regex_validator);
        self.lineEdit_epsilon.setValidator(float_regex_validator);
        self.lineEdit_min_samples.setValidator(integer_regex_validator);
        self.lineEdit_chunk_size_limit.setValidator(integer_regex_validator);


        self.lineEdit_cs_sensor_size.setText(str(self.cs_sensor_size))
        self.lineEdit_cs_min_cluster_size.setText(str(self.cs_min_cluster_size))
        self.lineEdit_cs_max_dist_tof.setText(str(self.cs_max_dist_tof))
        self.lineEdit_cs_tot_offset.setText(str(self.cs_tot_offset))

        self.lineEdit_tot_threshold.setText(str(self.tot_threshold))
        self.lineEdit_epsilon.setText(str(self.epsilon))
        self.lineEdit_min_samples.setText(str(self.min_samples))
        self.lineEdit_chunk_size_limit.setText(str(self.chunk_size_limit))

        self.lineEdit_cs_sensor_size.returnPressed.connect(self.cs_sensor_size_enter)
        self.lineEdit_cs_min_cluster_size.returnPressed.connect(self.cs_min_cluster_size_enter)
        self.lineEdit_cs_max_dist_tof.returnPressed.connect(self.cs_max_dist_tof_enter)
        self.lineEdit_cs_tot_offset.returnPressed.connect(self.cs_tot_offset_enter)

        self.lineEdit_tot_threshold.returnPressed.connect(self.tot_threshold_enter)
        self.lineEdit_epsilon.returnPressed.connect(self.epsilon_enter)
        self.lineEdit_min_samples.returnPressed.connect(self.min_samples_enter)
        self.lineEdit_chunk_size_limit.returnPressed.connect(self.chunk_size_limit_enter)


    def cs_sensor_size_enter(self):
        self.cs_sensor_size = int(self.lineEdit_cs_sensor_size.text())
    def cs_min_cluster_size_enter(self):
        self.cs_min_cluster_size = int(self.lineEdit_cs_min_cluster_size.text())
    def cs_max_dist_tof_enter(self):
        self.cs_max_dist_tof = float(self.lineEdit_cs_max_dist_tof.text())
    def cs_tot_offset_enter(self):
        value = float(self.lineEdit_cs_tot_offset.text())
        if value > 1.0:
            value = 1.0
            self.lineEdit_cs_tot_offset.setText(str(1.0))
        self.cs_tot_offset = value
    def tot_threshold_enter(self):
        self.tot_threshold = int(self.lineEdit_tot_threshold.text())
    def epsilon_enter(self):
        self.epsilon = float(self.lineEdit_epsilon.text())
    def min_samples_enter(self):
        self.min_samples = int(self.lineEdit_min_samples.text())
    def chunk_size_limit_enter(self):
        self.chunk_size_limit = int(self.lineEdit_chunk_size_limit.text())

    def closeEvent(self, event):
        if self._close_allowed:
            super().closeEvent(event)
        else:
            QtGui.QMessageBox.warning(
                self,
                "The processing is still running",
                "This window can only be closed if the processing is finished.",
            )
            event.ignore()

    def onBrowseInputFiles(self):
        file_names, _ = QtGui.QFileDialog.getOpenFileNames(
            self,
            "Choose input file(s)",
            None,
            "All files (*.*);;RAW (*.raw)",
            "RAW (*.raw)",
        )
        self.lineEditInputFiles.setText(FILE_SEPARATOR.join(file_names))

    def onBrowseTimeWalkFile(self):
        file_name, _ = QtGui.QFileDialog.getOpenFileName(
            self,
            "Choose time walk file",
            None,
            "All files (*.*);;Numpy (*.npy)",
            "Numpy (*.npy)",
        )
        self.lineEditTimeWalkFile.setText(file_name)

    def onBrowseTimeWalkFileCentroided(self):
        file_name, _ = QtGui.QFileDialog.getOpenFileName(
            self,
            "Choose centroided time walk file",
            None,
            "All files (*.*);;Numpy (*.npy)",
            "Numpy (*.npy)",
        )
        self.lineEditTimeWalkFileCentroided.setText(file_name)

    def onBrowseOutputDirectory(self):
        output_directory = QtGui.QFileDialog.getExistingDirectory(
            self, "Choose output directory"
        )
        self.lineEditOutputDirectory.setText(output_directory)

    def updateProgressBar(self, progress):
        progress = int(
            (
                (self.files_completed / self.files_for_processing)
                + progress / self.files_for_processing
            )
            * 100
        )
        self.progressBar.setValue(progress)

    def onStartProcessing(self):
        if not self.processing_is_running:
            self.processing_thread = Thread(target=self.run_post_processing_threaded)
            self.processing_thread.start()
        else:
            self.pushButtonStartProcessing.setDisabled(True)
            self.pushButtonStartProcessing.setText("Stopping")
            self.setToolTip(
                "Stopping after currently processed file. This can still take a while!"
            )
            self.processing_is_running = False

    def __set_disabled_controls(self, disabled):
        self.pushButtonBrowseInputFiles.setDisabled(disabled)
        self.pushButtonBrowseOutputDirectory.setDisabled(disabled)
        self.pushButtonBrowseTimeWalkFile.setDisabled(disabled)
        self.pushButtonBrowseTimeWalkFileCentroided.setDisabled(disabled)

        self.lineEditInputFiles.setDisabled(disabled)
        self.lineEditOutputDirectory.setDisabled(disabled)
        self.lineEditTimeWalkFile.setDisabled(disabled)
        self.lineEditTimeWalkFileCentroided.setDisabled(disabled)

    def __check_timewalk_file(self, timewalk_file):
        """Check if the given timewalk file is valid. Valid means in this context only that the file exists and can be read using numpy as a one-dimensional array."""
        return (
            os.path.isfile(timewalk_file) and len(np.fromfile(timewalk_file).shape) == 1
        )

    def run_post_processing_threaded(self):
        self._close_allowed = False
        self.pushButtonStartProcessing.setText("Stop Processing")
        self.setToolTip(
            "Stop after currently processed file. This can still take a while!"
        )
        self.__set_disabled_controls(True)
        self.processing_is_running = True

        input_files = self.lineEditInputFiles.text().split(FILE_SEPARATOR)
        self.files_for_processing = len(input_files)
        self.files_completed = 0
        time_walk_file = self.lineEditTimeWalkFile.text()
        if len(time_walk_file) == 0:
            time_walk_file = None
        else:
            if not self.__check_timewalk_file(time_walk_file):
                QtGui.QMessageBox.warning(
                    self,
                    "The selected timewalk-file is not valid",
                    "Please select a valid timewalk-file or remove it completely.",
                )
                return
        time_walk_file_centroided = self.lineEditTimeWalkFileCentroided.text()
        if len(time_walk_file_centroided) == 0:
            time_walk_file_centroided = None
        else:
            if not self.__check_timewalk_file(time_walk_file):
                QtGui.QMessageBox.warning(
                    self,
                    "The selected centroided timewalk-file is not valid",
                    "Please select a valid centroided timewalk-file or remove it completely.",
                )
                return
        output_directory = self.lineEditOutputDirectory.text()
        clustering_args = {
            'tot_threshold' : self.tot_threshold,
            'epsilon' : self.epsilon,
            'min_samples' : self.min_samples,
            'triggers_processed' : self.triggers_processed,
            'chunk_size_limit' : self.chunk_size_limit,
            'cs_sensor_size' : self.cs_sensor_size,
            'cs_min_cluster_size' : self.cs_min_cluster_size,
            'cs_max_dist_tof' : self.cs_max_dist_tof,
            'cs_tot_offset' : self.cs_tot_offset,
        }


        for input_file in input_files:
            self.progressBar.setToolTip(f"Processing: {input_file}")
            if not self.processing_is_running:
                break
            output_file = (
                Path(output_directory)
                / f"{Path(input_file).stem}.{OUTPUT_FILE_EXTENSION}"
            )

            pymepix.run_post_processing(
                input_file,
                output_file,
                None,
                time_walk_file,
                time_walk_file_centroided,
                progress_callback=self.updateProgressBar,
                clustering_args=clustering_args,
                dbscan_clustering=self.dbscan_rbutton.isChecked()
            )
            self.files_completed += 1

        self.processing_is_running = False
        self.__set_disabled_controls(False)
        self.progressBar.setToolTip(None)
        self.pushButtonStartProcessing.setText("Start Processing")
        self.setToolTip(None)
        self.pushButtonStartProcessing.setDisabled(False)
        self._close_allowed = True

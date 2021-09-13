from threading import Thread

from pyqtgraph.Qt import QtCore, QtGui
from pathlib import Path

from .ui.postprocessingui import Ui_Dialog
import pymepix as pymepix


FILE_SEPARATOR = ';'
OUTPUT_FILE_EXTENSION = 'hdf5'

class PostProcessing(QtGui.QDialog, Ui_Dialog):
    
    def __init__(self, parent=None):
        super(PostProcessing, self).__init__(parent)
        
        # Set up the user interface from Designer.
        self.setupUi(self)

        self.processing_is_running = False

        self.pushButtonBrowseInputFiles.clicked.connect(self.onBrowseInputFiles)
        self.pushButtonBrowseTimeWalkFile.clicked.connect(self.onBrowseTimeWalkFile)
        self.pushButtonBrowseTimeWalkFileCentroided.clicked.connect(self.onBrowseTimeWalkFileCentroided)
        self.pushButtonBrowseOutputDirectory.clicked.connect(self.onBrowseOutputDirectory)

        self.pushButtonStartProcessing.clicked.connect(self.onStartProcessing)

    def onBrowseInputFiles(self):
        file_names, _ = QtGui.QFileDialog.getOpenFileNames(self, 'Choose input file(s)', None, 'All files (*.*);;RAW (*.raw)', 'RAW (*.raw)')
        self.lineEditInputFiles.setText(FILE_SEPARATOR.join(file_names))

    def onBrowseTimeWalkFile(self):
        file_name, _ = QtGui.QFileDialog.getOpenFileName(self, 'Choose time walk file', None, 'All files (*.*);;Numpy (*.npy)', 'Numpy (*.npy)')
        self.lineEditTimeWalkFile.setText(file_name)

    def onBrowseTimeWalkFileCentroided(self):
        file_name, _ = QtGui.QFileDialog.getOpenFileName(self, 'Choose centroided time walk file', None, 'All files (*.*);;Numpy (*.npy)', 'Numpy (*.npy)')
        self.lineEditTimeWalkFileCentroided.setText(file_name)

    def onBrowseOutputDirectory(self):
        output_directory = QtGui.QFileDialog.getExistingDirectory(self, 'Choose output directory')
        self.lineEditOutputDirectory.setText(output_directory)

    def updateProgressBar(self, progress):
        progress = int(((self.files_completed / self.files_for_processing) + progress / self.files_for_processing) * 100)
        self.progressBar.setValue(progress)

    def onStartProcessing(self):
        if not self.processing_is_running:
            self.processing_thread = Thread(target = self.run_post_processing_threaded)
            self.processing_thread.start()
        else:
            self.processing_is_running = False
        # thread.join()

    def __set_disabled_controls(self, disabled):
        self.pushButtonBrowseInputFiles.setDisabled(disabled)
        self.pushButtonBrowseOutputDirectory.setDisabled(disabled)
        self.pushButtonBrowseTimeWalkFile.setDisabled(disabled)
        self.pushButtonBrowseTimeWalkFileCentroided.setDisabled(disabled)

        self.lineEditInputFiles.setDisabled(disabled)
        self.lineEditOutputDirectory.setDisabled(disabled)
        self.lineEditTimeWalkFile.setDisabled(disabled)
        self.lineEditTimeWalkFileCentroided.setDisabled(disabled)
    

    def run_post_processing_threaded(self):
        self.pushButtonStartProcessing.setText('Stop Processing')
        self.__set_disabled_controls(True)
        self.processing_is_running = True

        input_files = self.lineEditInputFiles.text().split(FILE_SEPARATOR)
        self.files_for_processing = len(input_files)
        self.files_completed = 0
        time_walk_file = self.lineEditTimeWalkFile.text()
        if len(time_walk_file) == 0:
            time_walk_file = None
        time_walk_file_centroided = self.lineEditTimeWalkFileCentroided.text()
        if len(time_walk_file_centroided) == 0:
            time_walk_file_centroided = None

        output_directory = self.lineEditOutputDirectory.text()
        
        for input_file in input_files:
            if not self.processing_is_running:
                break
            output_file = f'{output_directory}/{Path(input_file).stem}.{OUTPUT_FILE_EXTENSION}'
            pymepix.run_post_processing(input_file, output_file, None, time_walk_file, time_walk_file_centroided, progress_callback=self.updateProgressBar)
            self.files_completed += 1

        self.processing_is_running = False
        self.__set_disabled_controls(False)
        self.pushButtonStartProcessing.setText('Start Processing')
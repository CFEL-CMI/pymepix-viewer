import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from sklearn import cluster

from.ui.timepixsetupplotspanelui import Ui_DockWidget

class TimepixSetupPlotsPanel(QtGui.QDockWidget, Ui_DockWidget):

    def __init__(self, parent=None):
        super(TimepixSetupPlotsPanel, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)

        self.__size_histogram_max = 0
        self.__init_event_buffers()
        self.__init_centroided_buffers()


        self.toFRangeMinimumLineEdit.setValidator(QtGui.QIntValidator(self))
        self.toFRangeMaximumLineEdit.setValidator(QtGui.QIntValidator(self))
        self.toTRangeMinimumLineEdit.setValidator(QtGui.QIntValidator(self))
        self.toTRangeMaximumLineEdit.setValidator(QtGui.QIntValidator(self))
        self.numberPacketsLineEdit.setValidator(QtGui.QIntValidator(self))
        # TODO: ToF Range input fields (or alternatively the settings form the tof view)
        # TODO: Longer time for integration including settings for this


        # Event Data Plots Preparation
        self._event_data_tot_plt = pg.PlotDataItem()
        self.plt_event_data_histogram_tot.addItem(self._event_data_tot_plt)
        self.plt_event_data_histogram_tot.setLabel('bottom', text='Time over Threshold', units='ns')
        self.plt_event_data_histogram_tot.setLabel('left', text='Count')

        self._event_data_2d_histogram_tof_tot_data = pg.ImageItem()
        self.plt_event_data_2d_histogram_tof_tot.addItem(self._event_data_2d_histogram_tof_tot_data)
        self.plt_event_data_2d_histogram_tof_tot.setLabel('bottom', text='Time of Flight')
        self.plt_event_data_2d_histogram_tof_tot.setLabel('left', text='Time over Threshold')


        # Centroided Data Plots Preparation
        self._centroided_data_tot_plt = pg.PlotDataItem()
        self.plt_centroided_data_histogram_tot.addItem(self._centroided_data_tot_plt)
        self.plt_centroided_data_histogram_tot.setLabel('bottom', text='Mean Time over Threshold', units='ns')
        self.plt_centroided_data_histogram_tot.setLabel('left', text='Count')

        self._centroided_data_2d_histogram_tof_tot_data = pg.ImageItem()
        self.plt_centroided_data_2d_histogram_tof_tot.addItem(self._centroided_data_2d_histogram_tof_tot_data)
        self.plt_centroided_data_2d_histogram_tof_tot.setLabel('bottom', text='Time of Flight')
        self.plt_centroided_data_2d_histogram_tof_tot.setLabel('left', text='Mean Time over Threshold')

        self._centroided_data_cluster_size_data = pg.PlotDataItem()
        self.plt_centroided_data_histogram_size.addItem(self._centroided_data_cluster_size_data)
        self.plt_centroided_data_histogram_size.setLabel('bottom', text='Cluster Size')
        self.plt_centroided_data_histogram_size.setLabel('left', text='Count')

    def __init_event_buffers(self):
        self.__packet_counter_events = 0
        self.__event_tof = []
        self.__event_tot = []

    def __init_centroided_buffers(self):
        self.__packet_counter_centroided = 0
        self.__centroided_tof = []
        self.__centroided_tot = []
        self.__centroided_cluster_size = []

    def __update_event_buffers(self, tof, tot):
        if (self.__packet_counter_events >= int(self.numberPacketsLineEdit.text())):
            self.__init_event_buffers()
        self.__event_tof = np.concatenate((self.__event_tof, tof))
        self.__event_tot = np.concatenate((self.__event_tot, tot))
        self.__packet_counter_events += 1

    def __update_centroided_buffers(self, tof, tot, cluster_size):
        if (self.__packet_counter_centroided >= int(self.numberPacketsLineEdit.text())):
            self.__init_centroided_buffers()
        self.__centroided_tof = np.concatenate((self.__centroided_tof, tof))
        self.__centroided_tot = np.concatenate((self.__centroided_tot, tot))
        self.__centroided_cluster_size = np.concatenate((self.__centroided_cluster_size, cluster_size))

        self.__packet_counter_centroided += 1

    def __update_tot_histogram(self, tot, plt):
        y, x = np.histogram(tot, range(int(self.toTRangeMinimumLineEdit.text()), int(self.toTRangeMaximumLineEdit.text()) + 25, 25))
        plt.setData(x=x, y=y, stepMode='center', fillLevel=0, brush=(0, 0, 255, 150))

    def __update_cluster_size_histogram(self, cluster_size, plt):
        self.__size_histogram_max = max(self.__size_histogram_max, cluster_size.max())
        y, x = np.histogram(cluster_size, np.linspace(0, self.__size_histogram_max, self.__size_histogram_max, dtype=np.float))
        plt.setData(x=x, y=y, stepMode='center', fillLevel=0, brush=(0, 0, 255, 150))

    def __update_2d_histogram_tof_tot(self, tof, tot, plt):
        tot_bins = range(int(self.toTRangeMinimumLineEdit.text()), int(self.toTRangeMaximumLineEdit.text()) + 25, 25)
        tof_bins = np.linspace(int(self.toFRangeMinimumLineEdit.text()), int(self.toFRangeMaximumLineEdit.text()), 500)
        image, _, _ = np.histogram2d(tot, tof * 1e6, bins=(tot_bins, tof_bins))
        plt.setImage(image)

    def on_event(self, events):
        self.__update_event_buffers(events[3], events[4])
        self.__update_tot_histogram(self.__event_tot, self._event_data_tot_plt)
        self.__update_2d_histogram_tof_tot(self.__event_tof, self.__event_tot, self._event_data_2d_histogram_tof_tot_data)

    def on_centroid(self, centroids):
        self.__update_centroided_buffers(centroids[3], centroids[4], centroids[6])
        self.__update_tot_histogram(self.__centroided_tot, self._centroided_data_tot_plt)
        self.__update_2d_histogram_tof_tot(self.__centroided_tof, self.__centroided_tot, self._centroided_data_2d_histogram_tof_tot_data)
        self.__update_cluster_size_histogram(self.__centroided_cluster_size, self._centroided_data_cluster_size_data)

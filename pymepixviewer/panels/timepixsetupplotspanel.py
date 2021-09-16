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


        # Event Data Plots Preparation
        self._event_data_tot_plt = pg.PlotDataItem()
        self.plt_event_data_histogram_tot.addItem(self._event_data_tot_plt)
        self.plt_event_data_histogram_tot.setLabel('bottom', text='ToT', units='ns')
        self.plt_event_data_histogram_tot.setLabel('left', text='Count')

        self._event_data_2d_histogram_tof_tot_data = pg.ImageItem()
        self.plt_event_data_2d_histogram_tof_tot.addItem(self._event_data_2d_histogram_tof_tot_data)
        self.plt_event_data_2d_histogram_tof_tot.setLabel('bottom', text='ToT')
        self.plt_event_data_2d_histogram_tof_tot.setLabel('left', text='ToF')


        # Centroided Data Plots Preparation
        self._centroided_data_tot_plt = pg.PlotDataItem()
        self.plt_centroided_data_histogram_tot.addItem(self._centroided_data_tot_plt)
        self.plt_centroided_data_histogram_tot.setLabel('bottom', text='Mean ToT', units='ns')
        self.plt_centroided_data_histogram_tot.setLabel('left', text='Count')

        self._centroided_data_2d_histogram_tof_tot_data = pg.ImageItem()        
        self.plt_centroided_data_2d_histogram_tof_tot.addItem(self._centroided_data_2d_histogram_tof_tot_data)
        self.plt_centroided_data_2d_histogram_tof_tot.setLabel('bottom', text='Mean ToT')
        self.plt_centroided_data_2d_histogram_tof_tot.setLabel('left', text='ToF')

        self._centroided_data_cluster_size_data = pg.PlotDataItem()
        self.plt_centroided_data_histogram_size.addItem(self._centroided_data_cluster_size_data)
        self.plt_centroided_data_histogram_size.setLabel('bottom', text='Cluster Size')
        self.plt_centroided_data_histogram_size.setLabel('left', text='Count')

    def __init_event_buffers(self):
        self.__packet_counter_events = 0
        self.__event_window_tof = []
        self.__event_window_tot = []

    def __init_centroided_buffers(self):
        self.__packet_counter_centroided = 0
        self.__centroided_window_tof = []
        self.__centroided_window_tot = []
        self.__centroided_window_cluster_size = []

    def __update_event_buffers(self, tof, tot):
        if (self.__packet_counter_events >= int(self.numberPacketsLineEdit.text())):
            self.__event_window_tof = self.__event_window_tof[-1:]
            self.__event_window_tot = self.__event_window_tot[-1:]
        self.__event_window_tof.append(tof)
        self.__event_window_tot.append(tot)
        self.__packet_counter_events += 1

    def __update_centroided_buffers(self, tof, tot, cluster_size):
        if (self.__packet_counter_centroided >= int(self.numberPacketsLineEdit.text())):
            self.__centroided_window_tof = self.__centroided_window_tof[-1:]
            self.__centroided_window_tot = self.__centroided_window_tot[-1:]
            self.__centroided_window_cluster_size = self.__centroided_window_cluster_size[-1:]
        self.__centroided_window_tof.append(tof)
        self.__centroided_window_tot.append(tot)
        self.__centroided_window_cluster_size.append(cluster_size)

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

        tr = QtGui.QTransform()
        plt.setTransform(tr.scale(1 / len(tot_bins) * tot_bins[-2], 1 / len(tof_bins) * tof_bins[-1]))

        plt.setImage(image)

    def on_event(self, events):
        self.__update_event_buffers(events[3], events[4])
        tof = np.concatenate(self.__event_window_tof)
        tot = np.concatenate(self.__event_window_tot)
        self.__update_tot_histogram(tot, self._event_data_tot_plt)
        self.__update_2d_histogram_tof_tot(tof, tot, self._event_data_2d_histogram_tof_tot_data)

    def on_centroid(self, centroids):
        self.__update_centroided_buffers(centroids[3], centroids[4], centroids[6])
        tof = np.concatenate(self.__centroided_window_tof)
        tot = np.concatenate(self.__centroided_window_tot)
        cluster_size = np.concatenate(self.__centroided_window_cluster_size)
        self.__update_tot_histogram(tot, self._centroided_data_tot_plt)
        self.__update_2d_histogram_tof_tot(tof, tot, self._centroided_data_2d_histogram_tof_tot_data)
        self.__update_cluster_size_histogram(cluster_size, self._centroided_data_cluster_size_data)

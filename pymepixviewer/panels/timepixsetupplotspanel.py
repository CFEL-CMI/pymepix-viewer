from collections import deque

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from.ui.timepixsetupplotspanelui import Ui_DockWidget

# ATTENTION! If the defined initial values below are equal to the initial values defined in the .ui file, the onChange 
# events are not triggered for initialization. Be carefull when changing the initial values here and check against those 
# in the .ui file!
INITIAL_NUMBER_PACKETS = 10
INITIAL_RANGE_TOF_MINIMUM = 0
INITIAL_RANGE_TOF_MAXIMUM = 5
INITIAL_RANGE_TOT_MINIMUM = 0
INITIAL_RANGE_TOT_MAXIMUM = 1000

class TimepixSetupPlotsPanel(QtGui.QDockWidget, Ui_DockWidget):

    def __init__(self, parent=None):
        super(TimepixSetupPlotsPanel, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)

        self.__events_hist_tot_x = None
        self.__centroids_hist_mean_tot_x = None
        self.__centroids_hist_max_tot_x = None
        self.__centroids_hist_cluster_size_x = None

        self.__events_hist_tot_buffer = None
        self.__events_2d_hist_buffer = None

        self.__centroids_hist_mean_tot_buffer = None
        self.__centroids_hist_max_tot_buffer = None
        self.__centroids_2d_hist_mean_buffer = None
        self.__centroids_2d_hist_max_buffer = None
        self.__centroids_hist_cluster_size_buffer = None

        self.__tot_bins = None
        self.__tof_bins = None

        self.numberPacketsSpinBox.valueChanged.connect(self.onNumberPacketsChanged)
        self.toFRangeMinimumDoubleSpinBox.valueChanged.connect(self.toFRangeMinimumChanged)
        self.toFRangeMaximumDoubleSpinBox.valueChanged.connect(self.toFRangeMaximumChanged)
        self.toTRangeMinimumSpinBox.valueChanged.connect(self.toTRangeMinimumChanged)
        self.toTRangeMaximumSpinBox.valueChanged.connect(self.toTRangeMaximumChanged)

        self.numberPacketsSpinBox.setValue(INITIAL_NUMBER_PACKETS)
        self.toFRangeMinimumDoubleSpinBox.setValue(INITIAL_RANGE_TOF_MINIMUM)
        self.toFRangeMaximumDoubleSpinBox.setValue(INITIAL_RANGE_TOF_MAXIMUM)
        self.toTRangeMinimumSpinBox.setValue(INITIAL_RANGE_TOT_MINIMUM)
        self.toTRangeMaximumSpinBox.setValue(INITIAL_RANGE_TOT_MAXIMUM)

    def setupUi(self, dock_widget):
        result = super().setupUi(dock_widget)

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
        self._centroided_data_mean_tot_plt = pg.PlotDataItem()
        self.plt_centroided_data_histogram_mean_tot.addItem(self._centroided_data_mean_tot_plt)
        self.plt_centroided_data_histogram_mean_tot.setLabel('bottom', text='Mean ToT', units='ns')
        self.plt_centroided_data_histogram_mean_tot.setLabel('left', text='Count')

        self._centroided_data_max_tot_plt = pg.PlotDataItem()
        self.plt_centroided_data_histogram_max_tot.addItem(self._centroided_data_max_tot_plt)
        self.plt_centroided_data_histogram_max_tot.setLabel('bottom', text='Max ToT', units='ns')
        self.plt_centroided_data_histogram_max_tot.setLabel('left', text='Count')

        self._centroided_data_2d_histogram_tof_mean_tot_data = pg.ImageItem()        
        self.plt_centroided_data_2d_histogram_tof_mean_tot.addItem(self._centroided_data_2d_histogram_tof_mean_tot_data)
        self.plt_centroided_data_2d_histogram_tof_mean_tot.setLabel('bottom', text='Mean ToT')
        self.plt_centroided_data_2d_histogram_tof_mean_tot.setLabel('left', text='ToF')

        self._centroided_data_2d_histogram_tof_max_tot_data = pg.ImageItem()        
        self.plt_centroided_data_2d_histogram_tof_max_tot.addItem(self._centroided_data_2d_histogram_tof_max_tot_data)
        self.plt_centroided_data_2d_histogram_tof_max_tot.setLabel('bottom', text='Max ToT')
        self.plt_centroided_data_2d_histogram_tof_max_tot.setLabel('left', text='ToF')

        self._centroided_data_cluster_size_data = pg.PlotDataItem()
        self.plt_centroided_data_histogram_size.addItem(self._centroided_data_cluster_size_data)
        self.plt_centroided_data_histogram_size.setLabel('bottom', text='Cluster Size')
        self.plt_centroided_data_histogram_size.setLabel('left', text='Count')

        return result

    def onNumberPacketsChanged(self, number_packets):
        self.__events_hist_tot_buffer = deque(maxlen=number_packets)
        self.__events_2d_hist_buffer = deque(maxlen=number_packets)

        self.__centroids_hist_mean_tot_buffer = deque(maxlen=number_packets)
        self.__centroids_hist_max_tot_buffer = deque(maxlen=number_packets)
        self.__centroids_2d_hist_mean_buffer = deque(maxlen=number_packets)
        self.__centroids_2d_hist_max_buffer = deque(maxlen=number_packets)
        self.__centroids_hist_cluster_size_buffer = deque(maxlen=number_packets)

    def toFRangeMinimumChanged(self, tof_range_minimum):
        self.tof_range_changed()
        tof_range_maximum = self.toFRangeMaximumDoubleSpinBox.value()
        if tof_range_maximum is not None:
            self.__update_bins_tof(tof_range_minimum, tof_range_maximum)

    def toFRangeMaximumChanged(self, tof_range_maximum):
        self.tof_range_changed()
        tof_range_minimum = self.toFRangeMinimumDoubleSpinBox.value()
        if tof_range_minimum is not None:
            self.__update_bins_tof(tof_range_minimum, tof_range_maximum)

    def toTRangeMinimumChanged(self, tot_range_minimum):
        self.tot_range_changed()
        tot_range_maximum = self.toTRangeMaximumSpinBox.value()
        if tot_range_maximum is not None:
            self.__update_bins_tot(tot_range_minimum, tot_range_maximum)

    def toTRangeMaximumChanged(self, tot_range_maximum):
        self.tot_range_changed()
        tot_range_minimum = self.toTRangeMinimumSpinBox.value()
        if tot_range_minimum is not None:
            self.__update_bins_tot(tot_range_minimum, tot_range_maximum)

    def tof_range_changed(self):
        if self.__events_2d_hist_buffer is not None:
            self.__events_2d_hist_buffer.clear()
        if self.__centroids_2d_hist_mean_buffer is not None:
            self.__centroids_2d_hist_mean_buffer.clear()
        if self.__centroids_2d_hist_max_buffer is not None:
            self.__centroids_2d_hist_max_buffer.clear()

    def tot_range_changed(self):
        if self.__events_hist_tot_buffer is not None:
            self.__events_hist_tot_buffer.clear()
        self.__events_hist_tot_x = None
        if self.__events_2d_hist_buffer is not None:
            self.__events_2d_hist_buffer.clear()

        if self.__centroids_hist_mean_tot_buffer is not None:
            self.__centroids_hist_mean_tot_buffer.clear()
        self.__centroids_hist_mean_tot_x = None
        if self.__centroids_hist_max_tot_buffer is not None:
            self.__centroids_hist_max_tot_buffer.clear()
        self.__centroids_hist_max_tot_x = None
        if self.__centroids_2d_hist_mean_buffer is not None:
            self.__centroids_2d_hist_mean_buffer.clear()
        if self.__centroids_2d_hist_max_buffer is not None:
            self.__centroids_2d_hist_max_buffer.clear()

    def __update_bins_tot(self, tot_min, tot_max):
        self.__tot_bins = range(tot_min, tot_max + 25, 25)
        self.__update_image_transform()

    def __update_bins_tof(self, tof_min, tof_max):
        self.__tof_bins = np.linspace(tof_min, tof_max, 50)
        self.__update_image_transform()

    def __update_image_transform(self):
        if self.__tot_bins is not None and self.__tof_bins is not None:
            tr = QtGui.QTransform()
            tr = tr.scale(1 / len(self.__tot_bins) * self.__tot_bins[-2], 1 / len(self.__tof_bins) * self.__tof_bins[-1])
            self._event_data_2d_histogram_tof_tot_data.setTransform(tr)
            self._centroided_data_2d_histogram_tof_mean_tot_data.setTransform(tr)
            self._centroided_data_2d_histogram_tof_max_tot_data.setTransform(tr)

    def __update_events(self, tof, tot):
        # ToT histogram
        y, x = np.histogram(tot, self.__tot_bins)
        if self.__events_hist_tot_x is None:
            self.__events_hist_tot_x = x
        self.__events_hist_tot_buffer.append(y)
        self._event_data_tot_plt.setData(x=x, y=sum(self.__events_hist_tot_buffer), stepMode='center', fillLevel=0, brush=(0, 0, 255, 150))


        # ToF-ToT correlation
        image, _, _ = np.histogram2d(tot, tof * 1e6, bins=(self.__tot_bins, self.__tof_bins))
        self.__events_2d_hist_buffer.append(image)
        self._event_data_2d_histogram_tof_tot_data.setImage(sum(self.__events_2d_hist_buffer))

    def __update_centroids(self, tof, tot_mean, tot_max, cluster_size):
        # ToT (mean) histogram
        y, x = np.histogram(tot_mean, self.__tot_bins)
        if self.__centroids_hist_mean_tot_x is None:
            self.__centroids_hist_mean_tot_x = x
        self.__centroids_hist_mean_tot_buffer.append(y)
        self._centroided_data_mean_tot_plt.setData(x=x, y=sum(self.__centroids_hist_mean_tot_buffer), stepMode='center', fillLevel=0, brush=(0, 0, 255, 150))


        # ToF-ToT (mean) correlation
        image, _, _ = np.histogram2d(tot_mean, tof * 1e6, bins=(self.__tot_bins, self.__tof_bins))
        self.__centroids_2d_hist_mean_buffer.append(image)
        self._centroided_data_2d_histogram_tof_mean_tot_data.setImage(sum(self.__centroids_2d_hist_mean_buffer))

        # ToT (max) histogram
        y, x = np.histogram(tot_max, self.__tot_bins)
        if self.__centroids_hist_max_tot_x is None:
            self.__centroids_hist_max_tot_x = x
        self.__centroids_hist_max_tot_buffer.append(y)
        self._centroided_data_max_tot_plt.setData(x=x, y=sum(self.__centroids_hist_max_tot_buffer), stepMode='center', fillLevel=0, brush=(0, 0, 255, 150))

        # ToF-ToT (max) correlation
        image, _, _ = np.histogram2d(tot_mean, tof * 1e6, bins=(self.__tot_bins, self.__tof_bins))
        self.__centroids_2d_hist_max_buffer.append(image)
        self._centroided_data_2d_histogram_tof_max_tot_data.setImage(sum(self.__centroids_2d_hist_max_buffer))

        # Cluster size histogram
        y, x = np.histogram(cluster_size, np.linspace(0, 400, 100, dtype=np.float))
        if self.__centroids_hist_cluster_size_x is None:
            self.__centroids_hist_cluster_size_x = x
        self.__centroids_hist_cluster_size_buffer.append(y)
        self._centroided_data_cluster_size_data.setData(x=x, y=sum(self.__centroids_hist_cluster_size_buffer), stepMode='center', fillLevel=0, brush=(0, 0, 255, 150))

    def on_event(self, events):
        self.__update_events(events[3], events[4])

    def on_centroid(self, centroids):
        self.__update_centroids(centroids[3], centroids[4], centroids[5], centroids[6])
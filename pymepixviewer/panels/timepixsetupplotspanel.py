from collections import deque

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui

from .timepix_setup_histogram import TimepixSetupHistogram
from .ui.timepixsetupplotspanelui import Ui_DockWidget

# ATTENTION! If the defined initial values below are equal to the initial values defined in the .ui file, the onChange
# events are not triggered for initialization. Be carefull when changing the initial values here and check against those
# in the .ui file!
INITIAL_NUMBER_PACKETS = 10
INITIAL_RANGE_TOF_MINIMUM = 0
INITIAL_RANGE_TOF_MAXIMUM = 5
INITIAL_RANGE_TOT_MINIMUM = 0
INITIAL_RANGE_TOT_MAXIMUM = 1000

# The bins for the histogram of the clustersize are constant. Therefor they are calculated only once.
CLUSTER_SIZE_BINS = np.linspace(0, 400, 100, dtype=np.float)


class TimepixSetupPlotsPanel(QtGui.QDockWidget, Ui_DockWidget):
    """User interface to display some graphs and plots that are useful for setting up
    the timepix camera for experiments.

    The data displayed here can be aggregated for
    a specified number of packages. One package is the amount of information that is
    provided by the UDP sampler in a single packet. The size of a packet depends significantly
    on the datarate of the timepix camera and can vary heavily. For a lower datarate it is required
    to increase the number of integrated packets to get better statistics."""

    def __init__(self, parent=None):
        super(TimepixSetupPlotsPanel, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)

        self.__events_2d_hist_buffer = None

        self.__centroids_2d_hist_mean_buffer = None
        self.__centroids_2d_hist_max_buffer = None

        self.__tot_bins = None
        self.__tof_bins = None

        self.numberPacketsSpinBox.valueChanged.connect(self.onNumberPacketsChanged)
        self.toFRangeMinimumDoubleSpinBox.valueChanged.connect(
            self.toFRangeMinimumChanged
        )
        self.toFRangeMaximumDoubleSpinBox.valueChanged.connect(
            self.toFRangeMaximumChanged
        )
        self.toTRangeMinimumSpinBox.valueChanged.connect(self.toTRangeMinimumChanged)
        self.toTRangeMaximumSpinBox.valueChanged.connect(self.toTRangeMaximumChanged)
        self.pushButtonReset.clicked.connect(self.__reset_buffers)
        self.pushButtonSnapshot.clicked.connect(self.__snapshot)

        self.numberPacketsSpinBox.setValue(INITIAL_NUMBER_PACKETS)
        self.toFRangeMinimumDoubleSpinBox.setValue(INITIAL_RANGE_TOF_MINIMUM)
        self.toFRangeMaximumDoubleSpinBox.setValue(INITIAL_RANGE_TOF_MAXIMUM)
        self.toTRangeMinimumSpinBox.setValue(INITIAL_RANGE_TOT_MINIMUM)
        self.toTRangeMaximumSpinBox.setValue(INITIAL_RANGE_TOT_MAXIMUM)

    def setupUi(self, dock_widget):
        result = super().setupUi(dock_widget)

        # Event Data Plots Preparation
        self._event_data_tot_histogram = TimepixSetupHistogram(
            self.plt_event_data_histogram_tot, "Count", "ToT (ns)"
        )
        self.plt_event_data_2d_histogram_tof_tot = self.__setup_2d_hist_ui(
            "plt_event_data_2d_histogram_tof_tot", (2, 0), "ToT", "ToF"
        )

        # Centroided Data Plots Preparation
        self._centroided_data_mean_tot_histogram = TimepixSetupHistogram(
            self.plt_centroided_data_histogram_mean_tot, "Count", "Mean ToT (ns)"
        )

        self._centroided_data_max_tot_histogram = TimepixSetupHistogram(
            self.plt_centroided_data_histogram_max_tot, "Count", "Max ToT (ns)"
        )

        self.plt_centroided_data_2d_histogram_tof_mean_tot = self.__setup_2d_hist_ui(
            "plt_centroided_data_2d_histogram_tof_mean_tot", (2, 1), "Mean ToT", "ToF"
        )

        self.plt_centroided_data_2d_histogram_tof_max_tot = self.__setup_2d_hist_ui(
            "plt_centroided_data_2d_histogram_tof_max_tot", (2, 2), "Max ToT", "ToF"
        )

        self._centroided_data_cluster_size_histogram = TimepixSetupHistogram(
            self.plt_centroided_data_histogram_size, "Count", "Cluster Size", None
        )

        return result

    def __setup_2d_hist_ui(self, name, position, label_left, label_bottom):
        plt_2d_hist = pg.ImageView(view=pg.PlotItem())
        plt_2d_hist.setObjectName(name)
        self.gridLayout.addWidget(plt_2d_hist, position[0], position[1], 1, 1)

        plt_2d_hist.setPredefinedGradient("thermal")
        plt_2d_hist.getView().setLabel("bottom", text=label_left)
        plt_2d_hist.getView().setLabel("left", text=label_bottom)
        plt_2d_hist.getView().invertY(False)
        plt_2d_hist.getView().setAspectLocked(False)

        return plt_2d_hist

    def onNumberPacketsChanged(self, number_packets):
        if number_packets == 0:
            number_packets = None
            self.pushButtonReset.setEnabled(True)
        else:
            self.pushButtonReset.setEnabled(False)
        self.__init_buffers(number_packets)

    def __init_buffers(self, number_packets=None):
        self._event_data_tot_histogram.init_buffer(number_packets)
        self.__events_2d_hist_buffer = deque(maxlen=number_packets)

        self._centroided_data_mean_tot_histogram.init_buffer(number_packets)
        self._centroided_data_max_tot_histogram.init_buffer(number_packets)
        self.__centroids_2d_hist_mean_buffer = deque(maxlen=number_packets)
        self.__centroids_2d_hist_max_buffer = deque(maxlen=number_packets)
        self._centroided_data_cluster_size_histogram.init_buffer(number_packets)

    def __reset_buffers(self):
        self.__reset_tof_buffers()
        self.__reset_tot_buffers()

    def __reset_tof_buffers(self):
        if self.__events_2d_hist_buffer is not None:
            self.__events_2d_hist_buffer.clear()
        if self.__centroids_2d_hist_mean_buffer is not None:
            self.__centroids_2d_hist_mean_buffer.clear()
        if self.__centroids_2d_hist_max_buffer is not None:
            self.__centroids_2d_hist_max_buffer.clear()

    def __reset_tot_buffers(self):
        self._event_data_tot_histogram.clear_buffer()
        if self.__events_2d_hist_buffer is not None:
            self.__events_2d_hist_buffer.clear()

        self._centroided_data_mean_tot_histogram.clear_buffer()
        self._centroided_data_max_tot_histogram.clear_buffer()
        if self.__centroids_2d_hist_mean_buffer is not None:
            self.__centroids_2d_hist_mean_buffer.clear()
        if self.__centroids_2d_hist_max_buffer is not None:
            self.__centroids_2d_hist_max_buffer.clear()

    def __snapshot(self):
        self._event_data_tot_histogram.snapshot(self.__tot_bins)
        self._centroided_data_max_tot_histogram.snapshot(self.__tot_bins)
        self._centroided_data_mean_tot_histogram.snapshot(self.__tot_bins)
        self._centroided_data_cluster_size_histogram.snapshot(CLUSTER_SIZE_BINS)

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
        self.__reset_tof_buffers()

    def tot_range_changed(self):
        self.__reset_tot_buffers()

    def __update_bins_tot(self, tot_min, tot_max):
        self.__tot_bins = range(tot_min, tot_max + 25, 25)

    def __update_bins_tof(self, tof_min, tof_max):
        self.__tof_bins = np.linspace(tof_min, tof_max, 50)

    def __update_events(self, tof, tot):
        self._event_data_tot_histogram.refresh(tot, np.array(self.__tot_bins))
        self.__plot_2d_histogram(
            tot,
            tof,
            (self.__tot_bins, self.__tof_bins),
            self.__events_2d_hist_buffer,
            self.plt_event_data_2d_histogram_tof_tot,
        )

    def __update_centroids(self, tof, tot_mean, tot_max, cluster_size):
        # ToT (mean) histogram
        self._centroided_data_mean_tot_histogram.refresh(
            tot_mean, np.array(self.__tot_bins)
        )

        # ToF-ToT (mean) correlation
        self.__plot_2d_histogram(
            tot_mean,
            tof,
            (self.__tot_bins, self.__tof_bins),
            self.__centroids_2d_hist_mean_buffer,
            self.plt_centroided_data_2d_histogram_tof_mean_tot,
        )

        # ToT (max) histogram
        self._centroided_data_max_tot_histogram.refresh(
            tot_max, np.array(self.__tot_bins)
        )

        # ToF-ToT (max) correlation
        self.__plot_2d_histogram(
            tot_max,
            tof,
            (self.__tot_bins, self.__tof_bins),
            self.__centroids_2d_hist_max_buffer,
            self.plt_centroided_data_2d_histogram_tof_max_tot,
        )

        # Cluster size histogram
        self._centroided_data_cluster_size_histogram.refresh(
            cluster_size, CLUSTER_SIZE_BINS
        )

    def __plot_2d_histogram(self, data_x, data_y, bins, buffer, plt):
        image = np.histogram2d(data_x, data_y * 1e6, bins=bins)[0]
        buffer.append(image)

        img = sum(buffer)

        x0, x1 = (bins[0][0], bins[0][-1])
        y0, y1 = (bins[1][0], bins[1][-1])
        xscale = (x1 - x0) / img.shape[0]
        yscale = (y1 - y0) / img.shape[1]
        plt.setImage(
            img / img.max(),
            scale=[xscale, yscale / 1000],
            pos=[x0, y0 / 1000],
            autoRange=False,
            autoLevels=False,
            autoHistogramRange=False,
        )

    def on_event(self, events):
        self.__update_events(events[3], events[4])

    def on_centroid(self, centroids):
        self.__update_centroids(centroids[3], centroids[4], centroids[5], centroids[6])

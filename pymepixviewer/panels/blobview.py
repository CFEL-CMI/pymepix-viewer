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

from collections import deque

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

from ..core.datatypes import ViewerMode
from .ui.blobviewui import Ui_Form


class Crosshair(QtWidgets.QGraphicsItem):
    def __init__(self):
        QtWidgets.QGraphicsItem.__init__(self)
        self.setFlag(self.ItemIgnoresTransformations)

    def paint(self, p, *args):
        p.setPen(pg.mkPen("y"))
        p.drawLine(-10, 0, 10, 0)
        p.drawLine(0, -10, 0, 10)

    def boundingRect(self):
        return QtCore.QRectF(-10, -10, 20, 20)

class BlobView(QtGui.QWidget, Ui_Form):
    def __init__(self, parent=None, start=None, end=None, current_mode=ViewerMode.TOA, camera_generation=3):

        super(BlobView, self).__init__(parent)

        self.camera_generation = camera_generation

        if self.camera_generation == 3:
            self.matrix_dim = (256, 256)
        elif camera_generation == 4:
            self.matrix_dim = (448, 512)
        else:
            raise ValueError('Unknown camera generation')

        # Set up the user interface from Designer.
        self.setupUi(self)

        self._start_tof = start
        self._end_tof = end

        self._int_blob_count = 0
        self._triggers_processed = 1

        self._current_mode = current_mode

        self._matrix = np.ndarray(shape=self.matrix_dim, dtype=np.float)
        self._matrix[...] = 0.0

        self._blob_trend_trigger = deque(maxlen=100)  # blob trend x-axis
        self._blob_trend = deque(maxlen=100)  # blob trend y-axis
        self._blob_trend_graph = pg.PlotDataItem()
        self.blob_trend.addItem(self._blob_trend_graph)
        self.blob_trend.setLabel("left", text="Blob Count")
        self.blob_trend.setLabel("bottom", text="Trigger Number")
        self._last_trigger = 0
        self._blob_trend_roi_xAxe = deque(maxlen=100)  # roi graph x-axis
        self._blob_trend_roi_xAxe.append(0)  # initialise 1st x value
        self._blob_trend_roi_yAxe = deque(maxlen=100)  # roi graph y-axis
        self._blob_trend_roi_yAxe.append(0)  # initialise 1st y value
        self._blob_trend_roi_sum = 0  # temp variable to sum ions per n triggers
        self._blob_trend_roi_sum_triCount = 0  # count triggers integrated
        self._blob_trend_roi_graph = pg.PlotDataItem()
        self.blob_trend_roi.addItem(self._blob_trend_roi_graph)

        self._kernel = None  # smoothing kernel

        self.image_view.setPredefinedGradient("thermal")

        self._histogram_mode = False
        self._pixel_histogram_mode = False
        self._histogram_x = []
        self._histogram_y = []
        self._histogram_bins = self.matrix_dim[1]
        self._x = np.array(self.matrix_dim[1] * [np.arange(0, self.matrix_dim[1])])
        self._y = np.array(self.matrix_dim[1] * [np.arange(0, self.matrix_dim[1])]).T
        self.checkBox.stateChanged.connect(self.onHistogramCheck)
        self.checkBox_pixelhisto.stateChanged.connect(self.onPixelHistogramCheck)
        self.blob_trend_check.stateChanged.connect(self.onTrendCheck)
        self.roi_trend_check.stateChanged.connect(self.onROITrendCheck)
        self.histo_binning.setValue(self.matrix_dim[1])
        self.histo_binning.valueChanged[int].connect(self.onHistBinChange)
        self.show_center.stateChanged.connect(self.on_show_cross_change)
        self.x0_spin.setValue(int(self.matrix_dim[1]/2)-1)
        self.x0_spin.valueChanged.connect(self.on_move_cross)
        self.y0_spin.setValue(int(self.matrix_dim[1]/2)-1)
        self.y0_spin.valueChanged.connect(self.on_move_cross)
        self.trig_avg_spin.valueChanged.connect(self.on_roi_avg_change)
        self.avg_roi.stateChanged.connect(self.on_avg_roi_change)
        # self.r_inner.valueChanged.connect(self.on_redraw_roi)
        self.r_outer.valueChanged.connect(self.on_redraw_roi)

        self._histogram = None

        self.crosshair = Crosshair()
        self.roi_outer = None
        self._binning_fac = 1
        self.trigger_centroid_data = None
        self.trigger2plot = None
        self.last_event = None

    def modeChange(self, mode):
        self._current_mode = mode
        self.clearData()
        if self._current_mode == ViewerMode.Trig:
            self.show_centroids.setEnabled(True)
            self.maxRangeLabel.setEnabled(True)
            self.maxRangeSpinBox.setEnabled(True)
        else:
            self.show_centroids.setEnabled(False)
            self.maxRangeLabel.setEnabled(False)
            self.maxRangeSpinBox.setEnabled(False)

    def getFilter(self, tof):

        if self._start_tof is not None:
            return (tof >= self._start_tof) & (tof < self._end_tof)
        else:
            return tof >= 0.0

    def on_show_cross_change(self):
        if self.show_center.isChecked():
            self.image_view.addItem(self.crosshair)
            if self.roi_outer is not None:
                self.image_view.removeItem(self.roi_outer)
            self.roi_outer = pg.CircleROI(
                [0, 0], [1, 1], pen=pg.mkPen("r", width=1), movable=False
            )
            self.image_view.addItem(self.roi_outer)

            self.on_redraw_roi()
            self.on_move_cross()
        else:
            self.image_view.removeItem(self.crosshair)
            self.image_view.removeItem(self.roi_outer)

    def on_move_cross(self):
        x0 = self.x0_spin.value()
        y0 = self.y0_spin.value()
        radius = self.r_outer.value()
        self.crosshair.setPos(y0 * self._binning_fac, x0 * self._binning_fac)
        self.roi_outer.setPos(
            (y0 - radius) * self._binning_fac, (x0 - radius) * self._binning_fac
        )

    def on_redraw_roi(self):
        diam = 2 * self.r_outer.value() * self._binning_fac
        self.roi_outer.setSize(diam, diam)
        self.on_move_cross()

    def onHistBinChange(self, value):
        self._histogram_bins = value
        self._x = np.array(value * [np.arange(0, value)])
        self._y = np.array(value * [np.arange(0, value)]).T
        self._binning_fac = (
            1 / (self.matrix_dim[1] / self._histogram_bins) if self._histogram_mode else 1
        )
        if self._histogram_mode:
            self.clearData()
        self.on_show_cross_change()

    def onHistogramCheck(self, status):
        self._histogram_mode = status == 2
        self.clearData()

    def onPixelHistogramCheck(self, status):
        self._pixel_histogram_mode = status == 2
        self.clearData()

    def onTrendCheck(self, status):
        if status == 2:
            self.blob_trend.show()
        else:
            self.blob_trend.hide()

    def onROITrendCheck(self, status):
        if status == 2:
            self.blob_trend_roi.show()
        else:
            self.blob_trend_roi.hide()

    def on_roi_avg_change(self, value):
        self._kernel = np.ones(value) / value if value > 0 else None

    def on_avg_roi_change(self, state):
        if state == 2:
            self.trig_avg_spin.setMaximum(100_000)
            self.trig_avg_spin.setSingleStep(100)
            self.trig_avg_spin.setValue(1_000)
        else:
            self.trig_avg_spin.setMaximum(20)
            self.trig_avg_spin.setSingleStep(1)
            self.trig_avg_spin.setValue(0)
        self._blob_trend_roi_xAxe.clear()
        self._blob_trend_roi_yAxe.clear()
        self._blob_trend_roi_xAxe.append(0)
        self._blob_trend_roi_yAxe.append(0)

    def updateMatrix(self, x, y, tof, tot):
        tof_filter = self.getFilter(tof)
        if self._pixel_histogram_mode:
            self._matrix[x[tof_filter], y[tof_filter]] += 1
        else:
            self._matrix[x[tof_filter], y[tof_filter]] += tot[tof_filter]

    def clearMatrix(self):
        self._matrix[:,:] = 0

    def onRegionChange(self, start, end):
        self._start_tof = start
        self._end_tof = end
        self.clearData()

    def setTriggersProcessed(self, triggers_processed):
        self._triggers_processed = triggers_processed

    def _updateHist(self):
        h = np.histogram2d(
            np.concatenate(self._histogram_x),
            np.concatenate(self._histogram_y),
            bins=self._histogram_bins,
            range=[[0, self.matrix_dim[1]], [0, self.matrix_dim[1]]],
        )
        self._histogram_x = []
        self._histogram_y = []
        if self._histogram is None:
            self._histogram = h[0]
        else:
            self._histogram += h[0]

    def updateHistogram(self, x, y):
        self._histogram_x.append(x)
        self._histogram_y.append(y)

        if len(self._histogram_x) > 100:
            self._updateHist()

    def updateBlobData(self, cluster_shot, cluster_x, cluster_y, cluster_tof):
        tof_filter = self.getFilter(cluster_tof)

        total_triggers = (
            (cluster_shot.max() - cluster_shot.min()) + 1
        ) / self._triggers_processed

        x = cluster_x[tof_filter]
        y = cluster_y[tof_filter]
        shots = cluster_shot[tof_filter]
        if x.size == 0:
            self._last_trigger = cluster_shot.max()
            self.rec_blobs.setText(str(int(0)))
            return

        # update number for whole detector
        uniq_shot, counts = np.unique(shots, return_counts=True)
        self._int_blob_count += np.sum(counts)

        avg_blobs = np.sum(counts) / total_triggers
        self.rec_blobs.setText(f"{avg_blobs:.3f}")
        self.int_blobs.setText(str(self._int_blob_count))

        r, _, _ = self.get_radial_coordinate()
        mask = np.logical_and(r <= self.r_outer.value(), r >= self.r_inner.value())
        h = np.histogram2d(x, y, bins=self._histogram_bins, range=[[0, self.matrix_dim[1]], [0, self.matrix_dim[1]]])

        # update number for ROI area
        avg_blobs_roi = h[0][mask].sum() / total_triggers
        if not self.avg_roi.isChecked():
            self._blob_trend_roi_yAxe.append(
                avg_blobs_roi
            )  # for not integrating operation
        else:
            self._blob_trend_roi_sum += h[0][mask].sum()
            self._blob_trend_roi_sum_triCount += total_triggers
            if self._blob_trend_roi_sum_triCount >= self.trig_avg_spin.value():
                self._blob_trend_roi_xAxe.append(self._blob_trend_roi_xAxe[-1] + 1)
                self._blob_trend_roi_yAxe.append(0)
                self._blob_trend_roi_sum_triCount = 0
                self._blob_trend_roi_sum = 0
            else:
                self._blob_trend_roi_yAxe[-1] = (
                    self._blob_trend_roi_sum / self._blob_trend_roi_sum_triCount
                )

        self.int_blobs_roi.setText(f"{avg_blobs_roi:.3f}")

        self._last_trigger = shots.max()
        self.updateTrend(self._last_trigger, avg_blobs)

        if self._histogram_mode:
            self.updateHistogram(x, y)

    def updateTrend(self, trigger, avg_blobs):

        self._blob_trend.append(avg_blobs)
        self._blob_trend_trigger.append(trigger)
        # self._blob_trend_trigger[-1]= trigger

    def onCentroid(self, event):
        if self._current_mode in (ViewerMode.Centroid,):
            (
                cluster_shot,
                cluster_x,
                cluster_y,
                cluster_tof,
                cluster_totAvg,
                cluster_totMax,
                cluster_size,
            ) = event
            self.updateBlobData(cluster_shot, cluster_x, cluster_y, cluster_tof)
        elif self._current_mode in (ViewerMode.Trig,) and self.show_centroids.isChecked():
            trigg_filter = event[0] == self.trigger2plot
            self.trigger_centroid_data = (event[0, trigg_filter], event[1, trigg_filter],\
                                          event[2, trigg_filter], event[3, trigg_filter])

            self.draw_centroid_crosses()

    def onEvent(self, event):
        if (
            self._current_mode
            in (
                ViewerMode.TOF,
                ViewerMode.Centroid,
            )
            and not self._histogram_mode
        ):
            counter, x, y, tof, tot = event
            self.updateMatrix(x, y, tof, tot)
        elif self._current_mode == ViewerMode.Trig:
            x, y, toa, tot = self.get_max_voxels_triggerdata(event)
            self.clearMatrix()
            self.updateMatrix(x, y, toa, tot)


    def onToA(self, event):
        if self._current_mode in (ViewerMode.TOA,):
            x, y, toa, tot = event
            self.updateMatrix(x, y, toa, tot)

    def get_max_voxels_triggerdata(self, event):
        shots, x, y, tof, tot = event
        unique_triggers, unique_trig_nr_indices, unique_trig_nr_counts = np.unique(
            shots, return_index=True, return_counts=True
        )
        self.trigger2plot = unique_triggers[np.argmax(unique_trig_nr_counts)]
        max_trig_indxs = shots == self.trigger2plot
        return x[max_trig_indxs], y[max_trig_indxs], tof[max_trig_indxs], tot[max_trig_indxs],

    def validate_matrix_dimensions(self, dim, x):
        if x < 0:
            return 0
        if x > dim:
            return dim
        return x
    def draw_centroid_crosses(self):

        cross_half_length = 5
        centroids_shape = np.shape(self.trigger_centroid_data)
        mshape = np.shape(self._matrix)
        value2set = max(np.max(self._matrix), self.maxRangeSpinBox.value())

        for i in range(centroids_shape[1]):
            x = int(self.trigger_centroid_data[1][i])
            y = int(self.trigger_centroid_data[2][i])
            x_low  = self.validate_matrix_dimensions(mshape[0], x - cross_half_length)
            x_high = self.validate_matrix_dimensions(mshape[0], x + cross_half_length)
            y_low  = self.validate_matrix_dimensions(mshape[1], y - cross_half_length)
            y_high = self.validate_matrix_dimensions(mshape[1], y + cross_half_length)

            self._matrix[x, y_low:y_high] = value2set
            self._matrix[x_low:x_high, y] = value2set

    def plotData(self):
        self.image_view.clear()
        if not self._histogram_mode:
            # prevent 0 division
            if self._current_mode == ViewerMode.Trig and self.maxRangeSpinBox.value() > 0.0:
                divisor = self.maxRangeSpinBox.value()
            else:
                divisor = self._matrix.max() if self._matrix.max() != 0 else 1e-16
            self.image_view.setImage(
                self._matrix / divisor,
                autoLevels = False,
                autoRange = False,
                autoHistogramRange = False,
            )
        else:
            if len(self._histogram_x) > 0:
                self._updateHist()
            if self._histogram is not None:
                r, dx, binning_fac = self.get_radial_coordinate()
                cos_theta = dx / r
                cos2_theta = cos_theta ** 2
                mask = np.logical_and(
                    r <= self.r_outer.value() * binning_fac,
                    r >= self.r_inner.value() * binning_fac,
                )
                try:
                    expet_cos_theta = (self._histogram * cos_theta)[
                        mask
                    ].sum() / self._histogram[mask].sum()
                    expet_cos2_theta = (self._histogram * cos2_theta)[
                        mask
                    ].sum() / self._histogram[mask].sum()
                    self.cos_theta.setText(f"{expet_cos_theta:.3f}")
                    self.cos2_theta.setText(f"{expet_cos2_theta:.3f}")
                except Exception:
                    pass

                tmp_img = self._histogram / self._histogram.max()
                tmp_img[~mask] = 0
                self.image_view.setImage(
                    tmp_img, autoLevels=False, autoRange=False, autoHistogramRange=False
                )

        # standard blob trend
        x = np.array(self._blob_trend_trigger)
        x_idx = np.argsort(x)
        y = np.array(self._blob_trend)
        self._blob_trend_graph.setData(x=x[x_idx], y=y[x_idx])

        # roi blob trend
        if not self.avg_roi.isChecked():
            x = np.array(self._blob_trend_trigger)
            x_idx = np.argsort(x)
            if self._kernel is None:
                y = np.array(self._blob_trend_roi_yAxe)[x_idx]
            else:
                y = np.convolve(
                    np.array(self._blob_trend_roi_yAxe)[x_idx],
                    self._kernel,
                    mode="same",
                )

            self._blob_trend_roi_graph.setData(x = x[x_idx], y = y)
        else:
            self._blob_trend_roi_graph.setData(
                x=np.array(self._blob_trend_roi_xAxe),
                y=np.array(self._blob_trend_roi_yAxe),
            )

    def get_radial_coordinate(self):
        binning_fac = 1 / (self.matrix_dim[1] / self._histogram_bins)
        # add small value to prevent division by 0 when calculation r
        x0 = self.x0_spin.value() * binning_fac + 0.1
        y0 = self.y0_spin.value() * binning_fac + 0.1

        dx = self._x - x0
        dy = self._y - y0

        return np.sqrt(dx ** 2 + dy ** 2), dx, binning_fac

    def clearData(self):
        self._matrix[...] = 0.0
        self._int_blob_count = 0
        self._histogram = None
        self._histogram_x = []
        self._histogram_y = []
        # self.plotData()


def main():
    app = QtGui.QApplication([])
    config = BlobView()
    config.show()

    app.exec_()


if __name__ == "__main__":
    main()

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
from pyqtgraph.Qt import QtGui, QtCore

from .ui.blobviewui import Ui_Form
from ..core.datatypes import ViewerMode


class Crosshair(QtGui.QGraphicsItem):
    def __init__(self):
        QtGui.QGraphicsItem.__init__(self)
        self.setFlag(self.ItemIgnoresTransformations)

    def paint(self, p, *args):
        p.setPen(pg.mkPen('y'))
        p.drawLine(-10, 0, 10, 0)
        p.drawLine(0, -10, 0, 10)

    def boundingRect(self):
        return QtCore.QRectF(-10, -10, 20, 20)


class BlobView(QtGui.QWidget, Ui_Form):

    def __init__(self, parent=None, start=None, end=None, current_mode=ViewerMode.TOA):
        super(BlobView, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)

        self._start_tof = start
        self._end_tof = end

        self._int_blob_count = 0

        self._current_mode = current_mode

        self._matrix = np.ndarray(shape=(256, 256), dtype=np.float)
        self._matrix[...] = 0.0

        self._blob_trend = deque(maxlen=100)  # np.ndarray(shape=(400,),dtype=np.float)
        # self._blob_trend[...]=0.0
        # self._blob_trend_trigger = np.ndarray(shape=(400,),dtype=np.int)
        # self._blob_trend_trigger[...]=0
        self._blob_trend_trigger = deque(maxlen=100)
        self._blob_trend_data = pg.PlotDataItem()
        self.blob_trend.addItem(self._blob_trend_data)
        self.blob_trend.setLabel('left', text='Blob Count')
        self.blob_trend.setLabel('bottom', text='Trigger Number')
        self._last_trigger = 0

        self._histogram_mode = False
        self._histogram_x = []
        self._histogram_y = []
        self._histogram_bins = 256
        self._x = np.array(256 * [np.arange(0, 256)])
        self._y = np.array(256 * [np.arange(0, 256)]).T
        self.checkBox.stateChanged.connect(self.onHistogramCheck)
        self.blob_trend_check.stateChanged.connect(self.onTrendCheck)
        self.histo_binning.valueChanged[int].connect(self.onHistBinChange)
        self.show_center.stateChanged.connect(self.on_show_cross_change)
        self.x0_spin.valueChanged.connect(self.on_move_cross)
        self.y0_spin.valueChanged.connect(self.on_move_cross)

        self._histogram = None

        self.crosshair = Crosshair()

    def modeChange(self, mode):
        self._current_mode = mode
        self.clearData()

    def getFilter(self, tof):

        if self._start_tof is not None:
            return (tof >= self._start_tof) & (tof < self._end_tof)
        else:
            return (tof >= 0.0)

    def on_show_cross_change(self):
        if self.show_center.isChecked():
            self.image_view.addItem(self.crosshair)
            self.on_move_cross()
        else:
            self.image_view.removeItem(self.crosshair)

    def on_move_cross(self):
        if self._histogram_mode:
            binning_fac = 1 / (256 / self._histogram_bins)
        else:
            binning_fac = 1
        self.crosshair.setPos(self.y0_spin.value() * binning_fac,
                              self.x0_spin.value() * binning_fac)

    def onHistBinChange(self, value):
        self._histogram_bins = value
        self._x = np.array(value * [np.arange(0, value)])
        self._y = np.array(value * [np.arange(0, value)]).T
        if self._histogram_mode:
            self.clearData()
        self.on_show_cross_change()

    def onHistogramCheck(self, status):
        if status == 2:
            self._histogram_mode = True
            self.clearData()
        else:
            self._histogram_mode = False
            self.clearData()

    def onTrendCheck(self, status):
        if status == 2:
            self.blob_trend.show()
        else:
            self.blob_trend.hide()

    def updateMatrix(self, x, y, tof, tot):
        tof_filter = self.getFilter(tof)

        self._matrix[x[tof_filter], y[tof_filter]] += 1.0

    def onRegionChange(self, start, end):
        self._start_tof = start
        self._end_tof = end
        self.clearData()

    def _updateHist(self):
        h = np.histogram2d(np.concatenate(self._histogram_x), np.concatenate(self._histogram_y),
                           bins=self._histogram_bins, range=[[0, 256], [0, 256]])
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

        total_triggers = (cluster_shot.max() - cluster_shot.min()) + 1

        x = cluster_x[tof_filter]
        y = cluster_y[tof_filter]
        tof = cluster_tof[tof_filter]
        shots = cluster_shot[tof_filter]
        if x.size == 0:
            self._last_trigger = cluster_shot.max()
            # self.updateTrend(self._last_trigger,0)
            self.rec_blobs.setText(str(int(0)))
            return

        uniq_shot, counts = np.unique(shots, return_counts=True)

        self._int_blob_count += np.sum(counts)

        avg_blobs = np.sum(counts) / total_triggers

        self.rec_blobs.setText(str(int(avg_blobs)))

        self.int_blobs.setText(str(self._int_blob_count))

        self._last_trigger = shots.max()
        self.updateTrend(self._last_trigger, avg_blobs)

        if self._histogram_mode:
            self.updateHistogram(x, y)

    def onCentroid(self, event):
        if self._current_mode in (ViewerMode.Centroid,):
            cluster_shot, cluster_x, cluster_y, cluster_tof, cluster_tot = event
            self.updateBlobData(cluster_shot, cluster_x, cluster_y, cluster_tof)

    def onEvent(self, event):
        if self._current_mode in (ViewerMode.TOF, ViewerMode.Centroid,):

            if not self._histogram_mode:
                counter, x, y, tof, tot = event
                self.updateMatrix(x, y, tof, tot)

    def onToA(self, event):
        if self._current_mode in (ViewerMode.TOA,):
            x, y, toa, tot = event
            self.updateMatrix(x, y, toa, tot)

    def updateTrend(self, trigger, avg_blobs):

        self._blob_trend.append(avg_blobs)
        self._blob_trend_trigger.append(trigger)
        # self._blob_trend_trigger[-1]= trigger

    def plotData(self):
        if not self._histogram_mode:
            self.image_view.setImage(self._matrix / self._matrix.max(), autoLevels=False, autoRange=False,
                                     autoHistogramRange=False)
        else:
            if len(self._histogram_x) > 0:
                self._updateHist()
            if self._histogram is not None:
                binning_fac = 1 / (256 / self._histogram_bins)
                # add small value to prevent division by 0 when calculation r
                x0 = self.x0_spin.value() * binning_fac + 0.1
                y0 = self.y0_spin.value() * binning_fac + 0.1

                dx = self._x - x0
                dy = self._y - y0

                r = np.sqrt(dx ** 2 + dy ** 2) * binning_fac
                cos_theta = dx / r
                cos2_theta = cos_theta ** 2
                mask = np.logical_and(r <= self.r_outer.value() * binning_fac, r >= self.r_inner.value() * binning_fac)
                try:
                    expet_cos_theta = (self._histogram * cos_theta)[mask].sum() / self._histogram[mask].sum()
                    expet_cos2_theta = (self._histogram * cos2_theta)[mask].sum() / self._histogram[mask].sum()
                    self.cos_theta.setText(f'{expet_cos_theta:.3f}')
                    self.cos2_theta.setText(f'{expet_cos2_theta:.3f}')
                except:
                    pass

                tmp_img = self._histogram / self._histogram.max()
                tmp_img[~mask] = 0
                self.image_view.setImage(tmp_img, autoLevels=False, autoRange=False,
                                         autoHistogramRange=False)

        try:
            self._blob_trend_data.setData(x=np.array(self._blob_trend_trigger), y=np.array(self._blob_trend))
        except:
            pass

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

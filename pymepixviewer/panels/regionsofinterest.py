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

import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import QSettings
from pyqtgraph.Qt import QtCore, QtGui


class BaseItem(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self)
        self._data = ["", "", ""]
        self._children = []
        self._parent = parent

    def addChild(self, item):
        self._children.append(item)

    def removeChild(self, index):
        return self._children.pop(index)

    def child(self, row):
        if row < self.childCount():
            return self._children[row]
        return None

    @property
    def columnName(self):
        return self._data[0]

    @columnName.setter
    def columnName(self, value):
        self._data[0] = value

    @property
    def columnStart(self):
        return self._data[1]

    @columnStart.setter
    def columnStart(self, value):
        self._data[1] = value

    @property
    def columnEnd(self):
        return self._data[2]

    @columnEnd.setter
    def columnEnd(self, value):
        self._data[2] = value

    def childCount(self):
        return len(self._children)

    def row(self):
        if self._parent:
            return self._parent._children.index(self)
        return 0

    def columnCount(self):
        return len(self._data)

    def data(self, column):
        if column < self.columnCount():
            return self._data[column]
        return None

    def parentItem(self):
        return self._parent

    def clearChildren(self):
        for child in self._children:
            child._parent = None

        for x in range(self.childCount()):
            self.removeChild(0)


class RoiItem(BaseItem):
    roiUpdated = QtCore.pyqtSignal(str, float, float)
    roiRemoved = QtCore.pyqtSignal(str)

    def __init__(self, name, start_region, end_region, color=None, parent=None):
        BaseItem.__init__(self, parent=parent)
        self._name = name
        self._start_region = start_region
        self._end_region = end_region
        self._hist_x = np.array([])
        self._hist_y = np.array([])

        self._roi_item = pg.LinearRegionItem(
            values=[self._start_region, self._end_region], brush=color
        )

        self._data = [
            self._name,
            "{:4.2e} us".format(self._start_region * 1e6),
            "{:4.2e} us".format(self._end_region * 1e6),
        ]
        self._roi_item.sigRegionChangeFinished.connect(self.onUserUpdateRoi)

    @property
    def name(self):
        return self._name

    @property
    def start_connection(self):
        return self._start_region

    @property
    def end_region(self):
        return self._end_region

    def onUserUpdateRoi(self):
        self._start_region, self._end_region = self._roi_item.getRegion()

        self._data = [
            self._name,
            "{:4.2e} us".format(self._start_region * 1e6),
            "{:4.2e} us".format(self._end_region * 1e6),
        ]

        print(self._data)
        self.roiUpdated.emit(self._name, self._start_region, self._end_region)

    @property
    def RoiPlotItem(self):
        return self._roi_item

    def onRemove(self):
        self.roiRemoved.emit(self._name)

    @property
    def region(self):
        return self._start_region, self._end_region

    @property
    def histogram(self):
        """hold the histogram for the individual ROI
        use this for e.g. calculating the integral
        """
        return self._hist_x, self._hist_y

    @histogram.setter
    def histogram(self, data):
        self._hist_x = data[0]
        self._hist_y = data[1]

    @property
    def roi_sum(self):
        if self._hist_y is not None:
            return self._hist_y.sum()
        else:
            return None


class RoiModel(QtCore.QAbstractItemModel):
    roiUpdated = QtCore.pyqtSignal(str, float, float)
    roiRemoved = QtCore.pyqtSignal(str, object)

    def __init__(self, parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.rootItem = BaseItem()
        self.rootItem._data = ["Name", "Start", "End"]

    def onRoiUpdate(self, name, start, end):
        # self.layoutChanged.emit()

        self.roiUpdated.emit(name, start, end)

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return QtCore.QVariant()

    def addRegionofInterest(self, name, start, end):
        roiItem = self.addRegionofInterestWithoutSettings(name, start, end)
        if roiItem is not None:
            rois = self.get_rois_from_settings()
            rois.append((name, start, end))
            self.write_rois_to_settings(rois)
        return roiItem

    def get_rois_from_settings(self):
        settings = QSettings()
        rois = []
        size = settings.beginReadArray("regions_of_interest")
        for index in range(size):
            settings.setArrayIndex(index)
            rois.append(self.get_roi_from_settings(settings))
        settings.endArray()
        return rois

    def write_rois_to_settings(self, rois):
        settings = QSettings()
        settings.remove("regions_of_interest")
        settings.beginWriteArray("regions_of_interest")
        for index, (name, start, end) in enumerate(rois):
            settings.setArrayIndex(index)
            settings.setValue("name", name)
            settings.setValue("start", start)
            settings.setValue("end", end)
        settings.endArray()

    def get_roi_from_settings(self, settings):
        return (
            settings.value("name", type=str),
            settings.value("start", type=float),
            settings.value("end", type=float),
        )

    def addRegionofInterestWithoutSettings(self, name, start, end):
        """Add a new region of interest without changing the settings (QSettings). This method is used for loading
        the existing regions of interes on initialization."""
        idx, item = self.searchItem(name)

        if item is not None:
            # Show dialog box that item already exists
            QtGui.QMessageBox.warning(
                None,
                "Duplicate ROI",
                "Roi with name {} already exists".format(name),
                QtGui.QMessageBox.Ok,
                QtGui.QMessageBox.Ok,
            )
            return None
        # print('About to change')

        roiItem = RoiItem(name, start, end, parent=self.rootItem)

        # print('ADDING',name,start,end,self.rootItem)

        # print(self.rootItem)
        roiItem.roiUpdated.connect(self.onRoiUpdate)
        self.layoutAboutToBeChanged.emit()
        self.rootItem.addChild(roiItem)
        self.layoutChanged.emit()
        return roiItem

    def removeRegionofInterest(self, name):
        idx, item = self.searchItem(name)

        if item is None:
            # Show dialog box that item already exists
            QtGui.QMessageBox.warning(
                None,
                "ROI does not exist",
                "Roi with name {} does not exist".format(name),
                QtGui.QMessageBox.Ok,
                QtGui.QMessageBox.Ok,
            )
            return

        self.layoutAboutToBeChanged.emit()
        self._old_roi = self.rootItem.removeChild(idx)
        self.layoutChanged.emit()
        # print('REMOVING:',roi)
        self._old_roi.roiUpdated.disconnect(self.onRoiUpdate)

        rois = self.get_rois_from_settings()
        del rois[idx]
        self.write_rois_to_settings(rois)

        # rint(self.rootItem)

    def index(self, row, column, parent):

        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        parentItem = None

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):

        if not index.isValid():
            return QtCore.QModelIndex()
        # print(index)
        childItem = index.internalPointer()
        # print(type(childItem))
        parentItem = childItem.parentItem()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()
        if parentItem is None:
            return QtCore.QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):

        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()

        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        item = index.internalPointer()

        value = item.data(index.column())
        if not value:
            return QtCore.QVariant()

        return value

    def searchItem(self, search_term):

        for idx, child in enumerate(self.rootItem._children):
            # print (child.columnName)
            if child.columnName == search_term:
                return idx, child
        return -1, None

    def roiNameExists(self, name):
        idx, roi = self.searchItem(name)
        return roi is not None

    def isEmpty(self):
        return self.rootItem.childCount() == 0

    def load_settings(self):
        settings = QSettings()

        roi_items = []

        size = settings.beginReadArray("regions_of_interest")
        for index in range(size):
            settings.setArrayIndex(index)
            roi_items.append(
                self.addRegionofInterestWithoutSettings(
                    *self.get_roi_from_settings(settings)
                )
            )

        settings.endArray()

        return roi_items


def main():
    test_model = RoiModel()
    test_model.addRegionofInterest("test", 0, 100)
    test_model.removeRegionofInterest("test")
    test_model.addRegionofInterest("test", 0, 100)


if __name__ == "__main__":
    main()

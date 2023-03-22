import numpy as np
from pymepix.config.sophyconfig import SophyConfig
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.graphicsItems.ImageItem import ImageItem

from .ui.pixelmapeditui import Ui_DockWidget


class EditPixelMaskPanel(QtGui.QDockWidget, Ui_DockWidget):
    onCloseEvent = QtCore.pyqtSignal(SophyConfig)

    def __init__(self, sophy_config: SophyConfig, parent=None):
        super(EditPixelMaskPanel, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)

        self.__histogram_data = np.zeros((255, 255))
        self.image = self.setup_image(self.__histogram_data)

        # fname, _ = QtGui.QFileDialog.getOpenFileName(self, "Open file", "/home", "SoPhy File (*.spx)")
        self.__sophy_config = sophy_config
        self.__pixel_mask = self.__sophy_config.maskPixels
        self.__pixel_mask_plt = self.setup_pixel_mask(self.image, self.__pixel_mask)

    def closeEvent(self, event):
        self.__sophy_config.saveMask()
        self.onCloseEvent.emit(self.__sophy_config)

    def setup_image(self, histogram_data):
        image = pg.ImageView(view=pg.PlotItem())
        self.verticalLayout.addWidget(image)

        image.setPredefinedGradient("thermal")
        image.getView().setLabel("bottom", text="x")
        image.getView().setLabel("left", text="y")
        # image.getView().invertY(False)
        image.getView().setAspectLocked(False)

        image.getImageItem().mouseClickEvent = self.__image_clicked

        image.setImage(
            histogram_data, autoRange=False, autoLevels=False, autoHistogramRange=False
        )

        return image

    def setup_pixel_mask(self, image, mask):

        image_item = ImageItem()
        lookup_table = pg.ColorMap(
            [0, 1], np.array([[0, 0, 0, 0], [0, 0, 255, 255]])
        ).getLookupTable(alpha=True)
        image_item.setLookupTable(lookup_table)

        image.addItem(image_item)
        image_item.setImage(mask)

        return image_item

    def __update_pixel_mask(self, x, y):
        self.__pixel_mask[x, y] = 1 if self.__pixel_mask[x, y] == 0 else 0
        self.__pixel_mask_plt.setImage(self.__pixel_mask)
        self.__sophy_config.maskPixels = self.__pixel_mask

    def __image_clicked(self, event):
        event.accept()
        pos = event.pos()
        self.__update_pixel_mask(int(pos.x()), int(pos.y()))

    def onTofData(self, data):
        pass

    def onToaData(self, data):
        x, y, toa, tot = data
        histogram_data, _, _ = np.histogram2d(x, 255 - y, bins=range(256))
        self.__histogram_data += histogram_data

        self.image.setImage(
            self.__histogram_data / self.__histogram_data.max(),
            autoRange=False,
            autoLevels=False,
            autoHistogramRange=False,
        )

    def onCentroidData(self, centroids):
        pass

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.graphicsItems.ImageItem import ImageItem

from .ui.pixelmapeditui import Ui_DockWidget

class EditPixelMaskPanel(QtGui.QDockWidget, Ui_DockWidget):

    def __init__(self, parent=None):
        super(EditPixelMaskPanel, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)

        self.image = self.setup_image()
        self.__pixel_mask_plt, self.__pixel_mask = self.setup_pixel_mask(self.image)

        self.__histogram_data = None

    def setup_image(self):
        image = pg.ImageView(view=pg.PlotItem())
        self.verticalLayout.addWidget(image)
        
        image.setPredefinedGradient("thermal")
        image.getView().setLabel('bottom', text="x")
        image.getView().setLabel('left', text="y")
        image.getView().invertY(False)
        image.getView().setAspectLocked(False)

        image.getImageItem().mouseClickEvent = self.__image_clicked

        
        return image

    def setup_pixel_mask(self, image):

        mask = np.zeros((256,256))

        image_item = ImageItem()
        lookup_table = pg.ColorMap([0, 1],np.array([[0, 0, 0, 0], 
            [0, 0, 255, 255]])).getLookupTable(alpha=True)
        image_item.setLookupTable(lookup_table)

        image.addItem(image_item)
        image_item.setImage(mask)
        
        return image_item, mask


    def __update_pixel_mask(self, x, y):
        self.__pixel_mask[x, y] = 1 if self.__pixel_mask[x, y] == 0 else 0
        self.__pixel_mask_plt.setImage(self.__pixel_mask)

    def __image_clicked(self, event):
        event.accept()  
        pos = event.pos()
        # print(int(pos.x()),int(pos.y()))
        self.__update_pixel_mask(int(pos.x()),int(pos.y()))

    def onTofData(self, data):
        counter, x, y, tof, tot = data

    def onToaData(self, data):
        x, y, toa, tot = data
        histogram_data, _, _ = np.histogram2d(x, y, bins=range(256))
        if self.__histogram_data is None:
            self.__histogram_data = histogram_data
        else: 
            self.__histogram_data += histogram_data
        
        self.image.setImage(self.__histogram_data / self.__histogram_data.max(), autoRange=False, autoLevels=False, autoHistogramRange=False)

    def onCentroidData(self, centroids):
        cluster_shot, cluster_x, cluster_y, cluster_tof, cluster_tot = centroids
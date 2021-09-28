
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from .ui.pixelmapeditui import Ui_DockWidget

class EditPixelMaskPanel(QtGui.QDockWidget, Ui_DockWidget):

    def __init__(self, parent=None):
        super(EditPixelMaskPanel, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)

        self.image = self.setup_image()

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

    def __image_clicked(event):
        event.accept()  
        pos = event.pos()
        print(int(pos.x()),int(pos.y()))

    def onTofData(self, data):
        counter, x, y, tof, tot = data

    def onToaData(self, data):
        x, y, toa, tot = data

    def onCentroidData(self, centroids):
        cluster_shot, cluster_x, cluster_y, cluster_tof, cluster_tot = centroids
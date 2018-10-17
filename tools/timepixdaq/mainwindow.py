import pymepix
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
import weakref
import numpy as np
from pymepix import *
from ui.mainwindow_designer import Ui_MainWindow
from timepixconfig import TimepixConfiguration
from datavisualizer import DataVisualizer
class MainWindow(QtGui.QMainWindow,Ui_MainWindow):


    newPixelData = QtCore.pyqtSignal(object)
    newTriggerData = QtCore.pyqtSignal(object)
    acquisitionStart = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)
        self._viewer_widget = DataVisualizer(parent=self)
        self.setCentralWidget(self._viewer_widget)
        self._timepix = TimePixAcq(('192.168.1.10',50000))

        tabwidget = QtGui.QTabWidget(parent=self)
        

        self._dock_tab_widget = QtGui.QDockWidget(parent=self)
        self._dock_tab_widget.setWidget(tabwidget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,self._dock_tab_widget)

        self._timepix.attachEventCallback(self.onNewTrigger)
        self.connectSignals()

        self._timepix.startAcquisition()
    
    def onNewTrigger(self,trigger):

        print('new Trigger')
        self.newTriggerData.emit(trigger)

    def onNewPixel(self,pixel):

        self.newPixelData.emit(pixel)

    def connectSignals(self):

        self.newTriggerData.connect(self._viewer_widget.onNewTriggerData)

def main():
    import sys
    app = QtGui.QApplication([])
    daq = MainWindow()
    daq.show()
    app.exec_()
if __name__=="__main__":
    main()
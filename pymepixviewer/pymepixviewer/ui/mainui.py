# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuLoad_Setting = QtWidgets.QMenu(self.menuFile)
        self.menuLoad_Setting.setObjectName("menuLoad_Setting")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSophy_spx = QtWidgets.QAction(MainWindow)
        self.actionSophy_spx.setObjectName("actionSophy_spx")
        self.actionLoad_Hotpixel_Mask = QtWidgets.QAction(MainWindow)
        self.actionLoad_Hotpixel_Mask.setObjectName("actionLoad_Hotpixel_Mask")
        self.actionHot_Pixel_Mask = QtWidgets.QAction(MainWindow)
        self.actionHot_Pixel_Mask.setObjectName("actionHot_Pixel_Mask")
        self.menuLoad_Setting.addAction(self.actionSophy_spx)
        self.menuLoad_Setting.addAction(self.actionHot_Pixel_Mask)
        self.menuFile.addAction(self.menuLoad_Setting.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuLoad_Setting.setTitle(_translate("MainWindow", "Load Setting"))
        self.actionSophy_spx.setText(_translate("MainWindow", "SoPhy file"))
        self.actionLoad_Hotpixel_Mask.setText(_translate("MainWindow", "Load Hotpixel Mask"))
        self.actionHot_Pixel_Mask.setText(_translate("MainWindow", "Hot Pixel Mask"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


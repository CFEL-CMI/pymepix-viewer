# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pymepix-viewer/pymepixviewer/ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSophy_spx = QtWidgets.QAction(MainWindow)
        self.actionSophy_spx.setObjectName("actionSophy_spx")
        self.actionLaunchPostProcessing = QtWidgets.QAction(MainWindow)
        self.actionLaunchPostProcessing.setObjectName("actionLaunchPostProcessing")
        self.actionTimepixSetupPlotsPanel = QtWidgets.QAction(MainWindow)
        self.actionTimepixSetupPlotsPanel.setObjectName("actionTimepixSetupPlotsPanel")
        self.editPixelMask = QtWidgets.QAction(MainWindow)
        self.editPixelMask.setObjectName("editPixelMask")
        self.menuFile.addAction(self.actionLaunchPostProcessing)
        self.menuFile.addAction(self.actionTimepixSetupPlotsPanel)
        self.menuFile.addAction(self.editPixelMask)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSophy_spx.setText(_translate("MainWindow", "SoPhy file"))
        self.actionLaunchPostProcessing.setText(_translate("MainWindow", "Launch Post Processing"))
        self.actionTimepixSetupPlotsPanel.setText(_translate("MainWindow", "TimePix Setup Optimization"))
        self.editPixelMask.setText(_translate("MainWindow", "Edit Pixel Mask"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './pymepix-viewer/pymepixviewer/ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
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
        self.actionLaunchPostProcessing = QtWidgets.QAction(MainWindow)
        self.actionLaunchPostProcessing.setObjectName("actionLaunchPostProcessing")
        self.actionTimepixSetupPlotsPanel = QtWidgets.QAction(MainWindow)
        self.actionTimepixSetupPlotsPanel.setObjectName("actionTimepixSetupPlotsPanel")
        self.menuLoad_Setting.addAction(self.actionSophy_spx)
        self.menuFile.addAction(self.menuLoad_Setting.menuAction())
        self.menuFile.addAction(self.actionLaunchPostProcessing)
        self.menuFile.addAction(self.actionTimepixSetupPlotsPanel)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuLoad_Setting.setTitle(_translate("MainWindow", "Load Setting"))
        self.actionSophy_spx.setText(_translate("MainWindow", "SoPhy file"))
        self.actionLaunchPostProcessing.setText(_translate("MainWindow", "Launch Post Processing"))
        self.actionTimepixSetupPlotsPanel.setText(_translate("MainWindow", "TimePix Setup Optimization"))


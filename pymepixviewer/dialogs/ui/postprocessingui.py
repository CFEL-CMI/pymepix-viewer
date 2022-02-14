# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './pymepix-viewer/pymepixviewer/dialogs/ui/postprocessing.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(610, 239)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.labelTimeWalkFileCentroided = QtWidgets.QLabel(Dialog)
        self.labelTimeWalkFileCentroided.setObjectName("labelTimeWalkFileCentroided")
        self.gridLayout.addWidget(self.labelTimeWalkFileCentroided, 2, 1, 1, 1)
        self.labelTimeWalkFile = QtWidgets.QLabel(Dialog)
        self.labelTimeWalkFile.setObjectName("labelTimeWalkFile")
        self.gridLayout.addWidget(self.labelTimeWalkFile, 1, 1, 1, 1)
        self.lineEditTimeWalkFileCentroided = QtWidgets.QLineEdit(Dialog)
        self.lineEditTimeWalkFileCentroided.setObjectName(
            "lineEditTimeWalkFileCentroided"
        )
        self.gridLayout.addWidget(self.lineEditTimeWalkFileCentroided, 2, 2, 1, 1)
        self.pushButtonBrowseInputFiles = QtWidgets.QPushButton(Dialog)
        self.pushButtonBrowseInputFiles.setObjectName("pushButtonBrowseInputFiles")
        self.gridLayout.addWidget(self.pushButtonBrowseInputFiles, 0, 3, 1, 1)
        self.labelInputFiles = QtWidgets.QLabel(Dialog)
        self.labelInputFiles.setObjectName("labelInputFiles")
        self.gridLayout.addWidget(self.labelInputFiles, 0, 1, 1, 1)
        self.labelOutputDirectory = QtWidgets.QLabel(Dialog)
        self.labelOutputDirectory.setObjectName("labelOutputDirectory")
        self.gridLayout.addWidget(self.labelOutputDirectory, 4, 1, 1, 1)
        self.lineEditInputFiles = QtWidgets.QLineEdit(Dialog)
        self.lineEditInputFiles.setObjectName("lineEditInputFiles")
        self.gridLayout.addWidget(self.lineEditInputFiles, 0, 2, 1, 1)
        self.pushButtonBrowseOutputDirectory = QtWidgets.QPushButton(Dialog)
        self.pushButtonBrowseOutputDirectory.setObjectName(
            "pushButtonBrowseOutputDirectory"
        )
        self.gridLayout.addWidget(self.pushButtonBrowseOutputDirectory, 4, 3, 1, 1)
        self.lineEditOutputDirectory = QtWidgets.QLineEdit(Dialog)
        self.lineEditOutputDirectory.setObjectName("lineEditOutputDirectory")
        self.gridLayout.addWidget(self.lineEditOutputDirectory, 4, 2, 1, 1)
        self.pushButtonStartProcessing = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButtonStartProcessing.sizePolicy().hasHeightForWidth()
        )
        self.pushButtonStartProcessing.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonStartProcessing.setFont(font)
        self.pushButtonStartProcessing.setObjectName("pushButtonStartProcessing")
        self.gridLayout.addWidget(self.pushButtonStartProcessing, 5, 3, 1, 1)
        self.lineEditTimeWalkFile = QtWidgets.QLineEdit(Dialog)
        self.lineEditTimeWalkFile.setObjectName("lineEditTimeWalkFile")
        self.gridLayout.addWidget(self.lineEditTimeWalkFile, 1, 2, 1, 1)
        self.pushButtonBrowseTimeWalkFile = QtWidgets.QPushButton(Dialog)
        self.pushButtonBrowseTimeWalkFile.setObjectName("pushButtonBrowseTimeWalkFile")
        self.gridLayout.addWidget(self.pushButtonBrowseTimeWalkFile, 1, 3, 1, 1)
        self.pushButtonBrowseTimeWalkFileCentroided = QtWidgets.QPushButton(Dialog)
        self.pushButtonBrowseTimeWalkFileCentroided.setObjectName(
            "pushButtonBrowseTimeWalkFileCentroided"
        )
        self.gridLayout.addWidget(
            self.pushButtonBrowseTimeWalkFileCentroided, 2, 3, 1, 1
        )
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 3)
        self.horizontalLayout_3.addLayout(self.gridLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setEnabled(True)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Post Processing"))
        self.labelTimeWalkFileCentroided.setText(
            _translate("Dialog", "Time-walk File (centroided)")
        )
        self.labelTimeWalkFile.setText(_translate("Dialog", "Time-walk File"))
        self.pushButtonBrowseInputFiles.setText(_translate("Dialog", "Browse"))
        self.labelInputFiles.setText(_translate("Dialog", "Input File(s)"))
        self.labelOutputDirectory.setText(_translate("Dialog", "Output Directory"))
        self.lineEditInputFiles.setToolTip(
            _translate("Dialog", "Semicolon separated list of filenames")
        )
        self.pushButtonBrowseOutputDirectory.setText(_translate("Dialog", "Browse"))
        self.pushButtonStartProcessing.setText(_translate("Dialog", "Start Processing"))
        self.pushButtonBrowseTimeWalkFile.setText(_translate("Dialog", "Browse"))
        self.pushButtonBrowseTimeWalkFileCentroided.setText(
            _translate("Dialog", "Browse")
        )

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './pymepix-viewer/pymepixviewer/panels/ui/timepixsetupplotspanel.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(700, 614)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.toFRangeMinimumLabel = QtWidgets.QLabel(self.dockWidgetContents)
        self.toFRangeMinimumLabel.setObjectName("toFRangeMinimumLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.toFRangeMinimumLabel)
        self.toFRangeMinimumLineEdit = QtWidgets.QLineEdit(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toFRangeMinimumLineEdit.sizePolicy().hasHeightForWidth())
        self.toFRangeMinimumLineEdit.setSizePolicy(sizePolicy)
        self.toFRangeMinimumLineEdit.setObjectName("toFRangeMinimumLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.toFRangeMinimumLineEdit)
        self.toFRangeMaximumLabel = QtWidgets.QLabel(self.dockWidgetContents)
        self.toFRangeMaximumLabel.setObjectName("toFRangeMaximumLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.toFRangeMaximumLabel)
        self.toFRangeMaximumLineEdit = QtWidgets.QLineEdit(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toFRangeMaximumLineEdit.sizePolicy().hasHeightForWidth())
        self.toFRangeMaximumLineEdit.setSizePolicy(sizePolicy)
        self.toFRangeMaximumLineEdit.setObjectName("toFRangeMaximumLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.toFRangeMaximumLineEdit)
        self.toTRangeMinimumLabel = QtWidgets.QLabel(self.dockWidgetContents)
        self.toTRangeMinimumLabel.setObjectName("toTRangeMinimumLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.toTRangeMinimumLabel)
        self.toTRangeMinimumLineEdit = QtWidgets.QLineEdit(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toTRangeMinimumLineEdit.sizePolicy().hasHeightForWidth())
        self.toTRangeMinimumLineEdit.setSizePolicy(sizePolicy)
        self.toTRangeMinimumLineEdit.setObjectName("toTRangeMinimumLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.toTRangeMinimumLineEdit)
        self.toTRangeMaximumLabel = QtWidgets.QLabel(self.dockWidgetContents)
        self.toTRangeMaximumLabel.setObjectName("toTRangeMaximumLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.toTRangeMaximumLabel)
        self.toTRangeMaximumLineEdit = QtWidgets.QLineEdit(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toTRangeMaximumLineEdit.sizePolicy().hasHeightForWidth())
        self.toTRangeMaximumLineEdit.setSizePolicy(sizePolicy)
        self.toTRangeMaximumLineEdit.setObjectName("toTRangeMaximumLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.toTRangeMaximumLineEdit)
        self.numberPacketsLabel = QtWidgets.QLabel(self.dockWidgetContents)
        self.numberPacketsLabel.setObjectName("numberPacketsLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.numberPacketsLabel)
        self.numberPacketsLineEdit = QtWidgets.QLineEdit(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numberPacketsLineEdit.sizePolicy().hasHeightForWidth())
        self.numberPacketsLineEdit.setSizePolicy(sizePolicy)
        self.numberPacketsLineEdit.setObjectName("numberPacketsLineEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.numberPacketsLineEdit)
        self.gridLayout.addLayout(self.formLayout, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.plt_event_data_2d_histogram_tof_tot = PlotWidget(self.dockWidgetContents)
        self.plt_event_data_2d_histogram_tof_tot.setObjectName("plt_event_data_2d_histogram_tof_tot")
        self.gridLayout.addWidget(self.plt_event_data_2d_histogram_tof_tot, 2, 0, 1, 1)
        self.plt_event_data_histogram_tot = PlotWidget(self.dockWidgetContents)
        self.plt_event_data_histogram_tot.setObjectName("plt_event_data_histogram_tot")
        self.gridLayout.addWidget(self.plt_event_data_histogram_tot, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.plt_centroided_data_histogram_tot = PlotWidget(self.dockWidgetContents)
        self.plt_centroided_data_histogram_tot.setObjectName("plt_centroided_data_histogram_tot")
        self.gridLayout.addWidget(self.plt_centroided_data_histogram_tot, 1, 1, 1, 1)
        self.plt_centroided_data_2d_histogram_tof_tot = PlotWidget(self.dockWidgetContents)
        self.plt_centroided_data_2d_histogram_tof_tot.setObjectName("plt_centroided_data_2d_histogram_tof_tot")
        self.gridLayout.addWidget(self.plt_centroided_data_2d_histogram_tof_tot, 2, 1, 1, 1)
        self.plt_centroided_data_histogram_size = PlotWidget(self.dockWidgetContents)
        self.plt_centroided_data_histogram_size.setObjectName("plt_centroided_data_histogram_size")
        self.plt_centroided_data_2d_histogram_tof_tot.raise_()
        self.gridLayout.addWidget(self.plt_centroided_data_histogram_size, 3, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        DockWidget.setWindowTitle(_translate("DockWidget", "TimePix Setup Optimization"))
        self.toFRangeMinimumLabel.setText(_translate("DockWidget", "ToF Range Minimum"))
        self.toFRangeMinimumLineEdit.setText(_translate("DockWidget", "0"))
        self.toFRangeMaximumLabel.setText(_translate("DockWidget", "ToF Range Maximum"))
        self.toFRangeMaximumLineEdit.setText(_translate("DockWidget", "5"))
        self.toTRangeMinimumLabel.setText(_translate("DockWidget", "ToT Range Minimum"))
        self.toTRangeMinimumLineEdit.setText(_translate("DockWidget", "0"))
        self.toTRangeMaximumLabel.setText(_translate("DockWidget", "ToT Range Maximum"))
        self.toTRangeMaximumLineEdit.setText(_translate("DockWidget", "1000"))
        self.numberPacketsLabel.setToolTip(_translate("DockWidget", "<html><head/><body><p>Number of packets used for the sliding window calculation of the histograms</p></body></html>"))
        self.numberPacketsLabel.setText(_translate("DockWidget", "Number Packets"))
        self.numberPacketsLineEdit.setToolTip(_translate("DockWidget", "<html><head/><body><p>Number of packets used for the sliding window calculation of the histograms</p></body></html>"))
        self.numberPacketsLineEdit.setText(_translate("DockWidget", "10"))
        self.label.setText(_translate("DockWidget", "Event Data"))
        self.label_2.setText(_translate("DockWidget", "Centroided Data"))

from pyqtgraph import PlotWidget

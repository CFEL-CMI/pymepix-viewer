# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'timepixsetupplotspanel.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(1025, 631)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DockWidget.sizePolicy().hasHeightForWidth())
        DockWidget.setSizePolicy(sizePolicy)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
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
        self.plt_event_data_2d_histogram_tof_tot = ImageView(self.dockWidgetContents)
        self.plt_event_data_2d_histogram_tof_tot.setObjectName("plt_event_data_2d_histogram_tof_tot")
        self.gridLayout.addWidget(self.plt_event_data_2d_histogram_tof_tot, 2, 0, 1, 1)
        self.plt_event_data_histogram_tot = PlotWidget(self.dockWidgetContents)
        self.plt_event_data_histogram_tot.setObjectName("plt_event_data_histogram_tot")
        self.gridLayout.addWidget(self.plt_event_data_histogram_tot, 1, 0, 1, 1)
        self.plt_centroided_data_histogram_mean_tot = PlotWidget(self.dockWidgetContents)
        self.plt_centroided_data_histogram_mean_tot.setObjectName("plt_centroided_data_histogram_mean_tot")
        self.gridLayout.addWidget(self.plt_centroided_data_histogram_mean_tot, 1, 1, 1, 1)
        self.plt_centroided_data_histogram_max_tot = PlotWidget(self.dockWidgetContents)
        self.plt_centroided_data_histogram_max_tot.setObjectName("plt_centroided_data_histogram_max_tot")
        self.gridLayout.addWidget(self.plt_centroided_data_histogram_max_tot, 1, 2, 1, 1)
        self.plt_centroided_data_2d_histogram_tof_mean_tot = ImageView(self.dockWidgetContents)
        self.plt_centroided_data_2d_histogram_tof_mean_tot.setObjectName("plt_centroided_data_2d_histogram_tof_mean_tot")
        self.gridLayout.addWidget(self.plt_centroided_data_2d_histogram_tof_mean_tot, 2, 1, 1, 1)
        self.plt_centroided_data_2d_histogram_tof_max_tot = ImageView(self.dockWidgetContents)
        self.plt_centroided_data_2d_histogram_tof_max_tot.setObjectName("plt_centroided_data_2d_histogram_tof_max_tot")
        self.gridLayout.addWidget(self.plt_centroided_data_2d_histogram_tof_max_tot, 2, 2, 1, 1)
        self.plt_event_data_histogram_tot_2 = PlotWidget(self.dockWidgetContents)
        self.plt_event_data_histogram_tot_2.setObjectName("plt_event_data_histogram_tot_2")
        self.gridLayout.addWidget(self.plt_event_data_histogram_tot_2, 3, 0, 1, 1)
        self.plt_centroided_data_histogram_size = PlotWidget(self.dockWidgetContents)
        self.plt_centroided_data_histogram_size.setObjectName("plt_centroided_data_histogram_size")
        self.gridLayout.addWidget(self.plt_centroided_data_histogram_size, 3, 1, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.numberPacketsSpinBox = QtWidgets.QSpinBox(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numberPacketsSpinBox.sizePolicy().hasHeightForWidth())
        self.numberPacketsSpinBox.setSizePolicy(sizePolicy)
        self.numberPacketsSpinBox.setMinimum(0)
        self.numberPacketsSpinBox.setMaximum(1000)
        self.numberPacketsSpinBox.setProperty("value", 1)
        self.numberPacketsSpinBox.setObjectName("numberPacketsSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.numberPacketsSpinBox)
        self.toFRangeMinimumLabel_2 = QtWidgets.QLabel(self.dockWidgetContents)
        self.toFRangeMinimumLabel_2.setObjectName("toFRangeMinimumLabel_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.toFRangeMinimumLabel_2)
        self.toFRangeMinimumDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toFRangeMinimumDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.toFRangeMinimumDoubleSpinBox.setSizePolicy(sizePolicy)
        self.toFRangeMinimumDoubleSpinBox.setProperty("value", 0.01)
        self.toFRangeMinimumDoubleSpinBox.setObjectName("toFRangeMinimumDoubleSpinBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.toFRangeMinimumDoubleSpinBox)
        self.toFRangeMaximumLabel_2 = QtWidgets.QLabel(self.dockWidgetContents)
        self.toFRangeMaximumLabel_2.setObjectName("toFRangeMaximumLabel_2")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.toFRangeMaximumLabel_2)
        self.toFRangeMaximumDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toFRangeMaximumDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.toFRangeMaximumDoubleSpinBox.setSizePolicy(sizePolicy)
        self.toFRangeMaximumDoubleSpinBox.setProperty("value", 0.01)
        self.toFRangeMaximumDoubleSpinBox.setObjectName("toFRangeMaximumDoubleSpinBox")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.toFRangeMaximumDoubleSpinBox)
        self.toTRangeMinimumLabel_2 = QtWidgets.QLabel(self.dockWidgetContents)
        self.toTRangeMinimumLabel_2.setObjectName("toTRangeMinimumLabel_2")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.toTRangeMinimumLabel_2)
        self.toTRangeMinimumSpinBox = QtWidgets.QSpinBox(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toTRangeMinimumSpinBox.sizePolicy().hasHeightForWidth())
        self.toTRangeMinimumSpinBox.setSizePolicy(sizePolicy)
        self.toTRangeMinimumSpinBox.setMaximum(10000)
        self.toTRangeMinimumSpinBox.setSingleStep(25)
        self.toTRangeMinimumSpinBox.setProperty("value", 1)
        self.toTRangeMinimumSpinBox.setObjectName("toTRangeMinimumSpinBox")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.toTRangeMinimumSpinBox)
        self.toTRangeMaximumLabel = QtWidgets.QLabel(self.dockWidgetContents)
        self.toTRangeMaximumLabel.setObjectName("toTRangeMaximumLabel")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.toTRangeMaximumLabel)
        self.toTRangeMaximumSpinBox = QtWidgets.QSpinBox(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toTRangeMaximumSpinBox.sizePolicy().hasHeightForWidth())
        self.toTRangeMaximumSpinBox.setSizePolicy(sizePolicy)
        self.toTRangeMaximumSpinBox.setMaximum(10000)
        self.toTRangeMaximumSpinBox.setSingleStep(25)
        self.toTRangeMaximumSpinBox.setProperty("value", 25)
        self.toTRangeMaximumSpinBox.setObjectName("toTRangeMaximumSpinBox")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.toTRangeMaximumSpinBox)
        self.pushButtonReset = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonReset.setEnabled(False)
        self.pushButtonReset.setObjectName("pushButtonReset")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.pushButtonReset)
        self.pushButtonSnapshot = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonSnapshot.setObjectName("pushButtonSnapshot")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.pushButtonSnapshot)
        self.label_3 = QtWidgets.QLabel(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.numberPacketsLabel_2 = QtWidgets.QLabel(self.dockWidgetContents)
        self.numberPacketsLabel_2.setObjectName("numberPacketsLabel_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.numberPacketsLabel_2)
        self.gridLayout.addLayout(self.formLayout, 3, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        DockWidget.setWindowTitle(_translate("DockWidget", "TimePix Setup Optimization"))
        self.label.setText(_translate("DockWidget", "Event Data"))
        self.label_2.setText(_translate("DockWidget", "Centroided Data"))
        self.numberPacketsSpinBox.setToolTip(_translate("DockWidget", "<html><head/><body><p>The number of packets used for integration. With 0 integration will be indefinitely long.</p></body></html>"))
        self.toFRangeMinimumLabel_2.setText(_translate("DockWidget", "ToF Range Minimum"))
        self.toFRangeMaximumLabel_2.setText(_translate("DockWidget", "ToF Range Maximum"))
        self.toTRangeMinimumLabel_2.setToolTip(_translate("DockWidget", "<html><head/><body><p>in ns</p></body></html>"))
        self.toTRangeMinimumLabel_2.setText(_translate("DockWidget", "ToT Range Minimum"))
        self.toTRangeMinimumSpinBox.setToolTip(_translate("DockWidget", "<html><head/><body><p>in ns</p></body></html>"))
        self.toTRangeMaximumLabel.setToolTip(_translate("DockWidget", "<html><head/><body><p>in ns</p></body></html>"))
        self.toTRangeMaximumLabel.setText(_translate("DockWidget", "ToT Range Maximum"))
        self.toTRangeMaximumSpinBox.setToolTip(_translate("DockWidget", "<html><head/><body><p>in ns</p></body></html>"))
        self.pushButtonReset.setToolTip(_translate("DockWidget", "<html><head/><body><p>Reset the current buffer. All frames currently in the buffer will be disregarded. <span style=\" font-weight:600;\">Use this only if Number Packets is 0.</span></p></body></html>"))
        self.pushButtonReset.setText(_translate("DockWidget", "Reset Buffer"))
        self.pushButtonSnapshot.setToolTip(_translate("DockWidget", "<html><head/><body><p>Take a &quot;snapshot&quot; of the current data as a underlay to gathered data.</p></body></html>"))
        self.pushButtonSnapshot.setText(_translate("DockWidget", "Take Reference"))
        self.label_3.setText(_translate("DockWidget", "Settings/Controls"))
        self.numberPacketsLabel_2.setToolTip(_translate("DockWidget", "<html><head/><body><p>The number of packets used for integration. With 0 integration will be indefinitely long.</p></body></html>"))
        self.numberPacketsLabel_2.setText(_translate("DockWidget", "Number Packets"))

from pyqtgraph import ImageView, PlotWidget

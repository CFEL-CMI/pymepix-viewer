# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'blobview.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import ImageView, PlotWidget


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(516, 921)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.image_view = ImageView(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(80)
        sizePolicy.setHeightForWidth(self.image_view.sizePolicy().hasHeightForWidth())
        self.image_view.setSizePolicy(sizePolicy)
        self.image_view.setObjectName("image_view")
        self.horizontalLayout.addWidget(self.image_view)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setUnderline(True)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.rec_blobs = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rec_blobs.sizePolicy().hasHeightForWidth())
        self.rec_blobs.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.rec_blobs.setFont(font)
        self.rec_blobs.setAlignment(QtCore.Qt.AlignCenter)
        self.rec_blobs.setObjectName("rec_blobs")
        self.verticalLayout.addWidget(self.rec_blobs)
        self.verticalLayout_5.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setUnderline(True)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.int_blobs = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.int_blobs.setFont(font)
        self.int_blobs.setAlignment(QtCore.Qt.AlignCenter)
        self.int_blobs.setObjectName("int_blobs")
        self.verticalLayout_2.addWidget(self.int_blobs)
        self.verticalLayout_5.addLayout(self.verticalLayout_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.trig_avg_spin = QtWidgets.QSpinBox(Form)
        self.trig_avg_spin.setMaximum(10)
        self.trig_avg_spin.setSingleStep(1)
        self.trig_avg_spin.setProperty("value", 0)
        self.trig_avg_spin.setObjectName("trig_avg_spin")
        self.gridLayout.addWidget(self.trig_avg_spin, 2, 0, 1, 1)
        self.avg_roi = QtWidgets.QCheckBox(Form)
        self.avg_roi.setObjectName("avg_roi")
        self.gridLayout.addWidget(self.avg_roi, 2, 1, 1, 1)
        self.int_blobs_roi = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.int_blobs_roi.setFont(font)
        self.int_blobs_roi.setAlignment(QtCore.Qt.AlignCenter)
        self.int_blobs_roi.setObjectName("int_blobs_roi")
        self.gridLayout.addWidget(self.int_blobs_roi, 3, 0, 1, 2)
        self.label_int_blobs_roi = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setUnderline(True)
        self.label_int_blobs_roi.setFont(font)
        self.label_int_blobs_roi.setAlignment(QtCore.Qt.AlignCenter)
        self.label_int_blobs_roi.setObjectName("label_int_blobs_roi")
        self.gridLayout.addWidget(self.label_int_blobs_roi, 0, 0, 1, 2)
        self.verticalLayout_5.addLayout(self.gridLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_5 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setUnderline(True)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.cos_theta = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.cos_theta.setFont(font)
        self.cos_theta.setAlignment(QtCore.Qt.AlignCenter)
        self.cos_theta.setObjectName("cos_theta")
        self.verticalLayout_3.addWidget(self.cos_theta)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_9 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setUnderline(True)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_4.addWidget(self.label_9)
        self.cos2_theta = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.cos2_theta.setFont(font)
        self.cos2_theta.setAlignment(QtCore.Qt.AlignCenter)
        self.cos2_theta.setObjectName("cos2_theta")
        self.verticalLayout_4.addWidget(self.cos2_theta)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        spacerItem = QtWidgets.QSpacerItem(17, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_5.addWidget(self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(Form)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout_5.addWidget(self.checkBox_2)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.histo_binning = QtWidgets.QSpinBox(Form)
        self.histo_binning.setMinimum(8)
        self.histo_binning.setMaximum(1024)
        self.histo_binning.setProperty("value", 256)
        self.histo_binning.setDisplayIntegerBase(10)
        self.histo_binning.setObjectName("histo_binning")
        self.verticalLayout_5.addWidget(self.histo_binning)
        self.x0_label = QtWidgets.QLabel(Form)
        self.x0_label.setObjectName("x0_label")
        self.verticalLayout_5.addWidget(self.x0_label)
        self.x0_spin = QtWidgets.QSpinBox(Form)
        self.x0_spin.setMaximum(255)
        self.x0_spin.setProperty("value", 127)
        self.x0_spin.setObjectName("x0_spin")
        self.verticalLayout_5.addWidget(self.x0_spin)
        self.y0_label = QtWidgets.QLabel(Form)
        self.y0_label.setObjectName("y0_label")
        self.verticalLayout_5.addWidget(self.y0_label)
        self.y0_spin = QtWidgets.QSpinBox(Form)
        self.y0_spin.setMaximum(255)
        self.y0_spin.setProperty("value", 127)
        self.y0_spin.setObjectName("y0_spin")
        self.verticalLayout_5.addWidget(self.y0_spin)
        self.radius_label = QtWidgets.QLabel(Form)
        self.radius_label.setObjectName("radius_label")
        self.verticalLayout_5.addWidget(self.radius_label)
        self.r_inner = QtWidgets.QSpinBox(Form)
        self.r_inner.setMinimum(0)
        self.r_inner.setMaximum(255)
        self.r_inner.setProperty("value", 0)
        self.r_inner.setObjectName("r_inner")
        self.verticalLayout_5.addWidget(self.r_inner)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2)
        self.r_outer = QtWidgets.QSpinBox(Form)
        self.r_outer.setMaximum(300)
        self.r_outer.setProperty("value", 300)
        self.r_outer.setObjectName("r_outer")
        self.verticalLayout_5.addWidget(self.r_outer)
        self.maxRangeLabel = QtWidgets.QLabel(Form)
        self.maxRangeLabel.setEnabled(False)
        self.maxRangeLabel.setObjectName("maxRangeLabel")
        self.verticalLayout_5.addWidget(self.maxRangeLabel)
        self.maxRangeSpinBox = QtWidgets.QDoubleSpinBox(Form)
        self.maxRangeSpinBox.setEnabled(False)
        self.maxRangeSpinBox.setMaximum(1e+142)
        self.maxRangeSpinBox.setProperty("value", 0.0)
        self.maxRangeSpinBox.setObjectName("maxRangeSpinBox")
        self.verticalLayout_5.addWidget(self.maxRangeSpinBox)
        self.show_centroids = QtWidgets.QCheckBox(Form)
        self.show_centroids.setEnabled(False)
        self.show_centroids.setObjectName("show_centroids")
        self.verticalLayout_5.addWidget(self.show_centroids)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.blob_trend_check = QtWidgets.QCheckBox(Form)
        self.blob_trend_check.setEnabled(True)
        self.blob_trend_check.setChecked(True)
        self.blob_trend_check.setObjectName("blob_trend_check")
        self.horizontalLayout_6.addWidget(self.blob_trend_check)
        self.roi_trend_check = QtWidgets.QCheckBox(Form)
        self.roi_trend_check.setChecked(True)
        self.roi_trend_check.setObjectName("roi_trend_check")
        self.horizontalLayout_6.addWidget(self.roi_trend_check)
        self.show_center = QtWidgets.QCheckBox(Form)
        self.show_center.setObjectName("show_center")
        self.horizontalLayout_6.addWidget(self.show_center)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_61 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_61.setObjectName("horizontalLayout_61")
        self.blob_trend = PlotWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.blob_trend.sizePolicy().hasHeightForWidth())
        self.blob_trend.setSizePolicy(sizePolicy)
        self.blob_trend.setMaximumSize(QtCore.QSize(1100000, 3000))
        self.blob_trend.setObjectName("blob_trend")
        self.horizontalLayout_61.addWidget(self.blob_trend)
        self.blob_trend_roi = PlotWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.blob_trend_roi.sizePolicy().hasHeightForWidth())
        self.blob_trend_roi.setSizePolicy(sizePolicy)
        self.blob_trend_roi.setMaximumSize(QtCore.QSize(1100000, 3000))
        self.blob_trend_roi.setObjectName("blob_trend_roi")
        self.horizontalLayout_61.addWidget(self.blob_trend_roi)
        self.verticalLayout_6.addLayout(self.horizontalLayout_61)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "Blobs per shot"))
        self.rec_blobs.setText(_translate("Form", "0"))
        self.label_4.setText(_translate("Form", "Integrated Blobs"))
        self.int_blobs.setText(_translate("Form", "0"))
        self.avg_roi.setText(_translate("Form", "avg"))
        self.int_blobs_roi.setText(_translate("Form", "0"))
        self.label_int_blobs_roi.setText(_translate("Form", "Int. Blobs ROI"))
        self.label_5.setText(_translate("Form", "cos theta"))
        self.cos_theta.setText(_translate("Form", "0"))
        self.label_9.setText(_translate("Form", "cos2 theta"))
        self.cos2_theta.setText(_translate("Form", "0"))
        self.checkBox.setText(_translate("Form", "Histogram"))
        self.checkBox_2.setText(_translate("Form", "Pixel histogram"))
        self.label.setText(_translate("Form", "Binning"))
        self.x0_label.setText(_translate("Form", "y0"))
        self.y0_label.setText(_translate("Form", "x0"))
        self.radius_label.setText(_translate("Form", "inner-radius"))
        self.label_2.setText(_translate("Form", "outer-radius"))
        self.maxRangeLabel.setToolTip(_translate("Form", "<html><head/><body><p>Maximal intensity. Zero algoritjm scales to maximal value dynamically.</p></body></html>"))
        self.maxRangeLabel.setText(_translate("Form", "max range"))
        self.show_centroids.setText(_translate("Form", "show centroids"))
        self.blob_trend_check.setText(_translate("Form", "Show Blob Trend"))
        self.roi_trend_check.setText(_translate("Form", "Show ROI trend"))
        self.show_center.setText(_translate("Form", "Show Crosshair"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pymepixviewer\panels\ui\timeofflightpanel.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from pyqtgraph import PlotWidget


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(749, 301)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tof_view = PlotWidget(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tof_view.sizePolicy().hasHeightForWidth())
        self.tof_view.setSizePolicy(sizePolicy)
        self.tof_view.setObjectName("tof_view")
        self.horizontalLayout_4.addWidget(self.tof_view)
        self.verticalLayout_5.addWidget(self.groupBox_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.roi_list = QtWidgets.QTreeView(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.roi_list.sizePolicy().hasHeightForWidth())
        self.roi_list.setSizePolicy(sizePolicy)
        self.roi_list.setMaximumSize(QtCore.QSize(299, 88))
        self.roi_list.setObjectName("roi_list")
        self.verticalLayout.addWidget(self.roi_list)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_roi = QtWidgets.QPushButton(Form)
        self.add_roi.setObjectName("add_roi")
        self.horizontalLayout.addWidget(self.add_roi)
        self.remove_roi = QtWidgets.QPushButton(Form)
        self.remove_roi.setObjectName("remove_roi")
        self.horizontalLayout.addWidget(self.remove_roi)
        self.display_roi = QtWidgets.QPushButton(Form)
        self.display_roi.setObjectName("display_roi")
        self.horizontalLayout.addWidget(self.display_roi)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.event_start = QtWidgets.QLineEdit(self.groupBox_2)
        self.event_start.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.event_start.setObjectName("event_start")
        self.horizontalLayout_2.addWidget(self.event_start)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.event_end = QtWidgets.QLineEdit(self.groupBox_2)
        self.event_end.setObjectName("event_end")
        self.horizontalLayout_2.addWidget(self.event_end)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.bin_size = QtWidgets.QLineEdit(self.groupBox_2)
        self.bin_size.setObjectName("bin_size")
        self.horizontalLayout_3.addWidget(self.bin_size)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.blob_tof = QtWidgets.QCheckBox(self.groupBox_2)
        self.blob_tof.setObjectName("blob_tof")
        self.verticalLayout_3.addWidget(self.blob_tof)
        spacerItem = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        self.verticalLayout_3.addItem(spacerItem)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.update_config = QtWidgets.QPushButton(Form)
        self.update_config.setObjectName("update_config")
        self.verticalLayout_4.addWidget(self.update_config)
        self.horizontalLayout_5.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_3.setTitle(_translate("Form", "Time of Flight"))
        self.groupBox.setTitle(_translate("Form", "Regions of Interest"))
        self.add_roi.setText(_translate("Form", "Add"))
        self.remove_roi.setText(_translate("Form", "Remove"))
        self.display_roi.setText(_translate("Form", "Display"))
        self.groupBox_2.setTitle(_translate("Form", "Time of Flight Config"))
        self.label.setText(_translate("Form", "Event Window:"))
        self.label_2.setText(_translate("Form", "-"))
        self.label_4.setText(_translate("Form", "us"))
        self.label_3.setText(_translate("Form", "Binning"))
        self.blob_tof.setText(_translate("Form", "Use Centroid TOF"))
        self.update_config.setText(_translate("Form", "Update"))

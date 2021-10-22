# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './pymepix-viewer/pymepixviewer/panels/ui/processingconfig.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(506, 301)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.min_event_window = QtWidgets.QLineEdit(self.groupBox_3)
        self.min_event_window.setObjectName("min_event_window")
        self.horizontalLayout_4.addWidget(self.min_event_window)
        self.max_event_window = QtWidgets.QLineEdit(self.groupBox_3)
        self.max_event_window.setObjectName("max_event_window")
        self.horizontalLayout_4.addWidget(self.max_event_window)
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_4.addWidget(self.label_10)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(Form)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_queue_size = QtWidgets.QLabel(self.groupBox_4)
        self.label_queue_size.setObjectName("label_queue_size")
        self.horizontalLayout.addWidget(self.label_queue_size)
        self.lcd_queue_size = QtWidgets.QLCDNumber(self.groupBox_4)
        self.lcd_queue_size.setObjectName("lcd_queue_size")
        self.horizontalLayout.addWidget(self.lcd_queue_size)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_7 = QtWidgets.QLabel(self.groupBox_4)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_5.addWidget(self.label_7)
        self.triggers_processed = QtWidgets.QSpinBox(self.groupBox_4)
        self.triggers_processed.setMinimum(1)
        self.triggers_processed.setObjectName("triggers_processed")
        self.horizontalLayout_5.addWidget(self.triggers_processed)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_9 = QtWidgets.QLabel(self.groupBox_4)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_6.addWidget(self.label_9)
        self.number_processes = QtWidgets.QLineEdit(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.number_processes.sizePolicy().hasHeightForWidth()
        )
        self.number_processes.setSizePolicy(sizePolicy)
        self.number_processes.setObjectName("number_processes")
        self.horizontalLayout_6.addWidget(self.number_processes)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_11 = QtWidgets.QLabel(self.groupBox_4)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_7.addWidget(self.label_11)
        self.epsilon = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.epsilon.setProperty("value", 2.0)
        self.epsilon.setObjectName("epsilon")
        self.horizontalLayout_7.addWidget(self.epsilon)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_12 = QtWidgets.QLabel(self.groupBox_4)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_8.addWidget(self.label_12)
        self.min_samples = QtWidgets.QSpinBox(self.groupBox_4)
        self.min_samples.setProperty("value", 3)
        self.min_samples.setObjectName("min_samples")
        self.horizontalLayout_8.addWidget(self.min_samples)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_8 = QtWidgets.QLabel(self.groupBox_4)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_10.addWidget(self.label_8)
        self.tot_threshold = QtWidgets.QSpinBox(self.groupBox_4)
        self.tot_threshold.setMinimum(0)
        self.tot_threshold.setMaximum(30000)
        self.tot_threshold.setSingleStep(25)
        self.tot_threshold.setObjectName("tot_threshold")
        self.horizontalLayout_10.addWidget(self.tot_threshold)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.verticalLayout_4.addWidget(self.groupBox_4)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        spacerItem = QtWidgets.QSpacerItem(
            20, 44, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_3.setTitle(_translate("Form", "Pixel Processing"))
        self.label_6.setText(_translate("Form", "Event window:"))
        self.min_event_window.setText(_translate("Form", "0"))
        self.max_event_window.setText(_translate("Form", "10000"))
        self.label_10.setText(_translate("Form", "us"))
        self.groupBox_4.setTitle(_translate("Form", "Centroiding"))
        self.label_queue_size.setToolTip(_translate("Form", "Not working with MacOS!"))
        self.label_queue_size.setText(_translate("Form", "Input Queue Size:"))
        self.lcd_queue_size.setToolTip(_translate("Form", "Not working with MacOS!"))
        self.label_7.setText(_translate("Form", "Triggers Processed:"))
        self.triggers_processed.setToolTip(
            _translate(
                "Form",
                "Process every nth trigger frame (1 means all are processed, 2 means every second is processed)",
            )
        )
        self.label_9.setText(_translate("Form", "Number Processe:"))
        self.number_processes.setToolTip(
            _translate(
                "Form",
                "Number of processes used for centroiding (Press Enter to confirm)",
            )
        )
        self.label_11.setText(_translate("Form", "Epsilon:"))
        self.epsilon.setToolTip(
            _translate(
                "Form", "Describes the distance between events (DBSCAN parameter)"
            )
        )
        self.label_12.setText(_translate("Form", "Minimum Samples"))
        self.min_samples.setToolTip(
            _translate(
                "Form",
                "Minimum number of samples for a core cluster point (DBSCAN parameter)",
            )
        )
        self.label_8.setText(_translate("Form", "TOT threshold:"))
        self.tot_threshold.setToolTip(
            _translate(
                "Form",
                "Threshold on the TOT to improve the results and reduce the data volume",
            )
        )

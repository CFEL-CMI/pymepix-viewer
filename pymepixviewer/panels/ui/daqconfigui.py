# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'daqconfig.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(541, 510)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.acqtab = AcquisitionConfig()
        self.acqtab.setObjectName("acqtab")
        self.tabWidget.addTab(self.acqtab, "")
        self.viewtab = ViewerConfig()
        self.viewtab.setObjectName("viewtab")
        self.tabWidget.addTab(self.viewtab, "")
        self.proctab = ProcessingConfig()
        self.proctab.setObjectName("proctab")
        self.tabWidget.addTab(self.proctab, "")
        self.verticalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.acqtab), _translate("Form", "Acquisition"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.viewtab), _translate("Form", "Viewer"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.proctab), _translate("Form", "Processing"))
from pymepixviewer.panels.acqconfig import AcquisitionConfig
from pymepixviewer.panels.processingconfig import ProcessingConfig
from pymepixviewer.panels.viewerconfig import ViewerConfig

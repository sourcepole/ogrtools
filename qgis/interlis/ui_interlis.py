# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_interlis.ui'
#
# Created: Sat Jan 18 23:30:48 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Interlis(object):
    def setupUi(self, Interlis):
        Interlis.setObjectName(_fromUtf8("Interlis"))
        Interlis.resize(406, 287)
        self.verticalLayout = QtGui.QVBoxLayout(Interlis)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(Interlis)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.importtab = QtGui.QWidget()
        self.importtab.setObjectName(_fromUtf8("importtab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.importtab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton = QtGui.QPushButton(self.importtab)
        self.pushButton.setEnabled(False)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)
        self.mDataFileLabel = QtGui.QLabel(self.importtab)
        self.mDataFileLabel.setObjectName(_fromUtf8("mDataFileLabel"))
        self.gridLayout.addWidget(self.mDataFileLabel, 0, 0, 1, 1)
        self.mDataLineEdit = QtGui.QLineEdit(self.importtab)
        self.mDataLineEdit.setObjectName(_fromUtf8("mDataLineEdit"))
        self.gridLayout.addWidget(self.mDataLineEdit, 0, 1, 1, 1)
        self.cbDbConnections = QtGui.QComboBox(self.importtab)
        self.cbDbConnections.setObjectName(_fromUtf8("cbDbConnections"))
        self.gridLayout.addWidget(self.cbDbConnections, 4, 1, 1, 1)
        self.mModelFileLabel = QtGui.QLabel(self.importtab)
        self.mModelFileLabel.setObjectName(_fromUtf8("mModelFileLabel"))
        self.gridLayout.addWidget(self.mModelFileLabel, 2, 0, 1, 1)
        self.mDataFileButton = QtGui.QPushButton(self.importtab)
        self.mDataFileButton.setObjectName(_fromUtf8("mDataFileButton"))
        self.gridLayout.addWidget(self.mDataFileButton, 0, 2, 1, 1)
        self.mModelLineEdit = QtGui.QLineEdit(self.importtab)
        self.mModelLineEdit.setObjectName(_fromUtf8("mModelLineEdit"))
        self.gridLayout.addWidget(self.mModelLineEdit, 2, 1, 1, 1)
        self.mModelFileButton = QtGui.QPushButton(self.importtab)
        self.mModelFileButton.setObjectName(_fromUtf8("mModelFileButton"))
        self.gridLayout.addWidget(self.mModelFileButton, 2, 2, 1, 1)
        self.label = QtGui.QLabel(self.importtab)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.frame = QtGui.QFrame(self.importtab)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.pushButton_2 = QtGui.QPushButton(self.frame)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout_3.addWidget(self.pushButton_2, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(self.frame)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_3.addWidget(self.buttonBox, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 3, 0, 1, 1)
        self.tabWidget.addTab(self.importtab, _fromUtf8(""))
        self.exporttab = QtGui.QWidget()
        self.exporttab.setObjectName(_fromUtf8("exporttab"))
        self.tabWidget.addTab(self.exporttab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Interlis)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Interlis.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Interlis.reject)
        QtCore.QMetaObject.connectSlotsByName(Interlis)

    def retranslateUi(self, Interlis):
        Interlis.setWindowTitle(QtGui.QApplication.translate("Interlis", "Interlis", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Interlis", "Model Lookup", None, QtGui.QApplication.UnicodeUTF8))
        self.mDataFileLabel.setText(QtGui.QApplication.translate("Interlis", "Data file:", None, QtGui.QApplication.UnicodeUTF8))
        self.mModelFileLabel.setText(QtGui.QApplication.translate("Interlis", "IlisMeta Model:", None, QtGui.QApplication.UnicodeUTF8))
        self.mDataFileButton.setText(QtGui.QApplication.translate("Interlis", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.mModelFileButton.setText(QtGui.QApplication.translate("Interlis", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Interlis", "Database:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Interlis", "Import Enums", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.importtab), QtGui.QApplication.translate("Interlis", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.exporttab), QtGui.QApplication.translate("Interlis", "Export", None, QtGui.QApplication.UnicodeUTF8))


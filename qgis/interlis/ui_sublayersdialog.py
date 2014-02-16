# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_sublayersdialog.ui'
#
# Created: Sun Feb 16 23:08:06 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SublayersDialog(object):
    def setupUi(self, SublayersDialog):
        SublayersDialog.setObjectName(_fromUtf8("SublayersDialog"))
        SublayersDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(SublayersDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.mSublayersTreeWidget = QtGui.QTreeWidget(SublayersDialog)
        self.mSublayersTreeWidget.setObjectName(_fromUtf8("mSublayersTreeWidget"))
        self.mSublayersTreeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.gridLayout.addWidget(self.mSublayersTreeWidget, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SublayersDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(SublayersDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SublayersDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SublayersDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SublayersDialog)

    def retranslateUi(self, SublayersDialog):
        SublayersDialog.setWindowTitle(QtGui.QApplication.translate("SublayersDialog", "Interlis sublayers", None, QtGui.QApplication.UnicodeUTF8))


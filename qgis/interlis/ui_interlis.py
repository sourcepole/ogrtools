# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_interlis.ui'
#
# Created: Sat Jan 18 22:38:23 2014
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
        Interlis.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(Interlis)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        self.retranslateUi(Interlis)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Interlis.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Interlis.reject)
        QtCore.QMetaObject.connectSlotsByName(Interlis)

    def retranslateUi(self, Interlis):
        Interlis.setWindowTitle(QtGui.QApplication.translate("Interlis", "Interlis", None, QtGui.QApplication.UnicodeUTF8))


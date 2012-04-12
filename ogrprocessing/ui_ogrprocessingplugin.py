# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_ogrprocessingplugin.ui'
#
# Created: Thu Apr 12 11:35:45 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_OgrProcessingPlugin(object):
    def setupUi(self, OgrProcessingPlugin):
        OgrProcessingPlugin.setObjectName(_fromUtf8("OgrProcessingPlugin"))
        OgrProcessingPlugin.resize(400, 300)
        OgrProcessingPlugin.setWindowTitle(QtGui.QApplication.translate("OgrProcessingPlugin", "OgrProcessingPlugin", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonBox = QtGui.QDialogButtonBox(OgrProcessingPlugin)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        self.retranslateUi(OgrProcessingPlugin)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), OgrProcessingPlugin.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), OgrProcessingPlugin.reject)
        QtCore.QMetaObject.connectSlotsByName(OgrProcessingPlugin)

    def retranslateUi(self, OgrProcessingPlugin):
        pass


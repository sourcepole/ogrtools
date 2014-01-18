# -*- coding: utf-8 -*-
"""
/***************************************************************************
 InterlisDialog
                                 A QGIS plugin
 Interlis Import/Export
                             -------------------
        begin                : 2014-01-18
        copyright            : (C) 2014 by Pirmin Kalberer / Sourcepole
        email                : pka@sourcepole.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, QSettings, QFileInfo
from PyQt4.QtGui import QFileDialog, QDialogButtonBox
from ui_interlis import Ui_Interlis


class InterlisDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Interlis()
        self.ui.setupUi(self)

    def dataSourceUri(self):
        if self.ui.mDataLineEdit.text().isEmpty():
            return ""
        if not self.ui.mModelLineEdit.text().isEmpty():
            return self.ui.mDataLineEdit.text() + "," + self.ui.mModelLineEdit.text()
        else:
            return self.ui.mDataLineEdit.text()

    @pyqtSignature('')  # avoid two connections
    def on_mDataFileButton_clicked(self):
        #show file dialog and remember last directory
        settings = QSettings()
        lastDirectoryString = None  # settings.value("/qgis/plugins/interlis/datadir", type=str)
        dataFilePath = QFileDialog.getOpenFileName(None, "Open Interlis data file", lastDirectoryString, "*.itf *.ITF *.xtf *.XTF *.xml")
        if dataFilePath is None:
            return  # dialog canceled
        settings.setValue("/qgis/plugins/interlis/datadir", QFileInfo(dataFilePath).absolutePath())
        self.ui.mDataLineEdit.insert(dataFilePath)
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    @pyqtSignature('')  # avoid two connections
    def on_mModelFileButton_clicked(self):
        #show file dialog and remember last directory
        settings = QSettings()
        lastDirectoryString = None  # settings.value("/qgis/plugins/interlis2/modeldir", type=str)
        modelFilePath = QFileDialog.getOpenFileName(None, "Open Interlis data file", lastDirectoryString, "*.imd *.IMD")
        if modelFilePath is None:
            return  # dialog canceled
        settings.setValue("/qgis/plugins/interlis/modeldir", QFileInfo(modelFilePath).absolutePath())
        self.ui.mModelLineEdit.insert(modelFilePath)

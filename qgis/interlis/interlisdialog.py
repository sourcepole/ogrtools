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
from PyQt4.QtGui import QFileDialog
from qgis.core import QgsMessageLog
from ui_interlis import Ui_Interlis
import os.path
import tempfile
from ogrtools.ogrtransform.ogrconfig import OgrConfig
from ogrtools.ogrtransform.transformation import Transformation


class InterlisDialog(QtGui.QDialog):
    def __init__(self, interlis):
        QtGui.QDialog.__init__(self)
        self._interlis = interlis
        # Set up the user interface from Designer.
        self.ui = Ui_Interlis()
        self.ui.setupUi(self)
        #Not implemented yet:
        self.ui.chkModelLookup.setEnabled(False)
        self.ui.label_2.setEnabled(False)
        self.ui.mConfigButton.setEnabled(False)
        self.ui.mConfigLineEdit.setEnabled(False)
        self.ui.cbResetData.setEnabled(False)

    def show(self):
        #Initialize DB connection drop-down
        self.ui.cbDbConnections.clear()
        self.ui.cbDbConnections.addItem("QGIS Layer")
        self.ui.cbDbConnections.addItems(self.dbConnectionList())
        QtGui.QDialog.show(self)

    def dataSourceUri(self):
        if self.ui.mDataLineEdit.text().isEmpty():
            return ""
        if not self.ui.mModelLineEdit.text().isEmpty():
            return self.ui.mDataLineEdit.text() + "," + self.ui.mModelLineEdit.text()
        else:
            return self.ui.mDataLineEdit.text()

    def ogrDs(self):
        key = u"/PostgreSQL/connections/" + self.ui.cbDbConnections.currentText()
        settings = QSettings()
        settings.beginGroup(key)
        params = {
            'host': settings.value("host", type=str),
            'port': settings.value("port", type=str),
            'dbname': settings.value("database", type=str),
            'username': settings.value("username", type=str),
            'password': settings.value("password", type=str)
        }
        ds = 'PG:'
        for k, v in params.items():
            if v:
                ds = ds + k + "='" + v + "' "
        return ds

    def dbConnectionList(self):
        connection_names = []
        settings = QSettings()
        settings.beginGroup(u"/PostgreSQL/connections")
        for name in settings.childGroups():
            connection_names.append(name)
        settings.endGroup()
        return connection_names

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
        self.ui.mImportButton.setEnabled(True)

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

    @pyqtSignature('')  # avoid two connections
    def on_mImportButton_clicked(self):
        self.importtodb()

    def importtodb(self):
        format = 'PostgreSQL'
        ilids = self.ui.mDataLineEdit.text() + ',' + self.ui.mModelLineEdit.text()
        QgsMessageLog.logMessage(ilids, "Interlis", QgsMessageLog.INFO)
        trans = OgrConfig(ds=ilids, model=self.ui.mModelLineEdit.text())
        ogrconfig = self.ui.mConfigLineEdit.text()
        if not ogrconfig:
            ogrconfig = os.path.join(tempfile.gettempdir(), "ogrconfig.json")
            cfgjson = trans.generate_config(format, outfile=ogrconfig, layer_list=[])
            QgsMessageLog.logMessage(cfgjson, "Interlis", QgsMessageLog.INFO)
            self.ui.mConfigLineEdit.setText(ogrconfig)
        trans = Transformation(ogrconfig, ilids)
        trans.transform(dest=self.ogrDs(), debug=True)
        self._interlis.messageLogWidget().show()
        QgsMessageLog.logMessage("Import finished", "Interlis", QgsMessageLog.INFO)

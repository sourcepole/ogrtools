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
from PyQt4.QtGui import QFileDialog, QMessageBox, QDialog
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsDataSourceURI
from qgis.gui import QgsMessageBar
from ui_interlis import Ui_Interlis
from sublayersdialog import SublayersDialog
import os.path
import tempfile
from ogrtools.ogrtransform.ogrconfig import OgrConfig


class InterlisDialog(QtGui.QDialog):
    def __init__(self, plugin):
        QtGui.QDialog.__init__(self)
        self._plugin = plugin
        # Set up the user interface from Designer.
        self.ui = Ui_Interlis()
        self.ui.setupUi(self)
        #Not implemented yet:
        self.ui.mModelLookupButton.setEnabled(False)
        self.ui.cbResetData.setEnabled(False)
        #Initialize DB connection drop-down
        self.ui.cbDbConnections.clear()
        self.ui.cbDbConnections.addItem("QGIS Layer")
        self.ui.cbDbConnections.addItems(self.dbConnectionList())

    def setup(self):
        self.ui.mDataLineEdit.setText("")

    def iliDs(self):
        """OGR connection string for selected Interlis transfer file + model"""
        if not self.ui.mDataLineEdit.text():
            return ""
        if self.ui.mModelLineEdit.text():
            return self.ui.mDataLineEdit.text() + "," + self.ui.mModelLineEdit.text()
        else:
            return self.ui.mDataLineEdit.text()

    def pgDs(self):
        """OGR connection string for selected PostGIS DB"""
        key = u"/PostgreSQL/connections/" + self.ui.cbDbConnections.currentText()
        settings = QSettings()
        settings.beginGroup(key)
        params = {
            'host': settings.value("host", type=str),
            'port': settings.value("port", type=str),
            'dbname': settings.value("database", type=str),
            'user': settings.value("username", type=str),
            'password': settings.value("password", type=str)
        }
        ds = 'PG:'
        for k, v in params.items():
            if v:
                ds = ds + k + "='" + v + "' "
        return ds

    def pgUri(self):
        """QgsDataSourceURI for selected PostGIS DB"""
        key = u"/PostgreSQL/connections/" + self.ui.cbDbConnections.currentText()
        settings = QSettings()
        settings.beginGroup(key)
        uri = QgsDataSourceURI()
        uri.setConnection(
            settings.value("host", type=str),
            settings.value("port", type=str),
            settings.value("database", type=str),
            settings.value("username", type=str),
            settings.value("password", type=str),
            QgsDataSourceURI.SSLmode(settings.value("sslmode", type=int))
        )
        uri.setUseEstimatedMetadata(settings.value("estimatedMetadata", type=bool))
        return uri

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
        dataFilePath = QFileDialog.getOpenFileName(None, "Open Interlis data file", lastDirectoryString,
                                                   "*.itf *.ITF *.xtf *.XTF *.xml")
        if dataFilePath is None:
            return  # dialog canceled
        settings.setValue("/qgis/plugins/interlis/datadir", QFileInfo(dataFilePath).absolutePath())
        self.ui.mDataLineEdit.setText(dataFilePath)
        self.ui.mImportButton.setEnabled(True)

    @pyqtSignature('')  # avoid two connections
    def on_mModelFileButton_clicked(self):
        #show file dialog and remember last directory
        settings = QSettings()
        lastDirectoryString = None  # settings.value("/qgis/plugins/interlis2/modeldir", type=str)
        modelFilePath = QFileDialog.getOpenFileName(None, "Open Interlis data file", lastDirectoryString,
                                                    "*.imd *.IMD")
        if modelFilePath is None:
            return  # dialog canceled
        settings.setValue("/qgis/plugins/interlis/modeldir", QFileInfo(modelFilePath).absolutePath())
        self.ui.mModelLineEdit.setText(modelFilePath)

    @pyqtSignature('')  # avoid two connections
    def on_mConfigButton_clicked(self):
        #show file dialog and remember last directory
        settings = QSettings()
        lastDirectoryString = None  # settings.value("/qgis/plugins/interlis2/cfgdir", type=str)
        configPath = QFileDialog.getOpenFileName(None, "Open OGR mapping config file", lastDirectoryString,
                                                 "*.cfg *.CFG", ".json", ".JSON")
        if configPath is None:
            return  # dialog canceled
        settings.setValue("/qgis/plugins/interlis/cfgdir", QFileInfo(configPath).absolutePath())
        self.ui.mConfigLineEdit.setText(configPath)

    def on_mModelLineEdit_textChanged(self):
        self.ui.mConfigLineEdit.clear()

    @pyqtSignature('')  # avoid two connections
    def on_mImportButton_clicked(self):
        if self.ui.cbDbConnections.currentIndex() == 0:
            self.importtoqgis()
        else:
            self.importtodb()

    @pyqtSignature('')  # avoid two connections
    def on_mExportButton_clicked(self):
        self.exporttoxtf()

    def _ogr_config(self, ds):
        ogrconfig = self.ui.mConfigLineEdit.text()
        if ogrconfig:
            cfg = OgrConfig(ds=ds, config=ogrconfig)
        else:
            cfg = OgrConfig(ds=ds, model=self.ui.mModelLineEdit.text())
        return cfg

    def importtoqgis(self):
        dataSourceUri = self.iliDs()
        subLayerVectorLayer = QgsVectorLayer(dataSourceUri, "interlis_sublayers", "ogr")
        subLayerProvider = subLayerVectorLayer.dataProvider()
        if not subLayerProvider:
            QMessageBox.critical(None, "Error accessing interlis sublayers",
                                 "A problem occured during access of the sublayers")
            return
        #QGIS 1.8:
        #subLayerList = subLayerProvider.subLayers()
        #subLayerDialog = SublayersDialog()
        #subLayerDialog.setupSublayerList(subLayerList)
        #if subLayerDialog.exec_() == QDialog.Accepted:
        #    for layername in subLayerDialog.subLayerNames():
        #            #add a new ogr layer for each selected sublayer
        #        self._plugin.iface.addVectorLayer(dataSourceUri + "|layername=" + layername, layername, "ogr")
        #QGIS 2: Sublayer dialog opens automatically
        #Bug in 2.0 causes crash when adding sublayers
        self._plugin.iface.addVectorLayer(dataSourceUri, "Interlis layer", "ogr")
        self.accept()
        self._plugin.iface.messageBar().pushMessage("Interlis", "Import finished",
                                                    level=QgsMessageBar.INFO, duration=2)

    def importtodb(self):
        QgsMessageLog.logMessage(self.iliDs(), "Interlis", QgsMessageLog.INFO)
        cfg = self._ogr_config(self.iliDs())
        if not cfg.is_loaded():
            ogrconfig = os.path.join(tempfile.gettempdir(), "ogrconfig.json")
            format = 'PostgreSQL'
            cfgjson = cfg.generate_config(format, outfile=ogrconfig, layer_list=[])
            QgsMessageLog.logMessage(cfgjson, "Interlis", QgsMessageLog.INFO)
            self.ui.mConfigLineEdit.setText(ogrconfig)
        if self.ui.cbImportEnums.isChecked():
            cfg.write_enum_tables(dest=self.pgDs(), skipfailures=self.ui.cbSkipFailures.isChecked(), debug=True)
        ogroutput = cfg.transform(dest=self.pgDs(), skipfailures=self.ui.cbSkipFailures.isChecked(), debug=True)
        self._plugin.messageLogWidget().show()
        self._log_output(ogroutput)
        QgsMessageLog.logMessage("Import finished", "Interlis", QgsMessageLog.INFO)
        self.ui.mExportButton.setEnabled(True)

        uri = self.pgUri()
        layer_infos = cfg.layer_infos()
        layer_names = cfg.layer_names()
        if self.ui.cbImportEnums.isChecked():
            layer_infos += cfg.enum_infos()
            layer_names += cfg.enum_names()
        subLayerDialog = SublayersDialog()
        subLayerDialog.setupLayerList(layer_names)
        if subLayerDialog.exec_() == QDialog.Accepted:
            for layer_id in subLayerDialog.layerNames():
                #add a new layer for each selected row
                for layer in layer_infos:
                    if layer['name'] == layer_id:
                        geom_column = layer['geom_field'] if ('geom_field' in layer) else None
                        uri.setDataSource("", layer['name'], geom_column)
                        self._plugin.iface.addVectorLayer(uri.uri(), layer['name'], 'postgres')
            self.accept()
            self._plugin.iface.messageBar().pushMessage("Interlis", "Import finished",
                                                        level=QgsMessageBar.INFO, duration=2)

    def exporttoxtf(self):
        cfg = self._ogr_config(self.pgDs())
        ogroutput = cfg.transform_reverse(dest=self.iliDs(), skipfailures=self.ui.cbSkipFailures.isChecked(), debug=True)
        self._log_output(ogroutput)
        QgsMessageLog.logMessage("Export to '%s' finished" % self.ui.mDataLineEdit.text(),
                                 "Interlis", QgsMessageLog.INFO)

    def _log_output(self, output, lines_per_msg=None):
        if lines_per_msg is None:
            QgsMessageLog.logMessage(output, "Interlis", QgsMessageLog.INFO)
        else:
            lines = output.splitlines()
            for i in range(0, len(lines), lines_per_msg):
                msg = "\n".join(lines[i:i + lines_per_msg])
                QgsMessageLog.logMessage(msg, "Interlis", QgsMessageLog.INFO)

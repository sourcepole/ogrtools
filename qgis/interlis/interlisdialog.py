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
from PyQt4.QtCore import pyqtSlot, Qt, QSettings, qDebug
from PyQt4.QtGui import QFileDialog, QMessageBox, QDialog, QDockWidget
from qgis.core import QGis, QgsMessageLog, QgsVectorLayer, QgsDataSourceURI
from qgis.gui import QgsMessageBar
from ui_interlis import Ui_Interlis
from sublayersdialog import SublayersDialog
import os.path
import tempfile
import urllib2
import codecs
from xml.etree import ElementTree
from pyqtconfig import QSettingsManager
from ogrtools.ogrtransform.ogrconfig import OgrConfig
from ogrtools.interlis.model_loader import ModelLoader
from ogrtools.interlis.ilismeta import ImdParser


class InterlisDialog(QtGui.QDialog):

    def __init__(self, plugin):
        QtGui.QDialog.__init__(self)
        self._plugin = plugin
        # Set up the user interface from Designer.
        self.ui = Ui_Interlis()
        self.ui.setupUi(self)

        # Initialize DB connection drop-down
        self.ui.cbDbConnections.clear()
        # Bug in 2.0 causes crash when adding sublayers
        if QGis.QGIS_VERSION_INT >= 20200:
            self.ui.cbDbConnections.addItem("QGIS Layer")
        self.ui.cbDbConnections.addItems(self.dbConnectionList())

        self._add_settings_handlers()

        self.ui.mCfgGroupBox.setCollapsed(self.ui.mConfigLineEdit.text() == "")
        self.ui.cbResetData.setEnabled(False)  # Not implemented yet

    def setup(self):
        self.ui.mDataLineEdit.setText("")

    def _add_settings_handlers(self):
        self._settings = QSettingsManager()
        self._settings.add_handler(
            'interlis/iliFile', self.ui.mIliLineEdit)
        self._settings.add_handler(
            'interlis/modelFile', self.ui.mModelLineEdit)
        #self._settings.add_handler(
        #    'interlis/dataFile', self.ui.mDataLineEdit)
        self._settings.add_handler(
            'interlis/dbConnection', self.ui.cbDbConnections)
        self._settings.add_handler(
            'interlis/configFile', self.ui.mConfigLineEdit)
        self._settings.add_handler(
            'interlis/ili2cPath', self.ui.mIli2cLineEdit)
        self._settings.add_handler(
            'interlis/skipFailures', self.ui.cbSkipFailures)

    def iliDs(self):
        """OGR connection string for selected Interlis transfer file + model"""
        return self.iliFileDs(self.ui.mDataLineEdit.text())

    def iliFileDs(self, fn):
        """OGR connection string for Interlis transfer file + model"""
        if not fn:
            return ""
        if self.ui.mModelLineEdit.text():
            return fn + "," + self.ui.mModelLineEdit.text()
        else:
            return fn

    def _empty_transfer_ds(self):
        imd = ImdParser(self.ui.mModelLineEdit.text())
        transferfn = imd.gen_empty_transfer_file()
        ds = transferfn + "," + self.ui.mModelLineEdit.text()
        return ds

    def pgDs(self):
        """OGR connection string for selected PostGIS DB"""
        key = u"/PostgreSQL/connections/" + \
            self.ui.cbDbConnections.currentText()
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
        key = u"/PostgreSQL/connections/" + \
            self.ui.cbDbConnections.currentText()
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
        uri.setUseEstimatedMetadata(
            settings.value("estimatedMetadata", type=bool))
        return uri

    def dbConnectionList(self):
        connection_names = []
        settings = QSettings()
        settings.beginGroup(u"/PostgreSQL/connections")
        for name in settings.childGroups():
            connection_names.append(name)
        settings.endGroup()
        return connection_names

    def _create_wps_request(self, ili):
        return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<wps:Execute service="WPS" version="1.0.0" xmlns:wps="http://www.opengis.net/wps/1.0.0" xmlns:ows="http://www.opengis.net/ows/1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 http://schemas.opengis.net/wps/1.0.0/wpsExecute_request.xsd">
<ows:Identifier>ilismetalookup</ows:Identifier>
<wps:DataInputs>
<wps:Input>
<ows:Identifier>ilimodel</ows:Identifier>
<ows:Title>ilimodel</ows:Title>
<wps:Data>
<wps:LiteralData>%s</wps:LiteralData>
</wps:Data>
</wps:Input>
</wps:DataInputs>
</wps:Execute>
        """ % ili

    def _parse_wps_response(self, xml):
        tree = ElementTree.ElementTree(ElementTree.fromstring(xml))
        ns = {"wps": "http://www.opengis.net/wps/1.0.0"}
        imd = tree.find(
            "wps:ProcessOutputs/wps:Output/wps:Data/wps:LiteralData", ns)
        if imd is None:
            return None
        else:
            return imd.text

    @pyqtSlot()
    def on_mDataFileButton_clicked(self):
        dataFilePath = QFileDialog.getOpenFileName(
            None, "Open Interlis data file", self.ui.mDataLineEdit.text(),
            "Interlis transfer file (*.itf *.ITF *.xtf *.XTF *.xml);;All files (*.*)")
        if not dataFilePath:
            return  # dialog canceled
        self.ui.mDataLineEdit.setText(dataFilePath)

    @pyqtSlot(str)
    def on_mDataLineEdit_textChanged(self, s):
        self.ui.mModelLookupButton.setEnabled(
            self.ui.mDataLineEdit.text() != "")
        self._update_data_import_button()

    def _update_data_import_button(self):
        self.ui.mImportButton.setEnabled(
            self.ui.mDataLineEdit.text() != "" and
            self.ui.mModelLineEdit.text() != "")

    @pyqtSlot()
    def on_mIliButton_clicked(self):
        iliFilePath = QFileDialog.getOpenFileName(
            None, "Open Interlis data file", self.ui.mIliLineEdit.text(),
            "Interlis model file (*.ili *.ILI);;All files (*.*)")
        if not iliFilePath:
            return  # dialog canceled
        self.ui.mIliLineEdit.setText(iliFilePath)

    @pyqtSlot(str)
    def on_mIliLineEdit_textChanged(self, s):
        self.ui.mCreateIlisMetaButton.setEnabled(
            self.ui.mIliLineEdit.text() != "")

    @pyqtSlot()
    def on_mCreateIlisMetaButton_clicked(self):
        loader = ModelLoader("")
        outfile = QFileDialog.getSaveFileName(
            None, "Save File", self.ui.mIliLineEdit.text(),
            "IlisMeta model (*.imd *.IMD)")
        if not outfile:
            return
        os.environ['ILI2C'] = self.ui.mIli2cLineEdit.text()
        ret = loader.convert_model([self.ui.mIliLineEdit.text()], outfile)
        err = ("Error:" in ret)
        self._show_log_window()
        self._log_output("IlisMeta creation: " + str(ret))
        if not err:
            self.ui.mModelLineEdit.setText(outfile)

    @pyqtSlot()
    def on_mModelLookupButton_clicked(self):
        imd = None
        try:
            loader = ModelLoader(self.ui.mDataLineEdit.text())
            models = loader.detect_models()
            model_names = map(lambda m: m.name, models)
            self._log_output("Looking up models: " + ', '.join(model_names))
            ili = loader.gen_lookup_ili()
            qDebug(ili)
            wpsreq = self._create_wps_request(ili)
            req = urllib2.Request(url="http://wps.sourcepole.ch/wps?",
                                  data=wpsreq,
                                  headers={'Content-Type': 'application/xml'})
            # TODO: proxy support
            response = urllib2.urlopen(req)  # timeout=int(TIMEOUT)
            result = response.read()
            imd = self._parse_wps_response(result)
        except urllib2.HTTPError, err:
            qDebug("HTTPError %d" % err.code)
        except:
            qDebug("Exception during IlisModel download")
        if imd is None:
            self._show_log_window()
            QgsMessageLog.logMessage(
                "Couldn't download Ilismeta model", "Interlis",
                QgsMessageLog.WARNING)
            self.ui.mModelLineEdit.setText("")
        else:
            fh, imdfn = tempfile.mkstemp(suffix='.imd')
            os.close(fh)
            with codecs.open(imdfn, "w", encoding='utf-8') as file:
                file.write(imd)
            self.ui.mModelLineEdit.setText(imdfn)

    @pyqtSlot()
    def on_mModelFileButton_clicked(self):
        modelFilePath = QFileDialog.getOpenFileName(
            None, "Open Interlis model file", self.ui.mModelLineEdit.text(),
            "IlisMeta model (*.imd *.IMD);;All files (*.*)")
        if not modelFilePath:
            return  # dialog canceled
        self.ui.mModelLineEdit.setText(modelFilePath)

    @pyqtSlot(str)
    def on_mModelLineEdit_textChanged(self, s):
        self.ui.mConfigLineEdit.clear()
        self._update_model_import_buttons()
        self._update_data_import_button()

    @pyqtSlot(int)
    def on_cbDbConnections_currentIndexChanged(self, v):
        self._update_model_import_buttons()

    def _update_model_import_buttons(self):
        self.ui.mImportEnumsButton.setEnabled(
            self.ui.mModelLineEdit.text() != "" and
            self.ui.cbDbConnections.currentIndex() != 0)  # DB conn. selected
        self.ui.mCreateSchemaButton.setEnabled(
            self.ui.mModelLineEdit.text() != "" and
            self.ui.cbDbConnections.currentIndex() != 0)  # DB conn. selected

    @pyqtSlot()
    def on_mConfigButton_clicked(self):
        configPath = QFileDialog.getOpenFileName(
            None, "Open OGR mapping config file",
            self.ui.mConfigLineEdit.text(),
            "OGR config (*.cfg *.CFG *.json *.JSON);;All files (*.*)")
        if not configPath:
            return  # dialog canceled
        self.ui.mConfigLineEdit.setText(configPath)

    @pyqtSlot(str)
    def on_mConfigLineEdit_textChanged(self, s):
        self.ui.mExportButton.setEnabled(self.ui.mConfigLineEdit.text() != "")

    @pyqtSlot()
    def on_mImportButton_clicked(self):
        self.setCursor(Qt.WaitCursor)
        try:
            if self.ui.cbDbConnections.currentText() == "QGIS Layer":
                self.importtoqgis()
            else:
                self.importtodb()
        finally:
            self.unsetCursor()

    @pyqtSlot()
    def on_mImportEnumsButton_clicked(self):
        self.setCursor(Qt.WaitCursor)
        try:
            self.importenums()
        finally:
            self.unsetCursor()

    @pyqtSlot()
    def on_mCreateSchemaButton_clicked(self):
        self.setCursor(Qt.WaitCursor)
        try:
            self.createschema()
        finally:
            self.unsetCursor()

    @pyqtSlot()
    def on_mExportButton_clicked(self):
        self.exporttoxtf()

    @pyqtSlot()
    def on_mIli2cPathButton_clicked(self):
        ili2c_path = QFileDialog.getOpenFileName(
            None, "Select path to ili2.jar", self.ui.mIli2cLineEdit.text(),
            "JAR file (*.jar *.JAR);;All files (*.*)")
        if not ili2c_path:
            return  # dialog canceled
        self.ui.mIli2cLineEdit.setText(ili2c_path)

    def _ogr_config(self, ds):
        ogrconfig = self.ui.mConfigLineEdit.text()
        self._log_output("_ogr_config ds: %s cfg: %s" % (ds, ogrconfig))
        if ogrconfig:
            cfg = OgrConfig(ds=ds, config=ogrconfig)
        else:
            cfg = OgrConfig(ds=ds, model=self.ui.mModelLineEdit.text())
        return cfg

    def _ogr_config_tmp(self, ds):
        self._ogrconfig_tmp = None
        cfg = self._ogr_config(ds)
        if not cfg.is_loaded():
            __, self._ogrconfig_tmp = tempfile.mkstemp('.cfg', 'ogr_')
            format = 'PostgreSQL'
            cfgjson = cfg.generate_config(
                format, outfile=self._ogrconfig_tmp, layer_list=[], srs="EPSG:21781")
            qDebug(cfgjson)
            self.ui.mConfigLineEdit.setText(self._ogrconfig_tmp)
        return cfg

    def _remove_ogrconfig_tmp(self):
        if self._ogrconfig_tmp is not None:
            os.remove(self._ogrconfig_tmp)
            self.ui.mConfigLineEdit.setText("")

    def importtoqgis(self):
        dataSourceUri = self.iliDs()
        subLayerVectorLayer = QgsVectorLayer(
            dataSourceUri, "interlis_sublayers", "ogr")
        subLayerProvider = subLayerVectorLayer.dataProvider()
        if not subLayerProvider:
            QMessageBox.critical(None, "Error accessing interlis sublayers",
                                 "A problem occured during access of the sublayers")
            return
        # QGIS 1.8:
        #subLayerList = subLayerProvider.subLayers()
        #subLayerDialog = SublayersDialog()
        # subLayerDialog.setupSublayerList(subLayerList)
        # if subLayerDialog.exec_() == QDialog.Accepted:
        #    for layername in subLayerDialog.subLayerNames():
        # add a new ogr layer for each selected sublayer
        #        self._plugin.iface.addVectorLayer(dataSourceUri + "|layername=" + layername, layername, "ogr")
        # QGIS 2: Sublayer dialog opens automatically
        self._plugin.iface.addVectorLayer(
            dataSourceUri, "Interlis layer", "ogr")
        self.accept()
        self._plugin.iface.messageBar().pushMessage("Interlis", "Import finished",
                                                    level=QgsMessageBar.INFO, duration=2)

    def importenums(self):
        cfg = self._ogr_config_tmp(self._empty_transfer_ds())
        self._log_output("Import Enums from %s" % self.ui.mModelLineEdit.text())
        cfg.write_enum_tables(
            dest=self.pgDs(), skipfailures=self.ui.cbSkipFailures.isChecked(), debug=True)
        self._remove_ogrconfig_tmp()
        self._log_output("Import finished")

    def createschema(self):
        cfg = self._ogr_config_tmp(self._empty_transfer_ds())
        self._log_output("Create schema from %s" % self.ui.mModelLineEdit.text())
        ogroutput = cfg.transform(
            dest=self.pgDs(), skipfailures=self.ui.cbSkipFailures.isChecked(), debug=True)
        self._remove_ogrconfig_tmp()
        self._log_output("Import finished")

    def importtodb(self):
        self._log_output("Import data from %s" % self.iliDs())
        cfg = self._ogr_config_tmp(self.iliDs())
        ogroutput = cfg.transform(
            dest=self.pgDs(), skipfailures=self.ui.cbSkipFailures.isChecked(), debug=True)
        # Keep temp config for export
        # self._remove_ogrconfig_tmp()
        self._plugin.messageLogWidget().show()
        self._log_output(ogroutput)
        self._log_output("Import finished")

        uri = self.pgUri()
        layer_infos = cfg.layer_infos()
        layer_names = cfg.layer_names()
        # if self.ui.cbImportEnums.isChecked():
        #     layer_infos += cfg.enum_infos()
        #     layer_names += cfg.enum_names()
        subLayerDialog = SublayersDialog()
        subLayerDialog.setupLayerList(layer_names)
        if subLayerDialog.exec_() == QDialog.Accepted:
            for layer_id in subLayerDialog.layerNames():
                # add a new layer for each selected row
                for layer in layer_infos:
                    if layer['name'] == layer_id:
                        geom_column = layer['geom_field'] if (
                            'geom_field' in layer) else None
                        uri.setDataSource("", layer['name'], geom_column)
                        self._plugin.iface.addVectorLayer(
                            uri.uri(), layer['name'], 'postgres')
            self.accept()
            self._plugin.iface.messageBar().pushMessage("Interlis", "Import finished",
                                                        level=QgsMessageBar.INFO, duration=2)

    def exporttoxtf(self):
        cfg = self._ogr_config(self.pgDs())
        fn = QFileDialog.getSaveFileName(
            None, "Save File", "",
            "Interlis 2 transfer (*.xtf *.XTF *.xml)")
        if not fn:
            return
        ds = self.iliFileDs(fn)
        ogroutput = cfg.transform_reverse(
            dest=ds, skipfailures=self.ui.cbSkipFailures.isChecked(),
            debug=True)
        self._log_output(ogroutput)
        QgsMessageLog.logMessage(
            "Export to '%s' finished" % self.ui.mDataLineEdit.text(),
            "Interlis", QgsMessageLog.INFO)

    def _show_log_window(self):
        logDock = self._plugin.iface.mainWindow().findChild(
            QDockWidget, 'MessageLog')
        logDock.show()

    def _log_output(self, output, lines_per_msg=None):
        if lines_per_msg is None:
            QgsMessageLog.logMessage(output, "Interlis", QgsMessageLog.INFO)
        else:
            lines = output.splitlines()
            for i in range(0, len(lines), lines_per_msg):
                msg = "\n".join(lines[i:i + lines_per_msg])
                QgsMessageLog.logMessage(msg, "Interlis", QgsMessageLog.INFO)

# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Interlis
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from interlisdialog import InterlisDialog
import os.path
import tempfile
from ogrtools.ogrtransform.spec import Spec
from ogrtools.ogrtransform.transformation import Transformation


class Interlis:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'interlis_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = InterlisDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/interlis/icon.png"),
            u"Interlis", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&interlis", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&interlis", self.action)
        self.iface.removeToolBarIcon(self.action)

    def importtodb(self):
        format = 'PostgreSQL'
        ilids = self.dlg.ui.mDataLineEdit.text() + ',' + self.dlg.ui.mModelLineEdit.text()
        QgsMessageLog.logMessage(ilids, "Interlis", QgsMessageLog.INFO)
        spec = os.path.join(tempfile.gettempdir(), "spec.json")
        QgsMessageLog.logMessage(spec, "Interlis", QgsMessageLog.INFO)
        trans = Spec(ds=ilids, model=self.dlg.ui.mModelLineEdit.text())
        specjson = trans.generate_spec(format, outfile=spec, layer_list=[])
        QgsMessageLog.logMessage(specjson, "Interlis", QgsMessageLog.INFO)
        trans = Transformation(spec, ilids)
        trans.transform(dest=self.dlg.ogrDs(), debug=True)

    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == QDialog.Accepted:
            self.importtodb()

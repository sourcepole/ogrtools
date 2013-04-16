# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OgrProcessingPlugin
                                 A QGIS plugin
 Vector transformation based on OGR library
                              -------------------
        begin                : 2012-04-12
        copyright            : (C) 2012 by Sourcepole
        email                : gis@sourcepole.ch
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

import os, sys
import inspect
from sextante.core.Sextante import Sextante
from ogralgorithmprovider import OgrAlgorithmProvider

cmd_folder = os.path.split(inspect.getfile( inspect.currentframe() ))[0]
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

class OgrProcessingPlugin:

    def __init__(self, iface):
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/ogrprocessingplugin"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale").toString()[0:2]
       
        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/ogrprocessingplugin_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.provider = OgrAlgorithmProvider()
   

    def initGui(self):
        Sextante.addProvider(self.provider, True)

    def unload(self):
        Sextante.removeProvider(self.provider)

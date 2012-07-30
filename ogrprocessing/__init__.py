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
 This script initializes the plugin, making it known to QGIS.
"""
def name():
    return "OGR Processing"
def description():
    return "Vector transformation based on OGR library"
def version():
    return "0.3.0"
def experimental():
    return True
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "1.0"
def classFactory(iface):
    # load OgrProcessingPlugin class from file OgrProcessingPlugin
    from ogrprocessingplugin import OgrProcessingPlugin
    return OgrProcessingPlugin(iface)

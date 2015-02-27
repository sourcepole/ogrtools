# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OgrProcessingPluginDialog
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

from PyQt4 import QtCore, QtGui
from ui_ogrprocessingplugin import Ui_OgrProcessingPlugin
# create the dialog for zoom to point


class OgrProcessingPluginDialog(QtGui.QDialog):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_OgrProcessingPlugin()
        self.ui.setupUi(self)

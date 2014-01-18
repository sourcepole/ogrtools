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

from PyQt4 import QtCore, QtGui
from ui_interlis import Ui_Interlis
# create the dialog for zoom to point


class InterlisDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Interlis()
        self.ui.setupUi(self)

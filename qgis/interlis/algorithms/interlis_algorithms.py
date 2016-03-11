# -*- coding: utf-8 -*-

"""
/***************************************************************************
 Interlis
                                 A QGIS plugin
 Interlis Import/export
                              -------------------
        begin                : 2016-03-11
        copyright            : (C) 2016 by Pirmin Kalberer
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

__author__ = 'Pirmin Kalberer'
__date__ = '2016-03-11'
__copyright__ = '(C) 2016 by Pirmin Kalberer'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from PyQt4.QtCore import QSettings

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.core.parameters import ParameterVector, ParameterFile, ParameterSelection
from processing.core.outputs import OutputFile
from processing.core.ProcessingConfig import ProcessingConfig

from interlis_utils import IliUtils


def connectionOptions(connection):
    settings = QSettings()
    mySettings = '/PostgreSQL/connections/' + connection
    try:
        database = settings.value(mySettings + '/database')
        username = settings.value(mySettings + '/username')
        host = settings.value(mySettings + '/host')
        port = settings.value(mySettings + '/port', type=int)
        password = settings.value(mySettings + '/password')
    except Exception:
        raise GeoAlgorithmExecutionException(
            'Wrong database connection name: %s' % connection)
    connoptions = {
        "-dbhost": host,
        "-dbport": str(port),
        "-dbdatabase": database,
        "-dbusr": username,
        "-dbpwd": password
    }
    ili2pgargs = []
    for k, v in connoptions.items():
        if len(v) > 0:
            ili2pgargs.extend([k, v])
    return ili2pgargs


def dbConnectionNames():
    settings = QSettings()
    settings.beginGroup('/PostgreSQL/connections/')
    return settings.childGroups()


class Ili2PgAlgorithm(GeoAlgorithm):
    OUTPUT = "OUTPUT"
    ILI = "ILI"
    DB = "DB"

    def defineCharacteristics(self):
        self.name = "ili2pg schemaimport"
        self.group = "Interlis"

        self.addParameter(ParameterFile(
            self.ILI,
            self.tr('Interlis model file'), optional=False, ext='ili'))
        #File extension filter not working in file dialg with current Processing 
        self.DB_CONNECTIONS = dbConnectionNames()
        self.addParameter(ParameterSelection(
            self.DB,
            self.tr('Database (connection name)'), self.DB_CONNECTIONS))

        #self.addOutput(OutputHTML(self.OUTPUT, "Ili2Pg result"))

    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        ili = self.getParameterValue(self.ILI)
        db = self.DB_CONNECTIONS[self.getParameterValue(self.DB)]
        ili2pgargs = ['-schemaimport']
        ili2pgargs.extend(connectionOptions(db))
        ili2pgargs.extend(["-models", ili])

        IliUtils.runJava(
            ProcessingConfig.getSetting(IliUtils.ILI2PG_JAR),
            ili2pgargs, progress)


class Pg2IliAlgorithm(GeoAlgorithm):

    OUTPUT = "OUTPUT"
    ILI = "ILI"
    XTF = "XTF"
    DB = "DB"

    def defineCharacteristics(self):
        self.name = "ili2pg export"
        self.group = "Interlis"

        self.DB_CONNECTIONS = dbConnectionNames()
        self.addParameter(ParameterSelection(
            self.DB,
            self.tr('Database (connection name)'), self.DB_CONNECTIONS))
        self.addParameter(ParameterFile(
            self.ILI,
            self.tr('Interlis model file'), optional=False, ext='ili'))
        self.addOutput(OutputFile(
            self.XTF,
            description="Ilismeta XML model output file", ext='xtf'))
        # ext: xtf, xml, itf

        #self.addOutput(OutputHTML(self.OUTPUT, "Ili2Pg result"))

    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        db = self.DB_CONNECTIONS[self.getParameterValue(self.DB)]
        ili = self.getParameterValue(self.ILI)
        xtf = self.getOutputValue(self.XTF)

        ili2pgargs = ['-export']
        ili2pgargs.extend(connectionOptions(db))
        ili2pgargs.extend(["-models", ili, xtf])

        IliUtils.runJava(
            ProcessingConfig.getSetting(IliUtils.ILI2PG_JAR),
            ili2pgargs, progress)


class Ili2ImdAlgorithm(GeoAlgorithm):

    OUTPUT = "OUTPUT"
    ILI = "ILI"
    IMD = "IMD"

    def defineCharacteristics(self):
        self.name = "ili to XML metamodel"
        self.group = "Interlis"

        self.addParameter(ParameterFile(
            self.ILI,
            self.tr('Interlis model file'), optional=False, ext='ili'))
        self.addOutput(OutputFile(
            self.IMD,
            description="Ilismeta XML model output file", ext='imd'))

    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        ili = self.getParameterValue(self.ILI)
        imd = self.getOutputValue(self.IMD)
        IliUtils.runIli2c(["-oIMD", "--out", imd, ili], progress)

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
        "--dbhost": host,
        "--dbport": str(port),
        "--dbdatabase": database,
        "--dbusr": username,
        "--dbpwd": password
    }
    ili2pgargs = []
    for k, v in connoptions.items():
        if len(v) > 0:
            ili2pgargs.extend([k, v])
    return ili2pgargs

# USAGE
#   java -jar ili2pg.jar [Options] [file.xtf]
#
# OPTIONS
#
# --import               do an import.
# --update               do an update.
# --export               do an export.
# --schemaimport         do an schema import.
# --dbhost  host         The host name of the server. Defaults to localhost.
# --dbport  port         The port number the server is listening on. Defaults to 5432.
# --dbdatabase database  The database name.
# --dbusr  username      User name to access database.
# --dbpwd  password      Password of user used to access database.
# --deleteData           on schema/data import, delete existing data from existing tables.
# --defaultSrsAuth  auth Default SRS authority EPSG
# --defaultSrsCode  code Default SRS code 21781
# --modeldir  path       Path(s) of directories containing ili-files.
# --models modelname     Name(s) of ili-models to generate an db schema for.
# --baskets BID          Basket-Id(s) of ili-baskets to export.
# --topics topicname     Name(s) of ili-topics to export.
# --createscript filename  Generate a sql script that creates the db schema.
# --dropscript filename  Generate a sql script that drops the generated db schema.
# --noSmartMapping       disable all smart mappings
# --smartInheritance     enable smart mapping of class/structure inheritance
# --coalesceCatalogueRef enable smart mapping of CHBase:CatalogueReference
# --coalesceMultiSurface enable smart mapping of CHBase:MultiSurface
# --expandMultilingual   enable smart mapping of CHBase:MultilingualText
# --createGeomIdx        create a spatial index on geometry columns.
# --createEnumColAsItfCode create enum type column with value according to ITF (instead of XTF).
# --createEnumTxtCol     create an additional column with the text of the enumeration value.
# --createEnumTabs       generate tables with enum definitions.
# --createSingleEnumTab  generate all enum definitions in a single table.
# --createStdCols        generate T_User, T_CreateDate, T_LastChange columns.
# --t_id_Name name       change name of t_id column (T_Id)
# --createTypeDiscriminator  generate always a type discriminaor colum.
# --structWithGenericRef  generate one generic reference to parent in struct tables.
# --disableNameOptimization disable use of unqualified class name as table name.
# --nameByTopic          use topic+class name as table name.
# --maxNameLength length max length of sql names (60)
# --sqlEnableNull        create no NOT NULL constraints in db schema.
# --strokeArcs           stroke ARCS on import.
# --skipPolygonBuilding  keep linetables; don't build polygons on import.
# --skipPolygonBuildingErrors  report build polygon errors as info.
# --keepAreaRef          keep arreaRef as additional column on import.
# --importTid            read TID into additional column T_Ili_Tid
# --createBasketCol      generate T_basket column.
# --createFk             generate foreign key constraints.
# --createFkIdx          create an index on foreign key columns.
# --createUnique         create UNIQUE db constraints.
# --dbschema  schema     The name of the schema in the database. Defaults to not set.
# --oneGeomPerTable      If more than one geometry per table, create secondary table.
# --log filename         log message to given file.
# --gui                  start GUI.
# --trace                enable trace messages.
# --help                 Display this help text.
# --version              Display the version of ili2pg


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
        ili2pgargs = ['--schemaimport']
        ili2pgargs.extend(connectionOptions(db))
        ili2pgargs.extend(["--models", ili])

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

        ili2pgargs = ['--export']
        ili2pgargs.extend(connectionOptions(db))
        ili2pgargs.extend(["--models", ili, xtf])

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

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
from processing.core.parameters import ParameterVector, ParameterFile, ParameterString, ParameterBoolean, ParameterSelection
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
# --replace              do a replace.
# --delete               do a delete.
# --export               do an export.
# --schemaimport         do an schema import.
# --dbhost  host         The host name of the server. Defaults to localhost.
# --dbport  port         The port number the server is listening on. Defaults to 5432.
# --dbdatabase database  The database name.
# --dbusr  username      User name to access database.
# --dbpwd  password      Password of user used to access database.
# --validConfig file     Config file for validation.
# --disableValidation    Disable validation of data.
# --deleteData           on schema/data import, delete existing data from existing tables.
# --defaultSrsAuth  auth Default SRS authority EPSG
# --defaultSrsCode  code Default SRS code 21781
# --modeldir  path       Path(s) of directories containing ili-files.
# --models modelname     Name(s) of ili-models to generate an db schema for.
# --dataset name         Name of dataset.
# --baskets BID          Basket-Id(s) of ili-baskets to export.
# --topics topicname     Name(s) of ili-topics to export.
# --createscript filename  Generate a sql script that creates the db schema.
# --dropscript filename  Generate a sql script that drops the generated db schema.
# --noSmartMapping       disable all smart mappings
# --smart1Inheritance     enable smart1 mapping of class/structure inheritance
# --smart2Inheritance     enable smart2 mapping of class/structure inheritance
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
# --idSeqMin minValue    sets the minimum value of the id sequence generator.
# --idSeqMax maxValue    sets the maximum value of the id sequence generator.
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


class Ili2DbSchemaAlgorithm(GeoAlgorithm):
    OUTPUT = "OUTPUT"
    ILIDIR = "ILIDIR"
    ILIMODELS = "ILIMODELS"
    XTF = "XTF"
    DB = "DB"
    TABLE_NAMING = [
        'unqualified',
        'nameByTopic',
        'disableNameOptimization']
    INHERTIANCE_MAPPINGS = [
        'smart1Inheritance',
        'smart2Inheritance',
        'noSmartMapping']


    def defineCharacteristics(self):
        self.name = "Create Schema from Model"
        self.group = "ili2pg / ili2gpkg"

        self.addParameter(ParameterString(
            self.ILIMODELS,
            self.tr('Interlis models'), optional=False))
        self.addParameter(ParameterString(
            self.ILIDIR,
            self.tr('Interlis model search path'),
            default='http://models.geo.admin.ch/'))
        self.addParameter(ParameterFile(
            'iliLocalPath',
            self.tr('Local model directory'), isFolder=True))
        self.addParameter(ParameterBoolean(
            'nameByTopic',
            self.tr('Use topic+class name as table name'), default=True))
        self.addParameter(ParameterSelection(
            'tableNaming',
            self.tr('Table naming convention:'),
            options=self.TABLE_NAMING, default=1))
        self.addParameter(ParameterSelection(
            'inheritanceMapping',
            self.tr('Inheritance mapping strategy:'),
            options=self.INHERTIANCE_MAPPINGS, default=0))
        self.addParameter(ParameterBoolean(
            'sqlNotNull',
            self.tr('Create NOT NULL constraints in db schema'), default=False))
        self.addParameter(ParameterBoolean(
            'createBasketCol',
            self.tr('Generate T_basket column'), default=False))
        self.addParameter(ParameterBoolean(
            'createFk',
            self.tr('Generate foreign key constraints'), default=True))
        self.addParameter(ParameterBoolean(
            'createFkIdx',
            self.tr('Create an index on foreign key columns'), default=True))
        self.addParameter(ParameterBoolean(
            'createGeomIdx',
            self.tr('Create a spatial index on geometry columns'), default=True))
        self.addParameter(ParameterBoolean(
            'strokeArcs',
            self.tr('Stroke ARCS on import'), default=False))
        self.addParameter(ParameterBoolean(
            'createEnumTabs',
            self.tr('Generate tables with enum definitions'), default=True))
        self.addParameter(ParameterString(
            'defaultSrsCode',
            self.tr('Default SRS code (EPSG)'), default='21781'))
        self.DB_CONNECTIONS = dbConnectionNames()
        self.addParameter(ParameterSelection(
            self.DB,
            self.tr('Database (connection name)'), self.DB_CONNECTIONS))
        self.addParameter(ParameterString(
            'dbschema',
            self.tr('Database schema name'), default='public'))

    def processAlgorithm(self, progress):
        ili2pgargs = ['--schemaimport']

        models = self.getParameterValue(self.ILIMODELS)
        ili2pgargs.extend(["--models", models])

        modeldir = self.getParameterValue(self.ILIDIR)
        localmodeldir = self.getParameterValue('iliLocalPath')
        if localmodeldir:
            modeldir = "%s;%s" % (localmodeldir, modeldir)
        ili2pgargs.append("--modeldir '%s'" % modeldir)

        naming = self.TABLE_NAMING[self.getParameterValue('tableNaming')]
        if naming != 'unqualified':
            ili2pgargs.append("--%s" % naming)

        mapping = self.INHERTIANCE_MAPPINGS[self.getParameterValue('inheritanceMapping')]
        ili2pgargs.append("--%s" % mapping)

        if not self.getParameterValue('sqlNotNull'):
            ili2pgargs.append('--sqlEnableNull')

        if self.getParameterValue('createFk'):
            ili2pgargs.append('--createFk')

        if self.getParameterValue('createFkIdx'):
            ili2pgargs.append('--createFkIdx')

        if self.getParameterValue('createGeomIdx'):
            ili2pgargs.append('--createGeomIdx')

        if self.getParameterValue('strokeArcs'):
            ili2pgargs.append('--strokeArcs')

        if self.getParameterValue('createEnumTabs'):
            ili2pgargs.append('--createEnumTabs')

        defaultSrsCode = self.getParameterValue('defaultSrsCode')
        ili2pgargs.extend(["--defaultSrsCode", defaultSrsCode])

        db = self.DB_CONNECTIONS[self.getParameterValue(self.DB)]
        ili2pgargs.extend(connectionOptions(db))

        dbschema = self.getParameterValue('dbschema')
        ili2pgargs.extend(["--dbschema", dbschema])

        IliUtils.runJava(
            ProcessingConfig.getSetting(IliUtils.ILI2PG_JAR),
            ili2pgargs, progress)


class Ili2DbImportAlgorithm(GeoAlgorithm):
    OUTPUT = "OUTPUT"
    ILIDIR = "ILIDIR"
    ILIMODELS = "ILIMODELS"
    XTF = "XTF"
    DB = "DB"
    IMPORT_MODE = [
        'import',
        'update',
        'replace']

    def defineCharacteristics(self):
        self.name = "Import into DB"
        self.group = "ili2pg / ili2gpkg"

        self.addParameter(ParameterSelection(
            'importMode',
            self.tr('Import mode:'),
            options=self.IMPORT_MODE, default=0))
        self.addParameter(ParameterString(
            'dataset',
            self.tr('Name of dataset'), optional=True))
        self.addParameter(ParameterFile(
            self.XTF,
            self.tr('Interlis transfer input file'), optional=False))
        self.addParameter(ParameterString(
            self.ILIDIR,
            self.tr('Interlis model search path'),
            default='%ILI_FROM_DB;%XTF_DIR;http://models.geo.admin.ch/'))
        self.addParameter(ParameterString(
            self.ILIMODELS,
            self.tr('Interlis models'), optional=True))
        self.DB_CONNECTIONS = dbConnectionNames()
        self.addParameter(ParameterSelection(
            self.DB,
            self.tr('Database (connection name)'), self.DB_CONNECTIONS))
        self.addParameter(ParameterString(
            'dbschema',
            self.tr('Database schema name'), default='public'))

        #self.addOutput(OutputHTML(self.OUTPUT, "Ili2Pg result"))

    def processAlgorithm(self, progress):
        ili2pgargs = []

        mode = self.IMPORT_MODE[self.getParameterValue('importMode')]
        ili2pgargs.append("--%s" % mode)

        dataset = self.getParameterValue('dataset')
        if dataset:
            ili2pgargs.extend(["--dataset", dataset])

        db = self.DB_CONNECTIONS[self.getParameterValue(self.DB)]
        ili2pgargs.extend(connectionOptions(db))

        modeldir = self.getParameterValue(self.ILIDIR)
        ili2pgargs.append("--modeldir '%s'" % modeldir)

        models = self.getParameterValue(self.ILIMODELS)
        if models:
            ili2pgargs.extend(["--models", models])

        dbschema = self.getParameterValue('dbschema')
        ili2pgargs.extend(["--dbschema", dbschema])

        xtf = self.getParameterValue(self.XTF)
        ili2pgargs.append(xtf)

        IliUtils.runJava(
            ProcessingConfig.getSetting(IliUtils.ILI2PG_JAR),
            ili2pgargs, progress)


class Ili2DbExportAlgorithm(GeoAlgorithm):

    OUTPUT = "OUTPUT"
    ILIDIR = "ILIDIR"
    ILIMODELS = "ILIMODELS"
    XTF = "XTF"
    DB = "DB"

    def defineCharacteristics(self):
        self.name = "Export from DB"
        self.group = "ili2pg / ili2gpkg"

        self.DB_CONNECTIONS = dbConnectionNames()
        self.addParameter(ParameterSelection(
            self.DB,
            self.tr('Database (connection name)'), self.DB_CONNECTIONS))
        self.addParameter(ParameterString(
            'dbschema',
            self.tr('Database schema name'), default='public'))
        self.addParameter(ParameterString(
            'dataset',
            self.tr('Name of dataset'), optional=True))
        self.addParameter(ParameterString(
            self.ILIDIR,
            self.tr('Interlis model search path'),
            default='%ILI_FROM_DB;%XTF_DIR;http://models.geo.admin.ch/'))
        self.addParameter(ParameterString(
            self.ILIMODELS,
            self.tr('Interlis models')))
        self.addOutput(OutputFile(
            self.XTF,
            description="Interlis transfer output file"))
        # ext: xtf, xml, itf

        #self.addOutput(OutputHTML(self.OUTPUT, "Ili2Pg result"))

    def processAlgorithm(self, progress):
        ili2pgargs = ['--export']

        db = self.DB_CONNECTIONS[self.getParameterValue(self.DB)]
        ili2pgargs.extend(connectionOptions(db))

        dbschema = self.getParameterValue('dbschema')
        ili2pgargs.extend(["--dbschema", dbschema])

        dataset = self.getParameterValue('dataset')
        if dataset:
            ili2pgargs.extend(["--dataset", dataset])

        modeldir = self.getParameterValue(self.ILIDIR)
        ili2pgargs.append("--modeldir '%s'" % modeldir)

        models = self.getParameterValue(self.ILIMODELS)
        ili2pgargs.extend(["--models", models])

        xtf = self.getOutputValue(self.XTF)
        ili2pgargs.append(xtf)

        IliUtils.runJava(
            ProcessingConfig.getSetting(IliUtils.ILI2PG_JAR),
            ili2pgargs, progress)


class Ili2ImdAlgorithm(GeoAlgorithm):

    OUTPUT = "OUTPUT"
    ILI = "ILI"
    IMD = "IMD"

    def defineCharacteristics(self):
        self.name = "Ili Model -> IlisMeta"
        self.group = "ili2c"

        self.addParameter(ParameterFile(
            self.ILI,
            self.tr('Interlis model file'), optional=False, ext='ili'))
        self.addOutput(OutputFile(
            self.IMD,
            description="IlisMeta XML model output file", ext='imd'))

    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        ili = self.getParameterValue(self.ILI)
        imd = self.getOutputValue(self.IMD)
        IliUtils.runIli2c(["-oIMD", "--out", imd, ili], progress)

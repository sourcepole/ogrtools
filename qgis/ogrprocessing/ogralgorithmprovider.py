from sextante.core.AlgorithmProvider import AlgorithmProvider
from sextante.core.SextanteConfig import Setting, SextanteConfig
from ogrinfo import OgrInfo
from ogr2vrt import Ogr2Vrt
from ogr2ogr import Ogr2Ogr, Ogr2OgrVrt
from ogrsql import OgrSql
from ogrprocessing.interlis.IliUtils import IliUtils
from ogrprocessing.interlis.ili2pg import Ili2Pg, Pg2Ili
from ogrprocessing.interlis.ilismeta import Ili2Imd, EnumsAsGML, ImportGML, IliEnumsToPg, CreatePGDb
from ogrprocessing.interlis.iliogr2ogr import IliOgr2Ogr


class OgrAlgorithmProvider(AlgorithmProvider):

    def __init__(self):
        AlgorithmProvider.__init__(self)
        self.alglist = [OgrInfo(), Ogr2Vrt(), Ogr2Ogr(), Ogr2OgrVrt(), OgrSql(), Ili2Pg(), Pg2Ili(
        ), Ili2Imd(), EnumsAsGML(), ImportGML(), IliEnumsToPg(), CreatePGDb(), IliOgr2Ogr()]
        for alg in self.alglist:
            alg.provider = self

    def getDescription(self):
        return "OGR and INTERLIS transformation"

    def initializeSettings(self):
        '''In this method we add settings needed to configure our provider.
        Do not forget to call the parent method, since it takes care or
        automatically adding a setting for activating or deactivating the
        algorithms in the provider'''
        AlgorithmProvider.initializeSettings(self)
        SextanteConfig.addSetting(Setting(self.getDescription(
        ), IliUtils.JAVA_EXEC, "Java executable", IliUtils.java_exec_default()))
        SextanteConfig.addSetting(
            Setting(self.getDescription(), IliUtils.ILI2C_JAR, "ili2c.jar path", "ili2c.jar"))
        SextanteConfig.addSetting(Setting(
            self.getDescription(), IliUtils.ILI2PG_JAR, "ili2pg.jar path", "ili2pg.jar"))
        SextanteConfig.addSetting(Setting(
            self.getDescription(), IliUtils.CREATEDB_EXEC, "createdb path", "createdb"))

    def unload(self):
        '''Setting should be removed here, so they do not appear anymore
        when the plugin is unloaded'''
        AlgorithmProvider.unload(self)
        SextanteConfig.removeSetting(IliUtils.JAVA_EXEC)
        SextanteConfig.removeSetting(IliUtils.ILI2C_JAR)
        SextanteConfig.removeSetting(IliUtils.ILI2PG_JAR)

    def getName(self):
        '''This is the name that will appear on the toolbox group.
        It is also used to create the command line name of all the algorithms
        from this provider'''
        return "OGR"

    def getIcon(self):
        '''We return the default icon'''
        return AlgorithmProvider.getIcon(self)

    def getSupportedOutputVectorLayerExtensions(self):
        return ["shp", "sqlite"]

    def _loadAlgorithms(self):
        '''Here we fill the list of algorithms in self.algs.
        This method is called whenever the list of algorithms should be updated.
        If the list of algorithms can change while executing SEXTANTE for QGIS
        (for instance, if it contains algorithms from user-defined scripts and
        a new script might have been added), you should create the list again
        here.
        In this case, since the list is always the same, we assign from the pre-made list.
        This assignment has to be done in this method even if the list does not change,
        since the self.algs list is cleared before calling this method'''
        self.algs = self.alglist

from sextante.core.GeoAlgorithm import GeoAlgorithm
from sextante.outputs.OutputHTML import OutputHTML
from sextante.parameters.ParameterFile import ParameterFile
from sextante.parameters.ParameterString import ParameterString
from sextante.parameters.ParameterBoolean import ParameterBoolean
from sextante.core.Sextante import Sextante
from sextante.core.SextanteLog import SextanteLog
from sextante.core.SextanteConfig import Setting, SextanteConfig
from sextante.core.QGisLayers import QGisLayers
from ogralgorithm import OgrAlgorithm
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from IliUtils import IliUtils

class Ili2Pg(OgrAlgorithm):

    #constants used to refer to parameters and outputs.
    #They will be used when calling the algorithm from another algorithm,
    #or when calling SEXTANTE from the QGIS console.
    OUTPUT = "OUTPUT"
    INPUT_LAYER = "INPUT_LAYER"
    DB = "DB"
    ILI = "ILI"

    def defineCharacteristics(self):
        self.name = "ili2pg schemaimport"
        self.group = "Interlis"

        self.addParameter(ParameterFile(self.ILI, "Interlis model (.ili)"))
        self.addParameter(ParameterString(self.DB, "Database name"))

        #self.addOutput(OutputHTML(self.OUTPUT, "Ili2Pg result"))


    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        #input = self.getParameterValue(self.INPUT_LAYER)
        ili = self.getParameterValue(self.ILI)
        db = self.getParameterValue(self.DB)

        #output = self.getOutputValue(self.OUTPUT)

        IliUtils.runJava( SextanteConfig.getSetting(IliUtils.ILI2PG_JAR), ['-schemaimport', '-dbdatabase', db, '-dbusr', 'pi', "-models", ili], progress )

class Pg2Ili(OgrAlgorithm):

    #constants used to refer to parameters and outputs.
    #They will be used when calling the algorithm from another algorithm,
    #or when calling SEXTANTE from the QGIS console.
    OUTPUT = "OUTPUT"
    INPUT_LAYER = "INPUT_LAYER"
    DB = "DB"
    ILI = "ILI"
    XTF = "XTF"

    def defineCharacteristics(self):
        self.name = "ili2pg export"
        self.group = "Interlis"

        self.addParameter(ParameterString(self.DB, "Database name"))
        self.addParameter(ParameterFile(self.ILI, "Interlis model (.ili)"))
        self.addParameter(ParameterFile(self.XTF, "Interlis 2 tansfer file (.xtf)"))

        #self.addOutput(OutputHTML(self.OUTPUT, "Ili2Pg result"))


    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        #input = self.getParameterValue(self.INPUT_LAYER)
        db = self.getParameterValue(self.DB)
        ili = self.getParameterValue(self.ILI)
        xtf = self.getParameterValue(self.XTF)

        #output = self.getOutputValue(self.OUTPUT)

        IliUtils.runJava( SextanteConfig.getSetting(IliUtils.ILI2PG_JAR), ['-export', '-dbdatabase', db, '-dbusr', 'pi', "-models", ili,  xtf], progress )

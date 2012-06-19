from sextante.core.GeoAlgorithm import GeoAlgorithm
from sextante.outputs.OutputHTML import OutputHTML
from sextante.parameters.ParameterVector import ParameterVector
from sextante.parameters.ParameterString import ParameterString
from sextante.parameters.ParameterBoolean import ParameterBoolean
from sextante.core.Sextante import Sextante
from sextante.core.SextanteLog import SextanteLog
from sextante.core.QGisLayers import QGisLayers
from ogralgorithm import OgrAlgorithm
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from IliUtils import *

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

        #It is a mandatory (not optional) one, hence the False argument
        #self.addParameter(ParameterVector(self.INPUT_LAYER, "Input layer", ParameterVector.VECTOR_TYPE_ANY, False))
        self.addParameter(ParameterString(self.DB, "DB", "zplnaenikon"))
        self.addParameter(ParameterString(self.ILI, "ILI", "/home/pi/Dropbox/Projects/geosummit/workshop/NP_73_CH_de_ili2.ili"))

        #self.addOutput(OutputHTML(self.OUTPUT, "Ili2Pg result"))


    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        #input = self.getParameterValue(self.INPUT_LAYER)
        db = self.getParameterValue(self.DB)
        ili = self.getParameterValue(self.ILI)

        #output = self.getOutputValue(self.OUTPUT)

        IliUtils.runJava( '/home/pi/apps/ili2pg-1.4.0/ili2pg.jar', ['-schemaimport', '-dbdatabase', db, '-dbusr', 'pi', "-models", ili], progress )

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

        #It is a mandatory (not optional) one, hence the False argument
        #self.addParameter(ParameterVector(self.INPUT_LAYER, "Input layer", ParameterVector.VECTOR_TYPE_ANY, False))
        self.addParameter(ParameterString(self.DB, "DB", "zplnaenikon"))
        self.addParameter(ParameterString(self.ILI, "ILI", "/home/pi/Dropbox/Projects/geosummit/workshop/NP_73_CH_de_ili2.ili"))
        self.addParameter(ParameterString(self.XTF, "XTF", "/tmp/out.xtf"))

        #self.addOutput(OutputHTML(self.OUTPUT, "Ili2Pg result"))


    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        #input = self.getParameterValue(self.INPUT_LAYER)
        db = self.getParameterValue(self.DB)
        ili = self.getParameterValue(self.ILI)
        xtf = self.getParameterValue(self.XTF)

        #output = self.getOutputValue(self.OUTPUT)

        IliUtils.runJava( '/home/pi/apps/ili2pg-1.4.0/ili2pg.jar', ['-export', '-dbdatabase', db, '-dbusr', 'pi', "-models", ili,  xtf], progress )

from sextante.core.GeoAlgorithm import GeoAlgorithm
from sextante.outputs.OutputHTML import OutputHTML
from sextante.parameters.ParameterFile import ParameterFile
from sextante.parameters.ParameterString import ParameterString
from sextante.parameters.ParameterBoolean import ParameterBoolean
from ogrprocessing.sextanteext.ParameterDbConnection import ParameterDbConnection
from sextante.core.Sextante import Sextante
from sextante.core.SextanteLog import SextanteLog
from sextante.core.SextanteConfig import Setting, SextanteConfig
from sextante.core.QGisLayers import QGisLayers
from ogrprocessing.ogralgorithm import OgrAlgorithm
from IliUtils import IliUtils
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def connectionOptions(db):
    connoptions = {
        "-dbhost": db.getHost(),
        "-dbport": db.getPort(),
        "-dbdatabase": db.getDatabase(),
        "-dbusr": db.getUsername(),
        "-dbpwd": db.getPassword()
        }
    ili2pgargs = []
    for k,v in connoptions.items():
        if len(v)>0:
            ili2pgargs.extend([k, v])
    return ili2pgargs


class Ili2Pg(OgrAlgorithm):

    #constants used to refer to parameters and outputs.
    #They will be used when calling the algorithm from another algorithm,
    #or when calling SEXTANTE from the QGIS console.
    OUTPUT = "OUTPUT"
    DB = "DB"
    ILI = "ILI"

    def defineCharacteristics(self):
        self.name = "ili2pg schemaimport"
        self.group = "Interlis"

        self.addParameter(ParameterFile(self.ILI, "Interlis model (.ili)"))
        self.addParameter(ParameterDbConnection(self.DB, "Database"))

        #self.addOutput(OutputHTML(self.OUTPUT, "Ili2Pg result"))


    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        ili = self.getParameterValue(self.ILI)
        db = self.getParameterFromName(self.DB)
        ili2pgargs = ['-schemaimport']
        ili2pgargs.extend(connectionOptions(db))
        ili2pgargs.extend(["-models", ili])

        IliUtils.runJava( SextanteConfig.getSetting(IliUtils.ILI2PG_JAR), ili2pgargs, progress )

class Pg2Ili(OgrAlgorithm):

    #constants used to refer to parameters and outputs.
    #They will be used when calling the algorithm from another algorithm,
    #or when calling SEXTANTE from the QGIS console.
    OUTPUT = "OUTPUT"
    DB = "DB"
    ILI = "ILI"
    XTF = "XTF"

    def defineCharacteristics(self):
        self.name = "ili2pg export"
        self.group = "Interlis"

        self.addParameter(ParameterDbConnection(self.DB, "Database"))
        self.addParameter(ParameterFile(self.ILI, "Interlis model (.ili)"))
        self.addParameter(ParameterFile(self.XTF, "Interlis 2 tansfer file (.xtf)"))

        #self.addOutput(OutputHTML(self.OUTPUT, "Ili2Pg result"))


    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        db = self.getParameterFromName(self.DB)
        ili = self.getParameterValue(self.ILI)
        xtf = self.getParameterValue(self.XTF)

        ili2pgargs = ['-export']
        ili2pgargs.extend(connectionOptions(db))
        ili2pgargs.extend(["-models", ili, xtf])

        IliUtils.runJava( SextanteConfig.getSetting(IliUtils.ILI2PG_JAR), ili2pgargs, progress )

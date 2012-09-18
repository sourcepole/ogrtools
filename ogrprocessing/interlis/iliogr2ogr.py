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
from ogrprocessing.pyogr.ogr2ogr import *
from IliUtils import IliUtils
import osr
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class IliOgr2Ogr(OgrAlgorithm):

    #constants used to refer to parameters and outputs.
    #They will be used when calling the algorithm from another algorithm,
    #or when calling SEXTANTE from the QGIS console.
    OUTPUT = "OUTPUT"
    ILI = "ILI"
    ITF = "ITF"
    APPEND = "APPEND"
    SRS = "SRS"

    def defineCharacteristics(self):
        self.name = "ogr2ogr ILI->PG"
        self.group = "Interlis"

        self.addParameter(ParameterFile(self.ILI, "Interlis model (.ili)"))
        self.addParameter(ParameterFile(self.ITF, "Interlis tansfer file (.itf/.xtf)"))
        self.addParameter(ParameterDbConnection(self.DB, "Database"))
        self.addParameter(ParameterBoolean(self.APPEND, "Append"))

        #self.addOutput(OutputHTML(self.OUTPUT, "Ili2Pg result"))


    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        ili = self.getParameterValue(self.ILI)
        xtf = self.getParameterValue(self.ITF)
        ogrinput = "%s,%s" % (xtf, ili)
        db = self.getParameterFromName(self.DB)
        append = self.getParameterValue(self.APPEND)

        srs = osr.SpatialReference()
        srs.ImportFromEPSG( 21781 )

        ogr2ogr(pszFormat=db.getOgrDriverName(),
            pszDataSource=ogrinput,
            pszDestDataSource=db.getOgrConnection(),
            bAppend = append,
            bOverwrite = not append,
            poOutputSRS = srs,
            poSourceSRS = srs,
            errfunc=IliUtils.errfunc)

from sextante.core.GeoAlgorithm import GeoAlgorithm
from sextante.outputs.OutputHTML import OutputHTML
from sextante.parameters.ParameterVector import ParameterVector
from sextante.parameters.ParameterBoolean import ParameterBoolean
from sextante.core.Sextante import Sextante
from sextante.core.SextanteLog import SextanteLog
from sextante.core.QGisLayers import QGisLayers
from ogralgorithm import OgrAlgorithm
from pyogr.ogrvrt import *
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import string
import re
import cgi
import sys
import ogr
import gdal


class Ogr2Vrt(OgrAlgorithm):

    # constants used to refer to parameters and outputs.
    # They will be used when calling the algorithm from another algorithm,
    # or when calling SEXTANTE from the QGIS console.
    OUTPUT = "OUTPUT"
    INPUT_LAYER = "INPUT_LAYER"

    def defineCharacteristics(self):
        self.name = "Generate VRT"
        self.group = "Miscellaneous"

        # we add the input vector layer. It can have any kind of geometry
        # It is a mandatory (not optional) one, hence the False argument
        self.addParameter(ParameterVector(
            self.INPUT_LAYER, "Input layer", ParameterVector.VECTOR_TYPE_ANY, False))

        self.addOutput(OutputHTML(self.OUTPUT, "VRT"))

    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        input = self.getParameterValue(self.INPUT_LAYER)
        ogrLayer = self.ogrConnectionString(input)

        output = self.getOutputValue(self.OUTPUT)

        vrt = ogr2vrt(ogrLayer)
        if vrt == None:
            vrt = self.failure(ogrLayer)
        qDebug(vrt)

        f = open(output, "w")
        f.write("<pre>" + cgi.escape(vrt) + "</pre>")
        f.close()

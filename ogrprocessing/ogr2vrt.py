from sextante.core.GeoAlgorithm import GeoAlgorithm
from sextante.outputs.OutputHTML import OutputHTML
from sextante.parameters.ParameterVector import ParameterVector
from sextante.parameters.ParameterBoolean import ParameterBoolean
from sextante.core.Sextante import Sextante
from sextante.core.SextanteLog import SextanteLog
from sextante.core.QGisLayers import QGisLayers
from ogralgorithm import OgrAlgorithm
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

    #constants used to refer to parameters and outputs.
    #They will be used when calling the algorithm from another algorithm,
    #or when calling SEXTANTE from the QGIS console.
    OUTPUT = "OUTPUT"
    INPUT_LAYER = "INPUT_LAYER"

    def defineCharacteristics(self):
        self.name = "Generate VRT"
        self.group = "VRT"

        #we add the input vector layer. It can have any kind of geometry
        #It is a mandatory (not optional) one, hence the False argument
        self.addParameter(ParameterVector(self.INPUT_LAYER, "Input layer", ParameterVector.VECTOR_TYPE_ANY, False))

        self.addOutput(OutputHTML(self.OUTPUT, "VRT"))


    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        input = self.getParameterValue(self.INPUT_LAYER)
        ogrLayer = self.ogrConnectionString(input)

        output = self.getOutputValue(self.OUTPUT)

        vrt = self.gen_vrt( ogrLayer )
        if vrt == None:
            vrt = self.failure(ogrLayer)
        qDebug(vrt)

        f = open(output, "w")
        f.write("<pre>" + cgi.escape(vrt) + "</pre>")
        f.close()

    def GeomType2Name(self, type ):
        if type == ogr.wkbUnknown:
            return 'wkbUnknown'
        elif type == ogr.wkbPoint:
            return 'wkbPoint'
        elif type == ogr.wkbLineString:
            return 'wkbLineString'
        elif type == ogr.wkbPolygon:
            return 'wkbPolygon'
        elif type == ogr.wkbMultiPoint:
            return 'wkbMultiPoint'
        elif type == ogr.wkbMultiLineString:
            return 'wkbMultiLineString'
        elif type == ogr.wkbMultiPolygon:
            return 'wkbMultiPolygon'
        elif type == ogr.wkbGeometryCollection:
            return 'wkbGeometryCollection'
        elif type == ogr.wkbNone:
            return 'wkbNone'
        elif type == ogr.wkbLinearRing:
            return 'wkbLinearRing'
        else:
            return 'wkbUnknown'

    #############################################################################
    def Esc(self, x):
        return gdal.EscapeString( x, gdal.CPLES_XML )

    def gen_vrt(self, infile):
        outfile = None
        layer_list = []
        relative = "0"
        schema=0

        #############################################################################
        # Open the datasource to read.

        src_ds = ogr.Open( infile, update = 0 )

        if src_ds is None:
            return None

        if schema:
            infile = '@dummy@'

        if len(layer_list) == 0:
            for layer in src_ds:
                layer_list.append( layer.GetLayerDefn().GetName() )

        #############################################################################
        # Start the VRT file.

        vrt = '<OGRVRTDataSource>\n'

        #############################################################################
        #	Process each source layer.

        for name in layer_list:
            layer = src_ds.GetLayerByName(name)
            layerdef = layer.GetLayerDefn()

            vrt += '  <OGRVRTLayer name="%s">\n' % self.Esc(name)
            vrt += '    <SrcDataSource relativeToVRT="%s" shared="%d">%s</SrcDataSource>\n' \
                   % (relative,not schema,self.Esc(infile))
            if schema:
                vrt += '    <SrcLayer>@dummy@</SrcLayer>\n'
            else:
                vrt += '    <SrcLayer>%s</SrcLayer>\n' % self.Esc(name)
            vrt += '    <GeometryType>%s</GeometryType>\n' \
                   % self.GeomType2Name(layerdef.GetGeomType())
            srs = layer.GetSpatialRef()
            if srs is not None:
                vrt += '    <LayerSRS>%s</LayerSRS>\n' \
                       % (self.Esc(srs.ExportToWkt()))

            # Process all the fields.
            for fld_index in range(layerdef.GetFieldCount()):
                src_fd = layerdef.GetFieldDefn( fld_index )
                if src_fd.GetType() == ogr.OFTInteger:
                    type = 'Integer'
                elif src_fd.GetType() == ogr.OFTString:
                    type = 'String'
                elif src_fd.GetType() == ogr.OFTReal:
                    type = 'Real'
                elif src_fd.GetType() == ogr.OFTStringList:
                    type = 'StringList'
                elif src_fd.GetType() == ogr.OFTIntegerList:
                    type = 'IntegerList'
                elif src_fd.GetType() == ogr.OFTRealList:
                    type = 'RealList'
                elif src_fd.GetType() == ogr.OFTBinary:
                    type = 'Binary'
                elif src_fd.GetType() == ogr.OFTDate:
                    type = 'Date'
                elif src_fd.GetType() == ogr.OFTTime:
                    type = 'Time'
                elif src_fd.GetType() == ogr.OFTDateTime:
                    type = 'DateTime'
                else:
                    type = 'String'

                vrt += '    <Field name="%s" type="%s"' \
                       % (self.Esc(src_fd.GetName()), type)
                if not schema:
                    vrt += ' src="%s"' % self.Esc(src_fd.GetName())
                if src_fd.GetWidth() > 0:
                    vrt += ' width="%d"' % src_fd.GetWidth()
                if src_fd.GetPrecision() > 0:
                    vrt += ' precision="%d"' % src_fd.GetPrecision()
                vrt += '/>\n'

            vrt += '  </OGRVRTLayer>\n'

        vrt += '</OGRVRTDataSource>\n' 
        
        return vrt

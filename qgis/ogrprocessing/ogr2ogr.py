from sextante.core.GeoAlgorithm import GeoAlgorithm
from sextante.outputs.OutputVector import OutputVector
from sextante.parameters.ParameterVector import ParameterVector
from sextante.parameters.ParameterString import ParameterString
from sextante.parameters.ParameterBoolean import ParameterBoolean
from sextante.core.Sextante import Sextante
from sextante.core.SextanteLog import SextanteLog
from sextante.core.QGisLayers import QGisLayers
from ogrprocessing.ogralgorithm import OgrAlgorithm
from ogrprocessing.pyogr.ogr2ogr import *
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import string
from string import Template
import re
import os
import tempfile
import ogr
import gdal
import osr


GeomOperation = Enum(["NONE", "SEGMENTIZE", "SIMPLIFY_PRESERVE_TOPOLOGY"])


class Ogr2Ogr(OgrAlgorithm):

    # constants used to refer to parameters and outputs.
    # They will be used when calling the algorithm from another algorithm,
    # or when calling SEXTANTE from the QGIS console.
    OUTPUT_LAYER = "OUTPUT_LAYER"
    INPUT_LAYER = "INPUT_LAYER"
    DEST_DS = "DEST_DS"
    DEST_FORMAT = "DEST_FORMAT"
    DEST_DSCO = "DEST_DSCO"

    def defineCharacteristics(self):
        self.name = "ogr2ogr"
        self.group = "Transformation"

        # we add the input vector layer. It can have any kind of geometry
        # It is a mandatory (not optional) one, hence the False argument
        self.addParameter(ParameterVector(
            self.INPUT_LAYER, "Input layer", ParameterVector.VECTOR_TYPE_ANY, False))
        #self.addParameter(ParameterString(self.DEST_DS, "Output DS", "/tmp/out.sqlite"))
        self.addParameter(ParameterString(
            self.DEST_FORMAT, "Destination Format", "ESRI Shapefile"))  # SQLite
        # SPATIALITE=YES
        self.addParameter(
            ParameterString(self.DEST_DSCO, "Creation Options", ""))

        self.addOutput(OutputVector(self.OUTPUT_LAYER, "Output layer"))

    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        input = self.getParameterValue(self.INPUT_LAYER)
        ogrLayer = self.ogrConnectionString(input)
        output = self.getOutputValue(self.OUTPUT_LAYER)

        #dst_ds = self.getParameterValue(self.DEST_DS)
        dst_ds = self.ogrConnectionString(output)
        dst_format = self.getParameterValue(self.DEST_FORMAT)
        ogr_dsco = [self.getParameterValue(self.DEST_DSCO)]  # TODO: split
        #dst_ds = "PG:dbname='glarus_np' options='-c client_encoding=LATIN9'"
        #dst_format ="PostgreSQL"

        qDebug("Opening data source '%s'" % ogrLayer)
        poDS = ogr.Open(ogrLayer, False)
        if poDS is None:
            SextanteLog.addToLog(SextanteLog.LOG_ERROR, self.failure(ogrLayer))
            return

        srs = osr.SpatialReference()
        srs.ImportFromEPSG(21781)  # FIXME
        qDebug("Creating output '%s'" % dst_ds)
        if dst_format == "SQLite" and os.path.isfile(dst_ds):
            os.remove(dst_ds)
        qDebug("Using driver '%s'" % dst_format)
        driver = ogr.GetDriverByName(dst_format)
        poDstDS = driver.CreateDataSource(dst_ds, options=ogr_dsco)
        if poDstDS is None:
            SextanteLog.addToLog(
                SextanteLog.LOG_ERROR, "Error creating %s" % dst_ds)
            return
        self.ogrtransform(poDS, poDstDS, bOverwrite=True)
        #ogr2ogr(pszFormat = dst_format, pszDataSource = poDS, pszDestDataSource = poDstDS, bOverwrite = True)

    def transformed_template(self, template, substitutions):
        vrt_templ = Template(open(template).read())
        vrt_xml = vrt_templ.substitute(substitutions)
        vrt = tempfile.mktemp('.vrt', 'ogr_', '/vsimem')
        # Create in-memory file
        gdal.FileFromMemBuffer(vrt, vrt_xml)
        return vrt

    def transformed_datasource(self, template, substitutions):
        vrt = transformed_template(template, substitutions)
        ds = ogr.Open(vrt)
        return ds

    def ogrtransform(self,
                     poSrcDS,
                     poDstDS,
                     papszLayers=[],
                     papszLCO=[],
                     bTransform=False,
                     bAppend=False,
                     bUpdate=False,
                     bOverwrite=False,
                     poOutputSRS=None,
                     poSourceSRS=None,
                     pszNewLayerName=None,
                     pszWHERE=None,
                     papszSelFields=None,
                     eGType=-2,
                     eGeomOp=GeomOperation.NONE,
                     dfGeomOpParam=0,
                     papszFieldTypesToString=[],
                     pfnProgress=None,
                     pProgressData=None,
                     nCountLayerFeatures=0,
                     poClipSrc=None,
                     poClipDst=None,
                     bExplodeCollections=False,
                     pszZField=None):

        # Process each data source layer
        if len(papszLayers) == 0:
            nLayerCount = poSrcDS.GetLayerCount()
            papoLayers = [None for i in range(nLayerCount)]
            iLayer = 0

            for iLayer in range(nLayerCount):
                poLayer = poSrcDS.GetLayer(iLayer)

                if poLayer is None:
                    SextanteLog.addToLog(
                        SextanteLog.LOG_ERROR, "FAILURE: Couldn't fetch advertised layer %d!" % iLayer)
                    return False

                papoLayers[iLayer] = poLayer
                iLayer = iLayer + 1

        # Process specified data source layers
        else:
            nLayerCount = len(papszLayers)
            papoLayers = [None for i in range(nLayerCount)]
            iLayer = 0

            for layername in papszLayers:
                poLayer = poSrcDS.GetLayerByName(layername)

                if poLayer is None:
                    SextanteLog.addToLog(
                        SextanteLog.LOG_ERROR, "FAILURE: Couldn't fetch advertised layer %s!" % layername)
                    return False

                papoLayers[iLayer] = poLayer
                iLayer = iLayer + 1

        for poSrcLayer in papoLayers:
            qDebug(poSrcLayer.GetLayerDefn().GetName())
            # TODO: poDstDS.GetLayerByName for VRT layer fails if name is not
            # lower case

            ok = TranslateLayer(poSrcDS, poSrcLayer, poDstDS, papszLCO, pszNewLayerName,
                                bTransform, poOutputSRS, poSourceSRS, papszSelFields,
                                bAppend, eGType, bOverwrite, eGeomOp, dfGeomOpParam,
                                papszFieldTypesToString, nCountLayerFeatures,
                                poClipSrc, poClipDst, bExplodeCollections, pszZField, pszWHERE,
                                pfnProgress, pProgressData)
        return True


class Ogr2OgrVrt(Ogr2Ogr):

    INPUT_VRT = "INPUT_VRT"
    BASE_DIR = "BASE_DIR"
    TEMPL_VARS = "TEMPL_VARS"

    def defineCharacteristics(self):
        self.name = "VRT transformation"
        self.group = "Transformation"

        self.addParameter(ParameterString(
            self.INPUT_VRT, "VRT template", "/home/pi/code/gis/geodb-gl/import_np/NPGlarus.vrt"))
        self.addParameter(ParameterString(
            self.BASE_DIR, "Base path for data", "/home/pi/code/gis/geodb-gl/import_np"))
        self.addParameter(ParameterString(
            self.TEMPL_VARS, "Template variables (var1=value1;var2=value2,...)", "srcdata=NPRiedern.ITF,RaumPL_GL_v10304.ili;bfsnr=1625"))
        self.addParameter(ParameterString(
            self.DEST_FORMAT, "Destination Format", "ESRI Shapefile"))  # SQLite
        # SPATIALITE=YES
        self.addParameter(
            ParameterString(self.DEST_DSCO, "Creation Options", ""))

        self.addOutput(OutputVector(self.OUTPUT_LAYER, "Output layer"))

    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        input = self.getParameterValue(self.INPUT_VRT)
        base_dir = self.getParameterValue(self.BASE_DIR)
        templ_vars_str = self.getParameterValue(self.TEMPL_VARS)
        templ_vars = {}
        for pair in string.split(templ_vars_str, ';'):
            var, val = string.split(pair, '=')
            templ_vars[var] = val
        qDebug("Template vars '%s'" % templ_vars)
        output = self.getOutputValue(self.OUTPUT_LAYER)

        dst_ds = self.ogrConnectionString(output)
        dst_format = self.getParameterValue(self.DEST_FORMAT)
        ogr_dsco = [self.getParameterValue(self.DEST_DSCO)]  # TODO: split

        os.chdir(base_dir)
        # TODO: separate process step for nested templates
        templ_vars['ds'] = self.transformed_template(
            'custom-enums.vrt', templ_vars)
        ogrLayer = self.transformed_template(input, templ_vars)
        qDebug("Opening data source '%s'" % ogrLayer)
        poDS = ogr.Open(ogrLayer, False)
        if poDS is None:
            SextanteLog.addToLog(SextanteLog.LOG_ERROR, self.failure(ogrLayer))
            return

        qDebug("Creating output '%s'" % dst_ds)
        if dst_format == "SQLite" and os.path.isfile(dst_ds):
            os.remove(dst_ds)
        driver = ogr.GetDriverByName(dst_format)
        poDstDS = driver.CreateDataSource(dst_ds, options=ogr_dsco)
        if poDstDS is None:
            SextanteLog.addToLog(
                SextanteLog.LOG_ERROR, "Error creating %s" % dst_ds)
            return
        self.ogrtransform(poDS, poDstDS, bOverwrite=True)

        # Free memory associated with the in-memory file
        gdal.Unlink(templ_vars['ds'])

from sextante.core.GeoAlgorithm import GeoAlgorithm
from sextante.outputs.OutputVector import OutputVector
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
import string
import re
import os
import ogr
import gdal
import osr


class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

GeomOperation = Enum(["NONE", "SEGMENTIZE", "SIMPLIFY_PRESERVE_TOPOLOGY"])


class Ogr2Ogr(OgrAlgorithm):

    #constants used to refer to parameters and outputs.
    #They will be used when calling the algorithm from another algorithm,
    #or when calling SEXTANTE from the QGIS console.
    OUTPUT_LAYER = "OUTPUT_LAYER"
    INPUT_LAYER = "INPUT_LAYER"
    DEST_DS = "DEST_DS"
    DEST_FORMAT = "DEST_FORMAT"
    DEST_DSCO = "DEST_DSCO"

    def defineCharacteristics(self):
        self.name = "ogr2ogr"
        self.group = "Transformation"

        #we add the input vector layer. It can have any kind of geometry
        #It is a mandatory (not optional) one, hence the False argument
        self.addParameter(ParameterVector(self.INPUT_LAYER, "Input layer", ParameterVector.VECTOR_TYPE_ANY, False))
        #self.addParameter(ParameterString(self.DEST_DS, "Output DS", "/tmp/out.sqlite"))
        self.addParameter(ParameterString(self.DEST_FORMAT, "Destination Format", "SQLite"))
        self.addParameter(ParameterString(self.DEST_DSCO, "Creation Options", "SPATIALITE=YES"))

        self.addOutput(OutputVector(self.OUTPUT_LAYER, "Output layer"))

    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        input = self.getParameterValue(self.INPUT_LAYER)
        ogrLayer = self.ogrConnectionString(input)
        output = self.getOutputValue(self.OUTPUT_LAYER)

        #dst_ds = self.getParameterValue(self.DEST_DS)
        dst_ds = self.ogrConnectionString(output)
        dst_format = self.getParameterValue(self.DEST_FORMAT)
        ogr_dsco = [self.getParameterValue(self.DEST_DSCO)] #TODO: split
        #dst_ds = "PG:dbname='glarus_np' options='-c client_encoding=LATIN9'"
        #dst_format ="PostgreSQL"

        qDebug("Opening data source '%s'" % ogrLayer)
        poDS = ogr.Open( ogrLayer, False )
        if poDS is None:
            SextanteLog.addToLog(SextanteLog.LOG_ERROR, self.failure(ogrLayer))
            return

        srs = osr.SpatialReference()
        srs.ImportFromEPSG( 21781 )
        qDebug("Creating output '%s'" % dst_ds)
        if dst_format == "SQLite" and os.path.isfile(dst_ds):
            os.remove(dst_ds)
        qDebug("Using driver '%s'" % dst_format)
        driver = ogr.GetDriverByName(dst_format)
        poDstDS = driver.CreateDataSource(dst_ds, options = ogr_dsco)
        if poDstDS is None:
            SextanteLog.addToLog(SextanteLog.LOG_ERROR, "Error creating %s" % dst_ds)
            return
        #self.ogrtransform(poDS,  poDstDS,  bOverwrite = True,  poOutputSRS = srs,  poSourceSRS = srs)
        self.ogrtransform(poDS, poDstDS, bOverwrite = True)

    def vrtsource(self, vrt, vars):
        vrt_templ = Template(open(vrt).read())
        vrt_xml = vrt_templ.substitute(vars)
        gdal.FileFromMemBuffer('/vsimem/input.vrt', vrt_xml)
        poSrcDS = ogr.Open('/vsimem/input.vrt')
        return poSrcDS

    def ogrtransform(self, 
                     poSrcDS,
                    poDstDS,
                    papszLayers = [],
                    papszLCO = [],
                    bTransform = False,
                    bAppend = False,
                    bUpdate = False,
                    bOverwrite = False,
                    poOutputSRS = None,
                    poSourceSRS = None,
                    pszNewLayerName = None,
                    pszWHERE = None,
                    papszSelFields = None,
                    eGType = -2,
                    eGeomOp = GeomOperation.NONE,
                    dfGeomOpParam = 0,
                    papszFieldTypesToString = [],
                    pfnProgress = None,
                    pProgressData = None,
                    nCountLayerFeatures = 0,
                    poClipSrc = None,
                    poClipDst = None,
                    bExplodeCollections = False,
                    pszZField = None):

        qDebug("ogrtransform")
        for iLayer in range(poSrcDS.GetLayerCount()): #TODO: use papszLayers
          poSrcLayer = poSrcDS.GetLayer(iLayer)
          qDebug(poSrcLayer.GetLayerDefn().GetName())
          #TODO: poDstDS.GetLayerByName for VRT layer fails if name is not lower case

          TranslateLayer( poSrcDS, poSrcLayer, poDstDS, papszLCO, pszNewLayerName, \
                        bTransform,  poOutputSRS, poSourceSRS, papszSelFields, \
                        bAppend, eGType, bOverwrite, eGeomOp, dfGeomOpParam, \
                        papszFieldTypesToString, nCountLayerFeatures, \
                        poClipSrc, poClipDst, bExplodeCollections, pszZField, pszWHERE, \
                        pfnProgress, pProgressData)


# --------------------------------------------------
# From ogr2ogr.py implementation included in GDAL/OGR
# --------------------------------------------------

bSkipFailures = False
nGroupTransactions = 200
bPreserveFID = False
nFIDToFetch = ogr.NullFID

def CSLFindString(v, mystr):
    i = 0
    for strIter in v:
        if EQUAL(strIter, mystr):
            return i
        i = i + 1
    return -1

def IsNumber( pszStr):
    try:
        (float)(pszStr)
        return True
    except:
        return False

def LoadGeometry( pszDS, pszSQL, pszLyr, pszWhere):
    poGeom = None

    poDS = ogr.Open( pszDS, False )
    if poDS is None:
        return None

    if pszSQL is not None:
        poLyr = poDS.ExecuteSQL( pszSQL, None, None )
    elif pszLyr is not None:
        poLyr = poDS.GetLayerByName(pszLyr)
    else:
        poLyr = poDS.GetLayer(0)

    if poLyr is None:
        qDebug("Failed to identify source layer from datasource.")
        poDS.Destroy()
        return None

    if pszWhere is not None:
        poLyr.SetAttributeFilter(pszWhere)

    poFeat = poLyr.GetNextFeature()
    while poFeat is not None:
        poSrcGeom = poFeat.GetGeometryRef()
        if poSrcGeom is not None:
            eType = wkbFlatten(poSrcGeom.GetGeometryType())

            if poGeom is None:
                poGeom = ogr.Geometry( ogr.wkbMultiPolygon )

            if eType == ogr.wkbPolygon:
                poGeom.AddGeometry( poSrcGeom )
            elif eType == ogr.wkbMultiPolygon:
                for iGeom in range(poSrcGeom.GetGeometryCount()):
                    poGeom.AddGeometry(poSrcGeom.GetGeometryRef(iGeom) )

            else:
                qDebug("ERROR: Geometry not of polygon type." )
                if pszSQL is not None:
                    poDS.ReleaseResultSet( poLyr )
                poDS.Destroy()
                return None

        poFeat = poLyr.GetNextFeature()

    if pszSQL is not None:
        poDS.ReleaseResultSet( poLyr )
    poDS.Destroy()

    return poGeom


def wkbFlatten(x):
    return x & (~ogr.wkb25DBit)

#/************************************************************************/
#/*                               SetZ()                                 */
#/************************************************************************/

def SetZ (poGeom, dfZ ):

    if poGeom is None:
        return

    eGType = wkbFlatten(poGeom.GetGeometryType())
    if eGType == ogr.wkbPoint:
        poGeom.SetPoint(0, poGeom.GetX(), poGeom.GetY(), dfZ)

    elif eGType == ogr.wkbLineString or \
         eGType == ogr.wkbLinearRing:
        for i in range(poGeom.GetPointCount()):
            poGeom.SetPoint(i, poGeom.GetX(i), poGeom.GetY(i), dfZ)

    elif eGType == ogr.wkbPolygon or \
         eGType == ogr.wkbMultiPoint or \
         eGType == ogr.wkbMultiLineString or \
         eGType == ogr.wkbMultiPolygon or \
         eGType == ogr.wkbGeometryCollection:
        for i in range(poGeom.GetGeometryCount()):
            SetZ(poGeom.GetGeometryRef(i), dfZ)

#/************************************************************************/
#/*                           TranslateLayer()                           */
#/************************************************************************/

def TranslateLayer( poSrcDS, poSrcLayer, poDstDS, papszLCO, pszNewLayerName, \
                    bTransform,  poOutputSRS, poSourceSRS, papszSelFields, \
                    bAppend, eGType, bOverwrite, eGeomOp, dfGeomOpParam, \
                    papszFieldTypesToString, nCountLayerFeatures, \
                    poClipSrc, poClipDst, bExplodeCollections, pszZField, pszWHERE, \
                    pfnProgress, pProgressData) :

    bForceToPolygon = False
    bForceToMultiPolygon = False
    bForceToMultiLineString = False

    if pszNewLayerName is None:
        pszNewLayerName = poSrcLayer.GetLayerDefn().GetName()

    if wkbFlatten(eGType) == ogr.wkbPolygon:
        bForceToPolygon = True
    elif wkbFlatten(eGType) == ogr.wkbMultiPolygon:
        bForceToMultiPolygon = True
    elif wkbFlatten(eGType) == ogr.wkbMultiLineString:
        bForceToMultiLineString = True

#/* -------------------------------------------------------------------- */
#/*      Setup coordinate transformation if we need it.                  */
#/* -------------------------------------------------------------------- */
    poCT = None

    if bTransform:
        if poSourceSRS is None:
            poSourceSRS = poSrcLayer.GetSpatialRef()

        if poSourceSRS is None:
            qDebug("Can't transform coordinates, source layer has no\n" + \
                    "coordinate system.  Use -s_srs to set one." )
            return False

        poCT = osr.CoordinateTransformation( poSourceSRS, poOutputSRS )
        if gdal.GetLastErrorMsg().find( 'Unable to load PROJ.4 library' ) != -1:
            poCT = None

        if poCT is None:
            pszWKT = None

            qDebug("Failed to create coordinate transformation between the\n" + \
                "following coordinate systems.  This may be because they\n" + \
                "are not transformable, or because projection services\n" + \
                "(PROJ.4 DLL/.so) could not be loaded." )

            pszWKT = poSourceSRS.ExportToPrettyWkt( 0 )
            qDebug( "Source:\n" + pszWKT )

            pszWKT = poOutputSRS.ExportToPrettyWkt( 0 )
            qDebug( "Target:\n" + pszWKT )
            return False

#/* -------------------------------------------------------------------- */
#/*      Get other info.                                                 */
#/* -------------------------------------------------------------------- */
    poSrcFDefn = poSrcLayer.GetLayerDefn()

    if poOutputSRS is None:
        poOutputSRS = poSrcLayer.GetSpatialRef()

#/* -------------------------------------------------------------------- */
#/*      Find the layer.                                                 */
#/* -------------------------------------------------------------------- */

    #/* GetLayerByName() can instanciate layers that would have been */
    #*/ 'hidden' otherwise, for example, non-spatial tables in a */
    #*/ Postgis-enabled database, so this apparently useless command is */
    #/* not useless... (#4012) */
    gdal.PushErrorHandler('CPLQuietErrorHandler')
    poDstLayer = poDstDS.GetLayerByName(pszNewLayerName)
    gdal.PopErrorHandler()
    gdal.ErrorReset()

    iLayer = -1
    if poDstLayer is not None:
        nLayerCount = poDstDS.GetLayerCount()
        for iLayer in range(nLayerCount):
            poLayer = poDstDS.GetLayer(iLayer)
            # The .cpp version compares on pointers directly, but we cannot
            # do this with swig object, so just compare the names.
            if poLayer is not None \
                and poLayer.GetName() == poDstLayer.GetName():
                break

        if (iLayer == nLayerCount):
            # /* shouldn't happen with an ideal driver */
            poDstLayer = None

#/* -------------------------------------------------------------------- */
#/*      If the user requested overwrite, and we have the layer in       */
#/*      question we need to delete it now so it will get recreated      */
#/*      (overwritten).                                                  */
#/* -------------------------------------------------------------------- */
    if poDstLayer is not None and bOverwrite:
        if poDstDS.DeleteLayer( iLayer ) != 0:
            qDebug("DeleteLayer() failed when overwrite requested." )
            return False

        poDstLayer = None

#/* -------------------------------------------------------------------- */
#/*      If the layer does not exist, then create it.                    */
#/* -------------------------------------------------------------------- */
    if poDstLayer is None:
        if eGType == -2:
            eGType = poSrcFDefn.GetGeomType()

            if bExplodeCollections:
                n25DBit = eGType & ogr.wkb25DBit
                if wkbFlatten(eGType) == ogr.wkbMultiPoint:
                    eGType = ogr.wkbPoint | n25DBit
                elif wkbFlatten(eGType) == ogr.wkbMultiLineString:
                    eGType = ogr.wkbLineString | n25DBit
                elif wkbFlatten(eGType) == ogr.wkbMultiPolygon:
                    eGType = ogr.wkbPolygon | n25DBit
                elif wkbFlatten(eGType) == ogr.wkbGeometryCollection:
                    eGType = ogr.wkbUnknown | n25DBit

            if pszZField is not None:
                eGType = eGType | ogr.wkb25DBit

        if poDstDS.TestCapability( ogr.ODsCCreateLayer ) == False:
            qDebug("Layer " + pszNewLayerName + "not found, and CreateLayer not supported by driver.")
            return False

        gdal.ErrorReset()

        poDstLayer = poDstDS.CreateLayer( pszNewLayerName, poOutputSRS, \
                                            eGType, papszLCO )

        if poDstLayer is None:
            return False

        bAppend = False

#/* -------------------------------------------------------------------- */
#/*      Otherwise we will append to it, if append was requested.        */
#/* -------------------------------------------------------------------- */
    elif not bAppend:
        qDebug("FAILED: Layer " + pszNewLayerName + "already exists, and -append not specified.\n" + \
                            "        Consider using -append, or -overwrite.")
        return False
    else:
        if len(papszLCO) > 0:
            qDebug("WARNING: Layer creation options ignored since an existing layer is\n" + \
                    "         being appended to." )

#/* -------------------------------------------------------------------- */
#/*      Add fields.  Default to copy all field.                         */
#/*      If only a subset of all fields requested, then output only      */
#/*      the selected fields, and in the order that they were            */
#/*      selected.                                                       */
#/* -------------------------------------------------------------------- */

    # Initialize the index-to-index map to -1's
    nSrcFieldCount = poSrcFDefn.GetFieldCount()
    panMap = [ -1 for i in range(nSrcFieldCount) ]

    poDstFDefn = poDstLayer.GetLayerDefn()

    if papszSelFields is not None and not bAppend:

        nDstFieldCount = 0
        if poDstFDefn is not None:
            nDstFieldCount = poDstFDefn.GetFieldCount()

        for iField in range(len(papszSelFields)):

            iSrcField = poSrcFDefn.GetFieldIndex(papszSelFields[iField])
            if iSrcField >= 0:
                poSrcFieldDefn = poSrcFDefn.GetFieldDefn(iSrcField)
                oFieldDefn = ogr.FieldDefn( poSrcFieldDefn.GetNameRef(),
                                            poSrcFieldDefn.GetType() )
                oFieldDefn.SetWidth( poSrcFieldDefn.GetWidth() )
                oFieldDefn.SetPrecision( poSrcFieldDefn.GetPrecision() )

                if papszFieldTypesToString is not None and \
                    (CSLFindString(papszFieldTypesToString, "All") != -1 or \
                    CSLFindString(papszFieldTypesToString, \
                                ogr.GetFieldTypeName(poSrcFieldDefn.GetType())) != -1):

                    oFieldDefn.SetType(ogr.OFTString)

                # The field may have been already created at layer creation
                iDstField = -1;
                if poDstFDefn is not None:
                    iDstField = poDstFDefn.GetFieldIndex(oFieldDefn.GetNameRef())
                if iDstField >= 0:
                    panMap[iSrcField] = iDstField
                elif poDstLayer.CreateField( oFieldDefn ) == 0:
                    # now that we've created a field, GetLayerDefn() won't return NULL
                    if poDstFDefn is None:
                        poDstFDefn = poDstLayer.GetLayerDefn()

                    #/* Sanity check : if it fails, the driver is buggy */
                    if poDstFDefn is not None and \
                        poDstFDefn.GetFieldCount() != nDstFieldCount + 1:
                        qDebug("The output driver has claimed to have added the %s field, but it did not!" %  oFieldDefn.GetNameRef() )
                    else:
                        panMap[iSrcField] = nDstFieldCount
                        nDstFieldCount = nDstFieldCount + 1

            else:
                qDebug("Field '" + papszSelFields[iField] + "' not found in source layer.")
                if not bSkipFailures:
                    return False

        #/* -------------------------------------------------------------------- */
        #/* Use SetIgnoredFields() on source layer if available                  */
        #/* -------------------------------------------------------------------- */

        # Here we differ from the ogr2ogr.cpp implementation since the OGRFeatureQuery
        # isn't mapped to swig. So in that case just don't use SetIgnoredFields()
        # to avoid issue raised in #4015
        if poSrcLayer.TestCapability(ogr.OLCIgnoreFields) and pszWHERE is None:
            papszIgnoredFields = []
            for iSrcField in range(nSrcFieldCount):
                pszFieldName = poSrcFDefn.GetFieldDefn(iSrcField).GetNameRef()
                bFieldRequested = False
                for iField in range(len(papszSelFields)):
                    if EQUAL(pszFieldName, papszSelFields[iField]):
                        bFieldRequested = True
                        break

                if pszZField is not None and EQUAL(pszFieldName, pszZField):
                    bFieldRequested = True

                #/* If source field not requested, add it to ignored files list */
                if not bFieldRequested:
                    papszIgnoredFields.append(pszFieldName)

            poSrcLayer.SetIgnoredFields(papszIgnoredFields)

    elif not bAppend:

        nDstFieldCount = 0
        if poDstFDefn is not None:
            nDstFieldCount = poDstFDefn.GetFieldCount()

        for iField in range(nSrcFieldCount):

            poSrcFieldDefn = poSrcFDefn.GetFieldDefn(iField)
            oFieldDefn = ogr.FieldDefn( poSrcFieldDefn.GetNameRef(),
                                        poSrcFieldDefn.GetType() )
            oFieldDefn.SetWidth( poSrcFieldDefn.GetWidth() )
            oFieldDefn.SetPrecision( poSrcFieldDefn.GetPrecision() )

            if papszFieldTypesToString is not None and \
                (CSLFindString(papszFieldTypesToString, "All") != -1 or \
                CSLFindString(papszFieldTypesToString, \
                            ogr.GetFieldTypeName(poSrcFieldDefn.GetType())) != -1):

                oFieldDefn.SetType(ogr.OFTString)

            # The field may have been already created at layer creation 
            iDstField = -1;
            if poDstFDefn is not None:
                 iDstField = poDstFDefn.GetFieldIndex(oFieldDefn.GetNameRef())
            if iDstField >= 0:
                panMap[iField] = iDstField
            elif poDstLayer.CreateField( oFieldDefn ) == 0:
                # now that we've created a field, GetLayerDefn() won't return NULL
                if poDstFDefn is None:
                    poDstFDefn = poDstLayer.GetLayerDefn()

                #/* Sanity check : if it fails, the driver is buggy */
                if poDstFDefn is not None and \
                    poDstFDefn.GetFieldCount() != nDstFieldCount + 1:
                    qDebug("The output driver has claimed to have added the %s field, but it did not!" %  oFieldDefn.GetNameRef() )
                else:
                    panMap[iField] = nDstFieldCount
                    nDstFieldCount = nDstFieldCount + 1

    else:
        #/* For an existing layer, build the map by fetching the index in the destination */
        #/* layer for each source field */
        if poDstFDefn is None:
            qDebug( "poDstFDefn == NULL.\n" )
            return False

        for iField in range(nSrcFieldCount):
            poSrcFieldDefn = poSrcFDefn.GetFieldDefn(iField)
            iDstField = poDstFDefn.GetFieldIndex(poSrcFieldDefn.GetNameRef())
            if iDstField >= 0:
                panMap[iField] = iDstField

#/* -------------------------------------------------------------------- */
#/*      Transfer features.                                              */
#/* -------------------------------------------------------------------- */
    nFeaturesInTransaction = 0
    nCount = 0

    iSrcZField = -1
    if pszZField is not None:
        iSrcZField = poSrcFDefn.GetFieldIndex(pszZField)

    poSrcLayer.ResetReading()

    if nGroupTransactions > 0:
        poDstLayer.StartTransaction()

    while True:
        poDstFeature = None

        if nFIDToFetch != ogr.NullFID:

            #// Only fetch feature on first pass.
            if nFeaturesInTransaction == 0:
                poFeature = poSrcLayer.GetFeature(nFIDToFetch)
            else:
                poFeature = None

        else:
            poFeature = poSrcLayer.GetNextFeature()

        if poFeature is None:
            break

        nParts = 0
        nIters = 1
        if bExplodeCollections:
            poSrcGeometry = poFeature.GetGeometryRef()
            if poSrcGeometry is not None:
                eSrcType = wkbFlatten(poSrcGeometry.GetGeometryType())
                if eSrcType == ogr.wkbMultiPoint or \
                   eSrcType == ogr.wkbMultiLineString or \
                   eSrcType == ogr.wkbMultiPolygon or \
                   eSrcType == ogr.wkbGeometryCollection:
                        nParts = poSrcGeometry.GetGeometryCount()
                        nIters = nParts
                        if nIters == 0:
                            nIters = 1

        for iPart in range(nIters):
            nFeaturesInTransaction = nFeaturesInTransaction + 1
            if nFeaturesInTransaction == nGroupTransactions:
                poDstLayer.CommitTransaction()
                poDstLayer.StartTransaction()
                nFeaturesInTransaction = 0

            gdal.ErrorReset()
            poDstFeature = ogr.Feature( poDstLayer.GetLayerDefn() )

            if poDstFeature.SetFromWithMap( poFeature, 1, panMap ) != 0:

                if nGroupTransactions > 0:
                    poDstLayer.CommitTransaction()

                qDebug("Unable to translate feature %d from layer %s" % (poFeature.GetFID() , poSrcFDefn.GetName() ))

                return False

            if bPreserveFID:
                poDstFeature.SetFID( poFeature.GetFID() )

            poDstGeometry = poDstFeature.GetGeometryRef()
            if poDstGeometry is not None:

                if nParts > 0:
                    # /* For -explodecollections, extract the iPart(th) of the geometry */
                    poPart = poDstGeometry.GetGeometryRef(iPart).Clone()
                    poDstFeature.SetGeometryDirectly(poPart)
                    poDstGeometry = poPart

                if iSrcZField != -1:
                    SetZ(poDstGeometry, poFeature.GetFieldAsDouble(iSrcZField))
                    # /* This will correct the coordinate dimension to 3 */
                    poDupGeometry = poDstGeometry.Clone()
                    poDstFeature.SetGeometryDirectly(poDupGeometry)
                    poDstGeometry = poDupGeometry

                if eGeomOp == GeomOperation.SEGMENTIZE:
                    pass
                    #/*if (poDstFeature.GetGeometryRef() is not None and dfGeomOpParam > 0)
                    #    poDstFeature.GetGeometryRef().segmentize(dfGeomOpParam);*/
                elif eGeomOp == GeomOperation.SIMPLIFY_PRESERVE_TOPOLOGY and dfGeomOpParam > 0:
                    poNewGeom = poDstGeometry.SimplifyPreserveTopology(dfGeomOpParam)
                    if poNewGeom is not None:
                        poDstFeature.SetGeometryDirectly(poNewGeom)
                        poDstGeometry = poNewGeom

                if poClipSrc is not None:
                    poClipped = poDstGeometry.Intersection(poClipSrc)
                    if poClipped is None or poClipped.IsEmpty():
                        #/* Report progress */
                        nCount = nCount +1
                        if pfnProgress is not None:
                            pfnProgress(nCount * 1.0 / nCountLayerFeatures, "", pProgressData)
                        continue

                    poDstFeature.SetGeometryDirectly(poClipped)
                    poDstGeometry = poClipped

                if poCT is not None:
                    eErr = poDstGeometry.Transform( poCT )
                    if eErr != 0:
                        if nGroupTransactions > 0:
                            poDstLayer.CommitTransaction()

                        qDebug("Failed to reproject feature %d (geometry probably out of source or destination SRS)." % poFeature.GetFID())
                        if not bSkipFailures:
                            return False

                elif poOutputSRS is not None:
                    poDstGeometry.AssignSpatialReference(poOutputSRS)

                if poClipDst is not None:
                    poClipped = poDstGeometry.Intersection(poClipDst)
                    if poClipped is None or poClipped.IsEmpty():
                        #/* Report progress */
                        nCount = nCount +1
                        if pfnProgress is not None:
                            pfnProgress(nCount * 1.0 / nCountLayerFeatures, "", pProgressData)
                        continue

                    poDstFeature.SetGeometryDirectly(poClipped)
                    poDstGeometry = poClipped

                if bForceToPolygon:
                    poDstFeature.SetGeometryDirectly(ogr.ForceToPolygon(poDstGeometry))

                elif bForceToMultiPolygon:
                    poDstFeature.SetGeometryDirectly(ogr.ForceToMultiPolygon(poDstGeometry))

                elif bForceToMultiLineString:
                    poDstFeature.SetGeometryDirectly(ogr.ForceToMultiLineString(poDstGeometry))

            gdal.ErrorReset()
            if poDstLayer.CreateFeature( poDstFeature ) != 0 and not bSkipFailures:
                if nGroupTransactions > 0:
                    poDstLayer.RollbackTransaction()

                return False

        #/* Report progress */
        nCount = nCount  + 1
        if pfnProgress is not None:
            pfnProgress(nCount * 1.0 / nCountLayerFeatures, "", pProgressData)

    if nGroupTransactions > 0:
        poDstLayer.CommitTransaction()

    return True

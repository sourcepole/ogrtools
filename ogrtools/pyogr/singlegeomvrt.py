from osgeo import ogr
from ogrvrt import GeomType2Name, Esc


def has_multi_geom_tables(infile):
    has_multi = False
    ds = ogr.Open(infile, update=0)
    if ds is None:
        return False
    for iLayer in range(ds.GetLayerCount()):
        poLayer = ds.GetLayer(iLayer)
        if poLayer is not None:
            if poLayer.GetLayerDefn().GetGeomFieldCount() > 1:
                has_multi = True
                break
    return has_multi


def ogr2vrt(infile,
            outfile=None,
            relative="0"):

    src_ds = ogr.Open(infile, update=0)

    if src_ds is None:
        return None

    vrt = '<OGRVRTDataSource>\n'

    for iLayer in range(src_ds.GetLayerCount()):
        layer = src_ds.GetLayer(iLayer)
        nGeomFieldCount = layer.GetLayerDefn().GetGeomFieldCount()
        if nGeomFieldCount > 0:
            for iGeomField in range(nGeomFieldCount):
                vrt += vrt_layer(layer, infile, nGeomFieldCount > 1,
                                 iGeomField)
        else:
            vrt += vrt_layer(layer, infile, False, None)

    vrt += '</OGRVRTDataSource>\n'

    if outfile is not None:
        f = open(outfile, "w")
        f.write(vrt)
        f.close()

    return vrt


def vrt_layer(layer,
              infile,
              multiGeom,
              iGeom,
              relative="0"):
    layerdef = layer.GetLayerDefn()
    name = layerdef.GetName()
    if multiGeom:
        poGFldDefn = layerdef.GetGeomFieldDefn(iGeom)
        gFldType = GeomType2Name(poGFldDefn.GetType())
        gFldName = poGFldDefn.GetNameRef()
        nameSuffix = '_%s' % gFldName
    else:
        poGFldDefn = None
        gFldType = 'wkbUnknown'
        nameSuffix = ''

    vrt = ''
    vrt += '  <OGRVRTLayer name="%s">\n' % Esc(name+nameSuffix)
    vrt += '    <SrcDataSource relativeToVRT="%s" shared="%d">%s</SrcDataSource>\n' \
           % (relative, True, Esc(str(infile)))
    vrt += '    <SrcLayer>%s</SrcLayer>\n' % Esc(name)
    vrt += '    <GeometryType>%s</GeometryType>\n' % gFldType
    if poGFldDefn is not None:
        vrt += '    <GeometryField name="%s"/>\n' % gFldName
        if poGFldDefn.GetSpatialRef() is not None:
            vrt += '    <LayerSRS>%s</LayerSRS>\n' \
                   % (Esc(poGFldDefn.GetSpatialRef().ExportToWkt()))

    # Process all the fields.
    for fld_index in range(layerdef.GetFieldCount()):
        src_fd = layerdef.GetFieldDefn(fld_index)
        vrt += '    <Field name="%s" type="%s"' \
               % (Esc(src_fd.GetName()),
                  ogr.GetFieldTypeName(src_fd.GetType()))
        vrt += ' src="%s"' % Esc(src_fd.GetName())
        if src_fd.GetWidth() > 0:
            vrt += ' width="%d"' % src_fd.GetWidth()
        if src_fd.GetPrecision() > 0:
            vrt += ' precision="%d"' % src_fd.GetPrecision()
        vrt += '/>\n'

    vrt += '  </OGRVRTLayer>\n'
    return vrt

import json
from xml.etree import ElementTree
import tempfile
import os
from format_handler import FormatHandlerRegistry
from ..interlis.ilismeta import prettify
try:
    from osgeo import ogr
    from osgeo import gdal
except ImportError:
    import ogr
    import gdal

# Mapping of OGR integer geometry types to GeoJSON type names. (from Fiona)

GEOMETRY_TYPES = {
    0: 'Unknown',
    1: 'Point',
    2: 'LineString',
    3: 'Polygon',
    4: 'MultiPoint',
    5: 'MultiLineString',
    6: 'MultiPolygon',
    7: 'GeometryCollection',
    100: 'None',
    101: 'LinearRing',
    0x80000001: '3D Point',
    0x80000002: '3D LineString',
    0x80000003: '3D Polygon',
    0x80000004: '3D MultiPoint',
    0x80000005: '3D MultiLineString',
    0x80000006: '3D MultiPolygon',
    0x80000007: '3D GeometryCollection'
}

# Mapping of OGR integer field types to VRT field type names.

FIELD_TYPES = [
    'Integer',      # OFTInteger, Simple 32bit integer
    'IntegerList',  # OFTIntegerList, List of 32bit integers
    'Real',         # OFTReal, Double Precision floating point
    'RealList',     # OFTRealList, List of doubles
    'String',       # OFTString, String of ASCII chars
    'StringList',   # OFTStringList, Array of strings
    None,           # OFTWideString, deprecated
    None,           # OFTWideStringList, deprecated
    'Binary',       # OFTBinary, Raw Binary data
    'Date',         # OFTDate, Date
    'Time',         # OFTTime, Time
    'DateTime'      # OFTDateTime, Date and Time
]


def ogr2ogr(dst_format, ds, dest, bOverwrite, dsco=[], lco=[], layers=[], skipfailures=False):    # poOutputSRS=srs, poSourceSRS=srs
    # Get the input Layers
    inDataSource = ds
    layerList = []
    if layers:
        layerList = layers
    else:
        for lyr in inDataSource:
            daLayer = lyr.GetName()
            if not daLayer in layerList:
                layerList.append(daLayer)

    # Create the output Layers
    outDriver = ogr.GetDriverByName(dst_format)

    # Remove output shapefile if it already exists
    # if os.path.exists(dest):
    #     outDriver.DeleteDataSource(dest)

    # Create the output shapefile
    outDataSource = outDriver.CreateDataSource(dest)
    for layer in layerList:
        inLayer = inDataSource.GetLayer(layer)
        inLayerDefn = inLayer.GetLayerDefn()
        nGeomFieldCount = inLayerDefn.GetGeomFieldCount()

        multiGeomSupported = outDataSource.TestCapability(ogr.ODsCCreateGeomFieldAfterCreateLayer)
        if multiGeomSupported:
            outLayer = outDataSource.CreateLayer(layer, geom_type=ogr.wkbNone)
        else:
            outLayer = outDataSource.CreateLayer(layer, geom_type=inLayerDefn.GetGeomType())

        # Add input Layer Fields to the output Layer
        if "Interlis" not in dst_format:  # Interlis fields are created from model
            for i in range(0, inLayerDefn.GetFieldCount()):
                fieldDefn = inLayerDefn.GetFieldDefn(i)
                outLayer.CreateField(fieldDefn)

            if multiGeomSupported:
                for iGeom in range(nGeomFieldCount):
                    poGFldDefn = inLayerDefn.GetGeomFieldDefn(iGeom)
                    outLayer.CreateGeomField(poGFldDefn)

        # Get the output Layer's Feature Definition
        outLayerDefn = outLayer.GetLayerDefn()

        # Add features to the ouput Layer
        for inFeature in inLayer:
            # Create output Feature
            outFeature = ogr.Feature(outLayerDefn)

            # Add field values from input Layer
            for i in range(0, outLayerDefn.GetFieldCount()):
                fieldName = outLayerDefn.GetFieldDefn(i).GetNameRef()
                src_idx = inLayerDefn.GetFieldIndex(fieldName)
                if inFeature.IsFieldSet(src_idx):
                    outFeature.SetField(i, inFeature.GetField(src_idx))

            # Add geometry values
            for iGeom in range(nGeomFieldCount):
                geom = inFeature.GetGeomFieldRef(iGeom)
                if geom is not None:
                    outFeature.SetGeomField(iGeom, geom.Clone())

            # Add new feature to output Layer
            outLayer.CreateFeature(outFeature)

    # Close DataSources
    inDataSource.Destroy()
    outDataSource.Destroy()


class OgrConfig:
    """OGR transformation configuration"""

    format_handlers = FormatHandlerRegistry()

    def __init__(self, ds=None, config=None, model=None):
        self._ds_fn = ds
        self._ds = None
        self._config = self._load(config)
        self._model = model
        #if not self._model:
        #    if ds:
        #        self._model = ds.split(',')[-1]

    def _load(self, fn):
        config = None
        if fn is not None:
            with open(fn) as file:
                config = json.load(file)
        return config

    def is_loaded(self):
        return (self._config is not None)

    def open(self):
        self._ds = ogr.Open(self._ds_fn, update=False)
        if self._ds is None:
            raise IOError("Couldn't open file: %s" % self._ds_fn)
        return self._ds

    def close(self):
        if self._ds is not None:
            self._ds.Destroy()

    def _enums(self, src_format_handler, dst_format_handler):
        enum_tables = {}
        if self._model:
            enums = src_format_handler.extract_enums(self._model)
            for src_name, values in enums.items():
                dst_name = dst_format_handler.shorten_name(src_name, 'enum')
                dst_name = dst_format_handler.launder_name(dst_name)
                enum_tables[dst_name] = {
                    'src_name': src_name,
                    'values': values
                }
        return enum_tables

    def generate_config(self, dst_format, outfile=None, layer_list=[]):
        if self._ds is None:
            self.open()

        layer_names = list(layer_list)
        if len(layer_names) == 0:
            for layer in self._ds:
                layer_names.append(layer.GetLayerDefn().GetName())

        src_format = self._ds.GetDriver().GetName()
        src_format_handler = OgrConfig.format_handlers.handler(src_format)
        dst_format_handler = OgrConfig.format_handlers.handler(dst_format)

        self._config = {}

        #Javscript comments are not allowed JSON
        self._config['//'] = 'OGR transformation configuration'
        self._config['src_format'] = src_format
        self._config['dst_format'] = dst_format
        self._config['dst_dsco'] = dst_format_handler.default_ds_creation_options()
        self._config['dst_lco'] = dst_format_handler.default_layer_creation_options()
        layers = {}
        self._config['layers'] = layers

        for name in layer_names:
            layer = self._ds.GetLayerByName(name)
            if layer is None:
                raise ValueError("Layer '%s' not found" % name)
            layerdef = layer.GetLayerDefn()

            cfglayer = {}
            layer_name = dst_format_handler.launder_name(name)
            layers[layer_name] = cfglayer
            cfglayer['src_layer'] = name

            fields = {}
            cfglayer['fields'] = fields
            for fld_index in range(layerdef.GetFieldCount()):
                src_fd = layerdef.GetFieldDefn(fld_index)
                cfgfield = {}
                field_name = src_fd.GetName()
                dst_name = dst_format_handler.launder_name(field_name)
                fields[dst_name] = cfgfield
                cfgfield['src'] = field_name
                jsontype = FIELD_TYPES[src_fd.GetType()]
                cfgfield['type'] = jsontype
                if src_fd.GetWidth() > 0:
                    cfgfield['width'] = src_fd.GetWidth()
                if src_fd.GetPrecision() > 0:
                    cfgfield['precision'] = src_fd.GetPrecision()

            geom_field_count = layerdef.GetGeomFieldCount()
            if geom_field_count > 0:
                geom_fields = {}
                cfglayer['geom_fields'] = geom_fields
                for fld_index in range(geom_field_count):
                    src_fd = layerdef.GetGeomFieldDefn(fld_index)
                    cfgfield = {}
                    field_name = src_fd.GetName()
                    if field_name:
                        dst_name = dst_format_handler.launder_name(field_name)
                        geom_fields[dst_name] = cfgfield
                        cfgfield['src'] = field_name
                        cfgfield['type'] = GEOMETRY_TYPES[src_fd.GetType()]

            geom_type = GEOMETRY_TYPES[layerdef.GetGeomType()]
            cfglayer['geometry_type'] = geom_type

        enum_tables = self._enums(src_format_handler, dst_format_handler)
        if enum_tables:
            self._config['enums'] = enum_tables

        configstr = json.dumps(self._config, indent=2)

        if outfile is not None:
            f = open(outfile, "w")
            f.write(configstr)
            f.close()

        return configstr

    def src_format(self):
        return self._config['src_format']

    def ds_format(self):
        if self._ds is None:
            self.open()
        return self._ds.GetDriver().GetName()

    def dst_format(self):
        return self._config['dst_format']

    def layer_creation_options(self):
        options = []
        for key, value in self._config['dst_lco'].items():
            options.append(key + "=" + value)
        return options

    def ds_creation_options(self):
        options = []
        for key, value in self._config['dst_dsco'].items():
            options.append(key + "=" + value)
        return options

    def layer_names(self):
        if self._config and 'layers' in self._config:
            return self._config['layers'].keys()
        else:
            return []

    def enum_names(self):
        if self._config and 'enums' in self._config:
            return self._config['enums'].keys()
        else:
            return []

    def layer_infos(self):
        """Return Dict with layer name and geometry field name for each layer (one per geometry)"""
        layers = []
        if self._config and 'layers' in self._config:
            for name, cfglayer in self._config['layers'].items():
                layer = {"name": name}
                if 'geom_fields' in cfglayer:
                    for geom_name, cfgfield in cfglayer['geom_fields'].items():
                        layer['geom_field'] = geom_name
                        layers.append(layer)
                    #handle empty cfglayer['geom_fields'] (e.g. Shape file)
                    if 'geom_field' not in layer:
                        layers.append(layer)
                else:
                    layers.append(layer)
        return layers

    def enum_infos(self):
        """Return layer infos for enums"""
        layers = []
        for enum in self.enum_names():
            layers.append({"name": enum})
        return layers

    def generate_vrt(self, dst_format=None):
        #if dst_format is None:
        #    dst_format = self.dst_format()
        #dst_format_handler = OgrConfig.format_handlers.handler(dst_format)
        xml = ElementTree.Element('OGRVRTDataSource')
        for layer_name, cfglayer in self._config['layers'].items():
            layer_node = ElementTree.SubElement(xml, "OGRVRTLayer")
            layer_node.set('name', layer_name)
            node = ElementTree.SubElement(layer_node, "SrcDataSource")
            node.set('relativeToVRT', '0')
            node.set('shared', '1')
            if self._ds_fn is None:
                raise ValueError("Cannot create intermediate VRT - Input DS not defined")
            node.text = self._ds_fn
            node = ElementTree.SubElement(layer_node, "SrcLayer")
            node.text = cfglayer['src_layer']
            for dst_name, cfgfield in cfglayer['fields'].items():
                node = ElementTree.SubElement(layer_node, "Field")
                node.set('name', dst_name)
                node.set('src', cfgfield['src'])
                node.set('type', cfgfield['type'])
                if 'width' in cfgfield:
                    node.set('width', str(cfgfield['width']))
                if 'precision' in cfgfield:
                    node.set('precision', str(cfgfield['precision']))
            if 'geom_fields' in cfglayer:
                for geom_name, cfgfield in cfglayer['geom_fields'].items():
                    node = ElementTree.SubElement(layer_node, "GeometryField")
                    node.set('name', geom_name)
                    node.set('field', cfgfield['src'])
                    node = ElementTree.SubElement(node, "GeometryType")
                    node.text = 'wkb' + cfgfield['type']
            else:
                node = ElementTree.SubElement(layer_node, "GeometryType")
                node.text = 'wkb' + cfglayer['geometry_type']
        return ElementTree.tostring(xml, 'utf-8')

    def generate_reverse_vrt(self, dst_format=None):
        src_format = self.ds_format()
        src_format_handler = OgrConfig.format_handlers.handler(src_format)
        xml = ElementTree.Element('OGRVRTDataSource')
        for layer_name, cfglayer in self._config['layers'].items():
            layer_node = ElementTree.SubElement(xml, "OGRVRTLayer")
            layer_node.set('name', cfglayer['src_layer'])
            node = ElementTree.SubElement(layer_node, "SrcDataSource")
            node.set('relativeToVRT', '0')
            node.set('shared', '1')
            if self._ds_fn is None:
                raise ValueError("Cannot create intermediate VRT - Input DS not defined")
            node.text = self._ds_fn
            node = ElementTree.SubElement(layer_node, "SrcLayer")
            node.text = src_format_handler.layer_name(layer_name)
            for dst_name, cfgfield in cfglayer['fields'].items():
                node = ElementTree.SubElement(layer_node, "Field")
                node.set('name', cfgfield['src'])
                #FIXME: original type, not node.set('type', cfgfield['type'])
                node.set('src', dst_name)
            if 'geom_fields' in cfglayer and src_format != "GeoJSON":  # Workaround for bug in VRT driver?
                for geom_name, cfgfield in cfglayer['geom_fields'].items():
                    node = ElementTree.SubElement(layer_node, "GeometryField")
                    node.set('name', cfgfield['src'])
                    node.set('field', geom_name)
                    node = ElementTree.SubElement(node, "GeometryType")
                    node.text = 'wkb' + cfgfield['type']
            else:
                node = ElementTree.SubElement(layer_node, "GeometryType")
                node.text = 'wkb' + cfglayer['geometry_type']
        return ElementTree.tostring(xml, 'utf-8')

    def generate_enum_gml(self):
        xml = ElementTree.Element('ogr:FeatureCollection')
        xml.set('xmlns:xsi', 'http://ogr.maptools.org/ ogrtools-enums.xsd')
        xml.set('xmlns:schemaLocation', 'http://www.w3.org/2001/XMLSchema-instance')
        xml.set('xmlns:ogr', 'http://ogr.maptools.org/')
        xml.set('xmlns:gml', 'http://www.opengis.net/gml')
        node = ElementTree.SubElement(xml, 'gml:boundedBy')
        node = ElementTree.SubElement(node, 'gml:null')
        node.text = 'missing'
        if self._config['enums']:
            for name, enum_table in self._config['enums'].items():
                for enum in enum_table['values']:
                    # <gml:featureMember>
                    #   <ogr:landcover_type fid="landcover_type.0">
                    #     <ogr:ilicode>building</ogr:ilicode>
                    #     <ogr:dispname>building</ogr:dispname>
                    #   </ogr:landcover_type>
                    # </gml:featureMember>
                    node = ElementTree.SubElement(xml, 'gml:featureMember')
                    feature_node = ElementTree.SubElement(node, 'ogr:{0}'.format(name))
                    feature_node.set('fid', 'ogr:{0}.{1}'.format(name, enum['id']))
                    for colname, value in enum.items():
                        node = ElementTree.SubElement(feature_node, 'ogr:{0}'.format(colname))
                        node.text = str(value)
        return ElementTree.tostring(xml, 'utf-8')

    def _set_ogr_debug_flag(self, debug):
        os.environ["CPL_DEBUG"] = 'ON' if debug else 'OFF'

    def _activate_ogr_log(self):
        # Send OGR C lib output to file
        (ogrlogfd, ogrlogfn) = tempfile.mkstemp()
        os.close(ogrlogfd)
        os.environ["CPL_LOG"] = ogrlogfn
        os.environ["CPL_LOG_ERRORS"] = "ON"
        return ogrlogfn

    def _close_ogr_log(self, ogrlogfn):
        f = open(ogrlogfn, 'r')
        ogroutput = f.read()
        f.close()
        os.unlink(ogrlogfn)
        os.environ["CPL_LOG_ERRORS"] = "OFF"
        return ogroutput

    def transform(self, dest, format=None, layers=[], skipfailures=False, debug=False):
        vrt = self.generate_vrt(dst_format=format)
        #if debug:
        #    print prettify(vrt)
        f = open("/tmp/transform.vrt", "w")
        f.write(prettify(vrt))
        f.close()
        ds = self._tmp_datasource(vrt)
        dst_format = format or self.dst_format()
        dsco = []
        if dst_format == self.dst_format():
            dsco = self.ds_creation_options()
        lco = []
        if dst_format == self.dst_format():
            lco = self.layer_creation_options()
        self._set_ogr_debug_flag(debug)
        ogrlogfn = self._activate_ogr_log()
        ogr2ogr(dst_format=str(dst_format), ds=ds, dest=dest,
                bOverwrite=True, dsco=dsco, lco=lco, layers=layers, skipfailures=skipfailures)
        self._free_tmp_datasource()
        return self._close_ogr_log(ogrlogfn)

    def transform_reverse(self, dest, format=None, layers=[], skipfailures=False, debug=False):
        vrt = self.generate_reverse_vrt(dst_format=format)
        #if debug:
        #    print prettify(vrt)
        ds = self._tmp_datasource(vrt)
        dst_format = format or self.src_format()
        self._set_ogr_debug_flag(debug)
        ogrlogfn = self._activate_ogr_log()
        ogr2ogr(dst_format=str(dst_format), ds=ds, dest=dest,
                bOverwrite=True, layers=layers, skipfailures=skipfailures)
        self._free_tmp_datasource()
        return self._close_ogr_log(ogrlogfn)

    def write_enum_tables(self, dest, format=None, skipfailures=False, debug=False):
        gml = self.generate_enum_gml()
        #if debug:
        #    print prettify(gml)
        ds = self._tmp_datasource(gml)
        dst_format = format or self.dst_format()
        dsco = []
        if dst_format == self.dst_format():
            dsco = self.ds_creation_options()
        lco = []
        if dst_format == self.dst_format():
            lco = self.layer_creation_options()
        ogr2ogr(pszFormat=str(dst_format), pszDataSource=ds,
                pszDestDataSource=dest, bOverwrite=True, papszDSCO=dsco, papszLCO=lco, skipfailures=skipfailures)
        self._free_tmp_datasource()

    def _tmp_memfile(self, data):
        self._vsimem_tmp = tempfile.mktemp('.vrt', 'ogr_', '/vsimem')
        # Create in-memory file
        gdal.FileFromMemBuffer(self._vsimem_tmp, data)
        return self._vsimem_tmp

    def _free_tmp_datasource(self):
        # Free memory associated with the in-memory file
        gdal.Unlink(self._vsimem_tmp)

    def _tmp_datasource(self, data):
        #Call _free_tmp_datasource after closing datasource to free memeroy
        vrt = self._tmp_memfile(data)
        ds = ogr.Open(vrt)
        return ds

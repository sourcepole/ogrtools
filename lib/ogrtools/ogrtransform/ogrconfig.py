import json
from xml.etree import ElementTree
import tempfile
import os
from format_handler import FormatHandlerRegistry
from ..pyogr.ogr2ogr import ogr2ogr
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


class OgrConfig:
    """OGR transformation configuration"""

    format_handlers = FormatHandlerRegistry()

    def __init__(self, ds=None, config=None, model=None):
        self._ds_fn = ds
        self._ds = None
        self._config = self._load(config)
        self._model = model

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
            node.text = self._ds_fn
            node = ElementTree.SubElement(layer_node, "SrcLayer")
            node.text = cfglayer['src_layer']
            node = ElementTree.SubElement(layer_node, "GeometryType")
            node.text = 'wkb' + cfglayer['geometry_type']
            for dst_name, cfgfield in cfglayer['fields'].items():
                node = ElementTree.SubElement(layer_node, "Field")
                node.set('name', dst_name)
                node.set('src', cfgfield['src'])
                node.set('type', cfgfield['type'])
                if 'width' in cfgfield:
                    node.set('width', str(cfgfield['width']))
                if 'precision' in cfgfield:
                    node.set('precision', str(cfgfield['precision']))
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
            node.text = self._ds_fn
            node = ElementTree.SubElement(layer_node, "SrcLayer")
            node.text = src_format_handler.layer_name(layer_name)
            node = ElementTree.SubElement(layer_node, "GeometryType")
            node.text = 'wkb' + cfglayer['geometry_type']
            for dst_name, cfgfield in cfglayer['fields'].items():
                node = ElementTree.SubElement(layer_node, "Field")
                node.set('name', cfgfield['src'])
                #FIXME: original type, not node.set('type', cfgfield['type'])
                node.set('src', dst_name)
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

    def transform(self, dest, format=None, layers=[], debug=False):
        vrt = self.generate_vrt(dst_format=format)
        #if debug:
        #    print prettify(vrt)
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
        ogr2ogr(pszFormat=str(dst_format), pszDataSource=ds, pszDestDataSource=dest,
                bOverwrite=True, papszDSCO=dsco, papszLCO=lco, papszLayers=layers)  # poOutputSRS=srs, poSourceSRS=srs
        self._free_tmp_datasource()
        return self._close_ogr_log(ogrlogfn)

    def transform_reverse(self, dest, format=None, layers=[], debug=False):
        vrt = self.generate_reverse_vrt(dst_format=format)
        #if debug:
        #    print prettify(vrt)
        ds = self._tmp_datasource(vrt)
        dst_format = format or self.src_format()
        self._set_ogr_debug_flag(debug)
        ogrlogfn = self._activate_ogr_log()
        ogr2ogr(pszFormat=str(dst_format), pszDataSource=ds,
                pszDestDataSource=dest, bOverwrite=True, papszLayers=layers)
        self._free_tmp_datasource()
        return self._close_ogr_log(ogrlogfn)

    def write_enum_tables(self, dest, format=None, debug=False):
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
                pszDestDataSource=dest, bOverwrite=True, papszDSCO=dsco, papszLCO=lco)
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

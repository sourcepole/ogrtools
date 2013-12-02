import ogr
import json
from format_handler import *

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


class Spec:

    def __init__(self, ds, model=None):
        self.ds_fn = ds
        self.ds = None
        self.model = model
        self.src_format_handler = IliFormatHandler()
        self.dst_format_handler = PgFormatHandler()

    def open(self):
        self.ds = ogr.Open(self.ds_fn, update=False)
        return self.ds

    def close(self):
        if self.ds is not None:
            self.ds.Destroy()

    def enums(self):
        enum_tables = {}
        if self.model:
            enums = self.src_format_handler.extract_enums(self.model)
            for src_name, values in enums.items():
                dst_name = self.src_format_handler.shorten_name(src_name, 'enum')
                enum_tables[dst_name] = {
                    'src_name': src_name,
                    'values': values
                }
        return enum_tables

    def generate_spec(self, outfile=None, layer_list=[]):
        if self.ds is None:
            self.open()

        if len(layer_list) == 0:
            for layer in self.ds:
                layer_list.append(layer.GetLayerDefn().GetName())

        spec = {}
        #Javscript comments are not allowed JSON
        spec['comment'] = '// OGR transformation specification'
        layers = {}
        spec['layers'] = layers

        for name in layer_list:
            layer = self.ds.GetLayerByName(name)
            layerdef = layer.GetLayerDefn()

            speclayer = {}
            dst_name = self.dst_format_handler.launder_name(name)
            layers[dst_name] = speclayer
            speclayer['src_layer'] = name
            fields = {}
            speclayer['fields'] = fields

            for fld_index in range(layerdef.GetFieldCount()):
                src_fd = layerdef.GetFieldDefn(fld_index)

                specfield = {}
                field_name = src_fd.GetName()
                dst_name = self.dst_format_handler.launder_name(field_name)
                fields[dst_name] = specfield
                specfield['src'] = field_name
                jsontype = FIELD_TYPES[src_fd.GetType()]
                specfield['type'] = jsontype
                if src_fd.GetWidth() > 0:
                    specfield['width'] = src_fd.GetWidth()
                if src_fd.GetPrecision() > 0:
                    specfield['precision'] = src_fd.GetPrecision()

            geom_type = GEOMETRY_TYPES[layerdef.GetGeomType()]
            speclayer['geometry_type'] = geom_type

        enum_tables = self.enums()
        if enum_tables:
            spec['enums'] = enum_tables

        specstr = json.dumps(spec, indent=2)

        if outfile is not None:
            f = open(outfile, "w")
            f.write(specstr)
            f.close()

        return specstr

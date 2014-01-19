import tempfile
from ..pyogr.ogr2ogr import ogr2ogr
from ..ogrtransform.spec import Spec
from ..interlis.ilismeta import prettify
try:
    from osgeo import ogr
    from osgeo import gdal
except ImportError:
    import ogr
    import gdal


class Transformation:

    def __init__(self, spec, ds=None):
        self._trans = Spec(ds=ds, spec=spec)

    def transform(self, dest, format=None, debug=False):
        vrt = self._trans.generate_vrt()
        if debug:
            print prettify(vrt)
        ds = self.tmp_datasource(vrt)
        dst_format = format or self._trans.dst_format()
        dsco = []
        if dst_format == self._trans.dst_format():
            dsco = self._trans.ds_creation_options()
        lco = []
        if dst_format == self._trans.dst_format():
            lco = self._trans.layer_creation_options()
        ogr2ogr(pszFormat=str(dst_format), pszDataSource=ds, pszDestDataSource=dest,
                bOverwrite=True, papszDSCO=dsco, papszLCO=lco)  # poOutputSRS=srs, poSourceSRS=srs
        self.free_tmp_datasource()

    def transform_reverse(self, dest, format=None, debug=False):
        vrt = self._trans.generate_reverse_vrt()
        if debug:
            print prettify(vrt)
        ds = self.tmp_datasource(vrt)
        dst_format = format or self._trans.src_format()
        ogr2ogr(pszFormat=str(dst_format), pszDataSource=ds,
                pszDestDataSource=dest, bOverwrite=True)
        self.free_tmp_datasource()

    def write_enum_tables(self, dest, format=None, debug=False):
        gml = self._trans.generate_enum_gml()
        if debug:
            print prettify(gml)
        ds = self.tmp_datasource(gml)
        dst_format = format or self._trans.dst_format()
        dsco = []
        if dst_format == self._trans.dst_format():
            dsco = self._trans.ds_creation_options()
        lco = []
        if dst_format == self._trans.dst_format():
            lco = self._trans.layer_creation_options()
        ogr2ogr(pszFormat=str(dst_format), pszDataSource=ds,
                pszDestDataSource=dest, bOverwrite=True, papszDSCO=dsco, papszLCO=lco)
        self.free_tmp_datasource()

    def tmp_memfile(self, data):
        self._tmp_memfile = tempfile.mktemp('.vrt', 'ogr_', '/vsimem')
        # Create in-memory file
        gdal.FileFromMemBuffer(self._tmp_memfile, data)
        return self._tmp_memfile

    def free_tmp_datasource(self):
        # Free memory associated with the in-memory file
        gdal.Unlink(self._tmp_memfile)

    def tmp_datasource(self, data):
        #Call free_tmp_datasource after closing datasource to free memeroy
        vrt = self.tmp_memfile(data)
        ds = ogr.Open(vrt)
        return ds

import tempfile
from pyogr.ogr2ogr import ogr2ogr
from ogrtransform.spec import Spec
from interlis.ilismeta import prettify
try:
    from osgeo import ogr
    from osgeo import gdal
except ImportError:
    import ogr
    import gdal


class Transformation:

    def __init__(self, ds, spec):
        self._trans = Spec(ds, spec)

    def transform(self, args):
        vrt = self._trans.generate_vrt()
        if args.debug:
            print prettify(vrt)
        ds = self.vrt_datasource(vrt)
        dst_format = args.format or self._trans.dst_format()
        ogr2ogr(pszFormat=str(dst_format), pszDataSource=ds, pszDestDataSource=args.dest,
                bOverwrite=True)  # ,papszDSCO=["SPATIALITE=YES"],poOutputSRS=srs, poSourceSRS=srs
        self.free_vrt_datasource()

    def transform_reverse(self, args):
        vrt = self._trans.generate_reverse_vrt()
        if args.debug:
            print prettify(vrt)
        ds = self.vrt_datasource(vrt)
        dst_format = args.format or self._trans.src_format()
        ogr2ogr(pszFormat=str(dst_format), pszDataSource=ds,
                pszDestDataSource=args.dest, bOverwrite=True)
        self.free_vrt_datasource()

    def vrt_memfile(self, vrt_xml):
        self.vrt_memfile = tempfile.mktemp('.vrt', 'ogr_', '/vsimem')
        # Create in-memory file
        gdal.FileFromMemBuffer(self.vrt_memfile, vrt_xml)
        return self.vrt_memfile

    def free_vrt_datasource(self):
        # Free memory associated with the in-memory file
        gdal.Unlink(self.vrt_memfile)

    def vrt_datasource(self, vrt_xml):
        #Call free_vrt_datasource after closing datasource to free memeroy
        vrt = self.vrt_memfile(vrt_xml)
        ds = ogr.Open(vrt)
        return ds

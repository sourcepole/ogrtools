from ogrtools.pyogr.ogrinfo import ogrinfo, ogr_formats, ogr_version_info


def test_ogrinfo():
    expected = """INFO: Open of `tests/data/osm/railway.shp'
      using driver `ESRI Shapefile' successful.

Layer name: railway
Geometry: Line String
Feature Count: 73
Extent: (9.478497, 9.628118) - (47.124600, 47.262550)
Layer SRS WKT:
GEOGCS["GCS_WGS_1984",
    DATUM["WGS_1984",
        SPHEROID["WGS_84",6378137,298.257223563]],
    PRIMEM["Greenwich",0],
    UNIT["Degree",0.017453292519943295]]
type: String (255.0)
osm_id: Real (11.0)
lastchange: Date (10.0)
name: String (255.0)
keyvalue: String (80.0)
"""
    info = ogrinfo(readonly=True, summaryonly=True, all_layers=True,
                   datasource_name="tests/data/osm/railway.shp")
    assert info == 0  # should eventually be info == expected (ogrinfo prints on stdout)

import os
import tempfile
import codecs
from ogrtools.ogrtransform.transformation import Transformation


def test_shape_to_geojson():
    #ogr genconfig --format PostgreSQL tests/data/osm/railway.shp >tests/data/osm/railway.cfg
    trans = Transformation("tests/data/osm/railway.cfg", "tests/data/osm/railway.shp")
    __, dstfile = tempfile.mkstemp()
    os.remove(dstfile)
    trans.transform(dstfile, "GeoJSON")
    result = codecs.open(dstfile, encoding='utf-8').read()
    os.remove(dstfile)
    #Default import
    assert '{ "type": "rail"' not in result
    #Mapping from config
    assert '{ "osm_type": "rail"' in result
    geojsonstart = """{
"type": "FeatureCollection",
                                                                                
"features": [
{ "type": "Feature", "properties": {"""
    assert geojsonstart in result
    expected = """osm_id": 35324774.000000 }, "geometry": { "type": "LineString", "coordinates": [ [ 9.542907, 47.20156 ], [ 9.542616, 47.201195 ]"""
    assert expected in result

def test_ili_to_geojson():
    #ogr genconfig --format PostgreSQL tests/data/ili/roads23.xtf,tests/data/ili/RoadsExdm2ien.imd --model tests/data/ili/RoadsExdm2ien.imd >tests/data/ili/RoadsExdm2ien.cfg
    trans = Transformation("tests/data/ili/RoadsExdm2ien.cfg",
      "tests/data/ili/roads23.xtf,tests/data/ili/RoadsExdm2ien.imd")
    __, dstfile = tempfile.mkstemp()
    os.remove(dstfile)
    trans.transform(dstfile, "GeoJSON", layers=["streetaxis"])
    result = codecs.open(dstfile, encoding='utf-8').read()
    os.remove(dstfile)
    expected = """{ "type": "Feature", "properties": { "tid": "8", "precision": "precise", "street_id": 1 }, "geometry": { "type": "LineString", "coordinates": [ [ 55.6, 37.649 ], [ 15.573, 25.785 ] ] } }"""
    assert expected in result

def test_geojson_reverse_to_ili():
    #ogr transform --format GeoJSON --config tests/data/ili/RoadsExdm2ien.cfg tests/data/ili/RoadsExdm2ien_streetaxis.json tests/data/ili/roads23.xtf,tests/data/ili/RoadsExdm2ien.imd streetaxis
    trans = Transformation("tests/data/ili/RoadsExdm2ien.cfg",
      "tests/data/ili/RoadsExdm2ien_streetaxis.json")
    __, dstfile = tempfile.mkstemp()
    #os.remove(dstfile)
    trans.transform_reverse(dstfile+",tests/data/ili/RoadsExdm2ien.imd",
      layers=["RoadsExdm2ien.RoadsExtended.StreetAxis"])
    result = codecs.open(dstfile, encoding='utf-8').read()
    os.remove(dstfile)
    expected = """<DATASECTION>
<RoadsExdm2ien.RoadsExtended BID="RoadsExdm2ien.RoadsExtended">
<RoadsExdm2ien.RoadsExtended.StreetAxis TID="8">
<Geometry>
<POLYLINE>
<COORD><C1>55.6></C1><C2>37.649></C2></COORD>
<COORD><C1>15.573></C1><C2>25.785></C2></COORD>
</POLYLINE>
</Geometry>
<Street>1</Street>
<Precision>precise</Precision>
</RoadsExdm2ien.RoadsExtended.StreetAxis>"""
    print result
    assert expected in result

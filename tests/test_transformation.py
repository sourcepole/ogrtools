# -*- coding: utf-8 -*-

import os
import tempfile
import re
import codecs
from ogrtools.ogrtransform.ogrconfig import OgrConfig


def test_shape_to_geojson():
    #ogr genconfig --format PostgreSQL tests/data/osm/railway.shp >tests/data/osm/railway.cfg
    trans = OgrConfig(config="tests/data/osm/railway.cfg", ds="tests/data/osm/railway.shp")
    __, dstfile = tempfile.mkstemp(suffix='.json')
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
    trans = OgrConfig(config="tests/data/ili/RoadsExdm2ien.cfg",
                      ds="tests/data/ili/roads23.xtf,tests/data/ili/RoadsExdm2ien.imd")
    __, dstfile = tempfile.mkstemp(suffix='.json')
    os.remove(dstfile)
    trans.transform(dstfile, "GeoJSON", layers=["streetaxis"])
    result = codecs.open(dstfile, encoding='utf-8').read()
    os.remove(dstfile)
    expected = """{ "type": "Feature", "properties": { "tid": "8", "precision": "precise", "street_id": 1 }, "geometry": { "type": "LineString", "coordinates": [ [ 55.6, 37.649 ], [ 15.573, 25.785 ] ] } }"""
    print result
    assert expected in result


def test_geojson_reverse_to_ili():
    #ogr transform --format GeoJSON --config tests/data/ili/RoadsExdm2ien.cfg tests/data/ili/RoadsExdm2ien_streetaxis.json tests/data/ili/roads23.xtf,tests/data/ili/RoadsExdm2ien.imd streetaxis
    trans = OgrConfig(config="tests/data/ili/RoadsExdm2ien.cfg",
                      ds="tests/data/ili/RoadsExdm2ien_streetaxis.json")
    __, dstfile = tempfile.mkstemp(suffix='.xtf')
    #os.remove(dstfile)
    trans.transform_reverse(dstfile + ",tests/data/ili/RoadsExdm2ien.imd",
                            layers=["RoadsExdm2ien.RoadsExtended.StreetAxis"])
    result = codecs.open(dstfile, encoding='utf-8').read()
    os.remove(dstfile)
    expected = """<DATASECTION>
<RoadsExdm2ien.RoadsExtended BID="RoadsExdm2ien.RoadsExtended">
<RoadsExdm2ien.RoadsExtended.StreetAxis TID="8">
<Geometry>
<POLYLINE>
<COORD><C1>55.6</C1><C2>37.649</C2></COORD>
<COORD><C1>15.573</C1><C2>25.785</C2></COORD>
</POLYLINE>
</Geometry>
<Street>1</Street>
<Precision>precise</Precision>
</RoadsExdm2ien.RoadsExtended.StreetAxis>"""
    assert expected in result


def manualtest_ili_to_spatialite():
    #ogr genconfig --format SQLite tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.xtf,tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.imd --model tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.imd >tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.cfg
    trans = OgrConfig(config="tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.cfg",
      ds="tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.xtf,tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.imd")
    __, dstfile = tempfile.mkstemp(suffix='.sqlite')
    os.remove(dstfile)
    trans.transform(dstfile, "SQLite")
    print dstfile
    result = os.popen("echo .dump | sqlite3 %s" % dstfile).read()
    #print result
    assert False
    os.remove(dstfile)


def manualtest_ili_with_struct_to_gml():
    #ogr genconfig --format GML tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.xtf,tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.imd --model tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.imd >tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118-gml.cfg
    trans = OgrConfig(config="tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.cfg",
                      ds="tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.xtf,tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.imd")
    __, dstfile = tempfile.mkstemp(suffix='.gml')
    os.remove(dstfile)
    trans.transform(dstfile, "GML")
    print dstfile
    assert False
    os.remove(dstfile)


def test_encoding():
    #ogr genconfig --format GML tests/data/np/NP_Example.xtf,tests/data/np/NP_73_CH_de_ili2.imd --model tests/data/np/NP_73_CH_de_ili2.imd >tests/data/np/NP_73_CH_de_ili2.cfg
    trans = OgrConfig(config="tests/data/np/NP_73_CH_de_ili2.cfg",
                      ds="tests/data/np/NP_Example.xtf,tests/data/np/NP_73_CH_de_ili2.imd")
    __, dstfile = tempfile.mkstemp(suffix='.gml')
    os.remove(dstfile)
    trans.transform(dstfile, "GML")
    print dstfile
    gml = codecs.open(dstfile, encoding='utf-8').read()
    assert u"Bundesgesetz über die Raumplanung" in gml
    os.remove(dstfile)

    trans = OgrConfig(config="tests/data/np/NP_73_CH_de_ili2.cfg",
                      ds="tests/data/np/NP_Example_latin1.xtf,tests/data/np/NP_73_CH_de_ili2.imd")
    #NP_Example_latin1.xtf has latin1 header and contains entities like &#xfc; as ü
    __, dstfile = tempfile.mkstemp(suffix='.gml')
    os.remove(dstfile)
    trans.transform(dstfile, "GML")
    print dstfile
    gml = codecs.open(dstfile, encoding='utf-8').read()
    assert u"Bundesgesetz über die Raumplanung" not in gml
    os.remove(dstfile)


def test_ili_to_gml():
    #ogr genconfig --format GML tests/data/np/NP_Example.xtf,tests/data/np/NP_73_CH_de_ili2.imd --model tests/data/np/NP_73_CH_de_ili2.imd >tests/data/np/NP_73_CH_de_ili2.cfg
    trans = OgrConfig(config="tests/data/np/NP_73_CH_de_ili2.cfg",
                      ds="tests/data/np/NP_Example.xtf,tests/data/np/NP_73_CH_de_ili2.imd")
    __, dstfile = tempfile.mkstemp(suffix='.gml')
    os.remove(dstfile)
    trans.transform(dstfile, "GML")
    print dstfile
    gml = codecs.open(dstfile, encoding='utf-8').read()

    #GML -> XTF
    __, xtffile = tempfile.mkstemp(suffix='.xtf')
    trans.transform_reverse(xtffile + ",tests/data/np/NP_73_CH_de_ili2.imd")
    print xtffile
    xtf = codecs.open(xtffile, encoding='utf-8').read()
    zonentyp_kt = """<Nutzungsplanung.Nutzungsplanung.Grundnutzung_Zonentyp_Kt TID="xz4e43cb280000000a">
<Identifikator>142</Identifikator>
<Zonentyp_Kt>Kernzone</Zonentyp_Kt>
<Abkuerzung>K</Abkuerzung>
<Bemerkungen>Kernzone</Bemerkungen>
<Hauptnutzung_CH>Bauzonen_1.Zentrumszonen_14</Hauptnutzung_CH>
<Zonentyp_SIA>Zentrumszonen_14.Kernzone_142</Zonentyp_SIA>
</Nutzungsplanung.Nutzungsplanung.Grundnutzung_Zonentyp_Kt>"""
    assert zonentyp_kt in xtf
    assert "<COORD><C1>694511.547</C1><C2>247816.271</C2></COORD>" in xtf
    geometry_type = """<Geometrie>
<SURFACE>
<BOUNDARY>
<POLYLINE>
<COORD>"""
    assert geometry_type in xtf

    # XTF -> GML
    trans2 = OgrConfig(config="tests/data/np/NP_73_CH_de_ili2.cfg",
                       ds=xtffile + ",tests/data/np/NP_73_CH_de_ili2.imd")
    __, gmlfile2 = tempfile.mkstemp(suffix='.gml')
    trans.transform(gmlfile2, "GML")
    print gmlfile2
    gml2 = codecs.open(gmlfile2, encoding='utf-8').read()

    gml = re.sub(r'tmp.+.xsd', 'tmpXXX.xsd', gml, count=1)
    gml2 = re.sub(r'tmp.+.xsd', 'tmpXXX.xsd', gml2, count=1)
    assert gml == gml2

    # cleanup
    os.remove(dstfile)
    os.remove(xtffile)
    os.remove(gmlfile2)

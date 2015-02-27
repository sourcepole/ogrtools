# -*- coding: utf-8 -*-

import os
import tempfile
import re
import codecs
from ogrtools.ogrtransform.ogrconfig import OgrConfig


def test_shape_to_geojson():
    #ogr genconfig --format PostgreSQL tests/data/osm/railway.shp >tests/data/osm/railway.cfg
    trans = OgrConfig(
        config="tests/data/osm/railway.cfg",
        ds="tests/data/osm/railway.shp")
    __, dstfile = tempfile.mkstemp(suffix='.json')
    os.remove(dstfile)
    trans.transform(dstfile, "GeoJSON")
    print dstfile
    result = codecs.open(dstfile, encoding='utf-8').read()
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
    os.remove(dstfile)


def test_ili_to_geojson():
    #ogr genconfig --format PostgreSQL tests/data/ili/roads23.xtf,tests/data/ili/RoadsExdm2ien.imd --model tests/data/ili/RoadsExdm2ien.imd --srs=EPSG:21781 >tests/data/ili/RoadsExdm2ien.cfg
    trans = OgrConfig(
        config="tests/data/ili/RoadsExdm2ien.cfg",
        ds="tests/data/ili/roads23.xtf,tests/data/ili/RoadsExdm2ien.imd")
    __, dstfile = tempfile.mkstemp(suffix='.json')
    os.remove(dstfile)
    trans.transform(dstfile, "GeoJSON", layers=["streetaxis"])
    print dstfile
    result = codecs.open(dstfile, encoding='utf-8').read()
    expected = """{ "type": "Feature", "properties": { "tid": "8", "precision": "precise", "street_id": 1 }, "geometry": { "type": "LineString", "coordinates": [ [ 55.6, 37.649 ], [ 15.573, 25.785 ] ] } }"""
    assert expected in result
    os.remove(dstfile)


def test_geojson_reverse_to_ili():
    #ogr transform --format GeoJSON --config tests/data/ili/RoadsExdm2ien.cfg tests/data/ili/RoadsExdm2ien_streetaxis.json tests/data/ili/roads23.xtf,tests/data/ili/RoadsExdm2ien.imd streetaxis
    trans = OgrConfig(config="tests/data/ili/RoadsExdm2ien.cfg",
                      ds="tests/data/ili/RoadsExdm2ien_streetaxis.json")
    __, dstfile = tempfile.mkstemp(suffix='.xtf')
    #os.remove(dstfile)
    trans.transform_reverse(dstfile + ",tests/data/ili/RoadsExdm2ien.imd",
                            layers=["RoadsExdm2ien.RoadsExtended.StreetAxis"])
    print dstfile
    result = codecs.open(dstfile, encoding='utf-8').read()
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
    os.remove(dstfile)


def manualtest_ili_to_spatialite():
    #ogr genconfig --format SQLite tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.xtf,tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.imd --model tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.imd --srs=EPSG:21781 >tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.cfg
    trans = OgrConfig(
        config="tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.cfg",
        ds="tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.xtf,tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.imd")
    __, dstfile = tempfile.mkstemp(suffix='.sqlite')
    os.remove(dstfile)
    # Takes more than 2'
    trans.transform(dstfile, "SQLite")
    print dstfile
    result = os.popen("echo .dump | sqlite3 %s" % dstfile).read()
    assert False
    os.remove(dstfile)


def test_ili_to_postgis():
    # ogr genconfig --format PostgreSQL tests/data/np/NP_Example.xtf,tests/data/np/NP_73_CH_de_ili2.imd --model tests/data/np/NP_73_CH_de_ili2.imd --srs=EPSG:21781 >tests/data/np/NP_73_CH_de_ili2-pg.cfg
    trans = OgrConfig(
        config="tests/data/np/NP_73_CH_de_ili2-pg.cfg",
        ds="tests/data/np/NP_Example.xtf,tests/data/np/NP_73_CH_de_ili2.imd")
    __, dstfile = tempfile.mkstemp(suffix='.sql')
    trans.transform(dstfile, "PGDump")
    print dstfile
    sql = codecs.open(dstfile, encoding='utf-8').read()
    assert """CREATE TABLE "public"."n0_grundnutzung_zonenflaeche" (""" in sql
    assert """SELECT AddGeometryColumn('public','n0_grundnutzung_zonenflaeche','geometrie',21781,'POLYGON',2);""" in sql
    assert """INSERT INTO "public"."n0_grundnutzung_zonenflaeche" ("geometrie" , "zonentyp_1", "herkunft", "mutation", "tid", "qualitaet") VALUES ('01030000201555000001000000550000007D3F355ECA312541FA7E6ABCDD2E0E41355EBAC9923125411904560EC72D0E41EE7C3FB5923125412DB29DEF9D2C0E4154E3A55B80312541713D0AD7472C0E41A4703DCA7731254183C0CAA11F2C0E414C37898171312541F4FDD478F92B0E414260E5506E3125413D0AD7A3022C0E413F355EFA68312541BC749318122C0E4121B072A8633125416DE7FBA9212C0E4154E3A55B5E31254193180456312C0E41D9CEF7135931254177BE9F1A412C0E414260E5D053312541D122DBF9502C0E418D976E924E3125415C8FC2F5602C0E41448B6CE74A3125411D5A643B6C2C0E419A99995949312541E9263108712C0E418941602544312541A8C64B37812C0E41CBA145F63E31254123DBF97E912C0E415EBA49CC393125415A643BDFA12C0E41448B6CA73431254108AC1C5AB22C0E417B14AE872F3125412DB29DEFC22C0E4104560E6D2A3125410E2DB29DD32C0E41DF4F8D5725312541AC1C5A64E42C0E415839B4C8073125411904560E472D0E41D122DBF9F030254117D9CEF7952D0E410AD7A3B0D83025411F85EB51EE2D0E41E5D0221BAC302541022B87169C2E0E41273108ECA7302541BE9F1A2FAD2E0E41AE47E1FAA6302541D34D6210B12E0E41E9263188A23025417F6ABC74C32E0E41C3F5281C9E3025412DB29DEFD52E0E415C8FC2B599302541DD240681E82E0E41AE47E1FA97302541E5D022DBEF2E0E41B6F3FD54953025414A0C022BFB2E0E413F355EFA90302541FED478E90D2F0E41F853E3A58C302541B4C876BE202F0E41DF4F8D57883025416DE7FBA9332F0E41F853E3E574302541560E2DB2912F0E416F1283C08930254125068195DD2F0E41F4FDD4F8963025411283C0CA0C300E411F85EB519E3025416210583928300E41CDCCCCCCB83025417F6ABC7488300E41333333B3DC302541759318040F310E41B4C8763EE6302541D122DBF9F5300E411283C0CA2A312541EC51B81E42300E41C520B0B230312541C976BE9F32300E413D0AD7633A312541D122DBF988300E41378941E0BD3125414260E5D092320E4114AE4721C2312541931804567C320E41D34D6210E5312541CBA145B6C3310E419EEFA786E6312541BC749318BC310E41986E1203E8312541F6285C8FB4310E41C1CAA185E931254177BE9F1AAD310E418716D90EEB3125413F355EBAA5310E41EC51B89EEC3125410AD7A3709E310E4110583934EE3125411D5A643B97310E41643BDFCFEF31254177BE9F1A90310E41E7FBA971F13125418D976E1289310E419A999919F3312541EC51B81E82310E410C022BC7F4312541068195437B310E41AE47E17AF63125416891ED7C74310E4110583934F83125414260E5D06D310E41C520B0F2F93125416210583967310E41A8C64BB7FB312541FA7E6ABC60310E414C378981FD312541931804565A310E41986E1283FD312541643BDF4F5A310E414260E550FF312541E926310854310E418941602501322541B6F3FDD44D310E4191ED7CFF0232254185EB51B847310E41EC51B8DE0432254185EB51B841310E41986E12C3063225418716D9CE3B310E41273108AC08322541BA490C0236310E4108AC1C9A0A322541AAF1D24D30310E413BDF4F8D0C322541105839B42A310E4152B81E850E322541EE7C3F3525310E414C378981103225414260E5D01F310E41BA490C8212322541C74B37891A310E417B14AE8714322541C3F5285C15310E41B072689116322541F0A7C64B10310E415A643B9F18322541931804560B310E41E7FBA9B11A3225416891ED7C06310E415C8FC2B51A322541C520B07206310E417B14AEC72F322541A8C64B37DA300E41759318C43832254196438B6CCB300E41F0A7C60B2D3225417593180497300E417D3F355ECA312541FA7E6ABCDD2E0E41', 'xz4e43cb2800000014', 'Aufnahme', 'xz4e43d386e7880000', 'xz4e43d63ce7880007', 'AV93');""" in sql
    os.remove(dstfile)


def manualtest_ili_with_struct_to_gml():
    #ogr genconfig --format GML tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.xtf,tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.imd --model tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.imd --srs=EPSG:21781 >tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118-gml.cfg
    trans = OgrConfig(
        config="tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.cfg",
        ds="tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.xtf,tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.imd")
    __, dstfile = tempfile.mkstemp(suffix='.gml')
    os.remove(dstfile)
    trans.transform(dstfile, "GML")
    print dstfile
    assert False
    os.remove(dstfile)


def test_encoding():
    #ogr genconfig --format GML tests/data/np/NP_Example.xtf,tests/data/np/NP_73_CH_de_ili2.imd --model tests/data/np/NP_73_CH_de_ili2.imd --srs=EPSG:21781 >tests/data/np/NP_73_CH_de_ili2.cfg
    trans = OgrConfig(
        config="tests/data/np/NP_73_CH_de_ili2.cfg",
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
    trans = OgrConfig(
        config="tests/data/np/NP_73_CH_de_ili2.cfg",
        ds="tests/data/np/NP_Example.xtf,tests/data/np/NP_73_CH_de_ili2.imd")
    __, dstfile = tempfile.mkstemp(suffix='.gml')
    os.remove(dstfile)
    trans.transform(dstfile, "GML")
    print dstfile
    gml = codecs.open(dstfile, encoding='utf-8').read()

    # GML -> XTF
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

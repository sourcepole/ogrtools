from ogrtools.ogrtransform.ogrconfig import OgrConfig


def test_shape_config():
    cfg = OgrConfig(ds="tests/data/osm/railway.shp")
    cfgjson = cfg.generate_config(dst_format='PostgreSQL')
    expected = """{
  "//": "OGR transformation configuration", 
  "dst_dsco": {}, 
  "dst_lco": {
    "SCHEMA": "public"
  }, 
  "layers": {
    "railway": {
      "fields": {
        "keyvalue": {
          "src": "keyvalue", 
          "type": "String", 
          "width": 80
        }, 
        "lastchange": {
          "src": "lastchange", 
          "type": "Date", 
          "width": 10
        }, 
        "type": {
          "src": "type", 
          "type": "String", 
          "width": 255
        }, 
        "name": {
          "src": "name", 
          "type": "String", 
          "width": 255
        }, 
        "osm_id": {
          "src": "osm_id", 
          "type": "Real", 
          "width": 11
        }
      }, 
      "geometry_type": "LineString", 
      "src_layer": "railway", 
      "geom_fields": {}
    }
  }, 
  "src_format": "ESRI Shapefile", 
  "dst_format": "PostgreSQL"
}"""
    print cfgjson
    assert cfgjson == expected


def test_ili_config():
    cfg = OgrConfig(ds="./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd")
    cfgjson = cfg.generate_config(dst_format='PostgreSQL')
    expected = """"roadsexdm2ien_roadsextended_streetaxis": {
      "fields": {
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "street": {
          "src": "Street", 
          "type": "String"
        }, 
        "precision": {
          "src": "Precision", 
          "type": "String"
        }
      }, 
      "geometry_type": "MultiLineString", 
      "src_layer": "RoadsExdm2ien.RoadsExtended.StreetAxis", 
      "geom_fields": {
        "geometry": {
          "src": "Geometry", 
          "type": "MultiLineString"
        }
      }
    }"""
    print cfgjson
    assert expected in cfgjson


def test_np():
    cfg = OgrConfig(ds="tests/data/np/NP_Example.xtf,tests/data/np/NP_73_CH_de_ili2.imd", model="tests/data/np/NP_73_CH_de_ili2.imd")
    cfgjson = cfg.generate_config(dst_format='PostgreSQL')
    expected = """"n0_grundnutzung_zonenflaeche": {
      "fields": {
        "zonentyp_1": {
          "src": "Zonentyp_1", 
          "type": "String"
        }, 
        "herkunft": {
          "src": "Herkunft", 
          "type": "String"
        }, 
        "mutation": {
          "src": "Mutation", 
          "type": "String"
        }, 
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "qualitaet": {
          "src": "Qualitaet", 
          "type": "String"
        }, 
        "bemerkungen": {
          "src": "Bemerkungen", 
          "type": "String"
        }
      }, 
      "geometry_type": "Polygon", 
      "src_layer": "Nutzungsplanung.Nutzungsplanung.Grundnutzung_Zonenflaeche", 
      "geom_fields": {
        "geometrie": {
          "src": "Geometrie", 
          "type": "Polygon"
        }
      }
    }"""
    print cfgjson
    assert expected in cfgjson


def test_layer_info():
    cfg = OgrConfig(ds="./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd",
                    model="./tests/data/ili/RoadsExdm2ien.imd")
    assert not cfg.is_loaded()
    assert cfg.layer_names() == []
    assert cfg.enum_names() == []
    assert cfg.layer_infos() == []
    assert cfg.enum_infos() == []

    cfg.generate_config(dst_format='PostgreSQL')
    assert cfg.is_loaded()
    print cfg.layer_names()
    assert "roadsexdm2ien_roadsextended_roadsign" in cfg.layer_names()
    print cfg.enum_names()
    assert "_type" in str(cfg.enum_names())

    print cfg.layer_infos()
    #assert {'name': 'roadsexdm2ien_roadsextended_roadsign', 'geom_field': 'position'} in cfg.layer_infos()
    assert {'name': 'roadsexdm2ien_roadsextended_roadsign', 'geom_field': 'wkb_geometry'} in cfg.layer_infos()
    assert {'name': 'roadsexdm2ben_roads_lattrs'} in cfg.layer_infos()
    print cfg.enum_infos()
    assert '_precision' in str(cfg.enum_infos())


def test_enums():
    cfg = OgrConfig(ds="./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd",
                    model="./tests/data/ili/RoadsExdm2ien.imd")
    cfgjson = cfg.generate_config(dst_format='PostgreSQL')
    expected = """_lart": {
      "src_name": "RoadsExdm2ben.Roads.LAttrs.LArt", 
      "values": [
        {
          "enumtxt": "welldefined", 
          "enum": "welldefined", 
          "id": 0
        }, 
        {
          "enumtxt": "fuzzy", 
          "enum": "fuzzy", 
          "id": 1
        }
      ]
    }"""
    print cfgjson
    assert expected in cfgjson


def test_vrt():
    cfg = OgrConfig(config="./tests/data/ili/RoadsExdm2ien.cfg")
    vrt = cfg.generate_vrt()
    expected = """<OGRVRTDataSource><OGRVRTLayer name="lattrs"><SrcDataSource relativeToVRT="0" shared="1" /><SrcLayer>RoadsExdm2ben.Roads.LAttrs</SrcLayer><GeometryType>wkbNone</GeometryType><Field name="lart" src="LArt" type="String" /><Field name="ref_name" src="REF_NAME" type="String" /><Field name="ref_id" src="REF_ID" type="String" /></OGRVRTLayer><OGRVRTLayer name="roadsign"><SrcDataSource relativeToVRT="0" shared="1" /><SrcLayer>RoadsExdm2ien.RoadsExtended.RoadSign</SrcLayer><GeometryType>wkbPoint</GeometryType><Field name="tid" src="TID" type="String" /><Field name="type" src="Type" type="String" /></OGRVRTLayer><OGRVRTLayer name="street"><SrcDataSource relativeToVRT="0" shared="1" /><SrcLayer>RoadsExdm2ben.Roads.Street</SrcLayer><GeometryType>wkbNone</GeometryType><Field name="tid" src="TID" type="String" /><Field name="name" src="Name" type="String" /></OGRVRTLayer><OGRVRTLayer name="streetaxis"><SrcDataSource relativeToVRT="0" shared="1" /><SrcLayer>RoadsExdm2ien.RoadsExtended.StreetAxis</SrcLayer><GeometryType>wkbMultiLineString</GeometryType><Field name="tid" src="TID" type="String" /><Field name="precision" src="Precision" type="String" /><Field name="street_id" src="Street" type="Integer" /></OGRVRTLayer><OGRVRTLayer name="streetnameposition"><SrcDataSource relativeToVRT="0" shared="1" /><SrcLayer>RoadsExdm2ben.Roads.StreetNamePosition</SrcLayer><GeometryType>wkbPoint</GeometryType><Field name="tid" src="TID" type="String" /><Field name="street" src="Street" type="String" /><Field name="namori" src="NamOri" type="Real" /></OGRVRTLayer><OGRVRTLayer name="landcover"><SrcDataSource relativeToVRT="0" shared="1" /><SrcLayer>RoadsExdm2ben.Roads.LandCover</SrcLayer><GeometryType>wkbPolygon</GeometryType><Field name="tid" src="TID" type="String" /><Field name="type" src="Type" type="String" /></OGRVRTLayer></OGRVRTDataSource>"""
    print vrt
    assert expected in vrt


def test_reverse_vrt():
    cfg = OgrConfig(ds="./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd",
                    config="./tests/data/ili/RoadsExdm2ien.cfg")
    vrt = cfg.generate_reverse_vrt()
    expected = """<OGRVRTDataSource><OGRVRTLayer name="RoadsExdm2ben.Roads.LAttrs"><SrcDataSource relativeToVRT="0" shared="1">./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd</SrcDataSource><SrcLayer>lattrs</SrcLayer><GeometryType>wkbNone</GeometryType><Field name="LArt" src="lart" /><Field name="REF_NAME" src="ref_name" /><Field name="REF_ID" src="ref_id" /></OGRVRTLayer><OGRVRTLayer name="RoadsExdm2ien.RoadsExtended.RoadSign"><SrcDataSource relativeToVRT="0" shared="1">./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd</SrcDataSource><SrcLayer>roadsign</SrcLayer><GeometryType>wkbPoint</GeometryType><Field name="TID" src="tid" /><Field name="Type" src="type" /></OGRVRTLayer><OGRVRTLayer name="RoadsExdm2ben.Roads.Street"><SrcDataSource relativeToVRT="0" shared="1">./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd</SrcDataSource><SrcLayer>street</SrcLayer><GeometryType>wkbNone</GeometryType><Field name="TID" src="tid" /><Field name="Name" src="name" /></OGRVRTLayer><OGRVRTLayer name="RoadsExdm2ien.RoadsExtended.StreetAxis"><SrcDataSource relativeToVRT="0" shared="1">./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd</SrcDataSource><SrcLayer>streetaxis</SrcLayer><GeometryType>wkbMultiLineString</GeometryType><Field name="TID" src="tid" /><Field name="Precision" src="precision" /><Field name="Street" src="street_id" /></OGRVRTLayer><OGRVRTLayer name="RoadsExdm2ben.Roads.StreetNamePosition"><SrcDataSource relativeToVRT="0" shared="1">./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd</SrcDataSource><SrcLayer>streetnameposition</SrcLayer><GeometryType>wkbPoint</GeometryType><Field name="TID" src="tid" /><Field name="Street" src="street" /><Field name="NamOri" src="namori" /></OGRVRTLayer><OGRVRTLayer name="RoadsExdm2ben.Roads.LandCover"><SrcDataSource relativeToVRT="0" shared="1">./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd</SrcDataSource><SrcLayer>landcover</SrcLayer><GeometryType>wkbPolygon</GeometryType><Field name="TID" src="tid" /><Field name="Type" src="type" /></OGRVRTLayer></OGRVRTDataSource>"""
    print vrt
    assert expected in vrt

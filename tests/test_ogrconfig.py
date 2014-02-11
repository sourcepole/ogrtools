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
      "src_layer": "railway"
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
    expected = """{
  "//": "OGR transformation configuration", 
  "dst_dsco": {}, 
  "dst_lco": {
    "SCHEMA": "public"
  }, 
  "layers": {
    "roadsexdm2ien_roadsextended_roadsign": {
      "fields": {
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "type": {
          "src": "Type", 
          "type": "String"
        }
      }, 
      "geometry_type": "Point", 
      "src_layer": "RoadsExdm2ien.RoadsExtended.RoadSign"
    }, 
    "roadsexdm2ben_roads_landcover": {
      "fields": {
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "type": {
          "src": "Type", 
          "type": "String"
        }
      }, 
      "geometry_type": "Polygon", 
      "src_layer": "RoadsExdm2ben.Roads.LandCover"
    }, 
    "roadsexdm2ben_roads_streetnameposition": {
      "fields": {
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "street": {
          "src": "Street", 
          "type": "String"
        }, 
        "namori": {
          "src": "NamOri", 
          "type": "Real"
        }
      }, 
      "geometry_type": "Point", 
      "src_layer": "RoadsExdm2ben.Roads.StreetNamePosition"
    }, 
    "roadsexdm2ben_roads_lattrs": {
      "fields": {
        "ref_id": {
          "src": "REF_ID", 
          "type": "String"
        }, 
        "lart": {
          "src": "LArt", 
          "type": "String"
        }, 
        "ref_name": {
          "src": "REF_NAME", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "RoadsExdm2ben.Roads.LAttrs"
    }, 
    "roadsexdm2ien_roadsextended_streetaxis": {
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
      "src_layer": "RoadsExdm2ien.RoadsExtended.StreetAxis"
    }, 
    "roadsexdm2ben_roads_street": {
      "fields": {
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "name": {
          "src": "Name", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "RoadsExdm2ben.Roads.Street"
    }
  }, 
  "src_format": "Interlis 2", 
  "dst_format": "PostgreSQL"
}"""
    print cfgjson
    assert cfgjson == expected


def test_enums():
    cfg = OgrConfig(ds="./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd", model="./tests/data/ili/RoadsExdm2ien.imd")
    cfgjson = cfg.generate_config(dst_format='PostgreSQL')
    expected = """"enums": {
    "enum3_lart": {
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

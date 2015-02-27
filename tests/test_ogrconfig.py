from ogrtools.ogrtransform.ogrconfig import OgrConfig
from ogrtools.interlis.ilismeta import prettify


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
    cfg = OgrConfig(
        ds="./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd")
    cfgjson = cfg.generate_config(dst_format='PostgreSQL', srs=21781)
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
          "type": "MultiLineString", 
          "srs": 21781
        }
      }
    }"""
    print cfgjson
    assert expected in cfgjson


def test_np():
    cfg = OgrConfig(ds="tests/data/np/NP_Example.xtf,tests/data/np/NP_73_CH_de_ili2.imd",
                    model="tests/data/np/NP_73_CH_de_ili2.imd")
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
    print cfg.enum_infos()
    assert {'name': 'roadsexdm2ien_roadsextended_roadsign',
            'geom_field': 'position'} in cfg.layer_infos()
    assert {'name': 'roadsexdm2ben_roads_lattrs'} in cfg.layer_infos()
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
    cfg = OgrConfig(ds="./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd",
                    config="./tests/data/ili/RoadsExdm2ien.cfg")
    vrt = prettify(cfg.generate_vrt())
    expected = """<OGRVRTLayer name="roadsign">
    <SrcDataSource relativeToVRT="0" shared="1">./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd</SrcDataSource>
    <SrcLayer>RoadsExdm2ien.RoadsExtended.RoadSign</SrcLayer>
    <Field name="tid" src="TID" type="String"/>
    <Field name="type" src="Type" type="String"/>
    <GeometryField field="Position" name="position">
      <GeometryType>wkbPoint</GeometryType>
      <SRS>EPSG:21781</SRS>
    </GeometryField>
  </OGRVRTLayer>"""
    print vrt
    assert expected in vrt


def test_reverse_vrt():
    cfg = OgrConfig(ds="./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd",
                    config="./tests/data/ili/RoadsExdm2ien.cfg")
    vrt = prettify(cfg.generate_reverse_vrt())
    expected = """<OGRVRTLayer name="RoadsExdm2ien.RoadsExtended.RoadSign">
    <SrcDataSource relativeToVRT="0" shared="1">./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd</SrcDataSource>
    <SrcLayer>roadsign</SrcLayer>
    <Field name="TID" src="tid"/>
    <Field name="Type" src="type"/>
    <GeometryField field="position" name="Position">
      <GeometryType>wkbPoint</GeometryType>
    </GeometryField>
  </OGRVRTLayer>"""
    print vrt
    assert expected in vrt


def test_multigeom_vrt():
    cfg = OgrConfig(ds="./tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.xtf,./tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.imd",
                    config="./tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.cfg")
    vrt = prettify(cfg.generate_vrt())
    expected = """<OGRVRTLayer name="oerebkrm09trsfr_transferstruktur_geometrie">
    <SrcDataSource relativeToVRT="0" shared="1">./tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.xtf,./tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.imd</SrcDataSource>
    <SrcLayer>OeREBKRM09trsfr.Transferstruktur.Geometrie</SrcLayer>
    <Field name="publiziertab" src="publiziertAb" type="String"/>
    <Field name="metadatengeobasisdaten" src="MetadatenGeobasisdaten" type="String"/>
    <Field name="tid" src="TID" type="String"/>
    <Field name="zustaendigestelle" src="ZustaendigeStelle" type="String"/>
    <Field name="rechtsstatus" src="Rechtsstatus" type="String"/>
    <Field name="eigentumsbeschraenkung" src="Eigentumsbeschraenkung" type="String"/>
    <GeometryField field="Punkt" name="punkt">
      <GeometryType>wkbPoint</GeometryType>
      <SRS>EPSG:21781</SRS>
    </GeometryField>
    <GeometryField field="Flaeche" name="flaeche">
      <GeometryType>wkbPolygon</GeometryType>
      <SRS>EPSG:21781</SRS>
    </GeometryField>
    <GeometryField field="Linie" name="linie">
      <GeometryType>wkbMultiLineString</GeometryType>
      <SRS>EPSG:21781</SRS>
    </GeometryField>
  </OGRVRTLayer>"""
    print vrt
    assert expected in vrt

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
      "src_layer": "RoadsExdm2ien.RoadsExtended.RoadSign", 
      "geom_fields": {
        "position": {
          "src": "Position", 
          "type": "Point"
        }
      }
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
      "src_layer": "RoadsExdm2ben.Roads.LandCover", 
      "geom_fields": {
        "geometry": {
          "src": "Geometry", 
          "type": "Polygon"
        }
      }
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
      "src_layer": "RoadsExdm2ben.Roads.StreetNamePosition", 
      "geom_fields": {
        "nampos": {
          "src": "NamPos", 
          "type": "Point"
        }
      }
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
      "src_layer": "RoadsExdm2ien.RoadsExtended.StreetAxis", 
      "geom_fields": {
        "geometry": {
          "src": "Geometry", 
          "type": "MultiLineString"
        }
      }
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


def test_np():
    cfg = OgrConfig(ds="tests/data/np/NP_Example.xtf,tests/data/np/NP_73_CH_de_ili2.imd", model="tests/data/np/NP_73_CH_de_ili2.imd")
    cfgjson = cfg.generate_config(dst_format='PostgreSQL')
    expected = """{
  "//": "OGR transformation configuration", 
  "dst_dsco": {}, 
  "dst_lco": {
    "SCHEMA": "public"
  }, 
  "layers": {
    "nutzungsplanung_nutzungsplanung_r4": {
      "fields": {
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "vorschrift": {
          "src": "Vorschrift", 
          "type": "String"
        }, 
        "objektbez_festl": {
          "src": "Objektbez_Festl", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "Nutzungsplanung.Nutzungsplanung.R4"
    }, 
    "n3_objektbezogene_festlegung": {
      "fields": {
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
        "typ": {
          "src": "Typ", 
          "type": "String"
        }, 
        "bemerkungen": {
          "src": "Bemerkungen", 
          "type": "String"
        }
      }, 
      "geometry_type": "Point", 
      "src_layer": "Nutzungsplanung.Nutzungsplanung.Objektbezogene_Festlegung", 
      "geom_fields": {
        "geometrie": {
          "src": "Geometrie", 
          "type": "Point"
        }
      }
    }, 
    "n2_linienbezogene_festlegung": {
      "fields": {
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
        "typ": {
          "src": "Typ", 
          "type": "String"
        }, 
        "bemerkungen": {
          "src": "Bemerkungen", 
          "type": "String"
        }
      }, 
      "geometry_type": "MultiLineString", 
      "src_layer": "Nutzungsplanung.Nutzungsplanung.Linienbezogene_Festlegung", 
      "geom_fields": {
        "geometrie": {
          "src": "Geometrie", 
          "type": "MultiLineString"
        }
      }
    }, 
    "nutzungsplanung_metadaten_organisation": {
      "fields": {
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "orgimweb": {
          "src": "OrgImWeb", 
          "type": "String"
        }, 
        "name": {
          "src": "Name", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "Nutzungsplanung.Metadaten.Organisation"
    }, 
    "n1_ueberlagernde_zonenflaeche": {
      "fields": {
        "herkunft": {
          "src": "Herkunft", 
          "type": "String"
        }, 
        "zonentyp": {
          "src": "Zonentyp", 
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
      "src_layer": "Nutzungsplanung.Nutzungsplanung.Ueberlagernde_Zonenflaeche", 
      "geom_fields": {
        "geometrie": {
          "src": "Geometrie", 
          "type": "Polygon"
        }
      }
    }, 
    "nutzungsplanung_nutzungsplanung_r2": {
      "fields": {
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "vorschrift": {
          "src": "Vorschrift", 
          "type": "String"
        }, 
        "ueberl_zone": {
          "src": "Ueberl_Zone", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "Nutzungsplanung.Nutzungsplanung.R2"
    }, 
    "nutzungsplanung_nutzungsplanung_r3": {
      "fields": {
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "vorschrift": {
          "src": "Vorschrift", 
          "type": "String"
        }, 
        "linienbez_festl": {
          "src": "Linienbez_Festl", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "Nutzungsplanung.Nutzungsplanung.R3"
    }, 
    "nutzungsplanung_metadaten_datenbestand": {
      "fields": {
        "datensatzidentifikator": {
          "src": "Datensatzidentifikator", 
          "type": "String"
        }, 
        "lieferdatum": {
          "src": "Lieferdatum", 
          "type": "String"
        }, 
        "datenstand": {
          "src": "Datenstand", 
          "type": "String"
        }, 
        "buero": {
          "src": "Buero", 
          "type": "String"
        }, 
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "zustaendigestelle": {
          "src": "zustaendigeStelle", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "Nutzungsplanung.Metadaten.Datenbestand"
    }, 
    "nutzungsplanung_url_": {
      "fields": {
        "ref_id": {
          "src": "REF_ID", 
          "type": "String"
        }, 
        "value": {
          "src": "value", 
          "type": "String"
        }, 
        "ref_name": {
          "src": "REF_NAME", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "Nutzungsplanung.URL_"
    }, 
    "n4_linienbezogener_festlegungstyp": {
      "fields": {
        "identifikator": {
          "src": "Identifikator", 
          "type": "String"
        }, 
        "linien_typ_kt": {
          "src": "Linien_Typ_Kt", 
          "type": "String"
        }, 
        "festl_typ": {
          "src": "Festl_Typ", 
          "type": "String"
        }, 
        "verbindlichkeit": {
          "src": "Verbindlichkeit", 
          "type": "String"
        }, 
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "abkuerzung": {
          "src": "Abkuerzung", 
          "type": "String"
        }, 
        "bemerkungen": {
          "src": "Bemerkungen", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "Nutzungsplanung.Nutzungsplanung.Linienbezogener_Festlegungstyp"
    }, 
    "n0_grundnutzung_zonenflaeche": {
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
    }, 
    "nutzungsplanung_nutzungsplanung_dokument": {
      "fields": {
        "textimweb": {
          "src": "TextImWeb", 
          "type": "String"
        }, 
        "titel": {
          "src": "Titel", 
          "type": "String"
        }, 
        "offiziellertitel": {
          "src": "OffiziellerTitel", 
          "type": "String"
        }, 
        "offiziellenr": {
          "src": "OffizielleNr", 
          "type": "String"
        }, 
        "publiziertab": {
          "src": "publiziertAb", 
          "type": "String"
        }, 
        "kanton": {
          "src": "Kanton", 
          "type": "String"
        }, 
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "gemeinde": {
          "src": "Gemeinde", 
          "type": "Real"
        }, 
        "rechtsstatus": {
          "src": "Rechtsstatus", 
          "type": "String"
        }, 
        "abkuerzung": {
          "src": "Abkuerzung", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "Nutzungsplanung.Nutzungsplanung.Dokument"
    }, 
    "n6_ueberlagernder_zonentyp_kt": {
      "fields": {
        "zonentyp_kt": {
          "src": "Zonentyp_Kt", 
          "type": "String"
        }, 
        "identifikator": {
          "src": "Identifikator", 
          "type": "String"
        }, 
        "ueberl_hauptn_ch": {
          "src": "Ueberl_Hauptn_CH", 
          "type": "String"
        }, 
        "ueberl_zonentyp_sia": {
          "src": "Ueberl_Zonentyp_SIA", 
          "type": "String"
        }, 
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "abkuerzung": {
          "src": "Abkuerzung", 
          "type": "String"
        }, 
        "bemerkungen": {
          "src": "Bemerkungen", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "Nutzungsplanung.Nutzungsplanung.Ueberlagernder_Zonentyp_Kt"
    }, 
    "n5_objektbezogener_festlegungstyp": {
      "fields": {
        "identifikator": {
          "src": "Identifikator", 
          "type": "String"
        }, 
        "festl_typ": {
          "src": "Festl_Typ", 
          "type": "String"
        }, 
        "festl_typ_kt": {
          "src": "Festl_Typ_Kt", 
          "type": "String"
        }, 
        "verbindlichkeit": {
          "src": "Verbindlichkeit", 
          "type": "String"
        }, 
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "abkuerzung": {
          "src": "Abkuerzung", 
          "type": "String"
        }, 
        "bemerkungen": {
          "src": "Bemerkungen", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "Nutzungsplanung.Nutzungsplanung.Objektbezogener_Festlegungstyp"
    }, 
    "nutzungsplanung_nutzungsplanung_r1": {
      "fields": {
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "vorschrift": {
          "src": "Vorschrift", 
          "type": "String"
        }, 
        "grundn_zone": {
          "src": "Grundn_Zone", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "Nutzungsplanung.Nutzungsplanung.R1"
    }, 
    "nutzungsplanung_nutzungsplanung_ueberlagernder_zonentyp": {
      "fields": {
        "zonentyp_kt": {
          "src": "Zonentyp_Kt", 
          "type": "String"
        }, 
        "identifikator": {
          "src": "Identifikator", 
          "type": "String"
        }, 
        "zonentyp": {
          "src": "Zonentyp", 
          "type": "String"
        }, 
        "verbindlichkeit": {
          "src": "Verbindlichkeit", 
          "type": "String"
        }, 
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "abkuerzung": {
          "src": "Abkuerzung", 
          "type": "String"
        }, 
        "bemerkungen": {
          "src": "Bemerkungen", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "Nutzungsplanung.Nutzungsplanung.Ueberlagernder_Zonentyp"
    }, 
    "nutzungsplanung_nutzungsplanung_grundnutzung_zonentyp": {
      "fields": {
        "identifikator": {
          "src": "Identifikator", 
          "type": "String"
        }, 
        "zonentyp_kt_2": {
          "src": "Zonentyp_Kt_2", 
          "type": "String"
        }, 
        "zonentyp": {
          "src": "Zonentyp", 
          "type": "String"
        }, 
        "verbindlichkeit": {
          "src": "Verbindlichkeit", 
          "type": "String"
        }, 
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "abkuerzung": {
          "src": "Abkuerzung", 
          "type": "String"
        }, 
        "bemerkungen": {
          "src": "Bemerkungen", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "Nutzungsplanung.Nutzungsplanung.Grundnutzung_Zonentyp"
    }, 
    "nutzungsplanung_nutzungsplanung_grundnutzung_zonentyp_kt": {
      "fields": {
        "zonentyp_kt": {
          "src": "Zonentyp_Kt", 
          "type": "String"
        }, 
        "identifikator": {
          "src": "Identifikator", 
          "type": "String"
        }, 
        "zonentyp_sia": {
          "src": "Zonentyp_SIA", 
          "type": "String"
        }, 
        "hauptnutzung_ch": {
          "src": "Hauptnutzung_CH", 
          "type": "String"
        }, 
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "abkuerzung": {
          "src": "Abkuerzung", 
          "type": "String"
        }, 
        "bemerkungen": {
          "src": "Bemerkungen", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "Nutzungsplanung.Nutzungsplanung.Grundnutzung_Zonentyp_Kt"
    }, 
    "n7_linienbezogener_festlegungstyp_kt": {
      "fields": {
        "identifikator": {
          "src": "Identifikator", 
          "type": "String"
        }, 
        "festl_typ_sia": {
          "src": "Festl_Typ_SIA", 
          "type": "String"
        }, 
        "festl_typ_kt": {
          "src": "Festl_Typ_Kt", 
          "type": "String"
        }, 
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "abkuerzung": {
          "src": "Abkuerzung", 
          "type": "String"
        }, 
        "bemerkungen": {
          "src": "Bemerkungen", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "Nutzungsplanung.Nutzungsplanung.Linienbezogener_Festlegungstyp_Kt"
    }, 
    "n8_objektbezogener_festlegungstyp_kt": {
      "fields": {
        "identifikator": {
          "src": "Identifikator", 
          "type": "String"
        }, 
        "festl_typ_sia": {
          "src": "Festl_Typ_SIA", 
          "type": "String"
        }, 
        "festl_typ_kt": {
          "src": "Festl_Typ_Kt", 
          "type": "String"
        }, 
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "abkuerzung": {
          "src": "Abkuerzung", 
          "type": "String"
        }, 
        "bemerkungen": {
          "src": "Bemerkungen", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "Nutzungsplanung.Nutzungsplanung.Objektbezogener_Festlegungstyp_Kt"
    }, 
    "nutzungsplanung_nutzungsplanung_mutationshinweis": {
      "fields": {
        "tid": {
          "src": "TID", 
          "type": "String"
        }, 
        "erfasser": {
          "src": "Erfasser", 
          "type": "String"
        }, 
        "identifikator": {
          "src": "Identifikator", 
          "type": "String"
        }, 
        "bemerkungen": {
          "src": "Bemerkungen", 
          "type": "String"
        }, 
        "erfassungsdatum": {
          "src": "Erfassungsdatum", 
          "type": "String"
        }
      }, 
      "geometry_type": "None", 
      "src_layer": "Nutzungsplanung.Nutzungsplanung.Mutationshinweis"
    }
  }, 
  "src_format": "Interlis 2", 
  "enums": {
    "enum9_halignment": {
      "src_name": "INTERLIS.HALIGNMENT", 
      "values": [
        {
          "enumtxt": "Left", 
          "enum": "Left", 
          "id": 0
        }, 
        {
          "enumtxt": "Center", 
          "enum": "Center", 
          "id": 1
        }, 
        {
          "enumtxt": "Right", 
          "enum": "Right", 
          "id": 2
        }
      ]
    }, 
    "enum21_ueberl_hauptn_ch": {
      "src_name": "Nutzungsplanung.Nutzungsplanung.Ueberlagernder_Zonentyp_Kt.Ueberl_Hauptn_CH", 
      "values": [
        {
          "enumtxt": "ueberlagernde_Schutzzonen_61", 
          "enum": "ueberlagernde_Schutzzonen_61", 
          "id": 0
        }, 
        {
          "enumtxt": "ueberlagernde_Nutzungszonen_62", 
          "enum": "ueberlagernde_Nutzungszonen_62", 
          "id": 1
        }, 
        {
          "enumtxt": "ueberlagernde_Gefahrenzonen_63", 
          "enum": "ueberlagernde_Gefahrenzonen_63", 
          "id": 2
        }, 
        {
          "enumtxt": "ueberlagernde_Flaechenfestlegungen_64", 
          "enum": "ueberlagernde_Flaechenfestlegungen_64", 
          "id": 3
        }
      ]
    }, 
    "enum28_rechtsstatus": {
      "src_name": "Nutzungsplanung.Nutzungsplanung.Dokument.Rechtsstatus", 
      "values": [
        {
          "enumtxt": "inKraft", 
          "enum": "inKraft", 
          "id": 0
        }, 
        {
          "enumtxt": "laufendeAenderungen", 
          "enum": "laufendeAenderungen", 
          "id": 1
        }
      ]
    }, 
    "enum24_verbindlichkeit": {
      "src_name": "Nutzungsplanung.Nutzungsplanung.Linienbezogener_Festlegungstyp.Verbindlichkeit", 
      "values": [
        {
          "enumtxt": "eigentuemerverbindlich", 
          "enum": "eigentuemerverbindlich", 
          "id": 0
        }, 
        {
          "enumtxt": "orientierend", 
          "enum": "orientierend", 
          "id": 1
        }, 
        {
          "enumtxt": "hinweisend", 
          "enum": "hinweisend", 
          "id": 2
        }
      ]
    }, 
    "enum15_ueberl_zonen_sia": {
      "src_name": "Nutzungsplanung.Ueberl_Zonen_SIA", 
      "values": [
        {
          "enumtxt": "Ueberl_Schutzzonen_61.Ueberl_Ortsbildschutzzone_611", 
          "enum": "Ueberl_Schutzzonen_61.Ueberl_Ortsbildschutzzone_611", 
          "id": 0
        }, 
        {
          "enumtxt": "Ueberl_Schutzzonen_61.Ueberl_Naturschutzzone_612", 
          "enum": "Ueberl_Schutzzonen_61.Ueberl_Naturschutzzone_612", 
          "id": 1
        }, 
        {
          "enumtxt": "Ueberl_Schutzzonen_61.Grundwasserschutzzone_613", 
          "enum": "Ueberl_Schutzzonen_61.Grundwasserschutzzone_613", 
          "id": 2
        }, 
        {
          "enumtxt": "Ueberl_Schutzzonen_61.Landschaftsschutzzone_614", 
          "enum": "Ueberl_Schutzzonen_61.Landschaftsschutzzone_614", 
          "id": 3
        }, 
        {
          "enumtxt": "Ueberl_Schutzzonen_61.Freihaltezone_615", 
          "enum": "Ueberl_Schutzzonen_61.Freihaltezone_615", 
          "id": 4
        }, 
        {
          "enumtxt": "Ueberl_Schutzzonen_61.weiterer_Zonentyp_616", 
          "enum": "Ueberl_Schutzzonen_61.weiterer_Zonentyp_616", 
          "id": 5
        }, 
        {
          "enumtxt": "Ueberl_Zonen_nach_Art_18_RPG_62.Nutzungsanteilzone_621", 
          "enum": "Ueberl_Zonen_nach_Art_18_RPG_62.Nutzungsanteilzone_621", 
          "id": 6
        }, 
        {
          "enumtxt": "Ueberl_Zonen_nach_Art_18_RPG_62.Ueberl_Abbauzone_622", 
          "enum": "Ueberl_Zonen_nach_Art_18_RPG_62.Ueberl_Abbauzone_622", 
          "id": 7
        }, 
        {
          "enumtxt": "Ueberl_Zonen_nach_Art_18_RPG_62.Ueberl_Deponiezone_623", 
          "enum": "Ueberl_Zonen_nach_Art_18_RPG_62.Ueberl_Deponiezone_623", 
          "id": 8
        }, 
        {
          "enumtxt": "Ueberl_Zonen_nach_Art_18_RPG_62.Ueberl_Tourismus_und_Erholungszone_624", 
          "enum": "Ueberl_Zonen_nach_Art_18_RPG_62.Ueberl_Tourismus_und_Erholungszone_624", 
          "id": 9
        }, 
        {
          "enumtxt": "Ueberl_Zonen_nach_Art_18_RPG_62.Zone_fuer_Verkehrszone_ueber_oder_unter_Bauten_625", 
          "enum": "Ueberl_Zonen_nach_Art_18_RPG_62.Zone_fuer_Verkehrszone_ueber_oder_unter_Bauten_625", 
          "id": 10
        }, 
        {
          "enumtxt": "Ueberl_Zonen_nach_Art_18_RPG_62.Zone_fuer_Bauten_ueber_oder_unter_Verkehrszonen_626", 
          "enum": "Ueberl_Zonen_nach_Art_18_RPG_62.Zone_fuer_Bauten_ueber_oder_unter_Verkehrszonen_626", 
          "id": 11
        }, 
        {
          "enumtxt": "Ueberl_Zonen_nach_Art_18_RPG_62.Zone_fuer_Bauten_im_Gewaesserbereich_627", 
          "enum": "Ueberl_Zonen_nach_Art_18_RPG_62.Zone_fuer_Bauten_im_Gewaesserbereich_627", 
          "id": 12
        }, 
        {
          "enumtxt": "Ueberl_Zonen_nach_Art_18_RPG_62.Ueberl_Bauzone_628", 
          "enum": "Ueberl_Zonen_nach_Art_18_RPG_62.Ueberl_Bauzone_628", 
          "id": 13
        }, 
        {
          "enumtxt": "Ueberl_Zonen_nach_Art_18_RPG_62.weiterer_Zonentyp_629", 
          "enum": "Ueberl_Zonen_nach_Art_18_RPG_62.weiterer_Zonentyp_629", 
          "id": 14
        }, 
        {
          "enumtxt": "Ueberl_Gefahrenzonen_nach_Art_18_RPG_63.Zone_mit_Restgefaehrdung_631", 
          "enum": "Ueberl_Gefahrenzonen_nach_Art_18_RPG_63.Zone_mit_Restgefaehrdung_631", 
          "id": 15
        }, 
        {
          "enumtxt": "Ueberl_Gefahrenzonen_nach_Art_18_RPG_63.Zone_mit_geringer_Gefaehrdung_632", 
          "enum": "Ueberl_Gefahrenzonen_nach_Art_18_RPG_63.Zone_mit_geringer_Gefaehrdung_632", 
          "id": 16
        }, 
        {
          "enumtxt": "Ueberl_Gefahrenzonen_nach_Art_18_RPG_63.Zone_mit_mittlerer_Gefaehrdung_633", 
          "enum": "Ueberl_Gefahrenzonen_nach_Art_18_RPG_63.Zone_mit_mittlerer_Gefaehrdung_633", 
          "id": 17
        }, 
        {
          "enumtxt": "Ueberl_Gefahrenzonen_nach_Art_18_RPG_63.Zone_mit_erheblicher_Gefaehrdung_634", 
          "enum": "Ueberl_Gefahrenzonen_nach_Art_18_RPG_63.Zone_mit_erheblicher_Gefaehrdung_634", 
          "id": 18
        }, 
        {
          "enumtxt": "Ueberl_Flaechenfestlegungen_keine_eigentliche_Zonen_64.Bereich_Sondernutzungsplanungspflicht_641", 
          "enum": "Ueberl_Flaechenfestlegungen_keine_eigentliche_Zonen_64.Bereich_Sondernutzungsplanungspflicht_641", 
          "id": 19
        }, 
        {
          "enumtxt": "Ueberl_Flaechenfestlegungen_keine_eigentliche_Zonen_64.Bereich_rechtsgueltiger_Sondernutzungsplaene_642", 
          "enum": "Ueberl_Flaechenfestlegungen_keine_eigentliche_Zonen_64.Bereich_rechtsgueltiger_Sondernutzungsplaene_642", 
          "id": 20
        }, 
        {
          "enumtxt": "Ueberl_Flaechenfestlegungen_keine_eigentliche_Zonen_64.Bereich_einer_spaeteren_Erschliessungsetappe_643", 
          "enum": "Ueberl_Flaechenfestlegungen_keine_eigentliche_Zonen_64.Bereich_einer_spaeteren_Erschliessungsetappe_643", 
          "id": 21
        }, 
        {
          "enumtxt": "Ueberl_Flaechenfestlegungen_keine_eigentliche_Zonen_64.Archaeologische_Fundstelle_644", 
          "enum": "Ueberl_Flaechenfestlegungen_keine_eigentliche_Zonen_64.Archaeologische_Fundstelle_644", 
          "id": 22
        }, 
        {
          "enumtxt": "Ueberl_Flaechenfestlegungen_keine_eigentliche_Zonen_64.Gebiet_mit_erdgeschichtlicher_Bedeutung_Geotop_645", 
          "enum": "Ueberl_Flaechenfestlegungen_keine_eigentliche_Zonen_64.Gebiet_mit_erdgeschichtlicher_Bedeutung_Geotop_645", 
          "id": 23
        }, 
        {
          "enumtxt": "Ueberl_Flaechenfestlegungen_keine_eigentliche_Zonen_64.Bereich_Altlasten_646", 
          "enum": "Ueberl_Flaechenfestlegungen_keine_eigentliche_Zonen_64.Bereich_Altlasten_646", 
          "id": 24
        }, 
        {
          "enumtxt": "Ueberl_Flaechenfestlegungen_keine_eigentliche_Zonen_64.Bruecke_ueber_Gewaesser_647", 
          "enum": "Ueberl_Flaechenfestlegungen_keine_eigentliche_Zonen_64.Bruecke_ueber_Gewaesser_647", 
          "id": 25
        }, 
        {
          "enumtxt": "Ueberl_Flaechenfestlegungen_keine_eigentliche_Zonen_64.weitere_Flaechefestlegung_648", 
          "enum": "Ueberl_Flaechenfestlegungen_keine_eigentliche_Zonen_64.weitere_Flaechefestlegung_648", 
          "id": 26
        }
      ]
    }, 
    "enum22_herkunft": {
      "src_name": "Nutzungsplanung.Nutzungsplanung.Grundnutzung_Zonenflaeche.Herkunft", 
      "values": [
        {
          "enumtxt": "Aufnahme", 
          "enum": "Aufnahme", 
          "id": 0
        }, 
        {
          "enumtxt": "Uebernahme_Koordinaten", 
          "enum": "Uebernahme_Koordinaten", 
          "id": 1
        }, 
        {
          "enumtxt": "Planabgriff", 
          "enum": "Planabgriff", 
          "id": 2
        }, 
        {
          "enumtxt": "konstruktiv", 
          "enum": "konstruktiv", 
          "id": 3
        }, 
        {
          "enumtxt": "andere", 
          "enum": "andere", 
          "id": 4
        }
      ]
    }, 
    "enum29_herkunft": {
      "src_name": "Nutzungsplanung.Nutzungsplanung.Objektbezogene_Festlegung.Herkunft", 
      "values": [
        {
          "enumtxt": "Aufnahme", 
          "enum": "Aufnahme", 
          "id": 0
        }, 
        {
          "enumtxt": "Uebernahme_Koordinaten", 
          "enum": "Uebernahme_Koordinaten", 
          "id": 1
        }, 
        {
          "enumtxt": "Planabgriff", 
          "enum": "Planabgriff", 
          "id": 2
        }, 
        {
          "enumtxt": "konstruktiv", 
          "enum": "konstruktiv", 
          "id": 3
        }, 
        {
          "enumtxt": "andere", 
          "enum": "andere", 
          "id": 4
        }
      ]
    }, 
    "enum17_verbindlichkeit": {
      "src_name": "Nutzungsplanung.Nutzungsplanung.Objektbezogener_Festlegungstyp.Verbindlichkeit", 
      "values": [
        {
          "enumtxt": "eigentuemerverbindlich", 
          "enum": "eigentuemerverbindlich", 
          "id": 0
        }, 
        {
          "enumtxt": "orientierend", 
          "enum": "orientierend", 
          "id": 1
        }, 
        {
          "enumtxt": "hinweisend", 
          "enum": "hinweisend", 
          "id": 2
        }
      ]
    }, 
    "enum27_verbindlichkeit": {
      "src_name": "Nutzungsplanung.Nutzungsplanung.Grundnutzung_Zonentyp.Verbindlichkeit", 
      "values": [
        {
          "enumtxt": "eigentuemerverbindlich", 
          "enum": "eigentuemerverbindlich", 
          "id": 0
        }, 
        {
          "enumtxt": "orientierend", 
          "enum": "orientierend", 
          "id": 1
        }, 
        {
          "enumtxt": "hinweisend", 
          "enum": "hinweisend", 
          "id": 2
        }
      ]
    }, 
    "enum33_verbindlichkeit": {
      "src_name": "Nutzungsplanung.Nutzungsplanung.Ueberlagernder_Zonentyp.Verbindlichkeit", 
      "values": [
        {
          "enumtxt": "eigentuemerverbindlich", 
          "enum": "eigentuemerverbindlich", 
          "id": 0
        }, 
        {
          "enumtxt": "orientierend", 
          "enum": "orientierend", 
          "id": 1
        }, 
        {
          "enumtxt": "hinweisend", 
          "enum": "hinweisend", 
          "id": 2
        }
      ]
    }, 
    "enum31_boolean": {
      "src_name": "INTERLIS.BOOLEAN", 
      "values": [
        {
          "enumtxt": "false", 
          "enum": "false", 
          "id": 0
        }, 
        {
          "enumtxt": "true", 
          "enum": "true", 
          "id": 1
        }
      ]
    }, 
    "enum32_verbindlichkeit": {
      "src_name": "Nutzungsplanung.Verbindlichkeit", 
      "values": [
        {
          "enumtxt": "eigentuemerverbindlich", 
          "enum": "eigentuemerverbindlich", 
          "id": 0
        }, 
        {
          "enumtxt": "orientierend", 
          "enum": "orientierend", 
          "id": 1
        }, 
        {
          "enumtxt": "hinweisend", 
          "enum": "hinweisend", 
          "id": 2
        }
      ]
    }, 
    "enum25_qualitaet": {
      "src_name": "Nutzungsplanung.Nutzungsplanung.Grundnutzung_Zonenflaeche.Qualitaet", 
      "values": [
        {
          "enumtxt": "AV93", 
          "enum": "AV93", 
          "id": 0
        }, 
        {
          "enumtxt": "PV74", 
          "enum": "PV74", 
          "id": 1
        }, 
        {
          "enumtxt": "PN", 
          "enum": "PN", 
          "id": 2
        }, 
        {
          "enumtxt": "weitere", 
          "enum": "weitere", 
          "id": 3
        }
      ]
    }, 
    "enum13_qualitaet": {
      "src_name": "Nutzungsplanung.Nutzungsplanung.Ueberlagernde_Zonenflaeche.Qualitaet", 
      "values": [
        {
          "enumtxt": "AV93", 
          "enum": "AV93", 
          "id": 0
        }, 
        {
          "enumtxt": "PV74", 
          "enum": "PV74", 
          "id": 1
        }, 
        {
          "enumtxt": "PN", 
          "enum": "PN", 
          "id": 2
        }, 
        {
          "enumtxt": "weitere", 
          "enum": "weitere", 
          "id": 3
        }
      ]
    }, 
    "enum23_valignment": {
      "src_name": "INTERLIS.VALIGNMENT", 
      "values": [
        {
          "enumtxt": "Top", 
          "enum": "Top", 
          "id": 0
        }, 
        {
          "enumtxt": "Cap", 
          "enum": "Cap", 
          "id": 1
        }, 
        {
          "enumtxt": "Half", 
          "enum": "Half", 
          "id": 2
        }, 
        {
          "enumtxt": "Base", 
          "enum": "Base", 
          "id": 3
        }, 
        {
          "enumtxt": "Bottom", 
          "enum": "Bottom", 
          "id": 4
        }
      ]
    }, 
    "enum30_herkunft": {
      "src_name": "Nutzungsplanung.Nutzungsplanung.Linienbezogene_Festlegung.Herkunft", 
      "values": [
        {
          "enumtxt": "Aufnahme", 
          "enum": "Aufnahme", 
          "id": 0
        }, 
        {
          "enumtxt": "Uebernahme_Koordinaten", 
          "enum": "Uebernahme_Koordinaten", 
          "id": 1
        }, 
        {
          "enumtxt": "Planabgriff", 
          "enum": "Planabgriff", 
          "id": 2
        }, 
        {
          "enumtxt": "konstruktiv", 
          "enum": "konstruktiv", 
          "id": 3
        }, 
        {
          "enumtxt": "andere", 
          "enum": "andere", 
          "id": 4
        }
      ]
    }, 
    "enum11_qualitaet": {
      "src_name": "Nutzungsplanung.Nutzungsplanung.Linienbezogene_Festlegung.Qualitaet", 
      "values": [
        {
          "enumtxt": "AV93", 
          "enum": "AV93", 
          "id": 0
        }, 
        {
          "enumtxt": "PV74", 
          "enum": "PV74", 
          "id": 1
        }, 
        {
          "enumtxt": "PN", 
          "enum": "PN", 
          "id": 2
        }, 
        {
          "enumtxt": "weitere", 
          "enum": "weitere", 
          "id": 3
        }
      ]
    }, 
    "enum19_objektbez_festl_sia": {
      "src_name": "Nutzungsplanung.Objektbez_Festl_SIA", 
      "values": [
        {
          "enumtxt": "Naturobjekt_811", 
          "enum": "Naturobjekt_811", 
          "id": 0
        }, 
        {
          "enumtxt": "Denkmalschutz_und_Kulturobjekt_812.kommunales_Objekt_8121", 
          "enum": "Denkmalschutz_und_Kulturobjekt_812.kommunales_Objekt_8121", 
          "id": 1
        }, 
        {
          "enumtxt": "Denkmalschutz_und_Kulturobjekt_812.kantonales_Objekt_8122", 
          "enum": "Denkmalschutz_und_Kulturobjekt_812.kantonales_Objekt_8122", 
          "id": 2
        }, 
        {
          "enumtxt": "weitere_Objektbez_Festl_813", 
          "enum": "weitere_Objektbez_Festl_813", 
          "id": 3
        }
      ]
    }, 
    "enum26_herkunft": {
      "src_name": "Nutzungsplanung.Nutzungsplanung.Ueberlagernde_Zonenflaeche.Herkunft", 
      "values": [
        {
          "enumtxt": "Aufnahme", 
          "enum": "Aufnahme", 
          "id": 0
        }, 
        {
          "enumtxt": "Uebernahme_Koordinaten", 
          "enum": "Uebernahme_Koordinaten", 
          "id": 1
        }, 
        {
          "enumtxt": "Planabgriff", 
          "enum": "Planabgriff", 
          "id": 2
        }, 
        {
          "enumtxt": "konstruktiv", 
          "enum": "konstruktiv", 
          "id": 3
        }, 
        {
          "enumtxt": "andere", 
          "enum": "andere", 
          "id": 4
        }
      ]
    }, 
    "enum12_geometrie_herkunft": {
      "src_name": "Nutzungsplanung.Geometrie_Herkunft", 
      "values": [
        {
          "enumtxt": "Aufnahme", 
          "enum": "Aufnahme", 
          "id": 0
        }, 
        {
          "enumtxt": "Uebernahme_Koordinaten", 
          "enum": "Uebernahme_Koordinaten", 
          "id": 1
        }, 
        {
          "enumtxt": "Planabgriff", 
          "enum": "Planabgriff", 
          "id": 2
        }, 
        {
          "enumtxt": "konstruktiv", 
          "enum": "konstruktiv", 
          "id": 3
        }, 
        {
          "enumtxt": "andere", 
          "enum": "andere", 
          "id": 4
        }
      ]
    }, 
    "enum36_linienbez_festl_sia": {
      "src_name": "Nutzungsplanung.Linienbez_Festl_SIA", 
      "values": [
        {
          "enumtxt": "Baulinie_711", 
          "enum": "Baulinie_711", 
          "id": 0
        }, 
        {
          "enumtxt": "Uferlinie_Bachlauf_712", 
          "enum": "Uferlinie_Bachlauf_712", 
          "id": 1
        }, 
        {
          "enumtxt": "Allee_713", 
          "enum": "Allee_713", 
          "id": 2
        }, 
        {
          "enumtxt": "Hecke_714", 
          "enum": "Hecke_714", 
          "id": 3
        }, 
        {
          "enumtxt": "projektierte_bewilligte_Verkehrswege_715", 
          "enum": "projektierte_bewilligte_Verkehrswege_715", 
          "id": 4
        }, 
        {
          "enumtxt": "weitere_Linienbez_Festl_716", 
          "enum": "weitere_Linienbez_Festl_716", 
          "id": 5
        }
      ]
    }, 
    "enum14_rechtsstatus": {
      "src_name": "Nutzungsplanung.Rechtsstatus", 
      "values": [
        {
          "enumtxt": "inKraft", 
          "enum": "inKraft", 
          "id": 0
        }, 
        {
          "enumtxt": "laufendeAenderungen", 
          "enum": "laufendeAenderungen", 
          "id": 1
        }
      ]
    }, 
    "enum18_grundnutzung_sia": {
      "src_name": "Nutzungsplanung.Grundnutzung_SIA", 
      "values": [
        {
          "enumtxt": "Wohnzonen_11.Wohnzone_a_111", 
          "enum": "Wohnzonen_11.Wohnzone_a_111", 
          "id": 0
        }, 
        {
          "enumtxt": "Wohnzonen_11.Wohnzone_b_112", 
          "enum": "Wohnzonen_11.Wohnzone_b_112", 
          "id": 1
        }, 
        {
          "enumtxt": "Wohnzonen_11.Wohnzone_c_113", 
          "enum": "Wohnzonen_11.Wohnzone_c_113", 
          "id": 2
        }, 
        {
          "enumtxt": "Wohnzonen_11.Wohnzone_d_114", 
          "enum": "Wohnzonen_11.Wohnzone_d_114", 
          "id": 3
        }, 
        {
          "enumtxt": "Wohnzonen_11.weiterer_Zonentyp_115", 
          "enum": "Wohnzonen_11.weiterer_Zonentyp_115", 
          "id": 4
        }, 
        {
          "enumtxt": "Arbeitszonen_12.Arbeitszone_a_121", 
          "enum": "Arbeitszonen_12.Arbeitszone_a_121", 
          "id": 5
        }, 
        {
          "enumtxt": "Arbeitszonen_12.Arbeitszone_b_122", 
          "enum": "Arbeitszonen_12.Arbeitszone_b_122", 
          "id": 6
        }, 
        {
          "enumtxt": "Arbeitszonen_12.Arbeitszone_c_123", 
          "enum": "Arbeitszonen_12.Arbeitszone_c_123", 
          "id": 7
        }, 
        {
          "enumtxt": "Arbeitszonen_12.weiterer_Zonentyp_124", 
          "enum": "Arbeitszonen_12.weiterer_Zonentyp_124", 
          "id": 8
        }, 
        {
          "enumtxt": "Mischzonen_13.Wohn_und_Arbeitszone_a_131", 
          "enum": "Mischzonen_13.Wohn_und_Arbeitszone_a_131", 
          "id": 9
        }, 
        {
          "enumtxt": "Mischzonen_13.Wohn_und_Arbeitszone_b_132", 
          "enum": "Mischzonen_13.Wohn_und_Arbeitszone_b_132", 
          "id": 10
        }, 
        {
          "enumtxt": "Mischzonen_13.weiterer_Zonentyp_133", 
          "enum": "Mischzonen_13.weiterer_Zonentyp_133", 
          "id": 11
        }, 
        {
          "enumtxt": "Zentrumszonen_14.allgemeine_Zentrumszone_141", 
          "enum": "Zentrumszonen_14.allgemeine_Zentrumszone_141", 
          "id": 12
        }, 
        {
          "enumtxt": "Zentrumszonen_14.Kernzone_142", 
          "enum": "Zentrumszonen_14.Kernzone_142", 
          "id": 13
        }, 
        {
          "enumtxt": "Zentrumszonen_14.Geschaeftszone_143", 
          "enum": "Zentrumszonen_14.Geschaeftszone_143", 
          "id": 14
        }, 
        {
          "enumtxt": "Zentrumszonen_14.weiterer_Zonentyp_144", 
          "enum": "Zentrumszonen_14.weiterer_Zonentyp_144", 
          "id": 15
        }, 
        {
          "enumtxt": "Zonen_fuer_oeffentliche_Nutzungen_15.Zone_fuer_oeffentliche_Bauten_und_Anlagen_151", 
          "enum": "Zonen_fuer_oeffentliche_Nutzungen_15.Zone_fuer_oeffentliche_Bauten_und_Anlagen_151", 
          "id": 16
        }, 
        {
          "enumtxt": "Zonen_fuer_oeffentliche_Nutzungen_15.Zone_fuer_oeffentlichen_Sport_und_Freizeitanlagen_152", 
          "enum": "Zonen_fuer_oeffentliche_Nutzungen_15.Zone_fuer_oeffentlichen_Sport_und_Freizeitanlagen_152", 
          "id": 17
        }, 
        {
          "enumtxt": "Zonen_fuer_oeffentliche_Nutzungen_15.weiterer_Zonentyp_153", 
          "enum": "Zonen_fuer_oeffentliche_Nutzungen_15.weiterer_Zonentyp_153", 
          "id": 18
        }, 
        {
          "enumtxt": "eingeschraenkte_Bauzonen_16.Gruenzone_161", 
          "enum": "eingeschraenkte_Bauzonen_16.Gruenzone_161", 
          "id": 19
        }, 
        {
          "enumtxt": "eingeschraenkte_Bauzonen_16.weiterer_Zonentyp_162", 
          "enum": "eingeschraenkte_Bauzonen_16.weiterer_Zonentyp_162", 
          "id": 20
        }, 
        {
          "enumtxt": "Tourismus_und_Freizeitzonen_17.Kurzone_171", 
          "enum": "Tourismus_und_Freizeitzonen_17.Kurzone_171", 
          "id": 21
        }, 
        {
          "enumtxt": "Tourismus_und_Freizeitzonen_17.Hotelzone_172", 
          "enum": "Tourismus_und_Freizeitzonen_17.Hotelzone_172", 
          "id": 22
        }, 
        {
          "enumtxt": "Tourismus_und_Freizeitzonen_17.Campingzone_173", 
          "enum": "Tourismus_und_Freizeitzonen_17.Campingzone_173", 
          "id": 23
        }, 
        {
          "enumtxt": "Tourismus_und_Freizeitzonen_17.weiterer_Zonentyp_174", 
          "enum": "Tourismus_und_Freizeitzonen_17.weiterer_Zonentyp_174", 
          "id": 24
        }, 
        {
          "enumtxt": "Verkehrszonen_18.Strassenzone_181", 
          "enum": "Verkehrszonen_18.Strassenzone_181", 
          "id": 25
        }, 
        {
          "enumtxt": "Verkehrszonen_18.Bahnzone_182", 
          "enum": "Verkehrszonen_18.Bahnzone_182", 
          "id": 26
        }, 
        {
          "enumtxt": "Verkehrszonen_18.Flugplatzzone_183", 
          "enum": "Verkehrszonen_18.Flugplatzzone_183", 
          "id": 27
        }, 
        {
          "enumtxt": "Verkehrszonen_18.weiterer_Zonentyp_184", 
          "enum": "Verkehrszonen_18.weiterer_Zonentyp_184", 
          "id": 28
        }, 
        {
          "enumtxt": "weitere_Zonen_19.Sonderbauzone_191", 
          "enum": "weitere_Zonen_19.Sonderbauzone_191", 
          "id": 29
        }, 
        {
          "enumtxt": "weitere_Zonen_19.weiterer_Zonentyp_192", 
          "enum": "weitere_Zonen_19.weiterer_Zonentyp_192", 
          "id": 30
        }, 
        {
          "enumtxt": "Allgemeine_Landwirtschaftszonen_21.allgemeine_Landwirtschaftszone_211", 
          "enum": "Allgemeine_Landwirtschaftszonen_21.allgemeine_Landwirtschaftszone_211", 
          "id": 31
        }, 
        {
          "enumtxt": "Allgemeine_Landwirtschaftszonen_21.weiterer_Zonentyp_212", 
          "enum": "Allgemeine_Landwirtschaftszonen_21.weiterer_Zonentyp_212", 
          "id": 32
        }, 
        {
          "enumtxt": "Speziallandwirtschaftszonen_22.Speziallandwirtschaftszone_221", 
          "enum": "Speziallandwirtschaftszonen_22.Speziallandwirtschaftszone_221", 
          "id": 33
        }, 
        {
          "enumtxt": "Speziallandwirtschaftszonen_22.weiterer_Zonentyp_222", 
          "enum": "Speziallandwirtschaftszonen_22.weiterer_Zonentyp_222", 
          "id": 34
        }, 
        {
          "enumtxt": "Rebbauzonen_23.Rebbauzone_231", 
          "enum": "Rebbauzonen_23.Rebbauzone_231", 
          "id": 35
        }, 
        {
          "enumtxt": "Rebbauzonen_23.weiterer_Zonentyp_232", 
          "enum": "Rebbauzonen_23.weiterer_Zonentyp_232", 
          "id": 36
        }, 
        {
          "enumtxt": "Schutzzonen_fuer_Lebensraeume_und_Landschaften_31.allgemeine_Schutzzone_311", 
          "enum": "Schutzzonen_fuer_Lebensraeume_und_Landschaften_31.allgemeine_Schutzzone_311", 
          "id": 37
        }, 
        {
          "enumtxt": "Schutzzonen_fuer_Lebensraeume_und_Landschaften_31.Naturschutzzone_kommunal_312", 
          "enum": "Schutzzonen_fuer_Lebensraeume_und_Landschaften_31.Naturschutzzone_kommunal_312", 
          "id": 38
        }, 
        {
          "enumtxt": "Schutzzonen_fuer_Lebensraeume_und_Landschaften_31.Naturschutzzone_kantonal_313", 
          "enum": "Schutzzonen_fuer_Lebensraeume_und_Landschaften_31.Naturschutzzone_kantonal_313", 
          "id": 39
        }, 
        {
          "enumtxt": "Schutzzonen_fuer_Lebensraeume_und_Landschaften_31.weiterer_Zonentyp_314", 
          "enum": "Schutzzonen_fuer_Lebensraeume_und_Landschaften_31.weiterer_Zonentyp_314", 
          "id": 40
        }, 
        {
          "enumtxt": "Zonen_fuer_Baeche_Fluesse_Seen_und_ihre_Ufer_32.Gewaesserzone_321", 
          "enum": "Zonen_fuer_Baeche_Fluesse_Seen_und_ihre_Ufer_32.Gewaesserzone_321", 
          "id": 41
        }, 
        {
          "enumtxt": "Zonen_fuer_Baeche_Fluesse_Seen_und_ihre_Ufer_32.weiterer_Zonentyp_322", 
          "enum": "Zonen_fuer_Baeche_Fluesse_Seen_und_ihre_Ufer_32.weiterer_Zonentyp_322", 
          "id": 42
        }, 
        {
          "enumtxt": "weitere_Zonen_nach_Art18_Abs1_RPG_41.Zone_unkultivierbares_Land_411", 
          "enum": "weitere_Zonen_nach_Art18_Abs1_RPG_41.Zone_unkultivierbares_Land_411", 
          "id": 43
        }, 
        {
          "enumtxt": "weitere_Zonen_nach_Art18_Abs1_RPG_41.Strassenareal_412", 
          "enum": "weitere_Zonen_nach_Art18_Abs1_RPG_41.Strassenareal_412", 
          "id": 44
        }, 
        {
          "enumtxt": "weitere_Zonen_nach_Art18_Abs1_RPG_41.Bahnareal_413", 
          "enum": "weitere_Zonen_nach_Art18_Abs1_RPG_41.Bahnareal_413", 
          "id": 45
        }, 
        {
          "enumtxt": "weitere_Zonen_nach_Art18_Abs1_RPG_41.Flugplatzareal_414", 
          "enum": "weitere_Zonen_nach_Art18_Abs1_RPG_41.Flugplatzareal_414", 
          "id": 46
        }, 
        {
          "enumtxt": "weitere_Zonen_nach_Art18_Abs1_RPG_41.Abbauzone_415", 
          "enum": "weitere_Zonen_nach_Art18_Abs1_RPG_41.Abbauzone_415", 
          "id": 47
        }, 
        {
          "enumtxt": "weitere_Zonen_nach_Art18_Abs1_RPG_41.Deponiezone_416", 
          "enum": "weitere_Zonen_nach_Art18_Abs1_RPG_41.Deponiezone_416", 
          "id": 48
        }, 
        {
          "enumtxt": "weitere_Zonen_nach_Art18_Abs1_RPG_41.Abbau_und_Deponiezone_417", 
          "enum": "weitere_Zonen_nach_Art18_Abs1_RPG_41.Abbau_und_Deponiezone_417", 
          "id": 49
        }, 
        {
          "enumtxt": "weitere_Zonen_nach_Art18_Abs1_RPG_41.weiterer_Zonentyp_418", 
          "enum": "weitere_Zonen_nach_Art18_Abs1_RPG_41.weiterer_Zonentyp_418", 
          "id": 50
        }, 
        {
          "enumtxt": "weitere_Zonen_nach_Art18_Abs2_RPG_42.Reservezone_421", 
          "enum": "weitere_Zonen_nach_Art18_Abs2_RPG_42.Reservezone_421", 
          "id": 51
        }, 
        {
          "enumtxt": "weitere_Zonen_nach_Art18_Abs2_RPG_42.weiterer_Zonentyp_422", 
          "enum": "weitere_Zonen_nach_Art18_Abs2_RPG_42.weiterer_Zonentyp_422", 
          "id": 52
        }, 
        {
          "enumtxt": "Waldzonen_43.Wald_431", 
          "enum": "Waldzonen_43.Wald_431", 
          "id": 53
        }, 
        {
          "enumtxt": "Waldzonen_43.weiterer_Zonentyp_432", 
          "enum": "Waldzonen_43.weiterer_Zonentyp_432", 
          "id": 54
        }, 
        {
          "enumtxt": "Zonen_fuer_Kleinsiedlung_44.Weilerzone_441", 
          "enum": "Zonen_fuer_Kleinsiedlung_44.Weilerzone_441", 
          "id": 55
        }, 
        {
          "enumtxt": "Zonen_fuer_Kleinsiedlung_44.weiterer_Zonentyp_442", 
          "enum": "Zonen_fuer_Kleinsiedlung_44.weiterer_Zonentyp_442", 
          "id": 56
        }
      ]
    }, 
    "enum34_ueberl_zonen_ch": {
      "src_name": "Nutzungsplanung.Ueberl_Zonen_CH", 
      "values": [
        {
          "enumtxt": "ueberlagernde_Schutzzonen_61", 
          "enum": "ueberlagernde_Schutzzonen_61", 
          "id": 0
        }, 
        {
          "enumtxt": "ueberlagernde_Nutzungszonen_62", 
          "enum": "ueberlagernde_Nutzungszonen_62", 
          "id": 1
        }, 
        {
          "enumtxt": "ueberlagernde_Gefahrenzonen_63", 
          "enum": "ueberlagernde_Gefahrenzonen_63", 
          "id": 2
        }, 
        {
          "enumtxt": "ueberlagernde_Flaechenfestlegungen_64", 
          "enum": "ueberlagernde_Flaechenfestlegungen_64", 
          "id": 3
        }
      ]
    }, 
    "enum16_hauptnutzung_ch": {
      "src_name": "Nutzungsplanung.Nutzungsplanung.Grundnutzung_Zonentyp_Kt.Hauptnutzung_CH", 
      "values": [
        {
          "enumtxt": "Bauzonen_1.Wohnzonen_11", 
          "enum": "Bauzonen_1.Wohnzonen_11", 
          "id": 0
        }, 
        {
          "enumtxt": "Bauzonen_1.Arbeitszonen_12", 
          "enum": "Bauzonen_1.Arbeitszonen_12", 
          "id": 1
        }, 
        {
          "enumtxt": "Bauzonen_1.Mischzonen_13", 
          "enum": "Bauzonen_1.Mischzonen_13", 
          "id": 2
        }, 
        {
          "enumtxt": "Bauzonen_1.Zentrumszonen_14", 
          "enum": "Bauzonen_1.Zentrumszonen_14", 
          "id": 3
        }, 
        {
          "enumtxt": "Bauzonen_1.Zonen_fuer_oeffentliche_Nutzungen_15", 
          "enum": "Bauzonen_1.Zonen_fuer_oeffentliche_Nutzungen_15", 
          "id": 4
        }, 
        {
          "enumtxt": "Bauzonen_1.eingeschraenkte_Bauzonen_16", 
          "enum": "Bauzonen_1.eingeschraenkte_Bauzonen_16", 
          "id": 5
        }, 
        {
          "enumtxt": "Bauzonen_1.Tourismus_und_Freizeitzonen_17", 
          "enum": "Bauzonen_1.Tourismus_und_Freizeitzonen_17", 
          "id": 6
        }, 
        {
          "enumtxt": "Bauzonen_1.Verkehrszonen_innerhalbBauzonen_18", 
          "enum": "Bauzonen_1.Verkehrszonen_innerhalbBauzonen_18", 
          "id": 7
        }, 
        {
          "enumtxt": "Bauzonen_1.weitere_Zonen_19", 
          "enum": "Bauzonen_1.weitere_Zonen_19", 
          "id": 8
        }, 
        {
          "enumtxt": "Landwirtschaftszonen_2.allgemeine_Landwirtschaftszonen_21", 
          "enum": "Landwirtschaftszonen_2.allgemeine_Landwirtschaftszonen_21", 
          "id": 9
        }, 
        {
          "enumtxt": "Landwirtschaftszonen_2.Speziallandwirtschaftszonen_22", 
          "enum": "Landwirtschaftszonen_2.Speziallandwirtschaftszonen_22", 
          "id": 10
        }, 
        {
          "enumtxt": "Landwirtschaftszonen_2.Rebbauzonen_23", 
          "enum": "Landwirtschaftszonen_2.Rebbauzonen_23", 
          "id": 11
        }, 
        {
          "enumtxt": "Schutzzonen_3.Schutzzonen_fuer_Lebensraeume_und_Landschaften_31", 
          "enum": "Schutzzonen_3.Schutzzonen_fuer_Lebensraeume_und_Landschaften_31", 
          "id": 12
        }, 
        {
          "enumtxt": "Schutzzonen_3.Zonen_fuer_Baeche_Fluesse_Seen_und_ihre_Ufer_32", 
          "enum": "Schutzzonen_3.Zonen_fuer_Baeche_Fluesse_Seen_und_ihre_Ufer_32", 
          "id": 13
        }, 
        {
          "enumtxt": "weitere_Zonen_4.weitere_Zonen_ausserhalbBauzonen_41", 
          "enum": "weitere_Zonen_4.weitere_Zonen_ausserhalbBauzonen_41", 
          "id": 14
        }, 
        {
          "enumtxt": "weitere_Zonen_4.weitere_Zonen_Reservezonen_42", 
          "enum": "weitere_Zonen_4.weitere_Zonen_Reservezonen_42", 
          "id": 15
        }, 
        {
          "enumtxt": "weitere_Zonen_4.Waldzonen_43", 
          "enum": "weitere_Zonen_4.Waldzonen_43", 
          "id": 16
        }, 
        {
          "enumtxt": "weitere_Zonen_4.Zonen_fuer_Kleinsiedlung_44", 
          "enum": "weitere_Zonen_4.Zonen_fuer_Kleinsiedlung_44", 
          "id": 17
        }
      ]
    }, 
    "enum35_qualitaet": {
      "src_name": "Nutzungsplanung.Nutzungsplanung.Objektbezogene_Festlegung.Qualitaet", 
      "values": [
        {
          "enumtxt": "AV93", 
          "enum": "AV93", 
          "id": 0
        }, 
        {
          "enumtxt": "PV74", 
          "enum": "PV74", 
          "id": 1
        }, 
        {
          "enumtxt": "PN", 
          "enum": "PN", 
          "id": 2
        }, 
        {
          "enumtxt": "weitere", 
          "enum": "weitere", 
          "id": 3
        }
      ]
    }, 
    "enum20_geometrie_grundlage": {
      "src_name": "Nutzungsplanung.Geometrie_Grundlage", 
      "values": [
        {
          "enumtxt": "AV93", 
          "enum": "AV93", 
          "id": 0
        }, 
        {
          "enumtxt": "PV74", 
          "enum": "PV74", 
          "id": 1
        }, 
        {
          "enumtxt": "PN", 
          "enum": "PN", 
          "id": 2
        }, 
        {
          "enumtxt": "weitere", 
          "enum": "weitere", 
          "id": 3
        }
      ]
    }, 
    "enum10_hauptnutzung_ch": {
      "src_name": "Nutzungsplanung.Hauptnutzung_CH", 
      "values": [
        {
          "enumtxt": "Bauzonen_1.Wohnzonen_11", 
          "enum": "Bauzonen_1.Wohnzonen_11", 
          "id": 0
        }, 
        {
          "enumtxt": "Bauzonen_1.Arbeitszonen_12", 
          "enum": "Bauzonen_1.Arbeitszonen_12", 
          "id": 1
        }, 
        {
          "enumtxt": "Bauzonen_1.Mischzonen_13", 
          "enum": "Bauzonen_1.Mischzonen_13", 
          "id": 2
        }, 
        {
          "enumtxt": "Bauzonen_1.Zentrumszonen_14", 
          "enum": "Bauzonen_1.Zentrumszonen_14", 
          "id": 3
        }, 
        {
          "enumtxt": "Bauzonen_1.Zonen_fuer_oeffentliche_Nutzungen_15", 
          "enum": "Bauzonen_1.Zonen_fuer_oeffentliche_Nutzungen_15", 
          "id": 4
        }, 
        {
          "enumtxt": "Bauzonen_1.eingeschraenkte_Bauzonen_16", 
          "enum": "Bauzonen_1.eingeschraenkte_Bauzonen_16", 
          "id": 5
        }, 
        {
          "enumtxt": "Bauzonen_1.Tourismus_und_Freizeitzonen_17", 
          "enum": "Bauzonen_1.Tourismus_und_Freizeitzonen_17", 
          "id": 6
        }, 
        {
          "enumtxt": "Bauzonen_1.Verkehrszonen_innerhalbBauzonen_18", 
          "enum": "Bauzonen_1.Verkehrszonen_innerhalbBauzonen_18", 
          "id": 7
        }, 
        {
          "enumtxt": "Bauzonen_1.weitere_Zonen_19", 
          "enum": "Bauzonen_1.weitere_Zonen_19", 
          "id": 8
        }, 
        {
          "enumtxt": "Landwirtschaftszonen_2.allgemeine_Landwirtschaftszonen_21", 
          "enum": "Landwirtschaftszonen_2.allgemeine_Landwirtschaftszonen_21", 
          "id": 9
        }, 
        {
          "enumtxt": "Landwirtschaftszonen_2.Speziallandwirtschaftszonen_22", 
          "enum": "Landwirtschaftszonen_2.Speziallandwirtschaftszonen_22", 
          "id": 10
        }, 
        {
          "enumtxt": "Landwirtschaftszonen_2.Rebbauzonen_23", 
          "enum": "Landwirtschaftszonen_2.Rebbauzonen_23", 
          "id": 11
        }, 
        {
          "enumtxt": "Schutzzonen_3.Schutzzonen_fuer_Lebensraeume_und_Landschaften_31", 
          "enum": "Schutzzonen_3.Schutzzonen_fuer_Lebensraeume_und_Landschaften_31", 
          "id": 12
        }, 
        {
          "enumtxt": "Schutzzonen_3.Zonen_fuer_Baeche_Fluesse_Seen_und_ihre_Ufer_32", 
          "enum": "Schutzzonen_3.Zonen_fuer_Baeche_Fluesse_Seen_und_ihre_Ufer_32", 
          "id": 13
        }, 
        {
          "enumtxt": "weitere_Zonen_4.weitere_Zonen_ausserhalbBauzonen_41", 
          "enum": "weitere_Zonen_4.weitere_Zonen_ausserhalbBauzonen_41", 
          "id": 14
        }, 
        {
          "enumtxt": "weitere_Zonen_4.weitere_Zonen_Reservezonen_42", 
          "enum": "weitere_Zonen_4.weitere_Zonen_Reservezonen_42", 
          "id": 15
        }, 
        {
          "enumtxt": "weitere_Zonen_4.Waldzonen_43", 
          "enum": "weitere_Zonen_4.Waldzonen_43", 
          "id": 16
        }, 
        {
          "enumtxt": "weitere_Zonen_4.Zonen_fuer_Kleinsiedlung_44", 
          "enum": "weitere_Zonen_4.Zonen_fuer_Kleinsiedlung_44", 
          "id": 17
        }
      ]
    }
  }, 
  "dst_format": "PostgreSQL"
}"""
    print cfgjson
    assert cfgjson == expected


def test_layer_info():
    cfg = OgrConfig(ds="./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd")
    assert not cfg.is_loaded()
    assert cfg.layer_names() == []
    assert cfg.layer_infos() == []

    cfg.generate_config(dst_format='PostgreSQL')
    assert cfg.is_loaded()
    print cfg.layer_names()
    assert "roadsexdm2ien_roadsextended_roadsign" in cfg.layer_names()

    print cfg.layer_infos()
    #assert {'name': 'roadsexdm2ien_roadsextended_roadsign', 'geom_field': 'position'} in cfg.layer_infos()
    assert {'name': 'roadsexdm2ien_roadsextended_roadsign', 'geom_field': 'wkb_geometry'} in cfg.layer_infos()
    assert {'name': 'roadsexdm2ben_roads_lattrs'} in cfg.layer_infos()


def test_enums():
    cfg = OgrConfig(ds="./tests/data/ili/roads23.xtf,./tests/data/ili/RoadsExdm2ien.imd", model="./tests/data/ili/RoadsExdm2ien.imd")
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

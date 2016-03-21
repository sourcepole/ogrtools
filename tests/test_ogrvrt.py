from ogrtools.pyogr.ogrvrt import ogr2vrt


def test_ogrvrt():
    expected = """<OGRVRTDataSource>
  <OGRVRTLayer name="railway">
    <SrcDataSource relativeToVRT="0" shared="1">tests/data/osm/railway.shp</SrcDataSource>
    <SrcLayer>railway</SrcLayer>
    <GeometryType>wkbLineString</GeometryType>
    <LayerSRS>GEOGCS[&quot;GCS_WGS_1984&quot;,DATUM[&quot;WGS_1984&quot;,SPHEROID[&quot;WGS_84&quot;,6378137,298.257223563]],PRIMEM[&quot;Greenwich&quot;,0],UNIT[&quot;Degree&quot;,0.017453292519943295]]</LayerSRS>
    <Field name="type" type="String" src="type" width="255"/>
    <Field name="osm_id" type="Integer64" src="osm_id" width="11"/>
    <Field name="lastchange" type="Date" src="lastchange" width="10"/>
    <Field name="name" type="String" src="name" width="255"/>
    <Field name="keyvalue" type="String" src="keyvalue" width="80"/>
  </OGRVRTLayer>
</OGRVRTDataSource>
"""
    vrt = ogr2vrt(infile="tests/data/osm/railway.shp")
    print vrt
    assert vrt == expected

# Layer join test:
# <OGRVRTDataSource>
#   <OGRVRTLayer name="BoFlaechenJoined">
#     <SrcDataSource>data/ili/Beispiel.itf,data/ili/Beispiel.imd</SrcDataSource>
#     <SrcSQL>SELECT Bodenbedeckung__BoFlaechen.*, enumXX_Art.value FROM Bodenbedeckung__BoFlaechen LEFT JOIN enumXX_Art ON Bodenbedeckung__BoFlaechen.Art = enumXX_Art.id </SrcSQL>
#   </OGRVRTLayer>
# </OGRVRTDataSource>

ogrtools
========


Introduction
------------

ogrtools is a collection of libraries and tools built with the Python API of [OGR](http://www.gdal.org/ogr/).


pyogr library
-------------

pyogr gives you OGR commands like ogr2ogr or ogrinfo as Python library, i.e. without calling an external executable file. Most of the code is already included in the OGR source distribution as samples for using the Python API.

* ogr2ogr.py: ogr2ogr call with stdout/stderr redirection
* ogrinfo.py: ogrinfo call
* ogrvrt.py: generate a VRT from a datasource
* ogrds.py: Call OGR SQL commands on a datasource


interlis library
----------------

Extensions for the OGR [Interlis driver](http://www.gdal.org/ogr/drv_ili.html).

* Loading Interlis models from model repositories
* Automatic detection of used model
* Extracting enums from IlisMeta model


ogrtransform library
--------------------

OGR has many options to transform data when convertion from one format into an other. The ogrtransform library uses a specification in JSON format to transform data.

Example:

```
{
  "comment": "// OGR transformation specification", 
  "layers": {
    "roadsexdm2ben_roads_streetnameposition": {
      "fields": {
        "street": {
          "src": "Street", 
          "type": "String"
        }, 
        "namori": {
          "src": "NamOri", 
          "type": "String"
        }
      }, 
      "geometry_type": "Point", 
      "src_layer": "RoadsExdm2ben.Roads.StreetNamePosition"
    }, 
    "roadsexdm2ben_roads_streetaxis": {
      "fields": {
        "street": {
          "src": "Street", 
          "type": "String"
        }
      }, 
      "geometry_type": "Line", 
      "src_layer": "RoadsExdm2ben.Roads.StreetAxis"
    }, 
  }, 
  "enums": {
    "enum6_Type": {
      "src_name": "RoadsExdm2ien.RoadsExtended.RoadSign.Type", 
      "values": [
        {
          "enumtxt": "prohibition.noentry", 
          "enum": "prohibition.noentry", 
          "id": 0
        }, 
        {
          "enumtxt": "prohibition.noparking", 
          "enum": "prohibition.noparking", 
          "id": 1
        }, 
        {
          "enumtxt": "prohibition.other", 
          "enum": "prohibition.other", 
          "id": 2
        }
      ]
    }
  }
}
```

ogr command line tool
---------------------

The ogr command line tool exposes ogrtools functionality for using in a command shell.

```
ogr --help
usage: ogr [-h] {version,formats,info,sql,vrt,genspec} ...

Query and transform OGR compatible vector data

optional arguments:
  -h, --help            show this help message and exit

commands:
  valid commands

  {version,formats,info,sql,vrt,genspec,transform}
    version             Show version information
    formats             List available data formats
    info                Information about data
    sql                 Execute SQL Query
    vrt                 Create VRT from data source
    genspec             Generate transormation specification from data source
    transform           Transform data source based on transformation
                        specification
```

### ogr version

Show version information

```
usage: ogr version [-h]
```

### ogr formats

List available data formats

```
usage: ogr formats [-h]
```

### ogr info

Information about data

```
usage: ogr info [-h] source [layers [layers ...]]
```

Example:
```
ogr info tests/data/railway.shp
```
```
INFO: Open of `tests/data/railway.shp'
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
```

### ogr sql

Execute SQL Query

```
usage: ogr sql [-h] source sql-query
```

Example:
```
ogr sql tests/data/railway.shp "SELECT type,osm_id,lastchange FROM railway WHERE lastchange < '2008/04/01'"
```
```
INFO: Open of `tests/data/railway.shp'
      using driver `ESRI Shapefile' successful.

Layer name: railway
Geometry: Line String
Feature Count: 8
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
OGRFeature(railway):6
  type (String) = rail
  osm_id (Real) = 9675696
  lastchange (Date) = 2007/10/17
  LINESTRING (9.6174755 47.227974,9.6170635 47.22802)

OGRFeature(railway):8
  type (String) = rail
  osm_id (Real) = 9675711
  lastchange (Date) = 2007/10/17
  LINESTRING (9.617415 47.22794,9.617038 47.227985)
...
```

### ogr vrt

Create VRT from data source

```
usage: ogr vrt [-h] source [layers [layers ...]]
```

Example:
```
ogr vrt tests/data/railway.shp
```
```
<OGRVRTDataSource>
  <OGRVRTLayer name="railway">
    <SrcDataSource relativeToVRT="0" shared="1">tests/data/railway.shp</SrcDataSource>
    <SrcLayer>railway</SrcLayer>
    <GeometryType>wkbLineString</GeometryType>
    <LayerSRS>GEOGCS[&quot;GCS_WGS_1984&quot;,DATUM[&quot;WGS_1984&quot;,SPHEROID[&quot;WGS_84&quot;,6378137,298.257223563]],PRIMEM[&quot;Greenwich&quot;,0],UNIT[&quot;Degree&quot;,0.017453292519943295]]</LayerSRS>
    <Field name="type" type="String" src="type" width="255"/>
    <Field name="osm_id" type="Real" src="osm_id" width="11"/>
    <Field name="lastchange" type="Date" src="lastchange" width="10"/>
    <Field name="name" type="String" src="name" width="255"/>
    <Field name="keyvalue" type="String" src="keyvalue" width="80"/>
  </OGRVRTLayer>
</OGRVRTDataSource>
```

### ogr genspec

Generate transormation specification from data source

```
usage: ogr genspec [-h] [--model MODEL] source [layers [layers ...]]
```

Example:
```
ogr genspec tests/data/railway.shp
```
```
{
  "comment": "// OGR transformation specification", 
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
  }
}
```

### ogr transform

Transform data source based on transformation specification

```
usage: ogr transform [-h] [--format FORMAT] [--spec SPEC]
                     [dest] source [layers [layers ...]]
```

Example:
```
ogr transform roads.sqlite RoadsExdm2ien.xml --format=SQLite --spec=roads.spec
```


ogrprocessing QGIS plugin
-------------------------

Provides OGR functionality as QGIS SEXTANTE plugin. It was published for QGIS 1.8 and is now included into the core processing algorithms of QGIS 2.0.


License
-------

ogrtools is Copyright © 2013 Sourceepole AG. It is free software, and may be redistributed under the terms specified in the MIT-LICENSE file.

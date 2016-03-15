ogrtools
========

Introduction
------------

ogrtools is a collection of libraries and tools built with the Python
API of `OGR <http://www.gdal.org/ogr/>`__.

pyogr library
-------------

pyogr gives you OGR commands like ogr2ogr or ogrinfo as Python library,
i.e. without calling an external executable file. Most of the code is
already included in the OGR source distribution as samples for using the
Python API.

-  ogr2ogr.py: ogr2ogr call with stdout/stderr redirection
-  ogrinfo.py: ogrinfo call
-  ogrvrt.py: generate a VRT from a datasource
-  ogrds.py: Call OGR SQL commands on a datasource

interlis library
----------------

Extensions for the OGR `Interlis
driver <http://www.gdal.org/ogr/drv_ili.html>`__.

-  Automatic detection of used models in transfer files
-  Extracting enums from IlisMeta model
-  Loading and converting of Interlis models from model repositories

ogrtransform library
--------------------

OGR has many options to transform data when converting from one format
into an other. The ogrtransform library uses a configuration in JSON
format to transform data.

Example:

::

    {
      "//": "OGR transformation configuration", 
      "src_format": "Interlis 2", 
      "dst_format": "PostgreSQL",
      "dst_dsco": {}, 
      "dst_lco": {
        "SCHEMA": "public"
      }, 
      "layers": {
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
        "roadsexdm2ben_roads_streetaxis": {
          "fields": {
            "tid": {
              "src": "TID", 
              "type": "String"
            }, 
            "street": {
              "src": "Street", 
              "type": "String"
            }
          }, 
          "geometry_type": "MultiLineString", 
          "src_layer": "RoadsExdm2ben.Roads.StreetAxis", 
          "geom_fields": {
            "geometry": {
              "src": "Geometry", 
              "type": "MultiLineString"
            }
          }
        }
      }, 
      "enums": {
        "enum0_type": {
          "src_name": "RoadsExdm2ben.Roads.RoadSign.Type", 
          "values": [
            {
              "enumtxt": "prohibition", 
              "enum": "prohibition", 
              "id": 0
            }, 
            {
              "enumtxt": "indication", 
              "enum": "indication", 
              "id": 1
            }, 
            {
              "enumtxt": "danger", 
              "enum": "danger", 
              "id": 2
            }, 
            {
              "enumtxt": "velocity", 
              "enum": "velocity", 
              "id": 3
            }
          ]
        }
      }
    }

See `Wiki <https://github.com/sourcepole/ogrtools/wiki>`__ for more
information.

ogr command line tool
---------------------

The ogr command line tool exposes ogrtools functionality for using in a
command shell.

::

    ogr --help
    usage: ogr [-h]
               {version,formats,info,sql,vrt,genconfig,write-enums,transform} ...

    Query and transform OGR compatible vector data

    optional arguments:
      -h, --help            show this help message and exit

    commands:
      valid commands

      {version,formats,info,sql,vrt,genconfig,write-enums,transform}
        version             Show version information
        formats             List available data formats
        info                Information about data
        sql                 Execute SQL Query
        vrt                 Create VRT from data source
        genconfig           Generate OGR configuration from data source
        write-enums         Write tables with enumeration values
        transform           Transform data source based on OGR configuration

ogr version
~~~~~~~~~~~

Show version information

::

    usage: ogr version [-h]

ogr formats
~~~~~~~~~~~

List available data formats

::

    usage: ogr formats [-h]

ogr info
~~~~~~~~

Information about data

::

    usage: ogr info [-h] source [layers [layers ...]]

Example:

::

    ogr info tests/data/osm/railway.shp

::

    INFO: Open of `tests/data/osm/railway.shp'
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

ogr sql
~~~~~~~

Execute SQL Query

::

    usage: ogr sql [-h] source sql-query

Example:

::

    ogr sql tests/data/osm/railway.shp "SELECT type,osm_id,lastchange FROM railway WHERE lastchange < '2008/04/01'"

::

    INFO: Open of `tests/data/osm/railway.shp'
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

ogr vrt
~~~~~~~

Create VRT from data source

::

    usage: ogr vrt [-h] source [layers [layers ...]]

Example:

::

    ogr vrt tests/data/osm/railway.shp

::

    <OGRVRTDataSource>
      <OGRVRTLayer name="railway">
        <SrcDataSource relativeToVRT="0" shared="1">tests/data/osm/railway.shp</SrcDataSource>
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

ogr genconfig
~~~~~~~~~~~~~

Generate transormation specification from data source

::

    usage: ogr genconfig [-h] [--format FORMAT] [--model MODEL]
                       source [layers [layers ...]]

Example:

::

    ogr genconfig --format=PostgreSQL tests/data/osm/railway.shp

::

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

ogr write-enums
~~~~~~~~~~~~~~~

Write tables with enumeration values

::

    usage: ogr write-enums [-h] [--debug] [--format FORMAT] [--config CONFIG]
                           [dest]

    positional arguments:
      dest             output datasource

    optional arguments:
      -h, --help       show this help message and exit
      --debug          Display debugging information
      --format FORMAT  Destination format
      --config CONFIG  OGR configuration

Example:

::

    ogr write-enums --config=roads.cfg "PG:dbname=ogrili"

ogr transform
~~~~~~~~~~~~~

Transform data source based on transformation configuration

::

    usage: ogr transform [-h] [--debug] [--reverse] [--format FORMAT]
                         [--config CONFIG]
                         [dest] source [layers [layers ...]]

    positional arguments:
      dest             output datasource
      source           input datasource
      layers           layer names

    optional arguments:
      -h, --help       show this help message and exit
      --debug          Display debugging information
      --reverse        Reverse transformation
      --format FORMAT  Destination format
      --config CONFIG  OGR configuration

Example:

::

    ogr transform --config=roads.cfg "PG:dbname=ogrili" RoadsExdm2ien.xml

From Interlis to GML:

::

    ogr transform --format GML --config tests/data/ili/RoadsExdm2ien.cfg tests/data/ili/RoadsExdm2ien.gml tests/data/ili/roads23.xtf,tests/data/ili/RoadsExdm2ien.imd

Back to Interlis:

::

    ogr transform --reverse --config tests/data/ili/RoadsExdm2ien.cfg /tmp/roads23_from_gml.xtf,tests/data/ili/RoadsExdm2ien.imd tests/data/ili/RoadsExdm2ien.gml

ogrprocessing QGIS plugin
-------------------------

Provides OGR functionality as QGIS SEXTANTE plugin. It was published for
QGIS 1.8 and is now included in the core processing algorithms of QGIS
2.0.

Interlis QGIS plugin
--------------------

GUI for importing and exporting Interlis data with OGR/ogrtools.
Includes Python libraries for easy installation. Currently tested with
QGIS 2.0.

Development
-----------

::

    git clone https://github.com/sourcepole/ogrtools.git

Running tests:

::

    apt-get install python-nose

::

    nosetests

For running ogr commands from source tree:

::

    alias ogr="PYTHONPATH=$(pwd) $(pwd)/ogr_cli/ogr.py"

License
-------

ogrtools is Copyright © 2012-2015 Sourcepole AG. It is free software,
and may be redistributed under the terms specified in the LICENSE.txt
file.

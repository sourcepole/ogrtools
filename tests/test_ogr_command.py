import os


#Run with nosetests tests/test_ogr_command.py --nocapture
def test_generate_usage_markdown():
    ogr_help = os.popen("PYTHONPATH=lib bin/ogr --help").read()
    ogr_write_enums = os.popen("PYTHONPATH=lib bin/ogr write-enums -h").read()
    ogr_transform = os.popen("PYTHONPATH=lib bin/ogr transform -h").read()
    vrt = os.popen("PYTHONPATH=lib bin/ogr vrt tests/data/osm/railway.shp 2>&1").read()
    config_example = """{
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
}"""
    template = """
ogr command line tool
---------------------

The ogr command line tool exposes ogrtools functionality for using in a command shell.

```
ogr --help
{ogr_help}
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
{vrt}
```

### ogr genconfig

Generate transormation specification from data source

```
usage: ogr genconfig [-h] [--format FORMAT] [--model MODEL]
                   source [layers [layers ...]]
```

Example:
```
ogr genconfig --format=PostgreSQL tests/data/railway.shp
```
```
{config_example}
```

### ogr write-enums

Write tables with enumeration values

```
{ogr_write_enums}
```

Example:
```
ogr write-enums --config=roads.cfg "PG:dbname=ogrili"
```

### ogr transform

Transform data source based on transformation configuration

```
{ogr_transform}
```

Example:
```
ogr transform --config=roads.cfg "PG:dbname=ogrili" RoadsExdm2ien.xml
```"""
    print template.format(ogr_help=ogr_help,
        vrt=vrt,
        config_example=config_example,
        ogr_write_enums=ogr_write_enums,
        ogr_transform=ogr_transform
    )

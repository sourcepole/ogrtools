#http://docs.python.org/library/xml.etree.elementtree.html
import xml.etree.ElementTree as xml
from xml.dom import minidom
import string

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = xml.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
    
#
tree = xml.parse("/home/pi/Dropbox/Projects/geosummit/workshop/NP_73_CH_de_ili2.imd")
#Extract default namespace from root e.g. {http://www.interlis.ch/INTERLIS2.3}TRANSFER
#ns = tree.getroot().tag
ns = "http://www.interlis.ch/INTERLIS2.3"

models = tree.findall("{%s}DATASECTION/{%s}IlisMeta07.ModelData" % (ns, ns))
if models != None:
    #GML output
    gml = xml.Element('FeatureCollection')
    gml.set('xmlns', 'http://ogr.maptools.org/')
    gml.set('xmlns:gml', 'http://www.opengis.net/gml')
    #<ogr:FeatureCollection
    #     xmlns:ogr="http://ogr.maptools.org/"
    #     xmlns:gml="http://www.opengis.net/gml">

    for model in models:
        enumNodes = model.findall("{%s}IlisMeta07.ModelData.EnumNode" % ns)

        if enumNodes != None:
            curEnum = None
            curEnumName = None
            idx = None
            for enumNode in enumNodes:
                parent = enumNode.find("{%s}ParentNode" % ns)
                if parent == None:
                    curEnum = enumNode
                    #Remove trailing .TOP or .TYPE
                    curEnumName = string.replace(curEnum.get("TID"), '.TOP', '')
                    curEnumName = string.replace(curEnumName, '.TYPE', '')
                    idx = 0
                else:
                    #  <gml:featureMember>
                    #    <ogr:Grundzonen__GrundZonenCode__ZonenArt>
                    #      <ogr:value>Dorfkernzone</ogr:value><ogr:id>0</ogr:id>
                    #    </ogr:Grundzonen__GrundZonenCode__ZonenArt>
                    #  </gml:featureMember>
                    featureMember = xml.SubElement(gml, "gml:featureMember")
                    feat = xml.SubElement(featureMember, curEnumName)
                    value = xml.SubElement(feat, "value")
                    value.text = string.replace(enumNode.get("TID"), curEnum.get("TID")+'.', '')
                    id = xml.SubElement(feat, "id")
                    id.text = str(idx)
                    idx = idx + 1
        

file = open("/tmp/enums.gml", 'w')
#xml.ElementTree(gml).write(file, xml_declaration=True, encoding="utf-8")
file.write( prettify(gml) )
file.close()

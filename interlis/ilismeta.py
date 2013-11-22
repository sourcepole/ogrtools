from IliUtils import IliUtils
from xml.etree import ElementTree
from xml.dom import minidom
import string
import sys


def prettify(rawxml, indent="  "):
    """Return a pretty-printed XML string
    """
    reparsed = minidom.parseString(rawxml)
    return reparsed.toprettyxml(indent)

def extract_enums_asgml(fn):
    """Extract Interlis Enumerations as GML
    """
    tree = ElementTree.parse(fn)
    #Extract default namespace from root e.g. {http://www.interlis.ch/INTERLIS2.3}TRANSFER
    #ns = tree.getroot().tag
    ns = "http://www.interlis.ch/INTERLIS2.3"

    models = tree.findall("{%s}DATASECTION/{%s}IlisMeta07.ModelData" % (ns, ns))
    if models != None:
        #GML output
        gml = ElementTree.Element('FeatureCollection')
        gml.set('xmlns', 'http://ogr.maptools.org/')
        gml.set('xmlns:gml', 'http://www.opengis.net/gml')
        #<ogr:FeatureCollection
        #     xmlns:ogr="http://ogr.maptools.org/"
        #     xmlns:gml="http://www.opengis.net/gml">

        for model in models:
            enumNodes = model.findall("{%s}IlisMeta07.ModelData.EnumNode" % ns)

            if enumNodes != None:
                #Collect parent enums
                parent_nodes = set()
                for enumNode in enumNodes:
                    parent = enumNode.find("{%s}ParentNode" % ns)
                    if parent != None:
                        parent_nodes.add(parent.get("REF"))

                curEnum = None
                curEnumName = None
                enumIdx = 0
                idx = None
                for enumNode in enumNodes:
                    parent = enumNode.find("{%s}ParentNode" % ns)
                    if parent == None:
                        curEnum = enumNode
                        #enum name should not be longer than 63 chars, which is PG default name limit
                        #Nutzungsplanung.Nutzungsplanung.Grundnutzung_Zonenflaeche.Herkunft.TYPE -> enumXX_herkunft
                        enumTypeName = enumNode.find("{%s}EnumType" % ns).get('REF')
                        enumTypeName = string.replace(enumTypeName, '.TYPE', '')
                        enumTypeName = string.rsplit(enumTypeName,  '.',  maxsplit=1)[-1]
                        curEnumName = "enum%d_%s" % (enumIdx, enumTypeName)
                        enumIdx = enumIdx + 1
                        #curEnumName = curEnum.get("TID")
                        #Remove trailing .TOP or .TYPE
                        #curEnumName = string.replace(curEnumName, '.TOP', '')
                        #curEnumName = string.replace(curEnumName, '.TYPE', '')
                        #curEnumName = string.replace(curEnumName, '.', '__')
                        idx = 0
                    else:
                        if enumNode.get("TID") not in parent_nodes:
                            #  <gml:featureMember>
                            #    <ogr:Grundzonen__GrundZonenCode__ZonenArt>
                            #      <ogr:value>Dorfkernzone</ogr:value><ogr:id>0</ogr:id>
                            #    </ogr:Grundzonen__GrundZonenCode__ZonenArt>
                            #  </gml:featureMember>
                            featureMember = ElementTree.SubElement(gml, "gml:featureMember")
                            feat = ElementTree.SubElement(featureMember, curEnumName)
                            id = ElementTree.SubElement(feat, "id")
                            id.text = str(idx)
                            idx = idx + 1
                            enum = ElementTree.SubElement(feat, "enum")
                            enum.text = string.replace(enumNode.get("TID"), curEnum.get("TID")+'.', '')
                            enumtxt = ElementTree.SubElement(feat, "enumtxt")
                            enumtxt.text = enum.text
    return ElementTree.tostring(gml, 'utf-8')

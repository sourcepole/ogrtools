# -*- coding: utf-8 -*-
"""Interlis Meta Model functions

Extract information from Interlis Meta Models.
"""
from xml.etree import ElementTree
from xml.dom import minidom
import sys
import string

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
                        featureMember = ElementTree.SubElement(gml, "gml:featureMember")
                        feat = ElementTree.SubElement(featureMember, curEnumName)
                        value = ElementTree.SubElement(feat, "value")
                        value.text = string.replace(enumNode.get("TID"), curEnum.get("TID")+'.', '')
                        id = ElementTree.SubElement(feat, "id")
                        id.text = str(idx)
                        idx = idx + 1
    return ElementTree.tostring(gml, 'utf-8')


def main(argv=None):
    if argv is None:
        argv = sys.argv
    gml = extract_enums_asgml(argv[1])
    print prettify(gml)

if __name__ == '__main__':
    main()

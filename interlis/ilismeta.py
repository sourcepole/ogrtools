#!/usr/bin/env python

from xml.etree import ElementTree
from xml.dom import minidom
import json
import string
import re
import sys


def prettify(rawxml, indent="  "):
    """Return a pretty-printed XML string"""
    reparsed = minidom.parseString(rawxml)
    return reparsed.toprettyxml(indent)


def extract_enums_asgml(fn):
    """Extract Interlis Enumerations as GML"""
    tree = ElementTree.parse(fn)
    #Extract default namespace from root e.g. {http://www.interlis.ch/INTERLIS2.3}TRANSFER
    ns = {'xmlns': re.match(r'^{(.+)}', tree.getroot().tag).group(1)}

    models = tree.findall("xmlns:DATASECTION/xmlns:IlisMeta07.ModelData", ns)
    if models is not None:
        #GML output
        gml = ElementTree.Element('FeatureCollection')
        gml.set('xmlns', 'http://ogr.maptools.org/')
        gml.set('xmlns:gml', 'http://www.opengis.net/gml')
        #<ogr:FeatureCollection
        #     xmlns:ogr="http://ogr.maptools.org/"
        #     xmlns:gml="http://www.opengis.net/gml">

        for model in models:
            enumNodes = model.findall("xmlns:IlisMeta07.ModelData.EnumNode", ns)

            if enumNodes is not None:
                #Collect parent enums
                parent_nodes = set()
                for enumNode in enumNodes:
                    parent = enumNode.find("xmlns:ParentNode", ns)
                    if parent is not None:
                        parent_nodes.add(parent.get("REF"))

                curEnum = None
                curEnumName = None
                enumIdx = 0
                idx = None
                for enumNode in enumNodes:
                    parent = enumNode.find("xmlns:ParentNode", ns)
                    if parent is None:
                        curEnum = enumNode
                        #enum name should not be longer than 63 chars, which is PG default name limit
                        #Nutzungsplanung.Nutzungsplanung.Grundnutzung_Zonenflaeche.Herkunft.TYPE -> enumXX_herkunft
                        enumTypeName = enumNode.find("xmlns:EnumType", ns).get('REF')
                        enumTypeName = string.replace(enumTypeName, '.TYPE', '')
                        enumTypeName = string.rsplit(enumTypeName, '.', maxsplit=1)[-1]
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
                            enum.text = string.replace(enumNode.get("TID"), curEnum.get("TID") + '.', '')
                            enumtxt = ElementTree.SubElement(feat, "enumtxt")
                            enumtxt.text = enum.text
    return ElementTree.tostring(gml, 'utf-8')


def extract_enums_json(fn):
    """Extract Interlis Enumerations as JSON"""
    enum_tables = {}
    tree = ElementTree.parse(fn)
    #Extract default namespace from root e.g. {http://www.interlis.ch/INTERLIS2.3}TRANSFER
    ns = {'xmlns': re.match(r'^{(.+)}', tree.getroot().tag).group(1)}

    models = tree.findall("xmlns:DATASECTION/xmlns:IlisMeta07.ModelData", ns)
    if models is not None:

        for model in models:
            enumNodes = model.findall("xmlns:IlisMeta07.ModelData.EnumNode", ns)

            if enumNodes is not None:
                #Collect parent enums
                parent_nodes = set()
                for enumNode in enumNodes:
                    parent = enumNode.find("xmlns:ParentNode", ns)
                    if parent is not None:
                        parent_nodes.add(parent.get("REF"))

                curEnum = None
                idx = None
                for enumNode in enumNodes:
                    parent = enumNode.find("xmlns:ParentNode", ns)
                    if parent is None:
                        curEnum = enumNode
                        enumTypeName = enumNode.find("xmlns:EnumType", ns).get('REF')
                        enumTypeName = string.replace(enumTypeName, '.TYPE', '')
                        enum_table = []
                        enum_tables[enumTypeName] = enum_table
                        idx = 0
                    else:
                        if enumNode.get("TID") not in parent_nodes:
                            enum_record = {}
                            enum_record["id"] = idx  # str(idx)
                            idx = idx + 1
                            enum = string.replace(enumNode.get("TID"), curEnum.get("TID") + '.', '')
                            enum_record["enum"] = enum
                            enum_record["enumtxt"] = enum
                            enum_table.append(enum_record)
    return enum_tables


def nodeid(tid):
    return tid.replace(".", "_")


def imd_to_dot(fn):
    """Generate dot graph from IlisMeta file"""
    tree = ElementTree.parse(fn)
    #Extract default namespace from root e.g. {http://www.interlis.ch/INTERLIS2.3}TRANSFER
    ns = {'xmlns': re.match(r'^{(.+)}', tree.getroot().tag).group(1)}

    print "digraph {"
    models = tree.findall("xmlns:DATASECTION/xmlns:IlisMeta07.ModelData", ns) or []
    modelno = 0
    for model in models:
        bid = nodeid(model.get("BID"))
        if bid == 'MODEL_INTERLIS':
            continue
        print "subgraph {"
        modelno = modelno + 1
        print "node [style=filled,colorscheme=accent8,color={}]".format(modelno)
        for node in model:
            tag = node.tag.replace("{http://www.interlis.ch/INTERLIS2.3}IlisMeta07.ModelData.", "")
            if node.get("TID"):
                tid = nodeid(node.get("TID"))
                name = node.find("xmlns:Name", ns).text
                print tid + ' [label="' + name + "\\n" + tag + '"]'
                for refnode in node.findall("./*[@REF]"):
                    reftag = refnode.tag.replace("{http://www.interlis.ch/INTERLIS2.3}", "")
                    orderpos = refnode.get("ORDER_POS")
                    if orderpos:
                        reftag = reftag + "[{}]".format(orderpos)
                    if reftag != 'ElementInPackage':
                        print tid + " -> " + nodeid(refnode.get("REF")) + ' [label="' + reftag + '"]'
            else:
                relnodes = node.findall("./*[@REF]")
                n1 = nodeid(relnodes[0].get("REF"))
                #l1 = relnodes[0].tag.replace("{http://www.interlis.ch/INTERLIS2.3}", "")
                n2 = nodeid(relnodes[1].get("REF"))
                #l2 = relnodes[1].tag.replace("{http://www.interlis.ch/INTERLIS2.3}", "")
                #print n1 + " -> " + n2 + ' [headlabel="' + l2 + '" taillabel="' + l1 + '" style=dotted]'
                print n1 + " -> " + n2 + ' [label="' + tag + '" style=dotted]'

        print "}"
    print "}"


def main(argv):
    output = argv[1]
    fn = argv[2]
    if output == 'enumgml':
        print prettify(extract_enums_asgml(fn))
    elif output == 'enumjson':
        enum_tables = extract_enums_json(fn)
        print json.dumps(enum_tables, indent=2)
    elif output == 'dot':
        #./ilismeta.py dot ../tests/data/ili/RoadsExdm2ien.imd | dot -Tps >/tmp/imd.ps
        imd_to_dot(fn)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

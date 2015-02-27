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


def nodeid(tid):
    return tid.replace(".", "_")


DISPLAY_ATTRS = {
    # http://www.graphviz.org/content/attrs
    # Nodes
    "Class": "shape=hexagon,width=2.5",
    "AttrOrParam": "shape=box,width=2",
    "EnumNode": "shape=octagon",
    "EnumType": "shape=doubleoctagon",
    # Edges
    "Super": "color=red,fontcolor=red"
}

IGNORED_EDGE_TAGS = ["ElementInPackage", "AllowedInBasket", "AxisSpec", "Unit"]


class ImdParser():

    def __init__(self, fn):
        self._tree = ElementTree.parse(fn)
        # Extract default namespace from root e.g.
        # {http://www.interlis.ch/INTERLIS2.3}TRANSFER
        self._ns = {
            'xmlns': re.match(r'^{(.+)}', self._tree.getroot().tag).group(1)}

    def extract_enums(self):
        """Extract Interlis Enumerations"""
        enum_tables = {}
        self._enum_types = self._tree.findall(
            "xmlns:DATASECTION/xmlns:IlisMeta07.ModelData/xmlns:IlisMeta07.ModelData.EnumType", self._ns)
        self._enum_nodes = self._tree.findall(
            "xmlns:DATASECTION/xmlns:IlisMeta07.ModelData/xmlns:IlisMeta07.ModelData.EnumNode", self._ns)
        if self._enum_nodes is not None:
            # Collect parent enums (only leaf nodes have to be added as enums)
            parent_nodes = set()
            for enumNode in self._enum_nodes:
                parent = enumNode.find("xmlns:ParentNode", self._ns)
                if parent is not None:
                    parent_nodes.add(parent.get("REF"))

            # Collect top self._enum_nodes
            self._top_nodes = {}  # top node => [leaf nodes]
            for enumNode in self._enum_nodes:
                parent = enumNode.find("xmlns:ParentNode", self._ns)
                if parent is None:
                    self._top_nodes[enumNode] = []

            # Collect leafs
            for enumNode in self._enum_nodes:
                top_node = self._find_top_node(enumNode)
                if enumNode.get("TID") not in parent_nodes:
                    leafs = self._top_nodes[top_node]
                    leafs.append(enumNode)

            for top_node in self._top_nodes.keys():
                enum_table = []
                self._collect_enums(top_node, enum_table, 0)
                enumTypeName = top_node.find(
                    "xmlns:EnumType", self._ns).get('REF')
                enumTypeName = string.replace(enumTypeName, '.TYPE', '')
                enum_tables[enumTypeName] = enum_table

        return enum_tables

    def _find_top_node(self, enumNode):
        # <IlisMeta07.ModelData.EnumNode TID="RoadsExdm2ien.RoadsExtended.RoadSign.Type.TYPE.TOP.prohibition.noparking">
        #   <Name>noparking</Name>
        #   <Abstract>false</Abstract>
        #   <Final>false</Final>
        #   <ParentNode REF="RoadsExdm2ien.RoadsExtended.RoadSign.Type.TYPE.TOP.prohibition" ORDER_POS="2" />
        # </IlisMeta07.ModelData.EnumNode>
        if enumNode in self._top_nodes:
            return enumNode
        else:
            parent_tid = enumNode.find("xmlns:ParentNode", self._ns).get('REF')
            for node in self._enum_nodes:
                if parent_tid == node.get('TID'):
                    return self._find_top_node(node)

    def _collect_enums(self, top_node, enum_table, idx):
        """Add leafes of top_node to enum_table"""
        # Find enum type
        enumTypeName = top_node.find("xmlns:EnumType", self._ns).get('REF')
        for node in self._enum_types:
            if enumTypeName == node.get('TID'):
                enumType = node
                break

        # Handle type inheritance
        superRef = enumType.find("xmlns:Super", self._ns)
        if superRef is not None:
            superTypeName = superRef.get('REF')
            for node in self._top_nodes.keys():
                if superTypeName == node.find("xmlns:EnumType", self._ns).get('REF'):
                    idx = self._collect_enums(node, enum_table, idx)
                    break

        # Add leafes
        for enumNode in self._top_nodes[top_node]:
            enum_record = {}
            enum_record["id"] = idx  # str(idx)
            idx = idx + 1
            enum = string.replace(
                enumNode.get("TID"), top_node.get("TID") + '.', '')
            enum_record["enum"] = enum
            enum_record["enumtxt"] = enum
            enum_table.append(enum_record)

        return idx

    def extract_enums_asgml(self):
        """Extract Interlis Enumerations as GML"""
        enum_tables = self.extract_enums()
        # GML output
        gml = ElementTree.Element('FeatureCollection')
        gml.set('xmlns', 'http://ogr.maptools.org/')
        gml.set('xmlns:gml', 'http://www.opengis.net/gml')
        #<ogr:FeatureCollection
        #     xmlns:ogr="http://ogr.maptools.org/"
        #     xmlns:gml="http://www.opengis.net/gml">
        enumIdx = 0
        for name, defs in enum_tables.items():
            # enum name should not be longer than 63 chars, which is PG default name limit
            # Nutzungsplanung.Nutzungsplanung.Grundnutzung_Zonenflaeche.Herkunft.TYPE
            # -> enumXX_herkunft
            enumTypeName = string.rsplit(name, '.', maxsplit=1)[-1]
            curEnumName = "enum%d_%s" % (enumIdx, enumTypeName)
            enumIdx = enumIdx + 1
            for enumdef in defs:
                #  <gml:featureMember>
                #    <ogr:Grundzonen__GrundZonenCode__ZonenArt>
                #      <ogr:value>Dorfkernzone</ogr:value><ogr:id>0</ogr:id>
                #    </ogr:Grundzonen__GrundZonenCode__ZonenArt>
                #  </gml:featureMember>
                featureMember = ElementTree.SubElement(
                    gml, "gml:featureMember")
                feat = ElementTree.SubElement(featureMember, curEnumName)
                id = ElementTree.SubElement(feat, "id")
                id.text = str(enumdef['id'])
                enum = ElementTree.SubElement(feat, "enum")
                enum.text = enumdef['enum']
                enumtxt = ElementTree.SubElement(feat, "enumtxt")
                enumtxt.text = enumdef['enumtxt']

        return ElementTree.tostring(gml, 'utf-8')

    def imd_to_dot(self):
        """Generate dot graph from IlisMeta file"""
        print "digraph {"
        models = self._tree.findall(
            "xmlns:DATASECTION/xmlns:IlisMeta07.ModelData", self._ns) or []
        modelno = 0
        for model in models:
            taggroup = {}
            bid = nodeid(model.get("BID"))
            if bid == 'MODEL_INTERLIS':
                continue
            print "subgraph {"
            modelno = modelno + 1
            print "node [style=filled,colorscheme=accent8,fillcolor={}]".format(modelno)
            for node in model:
                tag = node.tag.replace(
                    "{http://www.interlis.ch/INTERLIS2.3}IlisMeta07.ModelData.", "")

                multistr = ""
                multi = node.find("xmlns:Multiplicity", self._ns)
                if multi is not None:
                    min = ""
                    max = ""
                    minnode = multi.find("./*/xmlns:Min", self._ns)
                    if minnode is not None:
                        min = minnode.text
                    maxnode = multi.find("./*/xmlns:Max", self._ns)
                    if maxnode is not None:
                        max = maxnode.text
                    multistr = " [{min}..{max}]".format(min=min, max=max)

                if node.get("TID"):
                    tid = nodeid(node.get("TID"))
                    name = node.find("xmlns:Name", self._ns).text
                    if tag not in taggroup:
                        taggroup[tag] = []
                    taggroup[tag].append(tid)
                    display_attrs = DISPLAY_ATTRS.get(tag, "")
                    print tid + ' [label="' + name + "\\n" + tag + multistr + '" ' + display_attrs + "]"
                    for refnode in node.findall("./*[@REF]"):
                        reftag = refnode.tag.replace(
                            "{http://www.interlis.ch/INTERLIS2.3}", "")
                        orderpos = refnode.get("ORDER_POS")
                        display_attrs = DISPLAY_ATTRS.get(reftag, "")
                        if orderpos:
                            reftag = reftag + "({})".format(orderpos)
                        if reftag not in IGNORED_EDGE_TAGS:
                            print tid + " -> " + nodeid(refnode.get("REF")) + ' [label="' + reftag + multistr + '" ' + display_attrs + "]"
                else:
                    relnodes = node.findall("./*[@REF]")
                    n1 = nodeid(relnodes[0].get("REF"))
                    #l1 = relnodes[0].tag.replace("{http://www.interlis.ch/INTERLIS2.3}", "")
                    n2 = nodeid(relnodes[1].get("REF"))
                    #l2 = relnodes[1].tag.replace("{http://www.interlis.ch/INTERLIS2.3}", "")
                    # print n1 + " -> " + n2 + ' [headlabel="' + l2 + '"
                    # taillabel="' + l1 + '" style=dotted]'
                    orderpos = relnodes[0].get(
                        "ORDER_POS") or relnodes[1].get("ORDER_POS")
                    if tag not in IGNORED_EDGE_TAGS:
                        if orderpos:
                            tag = tag + "({})".format(orderpos)
                        print n1 + " -> " + n2 + ' [label="' + tag + multistr + '" style=dotted,color=blue,fontcolor=blue]'
            print "{ rank = same; " + ";".join(taggroup["Class"]) + " }"
            if "EnumType" in taggroup:
                print "{ rank = same; " + ";".join(taggroup["EnumType"]) + " }"

            print "}"
        print "}"


def main(argv):
    output = argv[1]
    fn = argv[2]
    parser = ImdParser(fn)
    if output == 'enumgml':
        print prettify(parser.extract_enums_asgml())
    elif output == 'enumjson':
        enum_tables = parser.extract_enums()
        print json.dumps(enum_tables, indent=2)
    elif output == 'dot':
        #./ogrtools/interlis/ilismeta.py dot tests/data/ili/RoadsExdm2ien.imd | dot -Tsvg >tests/data/ili/RoadsExdm2ien.imd.svg
        parser.imd_to_dot()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

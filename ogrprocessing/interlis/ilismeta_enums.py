# -*- coding: utf-8 -*-
"""Interlis Meta Model functions

Extract information from Interlis Meta Models.
"""
from xml.etree import ElementTree
from xml.dom import minidom
from subprocess import call
import sys
import string

def prettify(rawxml, indent="  "):
    """Return a pretty-printed XML string
    """
    reparsed = minidom.parseString(rawxml)
    return reparsed.toprettyxml(indent)

def ili_to_meta(ili, ili2c="ili2c.jar"):
    #ili2c USAGE
    #  ili2c [Options] file1.ili file2.ili ...
    #
    #OPTIONS
    #
    #--no-auto             don't look automatically after required models.
    #-o0                   Generate no output (default).
    #-o1                   Generate INTERLIS-1 output.
    #-o2                   Generate INTERLIS-2 output.
    #-oXSD                 Generate an XML-Schema.
    #-oFMT                 Generate an INTERLIS-1 Format.
    #-oIMD                 Generate Model as IlisMeta INTERLIS-Transfer (XTF).
    #-oIOM                 (deprecated) Generate Model as INTERLIS-Transfer (XTF).
    #--out file/dir        file or folder for output.
    #--ilidirs %ILI_DIR;http://models.interlis.ch/;%JAR_DIR list of directories with ili-files.
    #--proxy host          proxy server to access model repositories.
    #--proxyPort port      proxy port to access model repositories.
    #--with-predefined     Include the predefined MODEL INTERLIS in
    #                      the output. Usually, this is omitted.
    #--without-warnings    Report only errors, no warnings. Usually,
    #                      warnings are generated as well.
    #--trace               Display detailed trace messages.
    #--quiet               Suppress info messages.
    #-h|--help             Display this help text.
    #-u|--usage            Display short information about usage.
    #-v|--version          Display the version of ili2c.

    #TODO: write in temp file and return as string
    return call(["java",  "-jar",  ili2c,  "-oIMD", "--out",  string.replace(ili,  '.ili',  '') + '.imd', ili])


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


def main(argv=None):
    if argv is None:
        argv = sys.argv
    #ili_to_meta(argv[1],  ili2c="/home/pi/apps/ili2c/ili2c.jar")
    gml = extract_enums_asgml(argv[1])
    print prettify(gml)

if __name__ == '__main__':
    main()

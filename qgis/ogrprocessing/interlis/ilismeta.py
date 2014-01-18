from sextante.core.GeoAlgorithm import GeoAlgorithm
from sextante.outputs.OutputHTML import OutputHTML
from sextante.parameters.ParameterFile import ParameterFile
from sextante.parameters.ParameterString import ParameterString
from sextante.parameters.ParameterBoolean import ParameterBoolean
from ogrprocessing.sextanteext.ParameterDbConnection import ParameterDbConnection
from sextante.core.Sextante import Sextante
from sextante.core.SextanteLog import SextanteLog
from sextante.core.SextanteConfig import SextanteConfig
from sextante.core.SextanteUtils import SextanteUtils
from sextante.core.QGisLayers import QGisLayers
from ogrprocessing.ogralgorithm import OgrAlgorithm
from ogrprocessing.pyogr.ogr2ogr import *
from ogrprocessing.dbconnection import DbConnection
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
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

class Ili2Imd(OgrAlgorithm):

    #constants used to refer to parameters and outputs.
    #They will be used when calling the algorithm from another algorithm,
    #or when calling SEXTANTE from the QGIS console.
    OUTPUT = "OUTPUT"
    ILI = "ILI"
    IMD = "IMD"

    def defineCharacteristics(self):
        self.name = "ili to XML metamodel"
        self.group = "Interlis"

        self.addParameter(ParameterFile(self.ILI, "Interlis model (.ili)"))
        self.addParameter(ParameterFile(self.IMD, "Ilismeta XML model output file"))

        #self.addOutput(OutputHTML(self.OUTPUT, "ili2c result"))


    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        ili = self.getParameterValue(self.ILI)
        imd = self.getParameterValue(self.IMD)

        IliUtils.runIli2c( ["-oIMD", "--out", imd, ili], progress )

        #output = self.getOutputValue(self.OUTPUT)


class EnumsAsGML(OgrAlgorithm):

    #constants used to refer to parameters and outputs.
    #They will be used when calling the algorithm from another algorithm,
    #or when calling SEXTANTE from the QGIS console.
    OUTPUT = "OUTPUT"
    IMD= "IMD"
    GML= "GML"

    def defineCharacteristics(self):
        self.name = "Export Enums to GML"
        self.group = "Interlis"

        self.addParameter(ParameterFile(self.IMD, "Interlis Ilismeta XML model"))
        self.addParameter(ParameterFile(self.GML, "GML output file"))

        #self.addOutput(OutputHTML(self.OUTPUT, "EnumsAsGML result"))


    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        imd = self.getParameterValue(self.IMD)
        gmlout = self.getParameterValue(self.GML)

        #output = self.getOutputValue(self.OUTPUT)

        gml = extract_enums_asgml(imd)

        f = open(gmlout, "w")
        f.write(prettify(gml))
        f.close()


class ImportGML(OgrAlgorithm):

    #constants used to refer to parameters and outputs.
    #They will be used when calling the algorithm from another algorithm,
    #or when calling SEXTANTE from the QGIS console.
    OUTPUT = "OUTPUT"
    GML= "GML"

    def defineCharacteristics(self):
        self.name = "Import Enums from GML"
        self.group = "Interlis"

        self.addParameter(ParameterFile(self.GML, "GML file"))
        self.addParameter(ParameterDbConnection(self.DB, "Database"))

        #self.addOutput(OutputHTML(self.OUTPUT, "EnumsAsGML result"))

    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        gml = self.getParameterValue(self.GML)
        db = self.getParameterFromName(self.DB)

        #output = self.getOutputValue(self.OUTPUT)

        #IliUtils.runShellCmd(["ogr2ogr", "-f", "PostgreSQL", db.getOgrConnection(), gml], progress)

        ogr2ogr(pszFormat=db.getOgrDriverName(),
            pszDataSource=gml,
            pszDestDataSource=db.getOgrConnection(),
            errfunc=IliUtils.errfunc)


class IliEnumsToPg(OgrAlgorithm):

    #constants used to refer to parameters and outputs.
    #They will be used when calling the algorithm from another algorithm,
    #or when calling SEXTANTE from the QGIS console.
    OUTPUT = "OUTPUT"
    ILI = "ILI"

    def defineCharacteristics(self):
        self.name = "Ili Enums to PG"
        self.group = "Interlis"

        self.addParameter(ParameterFile(self.ILI, "Interlis model (.ili)"))
        self.addParameter(ParameterDbConnection(self.DB, "Database"))

        #self.addOutput(OutputHTML(self.OUTPUT, "EnumsAsGML result"))


    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        ili = self.getParameterValue(self.ILI)
        imd = SextanteUtils.getTempFilename('imd')
        gml = SextanteUtils.getTempFilename('gml')
        db = self.getParameterFromName(self.DB)

        #output = self.getOutputValue(self.OUTPUT)

        IliUtils.runIli2c( ["-oIMD", "--out", imd, ili], progress )
        gmlstr = extract_enums_asgml(imd)
        f = open(gml, "w")
        f.write(gmlstr)
        f.close()

        #IliUtils.runShellCmd(["ogr2ogr", "-f", "PostgreSQL", db.getOgrConnection(), gml], progress)

        ogr2ogr(pszFormat=db.getOgrDriverName(),
            pszDataSource=gml,
            pszDestDataSource=db.getOgrConnection(),
            errfunc=IliUtils.errfunc)


class CreatePGDb(OgrAlgorithm):

    #constants used to refer to parameters and outputs.
    #They will be used when calling the algorithm from another algorithm,
    #or when calling SEXTANTE from the QGIS console.
    OUTPUT = "OUTPUT"
    TEMPLATE = "TEMPLATE"
    DBNAME = "DBNAME"
    HOST = "HOST"
    PORT = "PORT"
    USER = "USER"
    PASSWORD = "PASSWORD"

    def defineCharacteristics(self):
        self.name = "Create PostGIS databse"
        self.group = "Miscellaneous"

        self.addParameter(ParameterString(self.DBNAME, "Database name"))
        self.addParameter(ParameterString(self.TEMPLATE, "Database template", 'template_postgis'))
        self.addParameter(ParameterString(self.HOST, "Host", "localhost"))
        self.addParameter(ParameterString(self.PORT, "Port", "5432"))
        self.addParameter(ParameterString(self.USER, "User", "postgres"))
        self.addParameter(ParameterString(self.PASSWORD, "Password"))
        #self.addOutput(OutputHTML(self.OUTPUT, "EnumsAsGML result"))

    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        db = self.getParameterValue(self.DBNAME)

        connoptions = {
            "host": self.getParameterValue(self.HOST),
            "port": self.getParameterValue(self.PORT),
            "username": self.getParameterValue(self.USER),
            "password": self.getParameterValue(self.PASSWORD),
            "template": self.getParameterValue(self.TEMPLATE)
            }
        connargs = ['--no-password']
        for k,v in connoptions.items():
            if len(v)>0 and k<>'password':
                connargs.append("--%s=%s" % (k, v))

        #output = self.getOutputValue(self.OUTPUT)

        IliUtils.runShellCmd([SextanteConfig.getSetting(IliUtils.CREATEDB_EXEC),
                              ' '.join(connargs), db], progress)

        DbConnection.add_connection(db, connoptions["host"], connoptions["port"], db, connoptions["username"], connoptions["password"])

import os
import re
import urllib2
from xml.etree import ElementTree
from java_exec import run_java


class ModelLoader:
    """Load models of Interlis transfer files"""
    def __init__(self, fn):
        self.fn = fn
        self.model = None

    def detect_format(self):
        """Detect Interlis transfer file type"""
        #Detection as in OGR lib
        f = open(self.fn, "rb")
        header = f.read(1000)
        f.close()

        if "interlis.ch/INTERLIS2" in header:
            return 'Interlis 2'
        elif "SCNT" in header:
            return 'Interlis 1'
        else:
            return None

    def detect_model(self):
        """Find model in itf/xtf file"""
        self.model = None
        fmt = self.detect_format()
        f = open(self.fn, "r")
        if fmt == 'Interlis 1':
            #Search for MODL xxx
            regex = re.compile(r'^MODL\s+(\w+)')
            for line in f:
                m = regex.search(line)
                if m:
                    self.model = [m.group(1)]
                    break
        elif fmt == 'Interlis 2':
            #Search for <MODEL NAME="xxx"
            #Optimized for big files, but does't handle all cases
            self.model = []
            inmodels = False
            regex = re.compile(r'<MODEL[^>]*\sNAME\s*=\s*"([^"]+)"|</MODELS>')
            for line in f:
                if not inmodels:
                    inmodels = ("<MODELS>" in line)
                if inmodels:
                    for m in regex.finditer(line):
                        if m.group(0) == '</MODELS>':
                            break
                        else:
                            self.model.append(m.group(1))

        f.close()
        return self.model

    def repositories(self):
        return ["http://models.interlis.ch/"]

    def ili2c(self):
        return os.getenv("ILI2C", "ili2c.jar")

    def read_ilisite(self, repo):
        url = repo + "ilisite.xml"
        print "Loading " + url + " ..."
        fn = urllib2.urlopen(url)
        tree = ElementTree.parse(fn)
        ns = {'xmlns': "http://www.interlis.ch/INTERLIS2.3"}

        subsites = []
        path = "xmlns:DATASECTION/xmlns:IliSite09.SiteMetadata/xmlns:IliSite09.SiteMetadata.Site/xmlns:subsidiarySite/xmlns:IliSite09.RepositoryLocation_/xmlns:value"
        for location in tree.findall(path, ns):
            subsites.append(location.text)
        return subsites

    def load_model(self):
        """Load model of itf/xtf from model repository"""
        #http://www.interlis.ch/models/ModelRepository.pdf
        for repo in self.repositories():
            subsites = self.read_ilisite(repo)

        return None

    def load_ilismeta_model(self):
        #Call ilismeta service api with URL of ili model
        return None

    def convert_model(self, ilifiles, outfile):
        """Convert ili model to ilismeta model."""

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
        return run_java(self.ili2c(), ["-oIMD", "--out", outfile] + ilifiles)

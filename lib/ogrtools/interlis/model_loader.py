import os
import re
import urllib2
from xml.etree import ElementTree
from java_exec import run_java


NS = {'xmlns': "http://www.interlis.ch/INTERLIS2.3"}


class IliModel:
    """Metadata and link to model"""

    def __init__(self, name):
        self.name = name
        self.version = None
        self.path = None
        self.local_filename = None

    def load(self, repo):
        if self.path is None:
            print "Cannot load model '" + self.name + " with unkown path"
            return

        #TODO: lookup cache first
        url = repo + self.path
        print "Loading model '" + url + " ..."
        fn = urllib2.urlopen(url)
        #TODO: write in cache
        return fn.read()


class ModelLoader:
    """Load models of Interlis transfer files"""

    def __init__(self, fn):
        self._fn = fn
        self.models = None

    def detect_format(self):
        """Detect Interlis transfer file type"""
        #Detection as in OGR lib
        f = open(self._fn, "rb")
        header = f.read(1000)
        f.close()

        if "interlis.ch/INTERLIS2" in header:
            return 'Interlis 2'
        elif "SCNT" in header:
            return 'Interlis 1'
        else:
            return None

    def detect_models(self):
        """Find models in itf/xtf file"""
        self.models = None
        fmt = self.detect_format()
        f = open(self._fn, "r")
        if fmt == 'Interlis 1':
            #Search for MODL xxx
            regex = re.compile(r'^MODL\s+(\w+)')
            for line in f:
                m = regex.search(line)
                if m:
                    self.models = [IliModel(m.group(1))]
                    break
        elif fmt == 'Interlis 2':
            #Search for <MODEL NAME="xxx"
            #Optimized for big files, but does't handle all cases
            self.models = []
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
                            self.models.append(IliModel(m.group(1)))

        f.close()
        return self.models

    def repositories(self):
        return ["http://models.interlis.ch/"]

    def ili2c(self):
        return os.getenv("ILI2C", "ili2c.jar")

    def lookup_model(self, model, repo):
        url = repo + "ilimodels.xml"
        print "Searching model '" + model.name + "' in " + url + " ..."
        fn = urllib2.urlopen(url)
        tree = ElementTree.parse(fn)
        path = "xmlns:DATASECTION/xmlns:IliRepository09.RepositoryIndex/xmlns:IliRepository09.RepositoryIndex.ModelMetadata"
        for node in tree.findall(path, NS):
            name = node.find("xmlns:Name", NS)
            if name is not None and name.text == model.name:
                #TODO: compare Version
                mpath = node.find("xmlns:File", NS)
                if mpath is not None:
                    model.path = mpath.text
                    print "Found matching model."
                    break
        return model

    def lookup_sites(self, model, repo):
        model = self.lookup_model(model, repo)
        if model is not None:
            return model.load(repo)

        #Check site
        # url = repo + "ilisite.xml"
        # print "Loading " + url + " ..."
        # fn = urllib2.urlopen(url)
        # tree = ElementTree.parse(fn)
        # ns = {'xmlns': "http://www.interlis.ch/INTERLIS2.3"}

        # parentsite = repo  # Should be in ilisite.xml according to spec
        # peersites = []  # Not found in an existing ilisite.xml yet
        # subsites = []
        # path = "xmlns:DATASECTION/xmlns:IliSite09.SiteMetadata/xmlns:IliSite09.SiteMetadata.Site/xmlns:subsidiarySite/xmlns:IliSite09.RepositoryLocation_/xmlns:value"
        # for location in tree.findall(path, NS):
        #     subsites.append(location.text)
        # return subsites

    def load_models(self):
        """Load models of itf/xtf from model repository"""
        #http://www.interlis.ch/models/ModelRepository.pdf
        self.detect_models()
        for model in self.models:
            for repo in self.repositories():
                print self.lookup_sites(model, repo)

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

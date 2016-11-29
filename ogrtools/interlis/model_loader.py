import os
import tempfile
import mmap
import re
from xml.etree import ElementTree
from java_exec import run_java


NS = {'xmlns': "http://www.interlis.ch/INTERLIS2.3"}


class IliModel:

    """Metadata and link to model"""

    def __init__(self, name, version="", uri="http://interlis.sourcepole.ch/"):
        self.name = name
        self.version = version
        self.uri = uri


class ModelLoader:

    """Load models of Interlis transfer files"""

    def __init__(self, fn):
        self._fn = fn
        self._fmt = None
        self.models = None

    def detect_format(self):
        """Detect Interlis transfer file type"""
        # Detection as in OGR lib
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
        self._fmt = self.detect_format()
        f = open(self._fn, "r")
        if self._fmt == 'Interlis 1':
            # Search for MODL xxx
            regex = re.compile(r'^MODL\s+(\w+)')
            for line in f:
                m = regex.search(line)
                if m:
                    self.models = [IliModel(m.group(1))]
                    break
        elif self._fmt == 'Interlis 2':
            # Search for <MODEL NAME="xxx"
            size = os.stat(self._fn).st_size
            data = mmap.mmap(f.fileno(), size, access=mmap.ACCESS_READ)
            self.models = []
            m = re.search(r'<MODELS>.+?</MODELS>', data, re.DOTALL)
            if m:
                tree = ElementTree.fromstring(m.group())
                for elem in tree.iterfind('MODEL'):
                    model = IliModel(
                        elem.get("NAME"), elem.get("VERSION"), elem.get("URI"))
                    self.models.append(model)
        f.close()
        return self.models

    def ilidirs(self):
        return "%ILI_DIR;http://models.interlis.ch/"

    def ili2c(self):
        return os.getenv("ILI2C", "ili2c.jar")

    def gen_lookup_ili(self):
        self.detect_models()
        # if self._fmt == "Interlis 2":
        ili = 'INTERLIS 2.3;\nMODEL Lookup AT "http://interlis.sourcepole.ch/" VERSION "" =\n'
        for model in self.models:
            ili += "  IMPORTS %s;\n" % model.name
        ili += "END Lookup."
        return ili

    def create_ilismeta_model(self):
        ili = self.gen_lookup_ili()
        fh, ilifn = tempfile.mkstemp(suffix='.ili')
        os.write(fh, ili)
        os.close(fh)
        imd = self._fn + '.imd'  # TODO: use main model as prefix
        print self.convert_model([ilifn], imd)
        os.remove(ilifn)
        return imd

    def convert_model(self, ilifiles, outfile):
        """Convert ili model to ilismeta model."""

        # ili2c USAGE
        #  ili2c [Options] file1.ili file2.ili ...
        #
        # OPTIONS
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
        return run_java(self.ili2c(),
                        ["-oIMD", "--ilidirs", "'" +
                            self.ilidirs() + "'", "--out", outfile]
                        + ilifiles)

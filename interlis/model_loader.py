from java_exec import run_java

class ModelLoader:
    def __init__(self, fn):
        self.fn = fn
        self.model = None

    def detect_format(self):
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
        self.model = None
        fmt = self.detect_format(self.fn)
        if fmt == 'Interlis 1':
            #Search for MODL xxx
            self.model = 'xxx'
        elif fmt == 'Interlis 2':
            #Search for <MODEL NAME="xxx"
            self.model = 'xxx'
        return self.model

    def load_model(self):
        #Load model from model repository
        #http://www.interlis.ch/models/ModelRepository.pdf
        return None

    def load_ilismeta_model(self):
        #Call ilismeta service api with URL of ili model
        return None

    def convert_model(self):
        ili2c_jar = 'ili2c.jar'
        ili = self.model + '.ili'
        imd = self.model + '.imd'

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
        run_java(ili2c_jar, ["-oIMD", "--out", imd, ili])

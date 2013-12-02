import string
import re

from interlis.ilismeta import extract_enums_json


#Base class for format specific methods
class FormatHandler:
    def __init__(self):
        self.name_seq = 0

    def launder_name(self, src_name):
        #Do nothing in default implementation
        return src_name

    def detect_model(self, src_file):
        return None

    def extract_enums(self, model):
        return None

    def shorten_name(self, src_name, prefix, splitchar='.'):
        # Nutzungsplanung.Nutzungsplanung.Grundnutzung_Zonenflaeche.Herkunft
        # -> enumXX_herkunft
        short_name = string.rsplit(src_name, splitchar, maxsplit=1)[-1]
        short_name = "%s%d_%s" % (prefix, self.name_seq, short_name)
        self.name_seq = self.name_seq + 1
        return short_name


class PgFormatHandler(FormatHandler):
    #PG default name limit is 63 chars
    def __init__(self):
        FormatHandler.__init__(self)
        self.max_len = 63

    def launder_name(self, src_name):
        #OGRPGDataSource::LaunderName
        #return re.sub(r"[#'-]", '_', src_name.lower())
        name = unicode(src_name).lower().encode('ascii', 'replace')
        if len(name) > self.max_len - 7:
            return self.shorten_name(name, 'n')
        else:
            return re.compile("\W+", re.UNICODE).sub("_", name)


class IliFormatHandler(FormatHandler):
    def __init__(self):
        FormatHandler.__init__(self)

    def detect_model(self, src_file):
        return None

    def extract_enums(self, model):
        return extract_enums_json(model)

from sextante.parameters.ParameterSelection import ParameterSelection
from ogrprocessing.dbconnection import DbConnection


class ParameterDbConnection(ParameterSelection):

    def __init__(self, name="", description=""):
        self.options = DbConnection.qgis_connections()
        ParameterSelection.__init__(
            self, name, description, self.options, default=0)

    def getConnectionName(self):
        return self.options[self.value]

    def getConnectionURI(self):
        return DbConnection.layer_uri(self.getConnectionName())

    def getOgrConnection(self):
        connoptions = {
            "host": self.getHost(),
            "port": self.getPort(),
            "dbname": self.getDatabase(),
            "user": self.getUsername(),
            "password": self.getPassword()
        }
        connargs = []
        for k, v in connoptions.items():
            if len(v) > 0:
                connargs.append("%s='%s'" % (k, v))
        return "PG:%s" % " ".join(connargs)

    def getOgrDriverName(self):
        return 'PostgreSQL'

    def getHost(self):
        return DbConnection.connection_value(self.getConnectionName(), "host")

    def getPort(self):
        return DbConnection.connection_value(self.getConnectionName(), "port")

    def getDatabase(self):
        return DbConnection.connection_value(self.getConnectionName(), "database")

    def getUsername(self):
        return DbConnection.connection_value(self.getConnectionName(), "username")

    def getPassword(self):
        return DbConnection.connection_value(self.getConnectionName(), "password")

    def getValueAsCommandLineParameter(self):
        return "\"" + str(self.value) + "\""

    def getAsScriptCode(self):
        return "##" + self.name + "=dbconnection " + ";".join(self.options)

    def deserialize(self, s):
        tokens = s.split("|")
        if len(tokens) == 4:
            return ParameterSelection(tokens[0], tokens[1], tokens[2].split(";"), int(tokens[3]))
        else:
            return ParameterSelection(tokens[0], tokens[1], tokens[2].split(";"))

    def serialize(self):
        return self.__module__.split(".")[-1] + "|" + self.name + "|" + self.description + \
            "|" + ";".join(self.options)

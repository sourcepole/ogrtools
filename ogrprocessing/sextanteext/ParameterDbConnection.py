from sextante.parameters.ParameterSelection import ParameterSelection
from ogrprocessing.dbconnection import DbConnection

class ParameterDbConnection(ParameterSelection):

    def __init__(self, name="", description=""):
        self.options = DbConnection.qgis_connections()
        ParameterSelection.__init__(self, name, description, self.options, default = 0)

    def getConnectionName(self):
        return self.options[self.value]

    def getConnectionURI(self):
        return DbConnection.layer_uri(self.getConnectionName())

    def getOgrConnection(self):
        return "PG:\"dbname='%s'\"" % self.getDatabase() #FIXME

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

    def serialize(self):
        return self.__module__.split(".")[-1] + "|" + self.name + "|" + self.description

    def deserialize(self, s):
        tokens = s.split("|")
        return ParameterDbConnection(tokens[0], tokens[1])

    def getAsScriptCode(self):
        return "##" + self.name + "=dbconnection"

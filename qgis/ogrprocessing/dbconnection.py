from PyQt4.QtCore import *
from qgis.core import *


class DbConnection:

    @staticmethod
    def qgis_connections():
        connection_names = []
        settings = QSettings()
        settings.beginGroup(u"/PostgreSQL/connections")
        for name in settings.childGroups():
            settings.beginGroup(name)
            connection_names.append(name)
            settings.endGroup()
        settings.endGroup()
        return connection_names

    @staticmethod
    def layer_uri(connection):
        # find db connection and create uri
        uri = QgsDataSourceURI()
        settings = QSettings()
        settings.beginGroup(u"/PostgreSQL/connections")
        settings.beginGroup(connection)
        # create uri
        uri.setConnection(
            settings.value("host").toString(),
            settings.value("port").toString(),
            settings.value("database").toString(),
            settings.value("username").toString(),
            settings.value("password").toString(),
            QgsDataSourceURI.SSLmode(settings.value("sslmode").toInt()[0])
        )
        uri.setUseEstimatedMetadata(
            settings.value("estimatedMetadata").toBool())
        #uri.setDataSource("", table_name, geom_column)

        settings.endGroup()
        settings.endGroup()

        return uri

    @staticmethod
    def connection_value(connection, key):
        uri = QgsDataSourceURI()
        settings = QSettings()
        settings.beginGroup(u"/PostgreSQL/connections")
        settings.beginGroup(connection)
        value = str(settings.value(key).toString())
        settings.endGroup()
        settings.endGroup()
        return value

    @staticmethod
    def add_connection(name, host, port, database, username, password):
        settings = QSettings()
        key = u"/PostgreSQL/connections/" + name
        settings.setValue(key + "/host", QVariant(host))
        settings.setValue(key + "/port", port)
        settings.setValue(key + "/database", QVariant(database))
        settings.setValue(key + "/username", QVariant(username))
        settings.setValue(key + "/password", QVariant(password))
        settings.setValue(key + "/saveUsername", True)
        settings.setValue(key + "/savePassword", True)
        settings.setValue(key + "/geometryColumnsOnly", True)
        settings.setValue(key + "/estimatedMetadata", True)

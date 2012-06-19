from PyQt4.QtCore import *
from PyQt4.QtGui import *
import subprocess
from sextante.core.SextanteLog import SextanteLog
from sextante.core.SextanteUtils import SextanteUtils
import os

class IliUtils:

    @staticmethod
    def runJava(jar, args, progress):
        settings = QSettings()
        #path = str(settings.value( "/IliTools/IliPath", QVariant( "" ) ).toString())
        #envval = str(os.getenv("PATH"))
        #if not path.lower() in envval.lower().split(os.pathsep):
        #    envval += "%s%s" % (os.pathsep, str(path))
        #    os.putenv( "PATH", envval )
        loglines = []
        loglines.append("Ili execution console output")
        if SextanteUtils.isWindows():
            command = ["cmd.exe", "/C ", "java.exe", "-jar",  jar] + args
        else:
            command = ["java", "-jar",  jar] + args
        SextanteLog.addToLog(SextanteLog.LOG_INFO, ''.join(['%s ' % c for c in command]))
        fused_command = ''.join(['"%s" ' % c for c in command])
        proc = subprocess.Popen(fused_command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,stderr=subprocess.STDOUT, universal_newlines=False).stdout
        for line in iter(proc.readline, ""):
            loglines.append(line)
        SextanteLog.addToLog(SextanteLog.LOG_INFO, loglines)
        IliUtils.consoleOutput = loglines

    @staticmethod
    def runShellCmd(args, progress):
        loglines = []
        loglines.append("Ili execution console output")
        if SextanteUtils.isWindows():
            command = ["cmd.exe", "/C ",] + args
        else:
            command = args
        SextanteLog.addToLog(SextanteLog.LOG_INFO, ''.join(['%s ' % c for c in command]))
        fused_command = ''.join(['"%s" ' % c for c in command])
        proc = subprocess.Popen(fused_command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,stderr=subprocess.STDOUT, universal_newlines=False).stdout
        for line in iter(proc.readline, ""):
            loglines.append(line)
        SextanteLog.addToLog(SextanteLog.LOG_INFO, loglines)
        IliUtils.consoleOutput = loglines

    @staticmethod
    def getConsoleOutput():
        return IliUtils.consoleOutput

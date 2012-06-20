from PyQt4.QtCore import *
from PyQt4.QtGui import *
import subprocess
from sextante.core.SextanteLog import SextanteLog
from sextante.core.SextanteUtils import SextanteUtils
import os

class IliUtils:

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
    def runJava(jar, args, progress):
        if SextanteUtils.isWindows():
            args = ["java.exe", "-jar",  jar] + args
        else:
            args = ["java", "-jar",  jar] + args
        IliUtils.runShellCmd(args, progress)

    @staticmethod
    def runIli2c(args, progress):
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
        IliUtils.runJava( '/home/pi/apps/ili2c-4.4.4/ili2c.jar', args, progress )

    @staticmethod
    def getConsoleOutput():
        return IliUtils.consoleOutput

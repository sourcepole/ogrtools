from PyQt4.QtCore import *
from PyQt4.QtGui import *
import subprocess
import os
from processing.core.ProcessingLog import ProcessingLog
from processing.core.ProcessingConfig import ProcessingConfig
from processing.tools.system import isWindows


class IliUtils:

    JAVA_EXEC = "JAVA_EXEC"
    ILI2PG_JAR = "ILI2PG_JAR"
    ILI2GPKG_JAR = "ILI2GPKG_JAR"

    @staticmethod
    def runShellCmd(args, progress):
        loglines = []
        loglines.append("Ili execution console output")
        if isWindows():
            command = ["cmd.exe", "/C ", '""' + args[0] + '"'] + args[1:] + ['"']
        else:
            command = args
        ProcessingLog.addToLog(ProcessingLog.LOG_INFO, ' '.join(command))
        # java doesn't find quoted file on Win with: ''.join(['"%s" ' % c for c
        # in command])
        fused_command = ' '.join(command)
        proc = subprocess.Popen(fused_command, shell=True, stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout
        for line in iter(proc.readline, ""):
            loglines.append(line)
        ProcessingLog.addToLog(ProcessingLog.LOG_INFO, loglines)
        IliUtils.consoleOutput = loglines

    @staticmethod
    def java_exec_default():
        if isWindows():
            java = "java.exe"
        else:
            java = "java"
        return java

    @staticmethod
    def runJava(jar, args, progress):
        args = [ProcessingConfig.getSetting(IliUtils.JAVA_EXEC), "-jar", jar] + args
        IliUtils.runShellCmd(args, progress)

    @staticmethod
    def runIli2c(args, progress):
        # ili2c USAGE
        #  ili2c [Options] file1.ili file2.ili ...
        #
        # OPTIONS
        #
        # --no-auto             don't look automatically after required models.
        # -o0                   Generate no output (default).
        # -o1                   Generate INTERLIS-1 output.
        # -o2                   Generate INTERLIS-2 output.
        # -oXSD                 Generate an XTF XML-Schema.
        # -oFMT                 Generate an INTERLIS-1 Format.
        # -oIMD                 Generate Model as IlisMeta INTERLIS-Transfer (XTF).
        # -oUML                 Generate Model as UML2/XMI-Transfer (eclipse flavour).
        # -oIOM                 (deprecated) Generate Model as INTERLIS-Transfer (XTF).
        # --check-repo-ilis uri   check all ili files in the given repository.
        # --out file/dir        file or folder for output (folder must exist).
        # --ilidirs %ILI_DIR;http://models.interlis.ch/;%JAR_DIR list of directories with ili-files.
        # --proxy host          proxy server to access model repositories.
        # --proxyPort port      proxy port to access model repositories.
        # --with-predefined     Include the predefined MODEL INTERLIS in
        #                       the output. Usually, this is omitted.
        # --without-warnings    Report only errors, no warnings. Usually,
        #                       warnings are generated as well.
        # --trace               Display detailed trace messages.
        # --quiet               Suppress info messages.
        # -h|--help             Display this help text.
        # -u|--usage            Display short information about usage.
        # -v|--version          Display the version of ili2c.

        jarpath = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'jars'))
        args = [ProcessingConfig.getSetting(IliUtils.JAVA_EXEC),
                "-cp", '"%s/libs/*"' % jarpath, "ch.interlis.ili2c.Main"] + args
        IliUtils.runShellCmd(args, progress)

    @staticmethod
    def getConsoleOutput():
        return IliUtils.consoleOutput

    @staticmethod
    def errfunc(text):
        ProcessingLog.addToLog(ProcessingLog.LOG_ERROR, text)

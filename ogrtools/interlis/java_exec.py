import sys
import subprocess


def run_shell_cmd(args):
    if is_windows():
        command = ["cmd.exe", "/C ", '"' + args[0] + '"'] + args[1:]
    else:
        command = args
    # java doesn't find quoted file on Win with: ''.join(['"%s" ' % c for c in
    # command])
    fused_command = ' '.join(command)
    proc = subprocess.Popen(fused_command, shell=True, stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True).stdout
    return proc.read()


def is_windows():
    return sys.platform.startswith('win')


def java_exec():
    if is_windows():
        java = "java.exe"
    else:
        java = "java"
    return java


def run_java(jar, args):
    args = [java_exec(), "-jar", jar] + args
    return run_shell_cmd(args)

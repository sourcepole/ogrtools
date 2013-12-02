import subprocess


def run_shell_cmd(args, progress):
    if is_windows():
        command = ["cmd.exe", "/C ", '"' + args[0] + '"'] + args[1:]
    else:
        command = args
    fused_command = ' '.join(command)  # java doesn't find quoted file on Win with: ''.join(['"%s" ' % c for c in command])
    proc = subprocess.Popen(fused_command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout


def is_windows():
    return False  # TODO


def java_exec():
    if is_windows():
        java = "java.exe"
    else:
        java = "java"
    return java


def run_java(jar, args, progress):
    args = [java_exec(), "-jar", jar] + args
    run_shell_cmd(args, progress)

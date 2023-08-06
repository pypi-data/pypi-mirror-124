from . import paths
import os
import subprocess


def get_current_home_dir():
    return os.path.expanduser('~')


def execute_capture(command):
    os_exec = os.popen(command)
    Read = os_exec.read()
    os_exec.detach()
    return Read


def get_ip():
    p = os.popen('ipconfig getifaddr en0')
    ip = p.read()[:-1]
    p.close()
    return ip


def waste():
    pass


def command(args: list, quite=False):
    if quite:
        sub = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    else:
        sub = subprocess.Popen(args)

    sub.wait()
    sub.kill()
    sub.terminate()


def remove(file):
    command(args=['rm', '-rf', file])

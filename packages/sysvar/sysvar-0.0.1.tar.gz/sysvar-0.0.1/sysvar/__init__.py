#!/usr/bin/python3
import os
import platform

PLATFORM = platform.platform()
ARCH = platform.architecture()
LIBC = platform.libc_ver()
NODE = platform.node()
PROC = platform.processor()
RELEASE = platform.release()
SYSTEM = platform.system()
VERSION = platform.version()
WIN32_IS_IOT = platform.win32_is_iot()
PYTHON_VERSION = platform.python_version()
UNAME = platform.uname()


NAME = os.name
PARDIR = os.pardir
CURDIR = os.curdir
ENVIRON = os.environ
CWD = os.getcwd()
GID = os.getgid()
CWDB = os.getcwdb()
UID = os.getuid()


DEFPATH = os.path.defpath
ALTSEP = os.path.altsep
EXTSEP = os.extsep
DEVNULL = os.path.devnull
PATHSEP = os.path.pathsep
SEP = os.path.sep



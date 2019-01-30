# -*- coding: utf-8 -*-

"""
Copyright (c) 2017 hualala Security (https://www.beysec.com)
author : bey0nd
"""
import sys

def getTOP100():
    """
    生成TOP100弱口令密码
    """
    return [line.strip() for line in open("conf/top100.dic").xreadlines()]

def checkVersion():
    PYVERSION = sys.version.split()[0]
    if PYVERSION >= "3" or PYVERSION < "2.6":
        exit("[-] incompatible Python version detected ('%s'). For successfully running nstscan you'll have to use version 2.6 or 2.7 (visit 'http://www.python.org/download/')" % PYVERSION)



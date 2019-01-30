# -*- coding: utf-8 -*-

"""
Copyright (c) 2017 hualala Security (https://www.hualala.com)
author wenzhaowei[at]hualala.com
"""

from datatype import AttribDict

def prepare_param(argv):

    params = AttribDict()
    params.targets = argv.u
    params.cookies = argv.cookie
    params.file = argv.f
    params.plugins = argv.plugins
    params.threads = argv.threads
    return params



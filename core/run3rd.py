# -*- coding: utf-8 -*-

"""
Copyright (c) 2017 hualala Security (https://www.beysec.com)
author : bey0nd
"""
import os
import shutil
from core.colorlog import success

rootpath = os.getcwd() + os.path.sep

def runBBScan(param):
    ''' 运行BBScan进行敏感信息扫描 '''
    path = os.path.join("thirdparty","BBScan")
    bbscanpath = os.path.join(rootpath,'thirdparty','BBScan','BBScan.py')
    BBScanCmd = "cd %s && python %s%s -nnn --full" % (path,bbscanpath,param)
    os.system(BBScanCmd)
    success('generate html to reports directory')
    fromscr = os.path.join(rootpath,'thirdparty','BBScan','report')
    tosrc = os.path.join(rootpath,'reports')
    for root, dirs, files in os.walk(fromscr):
        for fp in files:
            if fp.endswith('html'):
                shutil.copy(os.path.join(root,fp),tosrc)




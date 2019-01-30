# -*- coding: utf-8 -*-

"""
Copyright (c) 2017 hualala Security (https://www.beysec.com)
author : bey0nd
"""
import sys
sys.dont_write_bytecode = True
import os
import glob
import gevent
from gevent import monkey
monkey.patch_all()
import core.run3rd
from gevent.queue import Queue
from core.cmdline import parse_args
from core.lib.prepare import prepare_param
from core.lib.function import normalize_url,url2ip
from core.portscan import getopenports
from core.lib.exploit import runPlugins
from core.colorlog import info,warning,error,success
from core.controller.weakservice import weakservice
from core.utils.utils import checkVersion

abspath =  os.path.abspath(os.path.dirname(__file__)) + os.path.sep

def main():
    checkVersion()
    fb = prepare_param(parse_args())
    warning("Init fb successfully")
    if fb.targets:
        targets = [normalize_url(t) for t in fb.targets]
        BBScanPars = " --host %s" % (" ".join(targets))
    elif fb.file:
        BBScanPars = " -f %s" % (abspath + fb.file)
        try:
            with open(fb.file) as fp:
                targets = [normalize_url(line.strip()) for line in fp.xreadlines()]
        except IOError as e:
            print '[!] No such file or directory , please check your file location'
            exit()
        
    # 后台扫描其他服务，如敏感信息泄露，目录爆破
    core.run3rd.runBBScan(BBScanPars)

    


    # service scanner , such as MySQL,redis 
    for target in targets:
        openport = getopenports(target)
        info("scan port complete " + ",".join(map(str, openport)))
        port_queue = []
        for portitem in openport:
            wk = weakservice(url2ip(target),[portitem])
            port_queue.append(gevent.spawn(wk.brute))
        gevent.joinall(port_queue)
        
        

    warning("Init poc scaner")
    # poc scanner part
    task_queue = Queue()
    result_queue = Queue()
    plugins = glob.glob('pocs/pocsuite/*.py') if (fb.plugins=='') else ["pocs\\pocsuite\\"+fb.plugins+'.py']
    for target in targets:
        # gen scan task queue
        for plugin in plugins:
            task_queue.put([target,plugin])

    # 放弃python muti-threading，使用协程，提升扫描速度
    gevent.joinall([gevent.spawn(runPlugins, task_queue, result_queue) for i in range(fb.threads)])
    # print result_queue.qsize()


if __name__ == '__main__':
    main()
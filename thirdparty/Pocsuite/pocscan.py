#coding=utf-8
from pocsuite.api.cannon import Cannon
import MySQLdb

import sys

target = "http://123.206.190.217"

conn = MySQLdb.connect(host='localhost',user='root',passwd='root',db='nstscan',charset='utf8')
cursor = conn.cursor()
cursor.execute("select * from poc limit 1")
data = cursor.fetchall()
conn.close()

pocstring = str(data[0][2])
info = {
    "pocname":"dlink_command_php_exec_noauth",
    "pocstring" : str(pocstring)
}


invoker = Cannon(target, info)
result = invoker.run()
print result
print result[7]

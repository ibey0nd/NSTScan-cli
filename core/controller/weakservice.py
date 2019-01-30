# -*- coding: utf-8 -*-

"""
Copyright (c) 2017 hualala Security (https://www.beysec.com)
author : bey0nd
"""
import socket
import paramiko
import binascii
import hashlib
import re
import ftplib
import urllib2
import struct
import time
import gevent
from gevent import monkey
monkey.patch_all()
from core.colorlog import info,warning

CONFIG_MAP = {
    22 : "ssh",
    3306 : "mysql",
    6379 : "redis",
    1433 : "mssql",
    21 : "ftp",
    873 : "rsync",
    27017 : "mongodb",
    27018 : "mongodb",
    9200 : "elasticsearch",
    9300 : "elasticsearch",
    11211 : "memcache"
}
USER_DIC = {
    "ssh":['root','data','web'],
    "ftp":['ftp','www','admin','root','db','wwwroot','data','web'],
    "mysql":['root'],
    "mssql":['sa'],
    "telnet":['administrator','admin','root','cisco'],
    "postgresql":['postgres','admin'],
    "redis":['null'],
    "mongodb":['null'],
    "memcached":['null'],
    "elasticsearch":['null']
}

PASSWORD_DIC = ['123456','sa','admin','root','password','123123','123','qwer1234!@#$','mysql_root_hualala','{user}','{user}{user}','{user}1','{user}123','{user}2016','{user}2015','{user}!','','P@ssw0rd!!','qwa123','12345678','test','123qwe!@#','123456789','123321','1314520','666666','woaini','fuckyou','000000','1234567890','8888888','qwerty','1qaz2wsx','abc123','abc123456','1q2w3e4r','123qwe','159357','p@ssw0rd','p@55w0rd','password!','p@ssw0rd!','password1','r00t','tomcat','apache','system']

REGEX = [['ftp', '21', '^220.*?ftp|^220-|^220 Service|^220 FileZilla'],  ['telnet', '23', '^\\xff[\\xfa-\\xfe]|^\\x54\\x65\\x6c|Telnet'],['mssql', '1433', ''], ['mysql', '3306', '^.\\0\\0\\0.*?mysql|^.\\0\\0\\0\\n|.*?MariaDB server'], ['postgresql', '5432', ''], ['redis', '6379', '-ERR|^\\$\\d+\\r\\nredis_version'], ['elasticsearch', '9200', ''], ['memcached', '11211', '^ERROR'], ['mongodb', '27017', '']]

class weakservice():
    def __init__(self, host, port):
        self.port = port
        self.host = host
    
    def mysql(self, port):
        warning("check msyql weak password")
        for user in USER_DIC['mysql']:
            for pass_ in PASSWORD_DIC:
                sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                sock.connect((self.host,int(port)))
                packet = sock.recv(254)
                plugin,scramble = self.get_scramble(packet)
                if not scramble:return 3
                pass_ = pass_.replace('{user}', user)
                auth_data = self.get_auth_data(user,pass_,scramble,plugin)
                sock.send(auth_data)
                result = sock.recv(1024)
                if result == "\x07\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00":
                    return "username:%s,password:%s,host:%s" % (user,pass_,self.host)
    
    def redis(self, port):
        warning("check redis weak password")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host,int(port)))
            s.send("INFO\r\n")
            result = s.recv(1024)
            if "redis_version" in result:
                return "%s redis unauthorized" % self.host
            elif "Authentication" in result:
                for pass_ in PASSWORD_DIC:
                    # 密码转换暂无
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((self.host,int(self.port)))
                    s.send("AUTH %s\r\n"%(pass_))
                    result = s.recv(1024)
                    if '+OK' in result:
                        return "username:%s,password:%s" % (user,pass_)
                        warning("username:%s,password:%s,host:%s" % (user, pass_,self.host))
        except Exception,e:
            return 3

    def ssh(self, port):
        warning("check ssh weak password")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        for user in USER_DIC['ssh']:
            for pass_ in PASSWORD_DIC:
                pass_ = str(pass_.replace('{user}', user))
                try:
                    # print "check %s:%s at %s" % (user,pass_,self.host)
                    ssh.connect(self.host, port, user, pass_, timeout=5)
                    ssh.exec_command('whoami')
                    ssh.close()

                    if pass_ == '': pass_ = "null"
                    return "username:%s,password:%s,host:%s" % (user, pass_,self.host)
                    warning("username:%s,password:%s,host:%s" % (user, pass_,self.host))
                    break
                except Exception, e:
                    pass
    
    def mssql(self, port):
        warning("check mssql weak password")
        for user in USER_DIC['mssql']:
            for pass_ in PASSWORD_DIC:
                pass_ = pass_.replace('{user}', user)
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((self.host,port))
                    hh=binascii.b2a_hex(self.host)
                    husername=binascii.b2a_hex(user)
                    lusername=len(user)
                    lpassword=len(pass_)
                    ladd=len(self.host)+len(str(self.port))+1
                    hladd=hex(ladd).replace('0x','')
                    hpwd=binascii.b2a_hex(pass_)
                    pp=binascii.b2a_hex(str(self.port))
                    address=hh+'3a'+pp
                    hhost= binascii.b2a_hex(self.host)
                    data="0200020000000000123456789000000000000000000000000000000000000000000000000000ZZ5440000000000000000000000000000000000000000000000000000000000X3360000000000000000000000000000000000000000000000000000000000Y373933340000000000000000000000000000000000000000000000000000040301060a09010000000002000000000070796d7373716c000000000000000000000000000000000000000000000007123456789000000000000000000000000000000000000000000000000000ZZ3360000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000Y0402000044422d4c6962726172790a00000000000d1175735f656e676c69736800000000000000000000000000000201004c000000000000000000000a000000000000000000000000000069736f5f31000000000000000000000000000000000000000000000000000501353132000000030000000000000000"
                    data1=data.replace(data[16:16+len(address)],address)
                    data2=data1.replace(data1[78:78+len(husername)],husername)
                    data3=data2.replace(data2[140:140+len(hpwd)],hpwd)
                    if lusername>=16:
                        data4=data3.replace('0X',str(hex(lusername)).replace('0x',''))
                    else:
                        data4=data3.replace('X',str(hex(lusername)).replace('0x',''))
                    if lpassword>=16:
                        data5=data4.replace('0Y',str(hex(lpassword)).replace('0x',''))
                    else:
                        data5=data4.replace('Y',str(hex(lpassword)).replace('0x',''))
                    hladd = hex(ladd).replace('0x', '')
                    data6=data5.replace('ZZ',str(hladd))
                    data7=binascii.a2b_hex(data6)
                    
                    sock.send(data7)
                    packet=sock.recv(1024)
                    if 'master' in packet:
                        return "username:%s,password:%s,host:%s" % (user, pass_,self.host)
                except Exception as e:
                    print e
            
    def ftp(self, port):
        warning("check ftp weak password")
        for user in USER_DIC['ftp']:
            for pass_ in PASSWORD_DIC:
                pass_ = pass_.replace('{user}', user)
                print pass_
                try:
                    ftp=ftplib.FTP()
                    ftp.connect(self.host,port)
                    ftp.login(user,pass_)
                    if user == 'ftp':return "anonymous"
                    return "username:%s,password:%s,host:%s"%(user,pass_,self.host)
                except Exception,e:
                    pass
  
    def rsync(self, port):
        """
            rsync 弱口令
        """
        warning("check rsync weak password")
        # ver= None# self.get_ver(ip)# get rsync moudle
        maxline = 8192
        CRLF = '\r\n'
        LF = '\n'
        def getline(file):
            line = file.readline(maxline + 1)
            if len(line) > maxline:
                raise Error("got more than %d bytes" % maxline)
            
            if not line: raise EOFError
            if line[-2:] == CRLF: line = line[:-2]
            elif line[-1:] in CRLF: line = line[:-1]
            return line
        def getresp(file):
            resp = getmultiline(file)
            
            if resp.find('ERROR') != -1:
                raise Error, resp
            else:
                return resp
        def getmultiline(file):
            line = getline(file)
            return line
        try:
            sock = socket.create_connection((self.host, port))
            af = sock.family
            file = sock.makefile('rb')
            server_protocol_version = getresp(file)
            return "host:%s,rsync:%s" % (self.host, server_protocol_version)
        except Exception as e:
            print e
            
        
       


    def mongodb(self, port):
        warning("check mongodb weak password")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host,port))
            data = binascii.a2b_hex("3a000000a741000000000000d40700000000000061646d696e2e24636d640000000000ffffffff130000001069736d6173746572000100000000")
            s.send(data)
            result = s.recv(1024)
            if "ismaster" in result:
                getlog_data = binascii.a2b_hex("480000000200000000000000d40700000000000061646d696e2e24636d6400000000000100000021000000026765744c6f670010000000737461727475705761726e696e67730000")
                s.send(getlog_data)
                result = s.recv(1024)
                if "totalLinesWritten" in result:
                    return "unauthorized"
                else:return ''
        except Exception,e:
            print e

    def elasticsearch(self, port):
        warning("check elasticsearch weak password, but i don't write code~ , it's A HTTP request ")
    
    def memcache(self, port):
        warning("check memcache weak password")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host,int(port)))
        s.send("stats\r\n")
        result = s.recv(1024)
        if "version" in result:
            return "memcache unauthorized"

    def get_scramble(self,packet):
        scramble,plugin = '',''
        try:
            tmp = packet[15:]
            m = re.findall("\x00?([\x01-\x7F]{7,})\x00", tmp)
            if len(m)>3:del m[0]
            scramble = m[0] + m[1]
        except:
            return '',''
        try:
            plugin = m[2]
        except:
            pass
        return plugin,scramble
    def get_hash(self,password, scramble):
        hash_stage1 = hashlib.sha1(password).digest()
        hash_stage2 = hashlib.sha1(hash_stage1).digest()
        to = hashlib.sha1(scramble+hash_stage2).digest()
        reply = [ord(h1) ^ ord(h3) for (h1, h3) in zip(hash_stage1, to)]
        hash = struct.pack('20B', *reply)
        return hash
    def get_auth_data(self,user,password,scramble,plugin):
        user_hex = binascii.b2a_hex(user)
        pass_hex = binascii.b2a_hex(self.get_hash(password,scramble))
        data = "85a23f0000000040080000000000000000000000000000000000000000000000" + user_hex + "0014" + pass_hex
        if plugin:data+=binascii.b2a_hex(plugin)+ "0055035f6f73076f737831302e380c5f636c69656e745f6e616d65086c69626d7973716c045f7069640539323330360f5f636c69656e745f76657273696f6e06352e362e3231095f706c6174666f726d067838365f3634"
        len_hex = hex(len(data)/2).replace("0x","")
        auth_data = len_hex + "000001" +data
        return binascii.a2b_hex(auth_data)

    def brute(self):
        result = []
        # t_queue = []
        for port,service in CONFIG_MAP.items():
            if port in self.port:
                rst = getattr(self,service)(port)
                info(rst)
                result.append(rst)
                
                # t_queue.append(gevent.spawn(getattr(self,service), port))

        # gevent.joinall(t_queue)
        return result

def main():
    wk = weakservice("172.16.32.28",[80,22,6379,3306,8089,8088])
    wk.brute()

if __name__ == '__main__':
    main()
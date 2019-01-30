#coding=utf-8
import json
import re
from urlparse import urlparse
import datetime
import random,string
import uuid
from socket import gethostbyname
from socket import gethostbyname_ex
from urlparse import urlsplit

def isJson(jsonstr):
    '''
        判断是否为json
    '''
    try:
        json.loads(jsonstr)
    except ValueError:
        return False
    return True

def url2ip(url):
    """
    works like turning 'http://baidu.com' => '180.149.132.47'
    """
    # url = url.replace("http://",'').replace("https://",'') if url.startswith("http") else url
    # url = url[:-1] if url.endswith('/') else url
    url = urlsplit(url)[1].split(':')[0]

    return gethostbyname_ex(url)[2][0]
    # iport = urlsplit(url)[1].split(':')
    # if len(iport) > 1:
    #     return gethostbyname(iport[0]), iport[1]
    # return gethostbyname(iport[0])

def decode_response_text(txt, charset=None):
    '''
        文本以各种编码形式解码
    '''
    if charset:
        try:
            return txt.decode(charset)
        except:
            pass
    for _ in ['UTF-8', 'GB2312', 'GBK', 'iso-8859-1', 'big5']:
        try:
            print _
            return txt.decode(_)
        except:
            pass
    try:
        return txt.decode('ascii', 'ignore')
    except:
        pass
    raise Exception('Fail to decode response Text')


def isIP(target):
    """is IP or not"""
    regexp = '^(\d{1,3}\.){3}\d{1,3}$'
    res = re.match(regexp, target)
    return False if res is None else True

def normalize_url(url):
    """normalize the URL as http://xxxx/"""
    url = url.strip()
    if not url.startswith('http'):
        url = "http://" + url
    if urlparse(url).path == "":
        url = url + '/'
    return url

def now():
    """return current time, 2017-01-01 12:26:10"""
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def getrandchrs(length=6):
    '''
    获取随机的字符串
    '''
    return ''.join([random.choice(string.letters) for _ in range(length)])


def getUUID():
    return str(uuid.uuid4())#.replace("-","")

def main():
    print isIP('https://www.beysec.com')
    print normalize_url('https://www.beysec.com')
    print now()
    print getrandchrs()
    print getUUID()



if __name__ == '__main__':
    main()

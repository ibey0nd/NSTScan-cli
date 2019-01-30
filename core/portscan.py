#!/usr/bin/python
# -*- coding:utf8 -*-
# Python:          2.7.13
# Platform:        Windows
# Authro:          s3xy

import socket, time, signal
from socket import gethostbyname
from socket import gethostbyname_ex
from urlparse import urlsplit
import threading
socket.setdefaulttimeout(5)

openports = list()
lock = threading.Lock()

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

def socket_port(ip, port):
    """
     scan open port by socket
    """
    global openports
    openports = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, port))
        if result == 0:
            lock.acquire()
            openports.append(port)
            lock.release()
        s.close()
    except Exception as e:
        openports.append(0)


def ip_scan(ip):
    """
        scan open ports from user assign
    """
    try:
        tmp = [21,22,23,80,81,82,83,84,85,86,87,88,89,90,91,92,93,95,96,97,98,99,389,443,873,1433,2049,2181,2375,3306,3389,5984,6379,7001,8069,8080,8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,8888,9090,9091,9092,9093,9094,9095,9096,9097,9098,9099,9200,9999,11211,27017,50070]
        thread_queue = []
        for i in tmp:
            t = threading.Thread(target=socket_port,args=(ip,i))
            t.start()
            thread_queue.append(t)
        for tt in thread_queue:
            tt.join()

    except Exception as e:
        openports.append(0)

def getopenports(ip):
    ip_scan(url2ip(ip))
    return openports



if __name__ == '__main__':

    domain = 'http://www.xusec.com/newtask'
    # print urlsplit(domain)[1].split(':')[0]
    # exit()
    # ip = url2ip(domain)
    # print ip
    print getopenports(domain)



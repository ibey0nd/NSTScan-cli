# -*- coding: utf-8 -*-

"""
Copyright (c) 2017 hualala Security (https://www.hualala.com)
author wenzhaowei[at]hualala.com
"""
import sys
import argparse


def parse_args():
    banner()
    parser = argparse.ArgumentParser(prog='NSTScan',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description='* weB vulnerability Scanner. *\n'
                                                 'Author : bey0nd [at] (https://www.beysec.com)',
                                     usage='NSTScan-cli.py [options]')

    parser.add_argument('-u', metavar='HOST [HOST2 HOST3 ...]', type=str, default='', nargs='*',
                        help='Scan several url from command line')

    parser.add_argument('-f', metavar='TargetFile', type=str, default='',
                        help='Load new line delimited targets from TargetFile')

    parser.add_argument('-p',"--plugins", metavar='', type=str, default='', help='Load plugins from TargetDirectory')

    parser.add_argument("-cookie", metavar='name=value', type=str, default='', help='HTTP cookies for Target')

    parser.add_argument('-t',"--threads", metavar='', type=int, default='1', help='Max number of concurrent HTTP(s) requests (default 1)')

    if(len(sys.argv))==1:
        sys.argv.append('-h')
    argv = parser.parse_args()
    return argv

def banner():
    banner = ''' 
 _   _  _____ _______ _____                 
| \ | |/ ____|__   __/ ____|                
|  \| | (___    | | | (___   ___ __ _ _ __  
| . ` |\___ \   | |  \___ \ / __/ _` | '_ \ 
| |\  |____) |  | |  ____) | (_| (_| | | | |
|_| \_|_____/   |_| |_____/ \___\__,_|_| |_|
                                 weB vulnerability Scanner 
                          bey0nd [at] (https://www.beysec.com)
'''
    print banner
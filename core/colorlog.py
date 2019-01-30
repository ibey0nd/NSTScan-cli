#coding=utf-8

import platform
import time
if 'Windows' in platform.system():
    import sys
    import ctypes
    __stdInputHandle = -10
    __stdOutputHandle = -11
    __stdErrorHandle = -12
    __foreGroundBLUE = 0x03
    __foreGroundGREEN = 0x02
    __foreGroundRED = 0x04
    __foreGroundYELLOW = 0x06
    stdOutHandle=ctypes.windll.kernel32.GetStdHandle(__stdOutputHandle)
    def setCmdColor(color,handle=stdOutHandle):
        return ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    def resetCmdColor():
        setCmdColor(__foreGroundRED | __foreGroundGREEN | __foreGroundBLUE)
    def success(msg):
        msg="[+] " + time.strftime('%H:%M:%S', time.localtime()) +' [SUCCESS] ' + msg
        setCmdColor(__foreGroundBLUE)
        sys.stdout.write(msg + '\n')
        resetCmdColor()
    def info(msg):
        msg="[+] " + time.strftime('%H:%M:%S', time.localtime()) +' [INFO] ' + msg
        setCmdColor(__foreGroundGREEN)
        sys.stdout.write(msg + '\n')
        resetCmdColor()
    def error(msg):
        msg="[+] " + time.strftime('%H:%M:%S', time.localtime()) +' [ERROR] ' + msg
        setCmdColor(__foreGroundRED)
        sys.stdout.write(msg + '\n')
        resetCmdColor()
    def warning(msg):
        msg="[-] " + time.strftime('%H:%M:%S', time.localtime()) +' [WARNING] ' + msg
        setCmdColor(__foreGroundYELLOW)
        sys.stdout.write(msg + '\n')
        resetCmdColor()
else:
    STYLE = {
        'fore':{
               'red': 31,
               'green': 32,
               'yellow': 33,
               'blue': 34,
        }
    }
    def UseStyle(msg, mode = '', fore = '', back = '40',tips="INFO"):
        msg="[-] " + time.strftime('%H:%M:%S', time.localtime()) +' [%s] %s' % (tips,msg)
        fore  = '%s' % STYLE['fore'][fore] if STYLE['fore'].has_key(fore) else ''
        style = ';'.join([s for s in [mode, fore, back] if s])
        style = '\033[%sm' % style if style else ''
        end   = '\033[%sm' % 0 if style else ''
        return '%s%s%s' % (style, msg, end)
    def error(msg):
        print UseStyle(msg,fore='red',tips="ERROR")
    def success(msg):
        print UseStyle(msg,fore='green',tips="SUCCESS")
    def warning(msg):
        print UseStyle(msg,fore='yellow',tips="WARNING")
    def info(msg):
        print UseStyle(msg,fore='blue',tips="INFO")


def main():
    info("insert [1] rows success")
    warning("insert [1] rows success")
    success("insert [1] rows success")
    time.sleep(3)
    error("insert [1] rows success")

if __name__ == '__main__':
    main()
from colorama import init, Fore, Back, Style
import time
import sys
import threading

class logging():
    def __init__(self):
        init(autoreset=True)
        self.lock = threading.Lock()

    def INFO(self,msg):
        self.lock.acquire()
        sys.stdout.write(Fore.GREEN  + '[-] ' + time.strftime('%H:%M:%S', time.localtime()) +' [INFO] '+ msg + '\n')
        self.lock.release()

    def ERROR(self,msg):
        self.lock.acquire()
        sys.stdout.write(Fore.RED + '[!] ' + time.strftime('%H:%M:%S', time.localtime()) +' [ERROR] '+ msg + '\n')
        self.lock.release()
    
    def WARNING(self,msg):
        self.lock.acquire()
        sys.stdout.write(Fore.YELLOW + '[!] ' + time.strftime('%H:%M:%S', time.localtime()) + ' [WARN] '+ msg + '\n')
        self.lock.release()
    
if __name__ == '__main__':
    logging = logging()
    str = "insert [1] row"
    logging.ERROR(str)
    logging.INFO(str)
    logging.WARNING(str)
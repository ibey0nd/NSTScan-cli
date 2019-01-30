# 插件化集成扫描器

## 前言
结合了市面上流行的一些扫描器思路，写了个比较完整的扫描规则。支持ip，domain，网段，批量检测。
及漏洞扫描支持。

 - web目录
 - 未授权访问
 - 弱口令
 - CMS
 - CVE

优化了几次，扫描速度相对较快。如果触发waf防火墙可设置线程。


## Usage
> 使用帮助


```bash
python nstscan-cli.py

 _   _  _____ _______ _____
| \ | |/ ____|__   __/ ____|
|  \| | (___    | | | (___   ___ __ _ _ __
| . ` |\___ \   | |  \___ \ / __/ _` | '_ \
| |\  |____) |  | |  ____) | (_| (_| | | | |
|_| \_|_____/   |_| |_____/ \___\__,_|_| |_|
                                 weB vulnerability Scanner
                          bey0nd [at] (https://www.beysec.com)

usage: NSTScan-cli.py [options]

* weB vulnerability Scanner. *
Author : bey0nd [at] (https://www.beysec.com)

optional arguments:
  -h, --help            show this help message and exit
  -u [HOST [HOST2 HOST3 ...] [HOST [HOST2 HOST3 ...] ...]]
                        Scan several url from command line
  -f TargetFile         Load new line delimited targets from TargetFile
  -p , --plugins        Load plugins from TargetDirectory
  -cookie name=value    HTTP cookies for Target
  -t , --threads        Max number of concurrent HTTP(s) requests (default 1)
```



> 指定扫描


```bash
python nstscan-cli.py -u 172.16.32.28

 _   _  _____ _______ _____
| \ | |/ ____|__   __/ ____|
|  \| | (___    | | | (___   ___ __ _ _ __
| . ` |\___ \   | |  \___ \ / __/ _` | '_ \
| |\  |____) |  | |  ____) | (_| (_| | | | |
|_| \_|_____/   |_| |_____/ \___\__,_|_| |_|
                                 weB vulnerability Scanner
                          bey0nd [at] (https://www.beysec.com)

[-] 17:02:58 [WARNING] Init fb successfully
[17:02:59] Batch web scan start.
[17:03:00] Report thread created, prepare target Queue...
[17:03:01] 1 targets entered Queue.
[17:03:01] Create 30 sub Processes...
[17:03:01] 30 sub process successfully created.
[17:03:06] Scan web: http://172.16.32.28
[+] [302] http://172.16.32.28/
[+] [] redis://172.16.32.28:6379
[17:03:39] Scan report saved to report/hosts_20180125_170300.html
[+] 17:03:39 [SUCCESS] generate html to reports directory
[+] 17:03:41 [INFO] scan port complete 80,22,3306,6379,8089,8088
[-] 17:03:41 [WARNING] check ssh weak password
[-] 17:03:41 [WARNING] check msyql weak password
[-] 17:03:41 [WARNING] check redis weak password
[+] 17:03:41 [INFO] 172.16.32.28 redis unauthorized
[+] 17:03:41 [INFO] username:root,password:mysql_pwd,host:172.16.32.28
[+] 17:03:55 [INFO] username:root,password:qwer1234!@#$,host:172.16.32.28
[-] 17:03:55 [WARNING] Init poc scaner
[+] 17:03:55 [INFO] url [http://172.16.32.28/] verify [axublog_1_6] is [Failed]
[+] 17:03:55 [INFO] url [http://172.16.32.28/] verify [dedecms_re] is [Failed]
[+] 17:03:55 [INFO] url [http://172.16.32.28/] verify [git_config_info_disclosure] is [failed]
[+] 17:03:55 [INFO] url [http://172.16.32.28/] verify [jboss] is [Failed]
[+] 17:03:55 [INFO] url [http://172.16.32.28/] verify [Joomla_3_7_0_sqli] is [Failed]
[+] 17:03:55 [INFO] url [http://172.16.32.28/] verify [ns_asg_6_2_gateway] is [Failed]
[+] 17:03:55 [INFO] url [http://172.16.32.28/] verify [redis-unauth] is [success]
[+] 17:03:55 [INFO] url [http://172.16.32.28/] verify [st2_045] is [Failed]
[+] 17:03:55 [INFO] url [http://172.16.32.28/] verify [st2_046] is [Failed]
[+] 17:03:55 [INFO] url [http://172.16.32.28/] verify [zimbra_lfi] is [Failed]
```

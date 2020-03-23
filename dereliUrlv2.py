# -*- coding: utf-8 -*-
__author__ = 'mehmet şerif paşa'

import re
import time
import socket
import random
import argparse
import requests
import threading
from bs4 import BeautifulSoup

try:
    import colorama
except ImportError:
    print("No module named 'Colorama' found")

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


## parse section
parse = argparse.ArgumentParser()
parse.add_argument('-u', '--url', help='example: http://evil.com')
parse.add_argument('-o', '--output', help='example: output.txt')
args = parse.parse_args()
host = args.url
output = args.output


class Machine:
    def __init__(self, host, output):
        self.host = host
        self.output = output
        self.GOOGLE_URL_LIST = set()
        self.CONTENT_URL_LIST = set()
        self.GOOGLE_AND_CONTENT_URL_LIST_KNIT = set()
        self.DIRECTORY = set()
        self.DIRECTORY_2 = set()
        self.TOTAL_URL = set()
        self.say = 0
        self.NOT_CONTENT_URL_LIST = set() # farklı domain'e ait siteleri tutar
        self.USERAGENT = [agent.strip() for agent in open('useragent.txt')]
        self.Random_Useragent = random.choice(self.USERAGENT)

    def Output(self, put):
        self.file = open(str(self.output), "a+")
        self.file.writelines(str(put) + "\n")

    def Request(self):
        # İstek burda yapılıyor ve bunun üzerinden işlem yapılıyor.
        self.req = requests.get(self.host)  # Siteye GET isteği yapılmıştır
        self.req_content = self.req.content  # Sitenin kaynak bilgisi
        self.req_headers = self.req.headers  # Sitenin Headers bilgisi
        self.req_status_code = self.req.status_code  # Sitenin durum kodu (200,301 vs.)
        self.req_history = self.req.history  # Sitedeki yönlendirmeleri gösteriyor
        self.req_text = self.req.text  # Düzenli bir şekilde kaynak kodu

    def Host_Look(self):
        # Düzenli gözükmesi için verilen site url'sini,  split işlemine sokarak temiz bir host elde ediyoruz.
        self.host_strip = self.host.split("://")[1]
        print(colorama.Fore.GREEN + "Taranan Site: " + colorama.Style.RESET_ALL + self.host_strip)
        Object_1.Output("Taranan Site: " + self.host_strip)

    def Ip_Look(self):
        # Verdiğimiz sitenin ip bilgisini veriyor
        self.host_ip = socket.gethostbyname(self.host_strip)
        print(colorama.Fore.GREEN + "Ip Adresi: " + colorama.Style.RESET_ALL + self.host_ip)
        Object_1.Output("Ip Adresi: " + self.host_ip)

    def Server_Check(self):
        # Headers bilgisinde yer alan bazı bilgileri derliyoruz.
        for i in self.req_headers.items():  # İtems ile headers üzerinde rahat işlem yapabiliyoruz
            if i[0] == 'Server':  # Server = kaynak sunucu tarafından kullanılan yazılım hakkında bilgi içerir.
                print(colorama.Fore.GREEN + "Server: " + colorama.Style.RESET_ALL + str(i[1]))
                Object_1.Output("Server: " + str(i[1]))
            if i[0] == 'X-Powered-By':  # Web uygulamasını destekleyen teknolojiyi (ör. ASP.NET, PHP, JBoss) belirtir
                print(colorama.Fore.GREEN + "X-Powered-By: " + colorama.Style.RESET_ALL + str(i[1]))
                Object_1.Output("X-Powered-By: " + str(i[1]))
            if i[0] == 'Access-Control-Allow-Origin':
                print(colorama.Fore.GREEN + "Access-Control-Allow-Origin: " + colorama.Style.RESET_ALL + str(i[1]))
                Object_1.Output("Access-Control-Allow-Origin: " + str(i[1]))
            if i[0] == 'Content-Security-Policy':
                print(colorama.Fore.GREEN + "Content-Security-Policy: " + colorama.Style.RESET_ALL + str(i[1]))
                Object_1.Output("Content-Security-Policy: " + str(i[1]))
            if i[0] == 'P3P':
                print(colorama.Fore.GREEN + "P3P: " + colorama.Style.RESET_ALL + str(i[1]))
                Object_1.Output("P3P: " + str(i[1]))
            else:
                pass

    def Robots_Txt(self):
        # Sitede robots dosyasını işliyoruz
        self.robots_txt = requests.get(self.host + '/robots.txt')
        self.robots_txt_text = self.robots_txt.text
        if self.robots_txt.status_code == 200:
            print(colorama.Fore.GREEN + "Robots.txt dosyası mevcut lütfen kontrol ediniz. " + colorama.Style.RESET_ALL)
            Object_1.Output("-" * 50)
        else:
            pass

    def Host_Strip_www(self):
        if 'www' in self.host_strip:
            self.host_strip_control = str(self.host_strip).split('www.')[1]
        else:
            self.host_strip_control = str(self.host_strip)

    def Google_Search_Path_Crawler(self):  # Google yardımıyla ek olarak url aldık
        print(colorama.Fore.GREEN + "Google Search:" + colorama.Style.RESET_ALL)
        query = "site:" + str(self.host_strip)
        for j in search(query, num=50, stop=50, pause=2):
            print(colorama.Fore.RED + "[+] " + colorama.Style.RESET_ALL + str(j))
            self.GOOGLE_URL_LIST.add(str(j))
            for k in self.GOOGLE_URL_LIST:
                self.GOOGLE_AND_CONTENT_URL_LIST_KNIT.add(k)
                Object_1.Output(str(k))

    def Url_Crawler_SECTION_1(self): # sayfa içerisindeki bütün url'leri çektik
        print(colorama.Fore.GREEN + "Url List Section 1: " + colorama.Style.RESET_ALL)
        html_page = self.req_content
        soup = BeautifulSoup(html_page,'html.parser')
        links = re.findall('"((http|ftp)s?://.*?)"', html_page)
        Object_1.Output("-" * 50)
        for t in links:
            if self.host_strip_control in t[0]:
                self.CONTENT_URL_LIST.add(t[0])
                Object_1.Output(str(t[0]))
            else:
                self.NOT_CONTENT_URL_LIST.add(t[0])
        # self.CONTENT_URL_LIST'da url'ler yer alıyor
        # self.NOT_CONTENT_URL_LIST'da ise kaynak'da yer alan fakat aynı domaine ait olmayan URL'ler
        for i in self.CONTENT_URL_LIST:
            print(colorama.Fore.RED + "[+] " + colorama.Style.RESET_ALL + str(i))
            self.GOOGLE_AND_CONTENT_URL_LIST_KNIT.add(i)

    def Url_Crawler_SECTION_2_(self): # DİZİN AYIRMA İŞLEMİ
        print(colorama.Fore.GREEN + "Url List Section 2: " + colorama.Style.RESET_ALL)
        for i in self.GOOGLE_AND_CONTENT_URL_LIST_KNIT:
            if self.host_strip_control in i.split('/')[2]: #[2] = domain
                try:
                    if i.split('/')[3]: # Neden 12 tane derseniz en son ihtimale kadar parçalama yapmaya çalıştım. Arttırılabilir
                        self.DIRECTORY_2.add(str(  i.split('/')[3]  ))
                    if i.split('/')[4]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4]))
                    if i.split('/')[5]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4]) + '/' + i.split('/')[5])
                    if i.split('/')[6]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4]) + '/' + i.split('/')[5] + '/' + i.split('/')[6])
                    if i.split('/')[7]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5] + '/' + i.split('/')[6]) + '/' + i.split('/')[7])
                    if i.split('/')[8]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5]) + '/' + i.split('/')[6] + '/' + i.split('/')[7] + '/' + i.split('/')[8])
                    if i.split('/')[9]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5] + '/' + i.split('/')[6]) + '/' + i.split('/')[7] + '/' + i.split('/')[8] + '/' + i.split('/')[9])
                    if i.split('/')[10]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5] + '/' + i.split('/')[6] + '/' +i.split('/')[7] + '/' +i.split('/')[8] + '/' + i.split('/')[9] + '/' + i.split('/')[10]))
                    if i.split('/')[11]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5] + '/' + i.split('/')[6] + '/' +i.split('/')[7] + '/' +i.split('/')[8] + '/' + i.split('/')[9] + '/' + i.split('/')[10] + '/' + i.split('/')[11]))
                    if i.split('/')[11]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5] + '/' + i.split('/')[6] + '/' +i.split('/')[7] + '/' +i.split('/')[8] + '/' + i.split('/')[9] + '/' + i.split('/')[10] + '/' + i.split('/')[11] + '/' + i.split('/')[11]))
                    """
                    test/test1/test2
                    |
                    |_______test1
                    |_________test1/test2
                    |____________test1/test2/test3
                    |_______________test1/test2/test3/test4 ...
                    """
                except:
                    continue
        Object_1.Output("-" * 50)
        for l in self.DIRECTORY_2:
            print(colorama.Fore.RED + "[+] " + colorama.Style.RESET_ALL + str(l))
            Object_1.Output(str(l))

    def Url_Crawler_SECTION_3(self):
        print(colorama.Fore.GREEN + "Url List Section 3: " + colorama.Style.RESET_ALL)
        Object_1.Output("-" * 50)
        """
        Parçalama yaptığımız URl'lere tekrar istek yollayarak yeni urller elde edicez
        """
        path = [path.strip() for path in self.DIRECTORY_2]
        def Section_3_Crawl():
            self.say += 1
            try:
                for i in self.DIRECTORY_2:
                    self.Section_3_Request = requests.get(self.host + '/' + i , timeout=2, headers= {'User-Agent':self.Random_Useragent})
                    self.Section_3_Content = self.Section_3_Request.content
                    links = re.findall('"((http|ftp)s?://.*?)"', self.Section_3_Content)
                    for t in links:
                        if self.host_strip_control in t[0]:
                            self.TOTAL_URL.add(t[0])
                            Object_1.Output(str(self.host + '/' + t[0]))
                            print(colorama.Fore.GREEN + "[+] " + colorama.Style.RESET_ALL + str(t[0]))
                        else:
                            self.NOT_CONTENT_URL_LIST.add(t[0])
            except requests.exceptions.ConnectionError:
                print(colorama.Fore.RED + "[-] " + colorama.Style.RESET_ALL + str(path[self.say]))
            except requests.exceptions.Timeout:
                print(colorama.Fore.RED + "[-] " + colorama.Style.RESET_ALL + str(path[self.say]))
            except requests.exceptions.SSLError:
                print(colorama.Fore.RED + "[-] " + colorama.Style.RESET_ALL + str(path[self.say]))
            except:
                pass
        Section_3_Crawl()

    def List_Pars(self): #Topladığımız bütün linkleri birleştiriyoruz
        for g in self.DIRECTORY_2:
            self.TOTAL_URL.add(str(g))
        for h in self.GOOGLE_AND_CONTENT_URL_LIST_KNIT:
            self.TOTAL_URL.add(str(h))
        for j in self.CONTENT_URL_LIST:
            self.TOTAL_URL.add(str(j))
        for t in self.GOOGLE_URL_LIST:
            self.TOTAL_URL.add(str(t))
    def Total(self):
        for k in self.TOTAL_URL:
            print(k)



Object_1 = Machine(host, output)
Object_1.Request()
print("-" * 70)
Object_1.Server_Check()
Object_1.Host_Look()
Object_1.Ip_Look()
print("-" * 70)
Object_1.Robots_Txt()
print("-" * 70)
Object_1.Host_Strip_www()
Object_1.Url_Crawler_SECTION_1()
print("-" * 70)
Object_1.Google_Search_Path_Crawler()
print("-" * 70)
Object_1.Url_Crawler_SECTION_2_()
print("-" * 70)
Object_1.Url_Crawler_SECTION_3()
print("-" * 70)
Object_1.List_Pars()
print("-" * 70)
Object_1.Total()
















x

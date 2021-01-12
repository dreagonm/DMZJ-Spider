import requests
import random
from bs4 import BeautifulSoup
import MySQLdb
import time
if __name__ == "__main__":
    Headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'}
    conn=MySQLdb.connect(host='localhost',user='root',passwd='********',database='scraping_proxy',autocommit = True)

class ProxyPool(object):
    def __init__(self):
        self.Http=[]
        self.Https=[]
    
    def CheckHttpProxy(self,proxy):
        try:
            requests.get('http://manhua.dmzj.com/',headers=Headers,proxies=proxy,timeout=5)
        except:
            return False
        else:
            return True

    def CheckHttpsProxy(self,proxy):
        try:
            requests.get('https://www.dmzj.com/',headers=Headers,proxies=proxy,timeout=5)
        except:
            return False
        else:
            return True        

    def UpdateHttpPool(self,page):
        print('getting Http Proxy...')
        cnt=0
        if page<2000:
            page = page+1
            print('page',page)
            Res=requests.get('http://www.nimadaili.com/http/'+str(page)+'/',headers=Headers)
            soup=BeautifulSoup(Res.text,'html.parser')
            L=soup.find('div',class_='mt-0 mb-2 table-responsive').find_all('tr')
            L.pop(0)
            # print(L)
            for x in L:
                l=x.find('td').text
                d={'http':l}
                print('checking',l)
                if self.CheckHttpProxy(d):
                    print('success')
                    cnt = cnt+1
                    cur=conn.cursor()
                    command=r'INSERT INTO proxies (type,url) VALUES ("http","' + l + r'")'
                    try:
                        cur.execute(command)
                    except:
                        print('http',l,'already exist')
                    cur.close()
    
    def UpdateHttpsPool(self,page):
        print('getting Https Proxy...')
        cnt=0
        if page<2000:
            page=page+1
            print('page',page)
            Res=requests.get('http://www.nimadaili.com/https/'+str(page)+'/',headers=Headers)
            soup=BeautifulSoup(Res.text,'html.parser')
            L=soup.find('div',class_='mt-0 mb-2 table-responsive').find_all('tr')
            L.pop(0)
            # print(L)
            for x in L:
                l=x.find('td').text
                d={'https':l}
                print('checking',l)
                if self.CheckHttpsProxy(d):
                    print('success')
                    cur=conn.cursor()
                    command=r'INSERT INTO proxies (type,url) VALUES ("https","' + l + r'")'
                    try:
                        cur.execute(command)
                    except:
                        print('http',l,'already exist')
                    cur.close()
                    cnt=cnt+1

    # def GetHttpProxy(self):
    #     i=0
    #     while i<10:
    #         if len(self.Http) < 5:
    #             i=i+1
    #             self.UpdateHttpPool()
    #         if len(self.Http) < 5:
    #             raise RuntimeError('无法获取Http代理')        
    #         Index = random.randint(0,len(self.Http)-1)
    #         if self.CheckHttpProxy(self.Http[Index]):
    #             return self.Http[Index]
    #         else:
    #             self.Http.pop(Index)
    #     raise RuntimeError('无法获取Http代理')

    # def GetHttpsProxy(self):
    #     i=0
    #     while i<10:
    #         if len(self.Https) < 5:
    #             i=i+1
    #             self.UpdateHttpsPool()
    #         if len(self.Https) < 5:
    #             raise RuntimeError('无法获取Https代理')
    #         Index = random.randint(0,len(self.Https)-1)
    #         if self.CheckHttpsProxy(self.Https[Index]):
    #             return self.Https[Index]
    #         else:
    #             self.Https.pop(Index)
    #     raise RuntimeError('无法获取Https代理')

if __name__ == "__main__":
    x = ProxyPool()
    for t in range(0,2000):
        x.UpdateHttpPool(t)
        x.UpdateHttpsPool(t)
    conn.close()
    
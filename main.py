import requests
import os
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver=webdriver.Chrome()
def DownloadPicture(url,Referer='http://manhua.dmzj.com/',Name='test.jpg'): # 下载图片,如果没有refers会报403
    Headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
        'Referer': Referer
    }
    Res=requests.get(url=url,headers=Headers)
    print(Res.status_code)
    with open(Name,'wb') as f:
        f.write(Res.content)

def DeleteAllFileInFolder(path): #删除已经存在的章节
    os.chdir(path)
    FileList=os.listdir()
    for x in FileList:
        if os.path.isfile(x):
            os.remove(x)
        else:
            DeleteAllFileInFolder(os.path.join(path,x))
            os.chdir(path)
    os.chdir('..')
    os.rmdir(path)

def GetChapter1(url,ChapterName=""):# 下载manhua.dmzj的章节
    print("Chapter Name:",ChapterName)
    print("Chapter URL:",url)
    if ChapterName != "":
        FileList=os.listdir()
        if ChapterName in FileList:
            if os.path.isdir(ChapterName):
                DeleteAllFileInFolder(os.path.join(os.getcwd(),ChapterName))
            else:
                os.remove(ChapterName)
        os.mkdir(ChapterName)
        os.chdir(ChapterName)
    else:
        return   
    PageName = 0
    while True:
        PageName = PageName+1
        print("getting page",PageName,"...")
        driver.get(url+'#@page='+str(PageName))
        PictureString=driver.find_element_by_css_selector('div#center_box').get_attribute('innerHTML')
        GetPicturelink=re.compile('<img.*?src="(.*?)">')
        Picturelink=GetPicturelink.search(PictureString).group(1)
        # print(Picturelink)
        if Picturelink=='//images.dmzj.com/undefined':
            break
        DownloadPicture('http:'+Picturelink,Name=str(PageName)+'.jpg')
        time.sleep(1)
        
    os.chdir('..')

# if __name__ == 'getchapter':
#     # DownloadPicture(r'http://images.dmzj.com/l/%E5%86%B7%E6%B7%A1%E7%9A%84%E4%BD%90%E8%97%A4%E5%90%8C%E5%AD%A6%E5%8F%AA%E5%AF%B9%E6%88%91%E6%92%92%E5%A8%87/%E7%AC%AC01%E8%AF%9D/01.jpg')
#     # %E5%86%B7%E6%B7%A1%E7%9A%84%E4%BD%90%E8%97%A4%E5%90%8C%E5%AD%A6%E5%8F%AA%E5%AF%B9%E6%88%91%E6%92%92%E5%A8%87/%E7%AC%AC02%E8%AF%9D/pic_001%20%E6%8B%B7%E8%B4%9D.jpg","l\/%E5%86%B7%E6%B7%A1%E7%9A%84%E4%BD%90%E8%97%A4%E5%90%8C%E5%AD%A6%E5%8F%AA%E5%AF%B9%E6%88%91%E6%92%92%E5%A8%87\/%E7%AC%AC02%E8%AF%9D\/pic_001.jpg","l\/%E5%86%B7%E6%B7%A1%E7%9A%84%E4%BD%90%E8%97%A4%E5%90%8C%E5%AD%A6%E5%8F%AA%E5%AF%B9%E6%88%91%E6%92%92%E5%A8%87\/%E7%AC%AC02%E8%AF%9D\/pic_002%20%E6%8B%B7%E8%B4%9D.jpg
#     GetChapter('http://manhua.dmzj.com/lendandezuotentongxuezhiduiwosajiao/98570.shtml')

def GetChapter2(url,ChapterName=""): #下载www.dmzj的章节
    print("Chapter Name:",ChapterName)
    print("Chapter URL:",url)
    if ChapterName != "":
        FileList=os.listdir()
        if ChapterName in FileList:
            if os.path.isdir(ChapterName):
                DeleteAllFileInFolder(os.path.join(os.getcwd(),ChapterName))
            else:
                os.remove(ChapterName)
        os.mkdir(ChapterName)
        os.chdir(ChapterName)
    else:
        return
    PageName = 0
    while True:
        PageName = PageName+1
        print("getting page",PageName,"...")
        driver.get(url+'#@page='+str(PageName))
        text=driver.find_element_by_css_selector('div.comic_wraCon.autoHeight').get_attribute('innerHTML')
        soup=BeautifulSoup(text)
        Link=soup.find('img')['src']
        # print(soup.find('img')['src'])
        if Link=='https://images.dmzj.com/undefined':
            break
        DownloadPicture(Link,Name=str(PageName)+'.jpg')
        time.sleep(1)

    os.chdir('..')

def MainWorker1(url): # 解析manhua.dmzj.com
    UserAgent={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'} # 请求头
    Res=requests.get(url=url,headers=UserAgent)
    print('status_code =',Res.status_code)
    GetComicTitle=re.compile(r'<div class="odd_anim_title_m"[ ]*>[\d\D]*?<span class="anim_title_text">[\d\D]*<a.*>[\d\D]*<h1>(.*)</h1>') # 获取漫画名称
    ComicName=GetComicTitle.search(Res.text).group(1)
    print(ComicName)
    FileList=os.listdir()
    if(ComicName not in FileList):
        os.mkdir(ComicName)
    os.chdir(ComicName)
    GetComicChapterAndLinkList=re.compile(r'<div class="cartoon_online_border"[ ]*>[\d\D]*?<ul>([\d\D]*?)</ul>')
    # print(GetComicChapterAndLinkList.search(Res.text).group(1))
    GetComicChapterAndLink=re.compile(r'<li><a.*href="(?P<link>.*?)".*?>(?P<name>.*?)</a>')
    ChapterList=GetComicChapterAndLinkList.search(Res.text).group(1)
    DataList=GetComicChapterAndLink.findall(ChapterList)
    # print(DataList)
    ChapterDetail=[]
    for Data in DataList:
        print('http://manhua.dmzj.com'+Data[0],Data[1])
        ChapterDetail.append(('http://manhua.dmzj.com'+Data[0],Data[1]))
    for x,y in ChapterDetail:
        print("Getting",y)
        GetChapter1(x,y)
    print('finish')

def MainWorker2(url): # 解析www.dmzj.com 
    Headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'}
    Res=requests.get(url='https://www.dmzj.com/info/buxihuannverfanerxihuanmamawoma.html',headers=Headers)
    print(Res.status_code)
    print(Res.encoding)
    Res.encoding=Res.apparent_encoding
    soup=BeautifulSoup(Res.text,'html.parser')
    ComicName=soup.find('div',class_='comic_deCon').h1.a.text
    print(ComicName)
    FileList=os.listdir()
    if(ComicName not in FileList):
        os.mkdir(ComicName)
    os.chdir(ComicName)
    ChapterList=soup.find('div',class_='tab-content tab-content-selected zj_list_con autoHeight').find_all('li')
    for x in ChapterList:
        print("Getting",x.text)
        GetChapter2(x.a['href'],x.text)
    print('finish!')

if __name__ == '__main__':
    UrlList=[]
    # UrlList.append(input())
    with open('url.txt','r') as f:
        UrlList=f.readlines()
    UrlList=map(lambda str:str.strip('\n'),UrlList)
    for x in UrlList:
        print(x)
        SwitchRegex=re.compile(r'http://manhua.dmzj.com/')
        if SwitchRegex.match(x) != None:
            MainWorker1(x)
        else:
            MainWorker2(x)
    driver.quit()
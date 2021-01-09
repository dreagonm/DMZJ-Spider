import requests
import os
import re

def DownloadPicture(url,Referer='http://manhua.dmzj.com/',Name='test.jpg'):
    Headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
        'Referer': Referer
    }
    Res=requests.get(url=url,headers=Headers)
    print(Res.status_code)
    with open(Name,'wb') as f:
        f.write(Res.content)

def GetPictureUrl(url):
    pass

def GetChapter(url):
    print("Chapter URL:",url)
    Res=requests.get('http://manhua.dmzj.com/lendandezuotentongxuezhiduiwosajiao/98570.shtml#@page=1')
    Res.encoding=Res.apparent_encoding
    # print(Res.text)
    GetComicPage=re.compile(r'<div id="center_box".*?>[\d\D]*?<img')
    with open("test.html","w") as f:
        f.write(Res.text)
    print(GetComicPage.search(Res.text).group())
    # Pages=[]
    # for x in Pages:
    #     PageUrl=
    #     GetPictureUrl(PageUrl)

if __name__ == '__main__':
    # DownloadPicture(r'http://images.dmzj.com/l/%E5%86%B7%E6%B7%A1%E7%9A%84%E4%BD%90%E8%97%A4%E5%90%8C%E5%AD%A6%E5%8F%AA%E5%AF%B9%E6%88%91%E6%92%92%E5%A8%87/%E7%AC%AC01%E8%AF%9D/01.jpg')
    # %E5%86%B7%E6%B7%A1%E7%9A%84%E4%BD%90%E8%97%A4%E5%90%8C%E5%AD%A6%E5%8F%AA%E5%AF%B9%E6%88%91%E6%92%92%E5%A8%87/%E7%AC%AC02%E8%AF%9D/pic_001%20%E6%8B%B7%E8%B4%9D.jpg","l\/%E5%86%B7%E6%B7%A1%E7%9A%84%E4%BD%90%E8%97%A4%E5%90%8C%E5%AD%A6%E5%8F%AA%E5%AF%B9%E6%88%91%E6%92%92%E5%A8%87\/%E7%AC%AC02%E8%AF%9D\/pic_001.jpg","l\/%E5%86%B7%E6%B7%A1%E7%9A%84%E4%BD%90%E8%97%A4%E5%90%8C%E5%AD%A6%E5%8F%AA%E5%AF%B9%E6%88%91%E6%92%92%E5%A8%87\/%E7%AC%AC02%E8%AF%9D\/pic_002%20%E6%8B%B7%E8%B4%9D.jpg
    GetChapter('http://manhua.dmzj.com/lendandezuotentongxuezhiduiwosajiao/98570.shtml')

if __name__ == 'test':
    url='http://manhua.dmzj.com/lendandezuotentongxuezhiduiwosajiao'
    UserAgent={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'}
    Res=requests.get(url=url,headers=UserAgent)
    print('status_code =',Res.status_code)
    GetComicTitle=re.compile(r'<div class="odd_anim_title_m"[ ]*>[\d\D]*?<span class="anim_title_text">[\d\D]*<a.*>[\d\D]*<h1>(.*)</h1>') # 获取漫画名称
    print(GetComicTitle.search(Res.text).group(1))
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
        GetChapter(x)
    # print(GetComicChapterAndLink.search(Res.text).group(1),GetComicChapterAndLink.search(Res.text).group(2))
    # print(Res.text)

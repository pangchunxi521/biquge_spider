import requests
from bs4 import BeautifulSoup
import random
import os
import sys
from progressbar import ProgressBar
import time


def getHTMLText(url,headers):#获得网页代码
    try:
        r=requests.get(url,timeout=60,headers=headers)
        r.encoding=r.apparent_encoding
        return r.text

    except:
        return "产生异常"
    
def WriteHtml(text):  #将网页代码写入本地文件
    filename=str(random.randint(1,10000))
    filename=filename+".html"
    print(filename)
    text=text.encode("utf-8")
    try:
        f=open("./HTML/"+filename, 'w')
        f.close()
    except:
        os.mkdir(os.getcwd()+"\\HTML")
    with open("./HTML/"+filename, 'wb') as f:
        f.write(text)
        f.close()
    return filename

def BeautifulsoupHtml(html): #beautifulsoup解析代码
    bs = BeautifulSoup(html,"html.parser")
    return bs



def writeTXTcontent(s,book): #将网页可见内容写进指定TXT
    filename=book
    filename=filename+".txt"
    s=s+"\r\n"
    s=s.encode("utf-8")
    try:
        f=open("./TXT/"+filename, 'a')
        f.close()
    except:
        os.mkdir(os.getcwd()+"\\TXT")
    with open("./TXT/"+filename, 'ab') as f:
        f.write(s)
        f.close()
    return filename

def renderHTML(url): #获取网页代码高级版
    #r=Render(url)
    #result=r.html
    #return result
    flag=1
    headers={
        'Cookie': '_abcde_qweasd=0; _abcde_qweasd=0',
        'Host': 'www.xbiquge.la',
        'Origin': 'http://www.xbiquge.la',
        'Referer': 'http://www.xbiquge.la/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    }
    while flag==1:
        try:
            r=requests.get(url,headers=headers)
        except:
            print ("IP被封等待中！")#等着IP解封接着爬
            pbar = ProgressBar(maxval=10).start()
            for i in range(1,11):
                pbar.update(i)
                time.sleep(1)
            pbar.finish()
        else:
            flag=0
            
    r.encoding=r.apparent_encoding
    text=r.text
    return text

def getHTMLcontent(s): #对内容进行修改 不要的部分删掉
    end=len(s)-184
    s=s[19:end]
    s=s.replace("<br />","\r\n")
    s=s.replace("<br/>","\r\n")
    s=s.replace("&nbsp;"," ")
    try:
        s=s.replace("[]"," ")
    except:
        time.sleep(0)
    return s

def outputTXT(url,book): #导出TXT
    
    host='http://www.xbiquge.la'
    bs=BeautifulsoupHtml(renderHTML(url))
    for i in bs.find_all('a'):
        if i.get_text()=="下一章":
            url=i.attrs['href']
            url=host+url
            print("下一章："+url)
            break
    title=str(bs.select("#wrapper > div.content_read > div > div.bookname > h1"))#小说章标题
    title=title.replace("[<h1>","")
    title=title.replace("</h1>]","")#把两遍标签去掉
    print (title)
    writeTXTcontent(title,book)
    writeTXTcontent(getHTMLcontent(str(bs.select("#content"))),book)#写入小说内容
    
    return url
          

def getTXT(book):
    flag=0
    headers={
        'Cookie': '_abcde_qweasd=0; _abcde_qweasd=0',
        'Host': 'www.xbiquge.la',
        'Origin': 'http://www.xbiquge.la',
        'Referer': 'http://www.xbiquge.la/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    }
    
    data={'searchkey':book} #搜索书名post数据用的就是searchkey
    r=requests.post(url="http://www.xbiquge.la/modules/article/waps.php",data=data,headers=headers,timeout=10)
    r.encoding=r.apparent_encoding
    text=r.text.encode("UTF-8")
    bs = BeautifulSoup(text,"html.parser")
    url=bs.select("#checkform > table > tbody > tr:nth-child(2) > td:nth-child(1) > a")#找文章地址
    try:
        for i in bs.find_all("a"):
            if i.text==book: #小说名完全匹配
                url=i.attrs['href']
                s=url
                print ("文章地址："+url)
                break
        r=requests.get(url,headers=headers,timeout=30)
    except:
        print("未找到小说，请确认输入与小说名完全一致。")
        return flag
    else: flag=1
    '''for u in bs.find_all('a'):
        soup.find_all('a'):
        url = u['href']
        print href'''

    r.encoding=r.apparent_encoding
    text=r.text.encode("UTF-8")
    bs = BeautifulSoup(text,"html.parser")
    url=bs.select("#list > dl > dd:nth-child(1) > a")
    host='http://www.xbiquge.la'
    for i in bs.find_all("a"):
        if (i.text.count("第一章")!= 0) or (i.text.count("第1章")!= 0):
            url=i.attrs['href']
            url=host+url
            print ("第一章链接："+url)
            break
    while len(url) != len(s):#下一章结束标志 下一章链接为文章链接
        url=outputTXT(url,book)
    flag=2
    return flag
headers={
    
    'Cookie': '_abcde_qweasd=0; _abcde_qweasd=0',
    'Host': 'www.xbiquge.la',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
}    
url="http://www.xbiquge.la/10/10489/4534454.html"

book=input("请输入书名：")
t=getTXT(book)
if t==2:
    print(book+".txt完成！")
input("回车键结束")

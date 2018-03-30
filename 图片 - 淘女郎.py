#coding = utf-8
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.error import HTTPError
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
import sys,os
import re

savepath=r"E:\pictures\save"
# 创建保存目录
def mkdir(path):
    if os.path.exists(path):
        return
    os.mkdir(path)

def getUrls(url):
    driver= webdriver.PhantomJS(executable_path=r'D:\Python练习\库\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    # # 查找class属性为lady-name的标签，然后取其href属性来获取各个模特各自的页面地址。
    html = urlopen(url).read().decode('gbk')
    bs = BeautifulSoup(html,"html.parser") # 前面是要解析的内容，后面的'html.parser'是指定解析器的意思。因为beautiful有不止一种解析器可以去解析内容
    girls = bs.findAll("a",{"class":"lady-name"})
    print(type(girls))
    namewithurl = {}
    # 提取模特的个性域名，组装其访问地址
    for item in girls:
        linkurl = item.get('href')  # 获取 link 的  href 属性内容
        driver.get("https:"+linkurl)
        bs1 = BeautifulSoup(driver.page_source,"html.parser")
        links = bs1.find("div",{"class":"mm-p-info mm-p-domain-info"})
        if links is not None:
            links = links.li.span.get_text()
            namewithurl[item.get_text()] = links
            print(links)
    return namewithurl

# 获取模特的图片
def getImgs(parms):
    personname = parms[0]
    personurl = "https:"+parms[1]
    html = urlopen(personurl).read().decode('gbk')
    bs = BeautifulSoup(html,"html.parser")
    contents = bs.find("div",{"class":"mm-aixiu-content"})
    imgs = contents.findAll("img",{"src":re.compile(r'//img\.alicdn\.com/.*\.jpg')})
    # 保存图片
    savefilename = os.path.join(savepath,personname)
    mkdir(savefilename)
    print("img num :",len(imgs))
    cnt = 0
    for img in imgs:
        try:
            urlretrieve(url = "https:"+img.get("src"),filename =os.path.join(savefilename,str(cnt)+".jpg"))
            cnt+=1
        except HTTPError as e:
            continue

#getUrls("https://mm.taobao.com/json/request_top_list.htm?page=1")
if __name__ == "__main__":
    mkdir(savepath)
    pagenum = 1
    for i in range(1,pagenum):
        urls = getUrls("https://mm.taobao.com/json/request_top_list.htm"+"?page="+str(i))
        pool = ThreadPool(4) #开启4个线程，https://blog.csdn.net/seetheworld518/article/details/49639651
        pool.map(getImgs,urls.items()) # 使进程阻塞直到返回结果
        pool.close() # 关闭进程池（pool），使其不在接受新的任务
        pool.join() # 等待子进程的退出
        # for (k,v) in urls.items():
        #     getImgs((k,v))
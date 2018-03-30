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


# 创建保存目录
def mkdir(path):
    if os.path.exists(path):
        return
    os.mkdir(path)

def getUrls(url):
    #driver= webdriver.PhantomJS(executable_path=r'D:\Python练习\库\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    # 查找class属性为item-link的标签，然后取其href、userId属性来获取各个模特各自的页面地址。
    html = urlopen(url).read().decode('gbk')
    print(html)
    bs = BeautifulSoup(html,"html.parser")
    girls = bs.findAll("a",{"class":"item-link"})
    print(girls)
    #girl_id = bs.findAll("a",{c})
    namewithurl = {}
    # 提取模特的个性域名，组装其访问地址
    for item in girls:
        linkurl = item.get('href')
        print(linkurl)
    #     driver.get("https:"+linkurl)
    #     bs1 = BeautifulSoup(driver.page_source,"html.parser")
    #     links = bs1.find("div",{"class":"mm-p-info mm-p-domain-info"})
    #     if links is not None:
    #         links = links.li.span.get_text()
    #         namewithurl[item.get_text()] = links
    #         print(links)
    # return namewithurl

def getImgs(parms):
    personname = parms[0]
    personurl = "https:"+parms[1]
    html = urlopen(personurl)
    bs = BeautifulSoup(html.read().decode('gbk'),"html.parser")
    contents = bs.find("div",{"class":"mm-aixiu-content"})
    imgs = contents.findAll("img",{"src":re.compile(r'//img\.alicdn\.com/.*\.jpg')})
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

if __name__ == "__main__":
    url = r'https://mm.taobao.com/search_tstar_model.htm?spm=5679.126488.640745.2.1b545b81JfmyGS&style=&place=city%3A'
    #savepath = r"E:\pictures\save"
    #mkdir(savepath)
    getUrls(url)


    # pagenum = 10
    # for i in range(1,pagenum):
    #
    #     # https://mm.taobao.com/self/aiShow.htm?spm=719.7763510.1998643336.2.NvmBRe&userId=362438816
    #     # https://mm.taobao.com/self/aiShow.htm?spm=719.7763510.1998643336.1.NvmBRe&userId=176817195
    #
    #     # https://mm.taobao.com/json/request_top_list.htm
    #     urls = getUrls("https://mm.taobao.com/json/request_top_list.htm"+"?page="+str(i))
    #
    #     pool = ThreadPool(4)
    #     pool.map(getImgs,urls.items())
    #     pool.close()
    #     pool.join()
    #     # for (k,v) in urls.items():
    #     #     getImgs((k,v))
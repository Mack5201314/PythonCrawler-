import urllib.request
from bs4 import BeautifulSoup
from urllib.request import URLError
from urllib.request import HTTPError
import time
import re
# 调用 publicHeaders 文件的方法
from 爬虫.publicHeaders import set_user_agent


# 抓取网页
def download(pagenum):
    url = r'https://www.qiushibaike.com/hot/page/'
    stories = []
    # 分页下载
    for i in range(1,pagenum):
        #组装url
        new_url = url + str(pagenum)
        print(new_url)
        # 有的时候访问某个网页会一直得不到响应，程序就会卡到那里，我让他1秒后自动超时而抛出异常
        header = set_user_agent()
        while 1:
            try:
                req = urllib.request.Request(url=new_url,headers=header)
                reponse = urllib.request.urlopen(req,timeout=1)
                break
            # HTTPError是URLError的子类，在产生URLError时也会触发产生HTTPError。因此应该先处理HTTPError
            except HTTPError as e:
                print(e.code)
                # 对于抓取到的异常，让程序停止1.1秒，再循环重新访问这个链接，访问成功时退出循环
                time.sleep(1.1)
            except URLError as err:
                print(err.reason)
        # 正常访问，则抓取网页内容
        html = reponse.read().decode('utf-8')
        pattern = re.compile('<div class="author clearfix">.*?<h2>(.*?)</h2>.*?<div.*?span>(.*?)</span>(.*?)<div class="stats">.*?"number">(.*?)</i>', re.S)
        items = re.findall(pattern, html)
        for item in items:
            #print(item)
            haveImg = re.search("img", item[2])
            if not haveImg:
                stories.append([item[0], item[1], item[3]])

                #print(stories.append([item[0], item[1], item[3]]))

    return stories

def printStory(story):
    for item in story:
        print("发布人:%s点赞数:%s\n段子:%s" %(item[0], item[2], item[1]))


printStory(download(3))

"""
如上图所示，划红对勾的是不同的段子，每个段子都由<div class="article block untagged mb15" id="...">...</div>包裹起来。我们点开其中一个，获取其中的用户名、段子内容和点赞数这三个信息。这三个信息分别用红、蓝、黑下划线圈起来。解析过程主要由正则表达式实现。
解析用户名。正则表达式为：<div class="author clearfix">.*?<h2>(.*?)</h2>   上图中用户名称为旖旎萌萌，处于<h2>和</h2>中间，用(.*?)代之。
解析段子内容。正则表达式为：<div.*?span>(.*?)</span>  同理，文字部分在<span>和</span>之间。<div .........span>之间的所有符号（含换行符）用.*?解决。
解析点赞数。正则表达式为：<div class="stats">.*?"number">(.*?)</i>  同理。用(.*?)代替1520。
正则表达式解释：（参考崔庆才博客）
1）.*? 是一个固定的搭配，.和*代表可以匹配任意无限多个字符，加上？表示使用非贪婪模式进行匹配，也就是我们会尽可能短地做匹配，以后我们还会大量用到 .*? 的搭配。
2）(.*?)代表一个分组，在这个正则表达式中我们匹配了五个分组，在后面的遍历item中，item[0]就代表第一个(.*?)所指代的内容，item[1]就代表第二个(.*?)所指代的内容，以此类推。
3）re.S 标志代表在匹配时为点任意匹配模式，点 . 也可以代表换行符。
"""
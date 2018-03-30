import urllib.request
from bs4 import BeautifulSoup
from urllib.request import URLError
from urllib.request import HTTPError
import time
# 调用 publicHeaders 文件的方法
from 爬虫.publicHeaders import set_user_agent


# 抓取网页
def download(pagenum):
    url = r'https://www.qiushibaike.com/hot/page/'

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
        # 找到所有的class名称为content 的div
        soup = BeautifulSoup(html,"html.parser")
        contents = soup.findAll("div",{"class":"content"})
        # # 循环遍历保存每一项,并保存
        with open("E:\JustForFun.txt", "w") as f:
            for item in contents:
                # 有些内容不是utf-8格式
                try:
                    each_story = item.get_text()
                #print(type(each_story))
                    f.writelines(each_story)
                except:
                    pass

download(3)

"""
urllib.request.urlopen(req,timeout=1)可能会产生error：主要有HTTPError和URLError。
产生URLError的原因可能是：
网络无连接，即本机无法上网
连接不到特定的服务器
服务器不存在

HTTPError是URLError的子类，利用urlopen方法发出一个请求时，
服务器上都会对应一个应答对象response，其中它包含一个数字”状态码”。
举个例子，假如response是一个”重定向”，需定位到别的地址获取文档，urllib将对此进行处理。常见的状态码：
200：请求成功      处理方式：获得响应的内容，进行处理
202：请求被接受，但处理尚未完成    处理方式：阻塞等待
204：服务器端已经实现了请求，但是没有返回新的信息。
如果客户是用户代理，则无须为此更新自身的文档视图。处理方式：丢弃
404：没有找到     处理方式：丢弃
500：服务器内部错误  服务器遇到了一个未曾预料的状况，
导致了它无法完成对请求的处理。一般来说，这个问题都会在服务器端的源代码出现错误时出现。

"""
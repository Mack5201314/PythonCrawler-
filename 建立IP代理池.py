import csv
import urllib.request
import re
from bs4 import BeautifulSoup
import random
#
# def IPspider(numpage):
#     with open('E://ips.csv', 'w') as csvfile:
#         writer = csv.writer(csvfile)
#         '''
#         先写入columns_name
#         writer.writerow(["index","a_name","b_name"])
#         写入多行用writerows
#         writer.writerows([[0,1,3],[1,2,3],[2,3,4]])'''
#
#     url = 'http://www.xicidaili.com/nn/'
#     user_agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; " \
#                  "SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"
#     headers = {'User-agent': user_agent}
#     for num in range(1, numpage + 1):
#         ipurl = url + str(num)
#         print('Now downloading the ' + str(num * 100) + ' ips')
#         request = urllib.request.Request(ipurl, headers=headers)
#         content = urllib.request.urlopen(request).read().decode('utf-8')
#
#         # 使用正则找到表格里的IP
#         res_str = re.compile(r'<table id="ip_list"><tbody>(.*?)</tbody></table>', re.M)
#         # # 获取表格内容
#         form = res_str.findall(content)
#         # # 循环遍历
#         print(form)
#         # for each in form:
#         #     print('each is :',each)
#         #     # 获取标题值，分析html发现都是<th>标签下
#         #     res_th = re.compile(r'<tr><th>(.*?)</th></tr>',re.M)
#         #     title = res_str.findall(each)
#         #     print('title is ',title)
#         # 使用正则找到表格标题
#         res_th = re.compile(r'<th(.*?)>(.*?)</th>', re.M)
#         title = res_th.findall(content)
#         print('title is ',title[1][1],title[2][1])
#         # 使用正则，找到IP和端口
#         # start = content.find(r'<tbody>')  # 起点记录查询位置
#         # end = content.find(r'</tbody>')
#         # infobox = content[start:end]
#         # print(infobox)
#         res_td = re.compile(r'<td >(.*?)</td>')
#
#
#         #
#         #
#         # bs = BeautifulSoup(content, 'html.parser')
#         # res = bs.find_all('tr')
#         # for item in res:
#         #     try:
#         #         temp = []
#         #         tds = item.find_all('td')
#         #         temp.append(tds[1].text.encode('utf-8'))
#         #         temp.append(tds[2].text.encode('utf-8'))
#         #         writer.writerow(temp)
#         #     except IndexError:
#         #         pass


def IPspider(numpage):
    with open('E:\\ips.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
    url = 'http://www.xicidaili.com/nn/'
    user_agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; " \
                  "SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"
    headers={'User-agent':user_agent}
    # 分页读取
    ipdict = {} #IP端口保存在字典中
    for num in range(1,numpage+1):
        # 观察可以发现每个分页的url都是“url+页码”的格式。
        ipurl=url+str(num)
        print('Now downloading the Page %d ...'%num)
        # 获取网页内容
        request=urllib.request.Request(ipurl,headers=headers)
        content=urllib.request.urlopen(request).read()
        # 创建BeautifulSoup对象
        bs=BeautifulSoup(content,'html.parser')
        res=bs.find_all('tr')
        for item in res:
            try:
                #temp=[]
                #tds=item.find_all('td')
                #temp.append(tds[1].text.encode('utf-8'))
                #print(tds[1].text)
                #temp.append(tds[2].text.encode('utf-8'))
                #writer.writerow(temp)
                tds = item.find_all('td')
                ipdict[tds[1].text] = tds[2].text
            except IndexError:
                    pass
    return ipdict

# 动态设置user agent:
def set_user_agent():
    agent_list = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]

    headers = {'User-Agent':random.choice(agent_list)}

    return headers


# 假设爬取前十页所有的IP和端口
#print(IPspider(1))
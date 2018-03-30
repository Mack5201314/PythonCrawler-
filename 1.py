import re
import urllib.request
import urllib.parse
import urllib.error as err
import time


# 下载 seed_url 网页的源代码
def download(url, num_retries=2):
    print('Downloading: ', url)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/63.0.3239.132 Safari/537.36'
    headers = {'User-Agent':user_agent}
    request = urllib.request.Request(url, headers=headers)
    try:
        response_html = urllib.request.urlopen(request).read().decode('utf-8')
    except err.URLError as e:
        print('Download error', e.reason)
        response_html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600: #hasattr() 函数用于判断对象是否包含对应的属性。
                # recursively retry 5xx HTTP errors 只有出现 5xx 错误码的时候，才执行重新下载程序
                download(url, num_retries-1)
    return response_html


# 获取 html 网页中所有的链接URL
def get_links(html):
    """Return a list of links from html
    """
    # a regular expression to extract all links from the webpage
    # re.IGNORECASE 让正则表达式忽略大小写，如[A-Z]也可以匹配小写字母了。
    # link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", content)
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    url_list = webpage_regex.findall(html)
    with open('E:\list_test.txt','w') as f:
        for each in url_list:
            f.write(each+'\n')
    return url_list


""" 功能：找出我们需要的url列表（1、满足我们需要的url格式 2、不能存在重复的url）， 这也是我们外部调用的方法。
思路：对get_links()匹配到的链接URL与link_regex 进行匹配，
如果链接URL里面有link_regex内容，就将这个链接URL放入到队列中，
下一次 执行 while crawl_queue: 就对这个 链接URL 进行同样的操作。
反反复复，直到 crawl_queue 队列为空，才退出函数。"""

def link_crawler(seed_url, link_regex):

    html = download(seed_url)
    url_list = get_links(html) # 获得seed_url下所有url
    crawl_queue = []  # 爬行队列,存放去重后的url
    # 判断是否满足格式，满足后再判断是否重复
    for link in url_list:
        # check if link matches expected regex
        if re.search(link_regex, link):
            # check if have already seen this link
            if link not in crawl_queue:
                crawl_queue.append(link)
    #print(crawl_queue)
    with open("E:\crawlerlist_test.txt",'w') as f:
        for each in crawl_queue:
            f.write(each+'\n')
    return crawl_queue

# 下载小说...
def download_stoy(crawl_list,header):

    # 创建文件流，将各个章节读入内存
    with open('E:\盗墓test22.txt', 'w',encoding='utf-8') as f:
        for each_url in crawl_list:
            # 有的时候访问某个网页会一直得不到响应，程序就会卡到那里，我让他0.6秒后自动超时而抛出异常
            while True:
                try:
                    request = urllib.request.Request(url=each_url, headers=header)
                    with urllib.request.urlopen(request, timeout=0.6) as response:
                        html = response.read().decode('utf-8')
                        break
                except:
                    # 对于抓取到的异常，让程序停止1.1秒，再循环重新访问这个链接，访问成功时退出循环
                    time.sleep(1.1)

            # 匹配文章标题
            title_req = re.compile(r'<h1>(.+?)</h1>')
            # 匹配文章内容，内容中有换行，所以使flags=re.S  re.S表示跨行匹配
            #content_req = re.compile(r'<div class ="content-body">(.+)</div>', re.S)
            content_req = re.compile(r'<p>(.*?)</p>', re.S)
            #"<div[^>]+>.+?<div>(.+?)</div></div>", re.I
            #content_req = re.compile(r'<div[^>]+>.+?<div>(.+?)</div></div>', re.S)
            # 获取标题
            title = title_req.findall(html)[0]
            # 获取内容
            content_test = content_req.findall(html)
            print('抓取章节>' + title)
            f.write(title + '\n')
            #print(content_test)
            for each in content_test:
                # 筛除不需要的的html元素
                str1 = each.replace('&ldquo;', ' ')
                str2 = str1.replace('&hellip;', ' ')
                str3 = str2.replace('&rdquo;',' ')
                f.write(str3 + '\n')

seed_url = "http://seputu.com/"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/63.0.3239.132 Safari/537.36'
headers = {'User-Agent': user_agent}
#link_regex = '/index|biji1|zanghaihua|hesui|daomubijichongqi'
link_regex = '.html'
#download(url = seed_url)
link_crawler = link_crawler(seed_url=seed_url, link_regex=link_regex)
download_stoy(link_crawler, header=headers)
"""扩展： 
互联网工程任务小组（英语：Internet Engineering Task Force，缩写为 IETF）
定义了HTTP错误的完整列表，详细内容到这个网站查看：
https://zh.wikipedia.org/wiki/HTTP%E7%8A%B6%E6%80%81%E7%A0%81 
从这个列表中，我们可以了解到：4XX 问题是客户端出现的问题；
5XX 问题是服务器出现了问题；而其他的，比如：1XX 是消息；2XX 是成功；3XX 是重定向。"""
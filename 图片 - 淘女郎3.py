import re
import urllib.request
import urllib.parse
import urllib.error as err
import time

# 思路，找出全部的url。。。
# 下载 seed_url 网页的源代码
def download(url, num_retries=2):
    print('Downloading: ', url)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/63.0.3239.132 Safari/537.36'
    headers = {'User-Agent':user_agent}
    request = urllib.request.Request(url, headers=headers)
    try:
        response_html = urllib.request.urlopen(request).read().decode('GBK')
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
    webpage_regex = re.compile('<a href=(.*?)</a>', re.IGNORECASE)
    # list of all links from the webpage
    url_list = webpage_regex.findall(html)
    with open('E:\淘女郎首页图片list.txt','w') as f:
        for each in url_list:
            f.write(each+'\n')
    return url_list


""" 功能：找出我们需要的url列表（1、满足我们需要的url格式 2、不能存在重复的url）， 这也是我们外部调用的方法。
思路：对get_links()匹配到的链接URL与link_regex 进行匹配，
如果链接URL里面有link_regex内容，就将这个链接URL放入到队列中，
下一次 执行 while crawl_queue: 就对这个 链接URL 进行同样的操作。
反反复复，直到 crawl_queue 队列为空，才退出函数。"""
def link_crawler2(seed_url, link_regex):

    crawl_queue = [seed_url]  # 爬行队列,将seed_url作为默认值
    # keep track which URL's have seen before
    seen = set(crawl_queue) #为避免爬取相同的链接

    while crawl_queue:
        url = crawl_queue.pop()  #pop() 函数用于移除列表中的一个元素（默认最后一个元素），并且返回该元素的值。
        html = download(url)
        url_list = get_links(html)
        for link in url_list:
            # check if link matches expected regex
            if re.match(link_regex, link):
                # form absolute link
                link = urllib.urlparse.urljoin(seed_url, link) #将基地址与一个相对地址形成一个绝对地址
                # check if have already seen this link
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)

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
    with open("E:\淘宝女郎crawlerlist.txt",'w') as f:
        for each in crawl_queue:
            f.write(each+'\n')
    return crawl_queue

url = r'https://mm.taobao.com/search_tstar_model.htm?spm=5679.126488.640745.2.1b545b81JfmyGS&style=&place=city%3A'
html = download(url= url)
get_links(html)
# 获取这个页面中的所有书籍名称 http://www.douban.com/tag/%E5%B0%8F%E8%AF%B4/?focus=book

import urllib.request as re
import urllib.parse as pr

url = "http://www.douban.com/tag/%E5%B0%8F%E8%AF%B4/?focus=book"
respose = re.urlopen(url)
html = respose.read().decode('utf-8')
print(html)
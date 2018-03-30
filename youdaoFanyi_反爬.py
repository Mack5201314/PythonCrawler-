# 反爬虫版

import urllib.parse
import urllib.request
import json
import random


#ipurl = 'http://www.whatismyid.com.tw/' # 查看自身IP的网站
url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
content = input("请输入要翻译的内容：")

data = {}
data['i']=content
data['doctype']='json'
data['keyfrom']='fanyi.web'
data['typoResult']='true'
data['from']='AUTO'
data['to']='AUTO'
data['smartresult']='dict'
data['client']='fanyideskweb'
data['salt']='1520416292076'
data['sign']='41fe7ea28425a0a4ceb88ab4c8609d13'
data['version']='2.1'
data['action']='FY_BY_CLICKBUTTION'
data['typoResult']='false'

'''
decode的作用是将其他编码的字符串转换成unicode编码，如str1.decode('gb2312')，表示将gb2312编码的字符串str1转换成unicode编码。
encode的作用是将unicode编码转换成其他编码的字符串，如str2.encode('gb2312')，表示将unicode编码的字符串str2转换成gb2312编码。
'''
data = urllib.parse.urlencode(data).encode('utf-8')
# 设置代理
# http://www.xicidaili.com/ 免费代理IP 网站
IP_list = ['121.31.137.244:8123','171.39.31.9:8123','119.164.20.193:8118','58.216.202.149:8118']
proxy_support = urllib.request.ProxyHandler({'http':random.choice})
opener = urllib.request.build_opener(proxy_support)
opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')]
urllib.request.install_opener(opener)
#response = urllib.request.urlopen(url)

# 请求网页
response = urllib.request.urlopen(url,data)
html = response.read().decode('utf-8')
print(html)

ta = json.loads(html)  # json.loads()用于将str类型的数据转成dict。
print(ta['translateResult'][0][0]['tgt'])
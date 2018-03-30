# 无反爬
import urllib.parse
import urllib.request
import json


content = input('请输入需要翻译的词语：')

url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
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
# 转换格式
data = urllib.parse.urlencode(data).encode('utf-8')
# 发送请求，带data就是post，不带data是get
response = urllib.request.urlopen(url,data)
# 转码
html = response.read().decode('utf-8')
print(html)
# ta = json.loads(html)  # json.loads()用于将str类型的数据转成dict。
# print(ta['translateResult'][0][0]['tgt'])
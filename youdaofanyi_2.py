import urllib.request
import urllib.parse
import time
import hashlib #提供了常见的摘要算法
import json
url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom=null'  #上一次群里面那个失效了 把_o去掉就可以了

# 找出每次提交都变化的值
u = 'fanyideskweb'
d = input('请输入翻译的内容：')
# js的代码： f = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10)),
# 通过13位的时间戳加上一个随机的个位数
# python 中的时间戳是 10位加小数点，可以乘以 1000 取整
f = str(int(time.time()*1000))

c = "rY0D^0'nM0}g5Mm1z%1G4"
g = hashlib.md5()
g.update((u + d + f + c).encode('utf-8'))
# 组装head
head = {}
head['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'
head['Host'] = 'fanyi.youdao.com'
head['Referer'] = 'http://fanyi.youdao.com/'
# 组装data
data = {}
data['i'] = d  # 这是我们要翻译的字符串
data['from'] = 'AUTO'
data['to'] = 'AUTO'
data['smartresult'] = 'dict'
data['client'] = u
data['salt'] = f   # 当前时间戳。
data['sign'] = g.hexdigest() # 签名字符串。
data['doctype'] = 'json'
data['version'] = '2.1'
data['keyfrom'] = 'fanyi.web'
data['action'] = 'FY_BY_CL1CKBUTTON'
data['typoResult'] = 'true'
data = urllib.parse.urlencode(data).encode('utf-8')

req = urllib.request.Request(url, data, head)  # 用Request类构建了一个完整的请求，增加了headers等一些信息
response = urllib.request.urlopen(req)
html = response.read().decode('utf-8')
target = json.loads(html)
print(target)
print('翻译结果： %s ' % (target['translateResult'][0][0]['tgt']))
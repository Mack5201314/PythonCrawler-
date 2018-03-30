import urllib.request as re

respose = re.urlopen("http://placekitten.com/g/500/600")
pict = respose.read()

with open('E:\\catpict.jpg','wb') as f:
    f.write(pict)

# respose.geturl()
# respose.code()
# respose.info()
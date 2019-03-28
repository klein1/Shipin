import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
url = "https://www.google.com"
proxy_dict = {
    # "http": "http://username:password@hogehoge.proxy.jp:8080/",
    # "https": "http://username:password@hogehoge.proxy.jp:8080/"
    "http:":'117.68.192.78:18118',
    "https:":'117.68.192.78:18118'
}
try:
    # html = requests.get(url, headers=headers).text

    # print(html)
    pass
except Exception as e:
    print('error:',e)

import urllib.parse, base64
from PIL import Image

# import urllib.request
# proxy = urllib.request.ProxyHandler({'http': 'www.google.com:1'})
# auth = urllib.request.HTTPBasicAuthHandler()
# opener = urllib.request.build_opener(proxy, auth, urllib.request.HTTPHandler)
# urllib.request.install_opener(opener)
# print(urllib.request.urlopen("https://www.baidu.com/").read())

img = requests.get('https://i.ytimg.com/vi/3zNKzFuPxtU/hqdefault.jpg?sqp=-oaymwEYCKgBEF5IVfKriqkDCwgBFQAAiEIYAXAB&rs=AOn4CLBLYMfKV6gM-W_cp2v59sjxSjkYLA').content
print(img)
print(base64.b64encode(img))
print(bytes.decode(base64.b64encode(img)))
# print(urllib.parse.quote(img))

# img = Image.open('a.jpg')
# print(img)
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
    html = requests.get(url, headers=headers).text

    print(html)
except Exception as e:
    print('error:',e)

# import urllib.request
# proxy = urllib.request.ProxyHandler({'http': 'www.google.com:1'})
# auth = urllib.request.HTTPBasicAuthHandler()
# opener = urllib.request.build_opener(proxy, auth, urllib.request.HTTPHandler)
# urllib.request.install_opener(opener)
# print(urllib.request.urlopen("https://www.baidu.com/").read())

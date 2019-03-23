# coding:utf-8

import re
import urllib.request


def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html


def getUrl(html):
    reg = r"(?<=a\shref=\"/watch).+?(?=\")"
    urlre = re.compile(reg)
    urllist = re.findall(urlre, html.decode('utf-8'))
    format = "https://www.youtube.com/watch%s\n"
    f = open("E:\output.txt", 'a')
    for url in urllist:
        result = (format % url)
        f.write(result)
    f.close()


pages = 10
for i in range(1, pages):
    html = getHtml("https://www.youtube.com/results?search_query=lion+king&lclk=short&filters=short&page=%s" % i)
    print(html)
    getUrl(html)
    i += 1
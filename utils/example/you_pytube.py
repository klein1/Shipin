# coding: utf-8
__author__ = "SK"
__date__ = "2017-03-19"
# https://pypi.org/project/pytube/#description

import urllib.request
from pytube import YouTube
from pprint import pprint
from lxml import html as hl
import sys, getopt


def getHtml(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.0 Safari/537.13'
    headers = {'User-Agent': user_agent}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read()
    return html


def getUrl(html):
    global savepath
    global maxNumber
    global timeThreshold
    global cur_count
    global videoLists
    etree = hl.etree
    tree = etree.HTML(html)
    urllist = tree.xpath(u'//div[@class="thumb-wrapper"]/a/@href')
    # print urllist
    urllist_time = tree.xpath(u'//div[@class="thumb-wrapper"]/a/span/span/text()')

    baseurl = r'https://www.youtube.com'
    for (item_name, item_length) in zip(urllist, urllist_time):
        # print item_name
        # print item_length
        try:
            yt = YouTube(baseurl + item_name)
        except:
            print("Some thing wrong about the authority")

        print("video name:" + yt.filename)
        print("video time:" + item_length)
        if yt.filename in videoLists:  # 文件已经存在
            print
            "This video has been downloaded!"
        else:
            if checktime(item_length):
                video = yt.filter('mp4')[-1]
                print("Now is loading %s------------>" % yt.filename)
                # video.download(savepath)
                print("ttt----------" + video.url)
                print("--------------->%sVideo is loaded!" % yt.filename)
                # cur_count += 1
                # videoLists.append(yt.filename)
                # if cur_count >= maxNumber:  # 达到要求
                #    print('There are %d videos downloaded!This task is completed!' % maxNumber)
                # TODO: if necessary, the videoLists can be logged
                #    sys.exit()
            else:
                print('This video is too long and it will not be downloaded, just be ignored!')
    if urllist:
        getUrl(baseurl + urllist[0])  # 下一个页面


def checktime(timelength):
    global timeThreshold
    strs = timelength.split(':')
    time = int(strs[0]) * 60 + int(strs[1])
    if time < timeThreshold:
        return True
    else:
        return False


def usage():
    print(
    '''
    usage: python dl_youtube [option] [arg]
    options and args:
    -s      : download path
    -t      : time threshold of the video to be loaded, in seconds
    -u      : start url which to be crawled, it can be set more than one time
    -n      : when downloading is stop, i.e. how many videos will be downloaded, default is 10000.
    -h      : print this help message
    ''')


# python dl_youtube.py -n 10 -s D://MyDownloads -t 600 -u https://www.youtube.com/watch?v=TThzH_sJo6o
if __name__ == "__main__":
    start_urls = [
        'https://www.youtube.com/watch?v=ykmvaJ2Cf3w'
        # 'https://www.youtube.com/watch?v=TThzH_sJo6o'
        # "https: // www.youtube.com / watch?v = TThzH_sJo6o"
    ]
    videoLists = []  # 保存文件名，防止重复下载
    # 初始值
    savepath = r"E://视频//MyDownloads"
    maxNumber = 10000
    timeThreshold = 600
    cur_count = 0

    #
    #    opts, args = getopt.getopt(sys.argv[1:], 'hs:t:n:u:')
    #    for op, value in opts:
    #        if op == "-s":  # 下载路径，如默认 D://MyDownloads
    #            savepath = value
    #        elif op == '-t':  # 时常限制，默认240s
    #            timeThreshold = int(value)
    #        elif op == "-h":  # help
    #           usage()
    #            sys.exit()
    #        elif op == '-n':
    #            maxNumber = int(value)
    #        elif op == '-u':  # 初始的搜索链接
    #            start_urls.append(value)
    #
    for item in start_urls:
        html = getHtml(item)
        getUrl(html)

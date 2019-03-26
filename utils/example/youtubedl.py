# coding:utf8
from pytube import YouTube
import requests, json, re, logging, random
from requests.exceptions import ConnectTimeout,ConnectionError,ReadTimeout,SSLError,MissingSchema,ChunkedEncodingError
import subprocess
import youtube_dl
import time
from pytube import YouTube
import os
logger = logging.getLogger("AppName")
# 查询视频信息语句
# COMMAND_PREFIX_CHECK = 'youtube-dl -F '
# 下载1080p视频语句
# COMMAND_PREFIX_DOWNLOAD = 'youtube-dl -f 137+140 '
COMMAND_PREFIX_DOWNLOAD = 'youtube-dl '


# 传入url，加载相应的1080p视频
def download_by_url(url):
    p = subprocess.Popen(COMMAND_PREFIX_DOWNLOAD + url, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    start = time.time()
    print("********\tStart download:" + url + "\t" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start)))
    while True:
        line = p.stdout.readline()
        # print(line)
        if not line == '':
            pass
            # print(line.decode('gbk').strip('\n'))
        else:
            break
    p.wait()
    end = time.time()
    print("********\tEnd\t" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end)))
    print( "taking：" + str(int(end - start)) + " seconds")

def download(youtube_url):
    # 定义某些下载参数
    ydl_opts = {
        # outtmpl 格式化下载后的文件名，避免默认文件名太长无法保存
        'outtmpl': '%(id)s%(ext)s'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

def downlaod(url, name ,path):
    urlhash = "https://weibomiaopai.com/"
    try:
        html = requests.get(urlhash).text
    except SSLError:
        logger.info(u"网络不稳定 正在重试")
        html = requests.get(urlhash).text
    reg = re.compile(r'var hash="(.*?)"', re.S)
    result = reg.findall(html)
    hash_v = result[0]

    file = os.path.join(path, '%s' + ".mp4") % name
    api = "https://steakovercooked.com/api/video/?cached&hash=" + hash_v + "&video=" + url
    api2 = "https://helloacm.com/api/video/?cached&hash=" + hash_v + "&video=" + url
    try:
        res = requests.get(api)
        result = json.loads(res.text)
    except (ValueError, SSLError):
        try:
            res = requests.get(api2)
            result = json.loads(res.text)
        except (ValueError, SSLError):
            print('error')
            return False
    vurl = result['url']
    logger.info(u"正在下载：%s" % name)
    try:
        r = requests.get(vurl)
    except SSLError:
        r = requests.get(vurl)
    except MissingSchema:
        print('error')
    try:
        with open(file, 'wb') as f:
            f.write(r.content)
    except IOError:
        name = u'好开心么么哒 %s' % random.randint(1, 9999)
        file = os.path.join(path, '%s' + ".mp4") % name
        with open(file, 'wb') as f:
            f.write(r.content)
    logger.info(u"下载完成：%s" % name)

if __name__ == '__main__':
     # download('https://www.youtube.com/watch?v=a3MlEeNwvtk')
     # download_by_url('https://www.youtube.com/watch?v=dOSFOjYjWbo')
     # YouTube('https://www.youtube.com/watch?v=a3MlEeNwvtk').streams.first().download()
     # downlaod('https://www.youtube.com/watch?v=dOSFOjYjWbo','dOSFOjYjWbo','./')
     YouTube('https://www.youtube.com/watch?v=dOSFOjYjWbo').streams.first().download('../../static/video/search')

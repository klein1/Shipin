from requests.exceptions import ConnectTimeout, ConnectionError, ReadTimeout, SSLError, MissingSchema, ChunkedEncodingError
import os, random, requests, re, json
from urllib import parse

loading_set = set()

def register_download(socketio):
    namespace = "/download"

    @socketio.on('imessage', namespace=namespace)
    def test_message(message):
        id = message["data"]
        name = parse.unquote(message["name"])
        rename = re.sub('[\/:*?"<>|]',' ', name)
        path = 'static/video/search'

        if os.path.exists(path + '/' + rename + '.mp4'):
            file = '/' + path + '/' + rename + '.mp4'
        else:
            if rename not in loading_set:
                loading_set.add(rename)
                file = download(path, id, rename)
            else:
                file = ""
        if file:
            socketio.emit('message', {'file': file,'name':name}, namespace=namespace)

    def download(path, id, name):
        try:
            url = 'https://www.youtube.com/watch?v=' + id
            urlhash = "https://weibomiaopai.com/"
            try:
                html = requests.get(urlhash).text
            except SSLError:
                print(u"网络不稳定 正在重试")
                try:
                    html = requests.get(urlhash).text
                except SSLError:
                    print('step1 error')
                    loading_set.remove(name)
                    return "error"
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
                    print('step2 error')
                    loading_set.remove(name)
                    return "error"
            vurl = result['url']
            print(u"正在下载：%s" % name)

            try:
                r = requests.get(vurl)
            except SSLError:
                try:
                    r = requests.get(vurl)
                except SSLError:
                    print('step3.1 error')
                    loading_set.remove(name)
                    return "error"
            except MissingSchema:
                print('step3.2 error')
                loading_set.remove(name)
                return "error"

            try:
                if not os.path.exists(file):
                    with open(file, 'wb') as f:
                        f.write(r.content)
                    print(u"下载完成：%s" % name)

                loading_set.remove(name)
                return '/' + path + '/' + name + '.mp4'
            except IOError:
                print('step4 error')
                loading_set.remove(name)
                return "error"

        except Exception as e:
            print(e)
            loading_set.remove(name)
            return "error"
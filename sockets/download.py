from requests.exceptions import ConnectTimeout, ConnectionError, ReadTimeout, SSLError, MissingSchema, ChunkedEncodingError
import os, random, requests, re, json

def register_download(socketio):
    namespace = "/download"

    @socketio.on('imessage', namespace=namespace)
    def test_message(message):
        id = message["data"]
        path = 'static/video/search'
        if os.path.exists(path + '/' + id + '.mp4'):
            file = '/' + path + '/' + id + '.mp4'
        else:
            file = download(path, id)

        socketio.emit('message', {'data': file}, namespace=namespace)

    def download(path, id):
        url = 'https://www.youtube.com/watch?v=' + id
        urlhash = "https://weibomiaopai.com/"
        try:
            html = requests.get(urlhash).text
        except SSLError:
            print(u"网络不稳定 正在重试")
            html = requests.get(urlhash).text
        reg = re.compile(r'var hash="(.*?)"', re.S)
        result = reg.findall(html)
        hash_v = result[0]

        file = os.path.join(path, '%s' + ".mp4") % id
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
                return "error "
        vurl = result['url']
        print(u"正在下载：%s" % id)

        try:
            r = requests.get(vurl)
        except SSLError:
            r = requests.get(vurl)
        except MissingSchema:
            print('error')

        try:
            if not os.path.exists(file):
                with open(file, 'wb') as f:
                    f.write(r.content)
                print(u"下载完成：%s" % id)

            return '/' + path + '/' + id + '.mp4'
        except IOError:
            print('error')

        return 'error'
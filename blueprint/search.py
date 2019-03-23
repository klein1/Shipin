from flask import *
import requests, re, json
from requests.exceptions import ConnectTimeout, ConnectionError, ReadTimeout, SSLError, MissingSchema, \
    ChunkedEncodingError

bp = Blueprint('search', __name__, url_prefix="/search")

@bp.route('/')
def index():
    return render_template("search/index.html")


@bp.route('/<keyword>/<page>', methods=['GET'])
def search(keyword, page):
    msg = ""
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    url = "https://www.youtube.com/results?search_query=" + keyword + "&page=" + str(page)
    try:
        html = requests.get(url, headers=headers).text
    except (ConnectTimeout, ConnectionError):
        msg = u"网络错误，请确保科学上网"
        return msg

    url_list = re.compile(r'"url":"/watch\?v=(.*?)","webPageType"', re.S).findall(html)

    data_from = html.find('window["ytInitialData"] =')
    data_to = html.find('window["ytInitialPlayerResponse"]')
    if data_from > 0 and data_to > data_from:
        data = json.loads(html[data_from + 26:data_to - 6])
        result = []

        for item in data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]:
            if 'videoRenderer' in item:
                result.append({'img':item['videoRenderer']['thumbnail']['thumbnails'][0]['url'],'title':item['videoRenderer']['title']['simpleText'],'id':item['videoRenderer']['videoId'] })

        if len(result) > 0:
            msg = str(result)
        else:
            msg = u"找不到搜索结果"
    else:
        msg = u"网络开小差了，请重试"

    return msg
from flask import *
import requests, re, json


bp = Blueprint('search', __name__, url_prefix="/search")

@bp.route('/')
def index():
    return render_template("search/default.html")

@bp.route('/<keyword>/<int:page>', methods=['GET'])
def search(keyword, page):
    msg = ""
    returnNo = '000'
    result = []
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    url = "https://www.youtube.com/results?search_query=" + keyword + "&page=" + str(page)
    try:
        requests.get('https://www.google.com', headers=headers)
        html = requests.get(url, headers=headers).text
    # except (ConnectTimeout, ConnectionError):
    except Exception as e:
        msg = u"网络错误，请确保科学上网"
        return render_template('search/index.html', message=msg, returnNo=returnNo, data=result, keyword=keyword, page=page)

    url_list = re.compile(r'"url":"/watch\?v=(.*?)","webPageType"', re.S).findall(html)

    data_from = html.find('window["ytInitialData"] =')
    data_to = html.find('window["ytInitialPlayerResponse"]')

    if data_from > 0 and data_to > data_from:
        data = json.loads(html[data_from + 26:data_to - 6])

        for item in data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]:
            if 'videoRenderer' in item:
                dict = {'img':'','title':'','id':'','description':'','publishtime':'','viewcount':'','linetext':'' }
                if 'thumbnail' in item['videoRenderer']:
                    dict['img'] = item['videoRenderer']['thumbnail']['thumbnails'][0]['url']
                if 'title' in item['videoRenderer']:
                    dict['title'] = item['videoRenderer']['title']['simpleText']
                if 'videoId' in item['videoRenderer']:
                    dict['id'] = item['videoRenderer']['videoId']
                if 'descriptionSnippet' in item['videoRenderer'] and 'simpleText' in item['videoRenderer']['descriptionSnippet']:
                    dict['description'] = item['videoRenderer']['descriptionSnippet']['simpleText']
                if 'publishedTimeText' in item['videoRenderer']:
                    dict['publishtime'] = item['videoRenderer']['publishedTimeText']['simpleText']
                if 'viewCountText' in item['videoRenderer']:
                    dict['viewcount'] = item['videoRenderer']['viewCountText']['simpleText']
                if 'longBylineText' in item['videoRenderer']:
                    dict['linetext'] = item['videoRenderer']['longBylineText']['runs'][0]['text']
                result.append(dict)

        if len(result) > 0:
            returnNo = '111'
        else:
            msg = u"找不到搜索结果"
    else:
        msg = u"网络开小差了，请重试"

    return render_template('search/index.html',message=msg,returnNo=returnNo,data=result, keyword=keyword, page=page)

@bp.route('/watch/<id>', methods=['GET'])
def watch(id):
    return render_template('search/player.html', id = id)


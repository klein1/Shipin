import json

with open("data.txt", "r", encoding="utf-8") as f:
    data = json.loads(f.read())

print(len(data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]))

for item in data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]:
    # print(item['videoRenderer']['title']['simpleText'],item['videoRenderer']['videoId'],item['videoRenderer']['thumbnail']['thumbnails'][0]['url'],item['videoRenderer']['longBylineText']['runs'][0]['text'],item['videoRenderer']['descriptionSnippet']['simpleText'])
    if 'descriptionSnippet' in item['videoRenderer'] and 'simpleText' in item['videoRenderer']['descriptionSnippet']:
        print(item['videoRenderer'].get('descriptionSnippet').get('simpleText'))
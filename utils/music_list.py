import os, json

def getMusic(path):
    music_list = []
    list = os.listdir(path)
    for file in list:
        with open(path + "/" + file, "r",encoding = 'utf-8') as f:
            load_dict = json.load(f)
        music_list.append(load_dict)

    music_list.sort(key=lambda x: x["date"])
    # print(music_list)
    return music_list[::-1]

if __name__ == "__main__":
    getMusic('../static/upload')
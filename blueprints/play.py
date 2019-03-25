from flask import *
from utils.func import random_name, file_extension, now
from utils.video_frame import capture
from utils.music_list import getMusic

bp = Blueprint('play',__name__,url_prefix="/play")

@bp.route('/upload', methods=['GET'])
def upload():
    return render_template('play/upload.html')
    # return '''<form action="/music/upload" method="post" enctype="multipart/form-data">
    #           <p><input name="header"></p>
    #           <p><input name="description"></p>
    #           <p><input name="author"></p>
    #           <p><input type="file" name="image"></p>
    #           <p><input type="file" name="video"></p>
    #           <p><button type="submit">upload</button></p>
    #           </form>'''

@bp.route('/music/upload', methods=['POST'])
def doupload():
    id = random_name()

    video = request.files['video']
    video.save('static/video/' + id  + file_extension(video.filename))

    # image = request.files['image']
    # image.save('static/image/' + id + file_extension(image.filename))

    image = 'static/image/' + id + '.jpg'
    capture('static/video/' + id  + file_extension(video.filename), image)

    data = {
        "author": request.form["author"],
        "date": now(),
        "image": "/" + image,
        "video": "/static/video/" + id  + file_extension(video.filename),
        "title": request.form["title"]
        # "description": request.form["description"]
    }
    with open("static/upload/" + id + ".json", "w") as f:
        json.dump(data, f)

    return redirect(url_for('play.index'))


@bp.route('/')
def index():
    music_list = getMusic('static/upload')
    return render_template('play/player.html', musicList=music_list)
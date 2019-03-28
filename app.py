from flask import *
from flask_socketio import SocketIO
from blueprints import play, rch, search
from sockets import comment, download

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df$gnd@fg#$0#hao'

# app.add_url_rule('/favicon.ico',endpoint='favicon', redirect_to=url_for('static', filename='img/favicon.ico'))

@app.route('/')
def index():
    return redirect(url_for("play.index"))

@app.route('/main')
def main():
    return render_template("web.html")

app.register_blueprint(play.bp)
app.register_blueprint(rch.bp)
app.register_blueprint(search.bp)

socketio = SocketIO(app)
comment.register_comment(socketio)
download.register_download(socketio)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80, debug=True, threaded='True')
    socketio.run(app, host='0.0.0.0', port=80, debug=True)

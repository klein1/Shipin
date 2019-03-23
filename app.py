from flask import *
from flask_socketio import SocketIO
from blueprint import play
from blueprint import rch
from blueprint import search

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df$gnd@fg#$0#hao'

# app.add_url_rule('/favicon.ico',endpoint='favicon', redirect_to=url_for('static', filename='img/favicon.ico'))

@app.route('/')
def index():
    return redirect(url_for("play.index"))

@app.route('/test')
def test():
    return render_template("web.html")

app.register_blueprint(play.bp)
app.register_blueprint(rch.bp)
app.register_blueprint(search.bp)

namespace = "/comment"
socketio = SocketIO(app)
@socketio.on('imessage', namespace=namespace)
def test_message(message):
    socketio.emit('message',{'data': message['data']},broadcast=True, namespace=namespace)

@socketio.on('connect', namespace=namespace)
def connected_msg():
    """socket client event - connected"""
    socketio.emit('message', {'data': '系统消息：欢迎进入！！！'}, broadcast=True, namespace=namespace)
    print('client connected!')

@socketio.on('disconnect', namespace=namespace)
def disconnect_msg():
    """socket client event - disconnected"""
    # socketio.emit('message', {'data': '系统消息：有人离开了！！！'}, broadcast=True, namespace=namespace)
    print('client disconnected!')

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80, debug=True, threaded='True')
    socketio.run(app, host='0.0.0.0', port=80, debug=True)

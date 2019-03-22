from flask import Flask, render_template
from flask_socketio import SocketIO

namespace = "/chat"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('web.html')

@socketio.on('imessage', namespace=namespace)
def test_message(message):
    socketio.emit('message',{'data': message['data']},broadcast=True, namespace=namespace)

@socketio.on('connect', namespace=namespace)
def connected_msg():
    """socket client event - connected"""
    print('client connected!')

@socketio.on('disconnect', namespace=namespace)
def disconnect_msg():
    """socket client event - disconnected"""
    print('client disconnected!')

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=5000, debug=True)
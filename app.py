from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
from light_thread import light_thread
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
thread = light_thread(1)
thread.set_method('rainbow')
thread.start()


"""
It will bring all the info about the lights
"""
@app.route('/')
def index():
    parameters = thread.get_parameters()
    return json.dumps(parameters)


@socketio.on('light')
def handleMessage(msg):
    data = (msg['data'])
    method = data['method']
    color = (data['red'], data['green'], data['blue'])
    thread.set_method(method)
    thread.set_color(color)
    thread.reset_active_pixel()
    emit('light', msg, broadcast=True)


@socketio.on('speed')
def handleSpeed(speed):
    thread.set_speed(speed)
    emit('speed', speed, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',port=3000)

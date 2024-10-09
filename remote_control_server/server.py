from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('frame')
def handle_frame(frame_data):
    emit('frame', frame_data, broadcast=True)

@socketio.on('command')
def handle_command(command):
    emit('command', command, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)  # Adjust port if necessary


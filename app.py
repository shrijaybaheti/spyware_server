from flask import Flask, render_template
from flask_socketio import SocketIO
import os

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('command')
def handle_command(data):
    # Send command to the client script
    socketio.emit('command', {'command': data['command']})

if __name__ == '__main__':
    # Make sure to set the host and port according to your deployment
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

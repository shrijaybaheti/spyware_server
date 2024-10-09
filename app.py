import cv2
import numpy as np
import pyautogui
from flask import Flask, Response
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames():
    while True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@socketio.on('command')
def handle_command(data):
    if data.startswith('/click'):
        coords = data.split('(')[1].strip(')').split(',')
        x, y = int(coords[0]), int(coords[1])
        pyautogui.click(x, y)
        
    elif data.startswith('/type'):
        text = data.split('"')[1]
        pyautogui.typewrite(text)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from sensors.gyro import get_data
import time
import threading
app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template("index.html") #Load HTML file

@socketio.on("connect")
def on_connect():
    print("[INFO] PC connected!")
    # Send the stream in another thread

    thread = threading.Thread(target=gyro_event, daemon=True)
    thread.start() 

@socketio.on("command")
def on_command(data):
    #print(data)
    print(data["action"])  # "forward"
    print(data["speed"])   # 60


def gyro_event():
    while True:
        data = get_data()
        socketio.emit("gyro", data)
        time.sleep(0.05)  

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)


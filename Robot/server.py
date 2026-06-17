import threading
import time
import logging
import atexit

from flask import Flask, render_template, request
from flask_socketio import SocketIO

from sensors.gyro import get_data
from sensors.radar import run_scan
from motors.motor_control import move_forward, move_backward, turn_left, turn_right, stop, set_speed, cleanup

GYRO_SAMPLE_RATE = 0.05  # seconds (20 Hz)
HOST = "0.0.0.0"
PORT = 5000

logger = logging.getLogger(__name__)

app = Flask(__name__,
            template_folder="/home/enzon/interface/templates",
            static_folder="/home/enzon/interface/static")
socketio = SocketIO(app, cors_allowed_origins="*")

_active_streams: dict[str, threading.Thread] = {}
_scan_lock = threading.Lock()

# motors_init()
atexit.register(cleanup)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def on_connect(auth):
    sid = request.sid
    if sid in _active_streams and _active_streams[sid].is_alive():
        return

    thread = threading.Thread(
        target=_gyro_stream,
        args=(sid,),
        daemon=True,
        name=f"gyro-{sid[:8]}"
    )
    _active_streams[sid] = thread
    thread.start()
    logger.info("Client connected: %s", sid[:8])


@socketio.on("disconnect")
def on_disconnect(reason):
    sid = request.sid
    _active_streams.pop(sid, None)
    logger.info("Client disconnected: %s — %s", sid[:8], reason)


@socketio.on("command")
def on_command(data):
    action = data.get("action")
    speed = data.get("speed")
    if action is None or speed is None:
        return

    set_speed(speed)  # Définit la vitesse

    if action == "forward":
        move_forward()
    elif action == "backward":
        move_backward()
    elif action == "left":
        turn_left()
    elif action == "right":
        turn_right()
    elif action == "stop":
        stop()

    logger.info("[CMD] action=%s speed=%s", action, speed)

@socketio.on("start_scan")
def on_start_scan():
    sid = request.sid

    if not _scan_lock.acquire(blocking=False):
        socketio.emit("scan_status", {"status": "busy"}, to=sid)
        return

    def _run():
        try:
            socketio.emit("scan_status", {"status": "started"}, to=sid)
            run_scan(lambda point: socketio.emit("scan_point", point, to=sid))
            socketio.emit("scan_status", {"status": "complete"}, to=sid)
        finally:
            _scan_lock.release()

    threading.Thread(target=_run, daemon=True, name="radar-scan").start()


def _gyro_stream(sid: str):
    """Push gyroscope data to a specific session at GYRO_SAMPLE_RATE."""
    while True:
        data = get_data()
        if data is not None:
            socketio.emit("gyro", data, to=sid)
        time.sleep(GYRO_SAMPLE_RATE)


if __name__ == "__main__":
    socketio.run(app, host=HOST, port=PORT, allow_unsafe_werkzeug=True)
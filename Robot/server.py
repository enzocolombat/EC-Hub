from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return """
    <h1>Robot Server</h1>
    <script src="https://cdn.socket.io/4.6.0/socket.io.min.js"></script>
    <script>
        // JS côté navigateur — se connecte au serveur SocketIO
        const socket = io();
        
        socket.on('connect', () => {
            console.log('Connected to Pi!');
            document.body.innerHTML += '<p>Connected!</p>';
        });
    </script>
    """

@socketio.on("connect")
def on_connect():
    # Cette fonction s'exécute sur le Pi quand le navigateur se connecte
    print("[INFO] PC connected!")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
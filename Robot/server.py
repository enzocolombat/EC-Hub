from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from sensors.gyro import get_data
import time
import threading
app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template("index.html")  # charge le fichier HTML

@socketio.on("connect")
def on_connect():
    print("[INFO] PC connected!")
    # Lance le stream dans un thread séparé
    thread = threading.Thread(target=gyro_event, daemon=True)
    thread.start() 


def gyro_event():
    while True:
        data = get_data()
        socketio.emit("gyro", data)
        time.sleep(0.05)  

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)

#bajbdshpbfqhfshf
## TO DO : reconnecté le rasp en server , vérifié que le code est bien deployé , executé server sur le pi (derniere modif : on a supp les print de gyro pour voir si ça libère le terminal 
# et on aussi supp le consol log de socket on gyro dans server en javascript ) , checker les consoles et la page html si elle marche et demandé à claude pk la connection et la page de s'affiche plus (suspection boucle infinie)   
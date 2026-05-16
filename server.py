"""Send MPU6050 accelerometer and gyroscope data over a TCP socket."""

import socket  # Provides the TCP server socket.
from mpu6050 import mpu6050  # Imports the MPU6050 helper class for I2C sensor access.
import json  # Converts sensor dictionaries to JSON text.
import time  # Controls the sending rate.

capteur = mpu6050(0x68)  # Creates the sensor object at the usual MPU6050 I2C address.
HOST = '0.0.0.0'  # Listens on every network interface of the Raspberry Pi.
PORT = 5000  # Uses port 5000 for the sensor data stream.

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates a TCP/IPv4 server socket. wifi stream by tcp
server.bind((HOST, PORT))  # Attaches the server socket to the chosen host and port.
server.listen(1)  # Waits for one client connection at a time.
print("Waiting a connection...")  # Tells the user that the server is ready.

conn, addr = server.accept()  # Blocks until a client connects and returns the connection object.
print(f"Connected : {addr}")  # Displays the client address after connection.

try:  # Keeps the connection open until an error or interruption happens.
    while True:  # Continuously sends fresh sensor data.
        accel = capteur.get_accel_data()  # Reads acceleration on the X, Y, and Z axes.
        gyro = capteur.get_gyro_data()  # Reads angular speed on the X, Y, and Z axes.
        data = json.dumps({  # Builds one JSON object containing both accelerometer and gyroscope data.
            "ax": accel['x'], "ay": accel['y'], "az": accel['z'],  # Stores acceleration values in the JSON payload.
            "gx": gyro['x'], "gy": gyro['y'], "gz": gyro['z']  # Stores gyroscope values in the JSON payload.
        }) + "\n"  # Adds a newline so the client can split complete messages cleanly.
        conn.sendall(data.encode())  # Encodes the JSON text to bytes and sends all of it.
        time.sleep(0.05)  # Sends about 20 updates per second.
except Exception:  # Handles disconnects and other runtime errors by closing the connection.
    conn.close()  # Closes the client socket cleanly.

# Robotics-box 🤖

A Raspberry Pi 3B based robot with real-time web interface, environment mapping via ultrasonic radar, and gyroscope-driven orientation tracking. Built toward full autonomous navigation.

---

## Current State

### Working
- Real-time gyroscope streaming (MPU-6050 → Pi → Browser via SocketIO)
- 2D canvas map with robot orientation tracked from gyro Z axis
- Ultrasonic radar scan (HC-SR04P + MG90S servo) — obstacles plotted on the map in world space
- Web interface : keyboard controls, scan button, zoomable/scrollable map, follow cam
- DC motors + L298N driver wiring and control
### In Progress
- HC-020K encoders for real odometry
- AI-guided navigation

---

## Demo

https://github.com/user-attachments/assets/d559aa59-24a0-41e6-a908-c51b7c77f7f3

---

## Hardware

| Component | Role |
|---|---|
| Raspberry Pi 3B | Main controller |
| MPU-6050 | Gyroscope + accelerometer |
| HC-SR04P | Ultrasonic distance sensor |
| MG90S micro servo | Radar rotation |
| 2× L298N | Motor driver (pending) |
| 4× DC motors | Drive (pending) |
| 4× HC-020K encoders | Odometry (pending) |

### Electrical Diagram

<img width="3000" height="2824" alt="circuit_image(2)" src="https://github.com/user-attachments/assets/f32e12d7-b2ac-49c4-91d5-1cb5d116c669" />


https://app.cirkitdesigner.com/project/6bdb54de-5863-4ef8-af36-00f08ab2924f

---

## Stack

- **Pi side** — Python, Flask, Flask-SocketIO, RPi.GPIO
- **Browser side** — Vanilla JS (ES modules), Canvas 2D, Socket.IO client
- **Transport** — WebSocket (polling fallback)

---

## Installation

### Raspberry Pi

```bash
git clone https://github.com/enzocolombat/EnzoColombat-s-hub.git
cd EnzoColombat-s-hub
python3 -m pip install -r requirements-pi.txt --break-system-packages
```

Enable I2C:
```bash
sudo raspi-config  # Interface Options → I2C → Enable
```

### Run

```bash
cd Robot
python server.py
```

Then open `http://<pi-ip>:5000` in your browser.

---

## Project Structure

```
Robot/
├── server.py           # Flask + SocketIO server, session management
├── sensors/
│   ├── gyro.py         # MPU-6050 reader
│   └── radar.py        # Servo sweep + ultrasonic scan
└── motors/             # Coming soon

Interface/
├── templates/
│   └── index.html
└── static/
    ├── robot.js        # Robot state and physics
    ├── canvas.js       # Rendering, viewport, zoom
    ├── radar.js        # Obstacle plotting
    └── socket.js       # Network and input binding
```

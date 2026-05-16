# EnzoColombat's hub
Hub of my robotics projects
## Obstacle avoidance car

An autonomous robot built on Raspberry Pi 3B, capable of mapping its environment and being guided by artificial intelligence.

## Hardware Requirements

- Raspberry Pi 3B
- Gyroscope/Accelerometer MPU-6050
- Ultrasonic sensor HC-SR04P
- 2x Motor Driver L298N
- 4x DC Motors
- 4-wheel chassis

## Installation

### On the Raspberry Pi

```bash
git clone https://github.com/enzocolombat/EnzoColombat-s-hub.git
cd EnzoColombat-s-hub
pip install -r requirements-pi.txt
```
### On the PC

```bash
git clone https://github.com/enzocolombat/EnzoColombat-s-hub.git
cd EnzoColombat-s-hub
pip install -r requirements-pc.txt
```
## Getting Started

### 1. Start the server on the Pi
```bash
python robot/main.py
```

### 2. Launch the interface on the PC
```bash
python interface/app.py
```
heyhey
Then open `http://localhost:5000` in your browser.

## Features

- 🗺️ Real-time environment mapping
- 🎮 Web-based control interface
- 📊 Live gyroscope & accelerometer data
- 🤖 AI-guided navigation
- 🚗 Autonomous obstacle avoidance

## Project Structure
### Electrical diagram

<img width="3000" height="1995" alt="Electrical diagram" src="https://github.com/user-attachments/assets/ecfe6f4a-8edb-4343-bbda-1d64ff7cda23" />
https://app.cirkitdesigner.com/project/c312c10f-f63f-401c-b78d-33313f44d202

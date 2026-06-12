# Objective: Autonomous and useful robotics 🤖 🎯
Ce dépôt contient une collection de projets robotiques pour Raspberry Pi, incluant l'intégration de capteurs en temps réel et le contrôle via une interface web.
by Enzo Colombat
# Obstacle avoidance car

An autonomous robot built on Raspberry Pi 3B, capable of mapping its environment and being guided by artificial intelligence.
## Current State

### Working
- Real-time gyroscope data streaming (MPU-6050 → Pi → Browser)
- Bidirectional communication via Flask + SocketIO
- Robot simulation on 2D canvas (rotation via gyro Z axis)
- Keyboard controls (arrow keys) with visual feedback
- Command sending from browser to Pi (action + speed)

### Hardware
- Raspberry Pi 3B
- MPU-6050 (gyroscope + accelerometer)
- HC-SR04P ultrasonic sensor (pending integration)

### Coming Soon
- DC motors + L298N wiring and control
- HC-020K encoders for real odometry
- Ultrasonic sensor for obstacle detection and mapping
- AI guidance
### Interface 
https://github.com/user-attachments/assets/d559aa59-24a0-41e6-a908-c51b7c77f7f3

## Project
### Hardware Requirements

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
https://app.cirkitdesigner.com/project/6bdb54de-5863-4ef8-af36-00f08ab2924f

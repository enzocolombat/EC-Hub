# =========================
# motors.py - Motor control
# =========================
import RPi.GPIO as GPIO

# =========================
# PIN CONFIGURATION
# =========================
# Left motors (L298N #1)
M1_EN  = 0   # placeholder
M1_IN1 = 0   # placeholder
M1_IN2 = 0   # placeholder
M2_EN  = 0   # placeholder
M2_IN1 = 0   # placeholder
M2_IN2 = 0   # placeholder

# Right motors (L298N #2)
M3_EN  = 0   # placeholder
M3_IN1 = 0   # placeholder
M3_IN2 = 0   # placeholder
M4_EN  = 0   # placeholder
M4_IN1 = 0   # placeholder
M4_IN2 = 0   # placeholder

# =========================
# GPIO SETUP
# =========================
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

all_pins = [
    M1_EN, M1_IN1, M1_IN2,
    M2_EN, M2_IN1, M2_IN2,
    M3_EN, M3_IN1, M3_IN2,
    M4_EN, M4_IN1, M4_IN2
]
for pin in all_pins:
    GPIO.setup(pin, GPIO.OUT)

# PWM for speed control (100Hz)
m1 = GPIO.PWM(M1_EN, 100)
m2 = GPIO.PWM(M2_EN, 100)
m3 = GPIO.PWM(M3_EN, 100)
m4 = GPIO.PWM(M4_EN, 100)

m1.start(0)
m2.start(0)
m3.start(0)
m4.start(0)

# =========================
# MOTOR FUNCTIONS
# =========================
def set_speed(speed):
    """Set speed for all motors (0-100)"""
    m1.ChangeDutyCycle(speed)
    m2.ChangeDutyCycle(speed)
    m3.ChangeDutyCycle(speed)
    m4.ChangeDutyCycle(speed)

def forward(speed=60):
    """Move forward"""
    set_speed(speed)
    GPIO.output(M1_IN1, GPIO.HIGH); GPIO.output(M1_IN2, GPIO.LOW)
    GPIO.output(M2_IN1, GPIO.HIGH); GPIO.output(M2_IN2, GPIO.LOW)
    GPIO.output(M3_IN1, GPIO.HIGH); GPIO.output(M3_IN2, GPIO.LOW)
    GPIO.output(M4_IN1, GPIO.HIGH); GPIO.output(M4_IN2, GPIO.LOW)

def backward(speed=60):
    """Move backward"""
    set_speed(speed)
    GPIO.output(M1_IN1, GPIO.LOW); GPIO.output(M1_IN2, GPIO.HIGH)
    GPIO.output(M2_IN1, GPIO.LOW); GPIO.output(M2_IN2, GPIO.HIGH)
    GPIO.output(M3_IN1, GPIO.LOW); GPIO.output(M3_IN2, GPIO.HIGH)
    GPIO.output(M4_IN1, GPIO.LOW); GPIO.output(M4_IN2, GPIO.HIGH)

def left(speed=60):
    """Turn left - left motors backward, right motors forward"""
    set_speed(speed)
    GPIO.output(M1_IN1, GPIO.LOW);  GPIO.output(M1_IN2, GPIO.HIGH)
    GPIO.output(M2_IN1, GPIO.LOW);  GPIO.output(M2_IN2, GPIO.HIGH)
    GPIO.output(M3_IN1, GPIO.HIGH); GPIO.output(M3_IN2, GPIO.LOW)
    GPIO.output(M4_IN1, GPIO.HIGH); GPIO.output(M4_IN2, GPIO.LOW)

def right(speed=60):
    """Turn right - right motors backward, left motors forward"""
    set_speed(speed)
    GPIO.output(M1_IN1, GPIO.HIGH); GPIO.output(M1_IN2, GPIO.LOW)
    GPIO.output(M2_IN1, GPIO.HIGH); GPIO.output(M2_IN2, GPIO.LOW)
    GPIO.output(M3_IN1, GPIO.LOW);  GPIO.output(M3_IN2, GPIO.HIGH)
    GPIO.output(M4_IN1, GPIO.LOW);  GPIO.output(M4_IN2, GPIO.HIGH)

def stop():
    """Stop all motors"""
    set_speed(0)
    for pin in [M1_IN1, M1_IN2, M2_IN1, M2_IN2,
                M3_IN1, M3_IN2, M4_IN1, M4_IN2]:
        GPIO.output(pin, GPIO.LOW)

def cleanup():
    """Clean up GPIO"""
    stop()
    GPIO.cleanup()
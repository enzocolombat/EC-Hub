# Robot/motors/motor_control.py
import RPi.GPIO as GPIO
from time import sleep
from config import GPIO as GPIO_PINS, Robot

MOTOR_PINS = [
    [GPIO_PINS.M1_EN, GPIO_PINS.M1_IN1, GPIO_PINS.M1_IN2],  # Motor 1
    [GPIO_PINS.M2_EN, GPIO_PINS.M2_IN1, GPIO_PINS.M2_IN2],  # Motor 2
    [GPIO_PINS.M3_EN, GPIO_PINS.M3_IN1, GPIO_PINS.M3_IN2],  # Motor 3
    [GPIO_PINS.M4_EN, GPIO_PINS.M4_IN1, GPIO_PINS.M4_IN2],  # Motor 4
]

# GPIO Initialization
GPIO.setmode(GPIO.BCM)
for pin in [pin for motor in MOTOR_PINS for pin in motor]:
    GPIO.setup(pin, GPIO.OUT)

# PWM Initialization for Each Motor
MOTOR_PWMS = [
    GPIO.PWM(GPIO_PINS.M1_EN, 100),
    GPIO.PWM(GPIO_PINS.M2_EN, 100),
    GPIO.PWM(GPIO_PINS.M3_EN, 100),
    GPIO.PWM(GPIO_PINS.M4_EN, 100),
]

# Starts all PWMs at their default speed
for pwm in MOTOR_PWMS:
    pwm.start(Robot.DEFAULT_SPEED)

def set_speed(speed: int) -> None:
    """Sets the speed for ALL motors (0-100%)."""
    for pwm in MOTOR_PWMS:
        pwm.ChangeDutyCycle(speed)

def move_forward() -> None:
    """Moves the robot forward (all motors forward)."""
    for i in range(4):
        GPIO.output(MOTOR_PINS[i][1], GPIO.HIGH)  # IN1 = HIGH
        GPIO.output(MOTOR_PINS[i][2], GPIO.LOW)   # IN2 = LOW

def move_backward() -> None:
    """Moves the robot backward (all motors backward)."""
    for i in range(4):
        GPIO.output(MOTOR_PINS[i][1], GPIO.LOW)   # IN1 = LOW
        GPIO.output(MOTOR_PINS[i][2], GPIO.HIGH)  # IN2 = HIGH

def turn_left() -> None:
    """Turns the robot left (left motors backward, right motors forward)."""
    # Left motors (M1 and M3) backward
    for i in [0, 2]:  # M1 (index 0) and M3 (index 2)
        GPIO.output(MOTOR_PINS[i][1], GPIO.LOW)
        GPIO.output(MOTOR_PINS[i][2], GPIO.HIGH)
    # Right motors (M2 and M4) forward
    for i in [1, 3]:  # M2 (index 1) and M4 (index 3)
        GPIO.output(MOTOR_PINS[i][1], GPIO.HIGH)
        GPIO.output(MOTOR_PINS[i][2], GPIO.LOW)

def turn_right() -> None:
    """Turns the robot right (left motors forward, right motors backward)."""
    # Left motors (M1 and M3) forward
    for i in [0, 2]:
        GPIO.output(MOTOR_PINS[i][1], GPIO.HIGH)
        GPIO.output(MOTOR_PINS[i][2], GPIO.LOW)
    # Right motors (M2 and M4) backward
    for i in [1, 3]:
        GPIO.output(MOTOR_PINS[i][1], GPIO.LOW)
        GPIO.output(MOTOR_PINS[i][2], GPIO.HIGH)

def stop() -> None:
    """Stops all motors."""
    for i in range(4):
        GPIO.output(MOTOR_PINS[i][1], GPIO.LOW)
        GPIO.output(MOTOR_PINS[i][2], GPIO.LOW)

def cleanup() -> None:
    """Cleans up GPIO resources."""
    for pwm in MOTOR_PWMS:
        pwm.stop()
    GPIO.cleanup()
# Robot/motors/motor_control.py
import RPi.GPIO as GPIO
from time import sleep
from config import GPIO as GPIO_PINS, Robot

# Initialisation des broches (importées depuis config.py)
MOTOR_PINS = [
    [GPIO_PINS.M1_EN, GPIO_PINS.M1_IN1, GPIO_PINS.M1_IN2],  # Moteur 1
    [GPIO_PINS.M2_EN, GPIO_PINS.M2_IN1, GPIO_PINS.M2_IN2],  # Moteur 2
]

# Configuration GPIO
GPIO.setmode(GPIO.BCM)
for pin in [pin for motor in MOTOR_PINS for pin in motor]:
    GPIO.setup(pin, GPIO.OUT)

# Initialisation PWM pour la vitesse
M1_PWM = GPIO.PWM(GPIO_PINS.M1_EN, 100)
M2_PWM = GPIO.PWM(GPIO_PINS.M2_EN, 100)
M1_PWM.start(Robot.DEFAULT_SPEED)
M2_PWM.start(Robot.DEFAULT_SPEED)

def set_speed(speed: int) -> None:
    """Set the speed for both motors (0-100%)."""
    M1_PWM.ChangeDutyCycle(speed)
    M2_PWM.ChangeDutyCycle(speed)

def move_forward() -> None:
    """Move the robot forward."""
    GPIO.output(GPIO_PINS.M1_IN1, GPIO.HIGH)
    GPIO.output(GPIO_PINS.M1_IN2, GPIO.LOW)
    GPIO.output(GPIO_PINS.M2_IN1, GPIO.HIGH)
    GPIO.output(GPIO_PINS.M2_IN2, GPIO.LOW)

def move_backward() -> None:
    """Move the robot backward."""
    GPIO.output(GPIO_PINS.M1_IN1, GPIO.LOW)
    GPIO.output(GPIO_PINS.M1_IN2, GPIO.HIGH)
    GPIO.output(GPIO_PINS.M2_IN1, GPIO.LOW)
    GPIO.output(GPIO_PINS.M2_IN2, GPIO.HIGH)

def turn_left() -> None:
    """Turn the robot left."""
    GPIO.output(GPIO_PINS.M1_IN1, GPIO.LOW)
    GPIO.output(GPIO_PINS.M1_IN2, GPIO.HIGH)
    GPIO.output(GPIO_PINS.M2_IN1, GPIO.HIGH)
    GPIO.output(GPIO_PINS.M2_IN2, GPIO.LOW)

def turn_right() -> None:
    """Turn the robot right."""
    GPIO.output(GPIO_PINS.M1_IN1, GPIO.HIGH)
    GPIO.output(GPIO_PINS.M1_IN2, GPIO.LOW)
    GPIO.output(GPIO_PINS.M2_IN1, GPIO.LOW)
    GPIO.output(GPIO_PINS.M2_IN2, GPIO.HIGH)

def stop() -> None:
    """Stop both motors."""
    GPIO.output(GPIO_PINS.M1_IN1, GPIO.LOW)
    GPIO.output(GPIO_PINS.M1_IN2, GPIO.LOW)
    GPIO.output(GPIO_PINS.M2_IN1, GPIO.LOW)
    GPIO.output(GPIO_PINS.M2_IN2, GPIO.LOW)

def cleanup() -> None:
    """Clean up GPIO resources."""
    M1_PWM.stop()
    M2_PWM.stop()
    GPIO.cleanup()
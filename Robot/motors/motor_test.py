# Robot/motors/motor_test.py
import RPi.GPIO as GPIO
from time import sleep
from config import GPIO as GPIO_PINS, Robot

# Configuration
PINS = [
    [GPIO_PINS.M1_EN, GPIO_PINS.M1_IN1, GPIO_PINS.M1_IN2],
    [GPIO_PINS.M2_EN, GPIO_PINS.M2_IN1, GPIO_PINS.M2_IN2],
    [GPIO_PINS.M3_EN, GPIO_PINS.M3_IN1, GPIO_PINS.M3_IN2],
    [GPIO_PINS.M4_EN, GPIO_PINS.M4_IN1, GPIO_PINS.M4_IN2],
]

SPEED = Robot.DEFAULT_SPEED

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in [pin for motor in PINS for pin in motor]:
    GPIO.setup(pin, GPIO.OUT)

# Initialisation PWM
M1_PWM = GPIO.PWM(GPIO_PINS.M1_EN, 100)
M2_PWM = GPIO.PWM(GPIO_PINS.M2_EN, 100)
M3_PWM = GPIO.PWM(GPIO_PINS.M3_EN, 100)
M4_PWM = GPIO.PWM(GPIO_PINS.M4_EN, 100)
M1_PWM.start(SPEED)
M2_PWM.start(SPEED)
M3_PWM.start(SPEED)
M4_PWM.start(SPEED)

def set_forward(motor_num: int) -> None:
    """Set the specified motor to move forward."""
    GPIO.output(PINS[motor_num - 1][1], GPIO.HIGH)
    GPIO.output(PINS[motor_num - 1][2], GPIO.LOW)
    print(f"Motor {motor_num} moving forward at {SPEED}%")

def set_backward(motor_num: int) -> None:
    """Set the specified motor to move backward."""
    GPIO.output(PINS[motor_num - 1][1], GPIO.LOW)
    GPIO.output(PINS[motor_num - 1][2], GPIO.HIGH)
    print(f"Motor {motor_num} moving backward at {SPEED}%")

def stop_motor(motor_num: int) -> None:
    """Stop the specified motor."""
    GPIO.output(PINS[motor_num - 1][1], GPIO.LOW)
    GPIO.output(PINS[motor_num - 1][2], GPIO.LOW)
    print(f"Motor {motor_num} stopped.")

def stop_all() -> None:
    """Stop all motors."""
    for i in range(4):
        stop_motor(i + 1)
    print("All motors stopped.")

# main 
stop_all()

while True:
    set_forward(1); set_forward(2); set_forward(3); set_forward(4)
    sleep(3)
    stop_all()
    sleep(5)
    set_backward(1); set_backward(2); set_backward(3); set_backward(4)
    sleep(3)
    stop_all()
    sleep(5)
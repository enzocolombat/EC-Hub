# Robot/motors/motor_control.py
import pigpio
from config import GPIO as GPIO_PINS, Robot

MOTOR_PINS = [
    [GPIO_PINS.M1_EN, GPIO_PINS.M1_IN1, GPIO_PINS.M1_IN2],  # Motor 1
    [GPIO_PINS.M2_EN, GPIO_PINS.M2_IN1, GPIO_PINS.M2_IN2],  # Motor 2
    [GPIO_PINS.M3_EN, GPIO_PINS.M3_IN1, GPIO_PINS.M3_IN2],  # Motor 3
    [GPIO_PINS.M4_EN, GPIO_PINS.M4_IN1, GPIO_PINS.M4_IN2],  # Motor 4
]

PWM_FREQUENCY = 100  # Hz
PWM_RANGE = 100       # duty cycle expressed as 0-100

_pi = pigpio.pi()

if not _pi.connected:
    raise RuntimeError("pigpiod not running. Run: sudo systemctl start pigpiod")

# GPIO + PWM Initialization for each motor
for en, in1, in2 in MOTOR_PINS:
    _pi.set_mode(en,  pigpio.OUTPUT)
    _pi.set_mode(in1, pigpio.OUTPUT)
    _pi.set_mode(in2, pigpio.OUTPUT)

    _pi.set_PWM_frequency(en, PWM_FREQUENCY)
    _pi.set_PWM_range(en, PWM_RANGE)
    _pi.set_PWM_dutycycle(en, Robot.DEFAULT_SPEED)


def set_speed(speed: int) -> None:
    """Sets the speed for ALL motors (0-100%)."""
    for en, _, _ in MOTOR_PINS:
        _pi.set_PWM_dutycycle(en, speed)


def move_forward() -> None:
    """Moves the robot forward (all motors forward)."""
    for i in range(4):
        _pi.write(MOTOR_PINS[i][1], 1)  # IN1 = HIGH
        _pi.write(MOTOR_PINS[i][2], 0)  # IN2 = LOW


def move_backward() -> None:
    """Moves the robot backward (all motors backward)."""
    for i in range(4):
        _pi.write(MOTOR_PINS[i][1], 0)  # IN1 = LOW
        _pi.write(MOTOR_PINS[i][2], 1)  # IN2 = HIGH


def turn_left() -> None:
    """Turns the robot left (left motors backward, right motors forward)."""
    # Left motors (M1 and M3) backward
    for i in [0, 2]:
        _pi.write(MOTOR_PINS[i][1], 0)
        _pi.write(MOTOR_PINS[i][2], 1)
    # Right motors (M2 and M4) forward
    for i in [1, 3]:
        _pi.write(MOTOR_PINS[i][1], 1)
        _pi.write(MOTOR_PINS[i][2], 0)


def turn_right() -> None:
    """Turns the robot right (left motors forward, right motors backward)."""
    # Left motors (M1 and M3) forward
    for i in [0, 2]:
        _pi.write(MOTOR_PINS[i][1], 1)
        _pi.write(MOTOR_PINS[i][2], 0)
    # Right motors (M2 and M4) backward
    for i in [1, 3]:
        _pi.write(MOTOR_PINS[i][1], 0)
        _pi.write(MOTOR_PINS[i][2], 1)


def stop() -> None:
    """Stops all motors."""
    for i in range(4):
        _pi.write(MOTOR_PINS[i][1], 0)
        _pi.write(MOTOR_PINS[i][2], 0)


def cleanup() -> None:
    """Cleans up pigpio resources."""
    stop()
    for en, _, _ in MOTOR_PINS:
        _pi.set_PWM_dutycycle(en, 0)
    _pi.stop()
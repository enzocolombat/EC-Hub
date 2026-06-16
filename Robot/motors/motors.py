import logging
import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)

# --- Pin configuration ---
MOTORS = {
    "front_right": {"en": 21, "in1": 20, "in2": 16},  # M1
    "front_left":  {"en": 18, "in1": 17, "in2": 27},  # M2
    "rear_left":   {"en": 26, "in1": 6,  "in2": 19},  # M3
    "rear_right":  {"en": 22, "in1": 13, "in2": 5},   # M4
}

DEFAULT_SPEED = 25  # PWM duty cycle (0–100)

_pwm: dict[str, GPIO.PWM] = {}


def init():
    """Initialize GPIO pins and PWM for all motors."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for name, pins in MOTORS.items():
        GPIO.setup(pins["en"],  GPIO.OUT)
        GPIO.setup(pins["in1"], GPIO.OUT)
        GPIO.setup(pins["in2"], GPIO.OUT)

        pwm = GPIO.PWM(pins["en"], 100)
        pwm.start(DEFAULT_SPEED)
        _pwm[name] = pwm

    stop()
    logger.info("Motors initialized")


def _set_motor(name: str, forward: bool):
    """Drive a single motor forward or backward."""
    pins = MOTORS[name]
    GPIO.output(pins["in1"], GPIO.HIGH if forward else GPIO.LOW)
    GPIO.output(pins["in2"], GPIO.LOW  if forward else GPIO.HIGH)


def set_speed(speed: int):
    """Set PWM duty cycle on all motors (0–100)."""
    speed = max(0, min(100, speed))
    for pwm in _pwm.values():
        pwm.ChangeDutyCycle(speed)


def forward():
    _set_motor("front_right", forward=True)
    _set_motor("front_left",  forward=True)
    _set_motor("rear_left",   forward=True)
    _set_motor("rear_right",  forward=True)
    logger.debug("forward")


def backward():
    _set_motor("front_right", forward=False)
    _set_motor("front_left",  forward=False)
    _set_motor("rear_left",   forward=False)
    _set_motor("rear_right",  forward=False)
    logger.debug("backward")


def turn_left():
    # Right wheels forward, left wheels backward
    _set_motor("front_right", forward=True)
    _set_motor("rear_right",  forward=True)
    _set_motor("front_left",  forward=False)
    _set_motor("rear_left",   forward=False)
    logger.debug("turn_left")


def turn_right():
    # Left wheels forward, right wheels backward
    _set_motor("front_left",  forward=True)
    _set_motor("rear_left",   forward=True)
    _set_motor("front_right", forward=False)
    _set_motor("rear_right",  forward=False)
    logger.debug("turn_right")


def stop():
    """Cut power to all motors."""
    for name, pins in MOTORS.items():
        GPIO.output(pins["in1"], GPIO.LOW)
        GPIO.output(pins["in2"], GPIO.LOW)
    logger.debug("stop")


def cleanup():
    """Stop all motors and release GPIO."""
    stop()
    for pwm in _pwm.values():
        pwm.stop()
    GPIO.cleanup()
    logger.info("Motors cleaned up")
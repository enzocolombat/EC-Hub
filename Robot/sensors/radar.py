# Robot/sensors/radar.py
import RPi.GPIO as GPIO
import time
import logging
from config import GPIO as GPIO_PINS, Radar, Ultrasonic

logger = logging.getLogger(__name__)

# Initialisation
_pwm = GPIO.PWM(GPIO_PINS.SERVO, 50)
GPIO.setup(GPIO_PINS.TRIG, GPIO.OUT)
GPIO.setup(GPIO_PINS.ECHO, GPIO.IN)
_pwm.start(0)

def _set_angle(angle: float) -> None:
    """Move servo to a given angle (0–180°)."""
    duty = 2.5 + (angle / 180.0) * 10.0
    _pwm.ChangeDutyCycle(duty)
    time.sleep(Radar.STEP_DELAY)
    _pwm.ChangeDutyCycle(0)

def _measure_distance() -> float | None:
    """Measure distance using HC-SR04P."""
    GPIO.output(GPIO_PINS.TRIG, False)
    time.sleep(0.05)

    GPIO.output(GPIO_PINS.TRIG, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_PINS.TRIG, False)

    timeout = time.time() + Ultrasonic.TIMEOUT_SECONDS

    while GPIO.input(GPIO_PINS.ECHO) == 0:
        if time.time() > timeout:
            return None
    start = time.time()

    while GPIO.input(GPIO_PINS.ECHO) == 1:
        if time.time() > timeout:
            return None
    end = time.time()

    return round(((end - start) * Ultrasonic.SPEED_OF_SOUND_CM_PER_S) / 2, 1)

def run_scan(on_point: callable) -> None:
    """Sweep 0°→180°→0° and call on_point for each valid point."""
    forward = range(0, 181, Radar.STEP_DEG)
    backward = range(180, -1, -Radar.STEP_DEG)

    for angle in list(forward) + list(backward):
        _set_angle(angle)
        distance = _measure_distance()
        if distance is not None:
            logger.debug("angle=%d distance=%.1f", angle, distance)
            on_point({"angle": angle, "distance": distance})
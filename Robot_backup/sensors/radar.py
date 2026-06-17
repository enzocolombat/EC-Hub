import RPi.GPIO as GPIO
import time
import logging

logger = logging.getLogger(__name__)

SERVO_PIN  = 12
TRIG_PIN   = 23
ECHO_PIN   = 24
STEP_DEG   = 5
STEP_DELAY = 0.3

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(TRIG_PIN,  GPIO.OUT)
GPIO.setup(ECHO_PIN,  GPIO.IN)

_pwm = GPIO.PWM(SERVO_PIN, 50)
_pwm.start(0)


def _set_angle(angle: float):
    """Move servo to a given angle (0–180°)."""
    duty = 2.5 + (angle / 180.0) * 10.0
    _pwm.ChangeDutyCycle(duty)
    time.sleep(STEP_DELAY)
    _pwm.ChangeDutyCycle(0)


def _measure_distance() -> float | None:
    """Trigger a single ultrasonic pulse and return distance in cm."""
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.05)

    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    timeout = time.time() + 1.0

    while GPIO.input(ECHO_PIN) == 0:
        start = time.time()
        if start > timeout:
            return None

    while GPIO.input(ECHO_PIN) == 1:
        end = time.time()
        if end > timeout:
            return None

    return round(((end - start) * 34300) / 2, 1)


def run_scan(on_point: callable):
    """
    Sweep 0°→180°→0°, call on_point({angle, distance}) at each valid step.
    on_point is a callback so server.py can emit each point in real time.
    """
    forward  = range(0,   181,  STEP_DEG)
    backward = range(180, -1,  -STEP_DEG)

    for angle in list(forward) + list(backward):
        _set_angle(angle)
        distance = _measure_distance()

        if distance is not None:
            logger.debug("angle=%d distance=%.1f", angle, distance)
            on_point({"angle": angle, "distance": distance})
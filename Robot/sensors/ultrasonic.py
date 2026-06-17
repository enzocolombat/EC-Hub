# Robot/sensors/ultrasonic.py
import RPi.GPIO as GPIO
import time
import logging
from config import GPIO as GPIO_PINS, Ultrasonic

logger = logging.getLogger(__name__)

def setup() -> None:
    """Configure the ultrasonic sensor GPIO pins."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PINS.TRIG, GPIO.OUT)
    GPIO.setup(GPIO_PINS.ECHO, GPIO.IN)

def measure_distance() -> float | None:
    """Measure distance using HC-SR04P."""
    GPIO.output(GPIO_PINS.TRIG, False)
    time.sleep(0.05)

    GPIO.output(GPIO_PINS.TRIG, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_PINS.TRIG, False)

    timeout = time.time() + Ultrasonic.TIMEOUT_SECONDS

    while GPIO.input(GPIO_PINS.ECHO) == 0:
        if time.time() > timeout:
            logger.error("Ultrasonic timeout: no echo start")
            return None
    start = time.time()

    while GPIO.input(GPIO_PINS.ECHO) == 1:
        if time.time() > timeout:
            logger.error("Ultrasonic timeout: echo did not end")
            return None
    end = time.time()

    return round(((end - start) * Ultrasonic.SPEED_OF_SOUND_CM_PER_S) / 2, 1)

def cleanup() -> None:
    """Clean up GPIO resources."""
    GPIO.cleanup()
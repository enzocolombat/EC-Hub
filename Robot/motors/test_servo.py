import RPi.GPIO as GPIO
import time

SERVO_PIN  = 12
STEP_DEG   = 5      # degrees per step
STEP_DELAY = 0.15   # seconds between steps — increase to slow down

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)


def set_angle(angle: float):
    """Move servo to a given angle (0–180°)."""
    duty = 2.5 + (angle / 180.0) * 10.0
    pwm.ChangeDutyCycle(duty)
    time.sleep(STEP_DELAY)
    pwm.ChangeDutyCycle(0)  # stop signal to avoid jitter


try:
    print("Sweeping 0° → 180°...")
    for angle in range(0, 181, STEP_DEG):
        set_angle(angle)

    print("Sweeping 180° → 0°...")
    for angle in range(180, -1, -STEP_DEG):
        set_angle(angle)

    print("Done.")

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
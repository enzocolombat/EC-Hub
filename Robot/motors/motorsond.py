import RPi.GPIO as GPIO
import time

# --- Pin configuration ---
SERVO_PIN  = 12
TRIG_PIN   = 23
ECHO_PIN   = 24

# --- Scan configuration ---
STEP_DEG   = 5      # degrees per step
STEP_DELAY = 0.3    # seconds between steps — leaves time for a clean measure

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(TRIG_PIN,  GPIO.OUT)
GPIO.setup(ECHO_PIN,  GPIO.IN)

pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)


def set_angle(angle: float):
    """Move servo to a given angle (0–180°)."""
    duty = 2.5 + (angle / 180.0) * 10.0
    pwm.ChangeDutyCycle(duty)
    time.sleep(STEP_DELAY)
    pwm.ChangeDutyCycle(0)  # stop signal to avoid jitter


def measure_distance() -> float | None:
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

    distance = ((end - start) * 34300) / 2
    return round(distance, 1)


def scan() -> list[dict]:
    """
    Sweep servo 0° → 180° then back to 0°, measure at each step.
    Returns a list of {angle, distance} readings.
    """
    results = []

    forward  = range(0, 181, STEP_DEG)
    backward = range(180, -1, -STEP_DEG)

    for angle in list(forward) + list(backward):
        set_angle(angle)
        distance = measure_distance()

        if distance is not None:
            print(f"  {angle:>4}° → {distance} cm")
            results.append({"angle": angle, "distance": distance})
        else:
            print(f"  {angle:>4}° → timeout")

    return results

try:
    print("Starting radar scan...")
    readings = scan()
    print(f"\nScan complete — {len(readings)} valid readings.")

except KeyboardInterrupt:
    print("Interrupted.")

finally:
    pwm.stop()
    GPIO.cleanup()
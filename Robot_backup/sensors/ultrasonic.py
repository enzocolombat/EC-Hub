import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def mesure_distance():
    # Reset
    GPIO.output(TRIG, False)
    time.sleep(0.1)
    
    # Envoie signal
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    timeout = time.time() + 1  # timeout 1 seconde

    while GPIO.input(ECHO) == 0:
        debut = time.time()
        if time.time() > timeout:
            print("❌ Ultrasonic timeout - check wiring")
            return None

    while GPIO.input(ECHO) == 1:
        fin = time.time()
        if time.time() > timeout:
            print("❌ ECHO signal blocked")
            return None

    duree = fin - debut
    distance = (duree * 34300) / 2
    return round(distance, 1)

try:
    print("Démarrage du test...")
    while True:
        d = mesure_distance()
        if d is not None:
            print(f"✅ Distance : {d} cm")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Clean stop")
    GPIO.cleanup()
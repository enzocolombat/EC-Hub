import RPi.GPIO as GPIO
from time import sleep, time

# =========================
# CONFIGURATION MOTEURS
# =========================

# Moteur 1
M1_En = 21
M1_In1 = 20
M1_In2 = 16

# Moteur 2
M2_En = 18
M2_In1 = 17
M2_In2 = 27

# =========================
# CAPTEUR ULTRASON
# =========================

TRIG = 23
ECHO = 24

# =========================
# SETUP GPIO
# =========================

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Moteurs
motor_pins = [[M1_En, M1_In1, M1_In2], [M2_En, M2_In1, M2_In2]]


for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

# Ultrasons
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# PWM
M1_Vitesse = GPIO.PWM(M1_En, 100)
M2_Vitesse = GPIO.PWM(M2_En, 100)

M1_Vitesse.start(100)
M2_Vitesse.start(100)

# =========================
# FONCTIONS MOTEURS
# =========================
def sens1(moteurNum) :
    GPIO.output(motor_pins[moteurNum - 1][1], GPIO.HIGH)
    GPIO.output(motor_pins[moteurNum - 1][2], GPIO.LOW)


def avancer():
    GPIO.output(M1_In1, GPIO.HIGH)
    GPIO.output(M1_In2, GPIO.LOW)

    GPIO.output(M2_In1, GPIO.HIGH)
    GPIO.output(M2_In2, GPIO.LOW)

def stop():
    GPIO.output(M1_In1, GPIO.LOW)
    GPIO.output(M1_In2, GPIO.LOW)

    GPIO.output(M2_In1, GPIO.LOW)
    GPIO.output(M2_In2, GPIO.LOW)

def set_vitesse(vitesse):
    M1_Vitesse.ChangeDutyCycle(vitesse)
    M2_Vitesse.ChangeDutyCycle(vitesse)

# =========================
# MESURE DISTANCE
# =========================

def distance():

    GPIO.output(TRIG, False)
    sleep(0.05)

    # impulsion TRIG
    GPIO.output(TRIG, True)
    sleep(0.00001)
    GPIO.output(TRIG, False)

    # début signal
    while GPIO.input(ECHO) == 0:
        debut = time()

    # fin signal
    while GPIO.input(ECHO) == 1:
        fin = time()

    duree = fin - debut

    # vitesse son = 34300 cm/s
    dist = (duree * 34300) / 2

    return dist

# =========================
# PROGRAMME PRINCIPAL
# =========================

try:

    avancer()

    while True:

        dist = distance()

        print(f"Distance : {dist:.1f} cm")

        # Très proche = STOP
        if dist < 15:
            print("Obstacle proche -> STOP")
            set_vitesse(0)

        # Moyen = ralenti
        elif dist < 40:
            print("Obstacle détecté -> RALENTI")
            set_vitesse(100)

        # Libre = vitesse normale
        else:
            print("Route libre -> ACCELERATION")
            set_vitesse(100)

        sleep(1)

except KeyboardInterrupt:
    print("Arrêt du programme")

finally:
    stop()
    GPIO.cleanup()
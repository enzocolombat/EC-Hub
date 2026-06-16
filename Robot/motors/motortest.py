import RPi.GPIO as GPIO
from time import sleep


# Definition des pins
M1_En = 21
M1_In1 = 20
M1_In2 = 16

M2_En = 18
M2_In1 = 17
M2_In2 = 27

# Definition des pin

M3_En = 26
M3_In1 = 6
M3_In2 = 19

M4_En = 22
M4_In1 = 13
M4_In2 = 5

# Creation d'une liste des pins pour chaque moteur pour compacter la suite du code
Pins = [[M1_En, M1_In1, M1_In2], [M2_En, M2_In1, M2_In2],
        [M3_En, M3_In1, M3_In2],[M4_En, M4_In1, M4_In2]]

Vitesse = 25
# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(M1_En, GPIO.OUT)
GPIO.setup(M1_In1, GPIO.OUT)
GPIO.setup(M1_In2, GPIO.OUT)

GPIO.setup(M2_En, GPIO.OUT)
GPIO.setup(M2_In1, GPIO.OUT)
GPIO.setup(M2_In2, GPIO.OUT)

GPIO.setup(M3_En, GPIO.OUT)
GPIO.setup(M3_In1, GPIO.OUT)
GPIO.setup(M3_In2, GPIO.OUT)

GPIO.setup(M4_En, GPIO.OUT)
GPIO.setup(M4_In1, GPIO.OUT)
GPIO.setup(M4_In2, GPIO.OUT)



M1_Vitesse = GPIO.PWM(M1_En, 100)
M2_Vitesse = GPIO.PWM(M2_En, 100)
M3_Vitesse = GPIO.PWM(M3_En, 100)
M4_Vitesse = GPIO.PWM(M4_En, 100)
M1_Vitesse.start(Vitesse)
M2_Vitesse.start(Vitesse)
M3_Vitesse.start(Vitesse)
M4_Vitesse.start(Vitesse)


def sens1(moteurNum) :
    GPIO.output(Pins[moteurNum - 1][1], GPIO.HIGH)
    GPIO.output(Pins[moteurNum - 1][2], GPIO.LOW)
    print("Moteur", moteurNum, "tourne dans le sens 1.", Vitesse)


def sens2(moteurNum) :
    GPIO.output(Pins[moteurNum - 1][1], GPIO.LOW)
    GPIO.output(Pins[moteurNum - 1][2], GPIO.HIGH)
    print("Moteur", moteurNum, "tourne dans le sens 2.", Vitesse)

def arret(moteurNum) :
    GPIO.output(Pins[moteurNum - 1][1], GPIO.LOW)
    GPIO.output(Pins[moteurNum - 1][2], GPIO.LOW)
    print("Moteur", moteurNum, "arret.")

def arretComplet() :
    GPIO.output(Pins[0][1], GPIO.LOW)
    GPIO.output(Pins[0][2], GPIO.LOW)
    GPIO.output(Pins[1][1], GPIO.LOW)
    GPIO.output(Pins[1][2], GPIO.LOW)
    GPIO.output(Pins[2][1], GPIO.LOW)
    GPIO.output(Pins[2][2], GPIO.LOW)
    GPIO.output(Pins[3][1], GPIO.LOW)
    GPIO.output(Pins[3][2], GPIO.LOW)
    print("Moteurs arretes.")
arretComplet()


while True :
 
    # Exemple de motif de boucle
      
      sens1(1)
      sens1(2)
      sens1(3)
      sens1(4)
      sleep(3)
      arretComplet()
      sleep(5)
      sens2(1)
      sens2(2)
      sens2(3)
      sens2(4)
      sleep(3)
      arretComplet()
      sleep(5)

# Robot/motors/motor_control.py
import RPi.GPIO as GPIO
from time import sleep
from config import GPIO as GPIO_PINS, Robot

# Configuration des 4 moteurs (importées depuis config.py)
MOTOR_PINS = [
    [GPIO_PINS.M1_EN, GPIO_PINS.M1_IN1, GPIO_PINS.M1_IN2],  # Moteur 1
    [GPIO_PINS.M2_EN, GPIO_PINS.M2_IN1, GPIO_PINS.M2_IN2],  # Moteur 2
    [GPIO_PINS.M3_EN, GPIO_PINS.M3_IN1, GPIO_PINS.M3_IN2],  # Moteur 3
    [GPIO_PINS.M4_EN, GPIO_PINS.M4_IN1, GPIO_PINS.M4_IN2],  # Moteur 4
]

# Initialisation GPIO
GPIO.setmode(GPIO.BCM)
for pin in [pin for motor in MOTOR_PINS for pin in motor]:
    GPIO.setup(pin, GPIO.OUT)

# Initialisation PWM pour chaque moteur
MOTOR_PWMS = [
    GPIO.PWM(GPIO_PINS.M1_EN, 100),
    GPIO.PWM(GPIO_PINS.M2_EN, 100),
    GPIO.PWM(GPIO_PINS.M3_EN, 100),
    GPIO.PWM(GPIO_PINS.M4_EN, 100),
]

# Démarre tous les PWMs avec la vitesse par défaut
for pwm in MOTOR_PWMS:
    pwm.start(Robot.DEFAULT_SPEED)

def set_speed(speed: int) -> None:
    """Définit la vitesse pour TOUS les moteurs (0-100%)."""
    for pwm in MOTOR_PWMS:
        pwm.ChangeDutyCycle(speed)

def move_forward() -> None:
    """Fait avancer le robot (tous les moteurs en avant)."""
    for i in range(4):
        GPIO.output(MOTOR_PINS[i][1], GPIO.HIGH)  # IN1 = HIGH
        GPIO.output(MOTOR_PINS[i][2], GPIO.LOW)   # IN2 = LOW

def move_backward() -> None:
    """Fait reculer le robot (tous les moteurs en arrière)."""
    for i in range(4):
        GPIO.output(MOTOR_PINS[i][1], GPIO.LOW)   # IN1 = LOW
        GPIO.output(MOTOR_PINS[i][2], GPIO.HIGH)  # IN2 = HIGH

def turn_left() -> None:
    """Fait tourner le robot à gauche (moteurs gauche en arrière, moteurs droit en avant)."""
    # Moteurs gauche (M1 et M3) en arrière
    for i in [0, 2]:  # M1 (index 0) et M3 (index 2)
        GPIO.output(MOTOR_PINS[i][1], GPIO.LOW)
        GPIO.output(MOTOR_PINS[i][2], GPIO.HIGH)
    # Moteurs droit (M2 et M4) en avant
    for i in [1, 3]:  # M2 (index 1) et M4 (index 3)
        GPIO.output(MOTOR_PINS[i][1], GPIO.HIGH)
        GPIO.output(MOTOR_PINS[i][2], GPIO.LOW)

def turn_right() -> None:
    """Fait tourner le robot à droite (moteurs gauche en avant, moteurs droit en arrière)."""
    # Moteurs gauche (M1 et M3) en avant
    for i in [0, 2]:
        GPIO.output(MOTOR_PINS[i][1], GPIO.HIGH)
        GPIO.output(MOTOR_PINS[i][2], GPIO.LOW)
    # Moteurs droit (M2 et M4) en arrière
    for i in [1, 3]:
        GPIO.output(MOTOR_PINS[i][1], GPIO.LOW)
        GPIO.output(MOTOR_PINS[i][2], GPIO.HIGH)

def stop() -> None:
    """Arrête tous les moteurs."""
    for i in range(4):
        GPIO.output(MOTOR_PINS[i][1], GPIO.LOW)
        GPIO.output(MOTOR_PINS[i][2], GPIO.LOW)

def cleanup() -> None:
    """Nettoie les ressources GPIO."""
    for pwm in MOTOR_PWMS:
        pwm.stop()
    GPIO.cleanup()
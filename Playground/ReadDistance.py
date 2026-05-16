"""Measure distance with an ultrasonic sensor connected to Raspberry Pi GPIO pins."""

import RPi.GPIO as GPIO  # Imports Raspberry Pi GPIO control functions.
import time  # Provides sleep calls and timeout timestamps.

GPIO.setmode(GPIO.BOARD)  # Uses physical board pin numbering instead of BCM numbering.
TRIG = 11  # Defines the physical pin used to send the ultrasonic trigger pulse.
ECHO = 13  # Defines the physical pin used to read the returned echo pulse.

GPIO.setup(TRIG, GPIO.OUT)  # Configures the trigger pin as an output.
GPIO.setup(ECHO, GPIO.IN)  # Configures the echo pin as an input.

def mesurer_distance():  # Sends one ultrasonic pulse and returns the measured distance in centimeters.
    GPIO.output(TRIG, False)  # Makes sure the trigger pin starts low.
    time.sleep(0.1)  # Lets the sensor settle before sending the pulse.

    GPIO.output(TRIG, True)  # Starts the trigger pulse.
    time.sleep(0.00001)  # Holds the trigger high for about 10 microseconds.
    GPIO.output(TRIG, False)  # Ends the trigger pulse.

    debut = None  # Will store the time when the echo pulse starts.
    fin = None  # Will store the time when the echo pulse ends.

    timeout = time.time() + 1  # Sets a one-second limit while waiting for the echo to start.
    while GPIO.input(ECHO) == 0:  # Waits until the echo pin goes high.
        debut = time.time()  # Updates the potential start time of the echo.
        if time.time() > timeout:  # Stops waiting if the sensor never answers.
            print("Timeout - verifie le cablage TRIG/ECHO")  # Warns that wiring may be wrong.
            return None  # Returns no distance because the measurement failed.

    timeout = time.time() + 1  # Sets a one-second limit while waiting for the echo to end.
    while GPIO.input(ECHO) == 1:  # Waits until the echo pin goes low again.
        fin = time.time()  # Updates the end time of the echo pulse.
        if time.time() > timeout:  # Stops waiting if the echo stays high too long.
            print("Timeout - objet trop loin")  # Warns that the echo did not come back normally.
            return None  # Returns no distance because the measurement failed.

    if debut is None or fin is None:  # Checks that both timestamps were captured.
        return None  # Returns no distance if the pulse timing is incomplete.

    duree = fin - debut  # Computes how long the ultrasonic wave traveled there and back.
    distance = (duree * 34300) / 2  # Converts travel time to centimeters and divides by two for one-way distance.
    return round(distance, 2)  # Rounds the result to two decimals for display.

try:  # Allows Ctrl+C to clean up GPIO pins.
    while True:  # Repeats measurements forever.
        dist = mesurer_distance()  # Takes one distance measurement.
        if dist:  # Prints only successful non-zero measurements.
            print(f"Distance : {dist} cm")  # Displays the measured distance.
        time.sleep(0.5)  # Waits half a second before measuring again.

except KeyboardInterrupt:  # Catches Ctrl+C from the terminal.
    print("Arret")  # Confirms that the program is stopping.
    GPIO.cleanup()  # Releases GPIO pins so they are left in a clean state.

"""Read and print accelerometer, gyroscope, and temperature values from an MPU6050."""

from mpu6050 import mpu6050  # Imports the MPU6050 helper class for I2C sensor access.
import time  # Provides the delay between readings.

capteur = mpu6050(0x68)  # Creates the sensor object at the usual MPU6050 I2C address.

try:  # Allows the loop to stop cleanly with Ctrl+C.
    while True:  # Continuously reads the sensor.
        accel = capteur.get_accel_data()  # Reads acceleration on the X, Y, and Z axes.
        gyro = capteur.get_gyro_data()  # Reads angular speed on the X, Y, and Z axes.
        temp = capteur.get_temp()  # Reads the internal sensor temperature.

        print(f"--- Accelerometre ---")  # Prints a label for acceleration values.
        print(f"X: {accel['x']:.2f}  Y: {accel['y']:.2f}  Z: {accel['z']:.2f}")  # Prints acceleration rounded to two decimals.
        print(f"--- Gyroscope ---")  # Prints a label for gyroscope values.
        print(f"X: {gyro['x']:.2f}  Y: {gyro['y']:.2f}  Z: {gyro['z']:.2f}")  # Prints angular speed rounded to two decimals.
        print(f"Temperature : {temp:.2f} C")  # Prints the sensor temperature in Celsius.
        print()  # Adds an empty line to make each reading block easier to read.
        time.sleep(0.5)  # Waits half a second before the next reading.

except KeyboardInterrupt:  # Catches Ctrl+C from the terminal.
    print("Arret")  # Confirms that the program is stopping.

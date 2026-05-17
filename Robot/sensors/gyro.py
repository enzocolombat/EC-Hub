"""Read and print accelerometer, gyroscope, and temperature values from an MPU6050."""

from mpu6050 import mpu6050

# Initialize sensor at I2C address 0x68
sensor = mpu6050(0x68)

def get_data():
    """
    Reads all data from the MPU-6050 sensor.
    
    Returns:
        dict: acceleration, gyroscope and temperature data
    """
    accel = sensor.get_accel_data()
    gyro = sensor.get_gyro_data()
    temp = sensor.get_temp()

    return {
        "accel": {"x": accel["x"], "y": accel["y"], "z": accel["z"]},
        "gyro":  {"x": gyro["x"],  "y": gyro["y"],  "z": gyro["z"]},
        "temp":  round(temp, 2)
    }

# try:  # Allows the loop to stop cleanly with Ctrl+C.
    while True:  # Continuously reads the sensor.
        accel = sensor.get_accel_data()  # Reads acceleration on the X, Y, and Z axes.
        gyro = sensor.get_gyro_data()  # Reads angular speed on the X, Y, and Z axes.
        temp = sensor.get_temp()  # Reads the internal sensor temperature.

        print(f"--- Accelerometre ---")  # Prints a label for acceleration values.
        print(f"X: {accel['x']:.2f}  Y: {accel['y']:.2f}  Z: {accel['z']:.2f}")  # Prints acceleration rounded to two decimals.
        print(f"--- Gyroscope ---")  # Prints a label for gyroscope values.
        print(f"X: {gyro['x']:.2f}  Y: {gyro['y']:.2f}  Z: {gyro['z']:.2f}")  # Prints angular speed rounded to two decimals.
        print(f"Temperature : {temp:.2f} C")  # Prints the sensor temperature in Celsius.
        print()  # Adds an empty line to make each reading block easier to read.
        time.sleep(0.5)  # Waits half a second before the next reading.

#except KeyboardInterrupt:  # Catches Ctrl+C from the terminal.
   # print("Arret")  # Confirms that the program is stopping.

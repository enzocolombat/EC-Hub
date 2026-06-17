import logging
from mpu6050 import mpu6050

I2C_ADDRESS  = 0x68
logger = logging.getLogger(__name__)

try:
    _sensor = mpu6050(I2C_ADDRESS)
except Exception as e:
    # Allows server to start even when sensor is unplugged (e.g. on PC)
    _sensor = None
    logger.warning("MPU-6050 not found at 0x%02X: %s", I2C_ADDRESS, e)


def get_data() -> dict | None:
    """
    Read acceleration, gyroscope and temperature from the MPU-6050.

    Returns None if the sensor is unavailable or the read fails,
    so callers can skip the frame rather than crash.
    """
    if _sensor is None:
        return None

    try:
        accel = _sensor.get_accel_data()
        gyro  = _sensor.get_gyro_data()
        temp  = _sensor.get_temp()
    except Exception as e:
        logger.error("MPU-6050 read failed: %s", e)
        return None

    return {
        "accel": {"x": accel["x"], "y": accel["y"], "z": accel["z"]},
        "gyro":  {"x": gyro["x"],  "y": gyro["y"],  "z": gyro["z"]},
        "temp":  round(temp, 2),
    }
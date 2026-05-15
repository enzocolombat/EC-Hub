import time

trigger = open("/sys/class/leds/ACT/trigger", "w")
led = open("/sys/class/leds/ACT/brightness", "w")

# Désactive le trigger automatique
trigger.write("none")
trigger.flush()

# Fait clignoter 10 fois
for i in range(3):
    led.write("1")
    led.flush()
    time.sleep(0.2)
    led.write("0")
    led.flush()
    time.sleep(0.2)

led.close()
trigger.close()
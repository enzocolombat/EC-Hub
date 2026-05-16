"""Blink the Raspberry Pi ACT LED manually for a short visual test."""

import time  # Gives access to sleep delays between LED state changes.

trigger = open("/sys/class/leds/ACT/trigger", "w")  # Opens the ACT LED trigger control in write mode.
led = open("/sys/class/leds/ACT/brightness", "w")  # Opens the ACT LED brightness control in write mode.

# Disable the automatic LED trigger so the script can control the LED directly.
trigger.write("none")  # Replaces the current trigger mode with manual control.
trigger.flush()  # Forces the trigger change to be written immediately.

# Blink the LED three times to confirm that manual control works.
for i in range(3):  # Repeats the on/off sequence three times.
    led.write("1")  # Turns the ACT LED on.
    led.flush()  # Sends the on state to the system file right away.
    time.sleep(0.2)  # Keeps the LED on briefly so the blink is visible.
    led.write("0")  # Turns the ACT LED off.
    led.flush()  # Sends the off state to the system file right away.
    time.sleep(0.2)  # Keeps the LED off briefly before the next blink.

led.close()  # Closes the brightness file handle cleanly.
trigger.close()  # Closes the trigger file handle cleanly.

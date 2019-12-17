"""This example prints the status of the slide switch. Try moving the switch back and forth to see
what's printed to the serial console!"""
import time
from adafruit_circuitplayground import cp

while True:
    print("Slide switch:", cp.switch)
    time.sleep(0.1)

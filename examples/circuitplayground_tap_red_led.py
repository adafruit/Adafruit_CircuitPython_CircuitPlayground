"""This example turns on the little red LED and prints to the serial console when you double-tap
the CPX!"""
import time
from adafruit_circuitplayground.express import cpx

# Change to 1 for detecting a single-tap!
cpx.detect_taps = 2

while True:
    if cpx.tapped:
        print("Tapped!")
        cpx.red_led = True
        time.sleep(0.1)
    else:
        cpx.red_led = False

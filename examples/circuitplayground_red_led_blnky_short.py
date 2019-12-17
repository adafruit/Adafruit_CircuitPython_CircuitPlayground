"""This is the "Hello, world!" of CircuitPython: Blinky! This example blinks the little red LED on
and off! It's a shorter version of the other Blinky example."""
import time
from adafruit_circuitplayground import cp

while True:
    cp.red_led = not cp.red_led
    time.sleep(0.5)

"""This is the "Hello, world!" of CircuitPython: Blinky! This example blinks the little red LED on
and off!"""
import time
from adafruit_circuitplayground.express import cpx

while True:
    cpx.red_led = True
    time.sleep(0.5)
    cpx.red_led = False
    time.sleep(0.5)

"""This example lights up all the NeoPixel LEDs red."""
from adafruit_circuitplayground import cp

while True:
    cp.pixels.fill((50, 0, 0))

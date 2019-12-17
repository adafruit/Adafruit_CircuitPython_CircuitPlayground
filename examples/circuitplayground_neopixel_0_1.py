"""This example lights up the first and second NeoPixel, red and blue respectively."""
from adafruit_circuitplayground import cp

cp.pixels.brightness = 0.3

while True:
    cp.pixels[0] = (255, 0, 0)
    cp.pixels[1] = (0, 0, 255)

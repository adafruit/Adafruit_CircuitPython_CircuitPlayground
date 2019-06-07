"""This example lights up half the NeoPixels red while button A is being pressed, and half the
NeoPixels green while button B is being pressed."""
from adafruit_circuitplayground.express import cpx

cpx.pixels.brightness = 0.3
cpx.pixels.fill((0, 0, 0))  # Turn off the NeoPixels if they're on!

while True:
    if cpx.button_a:
        cpx.pixels[0:5] = [(255, 0, 0)] * 5
    else:
        cpx.pixels[0:5] = [(0, 0, 0)] * 5

    if cpx.button_b:
        cpx.pixels[5:10] = [(0, 255, 0)] * 5
    else:
        cpx.pixels[5:10] = [(0, 0, 0)] * 5

"""This example lights up the third NeoPixel while button A is being pressed, and lights up the
eighth NeoPixel while button B is being pressed."""
from adafruit_circuitplayground.express import cpx

cpx.pixels.brightness = 0.3
cpx.pixels.fill((0, 0, 0))  # Turn off the NeoPixels if they're on!

while True:
    if cpx.button_a:
        cpx.pixels[2] = (0, 255, 0)
    else:
        cpx.pixels[2] = (0, 0, 0)

    if cpx.button_b:
        cpx.pixels[7] = (0, 0, 255)
    else:
        cpx.pixels[7] = (0, 0, 0)

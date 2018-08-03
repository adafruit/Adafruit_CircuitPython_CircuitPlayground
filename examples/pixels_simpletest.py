# CircuitPython demo - NeoPixel

import time
from adafruit_circuitplayground.express import cpx

# The number of pixels in the strip
numpix = 10


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0) or (pos > 255):
        return (0, 0, 0)
    if pos < 85:
        return (int(pos * 3), int(255 - (pos*3)), 0)
    if pos < 170:
        pos -= 85
        return (int(255 - pos*3), 0, int(pos*3))
    pos -= 170
    return (0, int(pos*3), int(255 - pos*3))


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(cpx.pixels.n):
            idx = int((i * 256 / len(cpx.pixels)) + j)
            cpx.pixels[i] = wheel(idx & 255)
        cpx.pixels.show()
        time.sleep(wait)


cpx.pixels.auto_write = False
cpx.pixels.brightness = 0.3
while True:
    rainbow_cycle(0.001)    # rainbowcycle with 1ms delay per step

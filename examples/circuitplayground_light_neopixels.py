"""
This example uses the light sensor on the CPX, located next to the picture of the eye on the board.
Once you have the library loaded, try shining a flashlight on your CPX to watch the number of
NeoPixels lit up increase, or try covering up the light sensor to watch the number decrease.
"""

import time
from adafruit_circuitplayground.express import cpx

cpx.pixels.auto_write = False
cpx.pixels.brightness = 0.3


def scale_range(value):
    """Scale a value from 0-320 (light range) to 0-10 (the number of NeoPixels).
    Allows remapping light value to pixel position."""
    return int(value / 320 * 10)


while True:
    peak = scale_range(cpx.light)
    print(cpx.light)
    print(int(peak))

    for i in range(10):
        if i <= peak:
            cpx.pixels[i] = (0, 255, 255)
        else:
            cpx.pixels[i] = (0, 0, 0)
    cpx.pixels.show()
    time.sleep(0.05)

"""THIS EXAMPLE REQUIRES A SEPARATE LIBRARY BE LOADED ONTO YOUR CIRCUITPY DRIVE.
This example requires the simpleio.mpy library.

This example uses the light sensor on the CPX, located net to the picture of the eye on the board.
Once you have the library loaded, try shining a flashlight on your CPX to watch the number of
NeoPixels lit up increase, or try covering up the light sensor to watch the number decrease."""
import time
from adafruit_circuitplayground.express import cpx
import simpleio

cpx.pixels.auto_write = False
cpx.pixels.brightness = 0.3

while True:
    # light value remapped to pixel position
    peak = simpleio.map_range(cpx.light, 0, 320, 0, 10)
    print(cpx.light)
    print(int(peak))

    for i in range(0, 10, 1):
        if i <= peak:
            cpx.pixels[i] = (0, 255, 255)
        else:
            cpx.pixels[i] = (0, 0, 0)
    cpx.pixels.show()
    time.sleep(0.05)

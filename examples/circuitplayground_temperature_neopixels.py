"""THIS EXAMPLE REQUIRES A SEPARATE LIBRARY BE LOADED ONTO YOUR CIRCUITPY DRIVE.
This example requires the simpleio.mpy library.

This example use the temperature sensor on the CPX, located next to the picture of the thermometer
on the board. Try warming up the board to watch the number of NeoPixels lit up increase, or cooling
it down to see the number decrease. You can set the min and max temperatures to make it more or
less sensitive to temperature changes.
"""
import time
from adafruit_circuitplayground.express import cpx
import simpleio

cpx.pixels.auto_write = False
cpx.pixels.brightness = 0.3

# Set these based on your ambient temperature in Celsius for best results!
minimum_temp = 24
maximum_temp = 30

while True:
    # temperature value remapped to pixel position
    peak = simpleio.map_range(cpx.temperature, minimum_temp, maximum_temp, 0, 10)
    print(cpx.temperature)
    print(int(peak))

    for i in range(0, 10, 1):
        if i <= peak:
            cpx.pixels[i] = (0, 255, 255)
        else:
            cpx.pixels[i] = (0, 0, 0)
    cpx.pixels.show()
    time.sleep(0.05)

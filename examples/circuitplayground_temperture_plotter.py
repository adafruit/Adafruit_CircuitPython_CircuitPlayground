"""If you're using Mu, this example will plot the temperature in C and F on the plotter! Click
"Plotter" to open it, and place your finger over the sensor to see the numbers change. The
sensor is located next to the picture of the thermometer on the CPX."""
import time
from adafruit_circuitplayground.express import cpx

while True:
    print("Temperature C:", cpx.temperature)
    print("Temperature F:", cpx.temperature * 1.8 + 32)
    print((cpx.temperature, cpx.temperature * 1.8 + 32))
    time.sleep(0.1)

"""If you're using Mu, this example will plot the light levels from the light sensor (located next
to the eye) on your CPX. Try shining a flashlight on your CPX, or covering the light sensor to see
the plot increase and decrease."""
import time
from adafruit_circuitplayground.express import cpx

while True:
    print("Light:", cpx.light)
    print((cpx.light,))
    time.sleep(0.1)

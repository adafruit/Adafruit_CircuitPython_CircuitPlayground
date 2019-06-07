"""This example uses the light sensor on your CPX, located next to the picture of the eye. Try
shining a flashlight on your CPX, or covering the light sensor with your finger to see the values
increase and decrease."""
import time
from adafruit_circuitplayground.express import cpx

while True:
    print("Light:", cpx.light)
    time.sleep(1)

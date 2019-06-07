"""This example uses the slide switch to control the little red LED. When the switch is to the
right it returns False, and when it's to the left, it returns True."""
from adafruit_circuitplayground.express import cpx

while True:
    cpx.red_led = cpx.switch

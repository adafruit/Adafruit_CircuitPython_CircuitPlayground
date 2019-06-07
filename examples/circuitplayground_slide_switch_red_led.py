"""This example uses the slide switch to control the little red LED."""
from adafruit_circuitplayground.express import cpx

# This code is written to be readable versus being Pylint compliant.
# pylint: disable=simplifiable-if-statement

while True:
    if cpx.switch:
        cpx.red_led = True
    else:
        cpx.red_led = False

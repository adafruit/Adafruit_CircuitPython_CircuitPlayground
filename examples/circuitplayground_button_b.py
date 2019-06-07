"""This example turns the little red LED on only while button B is currently being pressed."""
from adafruit_circuitplayground.express import cpx

# This code is written to be readable versus being Pylint compliant.
# pylint: disable=simplifiable-if-statement

while True:
    if cpx.button_b:
        cpx.red_led = True
    else:
        cpx.red_led = False

# Can also be written as:
#    cpx.red_led = cpx.button_b

"""This example plays a different tone for a duration of 1 second for each button pressed."""
from adafruit_circuitplayground.express import cpx

while True:
    if cpx.button_a:
        cpx.play_tone(262, 1)
    if cpx.button_b:
        cpx.play_tone(294, 1)

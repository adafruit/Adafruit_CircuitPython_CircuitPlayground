"""This example plays two tones for 1 second each. Note that the tones are not in a loop - this is
to prevent them from playing indefinitely!"""
from adafruit_circuitplayground.express import cpx

cpx.play_tone(262, 1)
cpx.play_tone(294, 1)

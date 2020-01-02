"""This example prints to the serial console when the board is double-tapped."""
from adafruit_circuitplayground import cp

cp.detect_taps = 2

while True:
    if cp.tapped:
        print("Tapped!")

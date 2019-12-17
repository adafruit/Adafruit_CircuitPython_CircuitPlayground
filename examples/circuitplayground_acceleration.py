"""This example uses the accelerometer on the Circuit Playground. It prints the values. Try moving
the board to see the values change."""
import time
from adafruit_circuitplayground import cp

while True:
    x, y, z = cp.acceleration
    print(x, y, z)

    time.sleep(0.1)

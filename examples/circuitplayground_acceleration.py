import time
from adafruit_circuitplayground import cp

while True:
    x, y, z = cp.acceleration
    print(x, y, z)

    time.sleep(0.1)

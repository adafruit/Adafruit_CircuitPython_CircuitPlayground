from adafruit_circuitplayground import cp

cp.detect_taps = 1

while True:
    if cp.tapped:
        print("Single tap detected!")

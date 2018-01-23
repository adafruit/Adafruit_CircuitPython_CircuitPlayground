from adafruit_circuitplayground.express import cpx

while True:
    x, y, z = cpx.acceleration
    print(x, y, z)

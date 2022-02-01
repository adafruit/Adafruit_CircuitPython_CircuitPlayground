# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example prints to the serial console when you touch the capacitive touch pads."""
from adafruit_circuitplayground import cp

print("Here are all the possible touchpads:")
print(cp.touchpads)

while True:
    print("Touchpads currently registering a touch:")
    print(cp.touched)

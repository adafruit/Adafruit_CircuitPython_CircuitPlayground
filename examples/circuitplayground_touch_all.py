# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example prints to the serial console when you touch the capacitive touch pads."""
from adafruit_circuitplayground import cp

while True:
    if cp.touch_A1:
        print("Touched pad A1")
    if cp.touch_A2:
        print("Touched pad A2")
    if cp.touch_A3:
        print("Touched pad A3")
    if cp.touch_A4:
        print("Touched pad A4")
    if cp.touch_A5:
        print("Touched pad A5")
    if cp.touch_A6:
        print("Touched pad A6")
    if cp.touch_TX:
        print("Touched pad TX")

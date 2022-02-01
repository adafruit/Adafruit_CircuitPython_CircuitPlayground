# SPDX-FileCopyrightText: 2021 Alec Delaney
# SPDX-License-Identifier: MIT

"""This example prints to the serial console when you touch the capacitive touch pads."""
from adafruit_circuitplayground import cp

print("Here are all the initially registered touchpads:")
print(cp.touchpads)

print("You can remove a few if you need those pins:")
cp.deinit_touchpad("A2")
cp.deinit_touchpad("A5")
print(cp.touchpads)

print("You can also readd them later!")
cp.init_touchpad("A2")
print(cp.touchpads)

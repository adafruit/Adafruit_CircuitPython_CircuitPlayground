# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example prints to the serial console when you touch the capacitive touch pads."""
import board
from adafruit_circuitplayground import cp


# You'll need to first use the touchpads individually to register them as active touchpads
# You don't have to keep the result though
is_a1_touched = cp.touch_A1  # This result can be saved if you want to use it like below
if is_a1_touched:
    print("A1 was touched upon startup!")
cp.touch_A2  # These work exactly the same as above, but we're not storing the result
cp.touch_A3
cp.touch_A4


while True:

    print("Pads that are currently setup as touchpads:")
    print(cp.touch_pins)

    print("Touchpads currently registering a touch:")
    print(cp.touched)

    if all(pad in cp.touched for pad in (board.A2, board.A3, board.A4)):
        print("This only prints when A2, A3, and A4 are being held at the same time!")

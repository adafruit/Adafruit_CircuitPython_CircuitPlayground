# SPDX-FileCopyrightText: 2021 Jeff Eplerfor Adafruit Industries
#
# SPDX-License-Identifier: MIT
class EventQueue:
    def __init__(self):
        self.overflowed = False

    def get(self):
        return None


class Keys:
    def __init__(self, pins, value_when_pressed, pull):
        self.key_count = len(pins)
        self.events = EventQueue()

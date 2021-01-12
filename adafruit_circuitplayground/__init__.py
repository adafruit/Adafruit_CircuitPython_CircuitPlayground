# SPDX-FileCopyrightText: 2019 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Verifies which board is being used and imports the appropriate module."""

import sys

if sys.platform == "nRF52840":
    from .bluefruit import cpb as cp
elif sys.platform == "Atmel SAMD21":
    from .express import cpx as cp

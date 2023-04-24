# SPDX-FileCopyrightText: 2019 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Verifies which board is being used and imports the appropriate module."""

import sys


class PlatformNotSupported:
    """throws exception when used"""

    def __getattribute__(self, *args, **kwargs):
        raise ImportError(f"{sys.platform} not supported by this lib")


if sys.platform == "nRF52840":
    from .bluefruit import cpb as cp
elif sys.platform == "Atmel SAMD21":
    from .express import cpx as cp
else:
    cp = PlatformNotSupported()

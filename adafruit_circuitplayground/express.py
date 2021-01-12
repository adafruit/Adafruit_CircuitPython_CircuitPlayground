# SPDX-FileCopyrightText: 2016 Scott Shawcroft for Adafruit Industries
# SPDX-FileCopyrightText: 2017-2019 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_circuitplayground.express`
====================================================

CircuitPython helper for Circuit Playground Express.

**Hardware:**

* `Circuit Playground Express <https://www.adafruit.com/product/3333>`_

* Author(s): Kattni Rembor, Scott Shawcroft
"""

import sys
import digitalio
import audioio

try:
    lib_index = sys.path.index("/lib")  # pylint: disable=invalid-name
    if lib_index < sys.path.index(".frozen"):
        # Prefer frozen modules over those in /lib.
        sys.path.insert(lib_index, ".frozen")
except ValueError:
    # Don't change sys.path if it doesn't contain "lib" or ".frozen".
    pass
from adafruit_circuitplayground.circuit_playground_base import (  # pylint: disable=wrong-import-position
    CircuitPlaygroundBase,
)


__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CircuitPlayground.git"


class Express(CircuitPlaygroundBase):
    """Represents a single CircuitPlayground Express. Do not use more than one at
    a time."""

    # Touch pad A7 is labeled both A7/TX on Circuit Playground Express and only TX on
    # the Circuit Playground Bluefruit. It is therefore referred to as TX in the
    # CircuitPlaygroundBase class, but can be used as either for Express.
    touch_A7 = CircuitPlaygroundBase.touch_TX
    _audio_out = audioio.AudioOut

    def __init__(self):
        # Only create the cpx module member when we aren't being imported by Sphinx
        if (
            "__module__" in dir(digitalio.DigitalInOut)
            and digitalio.DigitalInOut.__module__ == "sphinx.ext.autodoc"
        ):
            return

        super().__init__()

    @property
    def _unsupported(self):
        """This feature is not supported on Circuit Playground Express."""
        raise NotImplementedError(
            "This feature is not supported on Circuit Playground Express."
        )

    # The following is a list of the features available in other Circuit Playground modules but
    # not available for Circuit Playground Express. If called while using a Circuit Playground
    # Express, they will result in the NotImplementedError raised in the property above.
    sound_level = _unsupported
    loud_sound = _unsupported
    play_mp3 = _unsupported


cpx = Express()  # pylint: disable=invalid-name
"""Object that is automatically created on import.

   To use, simply import it from the module:

   .. code-block:: python

     from adafruit_circuitplayground.express import cpx
"""

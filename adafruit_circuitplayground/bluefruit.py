# The MIT License (MIT)
#
# Copyright (c) 2019 Kattni Rembor for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, bluefruit OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
`adafruit_circuitplayground.bluefruit`
====================================================

CircuitPython subclass for Circuit Playground Bluefruit.

* Author(s): Kattni Rembor

Implementation Notes
--------------------

**Hardware:**

* `Circuit Playground Bluefruit <https://www.adafruit.com/product/4333>`_

"""

import array
import math
import time
import audiocore
import digitalio
import board
import audiopwmio
import audiobusio
from adafruit_circuitplayground.circuit_playground_base import CircuitPlaygroundBase


__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CircuitPlayground.git"


class Bluefruit(CircuitPlaygroundBase):
    """Represents a single CircuitPlayground Bluefruit."""
    def __init__(self):
        # Only create the cpb module member when we aren't being imported by Sphinx
        if ("__module__" in dir(digitalio.DigitalInOut) and
                digitalio.DigitalInOut.__module__ == "sphinx.ext.autodoc"):
            return

        # Define audio:
        self._speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
        self._speaker_enable.switch_to_output(value=False)
        self._sample = None
        self._sine_wave = None
        self._sine_wave_sample = None

        # Define mic/sound sensor:
        self._mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
                                     sample_rate=16000, bit_depth=16)
        self._samples = None

        super().__init__()

    @staticmethod
    def _sine_sample(length):
        tone_volume = (2 ** 15) - 1
        shift = 2 ** 15
        for i in range(length):
            yield int(tone_volume * math.sin(2*math.pi*(i / length)) + shift)

    def _generate_sample(self, length=100):
        if self._sample is not None:
            return
        self._sine_wave = array.array("H", Bluefruit._sine_sample(length))
        self._sample = audiopwmio.PWMAudioOut(board.SPEAKER)
        self._sine_wave_sample = audiocore.RawSample(self._sine_wave)

    def play_tone(self, frequency, duration):
        """ Produce a tone using the speaker. Try changing frequency to change
        the pitch of the tone.

        :param int frequency: The frequency of the tone in Hz
        :param float duration: The duration of the tone in seconds

        .. image :: ../docs/_static/speaker.jpg
          :alt: Onboard speaker

        .. code-block:: python

            from adafruit_circuitplayground.bluefruit import cpb

            cpb.play_tone(440, 1)
        """
        # Play a tone of the specified frequency (hz).
        self.start_tone(frequency)
        time.sleep(duration)
        self.stop_tone()

    def start_tone(self, frequency):
        """ Produce a tone using the speaker. Try changing frequency to change
        the pitch of the tone.

        :param int frequency: The frequency of the tone in Hz

        .. image :: ../docs/_static/speaker.jpg
          :alt: Onboard speaker

        .. code-block:: python

             from adafruit_circuitplayground.bluefruit import cpb

             while True:
                 if cpb.button_a:
                     cpb.start_tone(262)
                 elif cpb.button_b:
                     cpb.start_tone(294)
                 else:
                     cpb.stop_tone()
        """
        self._speaker_enable.value = True
        length = 100
        if length * frequency > 350000:
            length = 350000 // frequency
        self._generate_sample(length)
        # Start playing a tone of the specified frequency (hz).
        self._sine_wave_sample.sample_rate = int(len(self._sine_wave) * frequency)
        if not self._sample.playing:
            self._sample.play(self._sine_wave_sample, loop=True)

    def stop_tone(self):
        """ Use with start_tone to stop the tone produced.

        .. image :: ../docs/_static/speaker.jpg
          :alt: Onboard speaker

        .. code-block:: python

             from adafruit_circuitplayground.bluefruit import cpb

             while True:
                 if cpb.button_a:
                     cpb.start_tone(262)
                 elif cpb.button_b:
                     cpb.start_tone(294)
                 else:
                     cpb.stop_tone()
        """
        # Stop playing any tones.
        if self._sample is not None and self._sample.playing:
            self._sample.stop()
            self._sample.deinit()
            self._sample = None
        self._speaker_enable.value = False

    def play_file(self, file_name):
        """ Play a .wav file using the onboard speaker.

        :param file_name: The name of your .wav file in quotation marks including .wav

        .. image :: ../docs/_static/speaker.jpg
          :alt: Onboard speaker

        .. code-block:: python

             from adafruit_circuitplayground.bluefruit import cpb

             while True:
                 if cpb.button_a:
                     cpb.play_file("laugh.wav")
                 elif cpb.button_b:
                     cpb.play_file("rimshot.wav")
        """
        # Play a specified file.
        self.stop_tone()
        self._speaker_enable.value = True
        with audiopwmio.PWMAudioOut(board.SPEAKER) as audio:
            wavefile = audiocore.WaveFile(open(file_name, "rb"))
            audio.play(wavefile)
            while audio.playing:
                pass
        self._speaker_enable.value = False

    @staticmethod
    def _normalized_rms(values):
        mean_values = int(sum(values) / len(values))
        return math.sqrt(sum(float(sample - mean_values) * (sample - mean_values)
                             for sample in values) / len(values))

    @property
    def sound_level(self):
        """Obtain the sound level from the microphone (sound sensor).

        .. image :: ../docs/_static/microphone.jpg
          :alt: Microphone (sound sensor)

        This example prints the sound levels. Try clapping or blowing on
        the microphone to see the levels change.

        .. code-block:: python

          from adafruit_circuitplayground.bluefruit import cpb

          while True:
              print(cpb.sound_level)
        """
        if self._sample is None:
            self._samples = array.array('H', [0] * 160)
        self._mic.record(self._samples, len(self._samples))
        return self._normalized_rms(self._samples)

    def loud_sound(self, sound_threshold=200):
        """Utilise a loud sound as an input.

        :param int sound_threshold: Threshold sound level must exceed to return true (Default: 200)

        .. image :: ../docs/_static/microphone.jpg
          :alt: Microphone (sound sensor)

        This example turns the LEDs red each time you make a loud sound.
        Try clapping or blowing onto the microphone to trigger it.

        .. code-block:: python

          from adafruit_circuitplayground.bluefruit import cpb

          while True:
              if cpb.loud_sound():
                  cpb.pixels.fill((50, 0, 0))
              else:
                  cpb.pixels.fill(0)

        You may find that the code is not responding how you would like.
        If this is the case, you can change the loud sound threshold to
        make it more or less responsive. Setting it to a higher number
        means it will take a louder sound to trigger. Setting it to a
        lower number will take a quieter sound to trigger. The following
        example shows the threshold being set to a higher number than
        the default.

        .. code-block:: python

          from adafruit_circuitplayground.bluefruit import cpb

          while True:
              if cpb.loud_sound(sound_threshold=300):
                  cpb.pixels.fill((50, 0, 0))
              else:
                  cpb.pixels.fill(0)
        """

        return self.sound_level > sound_threshold


cpb = Bluefruit()  # pylint: disable=invalid-name
"""Object that is automatically created on import.

   To use, simply import it from the module:

   .. code-block:: python

     from adafruit_circuitplayground.bluefruit import cpb
"""

# SPDX-FileCopyrightText: 2016 Scott Shawcroft for Adafruit Industries
# SPDX-FileCopyrightText: 2017-2019 Kattni Rembor for Adafruit Industries
# SPDX-FileCopyrightText: 2022 Ryan Keith for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# We have a lot of attributes for this complex library, as well as a lot of documentation.
# pylint: disable=too-many-instance-attributes, too-many-lines

"""
`adafruit_circuitplayground.circuit_playground_base`
====================================================

CircuitPython base class for Circuit Playground.

* `Circuit Playground Express <https://www.adafruit.com/product/3333>`_
* `Circuit Playground Bluefruit <https://www.adafruit.com/product/4333>`_.

* Author(s): Kattni Rembor, Scott Shawcroft, Ryan Keith
"""

import math
import array
import time
import os
import audiocore
import analogio
import board
import busio
import digitalio
import adafruit_lis3dh
import adafruit_thermistor
import neopixel
import touchio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CircuitPlayground.git"


class Photocell:
    """Simple driver for analog photocell on the Circuit Playground Express and Bluefruit."""

    # pylint: disable=too-few-public-methods
    def __init__(self, pin):
        self._photocell = analogio.AnalogIn(pin)

    # TODO(tannewt): Calibrate this against another calibrated sensor.
    @property
    def light(self):
        """Light level."""
        return self._photocell.value * 330 // (2**16)


class CircuitPlaygroundBase:  # pylint: disable=too-many-public-methods
    """Circuit Playground base class."""

    _audio_out = None
    SINE_WAVE = 0
    SQUARE_WAVE = 1

    def __init__(self):
        # Define switch:
        self._switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
        self._switch.switch_to_input(pull=digitalio.Pull.UP)

        # Define LEDs:
        self._led = digitalio.DigitalInOut(board.D13)
        self._led.switch_to_output()
        self._pixels = neopixel.NeoPixel(board.NEOPIXEL, 10)

        # Define sensors:
        self._temp = adafruit_thermistor.Thermistor(
            board.TEMPERATURE, 10000, 10000, 25, 3950
        )
        self._light = Photocell(board.LIGHT)

        # Define touch:
        # Initially, self._touches stores the pin used for a particular touch. When that touch is
        # used for the first time, the pin is replaced with the corresponding TouchIn object.
        # This saves a little RAM over using a separate read-only pin tuple.
        # For example, after `cp.touch_A2`, self._touches is equivalent to:
        # [None, board.A1, touchio.TouchIn(board.A2), board.A3, ...]
        # Slot 0 is not used (A0 is not allowed as a touch pin).
        self._touches = [
            None,
            board.A1,
            board.A2,
            board.A3,
            board.A4,
            board.A5,
            board.A6,
            board.TX,
        ]
        self._touch_threshold_adjustment = 0

        # Define acceleration:
        self._i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
        self._int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
        self._lis3dh = adafruit_lis3dh.LIS3DH_I2C(
            self._i2c, address=0x19, int1=self._int1
        )
        self._lis3dh.range = adafruit_lis3dh.RANGE_8_G

        # Define audio:
        self._speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
        self._speaker_enable.switch_to_output(value=False)
        self._sample = None
        self._wave = None
        self._wave_sample = None

        # Initialise tap:
        self._detect_taps = 1
        self.detect_taps = 1

        # Initialise buttons:
        self._a = None
        self._b = None

    @property
    def detect_taps(self):
        """Configure what type of tap is detected by ``cp.tapped``. Use ``1`` for single-tap
        detection and ``2`` for double-tap detection. This does nothing without ``cp.tapped``.

        .. image :: ../docs/_static/accelerometer.jpg
          :alt: Accelerometer

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp

          cp.detect_taps = 1
          while True:
            if cp.tapped:
              print("Single tap detected!")
        """
        return self._detect_taps

    @staticmethod
    def _default_tap_threshold(tap):
        if (
            "nRF52840" in os.uname().machine
        ):  # If we're on a CPB, use a higher tap threshold
            return 100 if tap == 1 else 70

        # If we're on a CPX
        return 90 if tap == 1 else 60

    @detect_taps.setter
    def detect_taps(self, value):
        self._detect_taps = value
        if value == 1:
            self._lis3dh.set_tap(
                value,
                self._default_tap_threshold(value),
                time_limit=4,
                time_latency=50,
                time_window=255,
            )
        if value == 2:
            self._lis3dh.set_tap(
                value,
                self._default_tap_threshold(value),
                time_limit=10,
                time_latency=50,
                time_window=255,
            )

    def configure_tap(  # pylint: disable-msg=too-many-arguments
        self,
        tap,
        accel_range=adafruit_lis3dh.RANGE_8_G,
        threshold=None,
        time_limit=None,
        time_latency=50,
        time_window=255,
    ):
        """Granular configuration of tap parameters. Expose the power of the
        adafruit_lis3dh module.

        :param int tap: 0 to disable tap detection, 1 to detect only single
                        taps, and 2 to detect only double taps.
        :param int accel_range: Takes the defined values from the adafruit_lis3dh
                        module [ RANGE_2_G, RANGE_4_G, RANGE_8_G, RANGE_16_G ]
                        (default sets the same value as the *detect_taps* setter)
        :param int threshold: A threshold for the tap detection.  The higher the value
                        the less sensitive the detection.  This changes based on the
                        accelerometer range.  Good values are 5-10 for 16G, 10-20
                        for 8G, 20-40 for 4G, and 40-80 for 2G.
                        (default sets the same value as the *detect_taps* setter)
        :param int time_limit: TIME_LIMIT register value
                        (default sets the same value as the *detect_taps* setter)
        :param int time_latency: TIME_LATENCY register value (default 50).
        :param int time_window: TIME_WINDOW register value (default 255).

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp
          import adafruit_lis3dh

          cp.configure_tap(1, accel_range=adafruit_lis3dh.RANGE_2_G, threshold=50)
          while True:
            if cp.tapped:
              print("Single tap detected!")

        """
        if tap < 0 or tap > 2:
            return

        self._detect_taps = tap

        if accel_range not in [
            adafruit_lis3dh.RANGE_2_G,
            adafruit_lis3dh.RANGE_4_G,
            adafruit_lis3dh.RANGE_8_G,
            adafruit_lis3dh.RANGE_16_G,
        ]:
            accel_range = adafruit_lis3dh.RANGE_8_G
        self._lis3dh.range = accel_range

        if tap == 1:
            if threshold is None or threshold < 0 or threshold > 127:
                threshold = self._default_tap_threshold(tap)
            if time_limit is None:
                time_limit = 4
        elif tap == 2:
            if threshold is None or threshold < 0 or threshold > 127:
                threshold = self._default_tap_threshold(tap)
            if time_limit is None:
                time_limit = 10
        else:
            # reasonable values for turning the tap detection off
            threshold = 100
            time_limit = 1

        self._lis3dh.set_tap(
            tap,
            threshold,
            time_limit=time_limit,
            time_latency=time_latency,
            time_window=time_window,
        )

    @property
    def tapped(self):
        """True once after a detecting a tap. Requires ``cp.detect_taps``.

        .. image :: ../docs/_static/accelerometer.jpg
          :alt: Accelerometer

        Tap the Circuit Playground once for a single-tap, or quickly tap twice for a double-tap.

        To use with Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp

          cp.detect_taps = 1

          while True:
              if cp.tapped:
                  print("Single tap detected!")

        To use single and double tap together, you must have a delay between them. It
        will not function properly without it. This example uses both by counting a
        specified number of each type of tap before moving on in the code.

        .. code-block:: python

          from adafruit_circuitplayground import cp

          # Set to check for single-taps.
          cp.detect_taps = 1
          tap_count = 0

          # We're looking for 2 single-taps before moving on.
          while tap_count < 2:
              if cp.tapped:
                  tap_count += 1
          print("Reached 2 single-taps!")

          # Now switch to checking for double-taps
          tap_count = 0
          cp.detect_taps = 2

          # We're looking for 2 double-taps before moving on.
          while tap_count < 2:
              if cp.tapped:
                 tap_count += 1
          print("Reached 2 double-taps!")
          print("Done.")
        """
        return self._lis3dh.tapped

    @property
    def acceleration(self):
        """Obtain data from the x, y and z axes.

        .. image :: ../docs/_static/accelerometer.jpg
          :alt: Accelerometer

        This example prints the values. Try moving the board to see how the
        printed values change.

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp

          while True:
              x, y, z = cp.acceleration
              print(x, y, z)
        """
        return self._lis3dh.acceleration

    def shake(self, shake_threshold=30):
        """Detect when device is shaken.

        :param int shake_threshold: The threshold shake must exceed to return true (Default: 30)

        .. image :: ../docs/_static/accelerometer.jpg
          :alt: Accelerometer

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp

          while True:
              if cp.shake():
                  print("Shake detected!")

        Decreasing ``shake_threshold`` increases shake sensitivity, i.e. the code
        will return a shake detected more easily with a lower ``shake_threshold``.
        Increasing it causes the opposite. ``shake_threshold`` requires a minimum
        value of 10 - 10 is the value when the board is not moving, therefore
        anything less than 10 will erroneously report a constant shake detected.

        .. code-block:: python

          from adafruit_circuitplayground import cp

          while True:
              if cp.shake(shake_threshold=20):
                  print("Shake detected more easily than before!")
        """
        return self._lis3dh.shake(shake_threshold=shake_threshold)

    def _touch(self, i):
        if not isinstance(self._touches[i], touchio.TouchIn):
            # First time referenced. Get the pin from the slot for this touch
            # and replace it with a TouchIn object for the pin.
            self._touches[i] = touchio.TouchIn(self._touches[i])
            self._touches[i].threshold += self._touch_threshold_adjustment
        return self._touches[i].value

    # We chose these verbose touch_A# names so that beginners could use it without understanding
    # lists and the capital A to match the pin name. The capitalization is not strictly Python
    # style, so everywhere we use these names, we whitelist the errors using:
    @property
    def touch_A1(self):  # pylint: disable=invalid-name
        """Detect touch on capacitive touch pad A1.

        .. image :: ../docs/_static/capacitive_touch_pad_A1.jpg
          :alt: Capacitive touch pad A1

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp

          while True:
              if cp.touch_A1:
                  print('Touched pad A1')
        """
        return self._touch(1)

    @property
    def touch_A2(self):  # pylint: disable=invalid-name
        """Detect touch on capacitive touch pad A2.

        .. image :: ../docs/_static/capacitive_touch_pad_A2.jpg
          :alt: Capacitive touch pad A2

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp

          while True:
              if cp.touch_A2:
                  print('Touched pad A2')
        """
        return self._touch(2)

    @property
    def touch_A3(self):  # pylint: disable=invalid-name
        """Detect touch on capacitive touch pad A3.

        .. image :: ../docs/_static/capacitive_touch_pad_A3.jpg
          :alt: Capacitive touch pad A3

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp

          while True:
              if cp.touch_A3:
                  print('Touched pad A3')
        """
        return self._touch(3)

    @property
    def touch_A4(self):  # pylint: disable=invalid-name
        """Detect touch on capacitive touch pad A4.

        .. image :: ../docs/_static/capacitive_touch_pad_A4.jpg
          :alt: Capacitive touch pad A4

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp

          while True:
              if cp.touch_A4:
                  print('Touched pad A4')
        """
        return self._touch(4)

    @property
    def touch_A5(self):  # pylint: disable=invalid-name
        """Detect touch on capacitive touch pad A5.

        .. image :: ../docs/_static/capacitive_touch_pad_A5.jpg
          :alt: Capacitive touch pad A5

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp

          while True:
              if cp.touch_A5:
                  print('Touched pad A5')
        """
        return self._touch(5)

    @property
    def touch_A6(self):  # pylint: disable=invalid-name
        """Detect touch on capacitive touch pad A6.

        .. image :: ../docs/_static/capacitive_touch_pad_A6.jpg
          :alt: Capacitive touch pad A6

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp

          while True:
              if cp.touch_A6:
                  print('Touched pad A6'
        """
        return self._touch(6)

    @property
    def touch_TX(self):  # pylint: disable=invalid-name
        """Detect touch on capacitive touch pad TX (also known as A7 on the Circuit Playground
        Express) Note: can be called as ``touch_A7`` on Circuit Playground Express.

        .. image :: ../docs/_static/capacitive_touch_pad_A7.jpg
          :alt: Capacitive touch pad TX

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp

          while True:
              if cp.touch_A7:
                  print('Touched pad A7')
        """
        return self._touch(7)

    def adjust_touch_threshold(self, adjustment):
        """Adjust the threshold needed to activate the capacitive touch pads.
        Higher numbers make the touch pads less sensitive.

        :param int adjustment: The desired threshold increase

        .. image :: ../docs/_static/capacitive_touch_pads.jpg
          :alt: Capacitive touch pads

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp

          cp.adjust_touch_threshold(200)

          while True:
              if cp.touch_A1:
                  print('Touched pad A1')
        """
        for touch_in in self._touches:
            if isinstance(touch_in, touchio.TouchIn):
                touch_in.threshold += adjustment
        self._touch_threshold_adjustment += adjustment

    @property
    def pixels(self):
        """Sequence-like object representing the ten NeoPixels around the outside
        of the Circuit Playground. Each pixel is at a certain index in the sequence
        as labeled below. Colors can be RGB hex like 0x110000 for red where each
        two digits are a color (0xRRGGBB) or a tuple like (17, 0, 0) where (R, G, B).
        Set the global brightness using any number from 0 to 1 to represent a
        percentage, i.e. 0.3 sets global brightness to 30%.

        See `neopixel.NeoPixel` for more info.

        .. image :: ../docs/_static/neopixel_numbering.jpg
          :alt: NeoPixel order diagram

        Here is an example that sets the first pixel green and the ninth red.

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp

          cp.pixels.brightness = 0.3
          cp.pixels[0] = 0x00FF00
          cp.pixels[9] = (255, 0, 0)
        """
        return self._pixels

    @property
    def button_a(self):
        """``True`` when Button A is pressed. ``False`` if not.

        .. image :: ../docs/_static/button_a.jpg
          :alt: Button A

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp

          while True:
              if cp.button_a:
                  print("Button A pressed!")
        """
        if self._a is None:
            self._a = digitalio.DigitalInOut(board.BUTTON_A)
            self._a.switch_to_input(pull=digitalio.Pull.DOWN)
        return self._a.value

    @property
    def button_b(self):
        """``True`` when Button B is pressed. ``False`` if not.

        .. image :: ../docs/_static/button_b.jpg
          :alt: Button B

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp

          while True:
              if cp.button_b:
                  print("Button B pressed!")
        """
        if self._b is None:
            self._b = digitalio.DigitalInOut(board.BUTTON_B)
            self._b.switch_to_input(pull=digitalio.Pull.DOWN)
        return self._b.value

    @property
    def switch(self):
        """``True`` when the switch is to the left next to the music notes.
        ``False`` when it is to the right towards the ear.

        .. image :: ../docs/_static/slide_switch.jpg
          :alt: Slide switch

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp
         import time

          while True:
              print("Slide switch:", cp.switch)
              time.sleep(0.1)
        """
        return self._switch.value

    @property
    def temperature(self):
        """The temperature in Celsius.

        .. image :: ../docs/_static/thermistor.jpg
          :alt: Temperature sensor

        Converting this to Fahrenheit is easy!

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp
          import time

          while True:
              temperature_c = cp.temperature
              temperature_f = temperature_c * 1.8 + 32
              print("Temperature celsius:", temperature_c)
              print("Temperature fahrenheit:", temperature_f)
              time.sleep(1)
        """
        return self._temp.temperature

    @property
    def light(self):
        """The light level.

        .. image :: ../docs/_static/light_sensor.jpg
          :alt: Light sensor

        Try covering the sensor next to the eye to see it change.

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp
          import time

          while True:
              print("Light:", cp.light)
              time.sleep(1)
        """
        return self._light.light

    @property
    def red_led(self):
        """The red led next to the USB plug marked D13.

        .. image :: ../docs/_static/red_led.jpg
          :alt: D13 LED

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

          from adafruit_circuitplayground import cp
          import time

          while True:
              cp.red_led = True
              time.sleep(0.5)
              cp.red_led = False
              time.sleep(0.5)
        """
        return self._led.value

    @red_led.setter
    def red_led(self, value):
        self._led.value = value

    @staticmethod
    def _sine_sample(length):
        tone_volume = (2**15) - 1
        # Amplitude shift up in order to not have negative numbers
        shift = 2**15
        for i in range(length):
            yield int(tone_volume * math.sin(2 * math.pi * (i / length)) + shift)

    @staticmethod
    def _square_sample(length):
        # Square waves are MUCH louder than then sine
        tone_volume = (2**16) - 1
        half_length = length // 2
        for _ in range(half_length):
            yield tone_volume
        for _ in range(half_length):
            yield 0

    def _generate_sample(self, length=100, waveform=SINE_WAVE):
        if self._sample is not None:
            return
        if waveform == self.SQUARE_WAVE:
            self._wave = array.array("H", self._square_sample(length))
        else:
            self._wave = array.array("H", self._sine_sample(length))
        self._sample = self._audio_out(board.SPEAKER)  # pylint: disable=not-callable
        self._wave_sample = audiocore.RawSample(self._wave)

    def play_tone(self, frequency, duration, waveform=SINE_WAVE):
        """Produce a tone using the speaker. Try changing frequency to change
        the pitch of the tone.

        :param int frequency: The frequency of the tone in Hz
        :param float duration: The duration of the tone in seconds
        :param str waveform: Type of waveform to be generated [SINE_WAVE, SQUARE_WAVE].

        Default is SINE_WAVE.

        .. image :: ../docs/_static/speaker.jpg
          :alt: Onboard speaker

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

            from adafruit_circuitplayground import cp

            cp.play_tone(440, 1)
        """
        # Play a tone of the specified frequency (hz).
        self.start_tone(frequency, waveform)
        time.sleep(duration)
        self.stop_tone()

    def start_tone(self, frequency, waveform=SINE_WAVE):
        """Produce a tone using the speaker. Try changing frequency to change
        the pitch of the tone.

        :param int frequency: The frequency of the tone in Hz
        :param str waveform: Type of waveform to be generated [SINE_WAVE, SQUARE_WAVE].

        Default is SINE_WAVE.

        .. image :: ../docs/_static/speaker.jpg
          :alt: Onboard speaker

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

             from adafruit_circuitplayground import cp

             while True:
                 if cp.button_a:
                     cp.start_tone(262)
                 elif cp.button_b:
                     cp.start_tone(294)
                 else:
                     cp.stop_tone()
        """
        self._speaker_enable.value = True
        length = 100
        if length * frequency > 350000:
            length = 350000 // frequency
        self._generate_sample(length, waveform)
        # Start playing a tone of the specified frequency (hz).
        self._wave_sample.sample_rate = int(len(self._wave) * frequency)
        if not self._sample.playing:
            self._sample.play(self._wave_sample, loop=True)

    def stop_tone(self):
        """Use with start_tone to stop the tone produced.

        .. image :: ../docs/_static/speaker.jpg
          :alt: Onboard speaker

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

             from adafruit_circuitplayground import cp

             while True:
                 if cp.button_a:
                     cp.start_tone(262)
                 elif cp.button_b:
                     cp.start_tone(294)
                 else:
                     cp.stop_tone()
        """
        # Stop playing any tones.
        if self._sample is not None and self._sample.playing:
            self._sample.stop()
            self._sample.deinit()
            self._sample = None
        self._speaker_enable.value = False

    def play_file(self, file_name):
        """Play a .wav file using the onboard speaker.

        :param file_name: The name of your .wav file in quotation marks including .wav

        .. image :: ../docs/_static/speaker.jpg
          :alt: Onboard speaker

        To use with the Circuit Playground Express or Bluefruit:

        .. code-block:: python

             from adafruit_circuitplayground import cp

             while True:
                 if cp.button_a:
                     cp.play_file("laugh.wav")
                 elif cp.button_b:
                     cp.play_file("rimshot.wav")
        """
        # Play a specified file.
        self.stop_tone()
        self._speaker_enable.value = True
        with self._audio_out(  # pylint: disable=not-callable
            board.SPEAKER
        ) as audio, audiocore.WaveFile(open(file_name, "rb")) as wavefile:
            audio.play(wavefile)
            while audio.playing:
                pass
        self._speaker_enable.value = False

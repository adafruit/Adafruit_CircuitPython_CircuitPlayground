# The MIT License (MIT)
#
# Copyright (c) 2016 Scott Shawcroft for Adafruit Industries
# Copyright (c) 2017-2018 Kattni Rembor for Adafruit Industries
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
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# We have a lot of attributes for this complex library.
# pylint: disable=too-many-instance-attributes

"""
`adafruit_circuitplayground.express`
====================================================

CircuitPython driver from `CircuitPlayground Express <https://www.adafruit.com/product/3333>`_.

* Author(s): Kattni Rembor, Scott Shawcroft
"""

import array
import math
import sys
import time
# pylint: disable=wrong-import-position
sys.path.insert(0, ".frozen")  # prefer frozen modules over local

import adafruit_lis3dh
import adafruit_thermistor
import analogio
import audioio
import board
import busio
import digitalio
import neopixel
import touchio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CircuitPlayground.git"


class Photocell:
    """Simple driver for analog photocell on the CircuitPlayground Express."""
    # pylint: disable=too-few-public-methods
    def __init__(self, pin):
        self._photocell = analogio.AnalogIn(pin)

    # TODO(tannewt): Calibrate this against another calibrated sensor.
    @property
    def light(self):
        """Light level in SI Lux."""
        return self._photocell.value * 330 // (2 ** 16)


class Express:     # pylint: disable=too-many-public-methods
    """Represents a single CircuitPlayground Express. Do not use more than one at
       a time."""
    def __init__(self):
        # Only create the cpx module member when we're aren't being imported by Sphinx
        if ("__module__" in dir(digitalio.DigitalInOut) and
                digitalio.DigitalInOut.__module__ == "sphinx.ext.autodoc"):
            return
        self._a = digitalio.DigitalInOut(board.BUTTON_A)
        self._a.switch_to_input(pull=digitalio.Pull.DOWN)
        self._b = digitalio.DigitalInOut(board.BUTTON_B)
        self._b.switch_to_input(pull=digitalio.Pull.DOWN)

        # Define switch:
        self._switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
        self._switch.switch_to_input(pull=digitalio.Pull.UP)

        # Define LEDs:
        self._led = digitalio.DigitalInOut(board.D13)
        self._led.switch_to_output()
        self._pixels = neopixel.NeoPixel(board.NEOPIXEL, 10)

        # Define sensors:
        self._temp = adafruit_thermistor.Thermistor(board.TEMPERATURE, 10000, 10000, 25, 3950)
        self._light = Photocell(board.LIGHT)

        # Define audio:
        self._speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
        self._speaker_enable.switch_to_output(value=False)
        self._sample = None
        self._sine_wave = None

        # Define touch:
        # We chose these verbose touch_A# names so that beginners could use it without understanding
        # lists and the capital A to match the pin name. The capitalization is not strictly Python
        # style, so everywhere we use these names, we whitelist the errors using:
        # pylint: disable=invalid-name
        self._touch_A1 = None
        self._touch_A2 = None
        self._touch_A3 = None
        self._touch_A4 = None
        self._touch_A5 = None
        self._touch_A6 = None
        self._touch_A7 = None
        self._touch_threshold_adjustment = 0

        # Define acceleration:
        self._i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
        self._int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
        try:
            self._lis3dh = adafruit_lis3dh.LIS3DH_I2C(self._i2c, address=0x19, int1=self._int1)
        except TypeError:
            self._lis3dh = adafruit_lis3dh.LIS3DH_I2C(self._i2c, address=0x19)
        self._lis3dh.range = adafruit_lis3dh.RANGE_8_G

        # Initialise tap:
        self._detect_taps = 1
        self.detect_taps = 1

    @property
    def detect_taps(self):
        """Configure what type of tap is detected by ``cpx.tapped``. Use ``1`` for single-tap
        detection and ``2`` for double-tap detection. This does nothing without ``cpx.tapped``.

        .. image :: ../docs/_static/accelerometer.jpg
          :alt: Accelerometer

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          cpx.detect_taps = 1
          while True:
            if cpx.tapped:
              print("Single tap detected!")
        """
        return self._detect_taps

    @detect_taps.setter
    def detect_taps(self, value):
        self._detect_taps = value
        try:
            if value == 1:
                self._lis3dh.set_tap(value, 90, time_limit=4, time_latency=50, time_window=255)
            if value == 2:
                self._lis3dh.set_tap(value, 60, time_limit=10, time_latency=50, time_window=255)
        except AttributeError:
            pass

    @property
    def tapped(self):
        """True once after a detecting a tap. Requires ``cpx.detect_taps``.

        .. image :: ../docs/_static/accelerometer.jpg
          :alt: Accelerometer

        Tap the CPX once for a single-tap, or quickly tap twice for a double-tap.

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          cpx.detect_taps = 1

          while True:
              if cpx.tapped:
                  print("Single tap detected!")

        To use single and double tap together, you must have a delay between them. It
        will not function properly without it. This example uses both by counting a
        specified number of each type of tap before moving on in the code.

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          # Set to check for single-taps.
          cpx.detect_taps = 1
          tap_count = 0

          # We're looking for 2 single-taps before moving on.
          while tap_count < 2:
              if cpx.tapped:
                  tap_count += 1
          print("Reached 2 single-taps!")

          # Now switch to checking for double-taps
          tap_count = 0
          cpx.detect_taps = 2

          # We're looking for 2 double-taps before moving on.
          while tap_count < 2:
              if cpx.tapped:
                 tap_count += 1
          print("Reached 2 double-taps!")
          print("Done.")

        """
        try:
            return self._lis3dh.tapped
        except AttributeError:
            raise RuntimeError("Oops! You need a newer version of CircuitPython "
                               "(2.2.0 or greater) to use this feature.")

    @property
    def acceleration(self):
        """Obtain data from the x, y and z axes.

        .. image :: ../docs/_static/accelerometer.jpg
          :alt: Accelerometer

        This example prints the values. Try moving the board to see how the
        printed values change.

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              x, y, z = cpx.acceleration
              print(x, y, z)
        """
        return self._lis3dh.acceleration

    def shake(self, shake_threshold=30):
        """Detect when device is shaken.

        :param int shake_threshold: The threshold shake must exceed to return true (Default: 30)

        .. image :: ../docs/_static/accelerometer.jpg
          :alt: Accelerometer

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if cpx.shake():
                  print("Shake detected!")

        Decreasing ``shake_threshold`` increases shake sensitivity, i.e. the code
        will return a shake detected more easily with a lower ``shake_threshold``.
        Increasing it causes the opposite. ``shake_threshold`` requires a minimum
        value of 10 - 10 is the value when the board is not moving, therefore
        anything less than 10 will erroneously report a constant shake detected.

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if cpx.shake(shake_threshold=20):
                  print("Shake detected more easily than before!")
        """
        try:
            return self._lis3dh.shake(shake_threshold=shake_threshold)
        except AttributeError:
            raise RuntimeError("Oops! You need a newer version of CircuitPython "
                               "(2.2.0 or greater) to use this feature.")

    @property
    def touch_A1(self): # pylint: disable=invalid-name
        """Detect touch on capacitive touch pad A1.

        .. image :: ../docs/_static/capacitive_touch_pad_A1.jpg
          :alt: Capacitive touch pad A1

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if cpx.touch_A1:
                  print('Touched pad A1')
        """
        if self._touch_A1 is None:
            self._touch_A1 = touchio.TouchIn(board.A1)
            self._touch_A1.threshold += self._touch_threshold_adjustment
        return self._touch_A1.value

    @property
    def touch_A2(self): # pylint: disable=invalid-name
        """Detect touch on capacitive touch pad A2.

        .. image :: ../docs/_static/capacitive_touch_pad_A2.jpg
          :alt: Capacitive touch pad A2

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if cpx.touch_A2:
                  print('Touched pad A2')
        """
        if self._touch_A2 is None:
            self._touch_A2 = touchio.TouchIn(board.A2)
            self._touch_A2.threshold += self._touch_threshold_adjustment
        return self._touch_A2.value

    @property
    def touch_A3(self): # pylint: disable=invalid-name
        """Detect touch on capacitive touch pad A3.

        .. image :: ../docs/_static/capacitive_touch_pad_A3.jpg
          :alt: Capacitive touch pad A3

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if cpx.touch_A3:
                  print('Touched pad A3')
        """
        if self._touch_A3 is None:
            self._touch_A3 = touchio.TouchIn(board.A3)
            self._touch_A3.threshold += self._touch_threshold_adjustment
        return self._touch_A3.value

    @property
    def touch_A4(self): # pylint: disable=invalid-name
        """Detect touch on capacitive touch pad A4.

        .. image :: ../docs/_static/capacitive_touch_pad_A4.jpg
          :alt: Capacitive touch pad A4

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if cpx.touch_A4:
                  print('Touched pad A4')
        """
        if self._touch_A4 is None:
            self._touch_A4 = touchio.TouchIn(board.A4)
            self._touch_A4.threshold += self._touch_threshold_adjustment
        return self._touch_A4.value

    @property
    def touch_A5(self): # pylint: disable=invalid-name
        """Detect touch on capacitive touch pad A5.

        .. image :: ../docs/_static/capacitive_touch_pad_A5.jpg
          :alt: Capacitive touch pad A5

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if cpx.touch_A5:
                  print('Touched pad A5')
        """
        if self._touch_A5 is None:
            self._touch_A5 = touchio.TouchIn(board.A5)
            self._touch_A5.threshold += self._touch_threshold_adjustment
        return self._touch_A5.value

    @property
    def touch_A6(self): # pylint: disable=invalid-name
        """Detect touch on capacitive touch pad A6.

        .. image :: ../docs/_static/capacitive_touch_pad_A6.jpg
          :alt: Capacitive touch pad A6

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if cpx.touch_A6:
                  print('Touched pad A6')
        """
        if self._touch_A6 is None:
            self._touch_A6 = touchio.TouchIn(board.A6)
            self._touch_A6.threshold += self._touch_threshold_adjustment
        return self._touch_A6.value

    @property
    def touch_A7(self): # pylint: disable=invalid-name
        """Detect touch on capacitive touch pad A7.

        .. image :: ../docs/_static/capacitive_touch_pad_A7.jpg
          :alt: Capacitive touch pad A7

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if cpx.touch_A7:
                  print('Touched pad A7')
        """
        if self._touch_A7 is None:
            self._touch_A7 = touchio.TouchIn(board.A7)
            self._touch_A7.threshold += self._touch_threshold_adjustment
        return self._touch_A7.value

    def adjust_touch_threshold(self, adjustment):
        """Adjust the threshold needed to activate the capacitive touch pads.
        Higher numbers make the touch pads less sensitive.

        :param int adjustment: The desired threshold increase

        .. image :: ../docs/_static/capacitive_touch_pads.jpg
          :alt: Capacitive touch pads

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          cpx.adjust_touch_threshold(200)

          while True:
              if cpx.touch_A1:
                  print('Touched pad A1')
        """
        for pad_name in ["_touch_A" + str(x) for x in range(1, 8)]:
            touch_in = getattr(self, pad_name)
            if touch_in:
                touch_in.threshold += adjustment
        self._touch_threshold_adjustment += adjustment

    @property
    def pixels(self):
        """Sequence like object representing the ten NeoPixels around the outside
        of the CircuitPlayground. Each pixel is at a certain index in the sequence
        as labeled below. Colors can be RGB hex like 0x110000 for red where each
        two digits are a color (0xRRGGBB) or a tuple like (17, 0, 0) where (R, G, B).
        Set the global brightness using any number from 0 to 1 to represent a
        percentage, i.e. 0.3 sets global brightness to 30%.

        See `neopixel.NeoPixel` for more info.

        .. image :: ../docs/_static/neopixel_numbering.jpg
          :alt: NeoPixel order diagram

        Here is an example that sets the first pixel green and the second red.

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          cpx.pixels.brightness = 0.3
          cpx.pixels[0] = 0x003000
          cpx.pixels[9] = (30, 0, 0)

          # Wait forever. CTRL-C to quit.
          while True:
              pass
        """
        return self._pixels

    @property
    def button_a(self):
        """``True`` when Button A is pressed. ``False`` if not.

            .. image :: ../docs/_static/button_a.jpg
              :alt: Button A

            .. code-block:: python

              from adafruit_circuitplayground.express import cpx

              while True:
                  if cpx.button_a:
                      print("Button A pressed!")
        """
        return self._a.value

    @property
    def button_b(self):
        """``True`` when Button B is pressed. ``False`` if not.

            .. image :: ../docs/_static/button_b.jpg
              :alt: Button B

            .. code-block:: python

              from adafruit_circuitplayground.express import cpx

              while True:
                  if cpx.button_b:
                      print("Button B pressed!")
        """
        return self._b.value

    @property
    def switch(self):
        """
          ``True`` when the switch is to the left next to the music notes.
          ``False`` when it is to the right towards the ear.

          .. image :: ../docs/_static/slide_switch.jpg
            :alt: Slide switch

          .. code-block:: python

            from adafruit_circuitplayground.express import cpx
            import time

            while True:
                print("Slide switch:", cpx.switch)
                time.sleep(1)
            """
        return self._switch.value

    @property
    def temperature(self):
        """The temperature of the CircuitPlayground in Celsius.

            .. image :: ../docs/_static/thermistor.jpg
              :alt: Temperature sensor

           Converting this to Farenheit is easy!

            .. code-block:: python

              from adafruit_circuitplayground.express import cpx
              import time

              while True:
                  temperature_c = cpx.temperature
                  temperature_f = temperature_c * 1.8 + 32
                  print("Temperature celsius:", temperature_c)
                  print("Temperature fahrenheit:", temperature_f)
                  time.sleep(1)
        """
        return self._temp.temperature

    @property
    def light(self):
        """The brightness of the CircuitPlayground in approximate Lux.

           .. image :: ../docs/_static/light_sensor.jpg
             :alt: Light sensor

           Try covering the sensor next to the eye to see it change.

           .. code-block:: python

             from adafruit_circuitplayground.express import cpx
             import time

             while True:
                 print("Lux:", cpx.light)
                 time.sleep(1)
        """
        return self._light.light

    @property
    def red_led(self):
        """The red led next to the USB plug marked D13.

           .. image :: ../docs/_static/red_led.jpg
             :alt: D13 LED

           .. code-block:: python

             from adafruit_circuitplayground.express import cpx
             import time

             while True:
                 cpx.red_led = True
                 time.sleep(1)
                 cpx.red_led = False
                 time.sleep(1)
        """
        return self._led.value

    @red_led.setter
    def red_led(self, value):
        self._led.value = value

    @staticmethod
    def _sine_sample(length):
        tone_volume = (2 ** 15) - 1
        shift = 2 ** 15
        for i in range(length):
            yield int(tone_volume * math.sin(2*math.pi*(i / length)) + shift)

    def _generate_sample(self):
        if self._sample is not None:
            return
        length = 100
        self._sine_wave = array.array("H", Express._sine_sample(length))
        self._sample = audioio.AudioOut(board.SPEAKER, self._sine_wave)

    def play_tone(self, frequency, duration):
        """ Produce a tone using the speaker. Try changing frequency to change
        the pitch of the tone.

        :param int frequency: The frequency of the tone in Hz
        :param float duration: The duration of the tone in seconds

        .. image :: ../docs/_static/speaker.jpg
          :alt: Onboard speaker

        .. code-block:: python

            from adafruit_circuitplayground.express import cpx

            cpx.play_tone(440, 1)
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

             from adafruit_circuitplayground.express import cpx

             while True:
                 if cpx.button_a:
                     cpx.start_tone(262)
                 elif cpx.button_b:
                     cpx.start_tone(294)
                 else:
                     cpx.stop_tone()
        """
        self._speaker_enable.value = True
        self._generate_sample()
        # Start playing a tone of the specified frequency (hz).
        self._sample.frequency = int(len(self._sine_wave) * frequency)
        if not self._sample.playing:
            self._sample.play(loop=True)

    def stop_tone(self):
        """ Use with start_tone to stop the tone produced.

        .. image :: ../docs/_static/speaker.jpg
          :alt: Onboard speaker

        .. code-block:: python

             from adafruit_circuitplayground.express import cpx

             while True:
                 if cpx.button_a:
                     cpx.start_tone(262)
                 elif cpx.button_b:
                     cpx.start_tone(294)
                 else:
                     cpx.stop_tone()
        """
        # Stop playing any tones.
        if self._sample is not None and self._sample.playing:
            self._sample.stop()
        self._speaker_enable.value = False

    def play_file(self, file_name):
        """ Play a .wav file using the onboard speaker.

        :param file_name: The name of your .wav file in quotation marks including .wav

        .. image :: ../docs/_static/speaker.jpg
          :alt: Onboard speaker

        .. code-block:: python

             from adafruit_circuitplayground.express import cpx

             while True:
                 if cpx.button_a:
                     cpx.play_file("laugh.wav")
                 elif cpx.button_b:
                     cpx.play_file("rimshot.wav")
        """
        # Play a specified file.
        self._speaker_enable.value = True
        if sys.implementation.version[0] == 3:
            audio = audioio.AudioOut(board.SPEAKER)
            file = audioio.WaveFile(open(file_name, "rb"))
            audio.play(file)
            while audio.playing:
                pass
        else:
            audio = audioio.AudioOut(board.SPEAKER, open(file_name, "rb"))
            audio.play()
            while audio.playing:
                pass
        self._speaker_enable.value = False


cpx = Express() # pylint: disable=invalid-name
"""Object that is automatically created on import.

   To use, simply import it from the module:

   .. code-block:: python

     from adafruit_circuitplayground.express import cpx
"""

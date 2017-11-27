import adafruit_lis3dh
import adafruit_thermistor
import analogio
import array
import audioio
import board
import busio
import digitalio
import math
import neopixel
import time
import touchio


class Photocell:
    def __init__(self, pin):
        self._photocell = analogio.AnalogIn(pin)

    # TODO(tannewt): Calibrate this against another calibrated sensor.
    @property
    def value(self):
        return self._photocell.value * 330 // (2 ** 16)

class Express:
    """Represents a single CircuitPlayground Express. Do not use more than one at
       a time."""
    def __init__(self):
        # Only create the circuit module member when we're aren't being imported by Sphinx
        if "__module__" in dir(digitalio.DigitalInOut) and digitalio.DigitalInOut.__module__ == "sphinx.ext.autodoc":
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
        self.sample = None
        self.sine_wave = None

        # Define touch:
        self._touch_A1 = None
        self._touch_A2 = None
        self._touch_A3 = None
        self._touch_A4 = None
        self._touch_A5 = None
        self._touch_A6 = None
        self._touch_A7 = None

        # Define acceleration:
        self._i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
        self._lis3dh = adafruit_lis3dh.LIS3DH_I2C(self._i2c, address=0x19)
        self._lis3dh.range = adafruit_lis3dh.RANGE_8_G
        self._lis3dh._write_register_byte(adafruit_lis3dh.REG_CTRL5, 0b01001000)
        self._lis3dh._write_register_byte(0x2E, 0b10000000)

    @property
    def acceleration(self):
        """Obtain data from the x, y and z axes.

        .. image :: /_static/accelerometer.jpg
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

    @property
    def shake(self):
        """Detect when device is shaken.

        .. image :: /_static/accelerometer.jpg
          :alt: Accelerometer

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if shake():
              print("Shake detected!")

        The `shake_threshold` default is 30. Decreasing this number increases
        shake sensitivity, i.e. the code will return a shake detected more
        easily with a lower `shake_threshold`. Increasing it causes the opposite.
        `shake_threshold` requires a minimum value of 10 - 10 is the value when
        the board is not moving, therefore anything less than 10 will
        erroneously report a constant shake detected.

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if shake(shake_threshold=20):
              print("Shake detected more easily than before!")
        """
        return self._lis3dh.shake


    @property
    def touch_A1(self):
        """Detect touch on capacitive touch pad A1.

        .. image :: /_static/capacitive_touch_pad_A1.jpg
          :alt: Capacitive touch pad A1

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if cpx.touch_A1:
                  print('Touched pad A1')
        """
        if self._touch_A1 is None:
            self._touch_A1 = touchio.TouchIn(board.A1)
        return self._touch_A1.value

    @property
    def touch_A2(self):
        """Detect touch on capacitive touch pad A2.

        .. image :: /_static/capacitive_touch_pad_A2.jpg
          :alt: Capacitive touch pad A2

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if cpx.touch_A2:
                  print('Touched pad A2')
        """
        if self._touch_A2 is None:
            self._touch_A2 = touchio.TouchIn(board.A2)
        return self._touch_A2.value

    @property
    def touch_A3(self):
        """Detect touch on capacitive touch pad A3.

        .. image :: /_static/capacitive_touch_pad_A3.jpg
          :alt: Capacitive touch pad A3

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if cpx.touch_A3:
                  print('Touched pad A3')
        """
        if self._touch_A3 is None:
            self._touch_A3 = touchio.TouchIn(board.A3)
        return self._touch_A3.value

    @property
    def touch_A4(self):
        """Detect touch on capacitive touch pad A4.

        .. image :: /_static/capacitive_touch_pad_A4.jpg
          :alt: Capacitive touch pad A4

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if cpx.touch_A4:
                  print('Touched pad A4')
        """
        if self._touch_A4 is None:
            self._touch_A4 = touchio.TouchIn(board.A4)
        return self._touch_A4.value

    @property
    def touch_A5(self):
        """Detect touch on capacitive touch pad A5.

        .. image :: /_static/capacitive_touch_pad_A5.jpg
          :alt: Capacitive touch pad A5

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if cpx.touch_A5:
                  print('Touched pad A5')
        """
        if self._touch_A5 is None:
            self._touch_A5 = touchio.TouchIn(board.A5)
        return self._touch_A5.value

    @property
    def touch_A6(self):
        """Detect touch on capacitive touch pad A6.

        .. image :: /_static/capacitive_touch_pad_A6.jpg
          :alt: Capacitive touch pad A6

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if cpx.touch_A6:
                  print('Touched pad A6')
        """
        if self._touch_A6 is None:
            self._touch_A6 = touchio.TouchIn(board.A6)
        return self._touch_A6.value

    @property
    def touch_A7(self):
        """Detect touch on capacitive touch pad A7.

        .. image :: /_static/capacitive_touch_pad_A7.jpg
          :alt: Capacitive touch pad A7

        .. code-block:: python

          from adafruit_circuitplayground.express import cpx

          while True:
              if cpx.touch_A7:
                  print('Touched pad A7')
        """
        if self._touch_A7 is None:
            self._touch_A7 = touchio.TouchIn(board.A7)
        return self._touch_A7.value

    @property
    def pixels(self):
        """Sequence like object representing the ten NeoPixels around the outside
        of the CircuitPlayground. Each pixel is at a certain index in the sequence
        as labeled below. Colors can be RGB hex like 0x110000 for red where each
        two digits are a color (0xRRGGBB) or a tuple like (17, 0, 0) where (R, G, B).
        Set the global brightness using any number from 0 to 1 to represent a
        percentage, i.e. 0.3 sets global brightness to 30%.

        See `neopixel.NeoPixel` for more info.

        .. image :: /_static/neopixel_numbering.jpg
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

            .. image :: /_static/button_a.jpg
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

            .. image :: /_static/button_b.jpg
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

          .. image :: ../_static/slide_switch.jpg
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

            .. image :: /_static/thermistor.jpg
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

           .. image :: /_static/light_sensor.jpg
             :alt: Light sensor

           Try covering the sensor next to the eye to see it change.

           .. code-block:: python

             from adafruit_circuitplayground.express import cpx
             import time

             while True:
                 print("Lux:", cpx.light)
                 time.sleep(1)
        """
        return self._light.value

    @property
    def red_led(self):
        """The red led next to the USB plug marked D13.

           .. image :: /_static/red_led.jpg
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
        TONE_VOLUME = (2 ** 15) - 1
        shift = 2 ** 15
        for i in range(length):
            yield int(TONE_VOLUME * math.sin(2*math.pi*(i / length)) + shift)

    def _generate_sample(self):
        if self.sample is not None:
            return
        length = 100
        self.sine_wave = array.array("H", Express._sine_sample(length))
        self.sample = audioio.AudioOut(board.SPEAKER, self.sine_wave)

    def play_tone(self, frequency, duration):
        """ Produce a tone using the speaker. Try changing frequency to change
        the pitch of the tone.

        :param int frequency: The frequency of the tone in Hz
        :param float duration: The duration of the tone in seconds

        .. image :: /_static/speaker.jpg
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

        .. image :: /_static/speaker.jpg
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
        self.sample.frequency = int(len(self.sine_wave) * frequency)
        if not self.sample.playing:
            self.sample.play(loop=True)

    def stop_tone(self):
        """ Use with start_tone to stop the tone produced.

        .. image :: /_static/speaker.jpg
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
        if self.sample is not None and self.sample.playing:
            self.sample.stop()
        self._speaker_enable.value = False

    def play_file(self, file_name):
        """ Play a .wav file using the onboard speaker.

        :param file_name: The name of your .wav file in quotation marks including .wav

        .. image :: /_static/speaker.jpg
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
        self.a = audioio.AudioOut(board.SPEAKER, open(file_name, "rb"))

        self.a.play()
        while self.a.playing:
            pass
        self._speaker_enable.value = False


cpx = Express()
"""Object that is automatically created on import.

   To use, simply import it from the module:

   .. code-block:: python

     from adafruit_circuitplayground.express import cpx
"""

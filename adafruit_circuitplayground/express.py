import adafruit_thermistor
import analogio
import array
import audioio
import board
import digitalio
import math
import neopixel
import time


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
        self.pixels = neopixel.NeoPixel(board.NEOPIXEL, 10)
        """Sequence like object representing the ten NeoPixels around the outside
        of the CircuitPlayground. Each pixel is at a certain index in the sequence
        as labeled below. Colors can be RGB hex like 0x110000 for red where each
        two digits are a color (0xRRGGBB) or a tuple like (17, 0, 0) where (R, G, B).

        See `neopixel.NeoPixel` for more info.

        .. image :: /_static/neopixel_numbering.jpg
            :alt: NeoPixel order diagram

        Here is an example that sets the first pixel green and the second red.

        .. code-block:: python

          from adafruit_circuitplayground.express import circuit

          circuit.pixels[0] = 0x000300
          circuit.pixels[9] = 0x030000

          # Wait forever. CTRL-C to quit.
          while True:
              pass
        """

        # Define sensors:
        self._temp = adafruit_thermistor.Thermistor(board.TEMPERATURE, 10000, 10000, 25, 3950)
        self._light = Photocell(board.LIGHT)

        # Define audio:
        self.speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
        self.speaker_enable.switch_to_output(value=False)

    @property
    def button_a(self):
        """``True`` when Button A is pressed. ``False`` if not.

            .. image :: /_static/button_a.jpg
              :alt: NeoPixel order diagram

            .. code-block:: python

              from adafruit_circuitplayground.express import circuit

              while True:
                  if circuit.button_a:
                      print("Button A pressed!")
        """
        return self._a.value

    @property
    def button_b(self):
        """``True`` when Button B is pressed. ``False`` if not.

            .. image :: /_static/button_b.jpg
              :alt: NeoPixel order diagram

            .. code-block:: python

              from adafruit_circuitplayground.express import circuit

              while True:
                  if circuit.button_b:
                      print("Button B pressed!")
        """
        return self._b.value

    @property
    def switch(self):
        """
          ``True`` when the switch is to the left next to the music notes.
          ``False`` when it is to the right towards the ear.

          .. image :: ../_static/slide_switch.jpg
            :alt: NeoPixel order diagram

          .. code-block:: python

            from adafruit_circuitplayground.express import circuit
            import time

            while True:
                print("Slide switch:", circuit.switch)
                time.sleep(1)
            """
        return self._switch.value

    @property
    def temperature(self):
        """The temperature of the CircuitPlayground in Celsius.

            .. image :: /_static/thermistor.jpg
              :alt: NeoPixel order diagram

           Converting this to Farenheit is easy!

            .. code-block:: python

              from adafruit_circuitplayground.express import circuit
              import time

              while True:
                  temperature_c = circuit.temperature
                  temperature_f = temperature_c * 1.8 + 32
                  print("Temperature celsius:", temperature_c)
                  print("Temperature farenheit:", temperature_f)
                  time.sleep(1)
        """
        return self._temp.temperature

    @property
    def light(self):
        """The brightness of the CircuitPlayground in approximate Lux.

           .. image :: /_static/light_sensor.jpg
             :alt: NeoPixel order diagram

           Try covering the sensor next to the eye to see it change.

           .. code-block:: python

             from adafruit_circuitplayground.express import circuit
             import time

             while True:
                 print("Lux:", circuit.light)
                 time.sleep(1)
        """
        return self._light.value

    @property
    def red_led(self):
        """The red led next to the USB plug marked D13.

           .. image :: /_static/red_led.jpg
             :alt: NeoPixel order diagram

           .. code-block:: python

             from adafruit_circuitplayground.express import circuit
             import time

             while True:
                 circuit.red_led = True
                 time.sleep(1)
                 circuit.red_led = False
                 time.sleep(1)
        """
        return self._led.value

    @red_led.setter
    def red_led(self, value):
        self._led.value = value

    def sine_sample(length):
        TONE_VOLUME = (2 ** 15) - 1
        shift = 2 ** 15
        for i in range(length):
            yield int(TONE_VOLUME * math.sin(2*math.pi*(i / length)) + shift)

    length = 100  # Amount of samples in the sine wave.
    sine_wave = array.array("H", sine_sample(length))

    # Initialize the audio output to play the generated sine wave.
    sample = audioio.AudioOut(board.SPEAKER, sine_wave)

    def play_tone(self, frequency, duration):
        """ Produce a tone using the speaker. Try changing frequency to change
        the pitch of the tone.

        :param int frequency: The frequency of the tone in Hz
        :param float duration: The duration of the tone in seconds

        .. image :: /_static/speaker.jpg

        .. code-block:: python

            from adafruit_circuitplayground.express import circuit

            circuit.play_tone(440, 1)
        """

        self.speaker_enable.value = True

        # Play a tone of the specified frequency (hz).
        self.sample.frequency = int(len(self.sine_wave) * frequency)
        if not self.sample.playing:
            self.sample.play(loop=True)
        time.sleep(duration)
        if self.sample.playing:
            self.sample.stop()
        self.speaker_enable.value = False

    def start_tone(self, frequency):
        """ Produce a tone using the speaker. Try changing frequency to change
        the pitch of the tone.

        :param int frequency: The frequency of the tone in Hz

        .. image :: /_static/speaker.jpg

        .. code-block:: python

             from adafruit_circuitplayground.express import circuit

             while True:
                 if circuit.button_a:
                     circuit.start_tone(262)
                 elif circuit.button_b:
                     circuit.start_tone(294)
                 else:
                     circuit.stop_tone()
        """
        self.speaker_enable.value = True
        # Start playing a tone of the specified frequency (hz).
        self.sample.frequency = int(len(self.sine_wave) * frequency)
        if not self.sample.playing:
            self.sample.play(loop=True)

    def stop_tone(self):
        """ Use with start_tone to stop the tone produced.

        .. image :: /_static/speaker.jpg

        .. code-block:: python

             from adafruit_circuitplayground.express import circuit

             while True:
                 if circuit.button_a:
                     circuit.start_tone(262)
                 elif circuit.button_b:
                     circuit.start_tone(294)
                 else:
                     circuit.stop_tone()
        """
        # Stop playing any tones.
        if self.sample.playing:
            self.sample.stop()
        self.speaker_enable.value = False


circuit = Express()
"""Object that is automatically created on import.

   To use, simply import it from the module:

   .. code-block:: python

     from adafruit_circuitplayground.express import circuit
"""

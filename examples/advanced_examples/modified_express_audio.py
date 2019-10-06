import array
import math
import time
import board
import digitalio
import audioio
try:
    import audiocore
except ImportError:
    audiocore = audioio


class ModifiedExpressAudio:
    'An enhanced set of audio features, perhaps to augment those in the current Adafruit library'
    def __init__(self):
        self._highest_supported_frequency = 20_000
        self._speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
        self._speaker_enable.switch_to_output(value=False)
        self._speaker_enable.value = False
        self._volume = 1.0
        self._audio_out = audioio.AudioOut(board.SPEAKER)
        self._generators = (
            (ModifiedExpressAudio._sine_waveform, 100),
            (ModifiedExpressAudio._square_waveform, 2),
            (ModifiedExpressAudio._triangle_waveform, 50)
        )
        self._waveform_index = 0
        self._create_waveform()

    def _create_waveform(self):
        generator, length = self._generators[self._waveform_index]
        self._audiocore_raw_sample = audiocore.RawSample(array.array("H", generator(length, self._volume)))

    @staticmethod
    def _sine_waveform(length, amplitude=1.0):
        max_amplitude = 2 ** 15 - 1
        angle = 0.0
        angle_change_per_sample = 2 * math.pi / length
        for _ in range(length):
            yield int(amplitude * max_amplitude * (math.sin(angle) + 1))
            angle += angle_change_per_sample

    @staticmethod
    def _square_waveform(length, amplitude=1.0):
        assert length == 2
        loudest_audible_amplitude = 0.5
        max_amplitude = 2 ** 16 - 1
        return 0, int(loudest_audible_amplitude * amplitude * max_amplitude)

    @staticmethod
    def _triangle_waveform(length, amplitude=1.0):
        max_amplitude = 2 ** 16 - 1
        top = int(amplitude * max_amplitude)
        dx = 2 / length
        x = -1
        while x < 1:
            yield round(top * (-abs(x) + 1))
            x += dx

    def set_volume(self, volume):
        self._volume = volume
        self._create_waveform()

    def start_tone(self, frequency):
        if frequency <= self._highest_supported_frequency and self._volume > 0:
            self._audiocore_raw_sample.sample_rate = int(self._generators[self._waveform_index][1] * frequency)
            self._speaker_enable.value = False
            self._audio_out.play(self._audiocore_raw_sample, loop=True)
            self._speaker_enable.value = True

    def stop_tone(self):
        if self._audio_out is not None and self._audio_out.playing:
            self._audio_out.stop()

    def clear_audio(self):
        self.stop_tone()
        if self._audio_out is not None:
            self._audio_out.deinit()
            self._audio_out = None

    def select_waveform(self, waveform_index):
        self._waveform_index = waveform_index
        self._create_waveform()


def run_demos():
    C1_FREQ = 32.70319566257483

    def play_midi(note):
        if 24 <= note <= 108:
            semitones_above_c1 = note - 24
            freq = C1_FREQ * 2 ** (semitones_above_c1 / 12)
            cpx.start_tone(freq)

    def arpeggio():
        HIGHEST_OCTAVE = 4
        for octave in range(HIGHEST_OCTAVE + 1):
            for note in (24, 28, 31):
                play_midi(octave * 12 + note)
                time.sleep(.2)
        play_midi((HIGHEST_OCTAVE + 1) * 12 + 24)
        time.sleep(0.3)

    def scale():
        STARTING_NOTE_FREQ = C1_FREQ
        STARTING_OCTAVE = 1
        NOTE_SPACING_SECONDS = 0.2
        KEYS = 'C Db D Eb E F Gb G Ab A Bb B'.split(' ')  # Using b to represent ♭

        next_note_play_time = time.monotonic()
        for octave_index in range(5):
            for semitone_index in range(12):
                semitones_above_start = octave_index * 12 + semitone_index
                freq = STARTING_NOTE_FREQ * 2 ** (semitones_above_start / 12)
                print(KEYS[semitone_index % 12] + str(octave_index + STARTING_OCTAVE), '\t', freq)
                next_note_play_time += NOTE_SPACING_SECONDS
                cpx.start_tone(freq)
                sleep_time = max(0.0, next_note_play_time - time.monotonic())
                time.sleep(sleep_time)
                # Not calling stop_tone()

    def changing_volume():
        for i in range(11):
            v = i / 10
            print(v)
            cpx.set_volume(v)
            play_midi(60)
            time.sleep(1)

    cpx = ModifiedExpressAudio()
    functions = (
        ('Arpeggio', arpeggio),
        ('Scale', scale),
        ('Changing Volume', changing_volume),
    )
    cpx.set_volume(1.0)
    waves = 'Sine Square Triangle'.split()
    for fn, f in functions:
        print(fn)
        for waveform_index, name in enumerate(waves):
            print(name)
            cpx.select_waveform(waveform_index)
            f()
    cpx.clear_audio()


if __name__ == '__main__':
    run_demos()

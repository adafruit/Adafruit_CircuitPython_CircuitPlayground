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
    def __init__(self):
        self._max_sample_rate = 350_000
        self._highest_supported_frequency = 20_000
        self._normal_sample_length = 300
        self._samples_change_frequency = self._max_sample_rate / self._normal_sample_length
        self._sample_lengths = (
            self._normal_sample_length,
            self._max_sample_rate / self._highest_supported_frequency)
        self._speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
        self._speaker_enable.switch_to_output(value=False)
        self._speaker_enable.value = True
        self._raw_samples = tuple(self._generate_samples())
        self._audio_out = audioio.AudioOut(board.SPEAKER)

    @staticmethod
    def _sine_waveform(length, amplitude=1):
        max_amplitude = 2 ** 15 - 1
        angle = 0.0
        angle_change_per_sample = 2 * math.pi / length
        for _ in range(length):
            yield int(amplitude * max_amplitude * (math.sin(angle) + 1))
            angle += angle_change_per_sample

    def _generate_samples(self):
        return [audiocore.RawSample(array.array("H", ModifiedExpressAudio._sine_waveform(length)))
                for length in self._sample_lengths]

    def start_tone(self, frequency):
        if frequency <= self._highest_supported_frequency:
            # Start playing a tone of the specified frequency (hz).
            samples_index = 0 if frequency < self._samples_change_frequency else 1
            length = self._sample_lengths[samples_index]
            sample_to_play = self._raw_samples[samples_index]
            sample_to_play.sample_rate = int(length * frequency)
            if not self._audio_out.playing:
                self._audio_out.play(sample_to_play, loop=True)

    def stop_tone(self):
        if self._audio_out is not None and self._audio_out.playing:
            self._audio_out.stop()

    def clear_audio(self):
        self.stop_tone()
        if self._audio_out is not None:
            self._audio_out.deinit()
            self._audio_out = None


cpx = ModifiedExpressAudio()

STARTING_NOTE_FREQ = 32.71  # C1
STARTING_OCTAVE = 1
NOTE_SPACING_SECONDS = 0.2
KEYS = 'C Db D Eb E F Gb G Ab A Bb B'.split(' ')  # Using b to represent ♭


for reset in (False, ):
    next_note_play_time = time.monotonic()
    for octave_index in range(9):
        for semitone_index in range(12):
            semitones_above_start = octave_index * 12 + semitone_index
            freq = STARTING_NOTE_FREQ * 2 ** (semitones_above_start / 12)
            print(KEYS[semitone_index % 12] + str(octave_index + STARTING_OCTAVE), '\t', freq)
            cpx.start_tone(freq)
            next_note_play_time += NOTE_SPACING_SECONDS
            time.sleep(next_note_play_time - time.monotonic())
            cpx.stop_tone()
    time.sleep(0.5)
cpx.clear_audio()

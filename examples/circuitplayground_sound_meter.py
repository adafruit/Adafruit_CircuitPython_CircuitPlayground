"""This example uses the sound sensor, located next to the picture of the ear on your board, to
light up the NeoPixels as a sound meter. Try talking to your Circuit Playground or clapping, etc,
to see the NeoPixels light up!"""
import array
import math
import audiobusio
import board
from adafruit_circuitplayground import cp


def constrain(value, floor, ceiling):
    return max(floor, min(value, ceiling))


def log_scale(input_value, input_min, input_max, output_min, output_max):
    normalized_input_value = (input_value - input_min) / (input_max - input_min)
    return output_min + math.pow(normalized_input_value, 0.630957) * (
        output_max - output_min
    )


def normalized_rms(values):
    minbuf = int(sum(values) / len(values))
    return math.sqrt(
        sum(float(sample - minbuf) * (sample - minbuf) for sample in values)
        / len(values)
    )


# Check to see if the board type is a Circuit Playground Express, and, if so, run the following:
if cp.circuit_playground_is_type("Express"):
    mic = audiobusio.PDMIn(
        board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=16000, bit_depth=16
    )

    samples = array.array("H", [0] * 160)
    mic.record(samples, len(samples))
    input_floor = normalized_rms(samples) + 10
# If it is not, run the following:
else:
    input_floor = cp.sound_level + 10

# Lower number means more sensitive - more LEDs will light up with less sound.
sensitivity = 500
input_ceiling = input_floor + sensitivity

peak = 0
while True:
    if cp.circuit_playground_is_type("Express"):  # Circuit Playground Express
        mic.record(samples, len(samples))
        magnitude = normalized_rms(samples)
    else:  # Not CPX
        magnitude = cp.sound_level

    print((magnitude,))  # Printed as a tuple for the Mu plotter.

    c = log_scale(
        constrain(magnitude, input_floor, input_ceiling),
        input_floor,
        input_ceiling,
        0,
        10,
    )

    cp.pixels.fill((0, 0, 0))
    for i in range(10):
        if i < c:
            cp.pixels[i] = (i * (255 // 10), 50, 0)
        if c >= peak:
            peak = min(c, 10 - 1)
        elif peak > 0:
            peak = peak - 1
        if peak > 0:
            cp.pixels[int(peak)] = (80, 0, 255)
    cp.pixels.show()

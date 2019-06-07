"""THIS EXAMPLE REQUIRES A SEPARATE LIBRARY BE LOADED ONTO YOUR CIRCUITPY DRIVE.
This example requires the adafruit_irremote.mpy library.

This example uses the IR transmitter found near the center of the board. Works with another CPX
running the cpx_ir_receive.py example. Press the buttons to light up the NeoPixels on the RECEIVING
CPX!"""
import time
import pulseio
import board
import adafruit_irremote
from adafruit_circuitplayground.express import cpx

# Create a 'pulseio' output, to send infrared signals from the IR transmitter
pwm = pulseio.PWMOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
pulseout = pulseio.PulseOut(pwm)
# Create an encoder that will take numbers and turn them into NEC IR pulses
encoder = adafruit_irremote.GenericTransmit(header=[9500, 4500], one=[550, 550],
                                            zero=[550, 1700], trail=0)

while True:
    if cpx.button_a:
        print("Button A pressed! \n")
        cpx.red_led = True
        encoder.transmit(pulseout, [66, 84, 78, 65])
        cpx.red_led = False
        # wait so the receiver can get the full message
        time.sleep(0.2)
    if cpx.button_b:
        print("Button B pressed! \n")
        cpx.red_led = True
        encoder.transmit(pulseout, [66, 84, 78, 64])
        cpx.red_led = False
        time.sleep(0.2)

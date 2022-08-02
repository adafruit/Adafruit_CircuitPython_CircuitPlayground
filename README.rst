
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-circuitplayground/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/circuitplayground/en/latest/
    :alt: Documentation Status

.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_CircuitPlayground/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_CircuitPlayground/actions/
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

This high level library provides objects that represent Circuit Playground Express and Bluefruit hardware.

.. image :: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_CircuitPlayground/main/docs/_static/circuit_playground_express_small.jpg
    :target: https://adafruit.com/product/3333
    :alt: Circuit Playground Express

.. image :: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_CircuitPlayground/main/docs/_static/circuit_playground_bluefruit_small.jpg
    :target: https://adafruit.com/product/4333
    :alt: Circuit Playground Bluefruit

Installation
=============
For Circuit Playground Express, simply install CircuitPython to use this library - the library itself and
all of its dependencies are built into CircuitPython for Circuit Playground Express.

For Circuit Playground Bluefruit, you must install this library and all of its dependencies. Please download
`the latest Adafruit CircuitPython library bundle <https://circuitpython.org/libraries>`_. Open the resulting
zip file, open the lib folder within, and copy the following folders and files to the lib folder on your
CIRCUITPY drive:

* adafruit_bus_device/
* adafruit_circuitplayground/
* adafruit_lis3dh.mpy
* adafruit_thermistor.mpy
* neopixel.mpy

Usage Example
=============
Using this library is super simple. Simply import the ``cp`` variable from the module and then use it.

.. code-block :: python

    from adafruit_circuitplayground import cp

    while True:
        if cp.button_a:
            print("Temperature:", cp.temperature)
        cp.red_led = cp.button_b

To learn more about all the features of this library, check out the
`CircuitPython Made Easy on Circuit Playground Express and Bluefruit guide <https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express>`_
on the Adafruit Learn System.

Circuit Playground Library Details
==================================

For a detailed explanation of how the Circuit Playground library functions, see
`The Technical Side page <https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/the-technical-side>`_
of the CircuitPython Made Easy on Circuit Playground Express and Bluefruit guide.

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/circuitplayground/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_CircuitPlayground/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

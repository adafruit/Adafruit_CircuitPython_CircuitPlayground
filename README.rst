
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-circuitplayground/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/circuitplayground/en/latest/
    :alt: Documentation Status

.. image :: https://badges.gitter.im/adafruit/circuitpython.svg
    :target: https://gitter.im/adafruit/circuitpython?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
    :alt: Gitter

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

This high level library provides objects that represent CircuitPlayground hardware.

.. image :: /_static/circuitplayground_express.jpg
    :target: https://adafruit.com/product/3333
    :alt: CircuitPlayground Express

Installation
=============
This driver depends on many other libraries! Please install it by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============
Using it is super simple. Simply import the `circuit` variable from the module
and then use it.

.. code-block :: python

    from adafruit_circuitplayground.express import circuit

    while True:
        if circuit.button_a:
            print("Temperature:", circuit.temperature)
        circuit.red_led = circuit.button_b

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_CircuitPlayground/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

API Reference
=============

.. toctree::
    :maxdepth: 2

    adafruit_circuitplayground/index

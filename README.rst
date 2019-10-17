
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-circuitplayground/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/circuitplayground/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://travis-ci.com/adafruit/Adafruit_CircuitPython_CircuitPlayground.svg?branch=master
    :target: https://travis-ci.com/adafruit/Adafruit_CircuitPython_CircuitPlayground
    :alt: Build Status

This high level library provides objects that represent CircuitPlayground hardware.

.. image :: ../docs/_static/circuitplayground_express.jpg
    :target: https://adafruit.com/product/3333
    :alt: CircuitPlayground Express

Installation
=============
This driver depends on many other libraries! Please install it by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============
Using it is super simple. Simply import the `cpx` variable from the module
and then use it.

.. code-block :: python

    from adafruit_circuitplayground.express import cpx

    while True:
        if cpx.button_a:
            print("Temperature:", cpx.temperature)
        cpx.red_led = cpx.button_b

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_CircuitPlayground/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

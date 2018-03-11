
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-circuitplayground/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/circuitplayground/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://travis-ci.org/adafruit/Adafruit_CircuitPython_CircuitPlayground.svg?branch=master
    :target: https://travis-ci.org/adafruit/Adafruit_CircuitPython_CircuitPlayground
    :alt: Build Status

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

Building locally
================

To build this library locally you'll need to install the
`circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install circuitpython-build-tools

Once installed, make sure you are in the virtual environment:

.. code-block:: shell

    source .env/bin/activate

Then run the build:

.. code-block:: shell

    circuitpython-build-bundles --filename_prefix adafruit-circuitpython-circuitplayground --library_location .

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.


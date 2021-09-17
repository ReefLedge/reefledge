"""A powerful API designed for the consumption of ML/TS model outputs.

**reefledge** is a Python package which provides a fast, simple and
powerful API designed to facilitate the consumption of cutting edge
density forecasting model outputs. These are generated from market data
on liquid instruments and are the result of demanding estimation and
simulation processes on a high-performance cloud cluster. Data is
produced for a wide range of reference dates and asset classes, yielding
forecasts for a variety of time horizons and metrics.

"""

import os

from .setup import setup as _setup, THIS_DIRECTORY_NAME

if 'reefledge' not in os.listdir(THIS_DIRECTORY_NAME):
    _setup()

from .reefledge import *

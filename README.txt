A powerful API designed for Quantitative Finance practitioners.

**reefledge** is a Python package which provides a fast, simple and
powerful API designed to facilitate the consumption of cutting edge
density forecasting model outputs. These are generated from market data
on liquid financial instruments and are the result of demanding
estimation and simulation processes on a high-performance cloud cluster.
Data is produced for a wide range of reference dates and asset classes,
yielding forecasts for a variety of time horizons and metrics.

Main Features
-------------
Here are just a few of the things that make reefledge special:

  - Intuitive object oriented interface.
  - Tight integration with Microsoft Excel.
  - Fast and robust Cython codebase.
  - Multithreading capabilities to overcome I/O overhead.
  - Efficient and highly available back end, featuring global load
    balancing, optimized connection pooling and extensive database table
    partitioning, besides an intelligent use of indexes to speed up SQL
    queries.

Basic Usage
-----------
>>> import reefledge as rl
>>> rl.login(user='stokes', api_key='secret')
>>> df = rl.get_df(target='NYSE', metric='STD', tickers=['GS', 'IBM'])


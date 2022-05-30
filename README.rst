A powerful API designed for Quantitative Finance practitioners.

**reefledge** is a Python/Cython package which provides a fast, simple
and powerful API designed to simplify the consumption of cutting-edge
density forecasting model outputs. These are generated from market data
on liquid financial instruments and are the result of demanding
estimation and simulation processes on a high-performance cloud cluster.
Data is produced for a wide range of reference dates and asset classes,
yielding forecasts for a variety of time horizons and metrics.

Main Features
-------------
Here are just a few of the things that make `reefledge` special:

  * Intuitive object oriented interface.
  * Type checking at runtime of all public functions/methods.
  * Tight integration with Microsoft Excel.
  * Fast and robust Cython codebase.
  * Multithreading capabilities to overcome I/O overheads.
  * Smart and 'respectful' (in terms of RAM usage) caching.
  * Efficient and highly available back end, featuring global load
    balancing, optimized connection pooling and extensive database table
    partitioning, besides an intelligent use of indexes to speed up SQL
    queries (not to mention full use of SSD disks).

Installation
------------
The easiest way to install `reefledge` and get updates is via `pip`:

    $ pip install reefledge

On Linux, the shell command above should return an error due to the
`xlwings` module dependency, which is only relevant on the Windows
platform. You can safely ignore it by preceding the installation command
with:

    $ export INSTALL_ON_LINUX=1

Basic Usage
-----------
>>> import reefledge as rl
>>> rl.login(user_name='foobar', api_key='secret')
>>> df = rl.get_point_forecasts_df( # Returns a pandas DataFrame instance.
        target='USA',
        metric='STD',
        tickers=['GS', 'IBM'])

Generic Error Catching
----------------------
>>> try:
        rl.get_point_forecasts_df(target='USA', metric='STD', tickers='GS')
    except rl.Error as exc:
        print(exc)

Basic Configuration
-------------------
>>> rl.APIConfig.allow_caching
True
>>> rl.APIConfig.allow_tickers_sorting
False
>>> rl.APIConfig.allow_caching = False # Disable caching.

Notes
-----
Further examples assume that `reefledge` has been imported as `rl`:

    >>> import reefledge as rl


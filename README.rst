A powerful API designed for Quantitative Finance practitioners.

**reefledge** is a Python package which provides a fast, simple and
powerful API designed to simplify the retrieval of price/return density
forecasts (on a ticker-by-ticker basis) generated from cutting-edge Time
Series Analysis models.
Our algorithms consume market data on liquid financial assets and
require demanding estimation and simulation steps, both accomplished on
a high-performance cloud cluster.
Forecasts are produced for a wide range of reference dates and
investment horizons, covering multiple metrics for a variety of asset
classes.

Delivery Frequency
------------------
Forecasts are generated on a daily basis.

Data Frequency
--------------
All models consume daily-frequency data.

Data Reporting Lag
------------------
Usually, every ticker which passes our demanding filtering criteria
requires around one minute of processing on a Google Cloud C2 compute
engine with a single vCPU and four gigabytes of RAM.
Our cluster boots as soon as the latest market data is available
and, at the time of writing, scales up to 120 vCPUs.

Data History
------------
In general, expect forecasts to be readily accessible for reference
dates going back at least four years.

Data Coverage
-------------
Currently, only the 'NYSE' target is in production. Nonetheless,
multiple targets - such as 'NASDAQ' - have already been extensively
tested and will be released soon.

Main Features
-------------
Here are just a few of the things that make `reefledge` special:

  * Intuitive object oriented interface.
  * Type checking at runtime of all public functions/methods.
  * Seamless integration with Microsoft Excel.
  * Fast and robust cythonized codebase.
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
        target='NYSE',
        metric='STD',
        tickers=['GS', 'IBM'])

Advanced Usage
--------------
Advanced users should refer to the following functions/classes:

  * `reefledge.reefledge.front_end.get.get`
    for retrieving and parsing data into a
    `reefledge.reefledge.back_end.data_wrapper.data_wrapper.DataWrapper` instance.
  * `reefledge.reefledge.front_end.get_point_forecasts_df.get_point_forecasts_df`
    for retrieving and parsing data into a
    `pandas.core.frame.DataFrame` instance.
  * `reefledge.reefledge.front_end.list_tickers.list_tickers`
    for querying all available tickers associated with a particular
    target.
  * `reefledge.reefledge.back_end.api_config.api_config.APIConfig`
    for configuring the API.

Generic Error Catching
----------------------
>>> try:
        rl.get_point_forecasts_df(target='NYSE', metric='STD', tickers='GS')
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


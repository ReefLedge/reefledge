from setuptools import setup

setup(
    name='reefledge',
    packages=['reefledge'],
    include_package_data=True,
    version='1.6.3',
    description="A powerful API designed for Quantitative Finance practitioners.", # DO NOT use single quotes!
    long_description="**reefledge** is a Python package which provides a fast, simple and\npowerful API designed to simplify the retrieval of price/return density\nforecasts (on a ticker-by-ticker basis) generated from cutting-edge Time\nSeries Analysis models.\nOur algorithms consume market data on liquid financial assets and\nrequire demanding estimation and simulation steps, both accomplished on\na high-performance cloud cluster.\nForecasts are produced for a wide range of reference dates and\ninvestment horizons, covering multiple metrics for a variety of asset\nclasses.\n\nDelivery Frequency\n------------------\nForecasts are generated on a daily basis.\n\nData Frequency\n--------------\nAll models consume daily-frequency data.\n\nData Reporting Lag\n------------------\nUsually, every ticker which passes our demanding filtering criteria\nrequires around one minute of processing on a Google Cloud C2 compute\nengine with a single vCPU and four gigabytes of RAM.\nOur cluster boots as soon as the latest market data is available\nand, at the time of writing, scales up to 120 vCPUs.\n\nData History\n------------\nIn general, expect forecasts to be readily accessible for reference\ndates going back at least four years.\n\nData Coverage\n-------------\nCurrently, only the 'NYSE' target is in production. Nonetheless,\nmultiple targets - such as 'NASDAQ' - have already been extensively\ntested and will be released soon.\n\nMain Features\n-------------\nHere are just a few of the things that make `reefledge` special:\n\n  * Intuitive object oriented interface.\n  * Type checking at runtime of all public functions/methods.\n  * Seamless integration with Microsoft Excel.\n  * Fast and robust cythonized codebase.\n  * Multithreading capabilities to overcome I/O overheads.\n  * Smart and 'respectful' (in terms of RAM usage) caching.\n  * Efficient and highly available back end, featuring global load\n    balancing, optimized connection pooling and extensive database table\n    partitioning, besides an intelligent use of indexes to speed up SQL\n    queries (not to mention full use of SSD disks).\n\nInstallation\n------------\nThe easiest way to install `reefledge` and get updates is via `pip`:\n\n    $ pip install reefledge\n\nOn Linux, the shell command above should return an error due to the\n`xlwings` module dependency, which is only relevant on the Windows\nplatform. You can safely ignore it by preceding the installation command\nwith:\n\n    $ export INSTALL_ON_LINUX=1\n\nBasic Usage\n-----------\n>>> import reefledge as rl\n>>> rl.login(user_name='foobar', api_key='secret')\n>>> df = rl.get_point_forecasts_df( # Returns a pandas DataFrame instance.\n        target='NYSE',\n        metric='STD',\n        tickers=['GS', 'IBM'])\n\nAdvanced Usage\n--------------\nAdvanced users should refer to the following functions/classes:\n\n  * `reefledge.reefledge.front_end.get.get`\n    for retrieving and parsing data into a\n    `reefledge.reefledge.back_end.data_wrapper.data_wrapper.DataWrapper` instance.\n  * `reefledge.reefledge.front_end.get_point_forecasts_df.get_point_forecasts_df`\n    for retrieving and parsing data into a\n    `pandas.core.frame.DataFrame` instance.\n  * `reefledge.reefledge.front_end.list_tickers.list_tickers`\n    for querying all available tickers associated with a particular\n    target.\n  * `reefledge.reefledge.back_end.api_config.api_config.APIConfig`\n    for configuring the API.\n\nGeneric Error Catching\n----------------------\n>>> try:\n        rl.get_point_forecasts_df(target='NYSE', metric='STD', tickers='GS')\n    except rl.Error as exc:\n        print(exc)\n\nBasic Configuration\n-------------------\n>>> rl.APIConfig.allow_caching\nTrue\n>>> rl.APIConfig.allow_tickers_sorting\nFalse\n>>> rl.APIConfig.allow_caching = False # Disable caching.\n\nNotes\n-----\nFurther examples assume that `reefledge` has been imported as `rl`:\n\n    >>> import reefledge as rl\n", # DO NOT use single quotes!
    author='ReefLedge',
    author_email='support@reefledge.com',
    url='https://www.reefledge.com/python_package/docs/',
    download_url='https://github.com/Reefledge/reefledge/archive/refs/tags/v1.6.3.tar.gz',
    keywords=['quant', 'quantitative', 'finance', 'forecasting', 'time-series', 'machine learning', 'trading', 'portfolio management', 'risk management'],
    install_requires=['setuptools>=50.3.2,<64.0.0', 'cryptography==38.0.3', 'packaging>=21.3,<22.0', 'requests>=2.27.1,<3.0.0', 'psycopg2>=2.9.3,<2.9.5', 'numpy>=1.22.4,<1.24.0', 'scipy>=1.8.1,<1.10.0', 'pandas>=1.4.2,<1.6.0', 'matplotlib>=3.5.2,<3.7.0', 'openpyxl>=3.0.10,<3.1.0', 'ipython>=7.34.0,<9.0.0', 'ipykernel>=5.5.6,<7.0.0', 'nptyping>=2.2.0,<3.0.0', 'psutil>=5.9.1,<6.0.0', 'python-dateutil>=2.8.2,<3.0.0', 'pdoc3>=0.10.0,<0.11.0', 'pydantic>=1.9.1,<1.10.0', 'backoff>=1.11.1,<3.0.0', 'cachetools>=4.2.4,<6.0.0', 'typing_extensions>=4.4.0,<5.0.0', 'pyqt5', 'xlwings==0.27.10',],
    platforms=['Windows', 'Linux', 'MacOS'],
    python_requires='>=3.8, <3.11',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: MacOS',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Typing :: Typed',
        "License :: OSI Approved :: MIT License",
    ]
)

from typing import Final
from setuptools import setup

LICENSE: Final[str] = 'MIT'

setup(
    name='reefledge',
    packages=['reefledge'],
    include_package_data=True,
    version='1.1.3',
    license=LICENSE,
    description="A powerful API designed for Quantitative Finance practitioners.", # DO NOT use single quotes!
    long_description="**reefledge** is a Python/Cython package which provides a fast, simple\nand powerful API designed to simplify the consumption of cutting edge\ndensity forecasting model outputs. These are generated from market data\non liquid financial instruments and are the result of demanding\nestimation and simulation processes on a high-performance cloud cluster.\nData is produced for a wide range of reference dates and asset classes,\nyielding forecasts for a variety of time horizons and metrics.\n\nMain Features\n-------------\nHere are just a few of the things that make `reefledge` special:\n\n  * Intuitive object oriented interface.\n  * Tight integration with Microsoft Excel.\n  * Fast and robust Cython codebase.\n  * Multithreading capabilities to overcome I/O overheads.\n  * Smart and 'respectful' (in terms of RAM usage) caching.\n  * Efficient and highly available back end, featuring global load\n    balancing, optimized connection pooling and extensive database table\n    partitioning, besides an intelligent use of indexes to speed up SQL\n    queries (not to mention full use of SSD disks).\n\nInstallation\n------------\nThe easiest way to install `reefledge` and get updates is via `pip`:\n\n    $ pip install reefledge\n\nBasic Usage\n-----------\n>>> import reefledge as rl\n>>> rl.login(user='stokes', api_key='secret')\n>>> df = rl.get_df(\n        target='NYSE',\n        metric='STD',\n        tickers=['GS', 'IBM']) # Returns a pandas DataFrame instance.\n\nGeneric Error Catching\n----------------------\n>>> try:\n        rl.get_df(target='NYSE', metric='STD', tickers='GS')\n    except rl.Error as exc:\n        print(exc)\n\nConfiguration\n-------------\n>>> rl.APIConfig.allow_caching\nTrue\n>>> rl.APIConfig.allow_tickers_sorting\nFalse\n>>> rl.APIConfig.allow_caching = False # Disable caching.\n\nNotes\n-----\nFurther examples assume that `reefledge` has been imported as `rl`:\n\n    >>> import reefledge as rl\n", # DO NOT use single quotes!
    author='ReefLedge',
    author_email='duarte.stokes@reefledge.com',
    url='https://reefledge.com',
    download_url='https://github.com/Reefledge/reefledge/archive/refs/tags/v1.1.3-beta.1.tar.gz',
    keywords=['quant', 'finance', 'api', 'forecasting', 'time-series', 'machine learning', 'trading', 'portfolio management', 'risk management'],
    install_requires=['setuptools>=50.3.1', 'cython>=0.29.22', 'requests>=2.25.1', 'twilio>=6.50.1', 'psycopg2>=2.8.6', 'numpy>=1.18.5', 'scipy>=1.5.0', 'pandas>=1.0.5', 'matplotlib>=3.2.2', 'openpyxl>=3.0.5', 'ipython>=7.19.0', 'ipykernel>=5.3.4', 'nptyping>=1.4.0', 'psutil>=5.8.0', 'pdoc3>=0.10.0', 'xlwings>=0.24.9', 'pyqt5',],
    python_requires='>=3.8',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        f"License :: OSI Approved :: {LICENSE} License",
        'Programming Language :: Python :: 3',
    ]
)

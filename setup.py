from typing import Final
from setuptools import setup

LICENSE: Final[str] = 'MIT'

setup(
    name='reefledge',
    packages=['reefledge'],
    include_package_data=True,
    version='1.4.0' + '-alpha.0',
    license=LICENSE,
    description="A powerful API designed for Quantitative Finance practitioners.", # DO NOT use single quotes!
    long_description="**reefledge** is a Python/Cython package which provides a fast, simple\nand powerful API designed to simplify the consumption of cutting-edge\ndensity forecasting model outputs. These are generated from market data\non liquid financial instruments and are the result of demanding\nestimation and simulation processes on a high-performance cloud cluster.\nData is produced for a wide range of reference dates and asset classes,\nyielding forecasts for a variety of time horizons and metrics.\n\nMain Features\n-------------\nHere are just a few of the things that make `reefledge` special:\n\n  * Intuitive object oriented interface.\n  * Type checking at runtime of all public functions/methods.\n  * Tight integration with Microsoft Excel.\n  * Fast and robust Cython codebase.\n  * Multithreading capabilities to overcome I/O overheads.\n  * Smart and 'respectful' (in terms of RAM usage) caching.\n  * Efficient and highly available back end, featuring global load\n    balancing, optimized connection pooling and extensive database table\n    partitioning, besides an intelligent use of indexes to speed up SQL\n    queries (not to mention full use of SSD disks).\n\nInstallation\n------------\nThe easiest way to install `reefledge` and get updates is via `pip`:\n\n    $ pip install reefledge\n\nOn Linux, the shell command above should return an error due to the\n`xlwings` module dependency, which is only relevant on the Windows\nplatform. You can safely ignore it by preceding the installation command\nwith:\n\n    $ export INSTALL_ON_LINUX=1\n\nBasic Usage\n-----------\n>>> import reefledge as rl\n>>> rl.login(user_name='foobar', api_key='secret')\n>>> df = rl.get_point_forecasts_df( # Returns a pandas DataFrame instance.\n        target='USA',\n        metric='STD',\n        tickers=['GS', 'IBM'])\n\nGeneric Error Catching\n----------------------\n>>> try:\n        rl.get_point_forecasts_df(target='USA', metric='STD', tickers='GS')\n    except rl.Error as exc:\n        print(exc)\n\nBasic Configuration\n-------------------\n>>> rl.APIConfig.allow_caching\nTrue\n>>> rl.APIConfig.allow_tickers_sorting\nFalse\n>>> rl.APIConfig.allow_caching = False # Disable caching.\n\nNotes\n-----\nFurther examples assume that `reefledge` has been imported as `rl`:\n\n    >>> import reefledge as rl\n", # DO NOT use single quotes!
    author='ReefLedge',
    author_email='support@reefledge.com',
    url='https://www.reefledge.com',
    download_url='https://github.com/Reefledge/reefledge/archive/refs/tags/v1.4.0' + '-alpha.0.tar.gz',
    keywords=['quant', 'quantitative', 'finance', 'forecasting', 'time-series', 'machine learning', 'trading', 'portfolio management', 'risk management'],
    install_requires=['setuptools>=50.3.1,<51.0.0', 'cython>=0.29.22,<1.0.0', 'requests>=2.25.1,<3.0.0', 'psycopg2>=2.8.6,<3.0.0', 'numpy>=1.18.5,<2.0.0', 'scipy>=1.5.0,<2.0.0', 'pandas>=1.0.5,<2.0.0', 'matplotlib>=3.2.2,<4.0.0', 'openpyxl>=3.0.5,<4.0.0', 'ipython>=7.19.0,<8.0.0', 'ipykernel>=5.3.4,<6.0.0', 'nptyping>=1.4.0,<2.0.0', 'psutil>=5.8.0,<6.0.0', 'python-dateutil>=2.8.1,<3.0.0', 'pdoc3>=0.10.0,<1.0.0', 'pydantic>=1.8.2,<2.0.0', 'cryptography>=36.0.1,<37.0.0', 'requests>=2.27.1,<3.0.0', 'backoff>=1.11.1,<2.0.0', 'cachetools>=4.2.2,<5.0.0', 'pyqt5', 'xlwings==0.27.5',],
    platforms=['Windows', 'Linux'],
    python_requires='>=3.8',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Typing :: Typed',
        f"License :: OSI Approved :: {LICENSE} License",
    ]
)

from typing import Final
from setuptools import setup

LICENSE: Final[str] = 'MIT'

setup(
    name='reefledge',
    packages=['reefledge'],
    include_package_data=True,
    version='1.1.2',
    license=LICENSE,
    description="A powerful API designed for Quantitative Finance practitioners.", # DO NOT use single quotes!
    long_description="**reefledge** is a Python package which provides a fast, simple and powerful API designed to facilitate the consumption of cutting edge density forecasting model outputs. These are generated from market data on liquid financial instruments and are the result of demanding estimation and simulation processes on a high-performance cloud cluster. Data is produced for a wide range of reference dates and asset classes, yielding forecasts for a variety of time horizons and metrics. Main Features ------------- Here are just a few of the things that make reefledge special: - Intuitive object oriented interface. - Tight integration with Microsoft Excel. - Fast and robust Cython codebase. - Multithreading capabilities to overcome I/O overhead. - Efficient and highly available back end, featuring global load  balancing, optimized connection pooling and extensive database table  partitioning, besides an intelligent use of indexes to speed up SQL  queries. Basic Usage ----------- >>> import reefledge as rl >>> rl.login(user='stokes', api_key='secret') >>> df = rl.get_df(target='NYSE', metric='STD', tickers=['GS', 'IBM'])", # DO NOT use single quotes!
    author='ReefLedge',
    author_email='duarte.stokes@reefledge.com',
    url='https://github.com/Reefledge/reefledge',
    download_url='https://github.com/Reefledge/reefledge/archive/refs/tags/v1.1.2-beta.1.tar.gz',
    keywords=['quant', 'finance', 'api', 'forecasting', 'time-series', 'machine learning', 'trading', 'portfolio management', 'risk management'],
    install_requires=['setuptools>=50.3.1', 'cython>=0.29.22', 'requests>=2.25.1', 'twilio>=6.50.1', 'psycopg2>=2.8.6', 'numpy>=1.18.5', 'scipy>=1.5.0', 'pandas>=1.0.5', 'matplotlib>=3.2.2', 'openpyxl>=3.0.5', 'ipython>=7.19.0', 'ipykernel>=5.3.4', 'nptyping>=1.4.0', 'psutil>=5.8.0', 'xlwings>=0.24.9', 'pyqt5',],
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

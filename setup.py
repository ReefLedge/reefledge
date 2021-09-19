from typing import Final
from distutils.core import setup

LICENSE: Final[str] = 'MIT'

setup(
    name='reefledge',
    packages=['reefledge'],
    version='1.0.0',
    license=LICENSE,
    description='A powerful API designed for the consumption of ML/TS model outputs.',
    author='ReefLedge',
    author_email='duarte.stokes@reefledge.com',
    url='https://github.com/Reefledge/reefledge',
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',#
    keywords=['quant', 'finance', 'api', 'forecasting', 'time-series', 'machine learning', 'trading', 'portfolio management', 'risk management'],
    install_requires=['setuptools>=50.3.1', 'cython>=0.29.22', 'requests>=2.25.1', 'twilio>=6.50.1', 'psycopg2>=2.8.6', 'numpy>=1.18.5', 'scipy>=1.5.0', 'pandas>=1.0.5', 'matplotlib>=3.2.2', 'openpyxl>=3.0.5', 'ipython>=7.19.0', 'ipykernel>=5.3.4', 'nptyping>=1.4.0', 'psutil>=5.8.0', 'xlwings>=0.24.9', 'pyqt5',],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        f"License :: OSI Approved :: {LICENSE} License",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ]
)

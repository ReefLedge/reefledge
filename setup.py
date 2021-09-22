from typing import Final, List
from distutils.core import setup

LICENSE: Final[str] = 'MIT'

with open('README.md', 'r', encoding='utf-8') as fh:
    full_description: List[str] = fh.read().splitlines()

setup(
    name='reefledge',
    packages=['reefledge'],
    version='1.0.1',
    license=LICENSE,
    description=full_description[0],
    long_description='\n'.join(full_description[2:]),
    author='ReefLedge',
    author_email='duarte.stokes@reefledge.com',
    url='https://github.com/Reefledge/reefledge',
    download_url="https://github.com/Reefledge/reefledge/archive/refs/tags/v1.0.1-beta.1.tar.gz",
    keywords=['quant', 'finance', 'api', 'forecasting', 'time-series', 'machine learning', 'trading', 'portfolio management', 'risk management'],
    install_requires=['setuptools>=50.3.1', 'cython>=0.29.22', 'requests>=2.25.1', 'twilio>=6.50.1', 'psycopg2>=2.8.6', 'numpy>=1.18.5', 'scipy>=1.5.0', 'pandas>=1.0.5', 'matplotlib>=3.2.2', 'openpyxl>=3.0.5', 'ipython>=7.19.0', 'ipykernel>=5.3.4', 'nptyping>=1.4.0', 'psutil>=5.8.0', 'xlwings>=0.24.9', 'pyqt5',],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        f"License :: OSI Approved :: {LICENSE} License",
        'Programming Language :: Python :: 3',
    ]
)

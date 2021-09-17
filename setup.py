from typing import Final
from distutils.core import setup

LICENSE: Final[str] = 'MIT'

setup(
  name = 'reefledge',
  packages = ['reefledge'],
  version = '{VERSION}',      # Start with a small number and increase it with every change you make
  license=LICENSE,
  description = 'A powerful API designed for the consumption of ML/TS model outputs.',
  author = 'ReefLedge',
  author_email = 'duarte.stokes@reefledge.com',
  url = 'https://github.com/Reefledge/reefledge',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords=['quant', 'finance', 'api', 'forecasting', 'time-series', 'trading'],
  install_requires=[            # I get to this in a second
          '{validators}',
          '{beautifulsoup4}',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    f"License :: OSI Approved :: {LICENSE} License",
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
  ],
)
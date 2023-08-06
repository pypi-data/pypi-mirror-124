# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pilotis_io', 'pilotis_io.local']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.2,<1.20.0',
 'pandas>=0.25.3,<0.26.0',
 'pyarrow>=0.17.1,<0.18.0',
 'scikit-learn>=0.22,<=1.0']

extras_require = \
{'format': ['isort>=4.3,<5.0', 'seed-isort-config>=1.9.3,<2.0.0', 'black'],
 'lint': ['flake8>=3.7,<4.0',
          'flake8-bugbear>=19.8.0,<20.0.0',
          'pydocstyle>=3.0,<4.0',
          'pylint>=2.3,<3.0',
          'yapf>=0.27.0,<0.28.0'],
 'repl': ['bpython>=0.18,<0.19'],
 'test': ['pytest>=5.1,<6.0',
          'pytest-cov>=2.8.1,<3.0.0',
          'pytest-mock>=1.13.0,<2.0.0',
          'pytest-html>=2.0.1,<3.0.0',
          'pytest-asyncio>=0.10.0,<0.11.0',
          'PyHamcrest>=2.0,<3.0'],
 'type': ['mypy>=0.740.0,<0.741.0']}

setup_kwargs = {
    'name': 'pilotis-io',
    'version': '0.2.0',
    'description': 'This is a lib with IO functions to use while coding Python ML projects',
    'long_description': None,
    'author': 'Ekinox',
    'author_email': 'contact@ekinox.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/ekinox-io/ekinox-libraries/pilotis-io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)

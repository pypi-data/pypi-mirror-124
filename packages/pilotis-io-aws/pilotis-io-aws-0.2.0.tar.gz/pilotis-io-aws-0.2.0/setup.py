# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pilotis_io_aws', 'pilotis_io_aws.s3']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.15.16,<2.0.0',
 'moto[s3]>=2.0.0,<3.0.0',
 'numpy>=1.19.2,<1.20.0',
 'pilotis-io>=0.2.0,<0.3.0',
 's3fs>=2021.5.0,<2022.0.0']

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
    'name': 'pilotis-io-aws',
    'version': '0.2.0',
    'description': 'This is the implementation of pilotis-io for AWS',
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

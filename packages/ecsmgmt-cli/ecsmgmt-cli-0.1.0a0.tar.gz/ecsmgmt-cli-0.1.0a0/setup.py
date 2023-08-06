# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecsmgmt', 'ecsmgmt._util', 'ecsmgmt.secret-key', 'ecsmgmt.user']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click>=8.0.1,<9.0.0',
 'inquirer>=2.7.0,<3.0.0',
 'python-ecsclient>=1.1.11,<2.0.0',
 'tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['ecsmgmt = ecsmgmt:cli']}

setup_kwargs = {
    'name': 'ecsmgmt-cli',
    'version': '0.1.0a0',
    'description': 'Small CLI tool for interacting with the ECS Management API',
    'long_description': None,
    'author': 'Dominik Rimpf',
    'author_email': 'dominik.rimpf@kit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

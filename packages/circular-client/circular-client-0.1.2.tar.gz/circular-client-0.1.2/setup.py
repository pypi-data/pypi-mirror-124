# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['circular_client']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'circular-client',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'CircularNetwork',
    'author_email': 'info@circularnetwork.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

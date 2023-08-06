# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skaha']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0', 'vos>=3.3.4,<4.0.0']

setup_kwargs = {
    'name': 'skaha',
    'version': '0.1.0',
    'description': 'Python Client for Skaha Container Platform in CANFAR',
    'long_description': None,
    'author': 'Shiny Brar',
    'author_email': 'charanjotbrar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

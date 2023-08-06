# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typety']

package_data = \
{'': ['*']}

install_requires = \
['sphinx-inline-tabs>=2021.8.17-beta.10,<2022.0.0']

setup_kwargs = {
    'name': 'typety',
    'version': '1.0.1',
    'description': 'A simple python packages that adds a typing effect to strings',
    'long_description': None,
    'author': 'Dragonlord1005',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Dragonlord1005/typety',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

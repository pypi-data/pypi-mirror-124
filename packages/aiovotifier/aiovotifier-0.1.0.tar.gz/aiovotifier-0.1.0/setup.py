# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiovotifier']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiovotifier',
    'version': '0.1.0',
    'description': 'An asynchronous MInecraft server votifier client in Python',
    'long_description': None,
    'author': 'Milo Weinberg',
    'author_email': 'iapetus011@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

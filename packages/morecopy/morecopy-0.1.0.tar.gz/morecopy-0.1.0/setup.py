# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['morecopy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'morecopy',
    'version': '0.1.0',
    'description': 'Copy even immutable objects as much as possible',
    'long_description': None,
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_manager']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fast-manager',
    'version': '0',
    'description': 'Create Python Web Fast, Manage Easily',
    'long_description': None,
    'author': 'weekwith.me',
    'author_email': 'leedobby@weekwith.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/0417taehyun/fast-manager',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

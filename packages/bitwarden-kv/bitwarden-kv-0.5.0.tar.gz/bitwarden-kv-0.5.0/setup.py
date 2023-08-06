# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitwarden_kv']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bitwarden-kv',
    'version': '0.5.0',
    'description': '',
    'long_description': None,
    'author': 'Afirium',
    'author_email': 'adw.rpv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

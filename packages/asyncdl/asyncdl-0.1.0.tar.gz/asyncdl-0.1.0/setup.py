# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncdl']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=3.0.0,<4.0.0', 'aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'asyncdl',
    'version': '0.1.0',
    'description': 'asyncdl is a simple wrapper around the aiohttp Python library. Its aim is to simplify the process of securely downloading files in Python applications.',
    'long_description': None,
    'author': 'Makoto',
    'author_email': 'makoto+github@taiga.sh',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

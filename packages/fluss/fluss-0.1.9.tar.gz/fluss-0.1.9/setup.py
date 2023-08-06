# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fluss', 'fluss.graphql', 'fluss.graphql.mutations', 'fluss.graphql.queries']

package_data = \
{'': ['*']}

install_requires = \
['arkitekt>=0.1.48,<0.2.0', 'herre>=0.1.28,<0.2.0']

setup_kwargs = {
    'name': 'fluss',
    'version': '0.1.9',
    'description': '',
    'long_description': None,
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

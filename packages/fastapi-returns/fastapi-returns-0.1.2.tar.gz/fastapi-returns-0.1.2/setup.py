# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_returns']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.70.0,<0.71.0',
 'requests>=2.26.0,<3.0.0',
 'returns>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'fastapi-returns',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Jakub Borusewicz',
    'author_email': 'jakub.borusewicz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jakub-borusewicz/fastapi-returns',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

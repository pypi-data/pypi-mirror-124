# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['venvarium']

package_data = \
{'': ['*']}

install_requires = \
['entry-points-txt>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'venvarium',
    'version': '0.1.0',
    'description': 'Object-based interaction with a Python virtual environment.',
    'long_description': None,
    'author': 'Maximillian Strand',
    'author_email': 'maximillian.strand@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

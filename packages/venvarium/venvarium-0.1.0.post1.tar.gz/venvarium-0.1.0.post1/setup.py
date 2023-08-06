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
    'version': '0.1.0.post1',
    'description': 'Object-based interaction with a Python virtual environment.',
    'long_description': '# venvarium\n\n## Installation\n\n```sh\npython -m pip install venvarium\n```\n\n### Example\n\n```py\nfrom venvarium import VEnv\n\n\n# Create the virtual environment\nENV_PATH = \'myproject/myenv\' \nvenv = VEnv(ENV_PATH)\n\n# Run Python, PIP, or any other package or program\nvenv.python(\'-c\', \'print("hello, world!")\')\nvenv.pip(\'install\', \'--upgrade\', \'pip\')\nvenv.run_package(\'flask\')\n\n# See all installed packages\npkgs = venv.installed_packages()\nprint(pkgs)\n\n# Get the entry points\nentry_points = venv.entry_points().get(\'my_entry_point\')\nprint(entry_points)\n```',
    'author': 'Maximillian Strand',
    'author_email': 'maximillian.strand@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/deepadmax/venvarium',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

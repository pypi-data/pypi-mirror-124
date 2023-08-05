# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fau_colors']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3,<4.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'fau-colors',
    'version': '0.3.0',
    'description': 'The official colors of the FAU as matplotlib/seaborn colormaps',
    'long_description': None,
    'author': 'Robert Richer',
    'author_email': 'robert.richer@fau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

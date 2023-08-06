# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['photogrid']
install_requires = \
['Pillow>=8.4.0,<9.0.0', 'click>=8.0.3,<9.0.0', 'rich>=10.12.0,<11.0.0']

entry_points = \
{'console_scripts': ['photogrid = photogrid:cli']}

setup_kwargs = {
    'name': 'photogrid',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Marco Rougeth',
    'author_email': 'pypi@rougeth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

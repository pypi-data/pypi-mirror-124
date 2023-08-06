# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['twalk']
entry_points = \
{'console_scripts': ['cli_command_name = twalk:main']}

setup_kwargs = {
    'name': 'twalk',
    'version': '1.0.2',
    'description': 'Condense a directory tree into a single txt file or extract it from one',
    'long_description': None,
    'author': 'Ovsyanka',
    'author_email': 'szmiev2000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ovsyanka83/twalk',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

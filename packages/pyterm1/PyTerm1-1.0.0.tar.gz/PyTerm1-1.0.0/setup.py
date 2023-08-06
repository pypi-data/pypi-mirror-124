# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyterm1']
setup_kwargs = {
    'name': 'pyterm1',
    'version': '1.0.0',
    'description': 'terminal on python3',
    'long_description': None,
    'author': 'LayfikRus',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)

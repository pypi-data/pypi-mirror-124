# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['voicennl']
setup_kwargs = {
    'name': 'voicennl',
    'version': '1.0.0',
    'description': 'ConventorizationShell("testvoice.txt").langDE()',
    'long_description': None,
    'author': 'adamsonScripts',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

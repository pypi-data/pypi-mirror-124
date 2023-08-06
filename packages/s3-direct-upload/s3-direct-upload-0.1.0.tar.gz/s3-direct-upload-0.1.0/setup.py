# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['s3_direct_upload']
setup_kwargs = {
    'name': 's3-direct-upload',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Mikhail Porokhovnichenko',
    'author_email': 'marazmiki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

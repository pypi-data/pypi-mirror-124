# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['tfa_car']
install_requires = \
['matplotlib>=3.4.3,<4.0.0',
 'numpy>=1.21.3,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'scipy>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'tfa-car',
    'version': '0.1.0',
    'description': 'A python implementation of tfa_car.m from the matlab package found at car-net.org.',
    'long_description': None,
    'author': 'Ken Liao',
    'author_email': 'cloudrainstar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)

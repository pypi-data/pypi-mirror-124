# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pk_model',
 'pk_model.dataCollectors',
 'pk_model.models',
 'pk_model.parameters',
 'pk_model.plotters',
 'pk_model.tests']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3,<4.0.0',
 'numpy>=1.20.0,<1.21.0',
 'pandas>=1.3.4,<2.0.0',
 'scipy>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'pk-model',
    'version': '0.1.5',
    'description': 'Basic Pharmokinetic Model',
    'long_description': None,
    'author': 'Kit Gallagher',
    'author_email': 'gallagherkit@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)

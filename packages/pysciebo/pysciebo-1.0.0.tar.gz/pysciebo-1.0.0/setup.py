# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysciebo']

package_data = \
{'': ['*']}

install_requires = \
['pyocclient>=0.6,<0.7']

setup_kwargs = {
    'name': 'pysciebo',
    'version': '1.0.0',
    'description': 'A Python client for sciebo aka hochschulcloud.nrw',
    'long_description': None,
    'author': 'Nils Müller',
    'author_email': 'nils.mueller@uni-bielefeld.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

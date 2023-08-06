# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybus', 'pybus.core', 'pybus.default']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'py-bus',
    'version': '0.1.5',
    'description': 'Type-safe, high-performance message bus for python users',
    'long_description': None,
    'author': 'ahnsv',
    'author_email': 'ahnsv@bc.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ahnsv/pybus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<3.9',
}


setup(**setup_kwargs)

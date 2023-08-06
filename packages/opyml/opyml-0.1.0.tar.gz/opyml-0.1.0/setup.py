# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opyml']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'opyml',
    'version': '0.1.0',
    'description': 'An OPML library for Python.',
    'long_description': None,
    'author': 'Holllo',
    'author_email': 'helllo@holllo.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['iterable_data_import',
 'iterable_data_import.data_sources',
 'iterable_data_import.error_recorders',
 'iterable_data_import.importers']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'iterable-data-import',
    'version': '0.1.0',
    'description': 'A library for ad-hoc bulk imports to Iterable',
    'long_description': None,
    'author': 'julianmclain',
    'author_email': 'julianrmclain@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

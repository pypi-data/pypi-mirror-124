# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py_vendor']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['py-vendor = py_vendor.console:main']}

setup_kwargs = {
    'name': 'py-vendor',
    'version': '0.1.2',
    'description': 'Easily vendor code into your project',
    'long_description': None,
    'author': 'Stanislav Schmidt',
    'author_email': 'stanislav.schmidt@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openconnecter']

package_data = \
{'': ['*']}

install_requires = \
['pyotp>=2.6.0,<3.0.0']

entry_points = \
{'console_scripts': ['openconnecter = openconnecter.__main__:main']}

setup_kwargs = {
    'name': 'openconnecter',
    'version': '0.0.1',
    'description': 'Wrapper for initiating an openconnect session',
    'long_description': '',
    'author': 'Kamyab Taghizadeh',
    'author_email': 'kamyab.zad@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kamyabzad/openconnecter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

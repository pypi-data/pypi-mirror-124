# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['talerbank',
 'talerbank.app',
 'talerbank.app.management',
 'talerbank.app.management.commands',
 'talerbank.app.migrations']

package_data = \
{'': ['*'],
 'talerbank.app': ['locale/*', 'static/*', 'templates/*', 'testconfigs/*']}

install_requires = \
['Babel>=2.8.0,<3.0.0',
 'Jinja2>=3.0.0,<4.0.0',
 'click>=7.1.2,<8.0.0',
 'django>=3.1.3,<4.0.0',
 'lxml>=4.6.1,<5.0.0',
 'psycopg2>=2.8.6,<3.0.0',
 'qrcode>=6.1,<7.0',
 'requests>=2.24.0,<3.0.0',
 'taler-util>=0.8.3,<0.9.0',
 'uWSGI>=2.0.19,<3.0.0']

entry_points = \
{'console_scripts': ['taler-bank-manage = talerbank.cli:run']}

setup_kwargs = {
    'name': 'talerbank',
    'version': '0.8.2',
    'description': 'Taler demo bank',
    'long_description': None,
    'author': 'Marcello Stanisci',
    'author_email': 'ms@taler.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

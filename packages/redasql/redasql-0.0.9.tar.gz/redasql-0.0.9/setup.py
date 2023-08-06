# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redasql']

package_data = \
{'': ['*']}

install_requires = \
['prettytable>=2.2.0,<3.0.0',
 'prompt-toolkit>=3.0.20,<4.0.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['redasql = redasql.command:main']}

setup_kwargs = {
    'name': 'redasql',
    'version': '0.0.9',
    'description': 'RedaSQL is query cli tool for redash.',
    'long_description': None,
    'author': 'denzow',
    'author_email': 'denzow@gmail.com',
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

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bracket_check', 'bracket_check.app']

package_data = \
{'': ['*']}

install_requires = \
['python-shell>=1.0.4,<2.0.0']

entry_points = \
{'console_scripts': ['create = create_util:run']}

setup_kwargs = {
    'name': 'bracket-check',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'skotwind',
    'author_email': 'skotwind@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

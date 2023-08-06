# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trackbranch']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['trackbranch = trackbranch.main:main']}

setup_kwargs = {
    'name': 'trackbranch',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Kevin Morris',
    'author_email': 'kevr@0cost.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

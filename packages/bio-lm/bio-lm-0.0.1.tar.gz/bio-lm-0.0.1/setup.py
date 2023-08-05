# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bio_lm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bio-lm',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Ryan Eloff',
    'author_email': 'rp.eloff@instadeep.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

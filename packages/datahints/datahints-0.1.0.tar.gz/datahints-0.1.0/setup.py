# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datahints']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'datahints',
    'version': '0.1.0',
    'description': 'Type hinting for pandas DataFrame',
    'long_description': None,
    'author': 'Ketil Albertsen',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

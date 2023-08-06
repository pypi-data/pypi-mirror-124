# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gateway2_lisa']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gateway2-lisa',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'matfonseca',
    'author_email': 'mfonseca@fi.uba.ar',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

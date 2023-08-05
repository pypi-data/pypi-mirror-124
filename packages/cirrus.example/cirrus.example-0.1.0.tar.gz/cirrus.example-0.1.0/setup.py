# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cirrus_example']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cirrus.example',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Bryant Tran',
    'author_email': 'Bryant.Tran@cirrus.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mockitup']

package_data = \
{'': ['*']}

install_requires = \
['PyHamcrest>=2.0.2,<3.0.0', 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'mockitup',
    'version': '0.0.4',
    'description': 'A `unittest.mock` wrapper for easier mocking',
    'long_description': None,
    'author': 'Shacham Ginat',
    'author_email': 'shacham6@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.10,<4.0.0',
}


setup(**setup_kwargs)

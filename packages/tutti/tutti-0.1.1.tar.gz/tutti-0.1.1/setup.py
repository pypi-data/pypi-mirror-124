# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tutti', 'tutti.backends']

package_data = \
{'': ['*']}

install_requires = \
['hiredis>=2.0.0,<3.0.0', 'redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'tutti',
    'version': '0.1.1',
    'description': 'Distributed Synchronization Primitives',
    'long_description': None,
    'author': 'Hamilton Kibbe',
    'author_email': 'ham@hamiltonkib.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

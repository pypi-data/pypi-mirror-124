# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vasyok']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.4,<2.0.0']

setup_kwargs = {
    'name': 'vasyok',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'konstantgr',
    'author_email': '60608301+konstantgr@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

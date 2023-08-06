# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pykage',
 'pykage.command',
 'pykage.console',
 'pykage.data',
 'pykage.errors',
 'pykage.files',
 'pykage.packages',
 'pykage.regex',
 'pykage.system']

package_data = \
{'': ['*']}

install_requires = \
['PyInquirer>=1.0.3,<2.0.0',
 'bs4>=0.0.1,<0.0.2',
 'click>=8.0.3,<9.0.0',
 'clint>=0.5.1,<0.6.0',
 'codegen>=1.0,<2.0',
 'cx-Freeze>=6.8.1,<7.0.0',
 'jk-json>=0.2021.3,<0.2022.0',
 'jk-pypiorgapi>=0.2021.4,<0.2022.0',
 'packaging>=21.0,<22.0',
 'requests>=2.26.0,<3.0.0',
 'sh>=1.14.2,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'pykage',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'antoineB24',
    'author_email': '85784092+antoineB24@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

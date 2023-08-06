# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['t2d']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0', 'telegram.py>=0.3.1,<0.4.0', 'typer>=0.4.0,<0.5.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 't2d',
    'version': '0.1.0',
    'description': 'Seamless integration between Typer and Telegram.py for CLI Telegram bots',
    'long_description': None,
    'author': 'Gabriel Gazola Milan',
    'author_email': 'gabriel.gazola@poli.ufrj.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

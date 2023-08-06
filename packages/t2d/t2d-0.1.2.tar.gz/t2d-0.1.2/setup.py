# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['t2d']

package_data = \
{'': ['*']}

install_requires = \
['discord.py>=1.7.3,<2.0.0', 'loguru>=0.5.3,<0.6.0', 'typer>=0.4.0,<0.5.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 't2d',
    'version': '0.1.2',
    'description': 'Seamless integration between Typer and Discord.py for CLI Discord bots',
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

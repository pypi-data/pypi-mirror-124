# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unasync_cli']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['unasync = unasync_cli.main:app']}

setup_kwargs = {
    'name': 'unasync-cli',
    'version': '0.0.2',
    'description': 'Command line interface for unasync',
    'long_description': '# CLI for unasync\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)\n[![Test](https://github.com/leynier/unasync-cli/workflows/CI/badge.svg)](https://github.com/leynier/unasync-cli/actions?query=workflow%3ACI)\n[![codecov](https://codecov.io/gh/leynier/unasync-cli/branch/main/graph/badge.svg?token=Z1MEEL3EAB)](https://codecov.io/gh/leynier/unasync-cli)\n[![Version](https://img.shields.io/pypi/v/unasync-cli?color=%2334D058&label=Version)](https://pypi.org/project/unasync-cli)\n[![Last commit](https://img.shields.io/github/last-commit/leynier/unasync-cli.svg?style=flat)](https://github.com/leynier/unasync-cli/commits)\n[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/leynier/unasync-cli)](https://github.com/leynier/unasync-cli/commits)\n[![Github Stars](https://img.shields.io/github/stars/leynier/unasync-cli?style=flat&logo=github)](https://github.com/leynier/unasync-cli/stargazers)\n[![Github Forks](https://img.shields.io/github/forks/leynier/unasync-cli?style=flat&logo=github)](https://github.com/leynier/unasync-cli/network/members)\n[![Github Watchers](https://img.shields.io/github/watchers/leynier/unasync-cli?style=flat&logo=github)](https://github.com/leynier/unasync-cli)\n[![Website](https://img.shields.io/website?up_message=online&url=https%3A%2F%2Fleynier.github.io/unasync-cli)](https://leynier.github.io/unasync-cli)\n[![GitHub contributors](https://img.shields.io/github/contributors/leynier/unasync-cli)](https://github.com/leynier/unasync-cli/graphs/contributors)\n\nCommand line interface for unasync\n',
    'author': 'Leynier Gutiérrez González',
    'author_email': 'leynier41@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/leynier/unasync-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.14,<4.0.0',
}


setup(**setup_kwargs)

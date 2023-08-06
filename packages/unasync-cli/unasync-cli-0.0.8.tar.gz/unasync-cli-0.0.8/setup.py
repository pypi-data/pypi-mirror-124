# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unasync_cli']

package_data = \
{'': ['*']}

install_requires = \
['setuptools>=58.2.0,<59.0.0', 'typer>=0.4.0,<0.5.0', 'unasync>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['unasync = unasync_cli.main:app']}

setup_kwargs = {
    'name': 'unasync-cli',
    'version': '0.0.8',
    'description': 'Command line interface for unasync',
    'long_description': '# CLI for unasync\n\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)\n[![Test](https://github.com/leynier/unasync-cli/workflows/CI/badge.svg)](https://github.com/leynier/unasync-cli/actions?query=workflow%3ACI)\n[![codecov](https://codecov.io/gh/leynier/unasync-cli/branch/main/graph/badge.svg?token=Z1MEEL3EAB)](https://codecov.io/gh/leynier/unasync-cli)\n[![Version](https://img.shields.io/pypi/v/unasync-cli?color=%2334D058&label=Version)](https://pypi.org/project/unasync-cli)\n[![Last commit](https://img.shields.io/github/last-commit/leynier/unasync-cli.svg?style=flat)](https://github.com/leynier/unasync-cli/commits)\n[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/leynier/unasync-cli)](https://github.com/leynier/unasync-cli/commits)\n[![Github Stars](https://img.shields.io/github/stars/leynier/unasync-cli?style=flat&logo=github)](https://github.com/leynier/unasync-cli/stargazers)\n[![Github Forks](https://img.shields.io/github/forks/leynier/unasync-cli?style=flat&logo=github)](https://github.com/leynier/unasync-cli/network/members)\n[![Github Watchers](https://img.shields.io/github/watchers/leynier/unasync-cli?style=flat&logo=github)](https://github.com/leynier/unasync-cli)\n[![Website](https://img.shields.io/website?up_message=online&url=https%3A%2F%2Fleynier.github.io/unasync-cli)](https://leynier.github.io/unasync-cli)\n[![GitHub contributors](https://img.shields.io/github/contributors/leynier/unasync-cli?label=code%20contributors)](https://github.com/leynier/unasync-cli/graphs/contributors) <!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->\n[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)\n<!-- ALL-CONTRIBUTORS-BADGE:END -->\n\nCommand line interface for unasync\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tr>\n    <td align="center"><a href="http://leynier.github.io"><img src="https://avatars.githubusercontent.com/u/36774373?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Leynier Gutiérrez González</b></sub></a><br /><a href="#maintenance-leynier" title="Maintenance">🚧</a> <a href="https://github.com/leynier/unasync-cli/commits?author=leynier" title="Code">💻</a> <a href="#infra-leynier" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>\n  </tr>\n</table>\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n',
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

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diskcsvsort', 'diskcsvsort.cli']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'diskcsvsort',
    'version': '0.1.0',
    'description': 'Sort huge csv files.',
    'long_description': "# Disk CSV Sort\n\n[![Supported Versions](https://img.shields.io/badge/python-3.10%2B-blue)](https://shields.io/)\n\n## Description\n\nSort huge CSV files using disk space and RAM together.\n\nFor now support only CSV files with **header**.\n\n## Usage\n\nSort CSV file `path/to/file.csv` by column `Some Column`.\n\n```python\nfrom pathlib import Path\nfrom diskcsvsort import CSVSort\n\ncsvsort = CSVSort(\n    src=Path('path/to/file.csv'),\n    key=lambda row: row['Some Column'],\n)\ncsvsort.apply()\n\n```\n\n### CLI\nSort CSV file `path/to/file.csv` by columns `col1` and `col2`.\n`col1` will be converted to python `str` and `col2` will be converted to python `int`.\n\n    python -m diskcsvsort path/to/file.csv --by col1:str --by col2:int\n\n#### Available types:\n - str\n - int\n - float\n - datetime\n - date\n - time\n\n#### Types usage:\n- str: `column:str` \n- int: `column:int` \n- float: `column:float` \n- datetime: `column:datetime(%Y-%m-%d %H:%M:%S)`\n- date: `column:datetime(%Y-%m-%d)`\n- time: `column:datetime(%H:%M:%S)`\n\n\n## Algorithm\nTODO\n",
    'author': 'volodymyrb',
    'author_email': 'volodymyr.borysiuk0@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/VolodymyrBor/diskcsvsort',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

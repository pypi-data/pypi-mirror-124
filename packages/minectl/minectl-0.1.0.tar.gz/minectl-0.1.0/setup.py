# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['minectl',
 'minectl.cli',
 'minectl.configs',
 'minectl.schemas',
 'minectl.tasks',
 'minectl.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'blackcap']

entry_points = \
{'console_scripts': ['minectl = minectl.cli.main:main']}

setup_kwargs = {
    'name': 'minectl',
    'version': '0.1.0',
    'description': 'InterMine automation helper',
    'long_description': None,
    'author': 'Ankur Kumar',
    'author_email': 'ank@leoank.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

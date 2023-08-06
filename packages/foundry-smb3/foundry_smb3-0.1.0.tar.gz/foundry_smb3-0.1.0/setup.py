# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['foundry',
 'foundry.game',
 'foundry.game.gfx',
 'foundry.game.gfx.drawable',
 'foundry.game.gfx.objects',
 'foundry.game.level',
 'foundry.gui',
 'foundry.smb3parse',
 'foundry.smb3parse.levels',
 'foundry.smb3parse.objects',
 'foundry.smb3parse.util']

package_data = \
{'': ['*'], 'foundry': ['data/*', 'data/icons/*', 'doc/*']}

install_requires = \
['PySide2>=5.15.2,<6.0.0', 'QDarkStyle>=3.0.2,<4.0.0']

entry_points = \
{'console_scripts': ['foundry = foundry.main:main']}

setup_kwargs = {
    'name': 'foundry-smb3',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'TheJoeSmo',
    'author_email': 'joesmo.joesmo12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<3.10',
}


setup(**setup_kwargs)

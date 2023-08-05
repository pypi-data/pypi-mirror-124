# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['questgen', 'questgen.quests', 'questgen.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'questgen',
    'version': '0.4.1',
    'description': 'Generator of nonlenear quests with events and flow validating.',
    'long_description': None,
    'author': 'Aliaksei Yaletski (Tiendil)',
    'author_email': 'a.eletsky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Tiendil/questgen',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)

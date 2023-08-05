# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deworld',
 'deworld.configs',
 'deworld.layers',
 'deworld.power_points',
 'deworld.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'deworld',
    'version': '0.2.2',
    'description': 'Developing world - python world generator.',
    'long_description': None,
    'author': 'Aliaksei Yaletski (Tiendil)',
    'author_email': 'a.eletsky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Tiendil/deworld',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)

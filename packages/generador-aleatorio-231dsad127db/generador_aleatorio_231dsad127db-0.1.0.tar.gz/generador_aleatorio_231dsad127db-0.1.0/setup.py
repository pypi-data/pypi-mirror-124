# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['generador_aleatorio']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'generador-aleatorio-231dsad127db',
    'version': '0.1.0',
    'description': 'El generador aleatorio de frases mas potente del mundo! No hay otro igual...tiembla Google!',
    'long_description': None,
    'author': 'internetmosquito',
    'author_email': 'alejandrovillamarin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['excprocess']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'excprocess',
    'version': '0.1.2',
    'description': 'Python subprocess with externalized exceptions',
    'long_description': '# Excprocess\n\nPython subprocess that will capture any exceptions raised inside it and re-raise them outside.',
    'author': 'Maximillian Strand',
    'author_email': 'maximillian.strand@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/deepadmax/excprocess',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

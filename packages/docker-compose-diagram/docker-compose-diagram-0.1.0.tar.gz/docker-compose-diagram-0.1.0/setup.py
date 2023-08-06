# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docker_compose_diagram']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'click>=8.0.3,<9.0.0', 'diagrams>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'docker-compose-diagram',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Skonik',
    'author_email': 's.konik.jobk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

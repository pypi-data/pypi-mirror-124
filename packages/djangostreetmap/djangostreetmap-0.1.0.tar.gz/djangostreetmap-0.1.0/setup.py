# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djangostreetmap',
 'djangostreetmap.management',
 'djangostreetmap.management.commands',
 'djangostreetmap.migrations',
 'djangostreetmap.test_config']

package_data = \
{'': ['*'],
 'djangostreetmap': ['notebooks/*',
                     'notebooks/.ipynb_checkpoints/*',
                     'requirements/*',
                     'stubs/osmium/*',
                     'stubs/osmium/osm/*',
                     'stubs/osmium/replication/*',
                     'templates/*']}

install_requires = \
['osmium>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'djangostreetmap',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Joshua Brooks',
    'author_email': 'josh.vdbroek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['authanon', 'authanon.management.commands', 'authanon.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0,<4.0']

setup_kwargs = {
    'name': 'django-authanon',
    'version': '0.1.0',
    'description': 'Allows permissions for an anonymous user and a generic signed-in user to be set as groups.',
    'long_description': None,
    'author': 'Robert Turnbull',
    'author_email': 'robert.turnbull@unimelb.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)

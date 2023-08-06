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
    'version': '0.1.2',
    'description': 'Allows permissions for an anonymous user and a generic signed-in user to be set as groups.',
    'long_description': '# django-authanon\n\n![pipline](https://github.com/rbturnbull/django-authanon/actions/workflows/pipeline.yml/badge.svg)\n[<img src="https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/rbturnbull/49262550cc8b0fb671d46df58de213d4/raw/django-authanon-coverage.json">](<https://rbturnbull.github.io/django-authanon/>)\n[<img src="https://img.shields.io/badge/code%20style-black-000000.svg">](<https://github.com/psf/black>)\n\nAllows permissions for an anonymous user and a generic signed-in user to be set as groups.\n\n## Installation \n\n```\npip install django-authanon\n```\n\nThen add to your `INSTALLED_APPS`:\n```\nINSTALLED_APPS += [\n    "authanon",\n]\n```\n\nThen add to your `AUTHENTICATION_BACKENDS`:\n```\nAUTHENTICATION_BACKENDS += [\n    "authanon.backends.AuthanonBackend",\n]\n```\n\n## Usage\n\nThis app creates two groups, one for anonymous users who aren\'t logged in and one group for users who are logged in. You can add permissions to these groups in the admin console in the \'Groups\' section under the \'AUTHENTICATION AND AUTHORIZATION\' section.\n\nTo display the permissions for these two groups on the command line, use this command.\n```\n./manage.py authanon\n```\n\nThese groups are automatically created when anonymous users or logged-in users try to access pages. If you find they haven\'t been created yet, use the `./manage.py authanon` command and then the groups will appear in the admin.\n\n## Configuration\nBy default, the two groups are called `Anonymous` and `Login Users`. You can change them by variables to the settings with the names `AUTHANON_ANONYMOUS_GROUP` or `AUTHANON_LOGIN_GROUP`.\n\n\n## Credits\nPackage authored by Robert Turnbull (Melbourne Data Analytics Platform)\n\nInspired by this Stack Overflow answer: https://stackoverflow.com/a/31520798 (User: jozxyqk)\n',
    'author': 'Robert Turnbull',
    'author_email': 'robert.turnbull@unimelb.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rbturnbull/django-authanon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)

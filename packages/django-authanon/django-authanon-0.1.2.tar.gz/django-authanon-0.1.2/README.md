# django-authanon

![pipline](https://github.com/rbturnbull/django-authanon/actions/workflows/pipeline.yml/badge.svg)
[<img src="https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/rbturnbull/49262550cc8b0fb671d46df58de213d4/raw/django-authanon-coverage.json">](<https://rbturnbull.github.io/django-authanon/>)
[<img src="https://img.shields.io/badge/code%20style-black-000000.svg">](<https://github.com/psf/black>)

Allows permissions for an anonymous user and a generic signed-in user to be set as groups.

## Installation 

```
pip install django-authanon
```

Then add to your `INSTALLED_APPS`:
```
INSTALLED_APPS += [
    "authanon",
]
```

Then add to your `AUTHENTICATION_BACKENDS`:
```
AUTHENTICATION_BACKENDS += [
    "authanon.backends.AuthanonBackend",
]
```

## Usage

This app creates two groups, one for anonymous users who aren't logged in and one group for users who are logged in. You can add permissions to these groups in the admin console in the 'Groups' section under the 'AUTHENTICATION AND AUTHORIZATION' section.

To display the permissions for these two groups on the command line, use this command.
```
./manage.py authanon
```

These groups are automatically created when anonymous users or logged-in users try to access pages. If you find they haven't been created yet, use the `./manage.py authanon` command and then the groups will appear in the admin.

## Configuration
By default, the two groups are called `Anonymous` and `Login Users`. You can change them by variables to the settings with the names `AUTHANON_ANONYMOUS_GROUP` or `AUTHANON_LOGIN_GROUP`.


## Credits
Package authored by Robert Turnbull (Melbourne Data Analytics Platform)

Inspired by this Stack Overflow answer: https://stackoverflow.com/a/31520798 (User: jozxyqk)

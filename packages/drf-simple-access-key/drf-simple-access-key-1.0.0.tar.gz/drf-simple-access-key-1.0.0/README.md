# DRF Simple Access Key

[![PyPI](https://badge.fury.io/py/drf-simple-access-key.svg)](https://pypi.org/project/drf-simple-access-key/)
[![Test Status](https://github.com/anexia-it/drf-simple-access-key/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/anexia-it/drf-simple-access-key/actions/workflows/test.yml)
[![Codecov](https://codecov.io/gh/anexia-it/drf-simple-access-key/branch/main/graph/badge.svg)](https://codecov.io/gh/anexia-it/drf-simple-access-key)

A library that provides a simple token authorization for Django REST framework.

## Installation

With a [correctly configured](https://pipenv.pypa.io/en/latest/basics/#basic-usage-of-pipenv) `pipenv` toolchain:

```sh
pipenv install drf-simple-access-key
```

You may also use classic `pip` to install the package:

```sh
pip install drf-simple-access-key
```

## Getting started

### Configuration options

#### `HTTP_AUTHORIZATION_HEADER: str`

Default: `'x-authorization'`

Name of the HTTP request header used for authorization.

#### `HTTP_AUTHORIZATION_SCHEME: str`

Default: `'bearer'`

Name of the HTTP authorization scheme.

#### `AUTHORIZATION_KEYS: list[str]`

Default: `[]`

List of valid authorization keys. Note that any request is allowed if this configuration option is empty!

### Example configuration for Django settings

```python
SIMPLE_ACCESS_KEY_SETTINGS = {
    'HTTP_AUTHORIZATION_HEADER': 'x-authorization',
    'HTTP_AUTHORIZATION_SCHEME': 'bearer',
    'AUTHORIZATION_KEYS': [
        'example-token-1234',
    ],
}

REST_FRAMEWORK = {
    # ...
    'DEFAULT_PERMISSION_CLASSES': [
        'drf_simple_access_key.SimpleAccessKey',
        # ...
    ],
    # ...
}
```

### How to use

All API endpoints that use the permission class are protected by the simple access key authorization.

```
GET http://my.tld/api/v1/resource/
x-authorization: bearer example-token-1234
```

## Supported versions

|             | Django REST framework 3.10 | Django REST framework 3.11 | Django REST framework 3.12 |
|-------------|----------------------------|----------------------------|----------------------------|
| Python 3.6  | ✓                          | ✓                          | ✓                          |
| Python 3.7  | ✓                          | ✓                          | ✓                          |
| Python 3.8  | ✓                          | ✓                          | ✓                          |
| Python 3.9  | ✓                          | ✓                          | ✓                          |
| Python 3.10 | ✓                          | ✓                          | ✓                          |
| PyPy3       | ✓                          | ✓                          | ✓                          |

## List of developers

* Andreas Stocker <AStocker@anexia-it.com>
* Harald Nezbeda <HNezbeda@anexia-it.com>

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asgi_correlation_id']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asgi-correlation-id',
    'version': '0.1.3',
    'description': 'Middleware that propagates HTTP header correlation IDs to project logs',
    'long_description': '[![test](https://github.com/snok/asgi-correlation-id/actions/workflows/test.yml/badge.svg)](https://github.com/snok/asgi-correlation-id/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/snok/asgi-correlation-id/branch/master/graph/badge.svg?token=1aXlWPm2gb)](https://codecov.io/gh/snok/asgi-correlation-id)\n[![pypi](https://pypi.org/pypi/asgi-correlation-id)](https://github.com/snok/asgi-correlation-id)\n\n\n# ASGI Correlation ID middleware\n\nThis is a rewrite of [django-guid](django-guid) for ASGI apps.\n',
    'author': 'Jonas Krüger Svensson',
    'author_email': 'jonas-ks@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/snok/asgi-correlation-id',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

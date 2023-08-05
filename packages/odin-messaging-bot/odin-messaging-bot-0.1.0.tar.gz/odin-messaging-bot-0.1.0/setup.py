# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odin_messaging_bot']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'odin-messaging-bot',
    'version': '0.1.0',
    'description': 'A NATS/STAN Bot to publish/subscribe messages.',
    'long_description': None,
    'author': 'adolfrodeno',
    'author_email': 'amvillalobos@uc.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

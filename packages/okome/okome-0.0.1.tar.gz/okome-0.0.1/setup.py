# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['okome']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.7"': ['dataclasses']}

setup_kwargs = {
    'name': 'okome',
    'version': '0.0.1',
    'description': 'dataclass comment parser',
    'long_description': None,
    'author': 'yukinarit',
    'author_email': 'yukinarit84@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

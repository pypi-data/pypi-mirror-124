# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_settings_env']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0,<4.0', 'envex>=1.0,<2.0']

extras_require = \
{'django-class-settings': ['django-class-settings>=0.2,<0.3']}

setup_kwargs = {
    'name': 'django-settings-env',
    'version': '3.0.1',
    'description': '12-factor.net settings support for Django based on envex',
    'long_description': None,
    'author': 'David Nugent',
    'author_email': 'davidn@uniquode.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

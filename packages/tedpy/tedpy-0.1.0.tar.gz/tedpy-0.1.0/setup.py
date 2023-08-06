# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tedpy']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.20.0,<0.21.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'tedpy',
    'version': '0.1.0',
    'description': 'Unofficial library for reading from The Energy Detective power meters',
    'long_description': None,
    'author': 'rianadon',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

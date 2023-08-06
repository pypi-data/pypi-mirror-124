# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bf_tools']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['bf-info = bf_tools.bf_info:main']}

setup_kwargs = {
    'name': 'bf-tools',
    'version': '0.7.0',
    'description': 'This is the package including tools for BrainFrame developers to debug the system.',
    'long_description': None,
    'author': 'Stephen Li',
    'author_email': 'stephen@aotu.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=2.7,<4.0',
}


setup(**setup_kwargs)

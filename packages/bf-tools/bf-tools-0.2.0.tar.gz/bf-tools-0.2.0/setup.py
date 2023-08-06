# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bf_tools']

package_data = \
{'': ['*']}

install_requires = \
['brainframe-cli>=0.2.0,<0.3.0',
 'docker>=5.0.3,<6.0.0',
 'mjson>=0.3.1,<0.4.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['bf-info = bf_tools.bf_info:main']}

setup_kwargs = {
    'name': 'bf-tools',
    'version': '0.2.0',
    'description': 'These are the tools for BrainFrame developers to debug the system issues.',
    'long_description': None,
    'author': 'Stephen Li',
    'author_email': 'stephen@aotu.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

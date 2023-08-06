# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colorsplash_common']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.19.3,<2.0.0']

setup_kwargs = {
    'name': 'colorsplash-common',
    'version': '0.2.0',
    'description': 'A common set of classes for the ColorSplash project python components',
    'long_description': '# colorsplash-common\n\nThis is a package deployed to PyPi to be used in the other application modules in the ColorSplash web application.',
    'author': 'Daniel Thurau',
    'author_email': 'daniel.n.thurau@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://thurau.io/colorsplash/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

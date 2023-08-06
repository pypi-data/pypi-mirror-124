# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['color_mask']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['clrmsk = color_mask.color_mask:main']}

setup_kwargs = {
    'name': 'color-mask',
    'version': '0.1.0',
    'description': "This library creates a color mask for an image and lets you download the masked image. To create a mask simply use command 'clrmsk createmsk <path of the image>. To save the mask simply use 'clrmsk savemsk <path of the image>.",
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

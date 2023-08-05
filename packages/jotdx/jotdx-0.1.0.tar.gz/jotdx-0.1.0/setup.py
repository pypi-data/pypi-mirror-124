# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jotdx',
 'jotdx.contrib',
 'jotdx.crawler',
 'jotdx.parser',
 'jotdx.reader',
 'jotdx.utils']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.20.0,<0.21.0',
 'loguru>=0.5.3,<0.6.0',
 'pandas>=1.3.4,<2.0.0',
 'tenacity>=8.0.1,<9.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'jotdx',
    'version': '0.1.0',
    'description': 'Get data',
    'long_description': None,
    'author': 'FangyangJz',
    'author_email': 'fangyang.jing@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loafer', 'loafer.ext']

package_data = \
{'': ['*']}

install_requires = \
['cached-property>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'pydrinker-loafer',
    'version': '1.0.0',
    'description': 'Asynchronous message dispatcher for concurrent tasks processing',
    'long_description': "# pydrinker-loafer\n\n![build on github actions](https://github.com/pydrinker/pydrinker-loafer/actions/workflows/test.yml/badge.svg?branch=main)\n\nThis is where the [pydrinker](https://github.com/pydrinker/pydrinker) starts, this project is based on [olist-loafer](https://github.com/olist/olist-loafer) the unique difference between olist-loafer and pydrinker-loafer is about dependencies with [aiobotocore](https://github.com/aio-libs/aiobotocore), pydrinker-loafer doesn't have this dependency.\n\nTo understand more about pydrinker [see the repo](https://github.com/pydrinker/pydrinker).\n",
    'author': 'Rafael Henrique da Silva Correia',
    'author_email': 'rafael@abraseucodigo.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pydrinker/pydrinker-loafer/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)

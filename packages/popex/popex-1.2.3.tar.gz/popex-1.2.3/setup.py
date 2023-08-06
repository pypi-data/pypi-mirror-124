# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['popex',
 'popex..ipynb_checkpoints',
 'popex.isampl',
 'popex.isampl..ipynb_checkpoints',
 'popex.isampl.test',
 'popex.test']

package_data = \
{'': ['*']}

install_requires = \
['colorcet>=2.0.6,<3.0.0',
 'jupyterlab>=3.0.9,<4.0.0',
 'pandas>=1.2.3,<2.0.0',
 'properscoring>=0.1,<0.2',
 'setuptools>=54.1.2,<55.0.0',
 'wquantiles>=0.5,<0.6']

setup_kwargs = {
    'name': 'popex',
    'version': '1.2.3',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

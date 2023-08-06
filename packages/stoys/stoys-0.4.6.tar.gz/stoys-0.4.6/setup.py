# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stoys',
 'stoys.deps',
 'stoys.integration',
 'stoys.scala',
 'stoys.spark',
 'stoys.spark.aggsum',
 'stoys.spark.dp',
 'stoys.spark.dq',
 'stoys.ui',
 'stoys.utils']

package_data = \
{'': ['*'], 'stoys.deps': ['_embedded/*']}

install_requires = \
['pandas>=1,<2', 'pyserde>=0.5.0', 'pyspark>=3,<3.3']

entry_points = \
{'console_scripts': ['get-deps = stoys.deps.download:download_dependencies']}

setup_kwargs = {
    'name': 'stoys',
    'version': '0.4.6',
    'description': 'Stoys: Spark Tools @ stoys.io',
    'long_description': None,
    'author': 'Stoys Authors',
    'author_email': 'authors@stoys.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stoys-io/stoys-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)

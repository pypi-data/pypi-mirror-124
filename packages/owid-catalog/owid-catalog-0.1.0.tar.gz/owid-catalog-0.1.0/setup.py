# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['owid', 'owid.catalog']

package_data = \
{'': ['*'], 'owid.catalog': ['schemas/*']}

install_requires = \
['dataclasses-json>=0.5.6,<0.6.0',
 'ipdb>=0.13.9,<0.14.0',
 'jsonschema>=3.2.0,<4.0.0',
 'pandas-stubs>=1.2.0,<2.0.0',
 'pandas>=1.3.3,<2.0.0',
 'pyarrow>=5.0.0,<6.0.0',
 'pytest-cov>=2.12.1,<3.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'owid-catalog',
    'version': '0.1.0',
    'description': 'Core data types used by OWID for managing data.',
    'long_description': None,
    'author': 'Our World In Data',
    'author_email': 'tech@ourworldindata.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfaudit', 'cfaudit.aws', 'cfaudit.cli', 'cfaudit.generic']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11,<3.0',
 'PyYAML>=5.3,<6.0',
 'boto3>=1.14,<2.0',
 'click>=7.1,<8.0',
 'colorama>=0.4.3,<0.5.0']

entry_points = \
{'console_scripts': ['cfaudit = cfaudit.sg_audit:main']}

setup_kwargs = {
    'name': 'cfaudit',
    'version': '0.3',
    'description': 'The CityFibre AWS security group analyzer',
    'long_description': None,
    'author': 'Sergii Reznichenko',
    'author_email': 'srezni@softserveinc.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

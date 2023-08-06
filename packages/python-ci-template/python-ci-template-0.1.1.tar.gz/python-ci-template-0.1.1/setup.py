# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['python_ci_template']

package_data = \
{'': ['*']}

install_requires = \
['awswrangler>=2.12.1,<3.0.0',
 'click>=8.0.3,<9.0.0',
 'desert>=2020.11.18,<2021.0.0']

entry_points = \
{'console_scripts': ['my-script = python_ci_template.console:main']}

setup_kwargs = {
    'name': 'python-ci-template',
    'version': '0.1.1',
    'description': 'template to create python package including generic CI tools',
    'long_description': None,
    'author': 'dolfno',
    'author_email': 'dnoordman@schubergphilis.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)

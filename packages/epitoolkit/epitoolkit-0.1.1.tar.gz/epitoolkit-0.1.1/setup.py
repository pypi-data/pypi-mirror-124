# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['epitoolkit']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=4.2.0,<5.0.0',
 'autopep8>=1.5.7,<2.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'numpy>=1.21.3,<2.0.0',
 'pandas>=1.3.4,<2.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'plotly>=5.3.1,<6.0.0',
 'scipy>=1.7.1,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'epitoolkit',
    'version': '0.1.1',
    'description': 'EpiToolkit is a set of tools useful in the analysis of data from EPIC / 450K microarrays.',
    'long_description': None,
    'author': 'Jan Bińkowski',
    'author_email': 'jan.binkowski@pum.edu.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)

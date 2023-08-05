# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sepplotlib']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3,<4.0.0', 'pandas>=1.3.4,<2.0.0', 'seaborn>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'sepplotlib',
    'version': '0.3.1',
    'description': 'Separation plots for classification problems',
    'long_description': '# sepplotlib\n\n> Separation plots for classification problems.\n\n## Installation\n\n`pip install sepplotlib` to install.\n\n## Example usage\n\nTo generate a one-dimensional separation plot:\n\n```python\n\n```\n\nTo generate a model criticism plot:\n\n```python\n\n```\n\nTo generate a two-dimensional, bi-separation plot:\n\n```python\n\n```\n',
    'author': 'Remco Bastiaan Jansen',
    'author_email': 'r.b.jansen.uu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

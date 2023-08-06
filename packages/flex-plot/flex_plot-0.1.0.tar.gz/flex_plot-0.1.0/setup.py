# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flex_plot', 'flex_plot.cli']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.1,<4.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['flex-plot-run = flex_plot.cli.run:main']}

setup_kwargs = {
    'name': 'flex-plot',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Ilyas Kuhlemann',
    'author_email': 'ilyasp.ku@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mtng']

package_data = \
{'': ['*'], 'mtng': ['template/*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'aiohttp>=3.7.4,<4.0.0',
 'gidgethub>=5.0.1,<6.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'python-dotenv>=0.17.1,<0.18.0',
 'requests>=2.25.1,<3.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['mtng = mtng.cli:cli']}

setup_kwargs = {
    'name': 'mtng',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Paul Gessinger',
    'author_email': 'hello@paulgessinger.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

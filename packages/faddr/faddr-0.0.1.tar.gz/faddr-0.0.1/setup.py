# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faddr']

package_data = \
{'': ['*']}

install_requires = \
['ciscoconfparse>=1.5.30,<2.0.0', 'tinydb>=4.4.0,<5.0.0']

extras_require = \
{':python_version >= "3.6.0" and python_version < "3.7.0"': ['dataclasses>=0.8,<0.9']}

entry_points = \
{'console_scripts': ['faddr-db = faddr.cli:faddr_db']}

setup_kwargs = {
    'name': 'faddr',
    'version': '0.0.1',
    'description': 'Tool to parse configuration of network devices such as Juniper routers and store gathered data in database',
    'long_description': '# FAddr\n\n![GitHub](https://img.shields.io/github/license/kido5217/faddr)\n![Codacy grade](https://img.shields.io/codacy/grade/0d75ea40d4f544438b4c892036132a04)\n![GitHub top language](https://img.shields.io/github/languages/top/kido5217/faddr)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/faddr)\n\nFAddr is a Python program for parsing configuration of network devices such as Juniper and Cisco routers and storing gathered data in database.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install faddr.\n\n```bash\npip install faddr\n```\n\n## Usage\n\nGenerate database:\n\n```bash\nfaddr-db -r [RANCID_DIR] -d [DATABASE LOCATION]\n```\n\nFind ip address termination point:\n\n```bash\nfaddr 10.20.30.1\n```\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Fedor Suchkov',
    'author_email': 'f.suchkov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kido5217/faddr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yami']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['aiohttp>=3.7.4.post0', 'hikari>=2.0.0.dev103']

setup_kwargs = {
    'name': 'yami',
    'version': '0.2.3',
    'description': 'A command handler that complements Hikari, a Discord API wrapper written in Python.',
    'long_description': '## Yami\n---\n[![CI](https://img.shields.io/github/workflow/status/Jonxslays/Yami/CI?label=Build&logo=github)](https://github.com/Jonxslays/Yami/actions/workflows/continuous-integration.yml)\n[![Python](https://img.shields.io/pypi/pyversions/yami?label=Python&logo=python)](https://github.com/Jonxslays/Yami/blob/master/LICENSE)\n[![License](https://img.shields.io/pypi/l/yami?label=License)](https://github.com/Jonxslays/Yami/blob/master/LICENSE)\n\n[![Latest Commit](https://img.shields.io/github/last-commit/jonxslays/yami?label=Latest%20Commit&logo=git)](https://github.com/Jonxslays/Yami)\n[![Maintained](https://img.shields.io/maintenance/yes/2021?label=Maintained)](https://github.com/Jonxslays/Yami)\n[![Latest Release](https://img.shields.io/pypi/v/yami?label=Latest%20Release&logo=pypi)](https://pypi.org/project/yami)\n\nStill in early development. Not ready for use.\n',
    'author': 'Jonxslays',
    'author_email': 'jon@jonxslays.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jonxslays/Yami',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['with_partial']

package_data = \
{'': ['*']}

install_requires = \
['addict>=2.4.0,<3.0.0']

extras_require = \
{'pipetools': ['pipetools>=1.0.1,<2.0.0']}

setup_kwargs = {
    'name': 'with-partial',
    'version': '0.1.0',
    'description': 'A utility for functional piping in Python that allows you to access any function in any scope as a partial.',
    'long_description': None,
    'author': 'Michael Milton',
    'author_email': 'michael.r.milton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)

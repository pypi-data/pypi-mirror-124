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
    'version': '1.0.1',
    'description': 'A utility for functional piping in Python that allows you to access any function in any scope as a partial.',
    'long_description': '# WithPartial\n## Introduction\n\nWithPartial is a simple utility for functional piping in Python.\nThe package exposes a context manager (used with `with`) called `PipeContext`, that allows you to access any function in any scope as a partial, meaning that it\'s naturally pipeable.\nHere\'s a contrived example from the test suite:\n\n```python\nimport numpy as np\nfrom with_partial import PartialContext\nfrom pipetools import pipe\n\nwith PartialContext() as _:\n    ret = (\n            10 > pipe |\n            _.np.ones() |\n            _.np.reshape(newshape=(5, 2)) |\n            _.np.mean() |\n            _.int()\n    )\n    assert ret == 1\n```\n\nAs you can see, we were able to call both `numpy` and built-in functions on the `_` object, and it executed the pipeline similarly to say R\'s `magrittr` package.\n\n## Installation\n```bash\npip install with_partial\n```\n\n## Usage\nActually WithPartial doesn\'t provide an actual piping mechanism, but it does add a useful syntax for use with pipes.\nFor the actual piping mechanism, I suggest that you try [pipetools](https://0101.github.io/pipetools/doc/index.html), which this package is actually tested against.\n\nWithPartial provides a single class: `PipeContext`.\nThe way you use `PipeContext` is by first using it as a context manager:\n```python\nwith PipeContext() as _:\n```\n\nThen, using the return value of the context manager, which we have named `_` (but you could call it anything), you access attributes and items (using `.attr` or `["key"]` or `[0]`) to locate the function you want and then you finally call it `()`, which will create the partial.\nYou can use positional and keyword arguments at this point if you need\n\nFor more usage information, refer to the [test suite](https://github.com/multimeric/WithPartial/tree/master/test).\n\n## Tests\n\nNote: you will need [poetry](https://python-poetry.org/docs/pyproject/) installed.\n\n```bash\ngit clone https://github.com/multimeric/WithPartial.git\ncd WithPartial\npoetry install --extras pipetools\npoetry run pytest test/\n```',
    'author': 'Michael Milton',
    'author_email': 'michael.r.milton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/multimeric/WithPartial',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)

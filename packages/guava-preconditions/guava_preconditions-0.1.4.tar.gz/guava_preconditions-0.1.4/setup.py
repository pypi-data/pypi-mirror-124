# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guava_preconditions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'guava-preconditions',
    'version': '0.1.4',
    'description': "A python version of guava's preconditions",
    'long_description': '# guava_preconditions\n\nThis library provides some simple functions from guava\n\n<!-- docs follow -->\n\n# Module guava_preconditions\n\n## Functions\n\n`checkArgument(expression: bool, errorMessageTemplate: Optional[str] = None, *errorMessageArgs: Any) ‑> None`\n: Ensures the truth of an expression involving one or more parameters to the calling method.\n\n`checkElementIndex(index: int, size: int, desc: str = None) ‑> int`\n: Ensures that index specifies a valid element in an array, list or string of size size.\n\n`checkNotNull(reference: Optional[~T], errorMessageTemplate: str, *errorMessageArgs: Any) ‑> ~T`\n: Ensures that an object reference passed as a parameter to the calling method is not null.\n\n`checkPositionIndex(index: int, size: int, desc: str = None) ‑> int`\n: Ensures that index specifies a valid position in an array, list or string of size size.\n\n`checkPositionIndexes(start: int, end: int, size: int) ‑> None`\n: Ensures that start and end specify a valid positions in an array, list or string of size size, and are in order.\n\n`checkState(expression: bool, errorMessageTemplate: str = None, *errorMessageArgs: Any) ‑> None`\n: Ensures the truth of an expression involving the state of the calling instance, but not involving any parameters to the calling method.\n\n## Classes\n\n`IllegalArgumentException(*args, **kwargs)`\n: Common base class for all non-exit exceptions.\n\n    ### Ancestors (in MRO)\n\n    * builtins.Exception\n    * builtins.BaseException\n\n`IllegalStateException(*args, **kwargs)`\n: Common base class for all non-exit exceptions.\n\n    ### Ancestors (in MRO)\n\n    * builtins.Exception\n    * builtins.BaseException\n',
    'author': 'Elliana',
    'author_email': 'me@mause.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Mause/guava_preconditions',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pravda']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pravda',
    'version': '0.0.0',
    'description': 'Python type-checker written in Rust',
    'long_description': '# pravda\n\n[![Build Status](https://github.com/wemake.services/pravda/workflows/test/badge.svg?branch=master&event=push)](https://github.com/wemake.services/pravda/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/wemake.services/pravda/branch/master/graph/badge.svg)](https://codecov.io/gh/wemake.services/pravda)\n[![Python Version](https://img.shields.io/pypi/pyversions/pravda.svg)](https://pypi.org/project/pravda/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nPython type-checker written in Rust\n\n\n## Features\n\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n- Add yours!\n\n\n## Installation\n\n```bash\npip install pravda\n```\n\n\n## Example\n\nShowcase how your project can be used:\n\n```python\nfrom pravda.example import some_function\n\nprint(some_function(3, 4))\n# => 7\n```\n\n## License\n\n[MIT](https://github.com/wemake.services/pravda/blob/master/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [5d436d64f7d0a9b3a506d130e3a5669c409061b5](https://github.com/wemake-services/wemake-python-package/tree/5d436d64f7d0a9b3a506d130e3a5669c409061b5). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/5d436d64f7d0a9b3a506d130e3a5669c409061b5...master) since then.\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wemake.services/pravda',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

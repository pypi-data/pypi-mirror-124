# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['codino', 'codino.data', 'codino.process']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'codino',
    'version': '0.1.0',
    'description': 'Calculating amino acid frequencies from codon design, and vice versa',
    'long_description': '# codino\n\nCalculating amino acid frequencies from codon design, and vice versa\n\n## Installation\n\n```bash\npip install codino\n```\n\n## Usage\n\n```python\nfrom codino.process import Converter\n\nc = Converter()\n\n# converting from codon design to AA frequencies\nc.cd_to_aa(first = {"A": 1}, second = {"T": 1}, third = {"G": 1})\n# Out: {\'M\': 1}\n\n# converting from AA frequency to codon design\nc.aa_to_cd(aa={\'M\': 1})\n# Out: ({\'A\': 1.0}, {\'T\': 1.0}, {\'G\': 1.0})\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`codino` was created by David Zhang. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`codino` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'David Zhang',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# codino

Calculating amino acid frequencies from codon design, and vice versa

## Installation

```bash
pip install codino
```

## Usage

```python
from codino.process import Converter

c = Converter()

# converting from codon design to AA frequencies
c.cd_to_aa(first = {"A": 1}, second = {"T": 1}, third = {"G": 1})
# Out: {'M': 1}

# converting from AA frequency to codon design
c.aa_to_cd(aa={'M': 1})
# Out: ({'A': 1.0}, {'T': 1.0}, {'G': 1.0})
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`codino` was created by David Zhang. It is licensed under the terms of the MIT license.

## Credits

`codino` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

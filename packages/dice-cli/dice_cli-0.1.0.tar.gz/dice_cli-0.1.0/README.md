# DICE Command Line Interface (CLI)

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]
[![Code style: black][black-badge]][black-link]

[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[actions-badge]:            https://github.com/uobdic/dice-cli/workflows/CI/badge.svg
[actions-link]:             https://github.com/uobdic/dice-cli/actions
[black-badge]:              https://img.shields.io/badge/code%20style-black-000000.svg
[black-link]:               https://github.com/psf/black
[pypi-link]:                https://pypi.org/project/dice-cli/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/dice-cli
[pypi-version]:             https://badge.fury.io/py/dice-cli.svg
[rtd-badge]:                https://readthedocs.org/projects/dice-cli/badge/?version=latest
[rtd-link]:                 https://dice-cli.readthedocs.io/en/latest/?badge=latest

## Installation

The best way to install `dice-cli` is via `pipx`.
This will setup a separate `virtualenv` for `dice-cli` preventing interference with your normal Python setup.

```bash
pipx install dice-cli
```

For tab-completion of the DICE CLI, you can run

```bash
dice --install-completion
```

which will install the completion for your shell.

Should you be using a "non-standard" shell, you can check what will be installed through

```bash
dice --show-completion
```

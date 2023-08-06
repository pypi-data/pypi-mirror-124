# pylint-aiida

[![PyPI version][pypi-badge]][pypi-link]

A small plugin for aiida-core related linting.

## Usage

```console
$ pip install pylint_aiida
```

Then add to your pylint configuration, e.g. in `pyproject.toml`:

```toml
[tool.pylint.master]
load-plugins = ["pylint_aiida"]
```

[pypi-badge]: https://img.shields.io/pypi/v/pylint_aiida.svg
[pypi-link]: https://pypi.org/project/pylint_aiida

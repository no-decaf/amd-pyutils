# Python Utils

![SemVer](https://img.shields.io/badge/SemVer-0.1.0-blue.svg)
![python](https://img.shields.io/badge/python-3.8-blue.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

A Python utility library.

## Scripts

`pfmt`

Format Python code by running [autoflake](https://github.com/myint/autoflake),
[isort](https://github.com/timothycrosley/isort), and
[Black](https://github.com/python/black), in that order. Autoflake removes unused and
uncecessary code, isort organizes imports, and Black runs last to apply a consistent
format.

`plint`

Lint Python code and docstrings by running [pydocstyle](https://github.com/PyCQA/pydocstyle)
for [PEP 257](https://www.python.org/dev/peps/pep-0257/) docstring compliance and
[pylint](https://github.com/PyCQA/pylint)
for [PEP 8](https://www.python.org/dev/peps/pep-0008/) code compliance. Both libraries
are maintained by the [Python Code Quality Authority](https://github.com/PyCQA).

`ptest`

Test code by running [pytest](https://github.com/pytest-dev/pytest) with the
[pytest-cov](https://github.com/pytest-dev/pytest-cov) plugin for code coverage. Uses
some intelligent defaults and an embedded `.coveragerc` file to ignore common Python
modules that do not need coverage.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/mashi/codecov-validator.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/mashi/codecov-validator/context:python)
[![codecov](https://codecov.io/gh/mashi/codecov-validator/branch/main/graph/badge.svg?token=WBOQOGFC51)](https://codecov.io/gh/mashi/codecov-validator)
[![github-actions](https://github.com/mashi/codecov-validator/actions/workflows/python.yml/badge.svg)](https://github.com/mashi/codecov-validator/actions)


# Description
Validates the `codecov.yml` configuration file.

This package is simply the `curl` command described in the [codecov documentation](https://docs.codecov.io/docs/codecov-yaml)
converted to python.

This package was inspired by [gitlab-lint](https://pypi.org/project/gitlab-lint/), package that checks `.gitlab-ci.yml`
configuration file.


## Usage
The recommended use is to add in the `.pre-commit-config.yaml` file
```
- repo: https://github.com/mashi/codecov-validator
  rev: v1.0.0  # replace by any tag version >= 1.0.0 available
  hooks:
    - id: ccv
      # args: [--filename, .codecov.yml]  # example with arguments
```

In this way, the `codecov.yml` file is checked before `commit` and prevents the user
from including invalid files in the version control.


## Instructions (Development)
Create a virtual environment and install the required packages with
```
python3 -m venv .venv
source .venv/bin/activate
pip install wheel
pip install -r requirements.txt
pre-commit install
```

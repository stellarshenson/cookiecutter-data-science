# Cookiecutter Data Science - Stellars' Fork

_A logical, reasonably standardized but flexible project structure for doing and sharing data science work._

[![tests](https://github.com/stellarshenson/cookiecutter-data-science/actions/workflows/tests.yml/badge.svg)](https://github.com/stellarshenson/cookiecutter-data-science/actions/workflows/tests.yml)
<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

This is **Stellars' fork** of Cookiecutter Data Science with enhanced features for data science workflows. See the [Philosophy Document](docs/docs/stellars-philosophy.md) for design principles.

**Key enhancements over upstream:**
- **uv default** - Modern, fast Python package manager as default
- **Local environments** - `.venv/` directory by default for project isolation
- **`lib_` prefix** - Clear module naming (`lib_myproject/` instead of `src/`)
- **Dev/prod separation** - Development tools separate from production dependencies
- **Zero boilerplate** - Jupyter kernel, linting, testing pre-configured
- **Environment checks** - No recreating existing environments
- **Model sync** - `sync_models_up/down` targets for cloud storage

> [!NOTE]
> This fork works with the standard `ccds` CLI from PyPI. Install it with `pipx install cookiecutter-data-science`.

## Installation

Cookiecutter Data Science v2 requires Python 3.9+. Since this is a cross-project utility application, we recommend installing it with [pipx](https://pypa.github.io/pipx/). Installation command options:

```bash
# With pipx from PyPI (recommended)
pipx install cookiecutter-data-science

# With pip from PyPI
pip install cookiecutter-data-science

# With conda from conda-forge (coming soon)
# conda install cookiecutter-data-science -c conda-forge
```

## Starting a new project

To start a new project with this fork:

```bash
ccds gh:stellarshenson/cookiecutter-data-science
```

Then follow the prompts, and once created:

```bash
cd my_project
make install   # Creates environment, installs dev tools and module
```

### The resulting directory structure

The directory structure of your new project will look something like this (depending on the settings that you choose):

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make install` or `make test`
├── README.md          <- The top-level README for developers using this project
├── pyproject.toml     <- Project configuration with package metadata and dev dependencies
│
├── data
│   ├── external       <- Data from third party sources
│   ├── interim        <- Intermediate data that has been transformed
│   ├── processed      <- The final, canonical data sets for modeling
│   └── raw            <- The original, immutable data dump
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
├── models             <- Trained and serialized models, model predictions, or model summaries
├── notebooks          <- Jupyter notebooks (naming: `01-initials-description.ipynb`)
├── references         <- Data dictionaries, manuals, and all other explanatory materials
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── environment.yml    <- conda only: development dependencies
├── requirements-dev.txt <- virtualenv only: development dependencies
│
└── lib_<project_name>/  <- Source code module (installable with pip install -e .)
    ├── __init__.py
    ├── config.py        <- Store useful variables and configuration
    ├── dataset.py       <- Scripts to download or generate data
    ├── features.py      <- Code to create features for modeling
    ├── plots.py         <- Code to create visualizations
    └── modeling/
        ├── __init__.py
        ├── predict.py   <- Code to run model inference with trained models
        └── train.py     <- Code to train models
```

## Using a specific branch

To use a specific branch of this fork:

```bash
ccds gh:stellarshenson/cookiecutter-data-science --checkout master
```

## Upstream

This fork is based on [DrivenData's Cookiecutter Data Science](https://github.com/drivendataorg/cookiecutter-data-science). See the [upstream documentation](https://cookiecutter-data-science.drivendata.org/) for the original project.

## Contributing

Contributions welcome! Fork, make changes, and submit a PR.

### Running the tests

```bash
pip install -r dev-requirements.txt
SKIP_GITHUB_TESTS=1 pytest tests -v
```

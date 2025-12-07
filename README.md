# Cookiecutter Data Science - Stellars' Fork

_A logical, reasonably standardized but flexible project structure for doing and sharing data science work._

[![tests](https://github.com/stellarshenson/cookiecutter-data-science/actions/workflows/tests.yml/badge.svg)](https://github.com/stellarshenson/cookiecutter-data-science/actions/workflows/tests.yml)
<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

This is **Stellars' fork** of Cookiecutter Data Science with enhanced features for data science workflows. See the [Philosophy Document](docs/docs/stellars-philosophy.md) for design principles.

## Key Features

| Feature | Upstream ccds | Stellars' Fork |
|---------|--------------|----------------|
| Module naming | `<project_name>` | `lib_<project_name>` |
| Environment managers | 6 (virtualenv, conda, pipenv, uv, pixi, poetry) | 3 (uv, conda, virtualenv) |
| Default env manager | virtualenv | uv |
| Dependency files | 5 (requirements.txt, pyproject.toml, environment.yml, Pipfile, pixi.toml) | 3 (pyproject.toml, requirements.txt, environment.yml) |
| Default Python | 3.10 | 3.12 |
| Conda env location | Global only | Local by default, global optional |
| Dev dependencies | Mixed with production | Separated |
| Jupyter kernel | Manual setup | Auto-registered with cleanup |
| Environment exists check | No | Yes |
| Cloud storage config | Inline in commands | Makefile variables |
| Model sync targets | No | Yes (`sync_models_up/down`) |
| virtualenv implementation | virtualenvwrapper | Standard venv |
| .env encryption | No | Optional (OpenSSL AES-256) |
| Build versioning | No | Auto-increment on `make build` |
| Docker support | No | Optional (Dockerfile + Makefile targets) |
| Copier support | No | Yes (parallel template) |

**Key enhancements:**
- **uv default** - Modern, fast Python package manager
- **Local environments** - `.venv/` directory for project isolation
- **`lib_` prefix** - Clear module naming (`lib_myproject/`)
- **Dev/prod separation** - Development tools separate from production dependencies
- **Zero boilerplate** - Jupyter kernel, linting, testing pre-configured
- **Environment checks** - Skip creation if environment exists
- **Model sync** - `sync_models_up/down` targets for cloud storage
- **.env encryption** - Optional AES-256 encryption for secrets (`make .env.enc`)
- **Build versioning** - Auto-increment build number in pyproject.toml on `make build`
- **Docker support** - Optional Dockerfile and Makefile targets (`docker_build`, `docker_run`, `docker_push`)
- **Copier support** - Alternative to cookiecutter with template update support

This template uses [nb_venv_kernels](https://github.com/stellarshenson/nb_venv_kernels) for automatic Jupyter kernel management - your project environments appear as kernels in JupyterLab without manual registration. For conda environments, [nb_conda_kernels](https://github.com/Anaconda-Platform/nb_conda_kernels) is used instead. Both provide automatic kernel discovery and cleanup when environments are removed.

> [!NOTE]
> This fork works with the standard `ccds` CLI from PyPI. Install it with `pipx install cookiecutter-data-science`.

## Installation

Requires Python 3.9+. We recommend installing with [pipx](https://pypa.github.io/pipx/):

```bash
# Cookiecutter (ccds command)
pipx install cookiecutter-data-science

# Copier (alternative with template update support)
pipx install copier
```

## Starting a new project

```bash
# Using Cookiecutter
ccds gh:stellarshenson/cookiecutter-data-science

# Using Copier (supports template updates)
copier copy --trust https://github.com/stellarshenson/cookiecutter-data-science.git my-project
```

See [Copier Support](docs/docs/copier-support.md) for Copier details. Then follow the prompts, and once created:

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

This fork stands on the shoulders of [DrivenData's giants](https://github.com/drivendataorg/cookiecutter-data-science) - peeping over their shoulder at the excellent work they've done, then adding some opinionated tweaks while they do the heavy lifting. See the [upstream documentation](https://cookiecutter-data-science.drivendata.org/) for the original project.

## Contributing

Contributions welcome! Fork, make changes, and submit a PR.

### Template Architecture

This project maintains two template formats:

- **`{{ cookiecutter.repo_name }}/`** - Master template (cookiecutter syntax)
- **`copier/template/`** - Derived template (copier syntax, auto-generated)

**Before pushing changes**, sync the copier template:

```bash
python copier/scripts/build_copier_template.py
```

This transforms cookiecutter syntax (`{{ cookiecutter.var }}`) to copier syntax (`{{ var }}`).

### Running the tests

```bash
pip install -r dev-requirements.txt
SKIP_GITHUB_TESTS=1 pytest tests -v
```

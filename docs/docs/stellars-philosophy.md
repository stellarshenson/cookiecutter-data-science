# Stellars' Cookiecutter Data Science Philosophy

This fork emphasizes **simplicity**, **separation of concerns**, and **minimal boilerplate**.

## Guiding Philosophy

**Promote best practices, not proliferate outdated ones.**

- **Adopt modern tooling** - uv over pip, ruff over flake8+black+isort
- **Simplify choices** - 4 environment managers instead of 7, focus on what works well
- **Separate dev from production** - clear dependency boundaries
- **Zero post-scaffold configuration** - Jupyter kernels, linting, testing all pre-configured

## Core Principles

### 1. Dev vs Production Dependencies

**Upstream**: All dependencies in one file, no separation.

**This fork**: Strict separation based on dependency file choice:

| Dependency File | Production | Development |
|-----------------|------------|-------------|
| `pyproject.toml` | `[project.dependencies]` | `[project.optional-dependencies.dev]` |
| `requirements.txt` | `requirements.txt` | `requirements-dev.txt` |
| `environment.yml` | conda packages | conda packages (all in one, conda-native) |

### 2. Installable Module with `lib_` Prefix

**Upstream**: Module named `<project_name>` (e.g., `my_project`).

**This fork**: Module named `lib_<project_name>` (e.g., `lib_my_project`).

This avoids conflicts with common package names and makes project code immediately recognizable.

### 3. Local Environment by Default

**Upstream**: Conda environments always global. Virtualenv uses virtualenvwrapper.

**This fork**:
- Conda: local `.venv/<env_name>/` by default, global optional
- uv/virtualenv: local `.venv/` using standard venv (no virtualenvwrapper)

### 4. Jupyter Kernel Auto-Registration

**Upstream**: No kernel registration - manual setup required.

**This fork**: Kernels auto-registered during `make create_environment`:
- Uses nb_conda_kernels/nb_venv_kernels when available
- Falls back to ipykernel with consistent naming: `Python [conda|uv|venv env:<name>]`
- Kernels cleaned up on `make remove_environment`

### 5. Environment Existence Checks

**Upstream**: `make create_environment` always tries to create, may fail or recreate.

**This fork**: Checks if environment exists first, skips creation if present.

## Key Differences from Upstream

| Feature | Upstream ccds | Stellars' Fork |
|---------|--------------|----------------|
| Module naming | `<project_name>` | `lib_<project_name>` |
| Environment managers | 7 (virtualenv, conda, pipenv, uv, pixi, poetry, none) | 4 (uv, conda, virtualenv, none) |
| Default env manager | virtualenv | uv |
| Dependency files | 5 (requirements.txt, pyproject.toml, environment.yml, Pipfile, pixi.toml) | 3 (pyproject.toml, requirements.txt, environment.yml) |
| Default Python | 3.10 | 3.12 |
| Conda env location | Global only | Local by default, global optional |
| Dev dependencies | Mixed with production | Separated |
| Jupyter kernel | Manual setup | Auto-registered with cleanup |
| Environment exists check | No | Yes |
| Cloud storage config | Inline in commands | Makefile variables |
| virtualenv implementation | virtualenvwrapper | Standard venv |

## When to Use What

| Scenario | Recommended |
|----------|-------------|
| Data science with conda packages | conda |
| Pure Python, fast setup | uv |
| Traditional Python | virtualenv |

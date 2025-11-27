# Environment Management Reference

This document describes how dependencies, dev dependencies, and Jupyter kernels are managed across different environment manager and dependency file combinations.

## Dependency Matrix

| Env Type | Dependencies File | Dev Dependencies | Env File | Automated Kernel Discovery | Manual Kernel Discovery |
|----------|------------------|------------------|----------|------------------------|---------------------|
| conda / requirements.txt | requirements.txt | requirements-dev.txt | environment.yml | conda via nb_conda_kernels | ipykernel install uninstall |
| conda / pyproject.toml | pyproject.toml dependencies | pyproject.toml dev dependencies | environment.yml | conda via nb_conda_kernels | ipykernel install uninstall |
| uv / requirements.txt | requirements.txt | requirements-dev.txt | n/a | nb_venv_kernels register unregister | ipykernel install uninstall |
| uv / pyproject.toml | pyproject.toml dependencies | pyproject.toml dev dependencies | n/a | nb_venv_kernels register unregister | ipykernel install uninstall |
| venv / requirements.txt | requirements.txt | requirements-dev.txt | n/a | nb_venv_kernels register unregister | ipykernel install uninstall |
| venv / pyproject.toml | pyproject.toml dependencies | pyproject.toml dev dependencies | n/a | nb_venv_kernels register unregister| ipykernel install uninstall |

## Key Points

**Dependencies**:
- `requirements.txt` - uses separate `requirements-dev.txt` for dev dependencies
- `pyproject.toml` - uses `[project.optional-dependencies.dev]` section for dev dependencies

**Environment Files**:
- Conda always creates `environment.yml` (minimal - just python and pip)
- uv and virtualenv do not use environment files

**Jupyter Kernel Registration**:
- Conda environments are auto-discovered by `nb_conda_kernels` if installed in base
- Virtual environments (uv, venv) use `nb_venv_kernels` for registration
- Fallback for all: manual `ipykernel install --user --name=ENV_NAME`

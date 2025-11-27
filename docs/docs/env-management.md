# Environment Management Reference

This document describes how dependencies, dev dependencies, and Jupyter kernels are managed across different environment manager and dependency file combinations.

## Dependency Matrix
| Env Type | requirements.txt | requirements-dev.txt | pyproject.toml | environment.yml | Auto Kernel Discovery | Manual Kernel Discovery |
|----------|------------------|----------------------|----------------|-----------------|-----------------------|-------------------------|
| conda / requirements.txt    | ✅ | ✅ | ❌ | ✅, minimal | conda / nb_conda_kernels | ipykernel / install uninstall |
| conda / pyproject.toml      | ❌  | ❌  | ✅, prod and dev | ✅, minimal | conda / nb_conda_kernels | ipykernel / install uninstall |
| uv / requirements.txt       | ✅ | ✅ | ❌ | ❌ | nb_venv_kernels register unregister | ipykernel install uninstall |
| uv / pyproject.toml         | ❌  | ❌  | ✅, prod and dev | ❌ | nb_venv_kernels register unregister | ipykernel install uninstall |
| venv / requirements.txt     | ✅ | ✅ | ❌ | ❌ | nb_venv_kernels register unregister | ipykernel install uninstall |
| venv / pyproject.toml       | ❌  | ❌  | ✅, prod and dev | ❌ | nb_venv_kernels register unregister| ipykernel install uninstall |


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

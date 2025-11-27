# Environment Management Reference

This document describes how dependencies, dev dependencies, and Jupyter kernels are managed across different environment manager and dependency file combinations.

## Dependency Matrix

| Env Type | requirements.txt | requirements-dev.txt | pyproject.toml | environment.yml | Auto Kernel Discovery | Manual Kernel Discovery |
|----------|------------------|----------------------|----------------|-----------------|-----------------------|-------------------------|
| conda / requirements.txt    | ✅ | ✅ | ✅ only metadata | ❌ | conda / nb_conda_kernels | ipykernel / install uninstall |
| conda / pyproject.toml      | ❌  | ❌  | ✅ prod and dev | ❌ | conda / nb_conda_kernels | ipykernel / install uninstall |
| conda / environment.yml      | ❌  | ❌  | ✅ prod | ✅ dev | conda / nb_conda_kernels | ipykernel / install uninstall |
| uv / requirements.txt       | ✅ | ✅ | ✅ only metadata | ❌ | nb_venv_kernels register unregister | ipykernel install uninstall |
| uv / pyproject.toml         | ❌  | ❌  | ✅ prod and dev | ❌ | nb_venv_kernels register unregister | ipykernel install uninstall |
| venv / requirements.txt     | ✅ | ✅ | ✅ only metadata | ❌ | nb_venv_kernels register unregister | ipykernel install uninstall |
| venv / pyproject.toml       | ❌  | ❌  | ✅ prod and dev | ❌ | nb_venv_kernels register unregister| ipykernel install uninstall |


## Key Points

**pyproject.toml**:
- Always present for project metadata, build configuration, and tool settings (ruff, black, isort, pytest)
- Contains dependencies section only when `dependency_file = pyproject.toml`

**Dependencies**:
- `requirements.txt` - uses separate `requirements-dev.txt` for dev dependencies
- `pyproject.toml` - uses `[project.optional-dependencies.dev]` section for dev dependencies
- `environment.yml` - conda-native dev dependencies (when selected as dependency file)

**Environment Files**:
- `environment.yml` only created when `dependency_file = environment.yml` (conda only)
- uv and virtualenv do not use environment files

**Jupyter Kernel Registration**:
- Conda environments are auto-discovered by `nb_conda_kernels` if installed in base
- Virtual environments (uv, venv) use `nb_venv_kernels` for registration
- Fallback for all: manual `ipykernel install --user --name=ENV_NAME`

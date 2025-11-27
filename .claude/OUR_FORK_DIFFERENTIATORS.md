# Our Cookiecutter Fork - Key Differentiators

This document captures the unique features of our fork that should be preserved when integrating with upstream ccds v2.

---

## 1. cookiecutter.json - Custom Variables

| Variable | Our Value | Upstream v2 | Notes |
|----------|-----------|-------------|-------|
| `env_name` | `{{ cookiecutter.project_name.lower().replace(' ', '_') }}` | Not present | Separate env name from repo name |
| `module_name` | `{{ 'lib_' + cookiecutter.repo_name.replace('-', '_') }}` | `{{ cookiecutter.project_name... }}` | **lib_ prefix** distinguishes module from project |
| `env_location` | `["local", "global"]` | Not present | **Local vs global conda env choice** |
| `python_version` | `"3.12"` | `"3.10"` | Newer Python default |

## 2. Makefile - Rich Output & Colored Messages

**Color scheme for user feedback:**
```makefile
MSG_PREFIX = \033[1m\033[36m>>>\033[0m      # Cyan bold for info
WARN_PREFIX = \033[33m>>>\033[0m            # Yellow for warnings
ERR_PREFIX = \033[31m>>>\033[0m             # Red for errors
WARN_STYLE = \033[33m
ERR_STYLE = \033[31m
HIGHLIGHT_STYLE = \033[1m\033[94m           # Bold blue for highlights
OK_STYLE = \033[92m                          # Green for success
NO_STYLE = \033[0m
```

Upstream v2 has no colored output.

## 3. Local vs Global Conda Environment

**Our Implementation:**
```makefile
ENV_LOCATION = {{ cookiecutter.env_location }}
CONDA_ENV_PATH = $(PROJECT_DIR)/.venv/$(CONDA_ENV_NAME)

ifeq ($(ENV_LOCATION),local)
CONDA_ENV_SELECTOR = -p $(CONDA_ENV_PATH)
else
CONDA_ENV_SELECTOR = --name $(CONDA_ENV_NAME)
endif
```

- **Local**: Creates env at `.venv/<env_name>/` using `conda -p`
- **Global**: Creates named env using `conda --name`
- All conda commands use `${CONDA_ENV_SELECTOR}` for flexibility

**Upstream v2**: Only supports global conda envs or virtualenv/pipenv/uv/poetry.

## 4. Environment Management Targets

| Target | Our Fork | Upstream v2 |
|--------|----------|-------------|
| `create_environment` | Full featured with checks, nbdime setup | Basic or missing |
| `remove_environment` | Supports both local/global | Not present |
| `test_environment` | Validates env exists, shows Python version | Basic check |
| `check_conda` | Error handling with colored output | Not present |

**Our create_environment features:**
- Checks if env already exists (skips if so)
- Creates with `environment.yml`
- Configures nbdime for git-jupyter integration
- Rich output with activation instructions

## 5. Package Build System

| Target | Description |
|--------|-------------|
| `install` | Creates env + installs package editable |
| `build` | Full build: install -> test -> increment version -> build wheel |
| `increment_build_number` | Auto-increments version in pyproject.toml |

**Upstream v2**: No build targets, no version management.

## 6. environment.yml - Development Dependencies

Our template includes pre-configured dev dependencies:
```yaml
dependencies:
  - python={{ cookiecutter.python_version }}
  - pip
  - pip:
    - build           # wheel building
    - ipykernel       # Jupyter kernel support
    - IPython
    - nbdime          # git-jupyter integration
    - pytest
    - pytest-cov
    - toml            # version management
```

**Upstream v2**: Uses requirements.txt or pyproject.toml with minimal deps.

## 7. pyproject.toml - Modern Packaging

- `build-system` with setuptools
- Runtime dependencies: loguru, python-dotenv, typer, tqdm
- Proper `packages.find` with exclude for tests
- `include-package-data = true`

## 8. Test Infrastructure

- Tests at project root `./tests/` (v2 aligned)
- pytest with coverage (`pytest --cov`)
- Pre-flight check for test existence before running
- Sample test file demonstrating pytest patterns

## 9. S3 Sync Targets

| Target | Description |
|--------|-------------|
| `sync_data_up` | Upload data/ to S3 |
| `sync_data_down` | Download data/ from S3 |
| `sync` | Full sync: models/ + artifacts/ |

With AWS profile support.

## 10. Help System

Simplified Python-based help with:
- Sorted targets alphabetically
- Cyan-colored target names
- Clean regex-based parsing

---

## Integration Strategy

When merging with upstream v2:

1. **Keep our conda-focused approach** - v2 supports multiple env managers, we can integrate as conda option
2. **Preserve colored output** - Add to v2's Makefile template
3. **Keep local/global env choice** - Unique to our fork
4. **Keep lib_ prefix** - Distinguishes installable package from project
5. **Keep build targets** - Essential for package development workflow
6. **Keep environment.yml** - Pre-configured dev environment
7. **Adopt v2 structure** where it makes sense (tests at root, etc.)

## Files to Preserve/Merge

| File | Action |
|------|--------|
| `cookiecutter.json` | Merge our vars into v2 structure |
| `Makefile` | Keep our targets, adopt v2 conditionals if needed |
| `environment.yml` | Keep as conda option |
| `pyproject.toml` | Keep our structure |
| `.gitignore` | Merge patterns |
| Module structure | Keep lib_ prefix option |

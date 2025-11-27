# Stellars' Cookiecutter Data Science Philosophy

This fork of cookiecutter-data-science emphasizes **simplicity**, **separation of concerns**, and **minimal boilerplate** for data science projects.

## Guiding Philosophy

**Promote best practices, not proliferate outdated ones.**

Project templates shape how thousands of developers work. A cookiecutter template isn't just scaffolding - it's an opinionated statement about how projects should be structured. We have a responsibility to:

- **Adopt modern tooling** - Use uv over pip where appropriate, ruff over flake8+black+isort
- **Deprecate legacy patterns** - Remove virtualenvwrapper support, drop outdated Python versions
- **Simplify where possible** - One way to do things well, not five ways to do them poorly
- **Keep dependencies minimal** - Separate dev from production, don't ship testing frameworks

Every choice in this template should answer: "Is this how we'd recommend someone start a new project today?"

## Core Principles

### 1. Lightweight Production, Comprehensive Development

**Problem**: Traditional project scaffolds mix development tools with production dependencies, resulting in bloated deployments and unclear dependency boundaries.

**Solution**: Strict separation between:
- **Production dependencies** (`pyproject.toml` dependencies) - Only what your module needs to run
- **Development dependencies** (`[project.optional-dependencies.dev]` or `requirements-dev.txt`) - Tools for development, testing, linting

This enables:
- Lightweight Docker images for production (`pip install .`)
- Full development environment (`pip install -e ".[dev]"`)
- Clear understanding of what ships vs what develops

### 2. Fewer Environment Managers, Done Right

**Problem**: Supporting many environment managers (conda, virtualenv, uv, pipenv, poetry, pixi) leads to inconsistent behavior, edge cases, and maintenance burden.

**Solution**: Focus on well-tested, complete support for:
- **conda** - Full-featured with local/global environments, environment.yml for dev dependencies
- **uv** - Modern, fast Python package manager
- **virtualenv** - Standard Python virtual environments

Each supported manager has:
- Environment existence checks (no recreating existing envs)
- Proper Jupyter kernel registration and cleanup
- Consistent Makefile targets across managers

### 3. Zero Boilerplate After Scaffold

**Problem**: Many project templates require significant manual configuration after creation - setting up linters, configuring tests, registering kernels.

**Solution**: Projects are immediately usable:
```bash
ccds gh:stellarshenson/cookiecutter-data-science
cd my_project
make install
# Ready to work
```

No post-scaffold configuration needed:
- Jupyter kernel auto-registered during environment creation
- Linting and formatting pre-configured (ruff or flake8+black+isort)
- Test framework ready (pytest with coverage)
- Git-Jupyter integration via nbdime

### 4. Installable Module with `lib_` Prefix

**Problem**: Project code often lives in ambiguously named directories, leading to import conflicts and unclear package boundaries.

**Solution**: All project code lives in `lib_<project_name>/`:
- Clear distinction: `lib_myproject` is your installable module
- Avoids conflicts with common package names
- Immediately recognizable as project-specific code
- Installable in editable mode: `pip install -e .`

> [!NOTE]
> You can rename the module folder to anything you prefer. The `lib_` prefix just makes it easy to spot your project code at a glance.


### 5. Development Dependencies Strategy

Dev dependencies location is determined by **dependency file choice**, not environment manager. This simplifies the mental model:

| Dependency File | Dev Dependencies |
|-----------------|------------------|
| `pyproject.toml` | `[project.optional-dependencies.dev]` |
| `requirements.txt` | `requirements-dev.txt` |

#### When using pyproject.toml:
Development tools are in `pyproject.toml` under `[project.optional-dependencies]`:
```toml
[project.optional-dependencies]
dev = [
    "ipykernel",
    "pytest",
    "pytest-cov",
    "ruff",
    ...
]
```

Installed with:
- conda: `pip install -e ".[dev]"`
- uv: `uv pip install -e ".[dev]"`
- virtualenv: `pip install -e ".[dev]"`

#### When using requirements.txt:
Development tools are in `requirements-dev.txt`:
```
ipykernel
pytest
pytest-cov
ruff
...
```

Installed with:
- conda: `pip install -r requirements-dev.txt`
- uv: `uv pip install -r requirements-dev.txt`
- virtualenv: `pip install -r requirements-dev.txt`

This keeps production dependencies clean while providing consistent behavior across all environment managers.

### 6. Local Environment by Default

**Problem**: Global conda environments pollute the base environment and can conflict across projects.

**Solution**: Local `.venv/` directory by default:
- Conda: `.venv/<env_name>/` for local environments
- uv/virtualenv: `.venv/`
- Easy cleanup: `rm -rf .venv`
- Clear project isolation

Global conda environments remain available for shared tooling.

## Key Differentiators from Upstream ccds

| Feature | Upstream ccds | Stellars' Fork |
|---------|--------------|----------------|
| Module prefix | `src/` | `lib_<project>/` |
| Environment location | Global only | Local by default |
| Dev dependencies | Mixed | Separated |
| Jupyter kernel | Manual setup | Auto-registered |
| Environment exists check | No | Yes |
| Kernel cleanup on remove | No | Yes |
| Default env manager | conda | uv |
| Default Python | 3.10 | 3.12 |

## Usage Philosophy

1. **Start simple** - Use defaults, they're sensible
2. **Iterate fast** - `make install` creates environment with dev tools and installs your module
3. **Deploy clean** - Production image only has what it needs (`pip install .`)
4. **Develop fully** - Development environment has all tools pre-configured

## When to Use What

| Scenario | Recommended Manager |
|----------|-------------------|
| Data science with conda packages | conda |
| Pure Python, modern tooling | uv |
| Traditional Python development | virtualenv |
| Maximum compatibility | virtualenv |
| Fastest environment creation | uv |

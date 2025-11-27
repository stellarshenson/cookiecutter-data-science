# Stellar's Cookiecutter Data Science Philosophy

This fork of cookiecutter-data-science emphasizes **simplicity**, **separation of concerns**, and **minimal boilerplate** for data science projects.

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
make create_environment
make requirements
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

### 5. Development Dependencies Strategy

#### For conda projects:
Development tools are managed in `environment.yml`:
- ipykernel (Jupyter kernel support)
- pytest, pytest-cov (testing)
- ruff or flake8+black+isort (linting/formatting)
- nbdime (Git-Jupyter integration)
- build, toml (packaging utilities)

This keeps `pyproject.toml` clean with only production dependencies.

#### For uv/virtualenv projects:
Development tools are in `[project.optional-dependencies]`:
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

Install with: `pip install -e ".[dev]"` or `uv pip install -e ".[dev]"`

### 6. Local Environment by Default

**Problem**: Global conda environments pollute the base environment and can conflict across projects.

**Solution**: Local `.venv/` directory by default:
- Conda: `.venv/<env_name>/` for local environments
- uv/virtualenv: `.venv/`
- Easy cleanup: `rm -rf .venv`
- Clear project isolation

Global conda environments remain available for shared tooling.

## Key Differentiators from Upstream ccds

| Feature | Upstream ccds | Stellar's Fork |
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
2. **Iterate fast** - `make create_environment && make requirements` gets you working
3. **Deploy clean** - Production image only has what it needs
4. **Develop fully** - Development environment has everything

## When to Use What

| Scenario | Recommended Manager |
|----------|-------------------|
| Data science with conda packages | conda |
| Pure Python, modern tooling | uv |
| Traditional Python development | virtualenv |
| Maximum compatibility | virtualenv |
| Fastest environment creation | uv |

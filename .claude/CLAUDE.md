<!-- Import workspace-level CLAUDE.md configuration -->
<!-- See /home/lab/workspace/.claude/CLAUDE.md for complete rules -->

# Project-Specific Configuration

This file extends workspace-level configuration with project-specific rules.

## Project Context

**Purpose**: Cookiecutter Data Science fork with enhanced features for conda-based data science workflows

**Key differentiators from upstream ccds**:
- Local vs global conda environment choice (`env_location`)
- `lib_` module prefix for installable packages
- Rich colored terminal output in Makefile
- environment.yml with pre-configured dev dependencies
- Build and version management targets
- Jupyter kernel auto-registration with nb_venv_kernels/nb_conda_kernels fallback

## Technology Stack

- Cookiecutter templating with Jinja2
- Conda/virtualenv/uv environment management
- pytest for testing
- ruff or flake8+black+isort for linting

## Testing

Run tests with parallel execution:
```bash
pytest tests/ -n 4 -v
```

Fast mode for quick iteration:
```bash
pytest tests/ -F
```

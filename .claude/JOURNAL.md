# Claude Code Journal

This journal tracks substantive work on documents, diagrams, and documentation content.

---

1. **Task - Port fork to ccds v2**: Integrated our cookiecutter-data-science fork differentiators with upstream ccds v2. Key features ported: local/global conda env choice, lib_ module prefix, colored Makefile output, environment.yml template, build/version targets<br>
   **Result**: Fork successfully rebased on ccds v2 with all differentiators preserved

2. **Task - Fix pytest test failures**: Ran pytest test suite with parallel execution, fixed multiple test failures including .ipynb_checkpoints exclusion, dependencies.py KeyAlreadyPresent error, environment.yml generation, Makefile tab indentation with Jinja2, virtualenv fallback to standard venv, and conda env_name conflicts<br>
   **Result**: All 24 tests pass with 4 parallel workers

3. **Task - Add Jupyter kernel support**: Implemented `jupyter_kernel` cookiecutter option with auto-registration during `create_environment`. For conda: tries nb_venv_kernels -> nb_conda_kernels -> ipykernel install. For venv/uv: tries nb_venv_kernels -> ipykernel install<br>
   **Result**: Added to ccds.json, environment.yml, Makefile, post_gen_project.py, conftest.py, and integration-tests.yml. All 24 tests pass

4. **Task - Add test teardown for environment cleanup**: Added Jupyter kernel cleanup to test harness scripts (conda_harness.sh, virtualenv_harness.sh, uv_harness.sh) to remove registered kernels from ~/.local/share/jupyter/kernels/ after tests complete<br>
   **Result**: Test harnesses now clean up both environments and Jupyter kernels. All 24 tests pass

5. **Task - Fix CI workflow and linting**: Changed integration-tests.yml to install ccds from local checkout (`pip install -e .`) instead of PyPI (which was installing upstream without KeyAlreadyPresent fix). Also formatted test files with black to pass lint checks<br>
   **Result**: CI workflow now uses fork code. Lint passes. All 24 tests pass

6. **Task - Refactor ccds config defaults**: Changed default dependency_file to pyproject.toml (removed environment.yml from choices since it's auto-created for conda). Renamed `jupyter_kernel` to `jupyter_kernel_support`. Kept `env_location` as top-level field (global only applies to conda, enforced via test filtering). Simplified CI workflow to use defaults<br>
   **Result**: All 20 tests pass. pyproject.toml is now default. jupyter_kernel_support renamed throughout

7. **Task - Align with upstream CI/CD workflows**: Updated tests.yml to match upstream (use `make docs` instead of direct mkdocs command). Updated generate-termynal.py with correct prompt sequence matching fork options. Updated ccds-help.json with all new/changed fields (env_name, env_location, jupyter_kernel_support, custom_config)<br>
   **Result**: tests.yml aligned with upstream. Docs scripts updated for termynal generation. All 20 tests pass

8. **Task - Make template standalone and uv default**: Inlined all ccds.hook_utils code into post_gen_project.py so template works with stock ccds CLI without depending on ccds package internals. Made uv the default environment manager. Updated generate-termynal.py to point to stellarshenson fork<br>
   **Result**: Template is now self-contained. uv is default. All 20 tests pass. Stock ccds CLI should work

9. **Task - Clean up dependencies and add missing targets**: Removed pip, ipykernel, jupyterlab, notebook from pyproject.toml dependencies (these are env tools not project deps). ipykernel now installed during create_environment. Added install/remove_environment targets for uv/virtualenv. remove_environment also unregisters Jupyter kernel. Made Python 3.12 default. Updated integration tests to explicitly set environment_manager<br>
   **Result**: Dependencies are now minimal. All environment managers have parity for install/remove targets. All 20 tests pass

10. **Task - Fix CI Python version mismatch**: CI uses Python 3.10 but project defaults to 3.12. Added python_version_number="3.10" to all 5 CI test jobs. Fixed YAML syntax errors from broken sed command (missing backslash continuations)<br>
   **Result**: integration-tests.yml fixed. All 20 local tests pass

11. **Task - Separate dev vs production dependencies**: Kept environment.yml for all conda projects (regardless of dependency_file) to hold dev dependencies (ipykernel, pytest, nbdime, etc.). This keeps pyproject.toml clean with only module dependencies. environment.yml is deleted for non-conda managers. Fixed Jinja whitespace issues causing Makefile syntax errors. Silenced verbose uv output. Added test expectation for environment.yml in conda projects<br>
   **Result**: Dev/prod dependency separation complete. All 20 tests pass

12. **Task - Add GitHub checkout tests**: Created tests/test_github_checkout.py with automated tests for using ccds with GitHub repo and --checkout master for conda, uv, and virtualenv environment managers. Tests verify project structure, lib_ prefix, and Makefile syntax<br>
   **Result**: New test file added for validating GitHub checkout workflow

13. **Task - Implement dev dependencies per environment manager**: Added per-manager dev dependencies system. Conda uses environment.yml, uv uses pyproject.toml `[project.optional-dependencies.dev]`, virtualenv uses requirements-dev.txt. Dev dependencies installed automatically during `make create_environment`. Updated philosophy doc and README to reflect fork features and point to philosophy document<br>
   **Result**: Complete dev dependencies separation. All 20 tests pass. README and philosophy doc updated

14. **Task - Documentation cleanup and lint fixes**: Moved STELLARS_CCDS_PHILOSOPHY.md to repo root. Updated naming from "Stellar's" to "Stellars'" throughout. Fixed black formatting in test_github_checkout.py. Updated README link to philosophy doc<br>
   **Result**: All 20 tests pass. Lint passes. Documentation properly organized

15. **Task - Fix uv dev dependencies and template cleanup**: Moved pip to dev dependencies in pyproject.toml (removed redundant install). Fixed Jinja whitespace in pyproject.toml template. Critical fix: `uv sync` now uses `--extra dev` to preserve dev dependencies - without this, `make requirements` was uninstalling ipykernel and other dev tools<br>
   **Result**: Dev dependencies preserved across make targets. Kernelspec creation works correctly

16. **Task - Simplify CI and add upgrade targets**: Removed pixi, poetry, pipenv from tests.yml (unsupported). Silenced nb_venv_kernels unregister output. Added `make upgrade` target for all environment managers to upgrade packages<br>
   **Result**: CI simplified to conda/uv/virtualenv. Upgrade targets added

17. **Task - Unify dev deps via pyproject.toml**: Conda now uses pyproject.toml `[project.optional-dependencies.dev]` instead of environment.yml for dev dependencies. environment.yml is now minimal (just python and pip). Updated Makefile create_environment, requirements, upgrade targets to install dev deps via pip. Fixed virtualenv to use standard venv only (removed virtualenvwrapper support which caused `.venv/bin/pip not found` error). Updated post_gen_project.py file cleanup logic. Fixed Jinja whitespace in requirements-dev.txt<br>
   **Result**: All managers now use consistent pip-based dev deps installation. All 20 tests pass

18. **Task - Update philosophy document**: Added "Guiding Philosophy" section emphasizing promoting best practices over proliferating outdated ones. Updated dev dependencies section to reflect new conda behavior (pyproject.toml instead of environment.yml)<br>
   **Result**: STELLARS_CCDS_PHILOSOPHY.md updated with best practices philosophy and accurate dev deps info

19. **Task - Separate cloud tools from API libs**: Moved CLI tools to dev dependencies, kept API libraries in main dependencies. awscli/gsutil -> dev deps, botocore/google-cloud-storage/azure-storage-blob -> main deps. Fixed ruff isort config (underscore to hyphen). Updated test expectations for conda with requirements.txt<br>
   **Result**: All 23 tests pass. Cloud dependencies properly separated

20. **Task - Simplify conda kernel handling**: Removed nb_venv_kernels from conda (use nb_conda_kernels auto-discovery or ipykernel install). Silenced nb_venv_kernels register output for virtualenv/uv. Added kernel cleanup to conda remove_environment. Simplified conda env remove command<br>
   **Result**: Cleaner kernel management for conda environments

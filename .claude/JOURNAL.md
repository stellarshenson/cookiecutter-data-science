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

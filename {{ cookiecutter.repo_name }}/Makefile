.PHONY: clean data lint format requirements build sync_data_up sync_data_down test

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = {{ cookiecutter.repo_name }}
MODULE_NAME = {{ cookiecutter.module_name }}
PYTHON_VERSION = {{ cookiecutter.python_version_number }}
PYTHON_INTERPRETER = python

#################################################################################
# STYLES                                                                        #
#################################################################################

MSG_PREFIX = \033[1m\033[36m>>>\033[0m
WARN_PREFIX = \033[33m>>>\033[0m
ERR_PREFIX = \033[31m>>>\033[0m
WARN_STYLE = \033[33m
ERR_STYLE = \033[31m
HIGHLIGHT_STYLE = \033[1m\033[94m
OK_STYLE = \033[92m
NO_STYLE = \033[0m

#################################################################################
# ENVIRONMENT CONFIGURATION                                                     #
#################################################################################

{% if cookiecutter.environment_manager == 'conda' -%}
# conda environment configuration
ENV_LOCATION = {{ cookiecutter.env_location }}
CONDA_FLAGS = --no-capture-output
{% if cookiecutter.dependency_file == 'environment.yml' -%}
CONDA_ENV_NAME = $(shell sed -n '/^name:/{ s/^name:[ \t]*//; s/[ \t]*\#.*//; s/[ \t]*$$//p; }' environment.yml)
{% else -%}
CONDA_ENV_NAME = {{ cookiecutter.env_name }}
{% endif -%}
CONDA_ENV_PATH = $(PROJECT_DIR)/.venv/$(CONDA_ENV_NAME)

# set conda env selector based on location (local vs global)
ifeq ($(ENV_LOCATION),local)
CONDA_ENV_SELECTOR = -p $(CONDA_ENV_PATH)
else
CONDA_ENV_SELECTOR = --name $(CONDA_ENV_NAME)
endif

# check if conda is present
ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

# check if environment was installed
ifeq ($(ENV_LOCATION),local)
ifeq (,$(wildcard $(CONDA_ENV_PATH)/conda-meta))
HAS_CONDA_ENV=False
else
HAS_CONDA_ENV=True
endif
else
ifeq (,$(shell conda env list | grep $(CONDA_ENV_NAME)))
HAS_CONDA_ENV=False
else
HAS_CONDA_ENV=True
endif
endif

{% elif cookiecutter.environment_manager == 'virtualenv' -%}
# virtualenv configuration
VENV_PATH = $(PROJECT_DIR)/.venv

{% elif cookiecutter.environment_manager == 'uv' -%}
# uv configuration
VENV_PATH = $(PROJECT_DIR)/.venv

{% endif -%}

#################################################################################
# COMMANDS                                                                      #
#################################################################################

{% if cookiecutter.dependency_file != 'none' %}
## Install Python dependencies
.PHONY: requirements
{% if cookiecutter.environment_manager == 'conda' %}
requirements: test_environment
	@echo "$(MSG_PREFIX) installing requirements for $(HIGHLIGHT_STYLE)$(CONDA_ENV_NAME)$(NO_STYLE) environment"
	conda run $(CONDA_ENV_SELECTOR) $(CONDA_FLAGS) python -m pip install -U pip setuptools wheel
{% if cookiecutter.dependency_file == 'environment.yml' %}
	conda env update $(CONDA_ENV_SELECTOR) -f environment.yml --prune
{% elif cookiecutter.dependency_file == 'requirements.txt' %}
	conda run $(CONDA_ENV_SELECTOR) $(CONDA_FLAGS) python -m pip install -r requirements.txt
{% elif cookiecutter.dependency_file == 'pyproject.toml' %}
	conda run $(CONDA_ENV_SELECTOR) $(CONDA_FLAGS) pip install -e .
{% endif %}
{% elif cookiecutter.environment_manager == 'virtualenv' %}
requirements:
	@echo "$(MSG_PREFIX) installing requirements"
	$(PYTHON_INTERPRETER) -m pip install -U pip
{% if cookiecutter.dependency_file == 'requirements.txt' %}
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
{% elif cookiecutter.dependency_file == 'pyproject.toml' %}
	pip install -e .
{% endif %}
{% elif cookiecutter.environment_manager == 'uv' %}
requirements:
	@echo "$(MSG_PREFIX) installing requirements with uv"
{% if cookiecutter.dependency_file == 'requirements.txt' %}
	uv pip install -r requirements.txt
{% elif cookiecutter.dependency_file == 'pyproject.toml' %}
	uv sync
{% endif %}
{% endif %}
{% endif %}

## Delete all compiled Python files
clean:
	@echo "$(MSG_PREFIX) removing cache and compiled files"
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name '__pycache__' -exec rm -r {} +
	@find . -type d -name '*.egg-info' -exec rm -r {} +
	@find . -type d -name '.ipynb_checkpoints' -exec rm -r {} +
	@find . -type d -name '.pytest_cache' -exec rm -r {} +
	@echo "$(MSG_PREFIX) removing dist and build directory"
	@rm -rf build dist

{% if cookiecutter.linting_and_formatting == 'ruff' -%}
## Lint using ruff (use `make format` to do formatting)
lint:
	@echo "$(MSG_PREFIX) linting the sourcecode"
	ruff format --check
	ruff check

## Format source code with ruff
format:
	@echo "$(MSG_PREFIX) formatting the sourcecode"
	ruff check --fix
	ruff format
{% elif cookiecutter.linting_and_formatting == 'flake8+black+isort' -%}
## Lint using flake8, black, and isort (use `make format` to do formatting)
lint:
	@echo "$(MSG_PREFIX) linting the sourcecode"
	flake8 {{ cookiecutter.module_name }}
	isort --check --diff {{ cookiecutter.module_name }}
	black --check {{ cookiecutter.module_name }}

## Format source code with black and isort
format:
	@echo "$(MSG_PREFIX) formatting the sourcecode"
	isort {{ cookiecutter.module_name }}
	black {{ cookiecutter.module_name }}
{% endif %}

{% if cookiecutter.testing_framework != 'none' %}
## Run tests
test:
	@echo "$(MSG_PREFIX) checking for tests"
{% if cookiecutter.environment_manager == 'conda' %}
{% if cookiecutter.testing_framework == 'pytest' %}
	@conda run $(CONDA_ENV_SELECTOR) $(CONDA_FLAGS) pytest --collect-only ./tests > /dev/null 2>&1; RESULT="$$?"; \
	if [ "$$RESULT" != "5" ]; then \
		echo "$(MSG_PREFIX) executing python tests"; \
		conda run $(CONDA_ENV_SELECTOR) $(CONDA_FLAGS) pytest --cov -v ./tests; \
	else \
		echo "$(WARN_PREFIX) $(WARN_STYLE)WARNING: no tests present$(NO_STYLE)"; \
	fi
{% elif cookiecutter.testing_framework == 'unittest' %}
	conda run $(CONDA_ENV_SELECTOR) $(CONDA_FLAGS) python -m unittest discover -s tests
{% endif %}
{% else %}
{% if cookiecutter.testing_framework == 'pytest' %}
	@pytest --collect-only ./tests > /dev/null 2>&1; RESULT="$$?"; \
	if [ "$$RESULT" != "5" ]; then \
		echo "$(MSG_PREFIX) executing python tests"; \
		pytest --cov -v ./tests; \
	else \
		echo "$(WARN_PREFIX) $(WARN_STYLE)WARNING: no tests present$(NO_STYLE)"; \
	fi
{% elif cookiecutter.testing_framework == 'unittest' %}
	python -m unittest discover -s tests
{% endif %}
{% endif %}
{% endif %}

{% if not cookiecutter.dataset_storage.none %}
## Download data from storage system
sync_data_down:
	@echo "$(MSG_PREFIX) downloading data from storage"
{% if cookiecutter.dataset_storage.s3 %}
	aws s3 sync s3://{{ cookiecutter.dataset_storage.s3.bucket }}/data/ \
		data/{% if cookiecutter.dataset_storage.s3.aws_profile != 'default' %} --profile {{ cookiecutter.dataset_storage.s3.aws_profile }}{% endif %}

{% elif cookiecutter.dataset_storage.azure %}
	az storage blob download-batch -s {{ cookiecutter.dataset_storage.azure.container }}/data/ \
		-d data/
{% elif cookiecutter.dataset_storage.gcs %}
	gsutil -m rsync -r gs://{{ cookiecutter.dataset_storage.gcs.bucket }}/data/ data/
{% endif %}

## Upload data to storage system
sync_data_up:
	@echo "$(MSG_PREFIX) uploading data to storage"
{% if cookiecutter.dataset_storage.s3 %}
	aws s3 sync data/ \
		s3://{{ cookiecutter.dataset_storage.s3.bucket }}/data{% if cookiecutter.dataset_storage.s3.aws_profile != 'default' %} --profile {{ cookiecutter.dataset_storage.s3.aws_profile }}{% endif %}

{% elif cookiecutter.dataset_storage.azure %}
	az storage blob upload-batch -d {{ cookiecutter.dataset_storage.azure.container }}/data/ \
		-s data/
{% elif cookiecutter.dataset_storage.gcs %}
	gsutil -m rsync -r data/ gs://{{ cookiecutter.dataset_storage.gcs.bucket }}/data/
{% endif %}
{% endif %}

{% if cookiecutter.environment_manager == 'conda' %}
#################################################################################
# CONDA ENVIRONMENT MANAGEMENT                                                  #
#################################################################################

## Check conda is available
check_conda:
ifeq (False,$(HAS_CONDA))
	@echo "$(ERR_PREFIX) $(ERR_STYLE)ERROR: conda not installed$(NO_STYLE)"
	@echo "$(ERR_PREFIX) $(ERR_STYLE)install anaconda or miniforge from https://github.com/conda-forge/miniforge$(NO_STYLE)"
	@exit 1
endif

## Set up conda environment
create_environment: check_conda
ifeq (True,$(HAS_CONDA))
ifeq ($(ENV_LOCATION),local)
	@echo "$(MSG_PREFIX) detected conda. Checking if local environment exists at .venv/$(CONDA_ENV_NAME)"
	@if [ -d "$(CONDA_ENV_PATH)/conda-meta" ]; then \
		echo "$(MSG_PREFIX) local conda environment already exists at .venv/$(CONDA_ENV_NAME). Skipping creation."; \
	else \
		echo "$(MSG_PREFIX) creating new local conda environment at $(HIGHLIGHT_STYLE).venv/$(CONDA_ENV_NAME)$(NO_STYLE)"; \
{%- if cookiecutter.dependency_file == 'environment.yml' %}
		conda env create -p $(CONDA_ENV_PATH) -f environment.yml; \
		echo "$(MSG_PREFIX) new conda env created successfully. Activate with: $(HIGHLIGHT_STYLE)conda activate $(CONDA_ENV_PATH)$(NO_STYLE)"; \
		conda run -p $(CONDA_ENV_PATH) $(CONDA_FLAGS) nbdime config-git --enable --global; \
		echo "$(MSG_PREFIX) environment was configured to integrate git with jupyter notebooks"; \
{%- else %}
		conda create -y -p $(CONDA_ENV_PATH) python=$(PYTHON_VERSION) pip; \
		echo "$(MSG_PREFIX) new conda env created successfully. Activate with: $(HIGHLIGHT_STYLE)conda activate $(CONDA_ENV_PATH)$(NO_STYLE)"; \
		echo "$(MSG_PREFIX) run 'make requirements' to install dependencies"; \
{%- endif %}
{%- if cookiecutter.jupyter_kernel_support == 'Yes' %}
		if command -v nb_venv_kernels >/dev/null 2>&1; then \
			echo "$(MSG_PREFIX) registering Jupyter kernel for $(HIGHLIGHT_STYLE)$(CONDA_ENV_PATH)$(NO_STYLE)"; \
			nb_venv_kernels register $(CONDA_ENV_PATH); \
			echo "$(OK_STYLE)>>> Kernel registered successfully$(NO_STYLE)"; \
		elif python -c "import nb_conda_kernels" 2>/dev/null; then \
			echo "$(MSG_PREFIX) nb_conda_kernels detected - kernel will be auto-discovered"; \
		else \
			echo "$(MSG_PREFIX) registering Jupyter kernel with ipykernel"; \
			conda run -p $(CONDA_ENV_PATH) $(CONDA_FLAGS) python -m ipykernel install --user --name=$(CONDA_ENV_NAME); \
			echo "$(OK_STYLE)>>> Kernel registered as $(CONDA_ENV_NAME)$(NO_STYLE)"; \
		fi; \
{%- endif %}
	fi
else
	@echo "$(MSG_PREFIX) detected conda. Checking if environment $(CONDA_ENV_NAME) exists."
	@if conda info --envs | grep -q "^$(CONDA_ENV_NAME)"; then \
		echo "$(MSG_PREFIX) conda environment $(CONDA_ENV_NAME) already exists. Skipping creation."; \
	else \
		echo "$(MSG_PREFIX) creating new conda environment $(HIGHLIGHT_STYLE)$(CONDA_ENV_NAME)$(NO_STYLE)"; \
{%- if cookiecutter.dependency_file == 'environment.yml' %}
		conda env create -f environment.yml; \
		echo "$(MSG_PREFIX) new conda env created successfully. Activate with: $(HIGHLIGHT_STYLE)conda activate $(CONDA_ENV_NAME)$(NO_STYLE)"; \
		conda run $(CONDA_ENV_SELECTOR) $(CONDA_FLAGS) nbdime config-git --enable --global; \
		echo "$(MSG_PREFIX) environment $(CONDA_ENV_NAME) was configured to integrate git with jupyter notebooks"; \
{%- else %}
		conda create -y --name $(CONDA_ENV_NAME) python=$(PYTHON_VERSION) pip; \
		echo "$(MSG_PREFIX) new conda env created successfully. Activate with: $(HIGHLIGHT_STYLE)conda activate $(CONDA_ENV_NAME)$(NO_STYLE)"; \
		echo "$(MSG_PREFIX) run 'make requirements' to install dependencies"; \
{%- endif %}
{%- if cookiecutter.jupyter_kernel_support == 'Yes' %}
		if python -c "import nb_conda_kernels" 2>/dev/null; then \
			echo "$(MSG_PREFIX) nb_conda_kernels detected - kernel will be auto-discovered"; \
		else \
			echo "$(MSG_PREFIX) registering Jupyter kernel with ipykernel"; \
			conda run --name $(CONDA_ENV_NAME) $(CONDA_FLAGS) python -m ipykernel install --user --name=$(CONDA_ENV_NAME); \
			echo "$(OK_STYLE)>>> Kernel registered as $(CONDA_ENV_NAME)$(NO_STYLE)"; \
		fi; \
{%- endif %}
	fi
endif
endif

## Remove previously created environment
remove_environment: check_conda
ifeq (True,$(HAS_CONDA))
ifeq ($(ENV_LOCATION),local)
	@echo "$(MSG_PREFIX) detected conda, removing local environment at $(HIGHLIGHT_STYLE).venv/$(CONDA_ENV_NAME)$(NO_STYLE)"
	conda run --name base conda env remove -y -p $(CONDA_ENV_PATH)
else
	@echo "$(MSG_PREFIX) detected conda, removing $(HIGHLIGHT_STYLE)$(CONDA_ENV_NAME)$(NO_STYLE) conda environment."
	conda run --name base conda env remove -y -n $(CONDA_ENV_NAME)
endif
endif

## Test python environment is setup correctly
test_environment: check_conda
ifeq ($(ENV_LOCATION),local)
	@echo "$(MSG_PREFIX) testing local environment at $(HIGHLIGHT_STYLE).venv/$(CONDA_ENV_NAME)$(NO_STYLE) if ready"
	@if [ ! -d "$(CONDA_ENV_PATH)/conda-meta" ]; then \
		echo "$(ERR_PREFIX) $(ERR_STYLE)ERROR: local environment not found at .venv/$(CONDA_ENV_NAME)$(NO_STYLE)"; \
		exit 1; \
	fi
	@echo "$(MSG_PREFIX) checking Python version"
	@conda run -p $(CONDA_ENV_PATH) $(CONDA_FLAGS) python --version
	@echo "$(OK_STYLE)>>> Local environment .venv/$(CONDA_ENV_NAME) is properly configured$(NO_STYLE)"
else
	@echo "$(MSG_PREFIX) testing environment $(HIGHLIGHT_STYLE)$(CONDA_ENV_NAME)$(NO_STYLE) if ready"
	@if ! conda env list | grep -q "^$(CONDA_ENV_NAME) "; then \
		echo "$(ERR_PREFIX) $(ERR_STYLE)ERROR: environment $(CONDA_ENV_NAME) not found$(NO_STYLE)"; \
		exit 1; \
	fi
	@echo "$(MSG_PREFIX) checking Python version"
	@conda run $(CONDA_ENV_SELECTOR) $(CONDA_FLAGS) python --version
	@echo "$(OK_STYLE)>>> Environment $(CONDA_ENV_NAME) is properly configured$(NO_STYLE)"
endif

{% elif cookiecutter.environment_manager == 'virtualenv' %}
#################################################################################
# VIRTUALENV ENVIRONMENT MANAGEMENT                                             #
#################################################################################

## Set up Python interpreter environment
create_environment:
	@echo "$(MSG_PREFIX) creating virtualenv environment"
	@if command -v virtualenvwrapper.sh >/dev/null 2>&1; then \
		echo "$(MSG_PREFIX) using virtualenvwrapper"; \
		bash -c "source `which virtualenvwrapper.sh`; mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER)"; \
		echo "$(MSG_PREFIX) new virtualenv created. Activate with: $(HIGHLIGHT_STYLE)workon $(PROJECT_NAME)$(NO_STYLE)"; \
	else \
		echo "$(MSG_PREFIX) using standard venv (virtualenvwrapper not found)"; \
		$(PYTHON_INTERPRETER) -m venv .venv; \
		echo "$(MSG_PREFIX) new virtual environment created at .venv/"; \
		echo "$(MSG_PREFIX) Activate with:"; \
		echo "$(MSG_PREFIX) Windows: $(HIGHLIGHT_STYLE).\\.venv\\Scripts\\activate$(NO_STYLE)"; \
		echo "$(MSG_PREFIX) Unix/macOS: $(HIGHLIGHT_STYLE)source .venv/bin/activate$(NO_STYLE)"; \
	fi
{% if cookiecutter.jupyter_kernel_support == 'Yes' %}
	@if command -v nb_venv_kernels >/dev/null 2>&1; then \
		echo "$(MSG_PREFIX) registering Jupyter kernel for $(HIGHLIGHT_STYLE).venv$(NO_STYLE)"; \
		nb_venv_kernels register $(PROJECT_DIR)/.venv; \
		echo "$(OK_STYLE)>>> Kernel registered successfully$(NO_STYLE)"; \
	else \
		echo "$(MSG_PREFIX) registering Jupyter kernel with ipykernel"; \
		$(PROJECT_DIR)/.venv/bin/python -m ipykernel install --user --name=$(PROJECT_NAME); \
		echo "$(OK_STYLE)>>> Kernel registered as $(PROJECT_NAME)$(NO_STYLE)"; \
	fi
{% endif %}

{% elif cookiecutter.environment_manager == 'uv' %}
#################################################################################
# UV ENVIRONMENT MANAGEMENT                                                     #
#################################################################################

## Set up Python interpreter environment
create_environment:
	@echo "$(MSG_PREFIX) creating uv virtual environment"
	uv venv --python $(PYTHON_VERSION)
	@echo "$(MSG_PREFIX) new uv virtual environment created. Activate with:"
	@echo "$(MSG_PREFIX) Windows: $(HIGHLIGHT_STYLE).\\\.venv\\\Scripts\\\activate$(NO_STYLE)"
	@echo "$(MSG_PREFIX) Unix/macOS: $(HIGHLIGHT_STYLE)source ./.venv/bin/activate$(NO_STYLE)"
{% if cookiecutter.jupyter_kernel_support == 'Yes' %}
	@if command -v nb_venv_kernels >/dev/null 2>&1; then \
		echo "$(MSG_PREFIX) registering Jupyter kernel for $(HIGHLIGHT_STYLE).venv$(NO_STYLE)"; \
		nb_venv_kernels register $(PROJECT_DIR)/.venv; \
		echo "$(OK_STYLE)>>> Kernel registered successfully$(NO_STYLE)"; \
	else \
		echo "$(MSG_PREFIX) registering Jupyter kernel with ipykernel"; \
		$(PROJECT_DIR)/.venv/bin/python -m ipykernel install --user --name=$(PROJECT_NAME); \
		echo "$(OK_STYLE)>>> Kernel registered as $(PROJECT_NAME)$(NO_STYLE)"; \
	fi
{% endif %}

{% endif %}

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

{% if cookiecutter.include_code_scaffold == 'Yes' %}
## Make dataset
data: requirements
	@echo "$(MSG_PREFIX) generating dataset"
{% if cookiecutter.environment_manager == 'conda' %}
	conda run $(CONDA_ENV_SELECTOR) $(CONDA_FLAGS) $(PYTHON_INTERPRETER) {{ cookiecutter.module_name }}/dataset.py
{% else %}
	$(PYTHON_INTERPRETER) {{ cookiecutter.module_name }}/dataset.py
{% endif %}
{% endif %}

{% if cookiecutter.environment_manager == 'conda' %}
## Install src modules without dependencies (editable)
install: check_conda clean create_environment
	@echo "$(MSG_PREFIX) installing $(MODULE_NAME) in the $(CONDA_ENV_NAME) environment $(OK_STYLE)EDITABLE$(NO_STYLE)"
	@conda run $(CONDA_ENV_SELECTOR) $(CONDA_FLAGS) pip install --editable .
	@echo "$(MSG_PREFIX) you can now import $(HIGHLIGHT_STYLE)$(MODULE_NAME)$(NO_STYLE) module in your notebooks and scripts\n"

## Build package and install
build: check_conda install test increment_build_number
	@echo "$(MSG_PREFIX) building $(MODULE_NAME)"
	@conda run $(CONDA_ENV_SELECTOR) $(CONDA_FLAGS) python -m build --wheel

## Increment build number
increment_build_number: check_conda
	@echo "$(MSG_PREFIX) incrementing build number"
	@conda run $(CONDA_ENV_SELECTOR) $(CONDA_FLAGS) python -c "import toml; data=toml.load('pyproject.toml'); ver=data['project']['version'].split('.'); ver[-1]=str(int(ver[-1])+1); data['project']['version']='.'.join(ver); f=open('pyproject.toml','w'); toml.dump(data,f); f.close(); print('New version:',data['project']['version'])"
{% endif %}

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = sys.stdin.read(); \
matches = re.findall(r'\n## ([^\n]+)\n([a-zA-Z_-]+):', lines); \
matches = sorted(matches, key=lambda x: x[1].lower()); \
print('\nAvailable rules:\n'); \
print('\n'.join(['\033[36m{:25}\033[0m{}'.format(*reversed(match)) for match in matches])); \
print()
endef
export PRINT_HELP_PYSCRIPT

## Print the list of available commands
help:
	@$(PYTHON_INTERPRETER) -c "$${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)

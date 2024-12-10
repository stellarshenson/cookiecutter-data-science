.PHONY: clean data lint requirements sync_data_to_s3 sync_data_from_s3 test

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUCKET = {{ cookiecutter.s3_bucket }}
PROFILE = {{ cookiecutter.aws_profile }}
PROJECT_NAME = {{ cookiecutter.repo_name }}
MODULE_NAME = {{ cookiecutter.module_name }}
PYTHON_INTERPRETER = {{ cookiecutter.python_interpreter }}
CONDA_FLAGS= --no-capture-output


ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

PYTHON3_VERSION=3.11


#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
requirements: test_environment
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Make Dataset
data: requirements
	$(PYTHON_INTERPRETER) src/{{ cookiecutter.module_name }}/data/make_dataset.py data/raw data/processed


## Upload Data to S3
sync_data_to_s3:
ifeq (default,$(PROFILE))
	aws s3 sync data/ s3://$(BUCKET)/data/
else
	aws s3 sync data/ s3://$(BUCKET)/data/ --profile $(PROFILE)
endif

## Download Data from S3
sync_data_from_s3:
ifeq (default,$(PROFILE))
	aws s3 sync s3://$(BUCKET)/data/ data/
else
	aws s3 sync s3://$(BUCKET)/data/ data/ --profile $(PROFILE)
endif


# Set up python interpreter environment
create_environment:
ifeq (True,$(HAS_CONDA))
	@echo ">>> Detected conda. Checking if environment $(PROJECT_NAME) exists."
	@if conda info --envs | grep -q "^$(PROJECT_NAME) "; then \
		echo ">>> Conda environment $(PROJECT_NAME) already exists. Skipping creation."; \
	else \
		echo ">>> Creating new conda environment $(PROJECT_NAME)."; \
		conda create -y --name $(PROJECT_NAME) python=$(PYTHON3_VERSION); \
		conda env update --name ${PROJECT_NAME} -f environment.yml; \
 		echo ">>> Creating JupyterLab kernel dedicated to environment $(PROJECT_NAME)."; \
	        conda run --name ${PROJECT_NAME} ${CONDA_FLAGS} pip install -U ipykernel; \
 		echo ">>> New conda env created. Activate with:\nconda activate $(PROJECT_NAME)"; \
	fi
endif

## Remove previously created environment
remove_environment:
ifeq (True,$(HAS_CONDA))
	@echo ">>> Detected conda, removing conda environment."
	conda env remove -y -n $(PROJECT_NAME)
	@echo ">>> Removing jupyterlab kernel for $(PROJECT_NAME)"
	@echo "y" | jupyter-kernelspec remove $(PROJECT_NAME) 
endif

## Test python environment is setup correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Delete all compiled Python files
clean:
	@echo ">>> removing cache and compiled files"
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name '__pycache__' -exec rm -r {} +
	@find . -type d -name '*.egg-info'  -exec rm -r {} +
	@find . -type d -name '.ipynb_checkpoints' -exec rm -r {} +
	@find . -type d -name '.pytest_cache' -exec rm -r {} +
	@echo ">>> removing dist and build directory"
	@rm -rf build dist
	@echo '>>> uninstalling local library'
	@conda run --name ${PROJECT_NAME} ${CONDA_FLAGS} pip uninstall -y $(MODULE_NAME) || true


## Install src modules without dependencies
install: clean create_environment
	@echo ">>> installing ${MODULE_NAME} in the ${PROJECT_NAME} environment"
	@conda run --name ${PROJECT_NAME} ${CONDA_FLAGS} pip install --editable .
	@echo ">>> fixing issues with jupyterlab 'jump to definition' by installing package in (base)"
	@conda run --name base pip install --no-dependencies --editable .
	@echo ">>> you can now import '$(MODULE_NAME)' module in your notebooks and scripts"

## Build package & install
build: install test pyproject.toml
	@echo ">>> building ${MODULE_NAME}" 
	@conda run --name ${PROJECT_NAME} ${CONDA_FLAGS} python -m build --wheel

## Lint using flake8
lint:
	flake8 src

## Run python tests
test:
	@echo ">>> executing python tests"
	pytest -v

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help

## prints the list of available commands
help:
	@echo ""
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' 
	@echo ""


# EOF

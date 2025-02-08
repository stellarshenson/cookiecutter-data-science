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
CONDA_ENV_NAME = $(PROJECT_NAME)
PYTHON3_VERSION=3.11

# checks if conda is present
ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

# checks if environment was installed
ifeq (,$(shell conda env list | grep $(PROJECT_NAME)))
HAS_CONDA_ENV=False
else
HAS_CONDA_ENV=True
endif


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
	@echo "\033[36m>>>\033[0m detected conda. Checking if environment ${CONDA_ENV_NAME} exists."
	@if conda info --envs | grep -q "^${CONDA_ENV_NAME}"; then \
		echo "\033[36m>>>\033[0m conda environment ${CONDA_ENV_NAME} already exists. Skipping creation."; \
	else \
		echo "\033[36m>>>\033[0m creating new conda environment \033[94m${CONDA_ENV_NAME}\033[0m"; \
		conda create -y --name ${CONDA_ENV_NAME} python=${PYTHON3_VERSION}; \
		conda env update --name ${CONDA_ENV_NAME} -f environment.yml; \
 		echo "\033[36m>>>\033[0m creating JupyterLab kernel dedicated to environment ${CONDA_ENV_NAME}"; \
	        conda run --name ${CONDA_ENV_NAME} ${CONDA_FLAGS} pip install -U ipykernel; \
 		echo "\033[36m>>>\033[0m new conda env created successfully. Activate with: \033[94mconda activate ${CONDA_ENV_NAME}\033[0m"; \
	        conda run --name ${CONDA_ENV_NAME} ${CONDA_FLAGS} nbdime config-git --enable --global; \
 		echo "\033[36m>>>\033[0m environment ${CONDA_ENV_NAME} was configured to integrate git with jupyter notebooks"; \
	fi
endif

## Remove previously created environment
remove_environment:
ifeq (True,$(HAS_CONDA))
	@echo "\033[36m>>>\033[0m detected conda, removing \033[94m${CONDA_ENV_NAME}\033[0m conda environment."
	conda run --name base conda env remove -y -n ${CONDA_ENV_NAME}
endif

## Test python environment is setup correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Delete all compiled Python files
clean:
	@echo "\033[36m>>>\033[0m removing cache and compiled files"
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name '__pycache__' -exec rm -r {} +
	@find . -type d -name '*.egg-info'  -exec rm -r {} +
	@find . -type d -name '.ipynb_checkpoints' -exec rm -r {} +
	@find . -type d -name '.pytest_cache' -exec rm -r {} +
	@echo "\033[36m>>>\033[0m removing dist and build directory"
	@rm -rf build dist
ifeq (True,$(HAS_CONDA_ENV))
	@echo "\033[36m>>>\033[0m uninstalling local library"
	@conda run --name ${CONDA_ENV_NAME} ${CONDA_FLAGS} pip uninstall -y $(MODULE_NAME) || true
endif

## Install src modules without dependencies
install: clean create_environment
	@echo "\033[36m>>>\033[0m installing ${MODULE_NAME} in the ${CONDA_ENV_NAME} environment [\033[092mEDITABLE\033[0m]"
	@conda run --name ${CONDA_ENV_NAME} ${CONDA_FLAGS} pip install --editable .
	@echo "\033[36m>>>\033[0m fixing issues with jupyterlab 'jump to definition' by installing package in (base)"
	@conda run --name base pip install --no-dependencies --editable .
	@echo "\033[36m>>>\033[0m you can now import \033[94m$(MODULE_NAME)\033[0m module in your notebooks and scripts\n"

## Build package & install
build: increment_build_number install test pyproject.toml
	@echo "\033[36m>>>\033[0m building ${MODULE_NAME}" 
	@conda run --name ${CONDA_ENV_NAME} ${CONDA_FLAGS} python -m build --wheel

# Increment build number
increment_build_number:
	@echo "\033[36m>>>\033[0m incrementing version number"
	@conda run --name ${CONDA_ENV_NAME} ${CONDA_FLAGS} python -c "import toml; data=toml.load('pyproject.toml'); ver=data['project']['version'].split('.'); ver[-1]=str(int(ver[-1])+1); data['project']['version']='.'.join(ver); f=open('pyproject.toml','w'); toml.dump(data,f); f.close(); print('New version:',data['project']['version'])"


## Lint using flake8
lint:
	@conda run --name ${CONDA_ENV_NAME} ${CONDA_FLAGS} flake8 src

## Run python tests
test:
	@echo "\033[36m>>>\033[0m checking for tests"
	@conda run --name ${CONDA_ENV_NAME} ${CONDA_FLAGS} pytest --collect-only > /dev/null 2>&1; RESULT="$$?"; \
	if [ "$$RESULT" != "5" ]; then \
		echo "\033[36m>>>\033[0m executing python tests"; \
		conda run --name ${CONDA_ENV_NAME} ${CONDA_FLAGS} pytest -v --cov; \
	else \
		echo "\033[36m>>>\033[0m WARNING: no tests present"; \
	fi

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

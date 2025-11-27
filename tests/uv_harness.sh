#!/bin/bash
set -ex

PROJECT_NAME=$(basename $1)
CCDS_ROOT=$(dirname $0)
MODULE_NAME=$2

# Configure exit / teardown behavior
function finish {
    # Deactivate venv if we're in one
    if [[ $(which python) == *".venv"* ]]; then
        deactivate || true
    fi
    # Clean up venv directory
    if [ -d ".venv" ]; then
        rm -rf .venv
    fi
}
trap finish EXIT

# Source the steps in the test
source $CCDS_ROOT/test_functions.sh

# Navigate to the generated project and run make commands
cd $1
make

# Create and activate virtual environment
make create_environment

# Check if running on Windows and use appropriate activate path
if [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* ]]; then
    source ".venv/Scripts/activate"
else
    source ".venv/bin/activate"
fi

make requirements
make lint
make format

# Test clean target
mkdir -p __pycache__
touch __pycache__/test.pyc
make clean
if [ -d "__pycache__" ]; then
    echo "ERROR: clean did not remove __pycache__"
    exit 1
fi

echo "All targets passed!"

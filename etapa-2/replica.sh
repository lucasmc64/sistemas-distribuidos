#! /usr/bin/bash

# Global variables

SCRIPT_DIRECTORY=$(pwd -P)

# Activating virtual environment

# shellcheck source=/dev/null
source "${SCRIPT_DIRECTORY}/pyenv/bin/activate"

python3 src/kvs_database.py $1

# Leave virtual environment

deactivate


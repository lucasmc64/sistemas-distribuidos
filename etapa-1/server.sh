#! /usr/bin/bash

# Global variables

SCRIPT_DIRECTORY=$(pwd -P)
PORT=12345

declare -A FLAGS=(
  ["--port"]="Enter a specific port on which the server will try to use"
  ["-v, --version"]="Shows the version the project is in"
  ["-h, --help"]="List all flag options and commands accepted by the server"
)

# Handling args

for arg in "$@"; do
  case "$arg" in
  "--port="*)
    PORT="${arg:7}"
    ;;
  esac

  if [ "$arg" = "--version" ] || [ "$arg" = "-v" ]; then
    echo -ne "Valkyrie server 0.6.0\n"
    exit 0
  fi

  if [ "$arg" = "--help" ] || [ "$arg" = "-h" ]; then
    echo -e "usage: ./client.sh [option] ..."
    echo -e "Options:"

    for key in "${!FLAGS[@]}"; do
      printf "%-20s ${FLAGS[$key]}\n" "$key"
    done

    exit 0
  fi
done

# Activating virtual environment

# shellcheck source=/dev/null
source "${SCRIPT_DIRECTORY}/pyenv/bin/activate"

# WIP

python3 src/kvs_server.py "$PORT"

# Leave virtual environment

deactivate

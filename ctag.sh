#!/usr/bin/env bash
# this script uses the created local python environment
venvdir="$(pwd)/_venv_python"

if [[ ! -d "$venvdir" ]]; then
    echo "You need to run first ./prepare.sh to use this script."
    exit 1
fi

. "$venvdir/bin/activate"
./ctag.py "$@"
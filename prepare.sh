#!/usr/bin/env bash

venvdir="$(pwd)/_venv_python"

pyvenv_preparation() {
    echo "py venv setup"
    python3.6 -m venv "$venvdir"
    . "$venvdir/bin/activate"
    pip3 install --upgrade pip
    pip3 install -r requirements.list

    wget -c https://github.com/jgm/pandoc/releases/download/2.3.1/pandoc-2.3.1-linux.tar.gz
    tar -xzf pandoc-2.3.1-linux.tar.gz
    mv pandoc-2.3.1 pandoc

    chmod +x "$(pwd)/pandoc/bin/pandoc"
    chmod +x "$(pwd)/pandoc/bin/pandoc-citeproc"
}

pyvenv_preparation

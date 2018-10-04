#!/usr/bin/env bash

venvdir="$(pwd)/_venv_python"

pyvenv_preparation() {
    echo "py venv setup"
    python3.6 -m venv "$venvdir"
    . "$venvdir/bin/activate"
    pip3 install --upgrade pip
    pip3 install -r requirements.list

    python3 - <<END
from pypandoc.pandoc_download import download_pandoc
download_pandoc(targetfolder='$(pwd)/pandoc')
END
    chmod +x "$(pwd)/pandoc/pandoc"
    chmod +x "$(pwd)/pandoc/pandoc-citeproc"
}

pyvenv_preparation

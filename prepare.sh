#!/usr/bin/env bash

venvdir="$(pwd)/_venv_python"

pyvenv_preparation() {
    echo "py venv setup"
    pyvenv "$venvdir"
    . "$venvdir/bin/activate"
    pip3 install --upgrade pip
    pip3 install numpy nltk
    pip3 install pypandoc

    python3 - <<END
from pypandoc.pandoc_download import download_pandoc
download_pandoc(targetfolder='$(pwd)/pandoc')
END
}

pyvenv_preparation

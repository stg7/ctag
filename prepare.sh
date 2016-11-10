#!/usr/bin/env bash

venvdir="$(pwd)/_venv_python"

pyvenv_preparation() {
    echo "py venv setup"
    pyvenv "$venvdir"
    . "$venvdir/bin/activate"
    pip3 install --upgrade pip
    pip3 install numpy nltk

    # scipy scikit-learn pandas matplotlib gensim pillow  #plotly
    # pip3 install exifread
    # pip3 install -U textblob
    # python3 -m textblob.download_corpora
}

pyvenv_preparation

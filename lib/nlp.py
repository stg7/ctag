#!/usr/bin/env python3
"""
    Copyright 2016-today
    Project Ctag

    natural language processing helper methods

    Author: Steve Göring
"""

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer

_tknzr = WordPunctTokenizer()

try:
    _stop_words = stopwords.words('english')
    _stop_words = stopwords.words('german')
except:
    nltk.download("stopwords")


def nlp_tokenize(x):
    """ Return word-tokens of a given string `x`
        Example:
            nlp_tokenize("Hello world") = ["Hello", "World"]
    """
    return _tknzr.tokenize(x)


def nlp_remove_stop_words(x, language="english"):
    """ Return word-vector without 'language' stopwords (e.g. remove 'a')
    """
    stop = stopwords.words(language)
    return [y for y in nlp_tokenize(x) if y not in stop]


if __name__ == "__main__":
    from log import lInfo
    lInfo(nlp_tokenize("hello world. what is happening?"))
    lInfo("this is just a lib")

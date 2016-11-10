#!/usr/bin/env python3
"""
    Cloudtag

    author: Steve Göring
    contact: stg7@gmx.de

"""
"""
    This file is part of cloudtag.

    cloudtag is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    cloudtag is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with cloudtag.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import os
import argparse
import time
import multiprocessing
from multiprocessing import Pool

import numpy as np

from lib.log import *
from lib.nlp import nlp_remove_stop_words


def add_dict(d1, d2):
    d = {}
    for x in d1:
        d[x] = d1[x]
    for x in d2:
        d[x] = d.get(x, 0) + d2[x]
    return d


def build_word_histogram(infilename, remove_stop_words, language, min_len):

    with open(infilename, "r") as infile:
        text = "".join(infile.readlines()).lower()
    # remove non [0-9] signs
    # tokenize
    # map
    lInfo(len(text))
    return {}


def ctag(inputfiles, output_dir, remove_stop_words, language, min_freq, min_len ,cpu_count):
    startTime = time.time()
    lInfo(inputfiles)
    pool = Pool(processes=cpu_count)
    params = [(inputfile, remove_stop_words, language, min_len) for inputfile in inputfiles]
    results = pool.starmap(build_word_histogram, params)

    global_histogram = {}
    for histogram in results:
        global_histogram = add_dict(global_histogram, histogram)

    jPrint(global_histogram)

    # filter out words with a frequency that is not >= min_freq
    lInfo("done: {} s".format(time.time() - startTime))


def main(params):
    # argument parsing
    parser = argparse.ArgumentParser(description='ctag - tag cloud generator', epilog="stg7 2016", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('inputfile', nargs="+", type=str, help="input file")
    parser.add_argument('--cpu_count', type=int, default=multiprocessing.cpu_count(), help="cpus/threads that are used for processing")
    parser.add_argument('--output_dir', type=str, default="./results", help="output_directory for storing tag cloud")
    parser.add_argument('--remove_stop_words', action='store_false', help="remove stopswords")
    parser.add_argument('--min_freq', type=int, default=1, help="min freq of a word")
    parser.add_argument('--min_len', type=int, default=1, help="min length of a word")
    parser.add_argument('--language', type=str, default="german", help="language in which the text is") # TODO: remove it maybe later by analyzing language

    argsdict = vars(parser.parse_args())

    lInfo("start ctag")

    # create output dir if it does not exist already
    os.makedirs(argsdict["output_dir"], exist_ok=True)

    ctag(argsdict["inputfile"],
         argsdict["output_dir"],
         argsdict["remove_stop_words"],
         argsdict["language"],
         argsdict["min_freq"],
         argsdict["min_len"],
         argsdict["cpu_count"])


if __name__ == "__main__":
    main(sys.argv[1:])

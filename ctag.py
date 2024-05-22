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
import json
import re
import shutil
import multiprocessing
import tempfile
from multiprocessing import Pool

from libs.log import *
from libs.nlp import *
from libs.cloud import svg_cloud

# set pypandoc path
os.environ.setdefault('PYPANDOC_PANDOC', os.path.dirname(os.path.realpath(__file__)) + '/pandoc/bin/pandoc')
lInfo(os.path.dirname(os.path.realpath(__file__)) + '/pandoc/bin/pandoc')
import pypandoc


def add_dict(d1, d2):
    d = {}
    for x in d1:
        d[x] = d1[x]
    for x in d2:
        d[x] = d.get(x, 0) + d2[x]
    return d


def extract_from_pdf(pdf_file_name):
    """ extract text from a pdf file using pdttotext via os.system """
    if shutil.which("pdftotext") is None:
        lError("pdftotext is not installed, therefore no pdf as input is possible")
        return ""
    f = tempfile.NamedTemporaryFile(delete=False)
    os.system("pdftotext {} {}".format(pdf_file_name, f.name))
    f.close()
    with open(f.name, "r") as fp:
        text = "".join(fp.readlines())
    os.unlink(f.name)
    return text


def read_input(infilename):
    """ read text from a file

        supported formats:
            * plain text
            * pdf
            * all formats from pandoc
    """
    if ".pdf" in infilename:
        return extract_from_pdf(infilename)
    try:
        return pypandoc.convert_file(infilename, 'md')
    except Exception as e:
        # if fileinput format is not available using pypandoc so try to read it as text
        with open(infilename, "r") as infile:
            return "".join(infile.readlines())


def build_word_histogram(infilename, remove_stop_words, language, min_len):
    input_text = read_input(infilename).lower()
    text = re.sub("[^a-zöäüß]", " ", input_text)
    if remove_stop_words:
        tokens = nlp_remove_stop_words(text, language)
    else:
        tokens = nlp_tokenize(text)
    # TODO: maybe use external file for storing results
    hist = {}
    for t in tokens:
        if len(t) > min_len:
            hist[t] = hist.get(t, 0) + 1

    return hist


def ctag(inputfiles, output_file, remove_stop_words, language, min_freq, min_len, pdf_output, debug, cpu_count):
    startTime = time.time()
    lInfo("process {} files".format(len(inputfiles)))

    pool = Pool(processes=cpu_count)
    params = [(inputfile, remove_stop_words, language, min_len) for inputfile in inputfiles]
    results = pool.starmap(build_word_histogram, params)

    global_histogram = {}
    for histogram in results:
        global_histogram = add_dict(global_histogram, histogram)

    # filter out words with a frequency that is not >= min_freq
    global_histogram = {t: global_histogram[t] for t in global_histogram if global_histogram[t] >= min_freq}

    if debug:
        histogram_file = output_file.replace(os.path.splitext(output_file)[1], ".debug.json")
        lInfo("for debugging write out intermediate histogram to: {}".format(histogram_file))
        with open(histogram_file, "w") as hist:
            hist.write(json.dumps(global_histogram, indent=4, sort_keys=True))

    with open(output_file, "w") as outfile:
        outfile.write(svg_cloud(global_histogram))
    if pdf_output:
        pdf_file_name = output_file.replace(os.path.splitext(output_file)[1], ".pdf")
        lInfo("create pdf graphic: {}".format(pdf_file_name))
        if shutil.which("inkscape") is None:
            lError("inkscape is not installed, therefore no pdf export is available.")
        else:
            os.system("""inkscape --export-filename="{pdffile}" {svgfile}""".format(svgfile=output_file, pdffile=pdf_file_name))
    lInfo("done: {} s".format(time.time() - startTime))


def main(params):
    # argument parsing
    parser = argparse.ArgumentParser(description='ctag - tag cloud generator', epilog="stg7 2016", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('inputfile', nargs="+", type=str, help="input file")
    parser.add_argument('--cpu_count', type=int, default=multiprocessing.cpu_count(), help="cpus/threads that are used for processing")
    parser.add_argument('--output_file', type=str, default="cloud.svg", help="outputfile for storing tag cloud")
    parser.add_argument('--remove_stop_words', action='store_false', help="remove stopswords")
    parser.add_argument('--min_freq', type=int, default=4, help="minimum freq of a word")
    parser.add_argument('--min_len', type=int, default=2, help="minimum length of a word")
    parser.add_argument('--language', type=str, default="german", help="language in which the text is")  # TODO: remove it maybe later by analyzing language
    parser.add_argument('--pdf_output', action='store_true', help="build a pdf file")
    parser.add_argument('--debug', action='store_true', help="debug mode (e.g. store intermediate results)")

    argsdict = vars(parser.parse_args())

    lInfo("start ctag")

    ctag(argsdict["inputfile"],
         argsdict["output_file"],
         argsdict["remove_stop_words"],
         argsdict["language"],
         argsdict["min_freq"],
         argsdict["min_len"],
         argsdict["pdf_output"],
         argsdict["debug"],
         argsdict["cpu_count"])


if __name__ == "__main__":
    main(sys.argv[1:])

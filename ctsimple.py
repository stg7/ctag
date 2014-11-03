#!/usr/bin/python3
# -*- coding: utf8 -*-
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

import os
import sys
import codecs
import re
import heapq
import random
import operator
import math

import ctlib


class htmlcloud:
    """
    simple html cloud
    """

    def __init__(self, patternFile, delim, config):
        # set color & font settings
        self._color = ctlib.ctcolor(config['color']['min'], config['color']['max'])
        self._font = ctlib.ctfont(config['font']['min'], config['font']['max'])

        # read pattern
        self._pattern = ctlib.ctpattern(patternFile, delim)

    def createCloud(self, Buckets, maxSize, minSize, maxWords, outfile):

        (minfreq, maxfreq, tmp) = ctlib.bucketsToList(Buckets, maxWords)

        D = {}
        for (i, k) in tmp:
            D[k] = i

        self._font.scale(minfreq, maxfreq)
        self._color.scale(minfreq, maxfreq)

        # write output file
        outfile.write(self._pattern.getHeader() + "\n")
        for k in sorted(D.keys()):
            size = self._font.calcSize(k, D[k])
            color = self._color.calcColor(k, D[k])
            outfile.write(self._pattern.getElement([size, color, k, "\n"]))

            print(".", end="")
            sys.stdout.flush()
        print("done")
        outfile.write(self._pattern.getFooter())

    def getExt(self):
        return ".html"


def cloudTag(infile, outfileName):
    print("ctsimple html")
    configfile = ctlib.getScriptDir() + "/cfg/config.cfg"
    if not os.path.isfile(configfile):
        ctlib.createDefaultConfig()

    config = ctlib.getConfig(configfile)

    # read config values
    maxWords = int(config['words']['max'])
    maxSize = int(config['font']['max'])
    minSize = int(config['font']['min'])

    patternsplitter = config['pattern']['split']
    patternbase = ctlib.getScriptDir() + "/" + config['pattern']['base']

    # create outputter instances
    out = htmlcloud(patternbase + config['pattern']['html'], patternsplitter, config)

    # read histogram
    B = ctlib.readPlain(infile, maxWords)

    # create output
    outfile = open(outfileName + out.getExt(), "w")
    out.createCloud(B, maxSize, minSize, maxWords, outfile)
    outfile.close()


def helpScreen():
    print("""\
 simple html cloud tag generator :-)
  usage: """ + __file__ + """ infile [outfile]

   params:
    infile   file to visualize
    outfile  optional output file name without extension

   config: see cfg/config.cfg

   example:
    run
         $""" + __file__ + """ test.txt
    creates a html tag cloud based on test.txt and
    save it as test.txt_.html

 infos: Steve Göring, stg7@gmx.de, 2012
""")


def main(args):
    # parse command line params
    if len(args) == 0:
        if not ctlib.calledfromCt:
            helpScreen()
        return 1

    # important: first param must be a valid file
    if not os.path.isfile(args[0]):
        if not ctlib.calledfromCt:
            helpScreen()
        print("\n error: file '" + args[0] + "' not exists")
        return 1

    try:
        if len(args) == 1:
            cloudTag(args[0], args[0] + "_")
            return 0

        if len(args) == 2:
            cloudTag(args[0], args[1])
            return 0

    except Exception as e:
        _, errormsg = e
        print("Error: " + e)
        return 1


if __name__ == "__main__":
    main(sys.argv[1:])

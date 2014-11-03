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

import sys
import io
import os
import configparser
import argparse

import ctana
import ctmerge
import ctsimple
import ctspiral
import ctlib


oldstdout = None


def hidestdout():
    # bypass stdout
    output = io.StringIO()
    oldstdout = sys.stdout
    sys.stdout = output


def ct(infile, outfilebase, splitter):
    # first analyse text
    if ctana.main([infile, splitter, outfilebase]) != 0:
        print(" error in module ctana")
        return 1
    print("")

    # read output plugins
    configfile = ctlib.getScriptDir() + "/cfg/config.cfg"
    if not (os.path.isfile(configfile)):
        ctlib.createDefaultConfig()

    config = ctlib.getConfig(configfile)

    # read config values
    outformat = config['output']['format'].split(",")
    if "html" in outformat:
        if ctsimple.main([outfilebase + ".plain"]) != 0:
            print(" error in ctsimple")
            return 1
        print("")
    if "svg" in outformat:
        if ctspiral.main([outfilebase + ".plain"]) != 0:
            print(" error in ctspiral")
            return 1
        print("")
    return 0


def main(args):
    ctlib.calledfromCt = True

    parser = argparse.ArgumentParser(description="cloud tag generator", epilog="stg7 2014")

    parser.add_argument("in", help="input file or directory")
    parser.add_argument("out", help="output base filename")

    parser.add_argument("-s", "--splitter", action="store", dest="splitter", default=" ", help="char that splits words in input texts, default \" \"")
    parser.add_argument("-r", "--recursive", action="store_true", dest="recursive", help="read recursive files from 'in' dir")
    parser.add_argument("-e", "--extension", action="store", dest="ext", default="", help="just handle files with this extension")
    parser.add_argument("-m", "--mute", action="store_true", dest="mute", help="no stdout messages")

    argsdict = vars(parser.parse_args())

    if len(args) < 2:
        parser.error("incorrect number of arguments, you need at least an inputfile/directory and outputfilebase")
        return 1

    if argsdict["mute"]:
        hidestdout()

    outfilebase = argsdict["out"]

    # just handle one input file
    if os.path.isfile(argsdict["in"]):
        infile = argsdict["in"]
    else:  # input dir
        if ctmerge.main([argsdict["in"], argsdict["out"], argsdict["ext"], argsdict["recursive"]]) != 0:
            print(" error in module ctmerge")
            return 1
        infile = argsdict["in"]
        print("")

    return ct(infile, outfilebase, argsdict["splitter"])


if __name__ == "__main__":
    main(sys.argv[1:])

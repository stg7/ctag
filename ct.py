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
import ctana, ctmerge, ctsimple, ctspiral, ctlib
import sys, io, os, configparser
from optparse import OptionParser

oldstdout = None

def hidestdout():
    # bypass stdout
    output = io.StringIO()
    oldstdout = sys.stdout
    sys.stdout = output
    #sys.stdout = old

def ct(infile, outfilebase, splitter):
    # first analyse text
    if(ctana.main([infile,splitter,outfilebase])!=0):
        print(" error in module ctana")
        return 1
    print("")

    # read output plugins
    configfile = ctlib.getScriptDir()+"/cfg/config.cfg"
    if(not (os.path.isfile(configfile))):
        ctlib.createDefaultConfig()

    config = ctlib.getConfig(configfile)

    # read config values
    outformat= config['output']['format'].split(",")
    if("html" in outformat):
        if(ctsimple.main([outfilebase + ".plain"])!=0):
            print(" error in ctsimple")
            return 1
        print("")
    if("svg" in outformat):
        if(ctspiral.main([outfilebase + ".plain"])!=0):
            print(" error in ctspiral")
            return 1
        print("")
    return 0

def main(args):
    ctlib.calledfromCt = True

    usage = "usage: %prog [options] in [out] \n in\t infile or directory \n out\t outfilebase"
    parser = OptionParser(usage)

    parser.add_option("-s", "--splitter", action="store", dest="splitter",default=" ", help="char that splits words in input texts, default \" \"")
    parser.add_option("-r", "--recursive", action="store_true", dest="recursive", help="read recursive files from 'in' dir")
    parser.add_option("-e", "--extension", action="store", dest="ext",default="", help="just handle files with this extension")

    parser.add_option("-m", "--mute", action="store_true", dest="mute", help="no stdout messages")
    (options, args) = parser.parse_args()

    if (len(args) < 2):
        parser.error("incorrect number of arguments, you need at least an inputfile/directory and outputfilebase")
        return 1

    if(options.mute):
        hidestdout()

    outfilebase = args[1]

    # just handle one input file
    if(os.path.isfile(args[0])):
        infile = args[0]
    else: # input dir
        if(ctmerge.main([args[0],args[1], options.ext, options.recursive])!=0):
            print(" error in module ctmerge")
            return 1
        infile = args[1]
        print("")

    return ct(infile, outfilebase, options.splitter)


if __name__ == "__main__":
    main(sys.argv[1:])

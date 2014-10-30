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
import os, sys, re, ctlib

def getFiles(indir,fileExt, recursive = True):
    res = []
    for f in os.listdir(indir):
        if os.path.isfile(indir+"/"+f):
            if re.match(fileExt,f):
                res += [indir + "/" + f]
        else:
            if(recursive):
                res += getFiles(indir+"/"+f,fileExt)
    return res

def merge(indir,outfile,fileExt, recursive = True):
    print("merge : inputfiles to " + outfile)

    out = open(outfile,"w")

    for f in getFiles(indir[0:-1],"."+fileExt,recursive):
        print(f)
        infile = open(f,"r")
        for l in infile:
            out.write(l)
        infile.close()
    out.close()

    return

def helpScreen():
    print("""\
 merge text files together :-)
  usage: """ + __file__ +"""" indir outfile [fileextension]  [recursive]

   params:
    indir: input directory
    outfile: filename of merged text files
    fileextension: optional filextension, e.g ".txt"
  infos: Steve Göring, stg7@gmx.de, 2012""")

def main(args):
    # parse command line params
    if(len(args)<2):
        if(not(ctlib.calledfromCt)):
            helpScreen()
        return 1

    # important: first param must be a valid file
    if(not(os.path.isdir(args[0]))):
        if(not(ctlib.calledfromCt)):
            helpScreen()
        print("\n error: dir '"+args[0]+"' not exists")
        return 1
    try:
        if(len(args)==2):
            merge(args[0],args[1],"")
            return 0

        if(len(args)==3):
            merge(args[0],args[1],args[2])
            return 0
        if(len(args)==4):
            merge(args[0],args[1],args[2], args[3])
            return 0
    except Exception as e:
        _,errormsg = e
        print("Error: " + e)
        return 1
if __name__ == "__main__":
    main(sys.argv[1:])


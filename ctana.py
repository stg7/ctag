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
import configparser, os,sys,codecs,re,heapq, random,operator, math, ctlib

"""
    simple text based output format
"""
class plaincloud:
    def __init__(self, patternFile, delim):
        return
    def createCloud(self, Buckets, maxSize, minSize ,maxWords, outfile):
        i = len(Buckets)-1 # last index
        tmp = []
        print("writing plain data")
        while(i>=0):
            if(Buckets[i]!=[]):
                outfile.write(str(i)+":" +str(Buckets[i])+"\n")
                print(".",end="")
                sys.stdout.flush()
            i -=1
        return
    def getExt(self):
        return ".plain"

def readIgnoreFile(ifile):
    words = []
    f = open(ctlib.getScriptDir()+"/"+ ifile, "r")
    for l in f:
        t = l[0:-1] # remove line break
        words.append(t.lower())
    f.close()
    return words

def readWords(infile, splitter, ignorechars, ignorecase):
    H = { }
    f = open(ctlib.getScriptDir()+"/"+infile, "r")

    for l in f :
        t =  l[0:-1] # remove line breaks
        # remove all ignorechars
        for c in ignorechars:
            t = t.replace(c,splitter)
            t = t.replace('\t',splitter) # remove tabs

        if(t!="" and t!=splitter):
            for w in t.split(splitter):
                if(w!=''):
                    if(ignorecase):
                        w = w.lower()
                    if( w in H):
                        H[w]+=1
                    else:
                        H[w]=1
    f.close()

    return H

def filterWords(H,ingonrewords,minLen, minFreq, maxFreq):
    # remove ignored words
    for w in ingonrewords:
        if( w in H):
            H[w] = 0
        if( w.title() in H):
            H[w.title()]=0 # remove capitalized words

    for k in H.keys():
        if (len(k) <= minLen):
            H[k] = 0
        if(minFreq > 0 and H[k] < minFreq):
            H[k] = 0
        if(maxFreq > 0  and H[k] > maxFreq):
            H[k] = 0
    # tidy up histogram -> remove values with freq 0
    HH ={}
    for k in H.keys():
        if(H[k]!=0):
            HH[k]=H[k]
    return HH

def textAnalysis(infile, splitter, ignorechars, ignorecase, ignorewords, minLenWords, minFreq, maxFreq):

    # build histogram
    H = filterWords(readWords(infile, splitter, ignorechars, ignorecase), ignorewords, minLenWords, minFreq, maxFreq)

    # get min/max values of H[i]
    min = None
    max = 0
    for k in H.keys():
        value = H[k]
        if(value > max):
            max = value
        if(min == None or value < min):
            min = value

    # create sorted list[count]= [words], maybe better for graph visualisation
    B = []

    for i in range(0,max+1): # create buckets
        B.append([])

    # "bucket" sort
    for k in H.keys():
        freq = H[k]
        if(freq > 0):
            if( B[freq] == []):
                B[freq] = [k]
            else:
                B[freq].append(k)
    return B



def cloudTag(infile, splitter, outfileName):
    print("text analysis")
    configfile = ctlib.getScriptDir()+"/cfg/config.cfg"
    if(not (os.path.isfile(configfile))):
        ctlib.createDefaultConfig()

    config = ctlib.getConfig(configfile)

    # read config values
    ignorechars = readIgnoreFile( config['ignore']['base'] + config['ignore']['chars'] )
    ignorewords = readIgnoreFile( config['ignore']['base'] + config['ignore']['words'])
    ignorecase = (config['ignore']['case'] =="True")
    minLenWords = int(config['words']['minlen'])
    minFreq = int(config['words']['minfreq'])
    maxFreq = int(config['words']['maxfreq'])
    maxWords = int(config['words']['max'])
    maxSize = int(config['font']['max'])
    minSize = int(config['font']['min'])

    outputformats = config['output']['format'].replace(" ","").lower().split(",")
    outputters =[]
    patternsplitter = config['pattern']['split']
    patternbase = ctlib.getScriptDir()+"/"+ config['pattern']['base']


    out = plaincloud(patternbase + config['pattern']['svg'] , patternsplitter)

    # create buckets: list[freq] = [words]
    Buckets = textAnalysis(infile, splitter, ignorechars, ignorecase, ignorewords, minLenWords, minFreq, maxFreq)

    outfile = open(outfileName+ out.getExt(),"w")
    out.createCloud(Buckets,maxSize,minSize,maxWords,outfile)
    outfile.close()
    print("done")


def helpScreen():
    print("""\
 text analyse :-)
  usage: """ + __file__ +""" infile [splitter] [out]

   params:
    infile: file to analyse")
    splitter: splitter char in file, default ' '
    out:  optional output file name, defalut infile_

  config: see cfg/config.cfg
  example:
   run
      $""" + __file__ + """" test.txt
   to create a cloud tag input file based on text.txt (histogram)
   infos: Steve Göring, stg7@gmx.de, 2012""")

def main(args):
    # parse command line params
    if(len(args)==0):
        if(not(ctlib.calledfromCt)):
            helpScreen()
        return 1

    # important: first param must be a valid file
    if(not(os.path.isfile(args[0]))):
        if(not(ctlib.calledfromCt)):
            helpScreen()
        print("\n error: inputfile '"+args[0]+"' not exists")
        return 1
    try:
        if(len(args)==1):
            cloudTag(args[0], " " ,args[0]+"_")
            return 0

        if(len(args)==2):
            cloudTag(args[0],args[1],args[0]+"_")
            return 0

        if(len(args)==3):
            cloudTag(args[0],args[1],args[2])
            return 0

    except Exception as e:
        _,errormsg = e
        print("Error: " + e)
        return 1
if __name__ == "__main__":
    main(sys.argv[1:])


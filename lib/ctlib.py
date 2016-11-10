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
import configparser

# global indicator, for handling, if modules are called from ct.py, :-( not the best solution FIXME
global calledfromCt
calledfromCt = False


def getConfig(configfile):
    """
    read config file
    @return config content
    """
    # FIXME: maybe better json format

    config = configparser.ConfigParser()
    config.readfp(open(configfile))

    try:
        # try to get an element in new python3.2 api style
        config['ignore']['base']

    except:
        # :( ugly, python-version <3.2
        # quick - fix -hack
        c = {}
        for s in config.sections():
            c[s] = {}
            for (key, value) in config.items(s):
                c[s][key] = value
        config = c

    return config


def createDefaultConfig():
    """
    create default configuration and write it to file
    """
    default = """\
#ignore settings
[ignore]
# base directory for ignore lists
base = cfg/ignore/

# ignore lower / uppercase
case = True
# textfilename for ignored word list
words = words.txt
# textfilename for ignored char list
chars = chars.txt

# tag cloud settings
[words]
# maximal words=-1 means use all words
max = -1
# maximal frequency of words
maxfreq = -1
# minimal frequency of words
minfreq = 10
# minimal length of words
minlen = 3

[font]
# font size in pixel
max = 90
min = 14
[color]
min = 555555
max = 00FF00
[pattern]
base = cfg/pattern/
# delimiter
split = #
# html pattern file
html= html.pat
# svg pattern
svg= svg.pat
[output]
format = html,svg
"""
    cfgfile = open(getScriptDir() + '/cfg/config.cfg', 'w')
    cfgfile.write(default)
    cfgfile.close()


def getHex(a):
    """
    convert value a to hex string, with leading zeros
    """
    aa = hex(a)[2:]
    if len(aa) < 2:
        aa = "0" + aa
    return aa


class ctcolor:
    """
    color class
    """

    def __init__(self, minColor, maxColor):
        self._minCol = (int(minColor[0:2], 16), int(minColor[2:4], 16), int(minColor[4:6], 16))
        self._maxCol = (int(maxColor[0:2], 16), int(maxColor[2:4], 16), int(maxColor[4:6], 16))
        self._colors = {}

    def scale(self, minfreq, maxfreq):
        self._scalefactor = ((self._maxCol[0] - self._minCol[0] + 0.0) / (maxfreq - minfreq),
                             (self._maxCol[1] - self._minCol[1] + 0.0) / (maxfreq - minfreq),
                             (self._maxCol[2] - self._minCol[2] + 0.0) / (maxfreq - minfreq))
        self._minfreq = minfreq
        self._maxfreq = maxfreq

    def calcColor(self, key, freq):
        self._colors[key] = "#" + "".join([getHex(self._minCol[j] + int(round((freq - self._minfreq) * self._scalefactor[j]))) for j in range(0, 3)])
        return self._colors[key]

    def getColor(self, key):
        return self._colors[key]


class ctfont:
    """
    font class
    """

    def __init__(self, minSize, maxSize):
        self._minSize = int(minSize)
        self._maxSize = int(maxSize)
        self._sizes = {}

    def scale(self, minfreq, maxfreq):
        self._scalefactor = (self._maxSize - self._minSize + 0.0) / (maxfreq - minfreq)
        self._minfreq = minfreq
        self._maxfreq = maxfreq

    def calcSize(self, key, freq):
        self._sizes[key] = str(self._minSize + int(round((freq - self._minfreq) * self._scalefactor)))
        return self._sizes[key]

    def getSize(self, key):
        return self._sizes[key]


class ctpattern:
    def __init__(self, patternFile, delim):
        # open pattern
        f = open(patternFile, "r")
        # read header
        header = ""
        l = ""
        while 3 * delim not in l:
            header += l
            l = f.readline()

        # read element, just one line
        element = f.readline().replace("\n", "").split(delim)
        f.readline()
        # read footer
        footer = ""
        while l != "":
            l = f.readline()
            footer += l
        f.close()
        self._header = header
        self._footer = footer
        self._element = element

    def getHeader(self):
        return self._header

    def getFooter(self):
        return self._footer

    def getElement(self, content):
        ret = ""
        i = 0
        for pattern in self._element:
            ret += pattern + str(content[i])
            i += 1
        return ret


def bucketsToList(Buckets, maxWords):
    """
    converts buckets to list
    """
    e = 0  # count elements
    tmp = []

    for i in sorted(Buckets.keys()):
        for k in Buckets[i]:
            tmp.append((i, k))
            e += 1
    tmp.reverse()

    if e == 0:
        raise Exception("error:", "text has no important words or is empty")
    # just work with maxwords words
    if maxWords > 0:
        tmp = tmp[0:maxWords]

    maxfreq = 0
    minfreq = None
    for (i, k) in tmp:
        if minfreq is None:
            minfreq = i
        maxfreq = max(maxfreq, i)
        minfreq = min(i, minfreq)

    return (minfreq, maxfreq, tmp)


def readPlain(infile, maxWords):
    """
    read plain text
    """

    infile = open(infile, "r")
    B = {}
    j = 0
    for l in infile:
        # every line "freq:[words]"
        p = l.find(":")
        freq = int(l[0:p])
        words = eval(l[p + 1:-1])  # not the best solution
        B[freq] = words
        j += len(words)
        if maxWords != -1 and j > maxWords:  # just read needed words
            break
    infile.close()
    return B


def getScriptDir():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

if __name__ == "__main__":
    pass

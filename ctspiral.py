#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
    Cloudtag 
    
    author: steve göring
    contact: stg7@gmx.de
    2012
    
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
import os,sys,codecs,re,heapq, random,operator, math, time, ctlib
# for font measuring 
from tkinter import *
from tkinter import font
        
"""
 minmal 2d vector class: no check that lengths are compatable.
"""
class xy(tuple):
    def __add__(self, a):
        return xy(x + y for x, y in zip(self, a))
    def __sub__(self, a):
        return xy(x - y for x, y in zip(self, a))
    def __mul__(self, c):
        return xy(x * c for x in self)
    def __rmul__(self, c):
        return xy(c * x for x in self)
    def nabs(self):
        (x,y) = self
        return x*x +y*y
    def man(self,o):
        (x,y) = self -o
        return abs(x) +abs(y)
    def min(self):
        (x,y) = self 
        return min(x,y)
    def x(self):
        (x,y) = self 
        return x
    def y(self):
        (x,y) = self 
        return y
    def swap(self):
        (x,y) = self
        return xy([y,x])
        

"""
check collision with i and all nodes in worked 

!! learn, that python tuple unpacking is a performance killer
"""
def checkAll(worked, pos, i,sizes):
    overlap = False
    ix = pos[i][0]
    iy = pos[i][1]
    
    six = sizes[i][0]/2
    siy = sizes[i][1]/2
    for k in worked.difference([i]):                
        dx = ix-pos[k][0]
        dy = iy-pos[k][1]
       
        sx = six+ sizes[k][0] /2
        sy = siy+ sizes[k][1] /2
        # colision
        if( abs(dx) < sx and abs(dy) < sy):
            return True
    return overlap
    

class svgcloud:
    
    def __init__(self, patternFile, delim, config):
        # set color & font settings
        self._color = ctlib.ctcolor(config['color']['min'], config['color']['max'])
        self._font = ctlib.ctfont(config['font']['min'], config['font']['max'])
               
        # read pattern 
        self._pattern = ctlib.ctpattern(patternFile, delim)
        
        
    def createCloud(self, Buckets, maxSize, minSize ,maxWords, outfile):
        start = time.time()
        
        (minfreq, maxfreq, tmp) = ctlib.bucketsToList(Buckets, maxWords)
        
        self._font.scale(minfreq, maxfreq)
        self._color.scale(minfreq, maxfreq)
        
        pos = {} # positions
        parent = Buckets[maxfreq][0] # parent word
        
        sizes = {}  # width and hight 
        fontsizes = {}       
        info = {} # freq values
        dirs = set([]) # directions
        colors = {}
        
        maxx = 30
        dir = 1 
        dirstep =1 # get from config param TODO
        random.seed(1)
        
        # for font measuing: initialize Tk
        Tk()
        
        print("precalculation")
        # initialize positions (random)
        for (i,k) in tmp:
            
            size = int(self._font.calcSize(k,i))
            color = self._color.calcColor(k,i)
            
            f = font.Font(family="courier", size=-int(size), weight=NORMAL)
            h = size
            w = f.measure(k)
            
            # get random x,y positions within a circle: x^2+y^2<= maxx^2
            x = random.randint(-maxx,maxx)
            yy = random.randint(0,maxx*maxx -x*x)
            y = math.sqrt(yy) 
            if(random.randint(0,1) == 0):
                y=-y
            
            info[k] = i
            sizes[k] =xy([w,h])
            
            if(dir % 2 == 0):
                # text is vertical: store direction and change size
                dirs.add(k)
                # find letter with max width
                w = max([ f.measure(c) for c in k] )
                # change dimension 
                sizes[k]=sizes[k].swap()
                dir = 0 
            
            pos[k] = xy([x,y]) 
            dir += dirstep
            print(".",end="")
            sys.stdout.flush()  
        print("done")
        # center parent
        pos[parent] = xy([0,0])
        
        # "pre"calculated spiral 
        spiral = {}
        
        colisionSum = 0
        worked = set([ parent]) # elements that fits
        print("calculate positions")
        
        # calculate positions that doesn't overlapp
        for (_,i) in tmp[1:]:     
            # check if node i overlaps any other node in worked set
            overlap =  checkAll( worked,pos, i ,sizes)

            # find new position with archimedis spiral
            # (1) spiralstep width = 1:
            a = 1 
            # (2) angle step delta phi
            dF = 0.1 
            F = dF
            
            colisionCount = 1  # count collision tests
            while(overlap ):          
                if(not F in spiral): # store spiral values 
                    spiral[F] = xy([math.sin(F)* a *F,math.cos(F)* a *F ]) 
                # calc new pos     
                pos[i]+=spiral[F]
                colisionCount += 1
                F+=dF
                # check overlapping
                overlap = checkAll(worked, pos, i, sizes)
                    
            colisionSum += colisionCount
            worked.add(i)
            print(".",end="")
            sys.stdout.flush()       
        end = time.time()
        rtime = str(end-start)
        print("done")
        print("with " + str(colisionSum) +" collision-tests in: " + rtime +" s")
        
        
        # output 
        maxx = 0
        minx = 0
        maxy = 0
        miny = 0
        outfile.write(self._pattern.getHeader()+"\n")
        for (_,o) in tmp:
            freq = info[o]
            (x,y) = pos[o]
            (w,h) = sizes[o]
            
            # calculate max / min x/y values 
            maxx = max(maxx, x ,x+w )
            maxy = max(maxy, y ,y+h )
            
            minx = min(minx, x ,x+w )
            miny = min(miny, y ,y+h )
           
            style = "fill:"+ self._color.getColor(o)
            
            if(o in dirs): # text o is vertical
                xx = int(x + w/3)
                yy = int(y + h/2)
                transform = "transform='rotate(-90,"+str(xx)+","+str(yy)+")'"                    
            else :
                xx = int(x - w/2)
                yy = int(y + h/3)
                transform =""
                
            # content for pattern
            content = [ xx, yy, self._font.getSize(o) , style, transform, o, "\n"]
            
            outfile.write(self._pattern.getElement(content))
            
        outfile.write(self._pattern.getFooter())
        outfile.write("<!-- size = " + str(int(max(maxx-minx,maxy-miny))) +" (should be <= 800, otherwise change viewbox and translate param in svg -->" )
        return

    def getExt(self):
        return ".svg"


def cloudTag(infile, outfileName):
    print("ctspiral")
    configfile = ctlib.getScriptDir()+"/cfg/config.cfg"

    if(not (os.path.isfile(configfile))):
        ctlib.createDefaultConfig()
        
    config = ctlib.getConfig(configfile)

    # read config values
    maxWords = int(config['words']['max'])
    maxSize = int(config['font']['max'])
    minSize = int(config['font']['min'])
    
    patternsplitter = config['pattern']['split']
    patternbase = ctlib.getScriptDir()+"/"+ config['pattern']['base']
    
    # create outputter instances
    out = svgcloud(patternbase + config['pattern']['svg'] , patternsplitter, config)
    
    # read histogram
    B = ctlib.readPlain(infile, maxWords)
    
    # create output
    outfile = open(outfileName + out.getExt(), "w")
    out.createCloud(B, maxSize, minSize, maxWords, outfile)
    outfile.close()
    

def helpScreen():
    print("""\
 spiral cloud tag generator :-)
  usage: """+ __file__ +""" infile [outfile]
   
   params:
    infile   file to visualize
    outfile  optional output file name without extension 
   
   config: see cfg/config.cfg 
   
   example: 
    run 
         $""" + __file__ + """ test.txt 
    creates a svg spiral tag cloud based on test.txt and
    save it as test.txt_.svg

 infos: Steve Göring, stg7@gmx.de, 2012
""")

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
        print("\n error: file '"+args[0]+"' not exists")
        return 1
    
    try:
        if(len(args)==1):
            cloudTag(args[0], args[0]+"_")
            return 0
                        
        if(len(args)==2):
            cloudTag(args[0],args[1])
            return 0

            
    except Exception as e:
        _,errormsg = e
        print("Error: " + e)
        return 1
if __name__ == "__main__":
    main(sys.argv[1:])


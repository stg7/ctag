#!/usr/bin/python
# -*- coding: utf8 -*-
import os,sys,codecs,re

# color consts
color_blue = "\033[94m"
color_green = "\033[92m"
color_red = "\033[91m"
color_end = "\033[0m"


def copy(outdir):
    if(not os.path.isdir(outdir)):
        os.system("mkdir " + outdir )
    
    os.system("rsync -a --delete * " + outdir + "/ --exclude=\"build.py\" --exclude=\"docu\" --exclude=\"src\" --exclude=\"" + outdir +"\"") 
    

def build(outdir, infile):  
    
    copy(outdir)
    
    name = infile[0:-4]
    olddir = os.getcwd()
    os.chdir(outdir)
    tmpfile = name + ".tmp.tex"    
    # move main.tex to tmp file
    os.system("mv " + infile + " " + tmpfile)
    
    # preprocess main file 
    os.system("python " + tmpfile + " > " + infile)
#    print(".")    
    # do it
    a = True
    a = a and (os.system("pdflatex " + infile + " " ) == 0 ) 
#    print(".")    
    a = a and (os.system("bibtex " + name + " " ) +1  ) 
#    print(".")    

    a = a and (os.system("pdflatex " + name + " " ) == 0 )
#    print(".")    

    a = a and (os.system("pdflatex " + name + " " ) == 0 ) 
#    print(".")    
    os.chdir(olddir)
#    if(a):
#	print( color_blue + " build done" + color_end)
#    else:
#        print( color_red  + " build fail" + color_end)

def clean(outdir):
    os.system("rm -rf " + outdir )
    
def dist(outdir, infile):
    # first build
    build(outdir, infile)
    
    name = infile[0:-4]
    # create other file formats: 
    # postscript
    #os.system("pdf2ps " + name + ".pdf")
    
    # pdf to plain html
    #ps2ascii
    # cleanup files
    
    os.chdir(outdir)
    #remoove all aux files
    os.system("find . -type f -name \"*.aux\" -exec rm -rf {} \;")
    # all log
    os.system("find . -type f -name \"*.log\" -exec rm -rf {} \;")
    os.system("find . -type f -name \"*.lof\" -exec rm -rf {} \;")
    # all out
    os.system("find . -type f -name \"*.out\" -exec rm -rf {} \;")
    os.system("find . -type f -name \"*.bbl\" -exec rm -rf {} \;")
    os.system("find . -type f -name \"*.blg\" -exec rm -rf {} \;")
    os.system("find . -type f -name \"*.toc\" -exec rm -rf {} \;")
    
    # all sh quark
    os.system("find . -type f -name \"*.sh\" -exec rm -rf {} \;")

    
    tmpfile = name + ".tmp.tex"    
    os.system("rm -rf "+tmpfile)
    
    buildInst = open("build.sh","w")
    buildInst.write("pdflatex "+infile + "\n")
    buildInst.write("bibtex "+name + "\n")
    buildInst.write("pdflatex "+name + "\n")
    buildInst.write("pdflatex "+name + "\n")
    buildInst.write("find . -type f -name \"*.aux\" -exec rm -rf {} \;\n")
    buildInst.write("find . -type f -name \"*.log\" -exec rm -rf {} \;\n")
    buildInst.write("find . -type f -name \"*.lof\" -exec rm -rf {} \;\n")
    buildInst.write("find . -type f -name \"*.out\" -exec rm -rf {} \;\n")
    buildInst.write("find . -type f -name \"*.bbl\" -exec rm -rf {} \;\n")
    buildInst.write("find . -type f -name \"*.blg\" -exec rm -rf {} \;\n")
    buildInst.write("find . -type f -name \"*.toc\" -exec rm -rf {} \;\n")
    
    
    buildInst.close()
    
    

def main(argv):
    outdir = "out"
    infile = "main.tex"
    if(len(argv) > 0 ):
        if(argv[0] == "clean"):
            clean(outdir)
        if(argv[0] == "copy"):
            copy(outdir)
        if(argv[0] == "build"):
            build(outdir, infile)    
    else: # default case distribution
        dist(outdir, infile)
    
    

if __name__ == "__main__":
    main(sys.argv[1:])




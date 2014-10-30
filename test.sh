#!/bin/bash

rm -rf out
mkdir out
# single files
./ct.py  in/gutenberg.org/goethe/faust.txt out/faust


# recursive
./ct.py  in/freiesMag/ out/freiesmag
./ct.py  in/wikipedia/startrek/ out/startrek -r -e *.txt
./ct.py  in/wikipedia/filme/ out/filme -r -e *.txt


# do all , but set maxwords =300
cp cfg/config.cfg cfg/config.old
config=$(cat <<EOT
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
max = 300
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
min = 001122
max = 0000FF
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
EOT
)
echo "$config" > cfg/config.cfg
./ct.py  in/ out/all -r -e *.txt
# restore old settings
mv cfg/config.old cfg/config.cfg

    



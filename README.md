ctag
====

Requirements
------------

In general you need:

* python3,
* python3-tk
* python3-venv
* pdftotext (for pdf support)


old
-----------------------

ctag
====
ctag is a tag-cloud generator written in python 3.2 for the 5. coding contest of http://www.freiesmagazin.de/.

parts
-----
ctag consists of 6 main scripts:

* ct.py: all in one script
* ctana.py: text analysis
* ctlib.py: core functions
* ctmerge.py: merging of multiple input files
* ctsimple.py: simple html based output format, for debugging
* ctspiral.py: spiral layout

working process
---------------
The "ct.py" script is the main script for creating a new tag cloud:

* first: analyse input text (maybe merge files)
* second: build .plain histogram
* third: build selected output format (svg, html or both)

more
----
for more informations about ctag, read the minimalistic german manual

PDF Support
-----------
For pdf as input format please use tools like `pdftotext` for extraction of plain ascii text.
For pdf output, you can use the provided bash script `convert_svg_to_pdf.sh`, it requires inkscape.


ctag
====
ctag is a tag-cloud generator, a first version was written for the 5. coding contest of http://www.freiesmagazin.de/, but i rewrote most parts.

Requirements
------------

In general you need:

* python3,
* python3-tk
* python3-venv
* pdftotext (for pdf support as input)
* inkscape (for pdf support as output)

Example:
--------
Run:
```
./ctag.sh in/ascii --pdf_output
```

Usage
-----
Just run `./ctag.sh -h`:
```
usage: ctag.py [-h] [--cpu_count CPU_COUNT] [--output_file OUTPUT_FILE]
               [--remove_stop_words] [--min_freq MIN_FREQ] [--min_len MIN_LEN]
               [--language LANGUAGE] [--pdf_output] [--debug]
               inputfile [inputfile ...]

ctag - tag cloud generator

positional arguments:
  inputfile             input file

optional arguments:
  -h, --help            show this help message and exit
  --cpu_count CPU_COUNT
                        cpus/threads that are used for processing (default: 2)
  --output_file OUTPUT_FILE
                        outputfile for storing tag cloud (default: cloud.svg)
  --remove_stop_words   remove stopswords (default: True)
  --min_freq MIN_FREQ   minimum freq of a word (default: 4)
  --min_len MIN_LEN     minimum length of a word (default: 2)
  --language LANGUAGE   language in which the text is (default: german)
  --pdf_output          build a pdf file (default: False)
  --debug               debug mode (e.g. store intermediate results) (default:
                        False)


```


pdflatex main.tex
bibtex main
pdflatex main
pdflatex main
find . -type f -name "*.aux" -exec rm -rf {} \;
find . -type f -name "*.log" -exec rm -rf {} \;
find . -type f -name "*.lof" -exec rm -rf {} \;
find . -type f -name "*.out" -exec rm -rf {} \;
find . -type f -name "*.bbl" -exec rm -rf {} \;
find . -type f -name "*.blg" -exec rm -rf {} \;
find . -type f -name "*.toc" -exec rm -rf {} \;

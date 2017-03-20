MAIN = main

all:
	pdflatex $(MAIN).tex
	bibtex   $(MAIN)
	pdflatex $(MAIN).tex
	pdflatex $(MAIN).tex
clean:
	rm -rf *.aux *.brf *.log *.out *.bbl *.blg *.thm *.synctex.gz

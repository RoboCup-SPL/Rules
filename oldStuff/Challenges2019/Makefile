# Paper Makefile (with bibtex, archive, and diff)


BIB_DIR = ./bibs
# Name old versions of your paper with .old.tex if you want diff functionality

FILENAME = Challenges2019

TARGET = $(FILENAME).pdf $(FILENAME).ps

VIEWER = xpdf
LATEX = latex
PS = dvips
PS2PDF = ps2pdf
PDFLATEX = pdflatex
BIBTEX = bibtex
GZIP = gzip
PUBINFO = pubinfo.yml
BANNER = banner.rb
DIFF_UTIL = ./latexdiff
OLD_FILE = $(FILENAME).old.tex
DIFF_FILENAME = $(FILENAME)-diff
PDFS = $(FILENAME).pdf $(DIFF_FILENAME).pdf
PSES = $(FILENAME).ps $(DIFF_FILENAME).ps
DVIS = $(FILENAME).dvi $(DIFF_FILENAME).dvi

all: $(TARGET)

archive: $(FILENAME).ps
	$(BANNER) $(PUBINFO) $(FILENAME).ps
	$(PS2PDF) -dPDFSETTINGS=/prepress $(FILENAME).ps
	$(GZIP) $(FILENAME).ps

diff: $(DIFF_FILENAME).pdf $(DIFF_FILENAME).ps
	rm -f $(DIFF_FILENAME).log $(DIFF_FILENAME).aux $(DIFF_FILENAME).nav $(DIFF_FILENAME).snm $(DIFF_FILENAME).out $(DIFF_FILENAME).toc $(DIFF_FILENAME).bbl $(DIFF_FILENAME).blg $(DIFF_FILENAME).rel $(DIFF_FILENAME).tex $(DIFF_FILENAME).dvi

$(PDFS): %.pdf: %.ps 
	$(PS2PDF) -dPDFSETTINGS=/prepress $<

$(PSES): %.ps: %.dvi
	$(PS) -t letter -Ppdf -G0 -o $@ $<

$(DVIS): %.dvi: %.tex
	$(LATEX) $<
	$(BIBTEX) $*
	$(LATEX) $<
	$(LATEX) $<

$(DIFF_FILENAME).tex: $(OLD_FILE) $(FILENAME).tex 
	$(DIFF_UTIL) $^ > $@

view: $(FILENAME).pdf
	$(VIEWER) $(FILENAME).pdf &

clean:
	rm -f $(DVIS) $(PSES) $(PDFS) $(FILENAME).log $(FILENAME).aux $(FILENAME).nav $(FILENAME).snm $(FILENAME).out $(FILENAME).toc $(FILENAME).bbl $(FILENAME).blg $(FILENAME).rel $(DIFF_FILENAME).log $(DIFF_FILENAME).aux $(DIFF_FILENAME).nav $(DIFF_FILENAME).snm $(DIFF_FILENAME).out $(DIFF_FILENAME).toc $(DIFF_FILENAME).bbl $(DIFF_FILENAME).blg $(DIFF_FILENAME).rel $(DIFF_FILENAME).tex *~

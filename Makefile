%.tex: %.regl
	./regl2tex $< $@

%.idx: %.tex
	pdflatex $<

%.ind: %.idx
	makeindex $<

%.pdf: %.tex %.ind
	pdflatex $<

.PHONY:

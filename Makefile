%.tex: %.regl
	./regl2tex $< $@

%.pdf: %.tex
	pdflatex $<

.PHONY:

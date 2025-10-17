.PHONY: all clean

all: descriptions.pdf flashcards.pdf

descriptions.pdf: descriptions.tex
	lualatex descriptions.tex

flashcards.pdf: flashcards.tex
	lualatex flashcards.tex

clean:
	rm --force descriptions.pdf descriptions.aux descriptions.log flashcards.pdf flashcards.aux flashcards.log

help:
	grep '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\), \(.*\)/\1, \2\t\3/' | expand -t30
.SILENT: help
.PHONY: help # h, print help and exit

h: help

clean:
	poetry env remove --all
.PHONY: clean # rm, clean all

rm: clean

install:
	poetry install
.PHONY: install # i, install dependencies

i: install

run:
	poetry run bash -c "jupyter-lab"
.PHONY: run # r, run program

r: run

# Investigación reproducible: determinantes del precio de la vivienda en España
# make all = data -> clean -> models -> report.  Las descargas se cachean en data/raw
# (FORCE=1 make data para volver a descargar).
PY ?= python3
FETCH  := $(sort $(wildcard src/fetch_*.py))
MODELS := $(sort $(wildcard src/f[2-6]_*.py))

.PHONY: all data clean models report distclean

all: data clean models report

data:
	@for s in $(FETCH); do echo ">> $$s"; $(PY) $$s || exit 1; done

clean:
	$(PY) src/build_dataset.py

models:
	@for s in $(MODELS); do echo ">> $$s"; $(PY) $$s || exit 1; done

report:
	@if [ -f src/report.py ]; then $(PY) src/report.py; else echo "report: src/report.py aún no existe"; fi

distclean:
	rm -rf data/processed/* output/*

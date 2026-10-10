# Investigación reproducible: determinantes del precio de la vivienda en España
# make all = data -> clean -> models -> report.  Las descargas se cachean en data/raw
# (FORCE=1 make data para volver a descargar).
PY ?= python3
FETCH  := $(sort $(wildcard src/fetch_*.py)) $(sort $(wildcard src/extract_*.py))
MODELS := $(sort $(wildcard src/f[2-6]_*.py)) $(sort $(wildcard src/v2/*_run.py src/v2/*_main.py))
# v2: solo los puntos de entrada de cada rama (<rama>_run.py o <rama>_main.py), que llaman a sus módulos
# Determinismo numérico: un solo hilo en BLAS/OpenMP (el control sintético dependía del nº de hilos)
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1

.PHONY: all data clean models report distclean

all: data clean models report

data:
	@for s in $(FETCH); do echo ">> $$s"; $(PY) $$s || exit 1; done

clean:
	flock data/processed/.clean.lock $(PY) src/build_dataset.py
	flock data/processed/.clean.lock $(PY) src/build_dataset_v2.py
	$(PY) src/holdout.py build

models:
	@mkdir -p output; for s in $(MODELS); do echo ">> $$s"; flock output/.models.lock $(PY) $$s || exit 1; done

report:
	@if [ -f src/report.py ]; then $(PY) src/report.py; else echo "report: src/report.py aún no existe"; fi

distclean:
	rm -rf data/processed/* output/*

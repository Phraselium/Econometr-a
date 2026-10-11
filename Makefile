# Investigación reproducible: determinantes del precio de la vivienda en España
# make all = data -> clean -> models -> report.  Las descargas se cachean en data/raw
# (FORCE=1 make data para volver a descargar).
PY ?= python3
V3_ORDEN := pa_run pb_run pot_run gl_run c1_run c3_run holm_v3 pd_run
V4_ORDEN := m0_run m2_run m1_run m3_run m4_run m7_run m5_run
V5_ORDEN := r1t_run r1c_run r1a_run r1b_run a23_run a4_run a5_run a5_validacion a5_hechos b1_run b2_run b3_potencia b3_run b4_run ca_run cb_run cc_run d1_run d2_run ../v5_1/t1_run ../v5_1/t2_run ../v5_1/t3_run ../v5_1/t4_run e_hechos cifras_clave d3_run cifras_clave render
V6_ORDEN := m0_run m1a_run m1b_run m2_run m3a_run m3a_bayes m3a_dl m3a_informe m3b_run m4_run
# v6.1: reanálisis (lee JSON versionados) y, al final, cifras_clave + render para recoger hechos de v6/v6.1
V6_1_ORDEN := k1_run k2_inmigracion k4b_run ../v5/cifras_clave ../v5/render k4b_comparar
FETCH  := $(sort $(wildcard src/fetch_*.py)) $(sort $(wildcard src/extract_*.py))
MODELS := $(sort $(wildcard src/f[2-6]_*.py)) $(foreach r,ba_run bv_main bi_run bo_run bp_main bm_run bd_run bs_run,$(wildcard src/v2/$(r).py))
# v3: puntos de entrada en orden (se añaden al aprobarse cada diseño); el verificador y los informes al final
MODELS_V3 := $(foreach r,$(V3_ORDEN),$(wildcard src/v3/$(r).py))
MODELS_V4 := $(foreach r,$(V4_ORDEN),$(wildcard src/v4/$(r).py))
MODELS_V5 := $(foreach r,$(V5_ORDEN),$(wildcard src/v5/$(r).py))
MODELS_V6 := $(foreach r,$(V6_ORDEN),$(wildcard src/v6/$(r).py))
MODELS_V6_1 := $(foreach r,$(V6_1_ORDEN),$(wildcard src/v6_1/$(r).py))
# v2: solo los puntos de entrada de cada rama, en ORDEN de dependencia (BD lee BA/BV/...; BS lee todo)
# Determinismo numérico: un solo hilo en BLAS/OpenMP (el control sintético dependía del nº de hilos)
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1

.PHONY: all data clean models report distclean check verificador

all: data clean models report

data:
	@for s in $(FETCH); do echo ">> $$s"; $(PY) $$s || exit 1; done

clean:
	flock data/processed/.clean.lock $(PY) src/build_dataset.py
	flock data/processed/.clean.lock $(PY) src/build_dataset_v2.py
	$(PY) src/holdout.py build

models:
	@mkdir -p output; for s in $(MODELS) $(MODELS_V3) $(MODELS_V4) $(MODELS_V5) $(MODELS_V6) $(MODELS_V6_1); do echo ">> $$s"; flock output/.models.lock $(PY) $$s || exit 1; done

report:
	@if [ -f src/report.py ]; then $(PY) src/report.py; else echo "report: src/report.py aún no existe"; fi
	@$(MAKE) --no-print-directory verificador

check:
	ruff check src tests --quiet
	$(PY) -m pytest -q tests
	$(PY) src/v3/check_texto.py
	$(PY) src/v5/check_v5.py
	$(PY) src/v6/check_v6.py

verificador:
	@if [ -f src/v3/verificador.py ]; then $(PY) src/v3/verificador.py; fi
	@if [ -f src/v4/verificador.py ]; then $(PY) src/v4/verificador.py; fi
	@if [ -f src/v5/verificador.py ]; then $(PY) src/v5/verificador.py; fi

distclean:
	rm -rf data/processed/* output/*

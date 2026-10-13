# Investigación reproducible: determinantes del precio de la vivienda en España
# make all = data -> clean -> models -> report.  Las descargas se cachean en data/raw
# (FORCE=1 make data para volver a descargar).
PY ?= python3
V3_ORDEN := pa_run pb_run pot_run gl_run c1_run c3_run holm_v3 pd_run
V4_ORDEN := m0_run m2_run m1_run m3_run m4_run m7_run m5_run
V5_ORDEN := r1t_run r1c_run r1a_run r1b_run a23_run a4_run a5_run a5_validacion a5_hechos b1_run b2_run b3_potencia b3_run b4_run ca_run cb_run cc_run d1_run d2_run ../v5_1/t1_run ../v5_1/t2_run ../v5_1/t3_run ../v5_1/t4_run e_hechos cifras_clave d3_run cifras_clave render
V6_ORDEN := m0_run m1a_run m1b_run m2_run m3a_run m3a_bayes m3a_dl m3a_informe m3b_run m4_run
# v6.1: reanálisis (lee JSON versionados) y, al final, cifras_clave + render para recoger hechos de v6/v6.1
# v6.2: déficit con correcciones alternativas de la EPA (L3) y su ficha; van antes de V6_1 (que cierra con cifras_clave y render)
V6_2_ORDEN := l3_deficit l3_ficha l1_verifica ../v6_3/ver_hechos
V6_1_ORDEN := k1_run k2_inmigracion k3_run k6_fichas k4b_run ../v5/cifras_clave ../v5/render k4b_comparar k4c_cifras k4d_docs ../v6_2/l5_publicables
FETCH  := $(sort $(wildcard src/fetch_*.py)) $(sort $(wildcard src/extract_*.py))
MODELS := $(sort $(wildcard src/f[2-6]_*.py)) $(foreach r,ba_run bv_main bi_run bo_run bp_main bm_run bd_run bs_run,$(wildcard src/v2/$(r).py))
# v3: puntos de entrada en orden (se añaden al aprobarse cada diseño); el verificador y los informes al final
MODELS_V3 := $(foreach r,$(V3_ORDEN),$(wildcard src/v3/$(r).py))
MODELS_V4 := $(foreach r,$(V4_ORDEN),$(wildcard src/v4/$(r).py))
MODELS_V5 := $(foreach r,$(V5_ORDEN),$(wildcard src/v5/$(r).py))
MODELS_V6 := $(foreach r,$(V6_ORDEN),$(wildcard src/v6/$(r).py))
MODELS_V6_1 := $(foreach r,$(V6_1_ORDEN),$(wildcard src/v6_1/$(r).py))
MODELS_V6_2 := $(foreach r,$(V6_2_ORDEN),$(wildcard src/v6_2/$(r).py))
# v2: solo los puntos de entrada de cada rama, en ORDEN de dependencia (BD lee BA/BV/...; BS lee todo)
# Determinismo numérico: un solo hilo en BLAS/OpenMP (el control sintético dependía del nº de hilos)
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1

.PHONY: all data clean models report distclean check verificador v7 v7_1 v7_2 evaluate_v7 publicacion v8 evaluate_v8 consulta datos_terceros

all: data clean models report

data:
	@for s in $(FETCH); do echo ">> $$s"; $(PY) $$s || exit 1; done

clean:
	flock data/processed/.clean.lock $(PY) src/build_dataset.py
	flock data/processed/.clean.lock $(PY) src/build_dataset_v2.py
	$(PY) src/holdout.py build

models:
	@mkdir -p output; for s in $(MODELS) $(MODELS_V3) $(MODELS_V4) $(MODELS_V5) $(MODELS_V6) $(MODELS_V6_2) $(MODELS_V6_1); do echo ">> $$s"; flock output/.models.lock $(PY) $$s || exit 1; done

report:
	@if [ -f src/report.py ]; then $(PY) src/report.py; else echo "report: src/report.py aún no existe"; fi
	@$(MAKE) --no-print-directory verificador

check:
	ruff check src tests --quiet
	$(PY) -m pytest -q tests
	$(PY) src/v3/check_texto.py
	$(PY) src/v5/check_v5.py
	$(PY) src/v6/check_v6.py
	$(PY) src/v8/check_v8.py

verificador:
	@if [ -f src/v3/verificador.py ]; then $(PY) src/v3/verificador.py; fi
	@if [ -f src/v4/verificador.py ]; then $(PY) src/v4/verificador.py; fi
	@if [ -f src/v5/verificador.py ]; then $(PY) src/v5/verificador.py; fi

distclean:
	rm -rf data/processed/* output/*

# V7: atlas econométrico regional (sin red; determinista). Orden en V7_ORDEN (src/v7/<modulo>.py).
V7_ORDEN := r1_panel r2_montecarlo r2_mc3 r4a_run r4b_run r5_prediccion r6_propuestas r7_fichas r7_atlas
v7:
	@for r in $(V7_ORDEN); do echo ">> src/v7/$$r.py"; $(PY) src/v7/$$r.py || exit 1; done
	@$(MAKE) --no-print-directory v7_1

# V7.1: consolidación (sin análisis nuevo): dosis y coste sobre R6 y entregables; después cifras_clave y render
V7_1_ORDEN := ../v7_2/ficha_burbuja s1_dosis_coste s1_atlas s3_hechos s4_ensayo
v7_1:
	@for r in $(V7_1_ORDEN); do echo ">> src/v7_1/$$r.py"; $(PY) src/v7_1/$$r.py || exit 1; done
	$(PY) src/v5/cifras_clave.py
	$(PY) src/v5/render.py
	$(PY) src/v6_2/l5_publicables.py
	$(PY) src/v7_1/s6_paquete.py

# V7.2: reverificación del GSADF nacional (mismo método y semilla que v5 R1B). Necesita el panel completo de `make clean`
# (src/holdout.py load_full); su salida (output/v7_2/gsadf/reverificacion.csv) está versionada y la lee `make v7_1`.
v7_2:
	$(PY) src/v7_2/gsadf_reverifica.py

# V7.1: publicacion/, metodologia/ y reproducir/ se generan desde output/ y docs/ (nunca a mano; tests/v7_1/test_publicacion.py)
publicacion:
	$(PY) src/v7_1/publicacion.py

# Validación limpia diferida de V7: CON red, UNA sola vez, tras la release del pre-registro (docs/v7/notas_release.md)
evaluate_v7:
	$(PY) src/v7/evaluate_v7.py

# V8: datos (F1) y, al añadirse, herramientas y modelos. Orden en V8_ORDEN (src/v8/<modulo>.py); añadir módulos al final de la lista.
V8_ORDEN := f1_paneles m0_periodos m1_factor_comun m2_svar m3_periodos_var m4_largo_plazo m5_lpiv m6_colinealidad m7_multiverso m8_regional m9_ml f5_atribucion f6_congelar f6_tablas f6_hechos f6_verificador
# V8.1: datos de terceros retirados del repositorio (docs/v8_1/datos_retirados.md): descarga y verifica sha256.
# Necesario antes de `make all` en un clon limpio. Sin red, solo verifica.
datos_terceros:
	$(PY) src/v8_1/datos_terceros.py

# V8.1: capa de consulta (consulta/ y llms.txt; nunca a mano; tests en tests/consulta)
consulta:
	$(PY) src/consulta/generar.py

# Validación limpia diferida de V8: CON red, UNA sola vez, tras la release del pre-registro (docs/v8/notas_release.md)
evaluate_v8:
	$(PY) src/v8/evaluate_v8.py

v8:
	@for r in $(V8_ORDEN); do echo ">> src/v8/$$r.py"; $(PY) src/v8/$$r.py || exit 1; done
	$(PY) src/v5/cifras_clave.py
	$(PY) src/v8/render_v8.py

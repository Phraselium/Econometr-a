# Revisión independiente del módulo R de v5 (R1T, R1A, R1B, R1C)

Fecha: 2026-10-10. Revisor independiente (no participó en el trabajo). Alcance: output/v5/R1{A,B,C,T}, src/v5/r1*_run.py y sus auxiliares, secciones R1 de docs/v5/fuentes_fallidas.md, ERRATA.md y docs/v5/backlog.md. No se ejecutó `make all` ni se leyó data/sealed.

## Comprobaciones ejecutadas

| Comprobación | Resultado |
|---|---|
| `r1t_run.py`, `r1c_run.py`, `r1a_run.py` dos veces, sin red (HTTPS_PROXY=http://127.0.0.1:9) | exit 0 en las 6 ejecuciones; md5 de todos los ficheros (salvo PNG) de R1A, R1C y R1T idénticos entre sí y a la versión confirmada; `git status` sin cambios en output/v5/R1* (también PNG) |
| `r1b_run.py` | no ejecutado (por indicación); revisión estática |
| `python3 src/v3/check_texto.py` | 0 errores |
| `python3 src/v5/check_v5.py` | 24 errores, **todos de A5** (trabajo en curso, ficheros sin confirmar); ninguno de R1 |
| `ruff check src/v5/r1*` | sin errores |
| Fórmula de Cinelli-Hazlett (src/v5/r1b_sens.py:41-46) | correcta: f = \|t\|/√gl; RV = ½(√(f⁴+4f²) − f²); RV_α con f* = f − t_{α/2, gl−1}/√(gl−1) y 0 si f* ≤ 0 (q = 1) |
| Semilla y registro | SEED=20261010 en todos los r1*; registros en R1A (9 specs, Holm), R1B (donut 320, sens 381, GSADF 51; Holm y BH por familia), R1C (Holm) |

## Respuesta a las preguntas del encargo

1. **Tenencia en propiedad 72-76 % como C1.** Aceptable. EFF 2022 (BdE, encuesta de riqueza), ECV 2022 (INE, encuesta de condiciones de vida, tabla 9994 en «% de hogares») y Censo 2021 (INE, censo basado en registros, viviendas principales = hogares) tienen productor o instrumento distintos y miden el mismo concepto (hogar con vivienda principal en propiedad). El rango es de 3,8 pp. Por tramos de edad no coinciden (5,4-6,4 pp a partir de 65 años) y quedan en C4 con ambas cifras: correcto. Faltan dos cosas: declarar la tolerancia de 5 pp como regla y no como umbral del código, y anotar las diferencias de fecha y concepto (ver N1).
2. **Rótulos del donut, la sensibilidad y el GSADF.** Los tres son C4, EXPLORATORIO, y el veredicto de R1B-V1 es ANALIZADA, NO CONCLUYENTE: correcto, sin promoción de capa. El donut da las dos fuentes aunque el signo de la especificación principal discrepa (tasado −0,044; SERPAVI +0,161), y Holm sobre 320 especificaciones no deja ninguna significativa. La sensibilidad de BP-H5 se rotula «colapsada, NO es el SDiD»: correcto.
3. **No residentes y precio.** La capa y el veredicto son correctos (C4; ANALIZADA, NO CONCLUYENTE). El problema está en la redacción: «desaparece» y «costa e islas confunden» o «refleja concentración común… no un efecto» afirman un mecanismo que no se ha probado. Con N = 50, el IC95 con controles, [−0,55; 0,59] % por punto, no excluye un 60 % del coeficiente bivariado (0,96). Ver B3.
4. **Supuestos explícitos.** Están declarados los radios (15/25/40/60 km), el sustituto de las áreas urbanas (capital o municipio con mayor parque, porque el Atlas devolvió 403), la fórmula propia de Cinelli-Hazlett y las cotas de la discrepancia VUT. Sin embargo, la descomposición de la discrepancia VUT es internamente incoherente (B2).
5. **Backlog.** No se ha actualizado tras R1 (B1).

## Hallazgos

| # | Tipo | Fichero:línea | Hallazgo | Corrección propuesta |
|---|---|---|---|---|
| B1 | **Bloqueante** | docs/v5/backlog.md:73-89 y 91-112 | La «Lista mínima R1» y el orden propuesto siguen en el estado de R0. Constan como «no hecho» el donut, el Notariado (BK-045) y los distritos SERPAVI (BK-046), que ya están hechos, y GSADF y Oster/CH, que ahora están parcialmente hechos. No se dice qué queda abierto tras R1 ni por qué: BK-014 (sin prueba de red), BK-017 (MESVAL), BK-040 (BO H4 no ejecutado), BK-009 (afiliación a la SS sin localizar), BK-034 (sin sección censal), BK-002 (sigue en C4, fuente única efectiva) y BK-038, 042, 048, 050 y 051 (no abordados). | Añadir la columna «Estado tras R1» (hecho / parcial / no abordado), con la ruta de la evidencia y, para lo no resuelto, el motivo y el coste revisado. Corregir la lista mínima. |
| B2 | **Bloqueante** | src/v5/r1a_run.py:316-323; output/v5/R1A/tablas/vut_discrepancia_descomposicion.csv; docs/v5/estado.md:9 | El factor «bajas no depuradas» se rotula como *cota inferior*, pero entra como valor puntual (mín = máx = 0,26). Con eso se deduce que el residual de definición está entre 0,528 y 0,74. Si las bajas son solo una cota inferior, el residual solo tiene cota superior (≤ 0,74), y el «53-74 % del log» de estado.md no está identificado. Además, f_bajas mezcla las bajas no depuradas con las bajas reales de 22 meses (fechas distintas). | Opción (a): dar el residual como «≤ 0,74», con el mínimo no identificado. Opción (b): justificar que 0,26 es un valor puntual y quitar el rótulo «cota inferior». En ambos casos, propagar el cambio a estado.md:9 y a las notas de R1A. |
| B3 | **Bloqueante** | src/v5/r1a_run.py:375, 384, 429 (ficha R1A-V1 «limites»; resultado.json «notas», «spec_curve»); docs/v5/estado.md:9 | «Desaparece», «costa e islas confunden» y «la bivariada refleja concentración común de costa e islas, no un efecto» atribuyen la asociación a un factor de confusión. Eso es una afirmación de mecanismo que no se ha probado con 50 unidades: costa e islas pueden ser a la vez factor de confusión y canal, porque el peso de no residentes es casi una función de la costa. | Redactar así: «con renta, población y costa/islas, el coeficiente deja de ser distinguible de cero (0,02 %; IC95 −0,55 a 0,59; p Holm = 1). El intervalo no excluye ni 0 ni un 60 % del coeficiente bivariado. Con N = 50 y la colinealidad con costa/islas, no se puede separar la asociación del peso de no residentes de la de la localización costera». |
| N1 | No bloqueante | src/v5/r1c_run.py:80; output/v5/R1C/hechos.json (R1C-001) | La regla C1 por «rango ≤ 5 pp» está fijada en el código y no figura en decisiones.md. El campo fecha_dato es «2022», aunque el Censo es de 2021-11. | Registrar la tolerancia en docs/v5/decisiones.md y poner fecha_dato = «2021-11/2022». En la nota, indicar que EFF incluye la propiedad parcial y que el Censo y la ECV separan la cesión gratuita. |
| N2 | No bloqueante | src/v5/r1b_gsadf.py:219; src/holdout.py:208 | `holdout.load_full` se usa para un análisis C4 exploratorio, aunque su docstring lo limita a hechos C1 y cotas C2. El acceso queda registrado y todas las evaluaciones selladas de v2 ya están hechas, así que no hay fuga sobre hipótesis pendientes. | Anotar en decisiones.md que el uso se extiende a C4 y por qué. |
| N3 | No bloqueante | src/v5/r1b_sens.py:226-227 | En H6 se fija gl = 39 («n_donantes − 1») sin fuente: h6_sellado.json no trae el número de donantes. Hay una errata: «datos selladas». | Citar de dónde salen los 40 donantes (o leerlo del registro v2). Corregir a «datos sellados». |
| N4 | No bloqueante | src/v5/r1b_run.py:87 (ficha R1B-V1) | «Episodios que persisten» aparece justo después de decir que ningún cociente sobrevive a BH, lo que puede leerse como contradictorio. La ficha omite que IPV/renta también rechaza sin ajuste (p = 0,012; BH 0,08). | Redactar: «fechados sin ajuste múltiple: …». Añadir IPV/renta a la lista de rechazos sin ajustar. |
| N5 | No bloqueante | src/v5/r1a_run.py:2; r1c_run.py; r1t_run.py | El docstring dice «un solo hilo», pero solo lo garantiza el Makefile (líneas 16-18). Al ejecutar los scripts sueltos no se fija. | Copiar el bloque OMP/OPENBLAS/MKL = 1 de r1b_run.py:12. |
| N6 | No bloqueante | docs/v5/fuentes_fallidas.md, sección R1A | La sección no lleva fecha en el título y declara que no hubo prueba de red. A23 sí obtuvo después las fianzas de la GVA (sin duración del contrato). | Añadir la fecha y una referencia cruzada a A23. Mantener BK-014 abierto en el backlog (ver B1). |
| N7 | No bloqueante | output/v5/R1A/fichas_verificador.json (R1A-V1 «literatura») | «NO VERIFICADA… cuartil no verificado» es correcto. Ninguna referencia figura como VERIFICADA sin DOI y cuartil. | — |

Otros puntos sin incidencias:
- ERRATA.md: las tres entradas (BK-044, BK-045 y gva_vut .gz) tienen el formato pedido y no reescriben lo publicado.
- R1T: el supuesto 46250dd = distrito dd (19 = 19) está declarado. Es DESCRIPTIVO.
- Neutralidad: no se ha encontrado lenguaje valorativo ni partidista. Las fichas evalúan afirmaciones, no a quién las hace.

## Veredicto

**REHACER**, limitado a B1, B2 y B3. Las tres son correcciones de documentación y redacción de bajo coste (estimadas en menos de 15 mil tokens) y no hay que volver a estimar nada. Los resultados numéricos, las capas, los veredictos de las fichas, la reproducibilidad (R1A, R1C y R1T) y la fórmula de Cinelli-Hazlett son correctos. Los puntos N1-N7 pueden ir en la misma pasada o pasar al backlog.

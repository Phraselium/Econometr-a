# Revisión independiente del módulo C (v5): CA, CB y CC

Revisor: subagente independiente (opus). Fecha: 2026-10-10. Objeto: output/v5/{CA,CB,CC}, src/v5/c[abc]_*.py y las secciones CA, CB y CC de docs/v5/fuentes_fallidas.md. No se ejecutó `make all` ni se leyó data/sealed.

## Comprobaciones realizadas

| Comprobación | Resultado |
|---|---|
| `ca_run.py`, `cb_run.py` y `cc_run.py` ejecutados dos veces sin red (HTTPS_PROXY=http://127.0.0.1:9) | exit 0 en las seis ejecuciones; md5 idénticos entre ejecuciones y con lo versionado (`git status` sin cambios en output/v5/C*) |
| Entradas leídas | Las 35 de data/raw/v5/c[abc]_* y las 12 de data/raw usadas están versionadas en git; no hay red ni data/sealed en los `*_run.py` |
| `python3 src/v3/check_texto.py` / `python3 src/v5/check_v5.py` / `ruff` | 0 errores / 0 errores / pasa |
| Registro y FDR | CA: 36 contrastes de crédito con Holm (1 rechazo: g_inmobiliarias, retardo 8, p_Holm 0,032) más DM-HLN; CB: 6 Spearman con Holm (permutación 10.000, SEED 20261010); CC: 0 contrastes (declarado) |
| Comparación fuera de muestra | CA crédito: ADL frente a AR(4) en la misma muestra (n = 30, embargo 4), DM-HLN p = 0,57; ECM v1 declarado como no aplicable (es un modelo del precio). CB y CC no tienen modelo predictivo: es correcto |

## Hallazgos

| # | Tipo | Fichero:línea | Hallazgo | Corrección |
|---|---|---|---|---|
| B1 | **Bloqueante** | src/v5/cc_run.py:112-123, 194-198; output/v5/CC/fichas_verificador.json (CC-V2); output/v5/CC/hechos.json (CC-C2-*) | **CC-V2 no es una cota C2 y el veredicto PARCIALMENTE no está respaldado.** (a) El código no recorre el supuesto declarado de 15-30 años: el escenario base aplica 30 años a todo; el bajo solo quita la cohorte de 2005; el alto suma 15 años únicamente para las calificaciones de 2013-2020. Con L = 15 para las cohortes de 1996-2005, que es el extremo del supuesto (el RD 1/2002 solo impide la descalificación voluntaria durante 15 años), esas cohortes habrían salido en 2011-2020, no en 2026-2035. La salida en la ventana sería entonces muy inferior a 532.040. (b) La propia nota del resultado.json reconoce que la cota inferior lógica es 0 y que el alto no cubre plazos <15 años. (c) Lo que se cuantifica es la salida por fin de plazo supuesto, no la descalificación observada, que es lo que dice la afirmación. Un intervalo que depende de un plazo no documentado y no acota ni siquiera bajo su propio supuesto no cumple C2 (supuestos explícitos que acoten), y un veredicto PARCIALMENTE sobre una afirmación cuyo núcleo no se observa va más allá de lo que da la evidencia. | Opción preferida: capa C4 y veredicto «ANALIZADA, NO CONCLUYENTE»; presentar 532.040-669.394 como escenarios condicionados («si el plazo fuese 30 años…»), no como cota. Alternativa C2: intervalo [0; máximo bajo L ∈ {15,…,30} y por cohorte], con la cota inferior 0 explícita; aun así el veredicto no puede pasar de NO CONCLUYENTE, porque el intervalo incluye la ausencia de salidas. Pasar CC-C2-salidas-* y CC-C2-ratio a la capa resultante y actualizar `capa`/`nivel_evidencia` del resultado.json. Revisar si la comparación con las 11.265 calificaciones/año debe mantenerse en la magnitud (es válida solo condicionada al escenario). |
| B2 | **Bloqueante** (corrección de texto) | src/v5/ca_run.py:398 → output/v5/CA/resultado.json, campo `capa` | «el valor de España es C1 donde coincide con el INE» promueve de capa: Eurostat toma los datos de España del INE (lo reconocen las notas, la ficha CA-V1 y docs/v5/decisiones.md, sección C-a), así que no hay dos fuentes independientes. | Sustituir por «C4 (Europa; Eurostat y el INE no son independientes: el contraste es de coherencia)». |
| N1 | No bloqueante | src/v5/cb_run.py:293 (ficha CB-V1) | La ficha redondea p_Holm = 0,0525 (verbales posesorios) a «0.05», que se lee como significativo al 5 %, cuando no lo es. Además, omite C5-S1 (cuota del Censo; p_Holm 0,074) y las tres especificaciones en variación 2021-2025 (C5-S4 a S6; p_Holm = 1), que son las más próximas a la afirmación («reduce la oferta» es un cambio). | Dar p con tres decimales y «no significativa al 5 % tras Holm». Añadir: «en variaciones 2021-2025 no hay asociación (rho −0,10 a 0,17; p_Holm = 1)». Sustituir «contrario al de la afirmación» por «el signo de la asociación transversal no coincide con el que sugeriría la afirmación; una correlación entre CCAA no contrasta un efecto». La lectura prudente (urbanización como factor común, sin diseño) es correcta y debe mantenerse. |
| N2 | No bloqueante | src/v5/cb_run.py:290, 302 (ficha CB-V3) | La magnitud llama «cota superior del peso de las empresas» al residual, pero el campo `cota` dice «Sin cota (C4)». Además, la ficha da «16.9-38.1» sin nombrar los métodos. | Nombrar los métodos en la ficha: A, stock del Censo 2021 en régimen común = 16,9 %; B, ECV 2025 × ECH 2025T4 = 38,1 %. Indicar que discrepan y que se reportan ambos. En `cota`, poner «cota superior del residual PJ + sector público + no declarado (C4, supuestos: declaración completa en IRPF y stock constante 2021-2024)». |
| N3 | No bloqueante | src/v5/cc_run.py:152-161 | `fecha_dato` de CC-C2-salidas-* y CC-C2-ratio = «2026-10-10», que es la fecha de ejecución y no la del dato. | Poner la última calificación (2025) y la fecha del BOE más reciente usada. |
| N4 | No bloqueante | src/v5/cc_run.py:88, 92 | En CC-C7b-jov-prop y jov-cesion se usan min/max como «2015/último», con lo que queda min > max (34,2 > 30,6; 17,4 > 14,7). | Usar min()/max() reales o dejar null y poner el valor de 2015 en `notas`. |
| N5 | No bloqueante | src/v5/ca_run.py:171; output/v5/CA/hechos.json (CA-EU-crec_pob-nivel) | El contraste de coherencia de crec_pob falla la tolerancia (0,946 frente a 0,5) y, sin embargo, las fuentes dicen «Eurostat + INE (contraste de coherencia)». | Rotular «Eurostat (contraste con el INE fuera de tolerancia)» y citarlo en las notas. |
| N6 | No bloqueante | output/v5/CA/resultado.json (`pregunta`), registro.csv (`fase` C1_credito, C3_contado, C4_europa); CB/CC (C5…C8, C2) | La numeración de los ángulos (C1-C8) coincide con la de las capas (C1-C4). Así, «(C1) ¿El crédito…?» o «C2: viviendas protegidas» pueden leerse como capas. | Renombrar los ángulos (p. ej. «ángulo 1» o «A-C1») en `pregunta`, `fase` e ids. |
| N7 | No bloqueante | docs/v5/fuentes_fallidas.md:79-111 | CA y CC no tienen columna de edición (CB sí); la fecha solo figura en el encabezado. | Añadir la columna «Edición/fecha de prueba» en CA y CC. |
| N8 | No bloqueante | output/v5/CB/* (todo el módulo) | Texto sin tildes («seguridad juridica», «ocupacion», «Espana»); el formato de `evidencia` y `convenciones` difiere del de CA/CC (cadena frente a lista o dict). | Normalizar las tildes y el formato del de output/v4/M5/fichas_verificador.json. |
| N9 | No bloqueante | output/v5/CA/fichas_verificador.json (CA-V3) | `cota` dice «C2-like» con capa C4. No hay promoción, pero la etiqueta puede confundir. | «Escenarios con supuesto sobre phi (C4)». |

## Valoración por criterio

1. **Capas.**
   - CA-V1 a V3, CB-V1 a V3 y CC-V1: correctamente en C4 con «ANALIZADA, NO CONCLUYENTE»; las fichas no promueven de capa.
   - Las parejas Eurostat/INE, SILC/ECV e INE/Registradores (origen registral común) se tratan como no independientes en las fichas. La excepción es el campo `capa` del resultado.json de CA (B2).
   - CC-V2 no es aceptable como C2/PARCIALMENTE (B1).
2. **Interpretación.**
   - Seguridad jurídica: lectura prudente, salvo la selección y el redondeo de N1.
   - Contado: el 30-58 % está bien derivado (phi crítico = 50/70,05 = 71,4 %) y «inversora ≠ contado» está explícito.
   - Crédito: 1 de 36 tras Holm, signo negativo, descrito como asociación descriptiva. DM-HLN p = 0,57: no mejora a AR(4).
   - Europa: el criterio IQR, sostenido 3 y 5 años, está aplicado y documentado.
   - Empresas: los dos métodos se reportan en las tablas y en hechos (min/max), pero la ficha no los nombra (N2).
3. **Fuentes.** Los endpoints y resultados están documentados. Falta la columna de edición en CA y CC (N7). No hay fuentes no oficiales en C1 (no hay C1 en el módulo).
4. **Lenguaje y neutralidad.**
   - No hay léxico causal ni valorativo en las salidas: el único «frena» está en el enunciado citado.
   - «Ocupación ilegal» es la denominación del CGPJ.
   - Los veredictos se refieren a afirmaciones, sin atribuirlas a actores.
5. **Reproducibilidad.** Las ejecuciones son deterministas, las lecturas están versionadas, el registro está completo y Holm se aplica donde hay contrastes.

## Veredicto: **REHACER**

Prioridad:
1. B1: reclasificar CC-V2 (C4 o C2 con cota inferior 0) y bajar el veredicto a «ANALIZADA, NO CONCLUYENTE»; regenerar los hechos CC-C2-*.
2. B2: corregir el campo `capa` de output/v5/CA/resultado.json.
3. N1 y N2, temas sensibles: completar y precisar las fichas CB-V1 y CB-V3.
4. N3-N9.

Tras corregir B1 y B2 y volver a ejecutar `cc_run.py`/`ca_run.py` y `make check`, el módulo puede aprobarse sin otra revisión completa.

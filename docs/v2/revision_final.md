# Revisión final v2 (puerta BS): output/v2/informe_v2.md

Revisor independiente (opus). Rama r2/main, HEAD 4f7a42e (e8851f9 + `docs/v2/estado.md`). Fecha: 2026-10-10.

## Veredicto: **APROBAR, condicionado a C1-C4**

C1-C4 son cambios en el generador (`src/v2/bs_informe.py` y `bs_tablas.py`) y en el texto. No hay que reestimar nada, no hay fugas y no se toca ninguna evaluación sellada. Se verifican con un diff y una reejecución de `bs_run.py`. Si no se hacen, el veredicto pasa a REHACER. C5-C8 son recomendables, pero no bloquean.

## 1. Reproducción (clon aislado, sin red, 1 hilo)

- Clon con `git clone --no-hardlinks` en el scratchpad. Ejecuté `HTTPS_PROXY=HTTP_PROXY=http://127.0.0.1:9`, `OMP/OPENBLAS/MKL_NUM_THREADS=1`, y `python3 src/v2/holm7.py` seguido de `python3 src/v2/bs_run.py`, dos veces.
- Las cuatro ejecuciones terminaron con exit 0. Comparé los md5 de 12 ficheros: `BS/holm7.csv`, `holm7_verificacion.csv`, `resultado.json`, `registro.csv`, `contribuciones_periodo.png`, `informe_v2.md` y los 6 `tablas/*.csv`. **Coinciden entre las dos ejecuciones y con la versión versionada.** `git status` queda limpio.
- BS solo lee `output/v2/*` y `docs/*`. No hay referencias a `data/sealed` ni a la red. Holm-7 recalculado a mano: 0,013986×7 = 0,0979; 0,0294×6 = 0,1764; 0,0463×5 = 0,2315; 0,1947×4 = 0,7787; el resto, 1. **Correcto**: ninguna hipótesis sobrevive.
- `docs/v2/hipotesis.md` no ha cambiado desde 910c42a (diff vacío).
- `holdout_accesos.md` registra exactamente 4 aperturas: H1, H2, H6 y H7. Cada una tiene su APERTURA anotada antes del resultado. No hay segundos intentos.

## 2. Trazabilidad (15 cifras comprobadas, todas coinciden)

| Cifra del informe | Origen | OK |
|---|---|---|
| H1: 20-34 0,1488 [0,0458; 0,2518], p Holm 0,015; extranjera −0,0184 | BA/h1_principal.csv | sí |
| H2: crédito 0,0087 [0,0033; 0,0141] p WCB 0,002; CU×expo −0,0044; crédito t−4 0,0019 (p 0,481) | BV/h2_resultados.csv | sí |
| H3: β alquiler 3,06, F 14,44, p_IUT 0,0294; H4: 0,794, p_IUT 0,0463 | BI/h3_principal.csv, BO/h4_principal.csv | sí |
| H5: +0,0037 [−0,0002; 0,0076], p una cola 0,968, pendiente pre 0,040 | BP/resultado.json | sí |
| H1 sellado: RMSE 0,0108 frente a 0,0122, DM 3,98, p 0,0053; ECM v1 p 0,031; 3 selladas p 0,589 | BA/h1_sellado.json | sí |
| H2 sellado: 0,0546 frente a 0,0619, DM 1,43, p 0,195 | BV/h2_sellado.json | sí |
| H6: τ −0,0117 [−0,0210; −0,0023], p 0,014; SC −0,0121 (p 0,044); DiD +0,0238 | BP/h6_sellado.json | sí |
| H7: A 0,0722 frente a 0,0508; ECM v1 0,0128; B 0,0111 frente a 0,0122 (p 0,499) | BM/h7_sellado.json | sí |
| Holm-7: H6 0,098, H3 0,176, H4 0,232, H2 0,779 | BS/holm7.csv (recalculado) | sí |
| Alquiler desde 2020: 5,66 [4,81; 6,58]; común 5,79 [4,16; 7,76] (102 %) | BD/tabla_resumen.csv | sí |
| Compra desde 2014: crédito/CU M1 2,27 [0,39; 4,81] frente a M2 0,03 | tablas/contribuciones_periodo.csv | sí |
| Validación BA: B_AR4_mas_H1 p 0,645 | tablas/modelos_fuera_muestra.csv | sí |
| BHJ: alquiler b 3,99 (p 0,0005), precio 2,90 (p 0,55) | BI/h3_resultados.json | sí (formato, C7) |
| Déficit: 632.861 / 598.157 | BO/deficit_nacional.csv | sí (matiz, C8) |
| v1: OLS 0,534 (p WCB 0,004), 2SLS 0,437 (0,119), DM p 0,509, 3.812 especificaciones | output/informe.md, output/tablas/inmigracion_iv.csv | sí |

## 3. Honestidad y escala de evidencia

- No hay lenguaje causal. Lo comprobé buscando efecto/causa/redujo/eleva/impulsa: todas las apariciones son negaciones o descripciones del método. Todas las etiquetas coinciden con las finales del orquestador: nada supera EXPLORATORIO. La mejora sellada de H1 se presenta como hecho predictivo y se dice expresamente que no es una asociación robusta de coeficientes. Lo mismo en el ranking: D = sí, nivel EXPLORATORIO.
- Están todos los resultados negativos: H2, H5, H7, LSTM, BHJ, suelo, turismo, panel UE y SHAP. Se reportan las discrepancias H6 SDiD/SC frente a DiD (incluida Tarragona) y BD M1 frente a M2 (19 componentes «no robustos»). El ECM v1 nacional aparece marcado como NO pre-registrado. Se declaran las dos fugas corregidas y la lectura indebida del orquestador, con su consecuencia para el umbral de H7.
- **Fallo (C1):** el informe omite el único componente de compra que **sí** se replica en M1 y M2: la demografía agregada desde 2014, con M1 −6,50 [−15,48; −0,16] y M2 −7,53 [−19,75; −2,62]. En `contribuciones_periodo.csv` figura como «replica en M1 y M2». La tabla «Compra, ventanas acumuladas» solo muestra 20-34 y extranjera por separado. Además, el texto afirma lo contrario: «Demografía, empleo y oferta: sin atribución estable en BD entre M1 y M2» (`bs_informe.py:244`; también en el resumen ejecutivo de BD). Lo mismo ocurre con P1 crédito/CU en compra (M1 −4,18 y M2 −5,49, ambos excluyen 0), que solo aparece en M1.
- **Fallo (C2):** el informe no contrasta H2 con el ECM v1. En la tabla 6.2 figura n/d, aunque `modelos_fuera_muestra.csv`, fila 101, sí tiene el dato: con 49 provincias, ECM v1 0,0531 frente a C3 0,0542, DM −0,12, p 0,91. Tampoco dice que en el sellado de compra provincial el ECM v1 tiene menor RMSE que el AR(4): 0,0528 frente a 0,0619, en la fila BM C de la propia tabla. Esto contradice «mejorarlo es un listón bajo» (línea 354), que solo vale en entrenamiento.

## 4. Requisitos del usuario

Todos están presentes: alquiler frente a compra (§3); ecuaciones con EE, IC y p (§4.1-4.2); contribuciones por periodo y ventanas con IC de M1 y M2 (§4.3); ranking con nivel de evidencia (§5); modelos fuera de muestra frente a AR(4) y ECM v1 con DM-HLN en la misma muestra (§6); Holm-7 (§7); cambios respecto de v1 y su motivo (§8); resultados negativos (§9); limitaciones priorizadas (§10); qué NO se puede afirmar (§11); referencias con estado y cuartil (§12). Las interpolaciones (población T2-T4) se usan en el modelo principal, pero están marcadas, ya se aprobaron en BA y la robustez con T1 observado coincide. SERPAVI (PDF) solo se usa en el módulo exploratorio de turismo.

## 5. Registro

- `registro_v2.csv` tiene 682 filas, de las que 6 son de presupuesto: quedan 676 especificaciones. Cuadra con los registros de rama: BA 50−1, BV 145−2, BI 96−1, BO 250−1, BP 46, BM 64−1, BD 31, BS 0. Los presupuestos se cumplen: BM 63 = 59 + 4 LSTM; BO suelo 160 con Holm sobre 160.
- **Fallo (C3), especificaciones no contadas:** las estimaciones de las evaluaciones selladas no están en ningún registro. Solo H6 suma 12 (SDiD, SC y DiD en ln; SDiD, SC y DiD en Δ4; ponderado por share; 4 por provincia; sin 2023Q3-Q4). A eso se añaden los secundarios de H1, H2 y H7. El total de 676 no lo declara.

## 6. Referencias

- Crossref, comprobadas hoy: Webb (2023) CJE 56(3) 839-858; Jofre-Monseny, Martínez-Mazza y Segú (2023) RSUE 101, 103916; Montiel Olea y Pflueger (2013) JBES 31(3) 358-369; Khametshin et al. (2024) BdE DO. **Todas coinciden.** Cavalleri et al. (2019): el DOI existe, pero sin autores (`author: None`), como dice la tabla.
- Las NO VERIFICADAS (Lundberg y Lee 2017; Ke et al. 2017) lo dicen en la tabla y en la lista final. Los cuartiles no verificados (Roodman 2019; Jofre-Monseny 2023) están marcados.
- **Fallo (C4):** en §2 (línea 83), Cavalleri et al. (2019) aparece como «[verificada]» y Jaeger, Ruist y Stuhler (2018) también. La función `t()` solo distingue NO VERIFICADA y cuartil. Debe reflejar «parcial» (Cavalleri) y «WP» (Jaeger), como hace la tabla de §12.

## 7. Cambios

**Obligatorios (solo generador y texto; reejecutar `bs_run.py` y comprobar md5 dos veces):**

1. **C1.** En las tablas de ventanas acumuladas (alquiler y compra), añadir la fila `demografia` agregada. Sustituir la frase de `bs_informe.py:244` y la de §4.3 «Sin atribución estable entre M1 y M2» por la verdad de la tabla: desde 2014, la demografía agregada de compra es negativa en M1 y en M2 (−6,50 y −7,53; ambos IC excluyen 0; EXPLORATORIO, por composición); desde 2020 no hay atribución estable. Mencionar P1 crédito/CU en compra (se replica).
2. **C2.** En §6.2, la fila H2 debe mostrar el contraste con el ECM v1 disponible (49 provincias: 0,0531; DM −0,12; p 0,91), indicando la muestra. En la «Observación NO pre-registrada», añadir que en el sellado de compra provincial el ECM v1 tiene menor RMSE que el AR(4) (0,0528 frente a 0,0619, solo RMSE, sin contraste). Matizar «listón bajo» a «en entrenamiento».
3. **C3.** En el anexo y en §1, declarar que las 676 excluyen las estimaciones de las 4 evaluaciones selladas, e indicar su número (H6: 12 más los secundarios de H1, H2 y H7), o bien añadirlas a `registro_v2.csv` con `fase=sellado`.
4. **C4.** Hacer que las etiquetas de §2 hereden el estado completo de `referencias_v2.csv` (Cavalleri: «parcial»; Jaeger: «WP; revista no verificada»).

**Recomendables (no bloquean):**

5. **C5.** `bs_informe.py:126`: «solo cumple (BA: …)» → «solo cumple 1 (BA: …)».
6. **C6.** Matizar «Ninguna cifra está escrita a mano»: hay literales con fuente (MDE ≈1,7 % de BP/resumen.md; 0,45 de v1; 0,029, 0,174 y 0,035 de versiones previas). Citarlos o leerlos de fichero.
7. **C7.** En la línea BHJ (§9), usar formato español y escribir p < 0,001 en lugar de «p=0.000».
8. **C8.** Déficit con protegida: 34.704 = observadas en 49 provincias (33.164) más un reescalado. Decir «observadas y reescaladas a 52 provincias» y dar la cota inferior (599.697).

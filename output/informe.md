# Determinantes del precio de la vivienda en España: síntesis (módulo C. Valenciana / València)

Documento generado por `src/report.py` a partir de las tablas de `output/` (ninguna cifra del texto está escrita a mano; cada sección cita el archivo de origen). Lenguaje: *asociación*; ninguna pregunta alcanza el nivel causal. Errores estándar: HAC Newey-West (4 retardos) en series temporales y cluster por CCAA (con wild cluster bootstrap y Driscoll-Kraay como robustez) en panel. Nivel de significación de referencia 5 % (docs/decisiones.md).

## 1. Resumen ejecutivo

- **Alcance de la búsqueda:** 3.812 especificaciones registradas en total (F2: 3.483, F3: 150, F4: 128, F5: 23, F6: 28); la búsqueda de corto plazo de F2 cubre 1.728 modelos con precio nominal y 1.728 con precio real. Ningún resultado de este informe es confirmatorio en el sentido de una única hipótesis prefijada.

- **P1 (asociación).** Ecuación final con precio **real**: largo plazo (DOLS, N=72) con empleo 1,482 (0,330) y corto plazo (ECM, N=73) con término de corrección del error -0,106 (0,035) (p = 0,002), que **cambia de signo antes de 2020** (0,010 (0,027), p = 0,720). Cointegración: real 3/3, nominal 1/3. El modelo preferido gana en el 9,6 % de las réplicas del bootstrap de la selección y no mejora al AR(4) fuera de muestra (DM p = 0,509).

- **P2 (asociación).** El flujo neto de extranjeros no se asocia de forma robusta con el precio de compra: 2SLS shift-share sobre IPV -1,615 (1,078); el menor p ajustado por Holm sobre 150 especificaciones es 0,051. Asociación positiva con el alquiler en OLS que no sobrevive al ajuste ni al 2SLS.

- **P3 (descriptivo / asociación débil).** Déficit acumulado 2021-2025 = 866.100 viviendas (EPA corregida; 810.936 con ECP) frente a ~750.000 del BdE. Elasticidad de la oferta (iniciadas, DOLS k=4) = 1,44 (0,21); en Δ4 no se rechaza 0,45 (p Holm = 0,272).

- **P4 (asociación; València descriptiva).** Panel de 17 CCAA: b2 = 0,0011 (0,0040) (p wild = 0,774); no se detecta heterogeneidad (p wild de poolability = 0,363), lo que no prueba homogeneidad. València: beta frente a España 1,73 (0,11), inestable por tramos.

- **P5 (descriptivo).** Chow (ECM real) rechaza en 2014Q1 (2014Q1: p = 0,004) y no rechaza en 2020Q1, 2022Q3; Bai-Perron en niveles: 2011Q4, 2019Q2, 2023Q2. El modelo **no es estable**.

- **Robustez** (13 coeficientes clave; regla en la sección 8): sobreviven ('sí') 1; parcialmente 7; no 5 (`tablas/robustez.csv`).

*Fuentes: `output/registro_busqueda.csv`; `output/tablas/ecuacion_final_lp.csv`; `output/tablas/ecuacion_final_cp.csv`; `output/tablas/robustez.csv`; `output/tablas/cointegracion.csv`; `output/tablas/deficit.csv`; `output/tablas/inmigracion_iv.csv`; `output/tablas/panel_ccaa.csv`; `output/tablas/valencia.csv`.*

## 2. Datos y muestra

Todos los modelos leen únicamente `data/processed` y las muestras se recortan a la común antes de estimar (docs/decisiones.md). N exacto por modelo:

| fase | ámbito | especificaciones | n_min | n_max |
|---|---|---|---|---|
| F2 | Precio nacional | 3.483 | 47 | 74 |
| F3 | Inmigración | 150 | 17 | 391 |
| F4 | Oferta | 128 | 47 | 1.122 |
| F5 | Panel CCAA | 23 | 272 | 1.088 |
| F6 | València | 28 | 73 | 85 |

| modelo | N | muestra | fuente |
|---|---|---|---|
| LP real (DOLS ±2) | 72 | 2008Q1-2025Q4 | `output/f2/ecuacion_real.csv` |
| CP real (ECM preferido) | 73 | 2008Q2-2026Q2 | `output/f2/ecuacion_real.csv` |
| Cointegración nominal/real | 74 | 2008Q1-2026Q2 | `output/f2/cointegracion.csv` |
| Pre-COVID real (ECM) | 47 | 2008Q2-2019Q4 | `output/f2/real_robustez.csv` |
| 2014+ real (ECM) | 50 | 2014Q1-2026Q2 | `output/f2/real_robustez.csv` |
| Proyecciones locales (IPV) | 65 | 2008Q2-2024Q2 | `output/f3/nacional_lp.csv` |
| Panel F3 IPV / valor tasado / SERPAVI / IPC alq. | 306 / 386 / 198 / 391 | 17 CCAA anuales | `output/f3/panel_primera_etapa.csv` |
| Oferta: DOLS / Δ4 | 63 / 61 | 2009Q4-2025Q4 / Δ4 | `output/f4/dols_resultados.csv; f4/ols_delta4.csv` |
| Panel F5 (FE principal) | 289 | 2009-2025, 17 CCAA | `output/f5/tabla_fe_principal.csv (N del registro)` |
| València: beta Δ4 / compraventas | 82 / 73 | 2005Q1-2026Q2 (Δ4) / 2007Q1-2026Q1 | `output/f6/beta_todos.csv` |

**Interpolaciones y limitaciones de datos** (de `docs/limitaciones.md`, sección Datos): 

- Población nacional antes de 2021: semestral (1 enero / 1 julio) interpolada log-linealmente a T2/T4 → Δ1 trimestral con MA mecánica.
- Población por CCAA: solo anual (1 enero) 2002-2025; en el panel trimestral está interpolada.
- No hay flujos de inmigración trimestrales útiles (INE EMCR desde 2023T2, muy dispersos); flujo anual nacional de Eurostat 1998-2024 con quiebre en 2021; sin flujos anuales por CCAA (tabla INE 69691 no descargada).
- Oferta: permisos (Eurostat) y viviendas libres iniciadas/terminadas (MIVAU) son proxies; no hay visados CSCAE ni certificados de fin de obra.
- Hogares: EPA trimestral 2002+ con quiebre metodológico en 2021T1 (−1,1 %); solo nacional.
- Precio largo: `p_bde` (BdE) = `p_tasado` (MIVAU); una única serie larga desde 1995.
- Deflactor: implícito del PIB (CNTR SA), no un deflactor de consumo.
- València: padrón por nacionalidad solo hasta 2022; varias series municipales con N corto (≤ 14 años).

**Datos no validados.** De las 40 series de `valencia.csv` listadas, 10 tienen validación 'plausibilidad' (no 'sí'); de ellas 0 entran en alguna estimación. Las series con N < 40 (26) se tratan solo de forma descriptiva y las series de PDF no validadas quedan limitadas a robustez, nunca al modelo principal (CLAUDE.md). Ninguna serie procede de OCR (docs/diccionario_variables.md).

*Fuentes: `output/registro_busqueda.csv`; `output/f6/tabla_N_series.csv`; `docs/limitaciones.md`; `docs/diccionario_variables.md`.*

### Métodos y diagnósticos utilizados

Errores estándar HAC: Newey y West (1987). Raíces unitarias: Dickey y Fuller (1979), Kwiatkowski, Phillips, Schmidt y Shin (1992) y Zivot y Andrews (1992); p-valores de MacKinnon (1996). Largo plazo: DOLS de Stock y Watson (1993); cointegración: Engle y Granger (1987), Johansen (1988, 1991) y contrastes de límites de Pesaran, Shin y Smith (2001). Diagnósticos por modelo: Durbin y Watson (1950), Breusch (1978) y Godfrey (1978b) para autocorrelación, Breusch y Pagan (1979), Jarque y Bera (1987), Ramsey (1969) para RESET, Brown, Durbin y Evans (1975) para CUSUM, Chow (1960) y Bai y Perron (1998, 2003) para quiebres, y factor de inflación de la varianza (VIF). Predicción: Diebold y Mariano (1995). Búsqueda de especificaciones: Holm (1979) y Bonferroni, y cotas extremas de Leamer (1983). Panel: Driscoll y Kraay (1998), Cameron, Gelbach y Miller (2008), Webb (2023), Pesaran (2006) y Pesaran (2007). Inmigración: Jordà (2005) para proyecciones locales y Card (2001) y Goldsmith-Pinkham, Sorkin y Swift (2020) para el diseño shift-share.

*Fuentes: `docs/literatura.md`.*

## 3. P1 - Ecuación de largo y corto plazo del precio nacional

**Respuesta.** La ecuación que se interpreta es la de precio **real** (IPV deflactado por el deflactor implícito del PIB), porque es la única cuya relación de nivel cointegra en los tres contrastes. Es una desviación motivada del pre-registro (docs/decisiones.md): la nominal se mantiene como réplica del punto de partida y se reportan ambas. Se lee como asociación estadística, no como relación estructural.

**Nivel de evidencia: ASOCIACIÓN.** Justificación: no hay identificación (regresores endógenos, sin instrumento); la cointegración del vector real es 3/3 pero la del nominal es 1/3; el término de corrección del error cambia de signo antes de 2020; ningún término del corto plazo sobrevive a Bonferroni (K = nº de modelos de la búsqueda que lo contienen).

### 3.1 Ecuación final de largo plazo (DOLS ±2, precio real)

| término | coef | EE_HAC | IC95 | p | p_Bonf_K | p_Holm | N |
|---|---|---|---|---|---|---|---|
| const | -15,1839 | 3,1359 | [-21,330; -9,038] | <0,001 | n/d | n/d | 72 |
| ln_ocupados | 1,4824 | 0,3301 | [0,835; 2,129] | <0,001 | <0,001 | <0,001 | 72 |
| tipo_hip_real | 0,0022 | 0,0081 | [-0,014; 0,018] | 0,782 | 1,000 | 0,817 | 72 |
| ln_permisos_l4 | 0,0321 | 0,0292 | [-0,025; 0,089] | 0,272 | 1,000 | 0,817 | 72 |
| ln_costes_real | -0,6598 | 0,2512 | [-1,152; -0,167] | 0,009 | 0,069 | 0,052 | 72 |

Ecuación: `ln IPV_real = -15,18 + 1,482·ln_ocupados + 0,002·tipo_hip_real + 0,032·ln_permisos_l4 - 0,660·ln_costes_real` (más dummies trimestrales y adelantos/retardos del DOLS; muestra 2008Q1-2025Q4). Corrección: familia de 8 pendientes de largo plazo (4 × {nominal, real}); no cubre la elección de regresores, que en el largo plazo no se buscó.

### 3.2 Ecuación final de corto plazo (ECM preferido por R² ajustado, precio real)

| término | coef | EE_HAC | IC95 | p | K | p_Bonf_K | N |
|---|---|---|---|---|---|---|---|
| Intercept | 0,0032 | 0,0033 | [-0,003; 0,010] | 0,337 | n/d | n/d | 73 |
| ect_l1 | -0,1064 | 0,0348 | [-0,175; -0,038] | 0,002 | 1.728 | 1,000 | 73 |
| q2 | 0,0057 | 0,0051 | [-0,004; 0,016] | 0,259 | n/d | n/d | 73 |
| q3 | 0,0003 | 0,0056 | [-0,011; 0,011] | 0,954 | n/d | n/d | 73 |
| q4 | -0,0201 | 0,0058 | [-0,032; -0,009] | <0,001 | n/d | n/d | 73 |
| d_ln_ocupados_l1 | 0,4665 | 0,1795 | [0,115; 0,818] | 0,009 | 576 | 1,000 | 73 |
| d_tipo_hip_l1 | -0,0120 | 0,0040 | [-0,020; -0,004] | 0,003 | 576 | 1,000 | 73 |
| d_ln_renta_hog_real | 0,1463 | 0,0792 | [-0,009; 0,302] | 0,065 | 864 | 1,000 | 73 |
| d_ln_ipv_real_l4 | 0,2996 | 0,0970 | [0,109; 0,490] | 0,002 | 576 | 1,000 | 73 |
| d_ln_credito_nuevo | 0,0383 | 0,0147 | [0,009; 0,067] | 0,009 | 864 | 1,000 | 73 |

R² ajustado = 0,676 (nominal: 0,749). Muestra 2008Q2-2026Q2. `ect_l1` es el residuo rezagado del DOLS real. El preferido aparece como ganador en el 9,6 % de las réplicas del bootstrap por bloques de la selección completa: la especificación concreta **no está identificada**; 1.728 modelos en la búsqueda real.

### 3.3 Réplica nominal del punto de partida

| término | coef | EE_HAC | p | N |
|---|---|---|---|---|
| const | -16,4689 | 3,8702 | <0,001 | 72 |
| ln_ocupados | 1,9510 | 0,4801 | <0,001 | 72 |
| tipo_hip | -0,0172 | 0,0171 | 0,315 | 72 |
| ln_permisos_l4 | 0,0595 | 0,0454 | 0,190 | 72 |
| ln_costes | 0,2659 | 0,1646 | 0,106 | 72 |

CP nominal: término de corrección -0,0968 (0,0309), R² ajustado 0,749. La réplica del punto de partida (EG estático) reproduce sus pendientes casi exactamente (`tablas/ecuacion_replica_nominal.csv`, bloque 'Réplica punto de partida').

### 3.4 Cointegración (los tres contrastes, nominal y real)

| precio | N | EG_p | Johansen_traza | ARDL_F | rechazos | decisión |
|---|---|---|---|---|---|---|
| nominal | 74 | 0,398 | 117,3 (cv 69,8) | 3,25 (I1 4,01; no concluyente) | 1 | evidencia mixta (1/3) |
| real | 74 | 0,023 | 133,1 (cv 69,8) | 7,20 (I1 4,01; rechaza (F>I1)) | 3 | cointegración (3/3) |

Regla: se exige concordancia de al menos 2 de 3 contrastes. El t del ect NO contrasta cointegración (distribución no estándar; Banerjee-Dolado-Mestre 1998). Con valor tasado y BdE (la misma serie) el vector base da: {cdf2.loc[[x for x in cdf2.index if x.startswith('ln_p_tasado') and x.endswith('/ base')][0], 'decision']} (`tablas/cointegracion.csv`).

### 3.5 Diagnósticos de la ecuación final

| modelo | N | DW | BG4_p | BP_p | JB_p | RESET_p | CUSUM_p | VIF_max | fallan |
|---|---|---|---|---|---|---|---|---|---|
| Preferido real (R2aj) | 73 | 1,99 | 0,480 | 0,148 | 0,531 | 0,184 | 0,896 | 1,2 | ninguno |
| Ganador BIC real | 73 | 1,74 | 0,170 | 0,032 | 0,809 | 0,498 | 0,828 | 1,3 | Breusch-Pagan |
| Ganador AIC real | 73 | 1,99 | 0,480 | 0,148 | 0,531 | 0,184 | 0,896 | 1,2 | ninguno |
| DOLS real (LR) | 72 | 0,61 | <0,001 | 0,584 | 0,347 | <0,001 | 0,217 | 17,4 | BG(4), RESET, VIF |

Chow (ECM real): 2014Q1 p = 0,004; 2020Q1 p = 0,126; 2022Q3 p = 0,616. El DOLS real de largo plazo falla autocorrelación, RESET y colinealidad: su inferencia es sólo indicativa.

### 3.6 Corrección por búsqueda y predicción fuera de muestra

Búsqueda de corto plazo con precio real: 1.728 modelos (nominal: 1.728). Bonferroni con K = modelos que contienen cada término (columna K arriba). Fuera de muestra (ventana expansiva, 34 periodos): RMSE del preferido 0,0244 frente a 0,0165 del AR(4) con dummies; Diebold-Mariano (HAC) vs AR(4): p = 0,509. Con precio nominal: p = 0,290. No se puede afirmar que el modelo prediga mejor que un AR(4).

### 3.7 Significatividad y signos frente a la literatura

| bloque | variable | coef | p | p_corregido | esperado | coincide |
|---|---|---|---|---|---|---|
| P1 LP real (DOLS) | Empleo (LP real) | 1,4824 | <0,001 | <0,001 | + | sí |
| P1 LP real (DOLS) | Tipo hipotecario real (LP real) | 0,0022 | 0,782 | 0,817 | - | no |
| P1 LP real (DOLS) | Permisos t-4 (LP real) | 0,0321 | 0,272 | 0,817 | - | no |
| P1 LP real (DOLS) | Costes reales (LP real) | -0,6598 | 0,009 | 0,052 | + | no |
| P1 LP nominal (réplica) | Empleo (LP nominal, réplica) | 1,9510 | <0,001 | <0,001 | + | sí |
| P1 LP nominal (réplica) | Tipo hipotecario (LP nominal) | -0,0172 | 0,315 | 0,817 | - | sí |
| P1 LP nominal (réplica) | Permisos t-4 (LP nominal) | 0,0595 | 0,190 | 0,761 | - | no |
| P1 LP nominal (réplica) | Costes (LP nominal) | 0,2659 | 0,106 | 0,530 | + | sí |
| P1 CP real (ECM) | Corrección de error ect(t-1) | -0,1064 | 0,002 | 1,000 | - | sí |
| P1 CP real (ECM) | Empleo Δ (t-1) (CP real) | 0,4665 | 0,009 | 1,000 | + | sí |
| P1 CP real (ECM) | Δ tipo hipotecario (t-1) (CP real) | -0,0120 | 0,003 | 1,000 | - | sí |
| P1 CP real (ECM) | Δ renta real del hogar (CP real) | 0,1463 | 0,065 | 1,000 | + | sí |
| P1 CP real (ECM) | Δ precio real (t-4) (CP real) | 0,2996 | 0,002 | 1,000 | n/a | n/a |
| P1 CP real (ECM) | Δ crédito nuevo (CP real; comovimiento) | 0,0383 | 0,009 | 1,000 | + | sí |

Signos esperados y referencias (docs/literatura.md, «Tabla: signos esperados»):

| clase | signo_esperado | referencia |
|---|---|---|
| ocupados | + | Martínez Pagés y Maza (2003); Bover y Jimeno (2007) |
| renta | + | Martínez Pagés y Maza (2003); Himmelberg et al. (2005) |
| tipo | - | Poterba (1984); Himmelberg et al. (2005); Martínez Pagés y Maza (2003) |
| costes_precio | + | Glaeser y Gyourko (2005, 2018) |
| costes_oferta | - | Glaeser y Gyourko (2005, 2018) (costes sobre oferta) |
| permisos | - | Saiz (2010); Hilber y Vermeulen (2016); BdE IA 2025 |
| terminadas | - | Saiz (2010); Hilber y Vermeulen (2016); BdE IA 2025 (oferta sobre precio) |
| credito | + | Mian y Sufi (2009, 2011) |
| ect | - | Engle y Granger (1987); Johansen (1988, 1991); Pesaran, Shin y Smith (2001) |
| inmig | + | Saiz (2007); González y Ortega (2013); Accetturo et al. (2014) (Sá 2015: negativo en UK) |
| elasticidad | + | Saiz (2010); BdE IA 2025 (elasticidad de oferta positiva) |
| persistencia | n/a | sin signo esperado en la tabla de literatura (inercia) |

Análisis de signos: el empleo y la persistencia del precio son las asociaciones más estables; el coste real tiene signo contrario al esperado y el tipo real es ≈ 0 en el largo plazo (relación estadística, no estructural). Tabla completa en `tablas/significatividad.csv`.

*Fuentes: `output/f2/ecuacion_real.csv`; `output/f2/largo_plazo.csv`; `output/f2/ecm_preferido.csv`; `output/f2/cointegracion.csv`; `output/f2/real_diagnosticos.csv`; `output/f2/real_chow.csv`; `output/f2/real_oos_dm.csv`; `output/f2/oos_dm.csv`; `output/f2/comparacion_nominal_real.csv`; `output/f2/real_busqueda_eba.csv`; `output/tablas/ecuacion_final_lp.csv`; `output/tablas/ecuacion_final_cp.csv`; `output/tablas/ecuacion_replica_nominal.csv`; `output/tablas/significatividad.csv`.*

## 4. P2 - Inmigración (stock y flujo): ¿cuánto aporta y es causal?

**Respuesta.** No es causal y no se documenta una aportación robusta al precio de compra. Hay una asociación positiva con el alquiler en OLS por CCAA que no sobrevive a la corrección por búsqueda ni al 2SLS, y con una pretendencia significativa en algunos grupos de países.

**Nivel de evidencia: ASOCIACIÓN.** Justificación: el IV shift-share (Card 2001; cuotas de 2002) supera F ≥ 10 en todos los resultados, pero ningún efecto sobrevive al wild cluster bootstrap ni a Holm (mínimo p Holm = 0,051 sobre 150 especificaciones); el alquiler tiene pretendencia significativa; con 17 clusters el J de Hansen tiene poca potencia y AKM/BHJ no son viables con tan pocos grupos de países. La condición de identificación (F > 10 + exclusión argumentada) no se cumple.

### 4.1 Panel de CCAA, IV shift-share (efectos fijos de CCAA y año)

| resultado | estimador | N | coef | EE_cluster | IC95_normal | p_WCB | F_1a_etapa |
|---|---|---|---|---|---|---|---|
| IPV (precio) | OLS | 306 | -0,454 | 0,503 | [-1,44; 0,53] | 0,385 | n/d |
| IPV (precio) | 2SLS | 306 | -1,615 | 1,078 | [-3,73; 0,50] | 0,210 | 17,9 |
| valor tasado | OLS | 386 | 0,361 | 0,716 | [-1,04; 1,76] | 0,622 | n/d |
| valor tasado | 2SLS | 386 | -0,875 | 0,952 | [-2,74; 0,99] | 0,489 | 53,2 |
| alquiler SERPAVI | OLS | 198 | 1,217 | 0,337 | [0,56; 1,88] | 0,007 | n/d |
| alquiler SERPAVI | 2SLS | 198 | 0,554 | 0,813 | [-1,04; 2,15] | 0,498 | 10,6 |
| IPC alquiler | OLS | 391 | 0,534 | 0,167 | [0,21; 0,86] | 0,004 | n/d |
| IPC alquiler | 2SLS | 391 | 0,437 | 0,293 | [-0,14; 1,01] | 0,119 | 54,4 |

IC95 % del 2SLS sobre IPV: [-3,90; 0,67] (según `f3/ic95_2sls_principal.csv`). Coeficiente = variación % del precio por cada punto porcentual de flujo neto de extranjeros sobre la población total.

### 4.2 Nivel de evidencia por resultado (F3)

| resultado | F≥10 | pretendencias no signif. | J no rechaza | sobrevive WCB | p_pretend_min | nivel |
|---|---|---|---|---|---|---|
| IPV (precio) | True | True | True | False | 0,519 | asociacion |
| valor tasado | True | True | True | False | 0,519 | asociacion |
| alquiler SERPAVI | True | False | True | False | 0,006 | asociacion |
| IPC alquiler | True | False | True | False | 0,006 | asociacion |

### 4.3 Series temporales nacionales (proyecciones locales, HAC)

| resultado | h | N | muestra | coef | EE_HAC | p |
|---|---|---|---|---|---|---|
| ln_ipv | 0 | 65 | 2008Q2-2024Q2 | -0,0412 | 0,0482 | 0,393 |
| ln_ipv | 4 | 65 | 2008Q2-2024Q2 | -0,1214 | 0,3204 | 0,705 |
| ln_ipv | 8 | 65 | 2008Q2-2024Q2 | -0,0673 | 0,6242 | 0,914 |
| ln_ipc_alquiler | 0 | 81 | 2004Q2-2024Q2 | 0,0061 | 0,0042 | 0,146 |
| ln_ipc_alquiler | 4 | 81 | 2004Q2-2024Q2 | 0,0526 | 0,0257 | 0,041 |
| ln_ipc_alquiler | 8 | 81 | 2004Q2-2024Q2 | 0,1883 | 0,0552 | <0,001 |

En frecuencia anual (N = 17), el flujo contemporáneo da 10,647 (2,972) (p < 0,001) y el stock 0,431 (0,237) (p = 0,068); tras Holm el p del flujo es 0,051. Con N tan pequeño no hay inferencia HAC fiable.

**Corrección por búsqueda para la variable de interés (inmigración).** Menor p sin corregir < 0,001; Holm sobre 150 (F3) = 0,051; Holm sobre las variantes de b2 de F5 = 0,151; Bonferroni con el total de especificaciones del proyecto (K = 3.812) = 1,000. No se calculó Romano-Wolf.

### 4.4 Comparación con la literatura

La literatura (Saiz 2007; González y Ortega 2013; Accetturo et al. 2014) apunta a efectos positivos sobre precios/alquileres; Sá (2015) obtiene un signo negativo en el Reino Unido. El IC95 % del 2SLS sobre IPV ([-3,90; 0,67]) excluye las magnitudes de Saiz y González-Ortega; la diferencia se atribuye a diseño y periodo (2008+, peso de la cuota europea de 2002), no a un error. Las unidades no son directamente comparables (docs/literatura.md).

### 4.5 Canal comprador

El coeficiente 2SLS del canal comprador (compras de extranjeros residentes) es muy negativo incluso sin 2008-09 y se interpreta como posible violación de la exclusión; no se interpreta (docs/limitaciones.md).

*Fuentes: `output/f3/panel_principal.csv`; `output/f3/panel_primera_etapa.csv`; `output/f3/nivel_evidencia.csv`; `output/f3/correccion_busqueda.csv`; `output/f3/nacional_lp.csv`; `output/f3/nacional_anual.csv`; `output/f3/ic95_2sls_principal.csv`; `output/f5/correccion_busqueda_beta2.csv`; `output/tablas/inmigracion_iv.csv`.*

## 5. P3 - Elasticidad precio de la oferta y déficit acumulado (contraste con el BdE)

**Respuesta.** (i) El déficit 2021-2025 es una cuenta contable (flujo acumulado de Δ hogares − viviendas terminadas) y sale por encima de la cifra del BdE; la diferencia se descompone en la fuente de hogares y en la vivienda protegida ausente de las terminadas MIVAU (libres). (ii) La elasticidad de la oferta es una asociación descriptiva débil, no una elasticidad estructural identificada.

**Nivel de evidencia: DESCRIPTIVO (déficit: aritmética contable con fuentes oficiales) y ASOCIACIÓN DÉBIL/DESCRIPTIVA (elasticidad).** Justificación de la elasticidad: la cointegración de la especificación principal es 1/3, el ECM no es significativo (p = 0,205), BG y RESET fallan, hay quiebre en 2014 y el IV solo es defendible con la renta como instrumento (ocupados y población extranjera afectan a la oferta).

### 5.1 Déficit (flujo acumulado desde 2021)

| variante | periodo | Δhogares | terminadas | déficit | pct_hogares_2025T4 |
|---|---|---|---|---|---|
| (a) EPA corregida (PRINCIPAL) | 2021T1-2025T4 | 1.278.000 | 411.900 | 866.100 | 4,4 |
| (a') EPA con Δ2021T1 = 0 | 2021T1-2025T4 | 1.243.400 | 411.900 | 831.500 | 4,2 |
| (a'') EPA sin corregir (solo referencia) | 2021T1-2025T4 | 1.035.600 | 411.900 | 623.700 | 3,1 |
| (b) ECP 60131 (stock a 1 de enero) | 2021T1-2025T4 (H 1-ene-2026 − H 1-ene-2021) | 1.222.836 | 411.900 | 810.936 | 4,1 |
| (c) Δparque MIVAU anual − Δhogares EPA corregida | 2021-2025 | 1.278.000 | 475.848 | 802.152 | 4,0 |

Extensión de la variante principal a 2026T2: 970.564. BdE (IA 2025): ≈ 750.000; IEF otoño 2025: ≈ 700.000. Diferencia con el BdE: 116.100, de la cual 55.164 por la fuente de hogares (EPA corregida frente a ECP a 1 de enero) y 60.936 por la vivienda protegida no incluida (inferencia nuestra; el BdE no nombra la operación estadística). La corrección del salto de 2021T1 pesa 242.400 viviendas: sin ella el déficit sería 623.700. Es un flujo acumulado, no un déficit en niveles (requeriría un equilibrio inicial). La cifra de ~100.980 terminadas en 2024 citada en prensa es NO VERIFICADA.

### 5.2 Elasticidad de la oferta (iniciadas libres, DOLS ±2, precio real retardado)

| variable | k | estimador | muestra | N | beta | EE | IC95 | p_H0_045 |
|---|---|---|---|---|---|---|---|---|
| iniciadas (código 'visados') | 4 | DOLS ±2 | 2009Q4-2025Q4 | 63 | 1,44 | 0,21 | [1,04; 1,85] | <0,001 |
| terminadas | 8 | DOLS ±2 | 2009Q4-2025Q4 | 63 | 4,26 | 0,26 | [3,75; 4,77] | <0,001 |
| permisos | 4 | DOLS ±2 | 2009Q4-2025Q4 | 63 | 3,11 | 0,41 | [2,31; 3,90] | <0,001 |
| iniciadas (código 'visados') | 4 | OLS estático | 2009Q4-2025Q4 | 63 | 1,34 | 0,27 | [0,82; 1,87] | <0,001 |
| terminadas | 8 | OLS estático | 2009Q4-2025Q4 | 63 | 3,69 | 0,34 | [3,03; 4,35] | <0,001 |
| permisos | 4 | OLS estático | 2009Q4-2025Q4 | 63 | 2,58 | 0,42 | [1,76; 3,41] | <0,001 |
| iniciadas (código 'visados') | 4 | IV 2SLS niveles | 2009Q4-2025Q4 | 63 | 2,22 | 0,66 | [0,93; 3,52] | 0,007 |
| terminadas | 8 | IV 2SLS niveles | 2009Q4-2025Q4 | 63 | 4,13 | 0,37 | [3,42; 4,85] | <0,001 |
| permisos | 4 | IV 2SLS niveles | 2009Q4-2025Q4 | 63 | 4,07 | 1,05 | [2,02; 6,12] | <0,001 |
| iniciadas (código 'visados') | 4 | IV 2SLS Δ4 | 2010Q1-2025Q4 | 61 | 1,06 | 0,89 | [-0,67; 2,80] | 0,489 |
| terminadas | 8 | IV 2SLS Δ4 | 2010Q1-2025Q4 | 61 | 3,17 | 1,15 | [0,91; 5,42] | 0,018 |
| permisos | 4 | IV 2SLS Δ4 | 2010Q1-2025Q4 | 61 | 3,61 | 1,12 | [1,42; 5,79] | 0,005 |
| iniciadas (código 'visados') | 4 | DOLS ±1 2014T1+ | 2014Q1- | 47 | 2,36 | 0,50 | [1,39; 3,34] | <0,001 |
| iniciadas (código 'visados') | 4 | IV niveles 2014T1+ | 2014Q1- | 47 | 3,47 | 0,54 | [2,41; 4,52] | <0,001 |
| terminadas | 8 | DOLS ±1 2014T1+ | 2014Q1- | 47 | 2,86 | 0,28 | [2,32; 3,41] | <0,001 |
| terminadas | 8 | IV niveles 2014T1+ | 2014Q1- | 47 | 3,25 | 0,28 | [2,69; 3,81] | <0,001 |
| permisos | 4 | DOLS ±1 2014T1+ | 2014Q1- | 47 | 3,18 | 0,91 | [1,40; 4,96] | 0,003 |
| permisos | 4 | IV niveles 2014T1+ | 2014Q1- | 47 | 5,78 | 1,01 | [3,80; 7,76] | <0,001 |

Los DOLS en niveles son descriptivos (cointegración 1/3 en la especificación principal). En Δ4 (válido con cualquier orden de integración) las iniciadas dan 1,39 (0,63) y **no se rechaza β = 0,45**: p Holm = 0,272 (IV Δ4: p = 0,489). Rango nacional de las 102 estimaciones de la familia: 1,04 a 6,66. Sin ajuste de frecuencia/concepto la comparación con el BdE no es de igual a igual (ver 5.3).

### 5.3 Comparación con el Banco de España

- **Déficit:** BdE ≈ 750.000 (IA 2025, p. 157); este trabajo 866.100 (EPA corregida), 810.936 (ECP a 1 de enero) y 802.152 (Δparque MIVAU).

- **Elasticidad 0,45:** cifra del IA 2025 (p. 156), que cita a Caldera y Johansson (2013) y Cavalleri, Cournède y Özsöğüt (2019): **ambas referencias NO VERIFICADAS** de forma independiente. Que el 0,45 sea la elasticidad de la inversión residencial es una **inferencia nuestra** (el BdE habla de una «elasticidad de la oferta a largo plazo» con modelos entre países, como cota superior). Nuestra elasticidad de flujo en niveles (1,44) es varias veces mayor, pero no es comparable en concepto; en Δ4 no se rechaza 0,45. La traducción de flujo a stock no se ha hecho: una elasticidad de flujo alta es compatible con una oferta de stock muy inelástica (aritmética en `f4/resumen_f4.md`).

- **Signo de costes:** en iniciadas y terminadas el coste real tiene el signo esperado (negativo); en permisos es positivo (4,73), contrario al esperado.

### 5.4 Quiebres y estabilidad de la oferta

Chow rechaza la estabilidad en 2014Q1 en las tres ecuaciones de oferta (p entre <0,001 y 0,003); Bai-Perron: visados (2013Q1;2016Q4;2021Q2); terminadas (2013Q1;2018Q2); permisos (2014Q1;2019Q2;2022Q3).

*Fuentes: `output/f4/deficit_variantes.csv`; `output/f4/comparacion_bde_deficit.csv`; `output/f4/descomposicion_diferencia_bde.csv`; `output/f4/contraste_bde.csv`; `output/f4/contraste_H0_045_principales.csv`; `output/f4/ols_delta4.csv`; `output/f4/cointegracion.csv`; `output/f4/ecm_resultados.csv`; `output/f4/chow.csv`; `output/f4/bai_perron.csv`; `output/tablas/deficit.csv`; `output/f4/resumen_f4.md`.*

## 6. P4 - Heterogeneidad entre CCAA y Comunitat Valenciana / València

**Respuesta.** No se detecta heterogeneidad entre CCAA con el panel disponible (lo que no prueba homogeneidad: el límite de aleatorización con 17 clusters es 1/17). La Comunitat Valenciana solo difiere en lo descriptivo y el signo depende de la medida de precio (IPV frente a valor tasado). Para València (municipio) hay una comparativa con HAC sobre el valor tasado (N ≥ 40) y el resto es descriptivo.

**Nivel de evidencia: ASOCIACIÓN (panel CCAA) y DESCRIPTIVO (València).** Justificación: ningún efecto de la cuota de extranjeros sobrevive a Holm en el panel; las series de València con N < 40 no admiten inferencia; la beta de València frente a España es un promedio inestable con diagnósticos que fallan y componente parte-todo. No hay identificación.

### 6.1 Panel de CCAA (F5): FE CCAA + año, Δln IPV

| variable | coef | EE_cluster | p_cluster | p_DK | p_wild_Webb |
|---|---|---|---|---|---|
| b1 dln ocupados | -0,0280 | 0,1037 | 0,787 | 0,800 | 0,812 |
| b2 d(extr/total, pp) | 0,0011 | 0,0040 | 0,777 | 0,913 | 0,774 |
| b3 dln pob espanola | 2,1701 | 1,0208 | 0,034 | 0,019 | 0,078 |
| b4 terminadas/1000 hab (t-1) | 0,0026 | 0,0011 | 0,021 | 0,001 | 0,075 |

N = 289, 17 CCAA, 2009-2025. EE cluster por CCAA (17 clusters), Driscoll-Kraay y wild cluster bootstrap. Alineación temporal de b2: flujo del anio t-1 (principal): 0,09 %/pp (p wild 0,857); cuota a mitad de anio t: 1,18 %/pp (p wild 0,068); flujo del anio t (contemporaneo): 1,89 %/pp (p wild 0,010). Holm sobre las 15 variantes de b2: mínimo 0,151 (nada es significativo tras la corrección). Poolability: F = 3,38, p clásico <0,001, p wild 0,363. Terminadas retardadas: signo positivo, contrario al esperado (p wild 0,075). El test CD de Pesaran no es interpretable sobre residuos de FE bidireccional/CCE (Juodis y Reese 2022).

### 6.2 Comunitat Valenciana frente a España (descriptivo)

| periodo | serie | CV_acum_pct | España_acum_pct | dif_pp |
|---|---|---|---|---|
| 2014Q1-2026Q2 | ipv | 95,9 | 109,9 | -14,1 |
| 2014Q1-2026Q2 | p_tasado | 73,6 | 61,4 | 12,2 |
| 2021Q1-2026Q2 | ipv | 59,2 | 56,4 | 2,8 |
| 2021Q1-2026Q2 | p_tasado | 58,5 | 44,9 | 13,6 |

### 6.3 València (valor tasado, N ≥ 40): beta de Δ4 frente a comparadores

| modelo | maxlags | N | beta | EE_HAC | IC95 | p_beta1 |
|---|---|---|---|---|---|---|
| beta_València_vs_Provincia | 4 | 82 | 1,395 | 0,094 | [1,21; 1,58] | <0,001 |
| beta_València_vs_Provincia | 6 | 82 | 1,395 | 0,092 | [1,21; 1,58] | <0,001 |
| beta_València_vs_C. Valenciana | 4 | 82 | 1,515 | 0,102 | [1,32; 1,71] | <0,001 |
| beta_València_vs_C. Valenciana | 6 | 82 | 1,515 | 0,100 | [1,32; 1,71] | <0,001 |
| beta_València_vs_España | 4 | 82 | 1,729 | 0,105 | [1,52; 1,94] | <0,001 |
| beta_València_vs_España | 6 | 82 | 1,729 | 0,103 | [1,53; 1,93] | <0,001 |
| beta_compraventas_València_vs_C. Valenciana | 4 | 73 | 1,061 | 0,052 | [0,96; 1,16] | 0,238 |
| beta_compraventas_València_vs_España | 4 | 73 | 1,140 | 0,056 | [1,03; 1,25] | 0,012 |
| beta_compraventas_València_vs_CV sin València (parte-todo) | 4 | 73 | 1,036 | 0,054 | [0,93; 1,14] | 0,506 |

Por tramos (interacciones, HAC8; EE aproximados por tener 24-26 trimestres efectivos por tramo):

| modelo | tramo | N | beta | EE_HAC | p_beta1 |
|---|---|---|---|---|---|
| València_vs_Provincia | 2006Q1-2013Q4 | 32 | 1,33 | 0,09 | <0,001 |
| València_vs_Provincia | 2014Q1-2019Q4 | 24 | 2,62 | 0,29 | <0,001 |
| València_vs_Provincia | 2020Q1-2026Q2 | 26 | 1,02 | 0,13 | 0,904 |
| València_vs_C. Valenciana | 2006Q1-2013Q4 | 32 | 1,58 | 0,12 | <0,001 |
| València_vs_C. Valenciana | 2014Q1-2019Q4 | 24 | 3,38 | 0,70 | <0,001 |
| València_vs_C. Valenciana | 2020Q1-2026Q2 | 26 | 1,02 | 0,11 | 0,857 |
| València_vs_España | 2006Q1-2013Q4 | 32 | 1,67 | 0,11 | <0,001 |
| València_vs_España | 2014Q1-2019Q4 | 24 | 2,80 | 0,63 | 0,004 |
| València_vs_España | 2020Q1-2026Q2 | 26 | 1,20 | 0,13 | 0,128 |

Diferencial medio de crecimiento por tramo (pp/año): València_vs_España 2006Q1-2013Q4: -1,7 (EE 2,0); València_vs_España 2014Q1-2019Q4: 0,3 (EE 2,5); València_vs_España 2020Q1-2026Q2: 5,6 (EE 1,0). Crecimiento acumulado del valor tasado 2020-2026Q2: València 100,0 %, CV 57,1 %, España 42,5 %; con el IPV del INE la CV (61,8 %) y España (59,5 %) casi no difieren: el exceso es sobre todo del valor tasado (composición de lo tasado). Cuota de compradores extranjeros CV superior a España en 77 de 77 trimestres (hecho descriptivo; no se cita el p-valor numérico).

Diagnósticos de los 3 modelos beta (Δ4): p máximos entre modelos de BG(4) < 0,001, RESET = 0,022, CUSUM = 0,043 (todos por debajo de 0,05); la beta es un promedio inestable y no debe leerse como parámetro estructural.

*Fuentes: `output/f5/tabla_fe_principal.csv`; `output/f5/timing_b2.csv`; `output/f5/poolability.csv`; `output/f5/correccion_busqueda_beta2.csv`; `output/f5/valencia_vs_espana.csv`; `output/f6/beta_todos.csv`; `output/f6/beta_por_tramos.csv`; `output/f6/diferencial_nivel_por_tramos.csv`; `output/f6/crecimiento_acumulado_p_tasado.csv`; `output/f6/ipv_vs_tasado_acumulado.csv`; `output/f6/cuota_extranjeros_inferencia.csv`; `output/f6/diagnosticos_beta.csv`; `output/tablas/panel_ccaa.csv`; `output/tablas/valencia.csv`.*

## 7. P5 - Quiebres (2008, 2014, 2020, 2022) y estabilidad del modelo

**Respuesta.** Chow rechaza la estabilidad en el ECM real en 2014Q1 y no la rechaza en 2020Q1, 2022Q3; Bai-Perron fecha 3 quiebres en el largo plazo en niveles (2011Q4, 2019Q2, 2023Q2). La corrección de error es inestable: el modelo no es estable.

**Nivel de evidencia: DESCRIPTIVO (diagnóstico de estabilidad; contrastes con fechas candidatas y fechas estimadas, sin identificación).** Los contrastes de Chow con fechas candidatas elegidas ex ante se complementan con Bai-Perron (fechas estimadas), cuya inferencia no es estándar.

### 7.1 Chow y Bai-Perron

| fecha | F | p_ECM_real | p_ECM_nominal | n1 | n2 |
|---|---|---|---|---|---|
| 2014Q1 | 3,09 | 0,004 | 0,012 | 23 | 50 |
| 2020Q1 | 1,62 | 0,126 | 0,124 | 47 | 26 |
| 2022Q3 | 0,81 | 0,616 | 0,377 | 57 | 16 |

Bai-Perron (ruptures): ECM real preferido: 0 quiebres; largo plazo real en niveles: 2011Q4, 2019Q2, 2023Q2. Oferta (F4): visados (2013Q1;2016Q4;2021Q2); terminadas (2013Q1;2018Q2); permisos (2014Q1;2019Q2;2022Q3).

### 7.2 Estabilidad del término de corrección del error

| muestra | N | ect | p | R2_aj | BG4_p | RESET_p |
|---|---|---|---|---|---|---|
| Muestra completa | 73 | -0,1064 (0,0348) | 0,002 | 0,676 | 0,480 | 0,184 |
| Con dummies EPA2021 y tipos 2022 | 73 | -0,1022 (0,0393) | 0,009 | 0,671 | 0,541 | 0,290 |
| Con escalones Bai-Perron | 73 | -0,1163 (0,0528) | 0,028 | 0,676 | 0,602 | 0,077 |
| Desde 2014Q1 | 50 | -0,1117 (0,0291) | <0,001 | 0,652 | 0,745 | 0,133 |
| Pre-COVID (≤2019Q4) | 47 | 0,0098 (0,0274) | 0,720 | 0,627 | 0,329 | 0,037 |

El ect recursivo pasa de -0,086 (hasta 2019Q4) a -0,097 (hasta 2026Q2). Por subperiodos, el DOLS cambia de signo en costes y permisos antes de 2020 (`f2/dols_subperiodos.csv`). Los escalones de 2021 (EPA) y de 2022 (tipos) no son significativos en el ECM real.

*Fuentes: `output/f2/real_chow.csv`; `output/f2/chow.csv`; `output/f2/real_bai_perron.csv`; `output/f2/real_robustez.csv`; `output/f2/ect_recursivo.csv`; `output/f2/dols_subperiodos.csv`; `output/f4/chow.csv`; `output/f4/bai_perron.csv`; `output/f6/quiebres_wald_hac.csv`.*

## 8. Robustez de los coeficientes clave

Regla (explícita, mecánica): sea B la estimación de la columna 'muestra completa' y A el conjunto de columnas alternativas con estimación disponible (pre-COVID, desde 2014, con dummies EPA2021/tipos2022, el precio nominal o real distinto del base, valor tasado y otras especificaciones; 'n/d' = no estimado, no cuenta). Una alternativa FALLA si cambia el signo de (coef - referencia) respecto de B o si su p >= 0.05 (cuando hay p). Resultado: 'no' si B no es significativa (p >= 0.05), o si fallan más de la mitad de A, o si el signo cambia en 2 o más alternativas; 'parcial' si hay al menos un fallo (pero no se cumple 'no'), si hay menos de 2 alternativas disponibles, o si la razón entre la mayor y la menor magnitud |coef - referencia| entre columnas con el mismo signo supera 3; 'sí' en otro caso. Para la beta de València la referencia es 1 (H0: beta = 1); para el resto es 0. p aproximado con la normal (coef/EE) si la tabla de origen no trae p (marcado '~').

| coeficiente | muestra_completa | pre_COVID | desde_2014 | dummies_EPA21_tipos22 | nominal | real | precio_valor_tasado | otra_especificacion_1 | otra_especificacion_2 | ¿sobrevive? |
|---|---|---|---|---|---|---|---|---|---|---|
| Empleo LP (ln ocupados) | 1,482 (0,330) [p<0,001] {real} | 3,527 [sin p] {real; sin EE en la tabla} | 0,826 (0,161) [p~<0,001] {nominal DOLS k=1} | 2,235 (0,481) [p<0,001] {nominal} | 1,951 (0,480) [p<0,001] {nominal} | 1,482 (0,330) [p<0,001] {real} | n/d | n/d | n/d | parcial |
| Tipo hipotecario LP (real) | 0,002 (0,008) [p=0,782] {real} | 0,053 [sin p] {real; sin EE en la tabla} | -0,072 (0,009) [p~<0,001] {nominal DOLS k=1} | -0,006 (0,019) [p=0,743] {nominal} | -0,017 (0,017) [p=0,315] {nominal} | 0,002 (0,008) [p=0,782] {real} | n/d | n/d | n/d | no |
| Permisos t-4 LP (proxy de oferta) | 0,032 (0,029) [p=0,272] {real} | -0,115 [sin p] {real; sin EE en la tabla} | 0,106 (0,014) [p~<0,001] {nominal DOLS k=1} | 0,011 (0,048) [p=0,814] {nominal} | 0,059 (0,045) [p=0,190] {nominal} | 0,032 (0,029) [p=0,272] {real} | n/d | n/d | n/d | no |
| Costes LP (reales / nominales) | -0,660 (0,251) [p=0,009] {real} | -0,104 [sin p] {real; sin EE en la tabla} | 0,918 (0,089) [p~<0,001] {nominal DOLS k=1} | 0,320 (0,199) [p=0,108] {nominal} | 0,266 (0,165) [p=0,106] {nominal} | -0,660 (0,251) [p=0,009] {real} | n/d | n/d | n/d | no |
| Corrección de error ect(t-1) | -0,106 (0,035) [p=0,002] {real} | 0,010 (0,027) [p=0,720] {real} | -0,112 (0,029) [p<0,001] {real} | -0,102 (0,039) [p=0,009] {real} | -0,097 (0,031) [p=0,002] {nominal} | -0,106 (0,035) [p=0,002] {real} | n/d | n/d | n/d | parcial |
| Empleo CP (Δ ln ocupados) | 0,467 (0,180) [p=0,009] {real (t-1)} | 0,744 (0,379) [p~=0,049] {nominal (t)} | 0,359 (0,129) [p~=0,005] {nominal (t)} | n/d | 0,474 (0,174) [p=0,006] {nominal (t)} | 0,467 (0,180) [p=0,009] {real (t-1)} | n/d | n/d | n/d | sí |
| Flujo neto extranjeros → IPV (panel F3, OLS FE) | -0,454 (0,503) [p=0,385] | -0,484 (0,530) [p=0,365] {sin 2020-21} | n/d | n/d | n/d | n/d | 0,361 (0,716) [p=0,622] {valor tasado} | -1,615 (1,078) [p=0,210] {2SLS} | n/d | no |
| Flujo neto extranjeros → alquiler IPC (panel F3, OLS FE) | 0,534 (0,167) [p=0,004] | 0,533 (0,172) [p=0,006] {sin 2020-21} | n/d | n/d | n/d | n/d | n/d | 0,437 (0,293) [p=0,119] {2SLS} | n/d | parcial |
| Flujo neto extranjeros → alquiler SERPAVI (panel F3, OLS FE) | 1,217 (0,337) [p=0,007] | 1,358 (0,351) [p=0,005] {sin 2020-21} | n/d | n/d | n/d | n/d | n/d | 0,554 (0,813) [p=0,498] {2SLS} | n/d | parcial |
| Cuota extranjera (pp) → Δln IPV (panel F5, FE CCAA+año) | 0,001 (0,004) [p=0,774] {WCB} | n/d | n/d | n/d | n/d | n/d | 0,016 (0,006) [p=0,010] {valor tasado; p cluster} | 0,022 (0,011) [p=0,040] {CCE-P} | -0,007 (0,007) [p=0,288] {FE+tendencias} | no |
| Stock de extranjeros LP (ln pob. extranjera, DOLS) | 0,768 (0,146) [p<0,001] {nominal} | n/d | n/d | n/d | n/d | n/d | n/d | n/d | n/d | parcial |
| Elasticidad de la oferta (iniciadas libres, DOLS k=4) | 1,444 (0,206) [p<0,001] {DOLS} | n/d | 2,362 (0,497) [p<0,001] {DOLS ±1, 2014T1+} | n/d | n/d | n/d | 2,226 (0,306) [p<0,001] {valor tasado real} | 1,393 (0,633) [p=0,028] {OLS Δ4} | 1,063 (0,886) [p=0,231] {IV Δ4} | parcial |
| Beta de València frente a España (Δ4 valor tasado, H0: beta = 1) | 1,729 (0,105) [p<0,001] {HAC4} | 1,671 (0,114) [p<0,001] {tramo 2006Q1-2013Q4} | n/d | n/d | n/d | n/d | 1,729 (0,105) [p<0,001] {es la base} | 2,800 (0,628) [p=0,004] {tramo 2014Q1-2019Q4} | 1,204 (0,134) [p=0,128] {tramo 2020Q1-2026Q2} | parcial |

Leyenda: cada celda es coef (EE) [p]; '{..}' indica la especificación de origen; '~' = p aproximado por la normal; 'n/d' = no estimado. Motivo de la clasificación y advertencias en `tablas/robustez.csv`.

- **Empleo LP (ln ocupados):** parcial (signo y significatividad estables pero magnitud inestable (razón 4,3)). valor tasado no estimado en el DOLS de F2; pre-COVID real sin EE; el LP real no es estable por subperiodos
- **Tipo hipotecario LP (real):** no (la estimación base no es significativa (p = 0,782)). tipo real ≈ 0 en la ecuación final
- **Permisos t-4 LP (proxy de oferta):** no (la estimación base no es significativa (p = 0,272)). 
- **Costes LP (reales / nominales):** no (fallan 3 de 4 alternativas (3 con cambio de signo)). el signo negativo del coste real contradice el signo esperado: relación estadística, no estructural
- **Corrección de error ect(t-1):** parcial (fallan 1 de 4 alternativas (1 con cambio de signo)). valor tasado no estimado en el ECM; el p del ect NO contrasta cointegración (distribución no estándar)
- **Empleo CP (Δ ln ocupados):** sí (0 fallos en 3 alternativas). el término es Δ ocupados en t (nominal) y en t-1 (real): la búsqueda elige uno u otro; no sobrevive a Bonferroni (K=576)
- **Flujo neto extranjeros → IPV (panel F3, OLS FE):** no (la estimación base no es significativa (p = 0,385)). columna 'pre_COVID' = muestra sin 2020-2021 (no hay muestra pre-COVID en el panel anual); p = wild cluster bootstrap
- **Flujo neto extranjeros → alquiler IPC (panel F3, OLS FE):** parcial (fallan 1 de 2 alternativas (0 con cambio de signo)). pretendencia significativa (grupo América); resultado posterior al diseño prefijado; p = WCB
- **Flujo neto extranjeros → alquiler SERPAVI (panel F3, OLS FE):** parcial (fallan 1 de 2 alternativas (0 con cambio de signo)). p = WCB
- **Cuota extranjera (pp) → Δln IPV (panel F5, FE CCAA+año):** no (la estimación base no es significativa (p = 0,774)). el efecto depende de la alineación temporal (f5/timing_b2.csv) y ninguna variante sobrevive a Holm
- **Stock de extranjeros LP (ln pob. extranjera, DOLS):** parcial (menos de 2 alternativas disponibles (0)). solo un DOLS con pob_extranj; sin contraste en otras muestras ni con precio real
- **Elasticidad de la oferta (iniciadas libres, DOLS k=4):** parcial (fallan 1 de 4 alternativas (0 con cambio de signo)). los p de niveles no son válidos (cointegración 1/3); el IV en Δ4 no es significativo; no se rechaza beta = 0,45 en Δ4 (f4/contraste_H0_045_principales.csv)
- **Beta de València frente a España (Δ4 valor tasado, H0: beta = 1):** parcial (fallan 1 de 3 alternativas (0 con cambio de signo)). el p es de H0: beta = 1; EE por tramo aproximados (24-26 trimestres); València forma parte de CV y España (componente parte-todo); el IPV no existe para el municipio

*Fuentes: `output/tablas/robustez.csv`.*

## 9. Limitaciones (priorizadas)

Prioridad según su efecto sobre la inferencia de P1-P5 (1 = invalida lecturas causales o la estabilidad; 2 = condiciona magnitudes; 3 = datos). Texto de `docs/limitaciones.md`.

**Prioridad 1 (estabilidad y selección de P1/P5) · F2 (aprobada en re-revisión; pendientes trasladados)**

- Cointegración con precio nominal: evidencia mixta (1/3: EG no rechaza, Johansen rechaza, ARDL no concluyente). Solo el precio real cointegra en los tres contrastes; la relación es estadística, no estructural (costes y tipo con signos no esperados en el DOLS real de control del revisor; inestable por subperiodos).
- Desde 2014Q1 el término de corrección del error deja de ser significativo (−0,068, EE 0,045; N=50) y el crédito desaparece: la dinámica de ajuste no es estable.
- El crédito nuevo contemporáneo es simultáneo con el precio (en t−1 cambia de signo); la variante con crédito en t−1 rechaza Breusch-Godfrey.
- Selección: el modelo preferido gana en solo el 1,5 % de las réplicas bootstrap; tras Bonferroni (K=1.728) ningún regresor es significativo al 5 %; fuera de muestra no mejora al AR(4) (selección hecha con la muestra completa).
- RESET rechaza en la ecuación preferida; quiebre en 2014Q1 (Chow p=0,012); Bai-Perron detecta 3 quiebres en el largo plazo.

**Prioridad 1 (estabilidad y selección de P1/P5; precio real) · F2 — bloque de precio real (condición de la re-revisión, cumplida)**

- Ecuación real: el término de corrección del error es significativo en toda la muestra (−0,106, EE 0,035) pero cambia de signo antes de 2020 (+0,010, p=0,72) y no es significativo desde 2014: la corrección hacia el equilibrio no es estable.
- Costes reales con signo negativo en el largo plazo (−0,66) y tipo real ≈0: relación estadística, no estructural. DOLS real con BG, RESET y VIF (17) que fallan.
- Ningún término del corto plazo real sobrevive a Bonferroni (K=576-1.728); el preferido rara vez gana en el bootstrap de la selección; no mejora al AR(4) fuera de muestra.

**Prioridad 1 (identificación de P2) · F3 (aprobada en re-revisión)**

- Inmigración y precios: con el IV shift-share (Card, cuotas 2002), ningún efecto sobrevive al wild cluster bootstrap ni a Holm (150 especificaciones; p Holm mínimo 0,051). El IC95 % del IPV [−3,90; 0,67] excluye las magnitudes de Saiz (2007) y González-Ortega (2013); la diferencia se atribuye a diseño y periodo (2008+, peso de la cuota europea 2002 y de Baleares), no a un error.
- Pretendencias: significativas para el IPC alquiler (grupo América); la prueba 1996-2001 no es computable con data/processed (sin precios por CCAA antes de 2002; cálculo externo del revisor p=0,13).
- 17 clusters: J de Hansen con baja potencia; AKM solo simplificado (5 grupos); BHJ inviable con 5 grupos.
- Canal comprador (compras de extranjeros residentes): coeficiente 2SLS muy negativo incluso sin 2008-09 → posible violación de la exclusión; no se interpreta.
- Sin flujos de inmigración trimestrales; el flujo anual nacional (N≈17-27) no permite inferencia HAC fiable.

**Prioridad 2 (alcance de P4) · F5 (aprobada en re-revisión)**

- Panel anual de 17 CCAA (2009-2025): el efecto de la cuota extranjera depende de la alineación temporal (0,1 a 1,9 % por pp) y ninguno sobrevive a Holm (mínimo 0,151); asociación.
- No se detecta heterogeneidad entre CCAA (poolability p wild 0,363; límite de aleatorización 1/17), lo que no prueba homogeneidad; la C. Valenciana solo difiere en lo descriptivo y el signo depende de la medida de precio (IPV vs valor tasado).
- El test CD de Pesaran no es interpretable sobre residuos de FE bidireccional/CCE (Juodis y Reese 2022); no se calculó el CDw.
- 17 clusters: inferencia apoyada en wild cluster bootstrap; terminadas retardadas con signo positivo (contrario a lo esperado, p wild 0,075).

**Prioridad 2 (magnitudes de P3) · F4 (aprobada en re-revisión)**

- Déficit 2021-2025: 866.100 (EPA corregida, principal), 810.936 (ECP a 1 de enero), frente a ~750.000 del BdE. La diferencia (≈116.100) se descompone en +55.164 por la fuente de hogares y +60.936 por la vivienda protegida, ausente de nuestras terminadas (solo vivienda libre MIVAU). Que el BdE use la ECP es una inferencia; la cifra de 100.980 terminadas en 2024 (prensa) está NO VERIFICADA.
- Elasticidad de la oferta: los DOLS en niveles son descriptivos (cointegración 1/3, ECM no significativo, BG y RESET fallan, quiebre 2014). En Δ4, iniciadas β=1,39 (EE 0,63): no se rechaza β=0,45 (p Holm 0,27). El 0,45 del BdE (Caldera-Johansson 2013; Cavalleri et al. 2019, NO VERIFICADAS) mide previsiblemente otro concepto (inversión residencial / stock); la traducción flujo→stock no se ha hecho.
- Instrumentos del precio: solo la renta es defendible como desplazador de demanda excluido; ocupados y población pueden afectar a la oferta (exclusión dudosa).

**Prioridad 3 (datos) · Datos (F1, aprobada)**

- Población nacional antes de 2021: semestral (1 enero / 1 julio) interpolada log-linealmente a T2/T4 → Δ1 trimestral con MA mecánica.
- Población por CCAA: solo anual (1 enero) 2002-2025; en el panel trimestral está interpolada.
- No hay flujos de inmigración trimestrales útiles (INE EMCR desde 2023T2, muy dispersos); flujo anual nacional de Eurostat 1998-2024 con quiebre en 2021; sin flujos anuales por CCAA (tabla INE 69691 no descargada).
- Oferta: permisos (Eurostat) y viviendas libres iniciadas/terminadas (MIVAU) son proxies; no hay visados CSCAE ni certificados de fin de obra.
- Hogares: EPA trimestral 2002+ con quiebre metodológico en 2021T1 (−1,1 %); solo nacional.
- Precio largo: `p_bde` (BdE) = `p_tasado` (MIVAU); una única serie larga desde 1995.
- Deflactor: implícito del PIB (CNTR SA), no un deflactor de consumo.
- València: padrón por nacionalidad solo hasta 2022; varias series municipales con N corto (≤ 14 años).

*Fuentes: `docs/limitaciones.md`.*

## 10. Qué NO se puede afirmar

1. Que la inmigración **cause** subidas de precios (o de alquileres): el IV no sobrevive al wild cluster bootstrap ni a Holm (mínimo 0,051) y el alquiler tiene pretendencia significativa.

2. Que el modelo del precio **prediga mejor que un AR(4)**: DM p = 0,509 (real) y 0,290 (nominal), y RMSE del preferido mayor que el del AR(4) (real).

3. Que la **elasticidad de la oferta esté identificada**: cointegración 1/3, ECM no significativo, IV solo defendible con la renta; en Δ4 no se rechaza 0,45.

4. Que exista un **equilibrio de largo plazo estable**: cointegración nominal 1/3; real 3/3 pero el ect pasa de 0,010 (pre-COVID, p = 0,720) a -0,106; costes y tipo con signos no esperados; Bai-Perron: 2011Q4, 2019Q2, 2023Q2.

5. **Efectos causales en València** (ni de la inmigración, ni del turismo, ni de ninguna otra variable): la comparativa es descriptiva y la beta es inestable con componente parte-todo.

6. Que cualquier coeficiente individual del corto plazo sea la «verdadera» especificación: el preferido gana en el 9,6 % de las réplicas del bootstrap de la selección y tras Bonferroni: ningún término del corto plazo sobrevive a Bonferroni (K = nº de modelos de la búsqueda que lo contienen).

7. Que la **heterogeneidad entre CCAA sea nula**: solo que no se detecta (p wild de poolability = 0,363; límite de aleatorización 1/17).

8. Que el **déficit sea exactamente** 750.000 o 866.100: depende de la fuente de hogares (rango 802.152-866.100 entre variantes con corrección) y de la ausencia de protegidas.

9. Que las referencias Caldera-Johansson (2013) y Cavalleri et al. (2019) respalden el 0,45 del BdE: NO VERIFICADAS de forma independiente.

## 11. Número total de especificaciones probadas y corrección por búsqueda

**Total: 3.812 especificaciones registradas** en `output/registro_busqueda.csv` (concatenación de las fases F2-F6, con columnas `fase`, `n_total_fase` y `n_total_registro`).

| fase | especificaciones |
|---|---|
| F2 | 3.483 |
| F3 | 150 |
| F4 | 128 |
| F5 | 23 |
| F6 | 28 |

De las 3.483 de F2, 1.728 son la búsqueda de corto plazo nominal y 1.728 la real (candidatos cerrados antes de estimar). Correcciones aplicadas: Bonferroni por término con K de la búsqueda (F2), Holm sobre 150 (F3), Holm sobre 15 variantes de b2 (F5), Holm sobre 114 modelos de elasticidad y sobre las 15 hipótesis β = 0,45 (F4) y Holm sobre 16 contrastes (F6). No se calculó Romano-Wolf. Las 'correcciones' del registro son parciales: condicionales a los p-valores válidos y no cubren la elección de la muestra ni del precio (nominal/real).

*Fuentes: `output/registro_busqueda.csv`; `output/f3/correccion_busqueda.csv`; `output/f4/correccion_busqueda.csv`; `output/f5/correccion_busqueda_beta2.csv`; `output/f6/correccion_holm.csv`.*

## 12. Referencias citadas (marca de verificación)

Marca según `docs/literatura.md`: VERIFICADA (comprobada contra Crossref/IDEAS/PDF oficial), PARCIAL (DOI, páginas o versión sin comprobar) y NO VERIFICADA. Se listan solo las referencias citadas en este informe o en los resúmenes de `output/`.

Total: 56 (VERIFICADA: 42; PARCIAL: 11; NO VERIFICADA: 3).

- [VERIFICADA] Accetturo et al. (2014). Don't stand so close to me: The urban impact of immigration
- [VERIFICADA] Bai y Perron (1998). Estimating and testing linear models with multiple structural changes
- [VERIFICADA] Bai y Perron (2003). Computation and analysis of multiple structural change models
- [PARCIAL] Banco de España (2025). Informe de Estabilidad Financiera, otoño 2025
- [VERIFICADA] Banco de España (2026). Informe Anual 2025
- [VERIFICADA] Banerjee, Dolado y Mestre (1998)
- [PARCIAL] Bover y Jimeno (2007). House prices and employment reallocation: International evidence
- [VERIFICADA] Breusch (1978)
- [PARCIAL] Breusch y Pagan (1979)
- [VERIFICADA] Brown, Durbin y Evans (1975)
- [NO VERIFICADA] Caldera y Johansson (2013). The price responsiveness of housing supply in OECD countries
- [VERIFICADA] Cameron, Gelbach y Miller (2008)
- [VERIFICADA] Card (2001). Immigrant inflows, native outflows, and the local labor market impacts of higher immigration
- [NO VERIFICADA] Cavalleri et al. (2019). How responsive are housing markets in the OECD? OECD Economics Department Working Papers 1589
- [PARCIAL] Chow (1960)
- [VERIFICADA] Dickey y Fuller (1979)
- [VERIFICADA] Diebold y Mariano (1995)
- [VERIFICADA] Driscoll y Kraay (1998)
- [VERIFICADA] Durbin y Watson (1950)
- [VERIFICADA] Engle y Granger (1987). Co-integration and error correction: Representation, estimation, and testing
- [VERIFICADA] Glaeser y Gyourko (2005). Urban decline and durable housing
- [VERIFICADA] Glaeser y Gyourko (2018). The economic implications of housing supply
- [PARCIAL] Godfrey (1978a)
- [VERIFICADA] Godfrey (1978b)
- [VERIFICADA] Goldsmith-Pinkham et al. (2020). Bartik instruments: What, when, why, and how
- [VERIFICADA] González y Ortega (2013). Immigration and housing booms: Evidence from Spain
- [VERIFICADA] Hilber y Vermeulen (2016). The impact of supply constraints on house prices in England
- [VERIFICADA] Himmelberg et al. (2005). Assessing high house prices: Bubbles, fundamentals and misperceptions
- [PARCIAL] Holm (1979)
- [PARCIAL] Jarque y Bera (1987)
- [VERIFICADA] Johansen (1988). Statistical analysis of cointegration vectors
- [VERIFICADA] Johansen (1991). Estimation and hypothesis testing of cointegration vectors in Gaussian vector autoregressive models
- [VERIFICADA] Jordà (2005). Estimation and inference of impulse responses by local projections
- [VERIFICADA] Juodis y Reese (2022)
- [NO VERIFICADA] Kinnon (1996)
- [VERIFICADA] Kwiatkowski, Phillips, Schmidt y Shin (1992)
- [VERIFICADA] Leamer (1983)
- [PARCIAL] MacKinnon (1996)
- [VERIFICADA] MacKinnon y Webb (2018)
- [PARCIAL] Martínez Pagés y Maza (2003). Análisis del precio de la vivienda en España
- [VERIFICADA] Mian y Sufi (2009). The consequences of mortgage credit expansion: Evidence from the U.S
- [VERIFICADA] Mian y Sufi (2011). House prices, home equity-based borrowing, and the US household leverage crisis
- [VERIFICADA] Newey y West (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix
- [PARCIAL] Pesaran (2004)
- [VERIFICADA] Pesaran (2006). Estimation and inference in large heterogeneous panels with a multifactor error structure
- [VERIFICADA] Pesaran (2007)
- [VERIFICADA] Pesaran (2015)
- [VERIFICADA] Pesaran et al. (2001). Bounds testing approaches to the analysis of level relationships
- [VERIFICADA] Poterba (1984). Tax subsidies to owner-occupied housing: An asset-market approach
- [VERIFICADA] Ramsey (1969)
- [VERIFICADA] Saiz (2007). Immigration and housing rents in American cities
- [VERIFICADA] Saiz (2010). The geographic determinants of housing supply
- [PARCIAL] Stock y Watson (1993)
- [VERIFICADA] Sá (2015). Immigration and house prices in the UK
- [VERIFICADA] Webb (2023; WP Queen's 2014)
- [VERIFICADA] Zivot y Andrews (1992). Further evidence on the Great Crash, the oil-price shock, and the unit-root hypothesis

*Fuentes: `output/tablas/referencias.csv`; `docs/literatura.md`.*

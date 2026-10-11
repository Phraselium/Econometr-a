# Hipótesis v6 — pre-registro M0 (rehecho tras docs/v6/revision_M0.md)

Fecha: 2026-10-11. Nada de lo que sigue se ha estimado. Variables en `docs/v6/diccionario.md`; paneles en
`output/v6/M0/paneles/*_train.csv.gz`; cortes en `output/v6/M0/sellado.md`.

Referencias (estado explícito): Caldera y Johansson (2013), *Journal of Housing Economics*, DOI 10.1016/j.jhe.2013.05.002,
VERIFICADA. Cavalleri, Cournède y Özsöğüt (2019), OECD Economics Department WP 1589, DOI 10.1787/4777e29a-en: DOI verificado;
cuartil no aplicable (documento de trabajo), no es VERIFICADA en sentido estricto. Sá (2015) y Saiz (2007): DOI en
`docs/literatura.md`, cuartil no verificado; solo orientan el signo.

Predicción no es causalidad: SHAP, importancias, ALE y dependencias parciales son descriptivas (C4).

## 1. Familias de modelos y criterio 1 (operativo)

Las tres familias de evidencia para cada variable son:
- **F1, econometría:** coeficiente del regresor en M1 (FE de unidad y de año, errores agrupados por CCAA con wild cluster bootstrap de Webb). Significativo tras Holm en la familia de la sección 4.
- **F2, BMA/PIP:** probabilidad de inclusión posterior (PIP) ≥ 0,5 en M2 (BMA sobre el conjunto preregistrado de regresores).
- **F3, ML:** importancia por permutación en M3 por encima del ruido (percentil 95 de la importancia con desenlace permutado).

**Criterio 1 de «relevante con seguridad»:** una variable se declara así solo si cumple A Y B:
- **A:** mismo signo que en la sección 2 en al menos 2 de las 3 familias.
- **B:** el mejor modelo que la incluye bate a la línea base en la validación sellada (M4): RMSE menor que AR(4) y que ECM v1 en la misma muestra, con DM-HLN significativo al 5 % (cola a favor del modelo con la variable).

Si solo cumple A, es EXPLORATORIA (C4). Con C4 el veredicto es como máximo «ANALIZADA, NO CONCLUYENTE». Sin lenguaje causal por debajo de C3.

## 2. Signos esperados (principal) y razón

Todas las variables entran en t−1 (flujos y estados). Desenlace en niveles de logaritmo.

| Mercado | Variable (t−1) | Signo | Razón |
|---|---|---|---|
| Compra (precio) | ln_pob, share_ext_pob | (+) | Demanda; efecto de inmigración (Sá, cuartil no verificado). |
| Compra (precio) | ln_pib_pc, ln_ocupados_miles | (+) | Renta y empleo. |
| Compra (precio) | paro_tasa | (−) | Menos demanda solvente. |
| Compra (precio) | ln_terminadas_libres, ln_iniciadas_libres | (−) | Oferta; elasticidad limitada (Caldera y Johansson, 2013; Cavalleri et al., 2019). |
| Compra (precio) | ln_suelo_pm2_m50k | (+) | Coste de suelo. |
| Compra (precio) | ln_vut | (?) | Demanda turística frente a sustitución: sin signo a priori. |
| Compra (precio) | ln_hip_viv_num | (+) | Crédito y precios (sin signo causal). |
| Alquiler (stock) | ln_pob, share_ext_pob | (+) | Demanda de alquiler (Saiz, 2007, cuartil no verificado). |
| Alquiler (stock) | ln_pib_pc | (+) | Renta. |
| Alquiler (stock) | ln_vut | (+) | Sustitución del stock residencial. |
| Alquiler (stock) | ln_terminadas_libres, ln_iniciadas_libres | (−) | Oferta. |
| Alquiler (stock) | n_mun_tensionados, n_mun_topes_cat | (−) condicionado | Tope legal; signo no fijado, es la hipótesis más expuesta a fallar. |
| Volumen de compra | ln_pib_pc, ln_ocupados_miles, ln_pob | (+) | Renta, empleo y demanda. |
| Volumen de compra | paro_tasa | (−) | Menos compras. |
| Volumen de compra | ln_terminadas_libres, ln_iniciadas_libres | (?) | Ciclo y oferta: sin signo a priori. |
| Contratos nuevos | — | — | **Sin modelo principal** (ver §4). |

## 3. Especificaciones

- **Regresores cerrados:** las listas de `src/v6/m0_run.py` (`CP_REG` de 10 variables para compra; `ALQ_REG` de 8 para alquiler; `DIS_REG` de 2 para distrito). Ninguna se añade en M1 o M2 sin nueva entrada en este documento.
- **Retardos:** t−1 para todas. Sin retardos adicionales en la especificación principal. Los retardos de orden superior van a robustez.
- **Forma funcional:** desenlace en log-niveles con FE de unidad y de año (M1). Diferencias d_ln como robustez.
- **Variables nacionales:** no entran como regresores de los modelos provinciales. Con FE de año, cualquier variable común a todas las provincias queda absorbida, así que no aportan identificación. Los agregados que suman desenlaces provinciales (`cv_etdp_nacional_suma_prov`, `hip_viv_num_nacional_suma_prov`, `pm2_tasado_nacional`, `ipc_alq_nacional_idx`) quedan excluidos de cualquier modelo por contener los desenlaces de las provincias selladas (N3). El IPV CCAA se usa en tasas (`ipv_tasa_anual_pct`), no en niveles.
- **Muestra común:** M1, AR(4) y ECM v1 se estiman en la misma muestra (mismas unidades y años). ECM v1 se define como el modelo de corrección de error del proyecto (v1) a nivel provincial, con los mismos regresores t−1 y el desenlace en log; si una unidad no tiene la serie completa, se excluye de los tres.
- **Contratos nuevos:** sin modelo. El panel tiene 3 provincias CV (GVA) y 4 CAT (Incasòl) con fianzas, N ≈ 15 filas, sin potencia. Queda como descriptivo.
- **M2:** BMA sobre los regresores de la sección 2 con priores uniformes sobre modelos; PIP ≥ 0,5 como umbral.
- **M3:** importancia por permutación sobre el mismo conjunto de regresores (no sobre variables fuera de la lista).

## 4. Corrección de contrastes

- **Holm** para las hipótesis confirmatorias: familia = variables de la sección 2 × mercado principal (compra con desenlace `ln_pm2_tasado`; alquiler con `ln_alq_m2_serpavi_vc`; volumen con `ln_cv_etdp`).
- **BH** (q = 0,10) para lo exploratorio y la robustez (desenlaces alternativos, retardos, diferencias).
- Todas las especificaciones probadas se registran en el Registry de `src/econ_utils.py`.

## 5. Validación temporal por bloques con embargo

- Dentro del entrenamiento: K = 3 pliegues de origen (años 2018, 2020 y 2022 para paneles anuales). Para cada origen, el entrenamiento son los años < origen − 1 y la validación son origen y origen + 1.
- **Embargo: 1 año** entre el último año de entrenamiento y el primero de validación.
- Trimestral: el embargo es de 4 trimestres.
- La muestra sellada (M4) no interviene en la elección de pliegues ni de modelos.

## 6. Métricas, Diebold-Mariano y horizonte

- RMSE y MAE en el horizonte h = 1 año (paneles anuales) o h = 1 trimestre (trimestral); h = 2 como robustez.
- **DM con corrección HLN** (Harvey, Leybourne y Newbold, 1997), pérdida de error cuadrático, varianza de largo plazo con truncamiento de Newey-West en h − 1 retardos, distribución t con n − 1 grados de libertad. Frente al AR(4) en la misma muestra.
- M4: una evaluación por modelo con `holdout.evaluate_v6`, registrada en `docs/v2/holdout_accesos.md`.

## 7. Limitaciones que condicionan la lectura (declaradas)

- **B5, validación contaminada:** el corte temporal de v6 (2025 en compra, 2024 en alquiler) cae dentro de la ventana sellada de v2 (`holdout._mascara_sellada`, años ≥ 2025), que ya se abrió en 8 contrastes (H1, H2, H3-1, H3-2, H3-3a, H3-3b, H6 y H7 de docs/v2/holdout_accesos.md). La parte nueva es la espacial (11 provincias). M4 reporta por separado: (i) provincias selladas en años de entrenamiento (parte nueva) y (ii) el último año (parte contaminada). Las conclusiones se apoyan en (i).
- Contratos nuevos: ninguna provincia GVA ni Incasòl sellada espacialmente (N5); su sellado es solo temporal.
- Distritos: desenlace = punto medio p25-p75 (SERPAVI v3 no trae mediana). p25 y p75 están en el panel para robustez.
- Potencia (`docs/v6/potencia.md`): con N de entrenamiento de 150-400 solo se detectan efectos grandes con seguridad tras Holm. Con 8-11 CCAA, la inferencia clúster exige wild cluster bootstrap.

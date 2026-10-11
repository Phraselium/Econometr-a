# Hipótesis v6 (preregistro M0, pendiente de etiqueta `prereg-v6`)

Fecha: 2026-10-11. Nada de lo que sigue se ha estimado. Las variables son las de `docs/v6/diccionario.md`. Las referencias
se citan solo con su estado: VERIFICADA (DOI en Crossref y cuartil Scimago) o «cuartil no verificado» / NO VERIFICADA.
Referencias VERIFICADAS usadas: Caldera y Johansson (2013), *Journal of Housing Economics*, DOI 10.1016/j.jhe.2013.05.002;
Cavalleri, Cournède y Özsöğüt (2019), OECD Economics Department WP 1589, DOI 10.1787/4777e29a-en. Sá (2015) y Saiz (2007)
tienen DOI en `docs/literatura.md`, pero su cuartil no está verificado: solo se citan como orientación de signo.

Advertencia de predicción: las importancias, SHAP, ALE y dependencias parciales son descriptivas (C4). Ninguna se
interpreta como causal.

## 1. Signos esperados por mercado

Signo: (+) el desenlace sube con la variable; (−) baja; (?) sin signo a priori.

### 1a. Precio de compra (`ln_pm2_tasado`, `ln_pm2_tasado_mun`, `ln_pm2_registradores`)

| Variable | Signo | Razón |
|---|---|---|
| ln_pob, share_ext_pob | (+) | Más demanda por población. Efecto de inmigración sobre precios (Sá, 2015, cuartil no verificado). |
| ln_pib_pc, ln_ocupados_miles | (+) | Renta y empleo elevan la demanda solvente (proxy de renta: PIB pc). |
| ln_terminadas_libres, ln_iniciadas_libres | (−) | Más oferta nueva, precio más bajo. Elasticidad de oferta limitada (Caldera y Johansson, 2013; Cavalleri et al., 2019, VERIFICADAS). |
| ln_suelo_pm2_m50k | (+) | Suelo caro encarece la vivienda nueva; el suelo también es precio (dato parcial). |
| ln_hip_viv_num, credito (nacional) | (+) | Crédito disponible y mayor número de hipotecas en épocas de precios altos (sin signo causal). |
| share_compra_ext_res_pct | (+) | Compra de extranjeros con demanda adicional en zonas de costa e islas (R1A). |
| n_mun_tensionados (en el alquiler) | (?) | No hay signo a priori en precios de compra. |
| ln_vut | (?) | Demanda turística sube precios (+) y sustituye vivienda residencial; el neto es ambiguo. |
| jefatura_proxy_pct | (+) | Más hogares formados por viviendas de demanda. Proxy débil. |

### 1b. Alquiler de stock (`ln_alq_m2_serpavi_vc`, `ln_alq_m2_serpavi_mun`, `ln_alq_m2_serpavi_dis`, `ln_ipc_alq_idx`)

| Variable | Signo | Razón |
|---|---|---|
| ln_pob, share_ext_pob, llegadas brutas desde el extranjero | (+) | Demanda de alquiler. Efecto de la inmigración sobre alquileres (Saiz, 2007, cuartil no verificado). |
| ln_vut, ln_vut_plazas_dis | (+) | Vivienda turística saca stock del residencial y sube alquileres (efecto de sustitución). |
| ln_iniciadas_libres, ln_terminadas_libres | (−) | Más oferta, alquiler más bajo (mismo canal que en compra). |
| n_mun_tensionados, tensionada_mun | (−) condicionado | Un tope legal debería frenar el alquiler registrado. El signo no está fijado: depende de la selección de contratos y del periodo; es la hipótesis más expuesta a fallar. |
| ln_pm2_tasado (ratio precio/alquiler) | (+) | Presión de demanda sobre la rentabilidad de la compra. |

### 1c. Contratos nuevos (`ln_fianza_media_gva_eur`, `pct_fianzas_600_incasol`, `ln_ipva_nuevo_idx`)

| Variable | Signo | Razón |
|---|---|---|
| ln_alq_m2_serpavi_vc (valor de referencia) | (+) | Fianza ligada a la renta del contrato (cuando la fianza es una mensualidad o más). |
| ln_pob, ln_vut | (+) | Demanda de contratos nuevos. |
| n_mun_topes_cat | (−) condicionado | Un tope en vigor limita la renta del contrato nuevo. Mismo caveat que en 1b. |
| ln_n_fianzas_gva / ln_n_fianzas_incasol | (?) | Volumen de rotación; sin signo a priori. |

Caveat: la fianza es un depósito en euros, no una renta mensual. Su transformación a €/mes necesita el número de
mensualidades depositadas, que no está en los datos. Ninguna conclusión en €/mes se obtiene de ellas.

### 1d. Volumen de compra (`ln_cv_etdp`, `ln_cv_registradores`, `ln_hip_viv_num`)

| Variable | Signo | Razón |
|---|---|---|
| ln_pib_pc, ln_ocupados_miles | (+) | Renta y empleo elevan las compras. |
| ln_pob, share_ext_pob | (+) | Más demanda. |
| paro_tasa | (−) | Mayor paro, menos compras. |
| ln_terminadas_libres | (?) | Oferta nueva puede aumentar o indicar ciclo; sin signo a priori. |
| share_contado_proxy | (?) | Proxy débil del peso de la compra al contado. |

## 2. Especificaciones principales

- **M1 (cuantitativa, panel provincial):** panel de efectos fijos por provincia y año, errores agrupados por CCAA
  (17 clústeres). Desenlace: el principal de cada mercado (sección 1 de diccionario.md). Retardos creados en el script de
  modelo (no en M0). Regresores: los de la familia de cada mercado con signo de la sección 1.
- **M2 (dinámica):** modelo de corrección de error (ECM) y AR(4) como línea base, en la MISMA muestra que M1, con el
  ECM v1 del proyecto como referencia de comparación.
- **Benchmark obligatorio:** AR(4) y ECM v1 sobre la misma muestra. Sin ellos, ninguna mejora se reporta.

## 3. Métricas de M3 y M4

- M3 (selección en validación en bloques con embargo, solo entrenamiento): RMSE y MAE en el horizonte 1 y 4 trimestres
  (paneles trimestrales) o 1 año (anuales), frente a la línea base. Diebold-Mariano (DM) frente al AR(4) con el
  ajuste de muestras pequeñas que se fije en M3.
- M4 (muestra sellada, una vez por modelo mediante `holdout.evaluate_v6`): RMSE, MAE y DM frente al AR(4), con la
  misma muestra sellada para todos los modelos comparados. Se registra el número de aperturas en
  `docs/v2/holdout_accesos.md`. No se usa la muestra sellada para elegir modelo.
- Todas las especificaciones probadas se registran en el Registry de `src/econ_utils.py`, con Holm o BH.

## 4. Criterio de «relevante con seguridad»

Una variable se declara relevante con seguridad solo si cumple las tres condiciones siguientes:

1. Coincidencia de al menos dos familias independientes de variables (demanda, oferta, crédito y tipo, turismo, regulación,
   renta), con el mismo signo que en la sección 1.
2. Significación tras Holm (o BH) sobre todas las especificaciones registradas del mercado.
3. Supervivencia en la validación en bloques con embargo (M3) y, una única vez, en la muestra sellada (M4), con
   DM frente al AR(4) favorable en la misma muestra.

Si una variable solo cumple (1) o (2), queda como EXPLORATORIA (C4). Si no cumple (3), no se declara relevante. Sin
lenguaje causal por debajo de C3. Con C4, el veredicto es como máximo «ANALIZADA, NO CONCLUYENTE».

## 5. Limitaciones que condicionan las hipótesis

- La validación sellada es contaminada descriptivamente (decisiones.md).
- El desenlace de alquiler de stock en distritos es un punto medio p25-p75, no la mediana.
- Contratos nuevos solo en 3 provincias CV y 4 CAT: la potencia es muy baja (ver potencia.md).
- Potencia: ninguna especificación con N < 400 detecta efectos pequeños con seguridad tras Holm (potencia.md).

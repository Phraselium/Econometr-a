# Peso predictivo de cada variable (M2, provincia) — C4, asociativo

Fecha: 2026-10-11. PIP = soporte predictivo/asociativo dentro del espacio de modelos, NO efecto causal. Datos: paneles *_train de M0 (anual, provincia); variables en t−1 con FE de unidad y año fuera del promedio. g-prior g = max(N, K²); prior uniforme (columna PIP) y beta-binomial(1,1) (PIP bb). «PIP núcleo» = BMA sin ln_vut ni ln_suelo (más observaciones). Rango BMA = intervalo creíble 95 %; mult. = mediana [p25; p75] del multiverso. Unidad: +10 % en variables ln_, +1 pp en share_/paro, +1 municipio en contadores. ALQUILER = stock SERPAVI, €/m²/mes → %, y €/mes con el alquiler medio del panel (413 €/mes). COMPRA = valor tasado MIVAU → %, y €/m² con el precio medio del panel (1257 €/m²). Mismo signo = % de especificaciones con el signo de la mediana. Sel. enet = elastic net conjunto (CV en bloques, embargo 1 año).

## ALQUILER (stock, SERPAVI; medida: mediana VC)

| Variable | Unidad | PIP | PIP bb | PIP núcleo | BMA media % [IC95] | Mult. mediana % [p25; p75] | Mult. €/mes | % mismo signo | Sel. enet | PDS coef % [IC95] | Capa |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ln_pob | +10 % | 1.00 | 1.00 | 1.00 | 10.07 [6.85; 12.99] | 5.31 [1.72; 9.58] | 21.92 [7.08; 39.51] | 82 | sí | 8.34 [3.75; 12.93] | C4 |
| share_ext_pob | +1 pp | 0.30 | 0.15 | 0.06 | 0.38 [0.00; 2.26] | 0.24 [-0.14; 0.79] | 0.98 [-0.58; 3.27] | 67 | sí | 1.30 [-1.01; 3.62] | C4 |
| ln_pib_pc | +10 % | 0.10 | 0.05 | 0.19 | 0.01 [-0.05; 0.28] | 0.06 [-0.17; 0.28] | 0.26 [-0.71; 1.14] | 55 | no | 0.15 [-0.48; 0.78] | C4 |
| ln_vut | +10 % | 0.12 | 0.06 | – | -0.01 [-0.24; 0.03] | 0.01 [-0.11; 0.15] | 0.04 [-0.45; 0.62] | 62 | no | -0.21 [-0.63; 0.22] | C4 |
| ln_terminadas_libres | +10 % | 0.17 | 0.08 | 0.06 | -0.01 [-0.06; 0.00] | 0.00 [-0.01; 0.01] | 0.01 [-0.05; 0.05] | 54 | no | -0.03 [-0.07; 0.01] | C4 |
| ln_iniciadas_libres | +10 % | 0.09 | 0.04 | 0.97 | -0.00 [-0.02; 0.02] | 0.00 [-0.01; 0.03] | 0.01 [-0.04; 0.13] | 65 | no | 0.01 [-0.06; 0.08] | C4 |
| n_mun_topes_cat | +1 municipio | 0.23 | 0.12 | 0.09 | 0.01 [0.00; 0.05] | 0.00 [-0.01; 0.01] | 0.00 [-0.03; 0.04] | 54 | no | 0.02 [0.00; 0.04] | C4 |

## COMPRA, precio (medida_precio: valor tasado MIVAU)

| Variable | Unidad | PIP | PIP bb | PIP núcleo | BMA media % [IC95] | Mult. mediana % [p25; p75] | Mult. €/m² | % mismo signo | Sel. enet | PDS coef % [IC95] | Capa |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ln_pob | +10 % | 0.76 | 0.79 | 1.00 | 14.24 [0.00; 26.55] | 6.06 [-0.15; 11.66] | 76.21 [-1.88; 146.53] | 72 | sí | 5.71 [-15.09; 26.51] | C4 |
| share_ext_pob | +1 pp | 0.31 | 0.23 | 0.77 | 1.21 [0.00; 6.51] | 1.06 [-0.53; 2.21] | 13.27 [-6.63; 27.81] | 61 | sí | 2.18 [-3.78; 8.13] | C4 |
| ln_pib_pc | +10 % | 0.84 | 0.59 | 0.47 | 3.77 [0.00; 7.43] | -0.05 [-0.30; 0.57] | -0.61 [-3.78; 7.16] | 51 | sí | 4.37 [1.83; 6.90] | C4 |
| paro_tasa | +1 pp | 0.13 | 0.05 | 0.19 | 0.05 [-0.12; 0.85] | 0.05 [-0.09; 0.37] | 0.61 [-1.19; 4.65] | 50 | sí | 0.74 [-0.25; 1.73] | C4 |
| ln_ocupados_miles | +10 % | 0.20 | 0.08 | 0.07 | 0.60 [0.00; 5.89] | 0.77 [0.18; 1.36] | 9.66 [2.29; 17.11] | 88 | sí | 4.16 [0.46; 7.86] | C4 |
| ln_terminadas_libres | +10 % | 0.12 | 0.05 | 0.49 | -0.01 [-0.25; 0.02] | 0.01 [-0.03; 0.10] | 0.16 [-0.40; 1.21] | 56 | sí | -0.04 [-0.22; 0.14] | C4 |
| ln_iniciadas_libres | +10 % | 0.12 | 0.05 | 0.06 | 0.01 [0.00; 0.26] | 0.00 [-0.03; 0.05] | 0.03 [-0.41; 0.62] | 55 | sí | 0.08 [-0.32; 0.48] | C4 |
| ln_suelo_pm2_m50k | +10 % | 0.14 | 0.06 | – | 0.03 [-0.01; 0.41] | 0.02 [-0.05; 0.15] | 0.22 [-0.57; 1.83] | 56 | sí | 0.20 [-0.28; 0.68] | C4 |
| ln_vut | +10 % | 0.10 | 0.04 | – | -0.00 [-0.26; 0.23] | 0.08 [-0.17; 0.39] | 0.96 [-2.10; 4.92] | 56 | no | 0.08 [-0.62; 0.79] | C4 |
| ln_hip_viv_num | +10 % | 0.12 | 0.05 | 0.18 | 0.09 [0.00; 1.70] | 0.05 [-0.14; 0.64] | 0.63 [-1.72; 8.10] | 62 | sí | 0.68 [-1.40; 2.76] | C4 |

## COMPRA, volumen (compraventas INE ETDP; efecto en %)

| Variable | Unidad | PIP | PIP bb | PIP núcleo | BMA media % [IC95] | Mult. mediana % [p25; p75] | % mismo signo | Sel. enet | PDS coef % [IC95] | Capa |
|---|---|---|---|---|---|---|---|---|---|---|
| ln_pob | +10 % | 0.10 | 0.03 | 0.35 | -0.10 [-6.91; 9.13] | -11.41 [-53.76; 13.25] | 69 | no | -12.57 [-71.47; 46.33] | C4 |
| share_ext_pob | +1 pp | 0.11 | 0.03 | 0.81 | 0.26 [-0.57; 4.55] | 2.87 [-2.88; 10.53] | 67 | no | 9.54 [-7.06; 26.14] | C4 |
| ln_pib_pc | +10 % | 0.09 | 0.02 | 0.06 | 0.06 [-1.88; 2.97] | 0.15 [-3.64; 1.72] | 55 | no | 0.42 [-4.81; 5.66] | C4 |
| paro_tasa | +1 pp | 0.22 | 0.06 | 0.06 | -0.33 [-2.72; 0.00] | -0.05 [-0.41; 0.84] | 53 | no | -2.35 [-4.66; -0.04] | C4 |
| ln_ocupados_miles | +10 % | 0.10 | 0.03 | 0.06 | -0.01 [-3.20; 3.45] | -1.24 [-3.31; 0.77] | 62 | no | -8.09 [-14.55; -1.64] | C4 |
| ln_terminadas_libres | +10 % | 0.11 | 0.03 | 0.07 | -0.03 [-0.63; 0.01] | -0.04 [-0.20; 0.03] | 64 | no | -0.25 [-1.16; 0.65] | C4 |
| ln_iniciadas_libres | +10 % | 0.98 | 0.83 | 0.79 | -1.46 [-2.30; -0.46] | -0.22 [-0.56; 0.27] | 52 | sí | -1.65 [-2.22; -1.08] | C4 |
| ln_suelo_pm2_m50k | +10 % | 0.10 | 0.02 | – | 0.02 [-0.15; 0.57] | -0.47 [-0.72; -0.28] | 88 | no | 0.22 [-0.88; 1.32] | C4 |
| ln_vut | +10 % | 0.14 | 0.04 | – | 0.12 [0.00; 1.71] | -0.92 [-1.40; 0.52] | 70 | no | 1.13 [-0.04; 2.31] | C4 |
| ln_hip_viv_num | +10 % | 0.09 | 0.02 | 0.99 | -0.03 [-1.88; 1.42] | 0.66 [-0.41; 4.24] | 65 | no | -0.34 [-4.02; 3.34] | C4 |

## Variables que aparecen en más modelos (PIP) en un mercado y no en el otro (PIP ≥ 0,5 en uno y < 0,2 en el otro)

- **share_ext_pob**: se asocia con COMPRA y no con ALQUILER (núcleo). PIP alquiler 0.30 (núcleo 0.06), PIP compra 0.31 (núcleo 0.77).
- **ln_pib_pc**: se asocia con COMPRA y no con ALQUILER (set completo). PIP alquiler 0.10 (núcleo 0.19), PIP compra 0.84 (núcleo 0.47).
- **ln_iniciadas_libres**: se asocia con ALQUILER y no con COMPRA (núcleo); el orden temporal con el crecimiento del alquiler no se distingue de cero (K3, C4): la asociación no indica que construir suba el alquiler. PIP alquiler 0.09 (núcleo 0.97), PIP compra 0.12 (núcleo 0.06).

Lectura: C4 en todas las filas; veredicto máximo «ANALIZADA, NO CONCLUYENTE». Sin lenguaje causal. El BMA completo usa solo observaciones con ln_vut y ln_suelo disponibles (alquiler N=106, compra N=64), por lo que su potencia es baja.
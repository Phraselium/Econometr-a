# Resumen F6: València (precios, alquiler, población extranjera, VUT)

Todo lo que sigue es **asociación** o descripción; no hay identificación causal en esta fase. Reproducible con `python3 src/f6_valencia.py`.

## A. Estimación (N >= 40 trimestres; HAC Newey-West, maxlags=4 salvo indicación)

Muestra común precios: 2005Q1-2026Q2 (N=86 niveles; N=82 en Δ4). Compraventas: 2007Q1-2026Q1 (N=77).

- **Índices 2015=100 y crecimiento acumulado (%) del valor tasado** (`crecimiento_acumulado_p_tasado.md`):
  2008-2013: València -44.6, provincia -32.0, CV -32.2, España -29.7;
  2014-2019: València 14.6, provincia 11.5, CV 9.2, España 12.7;
  2020-2026Q2: València 100.0, provincia 65.5, CV 57.1, España 42.5.
- **Sensibilidad a la base (variación acumulada %, `ipv_vs_tasado_acumulado.md`)**: 2019Q4->2026Q2 València 100,0, CV 57,1, España 42,5 (valor tasado); con base 2020Q1 València 97,3; medias anuales 2019->2025 València 83,2, España 29,6. El orden se mantiene.
- **Contraste con el IPV del INE (CV frente a España)**: 2019Q4->2026Q2 el IPV da CV 61,8 % frente a España 59,5 % (diferencia 2,3 pp), mientras que con valor tasado es 57,1 % frente a 42,5 % (14,6 pp). El exceso CV-España es sobre todo del valor tasado (composición de lo tasado). Diferencial medio CV-España 2020-26 (Δ4, pp): IPV 0,3 (EE 0,1) frente a valor tasado 1,3 (EE 0,4). **Para el municipio de València no hay un contraste independiente** (solo valor tasado), así que el +100 % puede reflejar en parte composición de tasaciones.
- **Beta de Δ4 ln p_tasado València (muestra completa, HAC4)**: vs Provincia: β=1,39 (EE HAC 0,09; p(β=1)=0,000); vs C. Valenciana: β=1,51 (EE HAC 0,10; p(β=1)=0,000); vs España: β=1,73 (EE HAC 0,11; p(β=1)=0,000). Esta beta es un **promedio inestable** (CUSUM, Wald de quiebre, Bai-Perron). Robusta a Δ1 sin solapamiento (`beta_delta1_robustez.md`): Provincia β=1,43 (EE 0,13); C. Valenciana β=1,48 (EE 0,16); España β=1,73 (EE 0,18).
- **Beta por tramos (interacciones, N=82, HAC8; `beta_por_tramos.md`; cada tramo N<40, descriptivo dentro del modelo)**: vs España 2006-2013: β=1,67 (EE 0,11); 2014-2019: β=2,80 (EE 0,63); 2020-2026: β=1,20 (EE 0,13); vs CV 2006-2013: β=1,58 (EE 0,12); 2014-2019: β=3,38 (EE 0,70); 2020-2026: β=1,02 (EE 0,11); vs provincia 2006-2013: β=1,33 (EE 0,09); 2014-2019: β=2,62 (EE 0,29); 2020-2026: β=1,02 (EE 0,13). Wald de igualdad de betas entre tramos: España p=0,002, CV p=0,000, provincia p=0,000.
- **Diferencial medio de crecimiento por tramo (pp/año, `diferencial_nivel_por_tramos.md`, HAC8)**: vs España 2006-2013: -1,7 (EE 2,0); 2014-2019: 0,3 (EE 2,5); 2020-2026: 5,6 (EE 1,0); vs CV 2006-2013: -1,0 (EE 1,9); 2014-2019: 0,7 (EE 2,6); 2020-2026: 4,2 (EE 0,7). El diferencial medio de toda la muestra (vs Provincia: 0,62 pp (IC95 % -1,36 a 2,59; EE HAC 1,01; p=0,541); vs C. Valenciana: 1,17 pp (IC95 % -1,08 a 3,43; EE HAC 1,15; p=0,308); vs España: 1,18 pp (IC95 % -1,37 a 3,74; EE HAC 1,30; p=0,364)) **promedia tramos de signo contrario y no resume bien**; no se presenta como resultado.
- **Conclusión de precios**: la beta de la muestra completa (>1) no es un parámetro estable. Desde 2020 el mayor crecimiento de València respecto a la CV y España se asocia con un **diferencial de nivel** (constante positiva del tramo) más que con una mayor sensibilidad (amplificación) al ciclo: ver las betas del último tramo. Es una asociación y, al ser València parte de provincia, CV y España, hay un componente mecánico parte-todo.
- **Compraventas MIVAU**: cuota de extranjeros CV (media 12,2 %) frente a España (8,2 %). Hecho descriptivo: la cuota CV supera a la de España en **77/77 trimestres** (mínimo 0,07 pp; diferencia media 3,93 pp, EE HAC4 0,33, HAC8 0,43, HAC12 0,49; la diferencia es muy persistente y el p-valor numérico no es fiable). Pendientes lineales descriptivas (series I(1), sin p-valor): CV 0,54 y España 0,34 pp/año. Aviso: salto de cobertura de `trans_extranjeros` entre 2008 y 2009. La serie MIVAU de extranjeros **no existe a nivel de municipio**.
- **Diagnósticos que fallan (p<0,05)** en los modelos beta (Δ4): beta_València_vs_Provincia:BG4_p=0.000, beta_València_vs_Provincia:RESET_p=0.000, beta_València_vs_Provincia:CUSUM_p=0.015, beta_València_vs_C. Valenciana:BG4_p=0.000, beta_València_vs_C. Valenciana:RESET_p=0.001, beta_València_vs_C. Valenciana:CUSUM_p=0.043, beta_València_vs_España:BG4_p=0.000, beta_València_vs_España:RESET_p=0.022, beta_València_vs_España:CUSUM_p=0.001. Quiebres con Wald HAC(8) significativos (sustituye al Chow clásico, que sobrerrechaza con residuos autocorrelacionados; `quiebres_wald_hac.md`): València_vs_Provincia@2020Q1(p=0.004), València_vs_Provincia@2022Q3(p=0.023), València_vs_C. Valenciana@2020Q1(p=0.000), València_vs_C. Valenciana@2022Q3(p=0.005), València_vs_España@2020Q1(p=0.000), València_vs_España@2022Q3(p=0.015). Bai-Perron (BIC, sin corregir autocorrelación, tiende a sobreestimar el nº de quiebres): beta_València_vs_Provincia: 1 (2018Q2); beta_València_vs_C. Valenciana: 3 (2013Q2;2016Q2;2020Q1); beta_València_vs_España: 2 (2009Q1;2018Q2).
- **Búsqueda**: 28 modelos registrados en `output/registro_busqueda_f6.csv`; corrección Holm/Bonferroni sobre 16 contrastes en `correccion_holm.md`. Con Holm, contrastes con p_Holm<0,05: cuota_ext_dif_CV_ES, beta=1_beta_València_vs_España, dif_nivel_2020-26_València_vs_C. Valenciana, dif_nivel_2020-26_València_vs_España, dif_nivel_2020-26_València_vs_Provincia, beta=1_beta_València_vs_C. Valenciana, wald_betas_iguales_València_vs_Provincia, beta=1_beta_València_vs_Provincia, wald_betas_iguales_València_vs_C. Valenciana, wald_betas_iguales_València_vs_España.

## B. Descriptivo (N insuficiente, N < 40; **sin inferencia**)

- **Padrón** (1998-2022, N=25; DPOP 1996-2025): extranjeros 1,1 % en 1998, máximo 15,1 % en 2009, 14,4 % en 2022 (`padron_valencia_nacionalidad.md`).
- **Alquiler SERPAVI València** (2011-2024, N=14): mediana 5,15 a 8,18 €/m²/mes; índice 2015=100 a 2024: València 175, CV 157, valor tasado València 189. Rentabilidad bruta aproximada València: 3,7 % (2011), **pico 5,2 % en 2017**, 5,0 % (2020) y 4,5 % (2024): caída desde 2020 porque el valor tasado sube más que la renta SERPAVI. Advertencias: mezcla fuentes y conceptos; SERPAVI es stock de contratos vigentes (retrasa la renta de mercado); la superficie de SERPAVI y la de la tasación pueden no coincidir (no verificado).
- **VUT GVA** (registradas, 2010-2024, N=15 años): València 569 a 6090; por 1.000 hab. 7,4 frente a 19,0 en la CV (2024). VUT INE: N=13 cortes irregulares, no comparable en niveles con GVA.
- **SERPAVI por distrito** (19 distritos, N=14 años): mayor mediana 2024 4625001 (10,90 €/m²), menor 4625017 (5,87); crecimiento 2015-2024 entre 51 % y 86 %; coeficiente de variación 0,110 (2011) a 0,157 (2024) (`serpavi_distritos_*.md`; por código).
- **Notariado (robustez)**: municipio 'Total general' 2021-2025 (N=5); provincia trimestral 2018-2025 (N=32), % con comprador extranjero 18,5 % (2018T1), máximo 24,7 % (2023Q3), 18,8 % (2025T4).
- **Correlaciones anuales** (`correlaciones_anuales.md`): solo descripción, sin p-valores.

### Tabla de N por serie
Ver `tabla_N_series.md` (todas las series de `valencia.csv`).

| variable                   | territorio            |   n | inicio   | fin    | uso                | usada_en_estimacion   |
|:---------------------------|:----------------------|----:|:---------|:-------|:-------------------|:----------------------|
| ipv                        | Comunitat Valenciana  |  78 | 2007Q1   | 2026Q2 | elegible (N>=40)   | sí                    |
| ipv                        | España                |  78 | 2007Q1   | 2026Q2 | elegible (N>=40)   | sí                    |
| ipva                       | València (municipio)  |  14 | 2011     | 2024   | descriptivo (N<40) | no                    |
| notariado_cuantia_esp_prov | Provincia de València |  32 | 2018Q1   | 2025Q4 | descriptivo (N<40) | no                    |
| notariado_cuantia_ext_prov | Provincia de València |  32 | 2018Q1   | 2025Q4 | descriptivo (N<40) | no                    |
| notariado_viv_esp_prov     | Provincia de València |  32 | 2018Q1   | 2025Q4 | descriptivo (N<40) | no                    |
| notariado_viv_ext_prov     | Provincia de València |  32 | 2018Q1   | 2025Q4 | descriptivo (N<40) | no                    |
| notariado_viv_extranj      | València (municipio)  |   5 | 2021     | 2025   | descriptivo (N<40) | no                    |
| p_tasado                   | Comunitat Valenciana  | 126 | 1995Q1   | 2026Q2 | elegible (N>=40)   | sí                    |
| p_tasado                   | España                | 126 | 1995Q1   | 2026Q2 | elegible (N>=40)   | sí                    |
| p_tasado                   | Provincia de València | 126 | 1995Q1   | 2026Q2 | elegible (N>=40)   | sí                    |
| p_tasado                   | València (municipio)  |  86 | 2005Q1   | 2026Q2 | elegible (N>=40)   | sí                    |
| pob_espanola               | València (municipio)  |  25 | 1998     | 2022   | descriptivo (N<40) | no                    |
| pob_extranjera             | València (municipio)  |  25 | 1998     | 2022   | descriptivo (N<40) | no                    |
| pob_extranjera_gva         | València (municipio)  |  18 | 2005     | 2022   | descriptivo (N<40) | no                    |
| pob_total                  | València (municipio)  |  29 | 1996     | 2025   | descriptivo (N<40) | no                    |
| pob_vlc_africa             | València (municipio)  |  25 | 1998     | 2022   | descriptivo (N<40) | no                    |
| pob_vlc_alemania           | València (municipio)  |  25 | 1998     | 2022   | descriptivo (N<40) | no                    |
| pob_vlc_america            | València (municipio)  |  25 | 1998     | 2022   | descriptivo (N<40) | no                    |
| pob_vlc_asia               | València (municipio)  |  25 | 1998     | 2022   | descriptivo (N<40) | no                    |
| pob_vlc_europa             | València (municipio)  |  25 | 1998     | 2022   | descriptivo (N<40) | no                    |
| pob_vlc_reino_unido        | València (municipio)  |  25 | 1998     | 2022   | descriptivo (N<40) | no                    |
| serpavi_vc_dist_agg        | València (municipio)  |  14 | 2011     | 2024   | descriptivo (N<40) | no                    |
| serpavi_vc_mediana         | València (municipio)  |  14 | 2011     | 2024   | descriptivo (N<40) | no                    |
| trans_extranjeros          | Comunitat Valenciana  |  78 | 2007Q1   | 2026Q2 | elegible (N>=40)   | sí                    |
| trans_extranjeros          | España                |  78 | 2007Q1   | 2026Q2 | elegible (N>=40)   | sí                    |
| trans_total                | Comunitat Valenciana  |  89 | 2004Q1   | 2026Q1 | elegible (N>=40)   | sí                    |
| trans_total                | España                |  89 | 2004Q1   | 2026Q1 | elegible (N>=40)   | sí                    |
| trans_total                | València (municipio)  |  89 | 2004Q1   | 2026Q1 | elegible (N>=40)   | sí                    |
| vut_pct_sobre_total        | Provincia de València |  13 | 2020Q3   | 2026Q2 | descriptivo (N<40) | no                    |
| vut_pct_sobre_total        | València (municipio)  |  13 | 2020Q3   | 2026Q2 | descriptivo (N<40) | no                    |
| vut_plazas                 | Provincia de València |  13 | 2020Q3   | 2026Q2 | descriptivo (N<40) | no                    |
| vut_plazas                 | València (municipio)  |  13 | 2020Q3   | 2026Q2 | descriptivo (N<40) | no                    |
| vut_plazas_por_vivienda    | Provincia de València |  13 | 2020Q3   | 2026Q2 | descriptivo (N<40) | no                    |
| vut_plazas_por_vivienda    | València (municipio)  |  13 | 2020Q3   | 2026Q2 | descriptivo (N<40) | no                    |
| vut_stock_gva              | Comunitat Valenciana  |  60 | 2010Q1   | 2024Q4 | elegible (N>=40)   | no                    |
| vut_stock_gva              | Provincia de València |  60 | 2010Q1   | 2024Q4 | elegible (N>=40)   | no                    |
| vut_stock_gva              | València (municipio)  |  60 | 2010Q1   | 2024Q4 | elegible (N>=40)   | no                    |
| vut_viviendas_turisticas   | Provincia de València |  13 | 2020Q3   | 2026Q2 | descriptivo (N<40) | no                    |
| vut_viviendas_turisticas   | València (municipio)  |  13 | 2020Q3   | 2026Q2 | descriptivo (N<40) | no                    |

## Problemas abiertos
- Distritos SERPAVI: el origen no trae nombres, solo código 4625NNN; mediana por distrito ruidosa (mín. 10 viviendas).
- Trans_extranjeros no existe para València municipio en MIVAU.
- El valor tasado municipal es de tasaciones (composición cambiante de inmuebles tasados); el padrón por nacionalidad acaba en 2022 (no hay 2023-2025 por municipio).
- Δ4 solapa: EE HAC(4) en la beta completa, HAC(8) en tramos y quiebres; el EE del diferencial medio crece con los retardos.
- Contradicción documental pendiente: `fuentes_fallidas.md` dice que la nacionalidad 2023-2025 no está publicada a nivel municipal, mientras `docs/fallidas/ine_ccaa.md` anota que la tabla 79544 es municipal desde 2021 (no se ha resuelto aquí).
- `rmse_oos` del registro en las betas es condicional al x contemporáneo (no es pronóstico).
- La VUT GVA es un registro con quiebres regulatorios; la serie 2026 no se encadena.

## Qué NO se puede afirmar
- Que las viviendas turísticas o la inmigración/compradores extranjeros **causen** variaciones del precio o del alquiler en València: solo hay N<40 anual, sin instrumento ni variación cruzada municipal.
- Que la rentabilidad bruta aproximada sea la rentabilidad real de un inversor (mezcla fuentes).
- Que las correlaciones anuales sean relaciones estables; que los niveles INE y GVA de VUT sean comparables.
- Que la cuota de extranjeros de la CV (MIVAU) sea la de València ciudad, ni que el Notariado municipal sea comparable en niveles con MIVAU.

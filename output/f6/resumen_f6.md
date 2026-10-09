# Resumen F6: València (precios, alquiler, población extranjera, VUT)

Todo lo que sigue es **asociación** o descripción; no hay identificación causal en esta fase. Reproducible con `python3 src/f6_valencia.py`.

## A. Estimación (N >= 40 trimestres; HAC Newey-West, maxlags=4)

Muestra común precios: 2005Q1-2026Q2 (N=86 niveles; N=82 en Δ4). Compraventas: 2007Q1-2026Q1 (N=77).

- **Índices 2015=100 y crecimiento acumulado (%) del valor tasado** (`crecimiento_acumulado_p_tasado.md`):
  2008-2013: València -44.6, provincia -32.0, CV -32.2, España -29.7;
  2014-2019: València 14.6, provincia 11.5, CV 9.2, España 12.7;
  2020-2026Q2: València 100.0, provincia 65.5, CV 57.1, España 42.5.
- **Diferencial medio de crecimiento interanual** (València menos comparador, pp, 100·Δ4 ln): vs Provincia: 0,62 pp (IC95 % -1,36 a 2,59; EE HAC 1,01; p=0,541); vs C. Valenciana: 1,17 pp (IC95 % -1,08 a 3,43; EE HAC 1,15; p=0,308); vs España: 1,18 pp (IC95 % -1,37 a 3,74; EE HAC 1,30; p=0,364).
- **Beta de Δ4 ln p_tasado València sobre España** (y otros comparadores): vs Provincia: β=1,39 (EE HAC 0,09; p(β=1)=0,000); vs C. Valenciana: β=1,51 (EE HAC 0,10; p(β=1)=0,000); vs España: β=1,73 (EE HAC 0,11; p(β=1)=0,000). Con maxlags=6 los EE cambian poco (ver `beta_valencia_vs_comparadores.md`).
- **Compraventas MIVAU**: cuota de extranjeros CV (media 12,2 %) frente a España (8,2 %); diferencia media CV-España 3,93 pp (EE HAC 0,33; p=0,000). Tendencia lineal (descriptiva): CV 0,54 pp/año (EE 0,07), España 0,34 pp/año (EE 0,05). La serie MIVAU de extranjeros **no existe a nivel de municipio**: no hay cuota de extranjeros de València en la parte estimada.
- **Diagnósticos que fallan (p<0,05)** en los modelos beta: beta_València_vs_Provincia:BG4_p=0.000, beta_València_vs_Provincia:RESET_p=0.000, beta_València_vs_Provincia:CUSUM_p=0.015, beta_València_vs_C. Valenciana:BG4_p=0.000, beta_València_vs_C. Valenciana:RESET_p=0.001, beta_València_vs_C. Valenciana:CUSUM_p=0.043, beta_València_vs_España:BG4_p=0.000, beta_València_vs_España:RESET_p=0.022, beta_València_vs_España:CUSUM_p=0.001. Chow significativos: beta_València_vs_Provincia@2020Q1(p=0.044), beta_València_vs_C. Valenciana@2020Q1(p=0.009), beta_València_vs_C. Valenciana@2022Q3(p=0.045), beta_València_vs_España@2020Q1(p=0.010). Quiebres Bai-Perron: beta_València_vs_Provincia: 1 (2018Q2); beta_València_vs_C. Valenciana: 3 (2013Q2;2016Q2;2020Q1); beta_València_vs_España: 2 (2009Q1;2018Q2). Ver `diagnosticos_beta.md`, `chow_beta.md`, `bai_perron_beta.md`.
- **Búsqueda**: 14 modelos registrados en `output/registro_busqueda_f6.csv`; corrección Holm/Bonferroni sobre 11 contrastes en `correccion_holm.md`. Con Holm, contrastes con p_Holm<0,05: cuota_ext_dif_CV_ES, tendencia_cuota_CV, tendencia_cuota_ES, beta=1_beta_València_vs_España, beta=1_beta_València_vs_C. Valenciana, beta=1_beta_València_vs_Provincia.

## B. Descriptivo (N insuficiente, N < 40; **sin inferencia**)

- **Padrón** (1998-2022, N=25; DPOP 1996-2025): extranjeros 1,1 % en 1998, máximo 15,1 % en 2009, 14,4 % en 2022 (`padron_valencia_nacionalidad.md`).
- **Alquiler SERPAVI València** (2011-2024, N=14): mediana 5,15 a 8,18 €/m²/mes; índice 2015=100 a 2024: València 175, CV 157, valor tasado València 189. Rentabilidad bruta aproximada València 3,7 % (2011) a 4,5 % (2024); mezcla fuentes y conceptos.
- **VUT GVA** (registradas, 2010-2024, N=15 años): València 569 a 6090; por 1.000 hab. 7,4 frente a 19,0 en la CV (2024). VUT INE: N=13 cortes irregulares, no comparable en niveles con GVA.
- **SERPAVI por distrito** (19 distritos, N=14 años): mayor mediana 2024 4625001 (10,90 €/m²), menor 4625017 (5,87); crecimiento 2015-2024 entre 51 % y 86 %; coeficiente de variación 0,110 (2011) a 0,157 (2024) (`serpavi_distritos_*.md`; por código).
- **Notariado (robustez)**: municipio 'Total general' 2021-2025 (N=5); provincia trimestral 2018-2025 (N=32), % con comprador extranjero 18,5 % (2018T1) a 18,8 % (2025T4).
- **Correlaciones anuales** (`correlaciones_anuales.md`): solo descripción, sin p-valores.

### Tabla de N por serie
Ver `tabla_N_series.md` (todas las series de `valencia.csv`).

| variable                   | territorio            |   n | inicio   | fin    | uso                |
|:---------------------------|:----------------------|----:|:---------|:-------|:-------------------|
| ipv                        | Comunitat Valenciana  |  78 | 2007Q1   | 2026Q2 | estimación (N>=40) |
| ipv                        | España                |  78 | 2007Q1   | 2026Q2 | estimación (N>=40) |
| ipva                       | València (municipio)  |  14 | 2011     | 2024   | descriptivo (N<40) |
| notariado_cuantia_esp_prov | Provincia de València |  32 | 2018Q1   | 2025Q4 | descriptivo (N<40) |
| notariado_cuantia_ext_prov | Provincia de València |  32 | 2018Q1   | 2025Q4 | descriptivo (N<40) |
| notariado_viv_esp_prov     | Provincia de València |  32 | 2018Q1   | 2025Q4 | descriptivo (N<40) |
| notariado_viv_ext_prov     | Provincia de València |  32 | 2018Q1   | 2025Q4 | descriptivo (N<40) |
| notariado_viv_extranj      | València (municipio)  |   5 | 2021     | 2025   | descriptivo (N<40) |
| p_tasado                   | Comunitat Valenciana  | 126 | 1995Q1   | 2026Q2 | estimación (N>=40) |
| p_tasado                   | España                | 126 | 1995Q1   | 2026Q2 | estimación (N>=40) |
| p_tasado                   | Provincia de València | 126 | 1995Q1   | 2026Q2 | estimación (N>=40) |
| p_tasado                   | València (municipio)  |  86 | 2005Q1   | 2026Q2 | estimación (N>=40) |
| pob_espanola               | València (municipio)  |  25 | 1998     | 2022   | descriptivo (N<40) |
| pob_extranjera             | València (municipio)  |  25 | 1998     | 2022   | descriptivo (N<40) |
| pob_extranjera_gva         | València (municipio)  |  18 | 2005     | 2022   | descriptivo (N<40) |
| pob_total                  | València (municipio)  |  29 | 1996     | 2025   | descriptivo (N<40) |
| pob_vlc_africa             | València (municipio)  |  25 | 1998     | 2022   | descriptivo (N<40) |
| pob_vlc_alemania           | València (municipio)  |  25 | 1998     | 2022   | descriptivo (N<40) |
| pob_vlc_america            | València (municipio)  |  25 | 1998     | 2022   | descriptivo (N<40) |
| pob_vlc_asia               | València (municipio)  |  25 | 1998     | 2022   | descriptivo (N<40) |
| pob_vlc_europa             | València (municipio)  |  25 | 1998     | 2022   | descriptivo (N<40) |
| pob_vlc_reino_unido        | València (municipio)  |  25 | 1998     | 2022   | descriptivo (N<40) |
| serpavi_vc_dist_agg        | València (municipio)  |  14 | 2011     | 2024   | descriptivo (N<40) |
| serpavi_vc_mediana         | València (municipio)  |  14 | 2011     | 2024   | descriptivo (N<40) |
| trans_extranjeros          | Comunitat Valenciana  |  78 | 2007Q1   | 2026Q2 | estimación (N>=40) |
| trans_extranjeros          | España                |  78 | 2007Q1   | 2026Q2 | estimación (N>=40) |
| trans_total                | Comunitat Valenciana  |  89 | 2004Q1   | 2026Q1 | estimación (N>=40) |
| trans_total                | España                |  89 | 2004Q1   | 2026Q1 | estimación (N>=40) |
| trans_total                | València (municipio)  |  89 | 2004Q1   | 2026Q1 | estimación (N>=40) |
| vut_pct_sobre_total        | Provincia de València |  13 | 2020Q3   | 2026Q2 | descriptivo (N<40) |
| vut_pct_sobre_total        | València (municipio)  |  13 | 2020Q3   | 2026Q2 | descriptivo (N<40) |
| vut_plazas                 | Provincia de València |  13 | 2020Q3   | 2026Q2 | descriptivo (N<40) |
| vut_plazas                 | València (municipio)  |  13 | 2020Q3   | 2026Q2 | descriptivo (N<40) |
| vut_plazas_por_vivienda    | Provincia de València |  13 | 2020Q3   | 2026Q2 | descriptivo (N<40) |
| vut_plazas_por_vivienda    | València (municipio)  |  13 | 2020Q3   | 2026Q2 | descriptivo (N<40) |
| vut_stock_gva              | Comunitat Valenciana  |  60 | 2010Q1   | 2024Q4 | estimación (N>=40) |
| vut_stock_gva              | Provincia de València |  60 | 2010Q1   | 2024Q4 | estimación (N>=40) |
| vut_stock_gva              | València (municipio)  |  60 | 2010Q1   | 2024Q4 | estimación (N>=40) |
| vut_viviendas_turisticas   | Provincia de València |  13 | 2020Q3   | 2026Q2 | descriptivo (N<40) |
| vut_viviendas_turisticas   | València (municipio)  |  13 | 2020Q3   | 2026Q2 | descriptivo (N<40) |

## Problemas abiertos
- Distritos SERPAVI: el origen no trae nombres, solo código 4625NNN; mediana por distrito ruidosa (mín. 10 viviendas).
- Trans_extranjeros no existe para València municipio en MIVAU.
- El valor tasado municipal es de tasaciones (composición cambiante de inmuebles tasados); el padrón por nacionalidad acaba en 2022 (no hay 2023-2025 por municipio).
- Δ4 solapa: los EE HAC(4) pueden quedarse cortos con N=82; se reporta HAC(6) como robustez.
- La VUT GVA es un registro con quiebres regulatorios; la serie 2026 no se encadena.

## Qué NO se puede afirmar
- Que las viviendas turísticas o la inmigración/compradores extranjeros **causen** variaciones del precio o del alquiler en València: solo hay N<40 anual, sin instrumento ni variación cruzada municipal.
- Que la rentabilidad bruta aproximada sea la rentabilidad real de un inversor (mezcla fuentes).
- Que las correlaciones anuales sean relaciones estables; que los niveles INE y GVA de VUT sean comparables.
- Que la cuota de extranjeros de la CV (MIVAU) sea la de València ciudad, ni que el Notariado municipal sea comparable en niveles con MIVAU.

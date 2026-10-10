# Accesos a la muestra sellada (copia versionada de data/sealed/_accesos.log)

| UTC | hipótesis | rama | paneles | evento / resultado |
|---|---|---|---|---|
| 2026-10-10T07:45:45Z | H1 | BA | panel_prov_q, nacional_q_v2 | APERTURA (antes de leer) |
| 2026-10-10T07:46:11Z | H1 | BA | panel_prov_q, nacional_q_v2 | {"n_omitidos_ecm": 0, "tmax": "2026Q2", "selladas": ["11", "16", "45"], "todas": {"modelo": "B_AR4_mas_H1", "n": 416.0, "n_periodos": 8.0, "rmse": 0.010785174515890483, "mae": 0.007736431202886496, "rmse_AR4": 0.012244975322719311, "dm_vs_AR4": 3.984829084760093, "p_vs_AR4": 0.005291203548195239, "r |
| 2026-10-10T07:53:07Z | H2 | BV | panel_prov_q, nacional_q_v2 | APERTURA (antes de leer) |
| 2026-10-10T07:53:11Z | H2 | BV | panel_prov_q, nacional_q_v2 | {"cfg": "C3", "regla": "RMSE_modelo < RMSE_AR4 y p < 0,05 (principal: todas las provincias)", "provincias_entrenamiento": 49, "provincias_selladas": ["11", "16", "45"], "PRINCIPAL_todas": {"modelo": "BV_C3", "n": 416, "n_periodos": 8, "rmse": 0.054645142613630605, "mae": 0.0464239490576576, "rmse_AR |
| 2026-10-10T09:23:21Z | H6 | BP | panel_prov_q | APERTURA (antes de leer) |
| 2026-10-10T09:24:16Z | H6 | BP | panel_prov_q | {"regla": "H6 se confirma si tau_SDiD(ln IPC alquiler) < 0 y p de permutación bilateral < 0,05", "tratadas": ["08", "17", "25", "43"], "n_donantes": 40, "donantes": ["02", "03", "04", "05", "06", "07", "09", "10", "12", "13", "14", "18", "19", "21", "22", "23", "24", "26", "27", "28", "29", "30", "3 |
| 2026-10-10T09:56:04Z | H7 | BM | panel_prov_q, nacional_q_v2 | APERTURA (antes de leer) |
| 2026-10-10T09:56:19Z | H7 | BM | panel_prov_q, nacional_q_v2 | {"L": "2024Q2", "fin": "2026Q2", "selladas": ["11", "16", "45"], "seleccion": {"A": "TVPVAR_k0.95", "B": "LGBM_nl4_n400", "C": "EN_l10.7_a0.4"}, "continuidad_max_dln_L_L1": 0.02768867229000005, "umbral_continuidad": 0.05, "secundarios_errores": {}, "regla": "objetivo cumple: RMSE<AR4 y <ECM v1, DM>0 |
| 2026-10-10T13:42:50Z | H3-3a | C3 | v3_c3_serpavi | APERTURA (antes de leer) |
| 2026-10-10T13:42:50Z | H3-3a | C3 | v3_c3_serpavi | {"hipotesis": "H3-3a", "resultado": "alq", "diseno": "DiD anual; Δ = media(2021-2022) - media(2018-2019); 2020 excluido", "beta": -0.007727674478050062, "se": 0.00318369914597447, "ic95": [-0.014008039007080106, -0.0014473099490200179], "p_dos_colas": 0.01615610463556489, "p_una_cola_neg": 0.0080780 |
| 2026-10-10T13:42:50Z | H3-3b | C3 | v3_c3_serpavi | APERTURA (antes de leer) |
| 2026-10-10T13:42:50Z | H3-3b | C3 | v3_c3_serpavi | {"hipotesis": "H3-3b", "resultado": "n_viv", "diseno": "DiD anual; Δ = media(2021-2022) - media(2018-2019); 2020 excluido", "beta": -0.0445597579218958, "se": 0.01079748760655884, "ic95": [-0.06585955889480388, -0.02325995694898772], "p_dos_colas": 5.5210740454896164e-05, "p_una_cola_neg": 2.7605370 |
| 2026-10-10T13:47:05Z | H3-1 | C1 | v3_c1_panel | APERTURA (antes de leer) |
| 2026-10-10T13:47:05Z | H3-1 | C1 | v3_c1_panel | {"nacional": {"b": 0.0010474035592148, "se": 0.0008780230560884313, "lo": -0.0006763362483441712, "hi": 0.0027711433667737713, "p": 0.23329013286895764, "F": null, "sd_x": 0.3817129398784633, "n": 20448, "G": 734}, "6_ciudades": {"b": -0.001297579114469623, "se": 0.000986796758909202, "lo": -0.00335 |
| 2026-10-10T13:47:09Z | H3-2 | C1 | v3_c1_panel | APERTURA (antes de leer) |
| 2026-10-10T13:47:09Z | H3-2 | C1 | v3_c1_panel | {"6_ciudades": {"b": 0.0041955308468032155, "se": 0.006119725148820581, "lo": -0.008569992120950167, "hi": 0.0169610538145566, "p": 0.5008513023066891, "F": 60.50577269033476, "sd_x": 0.37381155099743085, "n": 5280, "G": 21, "wcb_p": 0.503, "wcb_crit": 1.992755195662847}, "5_ciudades": {"b": 0.00478 |

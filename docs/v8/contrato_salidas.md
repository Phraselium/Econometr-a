# Contrato de salidas de F4 (obligatorio para todos los módulos M0-M9)

Cada módulo Mx escribe en output/v8/Mx/ y su script en src/v8/mx_*.py. Todo es determinista (SEED = 20261010, un hilo). Toda especificación probada se registra en el Registry (src/econ_utils.py) en output/v8/Mx/registro.csv. Cruces solo por código INE.

## Nombres comunes

- **mercado:** `compra` | `alquiler`.
- **ambito:** `nacional` | `ccaa:<cod>` | `ccaa_panel` | `cv_prov:<cod>` | `cv_panel` | `valencia_ciudad`.
- **periodo:** `P1` | `P2` | `P3` | `P4` | `P5` | `completo` | `<regimen>` (los regímenes detectados se describen en notas).
- **factor:** `demografia` | `empleo_renta` | `credito_tipos` | `oferta` | `demanda_externa` | `turismo` | `factor_europeo` | `residuo`.
- **capa:** `C1` | `C2` | `C3` | `C3s` | `C4`.

## coeficientes.csv (modelos con coeficientes)

Columnas, en este orden:

| Grupo | Columnas |
|---|---|
| Identificación del modelo | modelo_id, modulo, familia_modelo, mercado, ambito, periodo, dependiente, transformacion, medida_precio |
| Coeficiente | variable, beta, ee, tipo_ee, t, p, p_ajustado, metodo_ajuste (Holm\|BH), ic95_lo, ic95_hi, beta_std, elasticidad |
| Ajuste | n, r2, r2_adj, aic, bic |
| Dinámica | vel_ajuste, semivida |
| Diagnósticos | coint_p, bg_p, bp_p, jb_p, reset_p, cusum_estable, vif_max |
| Instrumentos | f1_etapa, ar_lo, ar_hi |
| Evaluación | capa, n_multiverso, pct_mismo_signo, pct_sig_bh, cumple_regla_m0, cumple_multiverso, destacado, motivo_destacado |
| Trazabilidad | script |

Si una columna no aplica, queda vacía.

## atribucion.csv (contribuciones por factor)

metodo (`svar_hd` | `dominancia` | `lpiv` | `contabilidad` | `shap` | ...), mercado, ambito, periodo, factor, contribucion_pp (puntos log ×100 de la variación acumulada del periodo), pct_total, b68_lo, b68_hi, b90_lo, b90_hi, capa, notas.

## Salidas del SVAR (M2) y de los regímenes (M3)

- **irf.csv:** variante, shock, variable, h, mediana, b68_lo, b68_hi, b90_lo, b90_hi.
- **fevd.csv:** variante, variable, h, shock, mediana, b68_lo, b68_hi.
- **hd_periodos.csv:** variante, mercado, periodo, factor (shock), contribucion_pp, pct_total, b68_lo, b68_hi, b90_lo, b90_hi, prob_pos.
- **M3: coef_periodo.csv:** variable_origen, variable_destino, periodo, mediana, b68_lo, b68_hi, b90_lo, b90_hi.

## resultado.json

Formato del proyecto: {rama, pregunta, capa, datos, N, metodo, estimacion, ic95, p_ajustado, nivel_evidencia, diagnosticos, fuera_muestra{modelo, rmse, dm_vs_ar4}, notas}.

## Reglas

- Nunca se elige un modelo por su p.
- Se reportan todos los resultados, sean o no significativos.
- No hay lenguaje causal por debajo de C3/C3s.
- Si un dato, una herramienta o una identificación falla, se marca con su motivo y se sigue.

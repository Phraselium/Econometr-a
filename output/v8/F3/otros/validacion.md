# Validación Monte Carlo — herramientas V8-F3 grupo B (no VAR), versión corregida tras la revisión F3

Solo datos simulados; SEED=20261010; un hilo por proceso; determinista. Bloques en procesos paralelos (4 núcleos): bp_pot 1068 s, bp_size 1080 s, dfm 12 s, dom 26 s, lp 462 s, lpiv 316 s, lpiv_inf 65 s, ms12 1536 s, ms23 936 s, msbic 600 s, perm 30 s, perm_multi 414 s, shap 45 s, umbral 205 s. Detalle por fila en `montecarlo.csv`; etiquetas en `etiquetas.csv`.

## Reglas de etiquetado (derivadas en el código, `REGLAS`)

Las reglas de «con reservas» las fijó el ejecutor tras ver las cifras de la primera pasada de F3 (no están pre-registradas). Una configuración (herramienta + remuestreo/EE) recibe dos etiquetas sobre sus filas PRINCIPALES (uso previsto: T ≈ 90-126; las filas de referencia, con n=200-300 o fuera del dominio de la configuración, se muestran pero no etiquetan):

| Tipo de cifra | apta | con reservas |
|---|---|---|
| tamano | [0,02; 0,10] | <= 0,15 |
| cobertura | [0,90; 0,98] | [0,80; 0,99] |
| potencia | >= 0,80 | >= 0,50 |
| acierto | >= umbral de la fila | >= 0,50 |
| error | < umbral de la fila | < 1,5 x umbral de la fila |

Validez = tamaño, cobertura, acierto y error; potencia aparte. «apta» si todas las filas cumplen; «con reservas» si todas están en la banda laxa; «no apta» en otro caso.

## Etiquetas por configuración

| Herramienta | Configuración | Validez | Potencia | Rango tamaño | Rango cobertura | Rango potencia | Filas que no cumplen (cifras) |
|---|---|---|---|---|---|---|---|
| bai_perron | bloque_8 | **no apta** | **apta** | 0,020-0,412 |  | 0,932-1,000 | H0 n=100 / errores AR(0.85): tamaño UDmax (5%) = 0,336; H0 n=126 / errores AR(0.85): tamaño UDmax (5%) = 0,412 |
| bai_perron | sieve | **apta** | **no apta** | 0,024-0,064 |  | 0,316-0,984 | H1 salto 2.0σ (σ marginal) n=100 / errores AR(0.85): potencia UDmax (5%) = 0,316; H1 salto 2.0σ (σ marginal) n=126 / errores AR(0.85): potencia UDmax (5%) = 0,420 |
| bai_perron | wild | **con reservas** | **sin datos** | 0,012-0,068 |  |  | H0 n=100 / errores AR(0): tamaño UDmax (5%) = 0,012 |
| bai_perron | bloque_pw | **no apta** | **sin datos** | 0,012-0,196 |  |  | H0 n=100 / errores AR(0): tamaño UDmax (5%) = 0,012; H0 n=100 / errores AR(0.5): tamaño UDmax (5%) = 0,156; H0 n=100 / errores AR(0.85): tamaño UDmax (5%) = 0,196 |
| dfm_baing | IC_p2 | **con reservas** | **sin datos** |  |  |  | T=110,N=17,r=2: % IC_p2 elige r verdadero = 0,875 |
| dfm_pca | PCA_r1 | **apta** | **sin datos** |  |  |  | todas las filas principales cumplen |
| dfm_ml | ML_r1 | **apta** | **sin datos** |  |  |  | todas las filas principales cumplen |
| dominancia | filas | **con reservas** | **sin datos** |  | 0,937-0,937 |  | p=5 colineal, n=100, regresores AR(0.0), errores AR(0.0): % acierto en las 2 variables dominantes (orden) = 0,667; p=5 colineal, n=100, regresores AR(0.0), errores AR(0.0): error relativo máx del VIF = 0,216 |
| dominancia | bloque_8 | **no apta** | **sin datos** |  | 0,857-0,893 |  | p=5 colineal, n=100, regresores AR(0.8), errores AR(0.5): error absoluto medio de phi (R2) = 0,038; p=5 colineal, n=100, regresores AR(0.8), errores AR(0.5): cobertura IC95 bootstrap de phi = 0,857; p=5 colineal, n=100, regresores AR(0.8), errores AR(0.5): % acierto en las 2 variables dominantes (orden) = 0,367; p=5 colineal, n=100, regresores AR(0.8), errores AR(0.5): error relativo máx del VIF = 0,654; p=5 colineal, n=126, regresores AR(0.8), errores AR(0.5): error absoluto medio de phi (R2) = 0,033; (+3 filas más, ver montecarlo.csv; 8 de 8 filas principales no cumplen) |
| lp_ols | NW_h+1 | **no apta** | **sin datos** |  | 0,782-0,943 |  | ρ=0.6, n=90, h=4: cobertura IC95 = 0,897; ρ=0.6, n=90, h=4-8: cobertura IC95 = 0,877; ρ=0.9, n=90, h=4: cobertura IC95 = 0,850; ρ=0.9, n=90, h=8: cobertura IC95 = 0,845; ρ=0.9, n=90, h=12: cobertura IC95 = 0,823; (+7 filas más, ver montecarlo.csv; 12 de 28 filas principales no cumplen) |
| lp_ols | NW_2h+2 | **no apta** | **sin datos** |  | 0,735-0,932 |  | ρ=0.6, n=90, h=4: cobertura IC95 = 0,873; ρ=0.6, n=90, h=8: cobertura IC95 = 0,868; ρ=0.6, n=90, h=12: cobertura IC95 = 0,843; ρ=0.6, n=90, h=-4 (pretendencia: efecto verdadero 0): cobertura IC95 = 0,890; ρ=0.6, n=90, h=4-8: cobertura IC95 = 0,825; (+11 filas más, ver montecarlo.csv; 16 de 28 filas principales no cumplen) |
| lp_ols | EWC | **con reservas** | **sin datos** |  | 0,838-0,948 |  | ρ=0.9, n=90, h=4: cobertura IC95 = 0,887; ρ=0.9, n=90, h=8: cobertura IC95 = 0,882; ρ=0.9, n=90, h=4-8: cobertura IC95 = 0,838; ρ=0.9, n=110, h=8: cobertura IC95 = 0,880; ρ=0.9, n=110, h=12: cobertura IC95 = 0,880; (+1 filas más, ver montecarlo.csv; 6 de 28 filas principales no cumplen) |
| lp_iv | AR | **no apta** | **sin datos** |  | 0,913-1,000 |  | instrumento_fuerte, n=90, h=12: cobertura IC Anderson-Rubin = 0,990; instrumento_debil, n=90, h=4: cobertura IC Anderson-Rubin = 0,997; instrumento_debil, n=90, h=8: cobertura IC Anderson-Rubin = 0,990; instrumento_debil, n=90, h=12: cobertura IC Anderson-Rubin = 1,000; instrumento_debil, n=90, h=4-8: cobertura IC Anderson-Rubin = 0,997; (+14 filas más, ver montecarlo.csv; 19 de 30 filas principales no cumplen) |
| lp_iv | IC_normal | **con reservas** | **sin datos** |  | 0,850-0,953 |  | instrumento_fuerte, n=90, h=4: cobertura IC normal 2SLS = 0,863; instrumento_fuerte, n=90, h=4-8: cobertura IC normal 2SLS = 0,850; instrumento_fuerte, n=110, h=4: cobertura IC normal 2SLS = 0,863; instrumento_fuerte, n=110, h=12: cobertura IC normal 2SLS = 0,897; instrumento_fuerte, n=110, h=4-8: cobertura IC normal 2SLS = 0,887 |
| lp_iv | AR_unilateral | **apta** | **con reservas** | 0,057-0,060 |  | 0,673-0,853 | efecto -1, IV fuerte, n=110, agregado 4-8: potencia AR unilateral (H1: β<0) al 5% = 0,673 |
| lp_iv | pretendencias | **apta** | **apta** | 0,040-0,040 |  | 0,993-0,993 | todas las filas principales cumplen |
| lp_iv | placebo_permutacion | **apta** | **no apta** | 0,063-0,090 |  | 0,213-0,353 | efecto 1, IV fuerte, n=110, h=4 (permutación libre): potencia (p_perm < 0,05) = 0,353; efecto 1, IV fuerte, n=110, agregado 4-8 (desplazamiento circular): potencia (p_perm < 0,05) = 0,213 |
| markov_switching | bootstrap_LR_1v2 | **con reservas** | **no apta** | 0,000-0,000 |  | 0,400-0,400 | H0_1reg (T=110): tamaño del bootstrap LR 1 vs 2 (5%) = 0,000; H1_2reg (T=110): potencia del bootstrap LR 1 vs 2 (5%) = 0,400 |
| markov_switching | BIC | **no apta** | **sin datos** |  |  |  | verdadero_2reg (T=110): % BIC elige k verdadero = 0,567; verdadero_3reg (T=110): % BIC elige k verdadero = 0,367 |
| permutacion_fechas | t_studentizado_2tramos | **apta** | **no apta** | 0,036-0,048 |  | 0,316-0,316 | H1_ruptura_pendiente (n=100): potencia (5%) = 0,316 |
| permutacion_fechas | dif_sin_studentizar_2tramos | **apta** | **no apta** | 0,024-0,036 |  | 0,244-0,244 | H1_ruptura_pendiente (n=100): potencia (5%) = 0,244 |
| permutacion_fechas | Q_homo_5tramos | **con reservas** | **no apta** | 0,015-0,025 |  | 0,240-0,315 | H0 pendiente constante, 5 tramos no contiguos, n=126, min 8, AR(0.8): tamaño (5%) = 0,015; H1 pendientes (0,3; 0,3; 1,2; 1,2; 0,3), 5 tramos no contiguos, n=126, min 8, AR(0.0): potencia (5%) = 0,315; H1 pendientes (0,3; 0,3; 1,2; 1,2; 0,3), 5 tramos no contiguos, n=126, min 8, AR(0.8): potencia (5%) = 0,240 |
| permutacion_fechas | maxt_homo_5tramos | **apta** | **no apta** | 0,020-0,025 |  | 0,110-0,135 | H1 pendientes (0,3; 0,3; 1,2; 1,2; 0,3), 5 tramos no contiguos, n=126, min 8, AR(0.0): potencia (5%) = 0,135; H1 pendientes (0,3; 0,3; 1,2; 1,2; 0,3), 5 tramos no contiguos, n=126, min 8, AR(0.8): potencia (5%) = 0,110 |
| permutacion_fechas | Q_hac_5tramos | **con reservas** | **no apta** | 0,000-0,015 |  | 0,075-0,080 | H0 pendiente constante, 5 tramos no contiguos, n=126, min 8, AR(0.0): tamaño (5%) = 0,015; H0 pendiente constante, 5 tramos no contiguos, n=126, min 8, AR(0.8): tamaño (5%) = 0,000; H1 pendientes (0,3; 0,3; 1,2; 1,2; 0,3), 5 tramos no contiguos, n=126, min 8, AR(0.0): potencia (5%) = 0,080; H1 pendientes (0,3; 0,3; 1,2; 1,2; 0,3), 5 tramos no contiguos, n=126, min 8, AR(0.8): potencia (5%) = 0,075 |
| umbral_hansen | wild | **apta** | **apta** | 0,040-0,043 |  | 0,890-0,890 | todas las filas principales cumplen |
| umbral_hansen | IC_LR | **apta** | **sin datos** |  | 0,900-0,937 |  | todas las filas principales cumplen |
| umbral_hansen | bloque_pw | **no apta** | **con reservas** | 0,067-0,157 |  | 0,663-0,803 | H0 / errores AR(0.85), q AR(0,9): tamaño (rechazo al 5%) = 0,157; H1 salto 0.8 / errores AR(0.5), q AR(0,9): potencia (rechazo al 5%) = 0,663 |
| umbral_hansen | sieve | **apta** | **con reservas** | 0,033-0,077 |  | 0,587-0,737 | H1 salto 0.8 / errores AR(0.5), q AR(0,9): potencia (rechazo al 5%) = 0,587; H1 salto 0.8 / errores AR(0.5), q AR(0,9): potencia (rechazo al 5%) = 0,737 |
| multiverso | - | no evaluada por MC | - | | | | sin Monte Carlo: verificación determinista por tests unitarios (tests/v8/test_herramientas_otros.py); registra todas las especificaciones, también las fallidas, con tope por defecto de 50.000 |

## Restricciones de uso (cifras generadas desde montecarlo.csv)

- **Bai-Perron (H5).** Tamaño de UDmax con errores AR(0,85): wild 0,992, bloque Politis-White 0,196, bloque fijo 8 0,596, sieve 0,108 (n=100) y 0,104 (n=126). Con AR(0,5): sieve 0,480. Uso: solo `boot='sieve'` con series persistentes; su potencia con salto de 2σ y AR(0,85) es 0,316 (n=100) y 0,420 (n=126): un no rechazo con series muy persistentes NO es evidencia de ausencia de ruptura.
- **Umbral de Hansen (H6).** Con errores AR(0,5) y q AR(0,9), n=100: tamaño wild 0,170, bloque 0,070, sieve 0,033; con AR(0,85): wild 0,510, bloque 0,157, sieve 0,077. Uso: `boot='wild'` solo con errores sin autocorrelación; con errores autocorrelacionados, `boot='sieve'`.
- **LP-OLS (H8).** Ver filas `lp_ols`: la cobertura NW(h+1) cae por debajo de 0,90 en varios horizontes con n=90-110 y ρ=0,9 (mínimo 0,782); EWC (0,838 mínimo) es la menos mala; el ancho de banda mayor NW(2h+2) empeora (0,735). LP-OLS no se usa como evidencia de C3.
- **LP-IV.** El IC Anderson-Rubin cubre entre 0,913 y 1,000; el p unilateral, las pretendencias y el placebo de permutación se resumen en las filas de `lp_iv` (potencia del placebo baja).

## Resultados por prueba

| Herramienta | Config. | Escenario | Métrica | Valor | Objetivo | Cumple | Rol | Réplicas | B | n |
|---|---|---|---|---|---|---|---|---|---|---|
| bai_perron | bloque_8 | H1 salto 1.0σ (σ marginal) n=100 / errores AR(0) | potencia UDmax (5%) | 0,952 | >= 0,80 | sí | referencia | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H1 salto 1.0σ (σ marginal) n=100 / errores AR(0) | error absoluto mediano de la fecha (obs.) | 1,000 | informativo |  | principal | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H1 salto 2.0σ (σ marginal) n=100 / errores AR(0) | potencia UDmax (5%) | 1,000 | >= 0,80 | sí | principal | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H1 salto 2.0σ (σ marginal) n=100 / errores AR(0) | error absoluto mediano de la fecha (obs.) | 0,000 | informativo |  | principal | 250 | 199.0 | 100 |
| bai_perron | sieve | H1 salto 1.0σ (σ marginal) n=100 / errores AR(0) | potencia UDmax (5%) | 0,940 | >= 0,80 | sí | referencia | 250 | 199.0 | 100 |
| bai_perron | sieve | H1 salto 1.0σ (σ marginal) n=100 / errores AR(0) | error absoluto mediano de la fecha (obs.) | 1,000 | informativo |  | principal | 250 | 199.0 | 100 |
| bai_perron | sieve | H1 salto 2.0σ (σ marginal) n=100 / errores AR(0) | potencia UDmax (5%) | 0,940 | >= 0,80 | sí | principal | 250 | 199.0 | 100 |
| bai_perron | sieve | H1 salto 2.0σ (σ marginal) n=100 / errores AR(0) | error absoluto mediano de la fecha (obs.) | 0,000 | informativo |  | principal | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H1 salto 1.0σ (σ marginal) n=100 / errores AR(0.5) | potencia UDmax (5%) | 0,644 | >= 0,80 | NO | referencia | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H1 salto 1.0σ (σ marginal) n=100 / errores AR(0.5) | error absoluto mediano de la fecha (obs.) | 4,000 | informativo |  | principal | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H1 salto 2.0σ (σ marginal) n=100 / errores AR(0.5) | potencia UDmax (5%) | 0,996 | >= 0,80 | sí | principal | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H1 salto 2.0σ (σ marginal) n=100 / errores AR(0.5) | error absoluto mediano de la fecha (obs.) | 0,000 | informativo |  | principal | 250 | 199.0 | 100 |
| bai_perron | sieve | H1 salto 1.0σ (σ marginal) n=100 / errores AR(0.5) | potencia UDmax (5%) | 0,480 | >= 0,80 | NO | referencia | 250 | 199.0 | 100 |
| bai_perron | sieve | H1 salto 1.0σ (σ marginal) n=100 / errores AR(0.5) | error absoluto mediano de la fecha (obs.) | 4,000 | informativo |  | principal | 250 | 199.0 | 100 |
| bai_perron | sieve | H1 salto 2.0σ (σ marginal) n=100 / errores AR(0.5) | potencia UDmax (5%) | 0,892 | >= 0,80 | sí | principal | 250 | 199.0 | 100 |
| bai_perron | sieve | H1 salto 2.0σ (σ marginal) n=100 / errores AR(0.5) | error absoluto mediano de la fecha (obs.) | 0,000 | informativo |  | principal | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H1 salto 1.0σ (σ marginal) n=100 / errores AR(0.85) | potencia UDmax (5%) | 0,596 | >= 0,80 | NO | referencia | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H1 salto 1.0σ (σ marginal) n=100 / errores AR(0.85) | error absoluto mediano de la fecha (obs.) | 11,500 | informativo |  | principal | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H1 salto 2.0σ (σ marginal) n=100 / errores AR(0.85) | potencia UDmax (5%) | 0,932 | >= 0,80 | sí | principal | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H1 salto 2.0σ (σ marginal) n=100 / errores AR(0.85) | error absoluto mediano de la fecha (obs.) | 1,000 | informativo |  | principal | 250 | 199.0 | 100 |
| bai_perron | sieve | H1 salto 1.0σ (σ marginal) n=100 / errores AR(0.85) | potencia UDmax (5%) | 0,108 | >= 0,80 | NO | referencia | 250 | 199.0 | 100 |
| bai_perron | sieve | H1 salto 1.0σ (σ marginal) n=100 / errores AR(0.85) | error absoluto mediano de la fecha (obs.) | 11,500 | informativo |  | principal | 250 | 199.0 | 100 |
| bai_perron | sieve | H1 salto 2.0σ (σ marginal) n=100 / errores AR(0.85) | potencia UDmax (5%) | 0,316 | >= 0,80 | NO | principal | 250 | 199.0 | 100 |
| bai_perron | sieve | H1 salto 2.0σ (σ marginal) n=100 / errores AR(0.85) | error absoluto mediano de la fecha (obs.) | 1,000 | informativo |  | principal | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H1 salto 1.0σ (σ marginal) n=126 / errores AR(0) | potencia UDmax (5%) | 0,992 | >= 0,80 | sí | referencia | 250 | 199.0 | 126 |
| bai_perron | bloque_8 | H1 salto 1.0σ (σ marginal) n=126 / errores AR(0) | error absoluto mediano de la fecha (obs.) | 2,000 | informativo |  | principal | 250 | 199.0 | 126 |
| bai_perron | bloque_8 | H1 salto 2.0σ (σ marginal) n=126 / errores AR(0) | potencia UDmax (5%) | 1,000 | >= 0,80 | sí | principal | 250 | 199.0 | 126 |
| bai_perron | bloque_8 | H1 salto 2.0σ (σ marginal) n=126 / errores AR(0) | error absoluto mediano de la fecha (obs.) | 0,000 | informativo |  | principal | 250 | 199.0 | 126 |
| bai_perron | sieve | H1 salto 1.0σ (σ marginal) n=126 / errores AR(0) | potencia UDmax (5%) | 0,932 | >= 0,80 | sí | referencia | 250 | 199.0 | 126 |
| bai_perron | sieve | H1 salto 1.0σ (σ marginal) n=126 / errores AR(0) | error absoluto mediano de la fecha (obs.) | 2,000 | informativo |  | principal | 250 | 199.0 | 126 |
| bai_perron | sieve | H1 salto 2.0σ (σ marginal) n=126 / errores AR(0) | potencia UDmax (5%) | 0,956 | >= 0,80 | sí | principal | 250 | 199.0 | 126 |
| bai_perron | sieve | H1 salto 2.0σ (σ marginal) n=126 / errores AR(0) | error absoluto mediano de la fecha (obs.) | 0,000 | informativo |  | principal | 250 | 199.0 | 126 |
| bai_perron | bloque_8 | H1 salto 1.0σ (σ marginal) n=126 / errores AR(0.5) | potencia UDmax (5%) | 0,752 | >= 0,80 | NO | referencia | 250 | 199.0 | 126 |
| bai_perron | bloque_8 | H1 salto 1.0σ (σ marginal) n=126 / errores AR(0.5) | error absoluto mediano de la fecha (obs.) | 5,000 | informativo |  | principal | 250 | 199.0 | 126 |
| bai_perron | bloque_8 | H1 salto 2.0σ (σ marginal) n=126 / errores AR(0.5) | potencia UDmax (5%) | 1,000 | >= 0,80 | sí | principal | 250 | 199.0 | 126 |
| bai_perron | bloque_8 | H1 salto 2.0σ (σ marginal) n=126 / errores AR(0.5) | error absoluto mediano de la fecha (obs.) | 0,000 | informativo |  | principal | 250 | 199.0 | 126 |
| bai_perron | sieve | H1 salto 1.0σ (σ marginal) n=126 / errores AR(0.5) | potencia UDmax (5%) | 0,624 | >= 0,80 | NO | referencia | 250 | 199.0 | 126 |
| bai_perron | sieve | H1 salto 1.0σ (σ marginal) n=126 / errores AR(0.5) | error absoluto mediano de la fecha (obs.) | 5,000 | informativo |  | principal | 250 | 199.0 | 126 |
| bai_perron | sieve | H1 salto 2.0σ (σ marginal) n=126 / errores AR(0.5) | potencia UDmax (5%) | 0,984 | >= 0,80 | sí | principal | 250 | 199.0 | 126 |
| bai_perron | sieve | H1 salto 2.0σ (σ marginal) n=126 / errores AR(0.5) | error absoluto mediano de la fecha (obs.) | 0,000 | informativo |  | principal | 250 | 199.0 | 126 |
| bai_perron | bloque_8 | H1 salto 1.0σ (σ marginal) n=126 / errores AR(0.85) | potencia UDmax (5%) | 0,688 | >= 0,80 | NO | referencia | 250 | 199.0 | 126 |
| bai_perron | bloque_8 | H1 salto 1.0σ (σ marginal) n=126 / errores AR(0.85) | error absoluto mediano de la fecha (obs.) | 13,000 | informativo |  | principal | 250 | 199.0 | 126 |
| bai_perron | bloque_8 | H1 salto 2.0σ (σ marginal) n=126 / errores AR(0.85) | potencia UDmax (5%) | 0,992 | >= 0,80 | sí | principal | 250 | 199.0 | 126 |
| bai_perron | bloque_8 | H1 salto 2.0σ (σ marginal) n=126 / errores AR(0.85) | error absoluto mediano de la fecha (obs.) | 1,000 | informativo |  | principal | 250 | 199.0 | 126 |
| bai_perron | sieve | H1 salto 1.0σ (σ marginal) n=126 / errores AR(0.85) | potencia UDmax (5%) | 0,104 | >= 0,80 | NO | referencia | 250 | 199.0 | 126 |
| bai_perron | sieve | H1 salto 1.0σ (σ marginal) n=126 / errores AR(0.85) | error absoluto mediano de la fecha (obs.) | 13,000 | informativo |  | principal | 250 | 199.0 | 126 |
| bai_perron | sieve | H1 salto 2.0σ (σ marginal) n=126 / errores AR(0.85) | potencia UDmax (5%) | 0,420 | >= 0,80 | NO | principal | 250 | 199.0 | 126 |
| bai_perron | sieve | H1 salto 2.0σ (σ marginal) n=126 / errores AR(0.85) | error absoluto mediano de la fecha (obs.) | 1,000 | informativo |  | principal | 250 | 199.0 | 126 |
| bai_perron | wild | H0_iid n=120 (errores sin autocorrelación) | tamaño UDmax (5%) | 0,068 | [0,02; 0,10] | sí | principal | 250 | 199.0 | 120 |
| bai_perron | wild | H0_iid n=120 (errores sin autocorrelación) | tamaño supF(1) (5%) | 0,056 | [0,02; 0,10] | sí | principal | 250 | 199.0 | 120 |
| bai_perron | wild | H0_heterocedastico n=120 (errores sin autocorrelación) | tamaño UDmax (5%) | 0,052 | [0,02; 0,10] | sí | principal | 250 | 199.0 | 120 |
| bai_perron | wild | H0_heterocedastico n=120 (errores sin autocorrelación) | tamaño supF(1) (5%) | 0,048 | [0,02; 0,10] | sí | principal | 250 | 199.0 | 120 |
| bai_perron | wild | H0 n=100 / errores AR(0) | tamaño UDmax (5%) | 0,012 | [0,02; 0,10] | NO | principal | 250 | 199.0 | 100 |
| bai_perron | wild | H0 n=100 / errores AR(0) | tamaño supF(1) (5%) | 0,028 | [0,02; 0,10] | sí | referencia | 250 | 199.0 | 100 |
| bai_perron | bloque_pw | H0 n=100 / errores AR(0) | tamaño UDmax (5%) | 0,012 | [0,02; 0,10] | NO | principal | 250 | 199.0 | 100 |
| bai_perron | bloque_pw | H0 n=100 / errores AR(0) | tamaño supF(1) (5%) | 0,016 | [0,02; 0,10] | NO | referencia | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H0 n=100 / errores AR(0) | tamaño UDmax (5%) | 0,020 | [0,02; 0,10] | sí | principal | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H0 n=100 / errores AR(0) | tamaño supF(1) (5%) | 0,020 | [0,02; 0,10] | sí | referencia | 250 | 199.0 | 100 |
| bai_perron | sieve | H0 n=100 / errores AR(0) | tamaño UDmax (5%) | 0,024 | [0,02; 0,10] | sí | principal | 250 | 199.0 | 100 |
| bai_perron | sieve | H0 n=100 / errores AR(0) | tamaño supF(1) (5%) | 0,024 | [0,02; 0,10] | sí | referencia | 250 | 199.0 | 100 |
| bai_perron | wild | H0 n=100 / errores AR(0.5) | tamaño UDmax (5%) | 0,620 | [0,02; 0,10] | NO | referencia | 250 | 199.0 | 100 |
| bai_perron | wild | H0 n=100 / errores AR(0.5) | tamaño supF(1) (5%) | 0,524 | [0,02; 0,10] | NO | referencia | 250 | 199.0 | 100 |
| bai_perron | bloque_pw | H0 n=100 / errores AR(0.5) | tamaño UDmax (5%) | 0,156 | [0,02; 0,10] | NO | principal | 250 | 199.0 | 100 |
| bai_perron | bloque_pw | H0 n=100 / errores AR(0.5) | tamaño supF(1) (5%) | 0,136 | [0,02; 0,10] | NO | referencia | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H0 n=100 / errores AR(0.5) | tamaño UDmax (5%) | 0,076 | [0,02; 0,10] | sí | principal | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H0 n=100 / errores AR(0.5) | tamaño supF(1) (5%) | 0,072 | [0,02; 0,10] | sí | referencia | 250 | 199.0 | 100 |
| bai_perron | sieve | H0 n=100 / errores AR(0.5) | tamaño UDmax (5%) | 0,056 | [0,02; 0,10] | sí | principal | 250 | 199.0 | 100 |
| bai_perron | sieve | H0 n=100 / errores AR(0.5) | tamaño supF(1) (5%) | 0,052 | [0,02; 0,10] | sí | referencia | 250 | 199.0 | 100 |
| bai_perron | wild | H0 n=100 / errores AR(0.85) | tamaño UDmax (5%) | 0,992 | [0,02; 0,10] | NO | referencia | 250 | 199.0 | 100 |
| bai_perron | wild | H0 n=100 / errores AR(0.85) | tamaño supF(1) (5%) | 0,944 | [0,02; 0,10] | NO | referencia | 250 | 199.0 | 100 |
| bai_perron | bloque_pw | H0 n=100 / errores AR(0.85) | tamaño UDmax (5%) | 0,196 | [0,02; 0,10] | NO | principal | 250 | 199.0 | 100 |
| bai_perron | bloque_pw | H0 n=100 / errores AR(0.85) | tamaño supF(1) (5%) | 0,208 | [0,02; 0,10] | NO | referencia | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H0 n=100 / errores AR(0.85) | tamaño UDmax (5%) | 0,336 | [0,02; 0,10] | NO | principal | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H0 n=100 / errores AR(0.85) | tamaño supF(1) (5%) | 0,288 | [0,02; 0,10] | NO | referencia | 250 | 199.0 | 100 |
| bai_perron | sieve | H0 n=100 / errores AR(0.85) | tamaño UDmax (5%) | 0,064 | [0,02; 0,10] | sí | principal | 250 | 199.0 | 100 |
| bai_perron | sieve | H0 n=100 / errores AR(0.85) | tamaño supF(1) (5%) | 0,056 | [0,02; 0,10] | sí | referencia | 250 | 199.0 | 100 |
| bai_perron | bloque_8 | H0 n=126 / errores AR(0) | tamaño UDmax (5%) | 0,032 | [0,02; 0,10] | sí | principal | 250 | 199.0 | 126 |
| bai_perron | bloque_8 | H0 n=126 / errores AR(0) | tamaño supF(1) (5%) | 0,036 | [0,02; 0,10] | sí | referencia | 250 | 199.0 | 126 |
| bai_perron | sieve | H0 n=126 / errores AR(0) | tamaño UDmax (5%) | 0,036 | [0,02; 0,10] | sí | principal | 250 | 199.0 | 126 |
| bai_perron | sieve | H0 n=126 / errores AR(0) | tamaño supF(1) (5%) | 0,028 | [0,02; 0,10] | sí | referencia | 250 | 199.0 | 126 |
| bai_perron | bloque_8 | H0 n=126 / errores AR(0.5) | tamaño UDmax (5%) | 0,068 | [0,02; 0,10] | sí | principal | 250 | 199.0 | 126 |
| bai_perron | bloque_8 | H0 n=126 / errores AR(0.5) | tamaño supF(1) (5%) | 0,064 | [0,02; 0,10] | sí | referencia | 250 | 199.0 | 126 |
| bai_perron | sieve | H0 n=126 / errores AR(0.5) | tamaño UDmax (5%) | 0,040 | [0,02; 0,10] | sí | principal | 250 | 199.0 | 126 |
| bai_perron | sieve | H0 n=126 / errores AR(0.5) | tamaño supF(1) (5%) | 0,040 | [0,02; 0,10] | sí | referencia | 250 | 199.0 | 126 |
| bai_perron | bloque_8 | H0 n=126 / errores AR(0.85) | tamaño UDmax (5%) | 0,412 | [0,02; 0,10] | NO | principal | 250 | 199.0 | 126 |
| bai_perron | bloque_8 | H0 n=126 / errores AR(0.85) | tamaño supF(1) (5%) | 0,340 | [0,02; 0,10] | NO | referencia | 250 | 199.0 | 126 |
| bai_perron | sieve | H0 n=126 / errores AR(0.85) | tamaño UDmax (5%) | 0,048 | [0,02; 0,10] | sí | principal | 250 | 199.0 | 126 |
| bai_perron | sieve | H0 n=126 / errores AR(0.85) | tamaño supF(1) (5%) | 0,056 | [0,02; 0,10] | sí | referencia | 250 | 199.0 | 126 |
| dfm_baing | IC_p2 | T=120,N=40,r=2 | % IC_p2 elige r verdadero | 1,000 | >= 0.9 | sí | referencia | 200 |  | 120 |
| dfm_baing | IC_p2 | T=120,N=10,r=2 | % IC_p2 elige r verdadero | 0,000 | >= 0.9 | NO | referencia | 200 |  | 120 |
| dfm_baing | IC_p2 | T=110,N=17,r=1 | % IC_p2 elige r verdadero | 0,990 | >= 0.9 | sí | principal | 200 |  | 110 |
| dfm_baing | IC_p2 | T=126,N=17,r=1 | % IC_p2 elige r verdadero | 1,000 | >= 0.9 | sí | principal | 200 |  | 126 |
| dfm_baing | IC_p2 | T=110,N=17,r=2 | % IC_p2 elige r verdadero | 0,875 | >= 0.9 | NO | principal | 200 |  | 110 |
| dfm_pca | PCA_r1 | T=110,N=17,r=1 (factor AR(0,7)) | sesgo medio de la varianza explicada por el 1.er factor (estimada - verdadera) | -0,028 | < 0.05 | sí | principal | 200 |  | 110 |
| dfm_ml | ML_r1 | T=100,N=8,r=1 | error absoluto medio del R2 por variable | 0,055 | < 0.1 | sí | referencia | 15 |  | 100 |
| dfm_ml | ML_r1 | T=110,N=17,r=1 | error absoluto medio del R2 por variable | 0,042 | < 0.1 | sí | principal | 15 |  | 110 |
| dominancia | filas | p=5 colineal, n=300 | /Johnson - LMG/ máx (en R2) | 0,023 | < 0.05 | sí | referencia | 1 |  | 300 |
| dominancia | filas | p=5 colineal, n=300, regresores AR(0.0), errores AR(0.0) | error absoluto medio de phi (R2) | 0,013 | < 0.03 | sí | referencia | 60 | 100.0 | 300 |
| dominancia | filas | p=5 colineal, n=300, regresores AR(0.0), errores AR(0.0) | cobertura IC95 bootstrap de phi | 0,943 | [0,90; 0,98] | sí | referencia | 60 | 100.0 | 300 |
| dominancia | filas | p=5 colineal, n=300, regresores AR(0.0), errores AR(0.0) | % acierto en las 2 variables dominantes (orden) | 0,900 | >= 0.8 | sí | referencia | 60 | 100.0 | 300 |
| dominancia | filas | p=5 colineal, n=300, regresores AR(0.0), errores AR(0.0) | error relativo máx del VIF | 0,125 | < 0.2 | sí | referencia | 60 |  | 300 |
| dominancia | filas | p=5 colineal, n=100, regresores AR(0.0), errores AR(0.0) | error absoluto medio de phi (R2) | 0,022 | < 0.03 | sí | principal | 60 | 100.0 | 100 |
| dominancia | filas | p=5 colineal, n=100, regresores AR(0.0), errores AR(0.0) | cobertura IC95 bootstrap de phi | 0,937 | [0,90; 0,98] | sí | principal | 60 | 100.0 | 100 |
| dominancia | filas | p=5 colineal, n=100, regresores AR(0.0), errores AR(0.0) | % acierto en las 2 variables dominantes (orden) | 0,667 | >= 0.8 | NO | principal | 60 | 100.0 | 100 |
| dominancia | filas | p=5 colineal, n=100, regresores AR(0.0), errores AR(0.0) | error relativo máx del VIF | 0,216 | < 0.2 | NO | principal | 60 |  | 100 |
| dominancia | filas | p=5 colineal, n=100, regresores AR(0.8), errores AR(0.5) | error absoluto medio de phi (R2) | 0,038 | < 0.03 | NO | referencia | 60 | 100.0 | 100 |
| dominancia | filas | p=5 colineal, n=100, regresores AR(0.8), errores AR(0.5) | cobertura IC95 bootstrap de phi | 0,713 | [0,90; 0,98] | NO | referencia | 60 | 100.0 | 100 |
| dominancia | filas | p=5 colineal, n=100, regresores AR(0.8), errores AR(0.5) | % acierto en las 2 variables dominantes (orden) | 0,367 | >= 0.8 | NO | referencia | 60 | 100.0 | 100 |
| dominancia | filas | p=5 colineal, n=100, regresores AR(0.8), errores AR(0.5) | error relativo máx del VIF | 0,654 | < 0.2 | NO | referencia | 60 |  | 100 |
| dominancia | bloque_8 | p=5 colineal, n=100, regresores AR(0.8), errores AR(0.5) | error absoluto medio de phi (R2) | 0,038 | < 0.03 | NO | principal | 60 | 100.0 | 100 |
| dominancia | bloque_8 | p=5 colineal, n=100, regresores AR(0.8), errores AR(0.5) | cobertura IC95 bootstrap de phi | 0,857 | [0,90; 0,98] | NO | principal | 60 | 100.0 | 100 |
| dominancia | bloque_8 | p=5 colineal, n=100, regresores AR(0.8), errores AR(0.5) | % acierto en las 2 variables dominantes (orden) | 0,367 | >= 0.8 | NO | principal | 60 | 100.0 | 100 |
| dominancia | bloque_8 | p=5 colineal, n=100, regresores AR(0.8), errores AR(0.5) | error relativo máx del VIF | 0,654 | < 0.2 | NO | principal | 60 |  | 100 |
| dominancia | bloque_8 | p=5 colineal, n=126, regresores AR(0.8), errores AR(0.5) | error absoluto medio de phi (R2) | 0,033 | < 0.03 | NO | principal | 60 | 100.0 | 126 |
| dominancia | bloque_8 | p=5 colineal, n=126, regresores AR(0.8), errores AR(0.5) | cobertura IC95 bootstrap de phi | 0,893 | [0,90; 0,98] | NO | principal | 60 | 100.0 | 126 |
| dominancia | bloque_8 | p=5 colineal, n=126, regresores AR(0.8), errores AR(0.5) | % acierto en las 2 variables dominantes (orden) | 0,583 | >= 0.8 | NO | principal | 60 | 100.0 | 126 |
| dominancia | bloque_8 | p=5 colineal, n=126, regresores AR(0.8), errores AR(0.5) | error relativo máx del VIF | 0,474 | < 0.2 | NO | principal | 60 |  | 126 |
| lp_ols | NW_h+1 | ρ=0.6, n=90, h=0 | cobertura IC95 | 0,917 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | NW_h+1 | ρ=0.6, n=90, h=4 | cobertura IC95 | 0,897 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | NW_h+1 | ρ=0.6, n=90, h=8 | cobertura IC95 | 0,900 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | NW_h+1 | ρ=0.6, n=90, h=12 | cobertura IC95 | 0,910 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | NW_h+1 | ρ=0.6, n=90, h=-4 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,930 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | NW_h+1 | ρ=0.6, n=90, h=-2 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,935 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | NW_h+1 | ρ=0.6, n=90, h=4-8 | cobertura IC95 | 0,877 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | NW_2h+2 | ρ=0.6, n=90, h=0 | cobertura IC95 | 0,915 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | NW_2h+2 | ρ=0.6, n=90, h=4 | cobertura IC95 | 0,873 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | NW_2h+2 | ρ=0.6, n=90, h=8 | cobertura IC95 | 0,868 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | NW_2h+2 | ρ=0.6, n=90, h=12 | cobertura IC95 | 0,843 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | NW_2h+2 | ρ=0.6, n=90, h=-4 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,890 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | NW_2h+2 | ρ=0.6, n=90, h=-2 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,920 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | NW_2h+2 | ρ=0.6, n=90, h=4-8 | cobertura IC95 | 0,825 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | EWC | ρ=0.6, n=90, h=0 | cobertura IC95 | 0,917 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | EWC | ρ=0.6, n=90, h=4 | cobertura IC95 | 0,907 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | EWC | ρ=0.6, n=90, h=8 | cobertura IC95 | 0,943 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | EWC | ρ=0.6, n=90, h=12 | cobertura IC95 | 0,948 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | EWC | ρ=0.6, n=90, h=-4 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,930 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | EWC | ρ=0.6, n=90, h=-2 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,935 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | EWC | ρ=0.6, n=90, h=4-8 | cobertura IC95 | 0,912 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | NW_h+1 | ρ=0.9, n=90, h=0 | cobertura IC95 | 0,938 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | NW_h+1 | ρ=0.9, n=90, h=4 | cobertura IC95 | 0,850 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | NW_h+1 | ρ=0.9, n=90, h=8 | cobertura IC95 | 0,845 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | NW_h+1 | ρ=0.9, n=90, h=12 | cobertura IC95 | 0,823 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | NW_h+1 | ρ=0.9, n=90, h=-4 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,927 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | NW_h+1 | ρ=0.9, n=90, h=-2 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,927 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | NW_h+1 | ρ=0.9, n=90, h=4-8 | cobertura IC95 | 0,782 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | NW_2h+2 | ρ=0.9, n=90, h=0 | cobertura IC95 | 0,927 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | NW_2h+2 | ρ=0.9, n=90, h=4 | cobertura IC95 | 0,833 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | NW_2h+2 | ρ=0.9, n=90, h=8 | cobertura IC95 | 0,807 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | NW_2h+2 | ρ=0.9, n=90, h=12 | cobertura IC95 | 0,735 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | NW_2h+2 | ρ=0.9, n=90, h=-4 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,902 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | NW_2h+2 | ρ=0.9, n=90, h=-2 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,925 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | NW_2h+2 | ρ=0.9, n=90, h=4-8 | cobertura IC95 | 0,762 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | EWC | ρ=0.9, n=90, h=0 | cobertura IC95 | 0,938 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | EWC | ρ=0.9, n=90, h=4 | cobertura IC95 | 0,887 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | EWC | ρ=0.9, n=90, h=8 | cobertura IC95 | 0,882 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | EWC | ρ=0.9, n=90, h=12 | cobertura IC95 | 0,910 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | EWC | ρ=0.9, n=90, h=-4 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,938 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | EWC | ρ=0.9, n=90, h=-2 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,948 | [0,90; 0,98] | sí | principal | 400 |  | 90 |
| lp_ols | EWC | ρ=0.9, n=90, h=4-8 | cobertura IC95 | 0,838 | [0,90; 0,98] | NO | principal | 400 |  | 90 |
| lp_ols | NW_h+1 | ρ=0.6, n=110, h=0 | cobertura IC95 | 0,927 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | NW_h+1 | ρ=0.6, n=110, h=4 | cobertura IC95 | 0,922 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | NW_h+1 | ρ=0.6, n=110, h=8 | cobertura IC95 | 0,905 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | NW_h+1 | ρ=0.6, n=110, h=12 | cobertura IC95 | 0,870 | [0,90; 0,98] | NO | principal | 400 |  | 110 |
| lp_ols | NW_h+1 | ρ=0.6, n=110, h=-4 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,922 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | NW_h+1 | ρ=0.6, n=110, h=-2 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,935 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | NW_h+1 | ρ=0.6, n=110, h=4-8 | cobertura IC95 | 0,877 | [0,90; 0,98] | NO | principal | 400 |  | 110 |
| lp_ols | NW_2h+2 | ρ=0.6, n=110, h=0 | cobertura IC95 | 0,927 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | NW_2h+2 | ρ=0.6, n=110, h=4 | cobertura IC95 | 0,900 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | NW_2h+2 | ρ=0.6, n=110, h=8 | cobertura IC95 | 0,870 | [0,90; 0,98] | NO | principal | 400 |  | 110 |
| lp_ols | NW_2h+2 | ρ=0.6, n=110, h=12 | cobertura IC95 | 0,830 | [0,90; 0,98] | NO | principal | 400 |  | 110 |
| lp_ols | NW_2h+2 | ρ=0.6, n=110, h=-4 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,917 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | NW_2h+2 | ρ=0.6, n=110, h=-2 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,920 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | NW_2h+2 | ρ=0.6, n=110, h=4-8 | cobertura IC95 | 0,850 | [0,90; 0,98] | NO | principal | 400 |  | 110 |
| lp_ols | EWC | ρ=0.6, n=110, h=0 | cobertura IC95 | 0,938 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | EWC | ρ=0.6, n=110, h=4 | cobertura IC95 | 0,938 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | EWC | ρ=0.6, n=110, h=8 | cobertura IC95 | 0,932 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | EWC | ρ=0.6, n=110, h=12 | cobertura IC95 | 0,920 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | EWC | ρ=0.6, n=110, h=-4 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,943 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | EWC | ρ=0.6, n=110, h=-2 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,932 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | EWC | ρ=0.6, n=110, h=4-8 | cobertura IC95 | 0,915 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | NW_h+1 | ρ=0.9, n=110, h=0 | cobertura IC95 | 0,935 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | NW_h+1 | ρ=0.9, n=110, h=4 | cobertura IC95 | 0,877 | [0,90; 0,98] | NO | principal | 400 |  | 110 |
| lp_ols | NW_h+1 | ρ=0.9, n=110, h=8 | cobertura IC95 | 0,865 | [0,90; 0,98] | NO | principal | 400 |  | 110 |
| lp_ols | NW_h+1 | ρ=0.9, n=110, h=12 | cobertura IC95 | 0,820 | [0,90; 0,98] | NO | principal | 400 |  | 110 |
| lp_ols | NW_h+1 | ρ=0.9, n=110, h=-4 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,927 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | NW_h+1 | ρ=0.9, n=110, h=-2 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,943 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | NW_h+1 | ρ=0.9, n=110, h=4-8 | cobertura IC95 | 0,812 | [0,90; 0,98] | NO | principal | 400 |  | 110 |
| lp_ols | NW_2h+2 | ρ=0.9, n=110, h=0 | cobertura IC95 | 0,925 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | NW_2h+2 | ρ=0.9, n=110, h=4 | cobertura IC95 | 0,853 | [0,90; 0,98] | NO | principal | 400 |  | 110 |
| lp_ols | NW_2h+2 | ρ=0.9, n=110, h=8 | cobertura IC95 | 0,812 | [0,90; 0,98] | NO | principal | 400 |  | 110 |
| lp_ols | NW_2h+2 | ρ=0.9, n=110, h=12 | cobertura IC95 | 0,760 | [0,90; 0,98] | NO | principal | 400 |  | 110 |
| lp_ols | NW_2h+2 | ρ=0.9, n=110, h=-4 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,907 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | NW_2h+2 | ρ=0.9, n=110, h=-2 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,932 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | NW_2h+2 | ρ=0.9, n=110, h=4-8 | cobertura IC95 | 0,782 | [0,90; 0,98] | NO | principal | 400 |  | 110 |
| lp_ols | EWC | ρ=0.9, n=110, h=0 | cobertura IC95 | 0,948 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | EWC | ρ=0.9, n=110, h=4 | cobertura IC95 | 0,907 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | EWC | ρ=0.9, n=110, h=8 | cobertura IC95 | 0,880 | [0,90; 0,98] | NO | principal | 400 |  | 110 |
| lp_ols | EWC | ρ=0.9, n=110, h=12 | cobertura IC95 | 0,880 | [0,90; 0,98] | NO | principal | 400 |  | 110 |
| lp_ols | EWC | ρ=0.9, n=110, h=-4 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,930 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | EWC | ρ=0.9, n=110, h=-2 (pretendencia: efecto verdadero 0) | cobertura IC95 | 0,948 | [0,90; 0,98] | sí | principal | 400 |  | 110 |
| lp_ols | EWC | ρ=0.9, n=110, h=4-8 | cobertura IC95 | 0,845 | [0,90; 0,98] | NO | principal | 400 |  | 110 |
| lp_iv | AR | instrumento_fuerte, n=90, h=0 | cobertura IC Anderson-Rubin | 0,970 | [0,90; 0,98] | sí | principal | 300 |  | 90 |
| lp_iv | IC_normal | instrumento_fuerte, n=90, h=0 | cobertura IC normal 2SLS | 0,953 | [0,90; 0,98] | sí | principal | 300 |  | 90 |
| lp_iv | AR | instrumento_fuerte, n=90, h=4 | cobertura IC Anderson-Rubin | 0,933 | [0,90; 0,98] | sí | principal | 300 |  | 90 |
| lp_iv | IC_normal | instrumento_fuerte, n=90, h=4 | cobertura IC normal 2SLS | 0,863 | [0,90; 0,98] | NO | principal | 300 |  | 90 |
| lp_iv | AR | instrumento_fuerte, n=90, h=8 | cobertura IC Anderson-Rubin | 0,967 | [0,90; 0,98] | sí | principal | 300 |  | 90 |
| lp_iv | IC_normal | instrumento_fuerte, n=90, h=8 | cobertura IC normal 2SLS | 0,900 | [0,90; 0,98] | sí | principal | 300 |  | 90 |
| lp_iv | AR | instrumento_fuerte, n=90, h=12 | cobertura IC Anderson-Rubin | 0,990 | [0,90; 0,98] | NO | principal | 300 |  | 90 |
| lp_iv | IC_normal | instrumento_fuerte, n=90, h=12 | cobertura IC normal 2SLS | 0,907 | [0,90; 0,98] | sí | principal | 300 |  | 90 |
| lp_iv | AR | instrumento_fuerte, n=90, h=4-8 | cobertura IC Anderson-Rubin | 0,953 | [0,90; 0,98] | sí | principal | 300 |  | 90 |
| lp_iv | IC_normal | instrumento_fuerte, n=90, h=4-8 | cobertura IC normal 2SLS | 0,850 | [0,90; 0,98] | NO | principal | 300 |  | 90 |
| lp_iv | AR | instrumento_debil, n=90, h=0 | cobertura IC Anderson-Rubin | 0,970 | [0,90; 0,98] | sí | principal | 300 |  | 90 |
| lp_iv | IC_normal | instrumento_debil, n=90, h=0 | cobertura IC normal 2SLS | 0,887 | [0,90; 0,98] | NO | referencia | 300 |  | 90 |
| lp_iv | AR | instrumento_debil, n=90, h=4 | cobertura IC Anderson-Rubin | 0,997 | [0,90; 0,98] | NO | principal | 300 |  | 90 |
| lp_iv | IC_normal | instrumento_debil, n=90, h=4 | cobertura IC normal 2SLS | 0,993 | [0,90; 0,98] | NO | referencia | 300 |  | 90 |
| lp_iv | AR | instrumento_debil, n=90, h=8 | cobertura IC Anderson-Rubin | 0,990 | [0,90; 0,98] | NO | principal | 300 |  | 90 |
| lp_iv | IC_normal | instrumento_debil, n=90, h=8 | cobertura IC normal 2SLS | 0,987 | [0,90; 0,98] | NO | referencia | 300 |  | 90 |
| lp_iv | AR | instrumento_debil, n=90, h=12 | cobertura IC Anderson-Rubin | 1,000 | [0,90; 0,98] | NO | principal | 300 |  | 90 |
| lp_iv | IC_normal | instrumento_debil, n=90, h=12 | cobertura IC normal 2SLS | 0,990 | [0,90; 0,98] | NO | referencia | 300 |  | 90 |
| lp_iv | AR | instrumento_debil, n=90, h=4-8 | cobertura IC Anderson-Rubin | 0,997 | [0,90; 0,98] | NO | principal | 300 |  | 90 |
| lp_iv | IC_normal | instrumento_debil, n=90, h=4-8 | cobertura IC normal 2SLS | 0,990 | [0,90; 0,98] | NO | referencia | 300 |  | 90 |
| lp_iv | AR | instrumento_debil_rho0.8, n=90, h=0 | cobertura IC Anderson-Rubin | 0,990 | [0,90; 0,98] | NO | principal | 300 |  | 90 |
| lp_iv | IC_normal | instrumento_debil_rho0.8, n=90, h=0 | cobertura IC normal 2SLS | 0,923 | [0,90; 0,98] | sí | referencia | 300 |  | 90 |
| lp_iv | AR | instrumento_debil_rho0.8, n=90, h=4 | cobertura IC Anderson-Rubin | 0,990 | [0,90; 0,98] | NO | principal | 300 |  | 90 |
| lp_iv | IC_normal | instrumento_debil_rho0.8, n=90, h=4 | cobertura IC normal 2SLS | 0,990 | [0,90; 0,98] | NO | referencia | 300 |  | 90 |
| lp_iv | AR | instrumento_debil_rho0.8, n=90, h=8 | cobertura IC Anderson-Rubin | 1,000 | [0,90; 0,98] | NO | principal | 300 |  | 90 |
| lp_iv | IC_normal | instrumento_debil_rho0.8, n=90, h=8 | cobertura IC normal 2SLS | 0,983 | [0,90; 0,98] | NO | referencia | 300 |  | 90 |
| lp_iv | AR | instrumento_debil_rho0.8, n=90, h=12 | cobertura IC Anderson-Rubin | 0,997 | [0,90; 0,98] | NO | principal | 300 |  | 90 |
| lp_iv | IC_normal | instrumento_debil_rho0.8, n=90, h=12 | cobertura IC normal 2SLS | 0,963 | [0,90; 0,98] | sí | referencia | 300 |  | 90 |
| lp_iv | AR | instrumento_debil_rho0.8, n=90, h=4-8 | cobertura IC Anderson-Rubin | 0,997 | [0,90; 0,98] | NO | principal | 300 |  | 90 |
| lp_iv | IC_normal | instrumento_debil_rho0.8, n=90, h=4-8 | cobertura IC normal 2SLS | 0,980 | [0,90; 0,98] | sí | referencia | 300 |  | 90 |
| lp_iv | AR | instrumento_fuerte, n=110, h=0 | cobertura IC Anderson-Rubin | 0,960 | [0,90; 0,98] | sí | principal | 300 |  | 110 |
| lp_iv | IC_normal | instrumento_fuerte, n=110, h=0 | cobertura IC normal 2SLS | 0,937 | [0,90; 0,98] | sí | principal | 300 |  | 110 |
| lp_iv | AR | instrumento_fuerte, n=110, h=4 | cobertura IC Anderson-Rubin | 0,913 | [0,90; 0,98] | sí | principal | 300 |  | 110 |
| lp_iv | IC_normal | instrumento_fuerte, n=110, h=4 | cobertura IC normal 2SLS | 0,863 | [0,90; 0,98] | NO | principal | 300 |  | 110 |
| lp_iv | AR | instrumento_fuerte, n=110, h=8 | cobertura IC Anderson-Rubin | 0,960 | [0,90; 0,98] | sí | principal | 300 |  | 110 |
| lp_iv | IC_normal | instrumento_fuerte, n=110, h=8 | cobertura IC normal 2SLS | 0,910 | [0,90; 0,98] | sí | principal | 300 |  | 110 |
| lp_iv | AR | instrumento_fuerte, n=110, h=12 | cobertura IC Anderson-Rubin | 0,983 | [0,90; 0,98] | NO | principal | 300 |  | 110 |
| lp_iv | IC_normal | instrumento_fuerte, n=110, h=12 | cobertura IC normal 2SLS | 0,897 | [0,90; 0,98] | NO | principal | 300 |  | 110 |
| lp_iv | AR | instrumento_fuerte, n=110, h=4-8 | cobertura IC Anderson-Rubin | 0,953 | [0,90; 0,98] | sí | principal | 300 |  | 110 |
| lp_iv | IC_normal | instrumento_fuerte, n=110, h=4-8 | cobertura IC normal 2SLS | 0,887 | [0,90; 0,98] | NO | principal | 300 |  | 110 |
| lp_iv | AR | instrumento_debil, n=110, h=0 | cobertura IC Anderson-Rubin | 0,963 | [0,90; 0,98] | sí | principal | 300 |  | 110 |
| lp_iv | IC_normal | instrumento_debil, n=110, h=0 | cobertura IC normal 2SLS | 0,913 | [0,90; 0,98] | sí | referencia | 300 |  | 110 |
| lp_iv | AR | instrumento_debil, n=110, h=4 | cobertura IC Anderson-Rubin | 0,990 | [0,90; 0,98] | NO | principal | 300 |  | 110 |
| lp_iv | IC_normal | instrumento_debil, n=110, h=4 | cobertura IC normal 2SLS | 0,993 | [0,90; 0,98] | NO | referencia | 300 |  | 110 |
| lp_iv | AR | instrumento_debil, n=110, h=8 | cobertura IC Anderson-Rubin | 0,993 | [0,90; 0,98] | NO | principal | 300 |  | 110 |
| lp_iv | IC_normal | instrumento_debil, n=110, h=8 | cobertura IC normal 2SLS | 0,987 | [0,90; 0,98] | NO | referencia | 300 |  | 110 |
| lp_iv | AR | instrumento_debil, n=110, h=12 | cobertura IC Anderson-Rubin | 0,997 | [0,90; 0,98] | NO | principal | 300 |  | 110 |
| lp_iv | IC_normal | instrumento_debil, n=110, h=12 | cobertura IC normal 2SLS | 0,970 | [0,90; 0,98] | sí | referencia | 300 |  | 110 |
| lp_iv | AR | instrumento_debil, n=110, h=4-8 | cobertura IC Anderson-Rubin | 0,983 | [0,90; 0,98] | NO | principal | 300 |  | 110 |
| lp_iv | IC_normal | instrumento_debil, n=110, h=4-8 | cobertura IC normal 2SLS | 0,983 | [0,90; 0,98] | NO | referencia | 300 |  | 110 |
| lp_iv | AR | instrumento_debil_rho0.8, n=110, h=0 | cobertura IC Anderson-Rubin | 0,980 | [0,90; 0,98] | sí | principal | 300 |  | 110 |
| lp_iv | IC_normal | instrumento_debil_rho0.8, n=110, h=0 | cobertura IC normal 2SLS | 0,930 | [0,90; 0,98] | sí | referencia | 300 |  | 110 |
| lp_iv | AR | instrumento_debil_rho0.8, n=110, h=4 | cobertura IC Anderson-Rubin | 0,997 | [0,90; 0,98] | NO | principal | 300 |  | 110 |
| lp_iv | IC_normal | instrumento_debil_rho0.8, n=110, h=4 | cobertura IC normal 2SLS | 0,997 | [0,90; 0,98] | NO | referencia | 300 |  | 110 |
| lp_iv | AR | instrumento_debil_rho0.8, n=110, h=8 | cobertura IC Anderson-Rubin | 0,993 | [0,90; 0,98] | NO | principal | 300 |  | 110 |
| lp_iv | IC_normal | instrumento_debil_rho0.8, n=110, h=8 | cobertura IC normal 2SLS | 0,973 | [0,90; 0,98] | sí | referencia | 300 |  | 110 |
| lp_iv | AR | instrumento_debil_rho0.8, n=110, h=12 | cobertura IC Anderson-Rubin | 1,000 | [0,90; 0,98] | NO | principal | 300 |  | 110 |
| lp_iv | IC_normal | instrumento_debil_rho0.8, n=110, h=12 | cobertura IC normal 2SLS | 0,983 | [0,90; 0,98] | NO | referencia | 300 |  | 110 |
| lp_iv | AR | instrumento_debil_rho0.8, n=110, h=4-8 | cobertura IC Anderson-Rubin | 0,997 | [0,90; 0,98] | NO | principal | 300 |  | 110 |
| lp_iv | IC_normal | instrumento_debil_rho0.8, n=110, h=4-8 | cobertura IC normal 2SLS | 0,983 | [0,90; 0,98] | NO | referencia | 300 |  | 110 |
| lp_iv | AR_unilateral | efecto nulo, IV fuerte, n=110, h=4 | tamaño AR unilateral (H1: β<0) al 5% | 0,057 | [0,02; 0,10] | sí | principal | 300 |  | 110 |
| lp_iv | AR_unilateral | efecto nulo, IV fuerte, n=110, agregado 4-8 | tamaño AR unilateral (H1: β<0) al 5% | 0,060 | [0,02; 0,10] | sí | principal | 300 |  | 110 |
| lp_iv | AR_unilateral | efecto nulo, IV fuerte, n=110, h=4 | tamaño AR bilateral al 5% | 0,033 | [0,02; 0,10] | sí | referencia | 300 |  | 110 |
| lp_iv | AR_unilateral | efecto -1, IV fuerte, n=110, h=4 | potencia AR unilateral (H1: β<0) al 5% | 0,853 | >= 0,80 | sí | principal | 300 |  | 110 |
| lp_iv | AR_unilateral | efecto -1, IV fuerte, n=110, agregado 4-8 | potencia AR unilateral (H1: β<0) al 5% | 0,673 | >= 0,80 | NO | principal | 300 |  | 110 |
| lp_iv | AR_unilateral | efecto -1, IV fuerte, n=110, h=4 | potencia AR bilateral al 5% | 0,740 | >= 0,80 | NO | referencia | 300 |  | 110 |
| lp_iv | pretendencias | IV válido, n=110, h=-1 | tamaño (p AR bilateral < 0,05) | 0,040 | [0,02; 0,10] | sí | principal | 300 |  | 110 |
| lp_iv | pretendencias | IV válido, n=110, algún h en -4..-1 | tamaño (p AR bilateral < 0,05 en algún h) | 0,143 | informativo |  | referencia | 300 |  | 110 |
| lp_iv | pretendencias | IV contaminado, n=110, h=-1 | detección (p AR bilateral < 0,05) | 0,993 | >= 0,80 | sí | principal | 300 |  | 110 |
| lp_iv | pretendencias | IV contaminado, n=110, algún h en -4..-1 | detección (p AR bilateral < 0,05 en algún h) | 0,993 | >= 0,80 | sí | referencia | 300 |  | 110 |
| lp_iv | placebo_permutacion | efecto nulo, IV fuerte, n=110, h=4 (permutación libre) | tamaño (p_perm < 0,05) | 0,063 | [0,02; 0,10] | sí | principal | 300 | 199.0 | 110 |
| lp_iv | placebo_permutacion | efecto nulo, IV fuerte, n=110, agregado 4-8 (desplazamiento circular) | tamaño (p_perm < 0,05) | 0,090 | [0,02; 0,10] | sí | principal | 300 | 199.0 | 110 |
| lp_iv | placebo_permutacion | efecto 1, IV fuerte, n=110, h=4 (permutación libre) | potencia (p_perm < 0,05) | 0,353 | >= 0,80 | NO | principal | 300 | 199.0 | 110 |
| lp_iv | placebo_permutacion | efecto 1, IV fuerte, n=110, agregado 4-8 (desplazamiento circular) | potencia (p_perm < 0,05) | 0,213 | >= 0,80 | NO | principal | 300 | 199.0 | 110 |
| markov_switching | bootstrap_LR_1v2 | H0_1reg (T=200) | tamaño del bootstrap LR 1 vs 2 (5%) | 0,000 | [0,02; 0,10] | NO | referencia | 20 | 39.0 | 200 |
| markov_switching | bootstrap_LR_1v2 | H1_2reg (T=200) | potencia del bootstrap LR 1 vs 2 (5%) | 0,800 | >= 0,80 | sí | referencia | 20 | 39.0 | 200 |
| markov_switching | bootstrap_LR_1v2 | H0_1reg (T=110) | tamaño del bootstrap LR 1 vs 2 (5%) | 0,000 | [0,02; 0,10] | NO | principal | 20 | 39.0 | 110 |
| markov_switching | bootstrap_LR_1v2 | H1_2reg (T=110) | potencia del bootstrap LR 1 vs 2 (5%) | 0,400 | >= 0,80 | NO | principal | 20 | 39.0 | 110 |
| markov_switching | bootstrap_LR_2v3 | 2reg_test_2v3 (T=250) | rechazo bootstrap LR 2 vs 3 (5%) | 0,000 | informativo |  | referencia | 6 | 19.0 | 250 |
| markov_switching | bootstrap_LR_2v3 | 3reg_test_2v3 (T=250) | rechazo bootstrap LR 2 vs 3 (5%) | 0,000 | informativo |  | referencia | 6 | 19.0 | 250 |
| markov_switching | BIC | verdadero_1reg (T=250) | % BIC elige k verdadero | 1,000 | >= 0.7 | sí | referencia | 30 |  | 250 |
| markov_switching | BIC | verdadero_2reg (T=250) | % BIC elige k verdadero | 0,800 | >= 0.7 | sí | referencia | 30 |  | 250 |
| markov_switching | BIC | verdadero_3reg (T=250) | % BIC elige k verdadero | 0,700 | >= 0.7 | sí | referencia | 30 |  | 250 |
| markov_switching | BIC | verdadero_1reg (T=110) | % BIC elige k verdadero | 0,967 | >= 0.7 | sí | principal | 30 |  | 110 |
| markov_switching | BIC | verdadero_2reg (T=110) | % BIC elige k verdadero | 0,567 | >= 0.7 | NO | principal | 30 |  | 110 |
| markov_switching | BIC | verdadero_3reg (T=110) | % BIC elige k verdadero | 0,367 | >= 0.7 | NO | principal | 30 |  | 110 |
| permutacion_fechas | t_studentizado_2tramos | H0_iid (n=100) | tamaño (5%) | 0,048 | [0,02; 0,10] | sí | principal | 250 | 2000.0 | 100 |
| permutacion_fechas | dif_sin_studentizar_2tramos | H0_iid (n=100) | tamaño (5%) | 0,036 | [0,02; 0,10] | sí | principal | 250 | 2000.0 | 100 |
| permutacion_fechas | t_studentizado_2tramos | H0_AR0.5 (n=100) | tamaño (5%) | 0,036 | [0,02; 0,10] | sí | principal | 250 | 2000.0 | 100 |
| permutacion_fechas | dif_sin_studentizar_2tramos | H0_AR0.5 (n=100) | tamaño (5%) | 0,024 | [0,02; 0,10] | sí | principal | 250 | 2000.0 | 100 |
| permutacion_fechas | t_studentizado_2tramos | H1_ruptura_pendiente (n=100) | potencia (5%) | 0,316 | >= 0,80 | NO | principal | 250 | 2000.0 | 100 |
| permutacion_fechas | dif_sin_studentizar_2tramos | H1_ruptura_pendiente (n=100) | potencia (5%) | 0,244 | >= 0,80 | NO | principal | 250 | 2000.0 | 100 |
| permutacion_fechas | t_studentizado_2tramos | H0_iid salto 1,0 (n=200) | tamaño (5%) | 0,040 | [0,02; 0,10] | sí | referencia | 250 | 2000.0 | 200 |
| permutacion_fechas | dif_sin_studentizar_2tramos | H0_iid salto 1,0 (n=200) | tamaño (5%) | 0,020 | [0,02; 0,10] | sí | referencia | 250 | 2000.0 | 200 |
| permutacion_fechas | t_studentizado_2tramos | H1_ruptura_pendiente salto 1,0 (n=200) | potencia (5%) | 0,800 | >= 0,80 | sí | referencia | 250 | 2000.0 | 200 |
| permutacion_fechas | dif_sin_studentizar_2tramos | H1_ruptura_pendiente salto 1,0 (n=200) | potencia (5%) | 0,732 | >= 0,80 | NO | referencia | 250 | 2000.0 | 200 |
| permutacion_fechas | Q_homo_5tramos | H0 pendiente constante, 5 tramos no contiguos, n=126, min 8, AR(0.0) | tamaño (5%) | 0,025 | [0,02; 0,10] | sí | principal | 200 | 499.0 | 126 |
| permutacion_fechas | maxt_homo_5tramos | H0 pendiente constante, 5 tramos no contiguos, n=126, min 8, AR(0.0) | tamaño (5%) | 0,025 | [0,02; 0,10] | sí | principal | 200 | 499.0 | 126 |
| permutacion_fechas | Q_hac_5tramos | H0 pendiente constante, 5 tramos no contiguos, n=126, min 8, AR(0.0) | tamaño (5%) | 0,015 | [0,02; 0,10] | NO | principal | 200 | 499.0 | 126 |
| permutacion_fechas | Q_homo_5tramos | H1 pendientes (0,3; 0,3; 1,2; 1,2; 0,3), 5 tramos no contiguos, n=126, min 8, AR(0.0) | potencia (5%) | 0,315 | >= 0,80 | NO | principal | 200 | 499.0 | 126 |
| permutacion_fechas | maxt_homo_5tramos | H1 pendientes (0,3; 0,3; 1,2; 1,2; 0,3), 5 tramos no contiguos, n=126, min 8, AR(0.0) | potencia (5%) | 0,135 | >= 0,80 | NO | principal | 200 | 499.0 | 126 |
| permutacion_fechas | Q_hac_5tramos | H1 pendientes (0,3; 0,3; 1,2; 1,2; 0,3), 5 tramos no contiguos, n=126, min 8, AR(0.0) | potencia (5%) | 0,080 | >= 0,80 | NO | principal | 200 | 499.0 | 126 |
| permutacion_fechas | Q_homo_5tramos | H0 pendiente constante, 5 tramos no contiguos, n=126, min 8, AR(0.8) | tamaño (5%) | 0,015 | [0,02; 0,10] | NO | principal | 200 | 499.0 | 126 |
| permutacion_fechas | maxt_homo_5tramos | H0 pendiente constante, 5 tramos no contiguos, n=126, min 8, AR(0.8) | tamaño (5%) | 0,020 | [0,02; 0,10] | sí | principal | 200 | 499.0 | 126 |
| permutacion_fechas | Q_hac_5tramos | H0 pendiente constante, 5 tramos no contiguos, n=126, min 8, AR(0.8) | tamaño (5%) | 0,000 | [0,02; 0,10] | NO | principal | 200 | 499.0 | 126 |
| permutacion_fechas | Q_homo_5tramos | H1 pendientes (0,3; 0,3; 1,2; 1,2; 0,3), 5 tramos no contiguos, n=126, min 8, AR(0.8) | potencia (5%) | 0,240 | >= 0,80 | NO | principal | 200 | 499.0 | 126 |
| permutacion_fechas | maxt_homo_5tramos | H1 pendientes (0,3; 0,3; 1,2; 1,2; 0,3), 5 tramos no contiguos, n=126, min 8, AR(0.8) | potencia (5%) | 0,110 | >= 0,80 | NO | principal | 200 | 499.0 | 126 |
| permutacion_fechas | Q_hac_5tramos | H1 pendientes (0,3; 0,3; 1,2; 1,2; 0,3), 5 tramos no contiguos, n=126, min 8, AR(0.8) | potencia (5%) | 0,075 | >= 0,80 | NO | principal | 200 | 499.0 | 126 |
| shap_grupos | ranking_familias | DGP aditivo+interacción (orden verdadero F1>F2>F3>F4) | % ranking correcto de familias | 1,000 | >= 0.9 | sí | referencia | 30 |  | 400 |
| shap_grupos | estabilidad_bootstrap | DGP claro | % réplicas bootstrap con ranking completo igual (media) | 1,000 | >= 0.8 | sí | referencia | 10 | 20.0 | 400 |
| shap_grupos | estabilidad_pliegues | DGP claro | % pliegues temporales con ranking completo igual (media) | 1,000 | informativo |  | referencia | 10 | 4.0 | 400 |
| shap_grupos | estabilidad_bootstrap | DGP duro (F1≈F2) | % réplicas bootstrap con ranking completo igual (media) | 0,835 | informativo |  | referencia | 10 | 20.0 | 400 |
| shap_grupos | estabilidad_pliegues | DGP duro (F1≈F2) | % pliegues temporales con ranking completo igual (media) | 0,750 | informativo |  | referencia | 10 | 4.0 | 400 |
| shap_grupos | sustituto | arbol sustituto prof.3 | fidelidad R2 | 0,753 | informativo |  | principal | 1 |  | 400 |
| shap_grupos | ALE | ALE de c vs sin(2c) centrado | correlación | 0,950 | >= 0.9 | sí | referencia | 1 |  | 400 |
| umbral_hansen | wild | H0_iid (errores sin autocorrelación) | tamaño (rechazo al 5%) | 0,043 | [0,02; 0,10] | sí | principal | 300 | 299.0 | 120 |
| umbral_hansen | wild | H0_heterocedastico (errores sin autocorrelación) | tamaño (rechazo al 5%) | 0,040 | [0,02; 0,10] | sí | principal | 300 | 299.0 | 120 |
| umbral_hansen | wild | H1_salto_pendiente (errores sin autocorrelación) | potencia (rechazo al 5%) | 0,890 | >= 0,80 | sí | principal | 300 | 299.0 | 120 |
| umbral_hansen | IC_LR | H1_salto_pendiente (errores sin autocorrelación) | cobertura IC95 del umbral por inversión de LR | 0,937 | [0,90; 0,98] | sí | principal | 300 | 299.0 | 120 |
| umbral_hansen | IC_LR | H1_salto_pendiente (errores sin autocorrelación) | sesgo mediano del umbral | -0,013 | < 0.15 | sí | principal | 300 | 299.0 | 120 |
| umbral_hansen | wild | H0 / errores AR(0.5), q AR(0,9) | tamaño (rechazo al 5%) | 0,170 | [0,02; 0,10] | NO | referencia | 300 | 299.0 | 100 |
| umbral_hansen | bloque_pw | H0 / errores AR(0.5), q AR(0,9) | tamaño (rechazo al 5%) | 0,070 | [0,02; 0,10] | sí | principal | 300 | 299.0 | 100 |
| umbral_hansen | sieve | H0 / errores AR(0.5), q AR(0,9) | tamaño (rechazo al 5%) | 0,033 | [0,02; 0,10] | sí | principal | 300 | 299.0 | 100 |
| umbral_hansen | wild | H0 / errores AR(0.5), q AR(0,9) | tamaño (rechazo al 5%) | 0,153 | [0,02; 0,10] | NO | referencia | 300 | 299.0 | 126 |
| umbral_hansen | bloque_pw | H0 / errores AR(0.5), q AR(0,9) | tamaño (rechazo al 5%) | 0,067 | [0,02; 0,10] | sí | principal | 300 | 299.0 | 126 |
| umbral_hansen | sieve | H0 / errores AR(0.5), q AR(0,9) | tamaño (rechazo al 5%) | 0,037 | [0,02; 0,10] | sí | principal | 300 | 299.0 | 126 |
| umbral_hansen | wild | H0 / errores AR(0.85), q AR(0,9) | tamaño (rechazo al 5%) | 0,510 | [0,02; 0,10] | NO | referencia | 300 | 299.0 | 110 |
| umbral_hansen | bloque_pw | H0 / errores AR(0.85), q AR(0,9) | tamaño (rechazo al 5%) | 0,157 | [0,02; 0,10] | NO | principal | 300 | 299.0 | 110 |
| umbral_hansen | sieve | H0 / errores AR(0.85), q AR(0,9) | tamaño (rechazo al 5%) | 0,077 | [0,02; 0,10] | sí | principal | 300 | 299.0 | 110 |
| umbral_hansen | bloque_pw | H1 salto 0.8 / errores AR(0.5), q AR(0,9) | potencia (rechazo al 5%) | 0,663 | >= 0,80 | NO | principal | 300 | 299.0 | 100 |
| umbral_hansen | IC_LR | H1 salto 0.8 / errores AR(0.5), q AR(0,9) / boot=bloque | cobertura IC95 del umbral por inversión de LR | 0,900 | [0,90; 0,98] | sí | referencia | 300 | 299.0 | 100 |
| umbral_hansen | sieve | H1 salto 0.8 / errores AR(0.5), q AR(0,9) | potencia (rechazo al 5%) | 0,587 | >= 0,80 | NO | principal | 300 | 299.0 | 100 |
| umbral_hansen | IC_LR | H1 salto 0.8 / errores AR(0.5), q AR(0,9) / boot=sieve | cobertura IC95 del umbral por inversión de LR | 0,900 | [0,90; 0,98] | sí | principal | 300 | 299.0 | 100 |
| umbral_hansen | bloque_pw | H1 salto 0.8 / errores AR(0.5), q AR(0,9) | potencia (rechazo al 5%) | 0,803 | >= 0,80 | sí | principal | 300 | 299.0 | 126 |
| umbral_hansen | IC_LR | H1 salto 0.8 / errores AR(0.5), q AR(0,9) / boot=bloque | cobertura IC95 del umbral por inversión de LR | 0,913 | [0,90; 0,98] | sí | referencia | 300 | 299.0 | 126 |
| umbral_hansen | sieve | H1 salto 0.8 / errores AR(0.5), q AR(0,9) | potencia (rechazo al 5%) | 0,737 | >= 0,80 | NO | principal | 300 | 299.0 | 126 |
| umbral_hansen | IC_LR | H1 salto 0.8 / errores AR(0.5), q AR(0,9) / boot=sieve | cobertura IC95 del umbral por inversión de LR | 0,913 | [0,90; 0,98] | sí | principal | 300 | 299.0 | 126 |

## Notas y límites

- Con R réplicas el error de Monte Carlo del tamaño nominal 5 % es ±1,96·sqrt(0,05·0,95/R): ±0,027 con R=250, ±0,031 con R=200, ±0,043 con R=100; con R<=30 las cifras de MS son orientativas.
- Bai-Perron: el bootstrap `wild` no corrige autocorrelación (sobre-rechaza); `bloque_pw` (Politis-White) elige bloques cortos y deja tamaño inflado; `sieve` (AR por BIC sobre los residuos de la nula) es la configuración con tamaño más cercano al nominal y sacrifica potencia con persistencia alta. Una variante que estima el AR sobre los residuos del mejor modelo con un corte se probó en un piloto (tamaño 0,13-0,21 con R=300) y se descartó.
- Umbral de Hansen: el IC del umbral por inversión de la LR es homocedástico y no se corrige por autocorrelación; su cobertura se informa aparte (config. IC_LR).
- Permutación de fechas: validez aproximada (no exacta); con 5 tramos no contiguos el contraste resulta conservador y de potencia baja (ver filas).
- Markov switching: el bootstrap paramétrico es costoso (cada réplica reajusta k0 y k1); el contraste 2 vs 3 solo se probó con R muy pequeño y es NO concluyente. Y3/desviaciones: k por BIC.
- LP-IV: el p-valor AR unilateral usa el signo de la primera etapa estimada (válido si el signo se da por conocido).
- Ninguna herramienta se ha estimado con datos reales. Predicción != causalidad (SHAP, ALE, dominancia son descriptivos).

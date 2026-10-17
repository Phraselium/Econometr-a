# Auditoría V16 fase 1: demanda_internacional (C4, descriptivo)

Script: `src/v16/auditoria/demanda_internacional.py` (SEED=20261010). Detalle en `resultado.json`. EA-MPD (terceros) solo para contar fechas.

## 1. Tipos del BdE por periodo de fijación
- **Coherencia interna**: be1903 y be1904 (TEDR total) coinciden salvo redondeo (máx. 0,0045 pp, 284 meses 2003-01 a 2026-08). La TEDR total del parquet coincide con `DN_1TI2T0135` de `data/raw/bde_tipos_hipotecas_nuevas.csv` (dif. 0). La media de los cuatro tramos ponderada por importes reproduce el total (dif. máx. 0,004 pp). La suma de importes por tramo es 99,0-100,1 % del total be1911; be1911 y be1912 difieren como mucho 25 M€.
- **Frente al BCE (MIR, AAR hogares vivienda, España)**: TEDR BdE vs BCE: corr. niveles 0,9996, diferencia media +0,008 pp, máxima 0,155 pp; variaciones interanuales corr. 0,999, sin ventanas de signo opuesto. TAE BdE vs MIR: media +0,163 pp (la TAE incluye comisiones, diferencia esperable), corr. 0,997, sin divergencias de signo. Total frente a «excluidas renegociaciones» (2014-12 en adelante): máx. 0,13 pp, sin ventanas de signo opuesto.
- **Atípicos (|z robusto|>5 en variación mensual)**: total, BCE y TAE: enero-marzo de 2009 (caída de Euribor, real). Tramo «más de 10 años»: 26 meses, con máximos en 2012-09, 2013-03 y 2015-01 que coinciden con volúmenes de 9-41 M€ (0,5-1,7 % del importe): ruido de muestra pequeña, no error. «Hasta 1 año» pasa de 79 % del importe (2003) y 91 % (2008) a 8 % (2025): cualquier uso como proxy de variable cambia de significado en el tiempo (deriva composicional).
- Sin huecos mensuales; sin NaN en los tramos.

## 2. Índices de precios, España (tasas interanuales)
- OCDE HPI vs Eurostat TOTAL: corr. 0,9999, dif. media -0,004 pp, máx. 0,36 pp (2006-Q4). Prácticamente idénticas: **no son fuentes independientes** (el nivel 2015 es 100 en ambas). Vs Eurostat existentes (DW_EXST): corr. 0,986, +0,72 pp de media, 7 trimestres con |dif|>3 pp. Vs nuevas (DW_NEW): corr. 0,948, -1,48 pp, 23 trimestres con |dif|>3 pp y una ventana de signo opuesto (2008-Q2 a 2008-Q4).
- OCDE vs BIS nominal: corr. 0,996, mediana de |dif| 0,08 pp, máx. 3,6 pp (2006-Q2), sin ventanas de signo opuesto. BIS termina en 2026-Q1; OCDE y Eurostat en 2026-Q2.
- Tasas publicadas frente a recalculadas: Eurostat máx. 0,06 pp, BIS 0,00 pp. La nueva descarga OCDE reproduce el fichero antiguo de `data/raw/oecd_house_prices.csv` (106 trimestres, dif. 0): no hay revisión entre vintages. Sin atípicos robustos en OCDE HPI.

## 3. Choques J-K
Los mensuales (`_m`) son exactamente la suma de los diarios (`_d`) del mes en las seis variables (pc1, STOXX50, MP/CBI pm y mediana; 322 meses, dif. máx. 0,0; 0 meses sin reunión con valor distinto de 0). La identidad MP+CBI=pc1 se cumple en el diario (dif. 0). Hasta 3 reuniones por mes; usar la media en vez de la suma cambia hasta 0,11 (pc1) por mes: debe fijarse la agregación. Los nombres de columnas difieren entre ficheros (`pc1_hf`, `STOXX50_hf` en el mensual). 18 reuniones con |z|>5 (p. ej. 2001-05-10, 2008-11-06, 2023-03-16; son recortes o subidas conocidos, no error). Las 312 fechas del JK diario están en EA-MPD (902 fechas, que incluye no-reuniones).

Limitaciones: la TEDR y los precios no se contrastan con una fuente totalmente independiente (OCDE=Eurostat). Nivel de evidencia: DESCRIPTIVO.

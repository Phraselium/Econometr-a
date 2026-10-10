# M0 · Conciliación de las cifras de déficit 2021-2025 (capas C1 y C2)

Déficit contable = Δ hogares − viviendas terminadas (flujo acumulado desde 2021, no un déficit en niveles). Fuentes: output/informe.md (v1), output/v3/PA/tablas (A1), docs/v3/literatura_v3.md. Sin datos nuevos.

## Cifras

| id | fuente de hogares | medida de hogares | oferta | bajas | periodo | cifra |
|---|---|---|---|---|---|---|
| v1_epa | EPA | media trimestral, EPA corregida del quiebre 2021T1 | fin de obra libres MIVAU (sin protegida) | no (0) | 2021T1 a 2025T4 | 866.100 |
| v1_ecp | ECP | stock a 1 de enero (1-ene-2026 menos 1-ene-2021) | fin de obra libres MIVAU (sin protegida) | no (0) | 2021-01-01 a 2026-01-01 | 810.936 |
| v1_parque | EPA | media trimestral, EPA corregida | variación del parque MIVAU (neta) | implícitas en el parque (netas) | 2021 a 2025 | 802.152 |
| v3_ecp_ref | Censo 2021 + ECP | media trimestral 2021T1-2025T4 (sin quiebre: anclada al censo) | fin de obra libres + protegida (calif. definitivas) | no (0) | 2021T1 a 2025T4 | 700.934 |
| v3_mediana | EPA sin corregir y Censo+ECP | media trimestral | las 14 combinaciones (con/sin protegida, bajas 0/0,1/0,2 %, Δparque) | 0 a 0,2 % anual del parque | 2021T1 a 2025T4 | 701.187 |
| v3_min | EPA sin corregir | media trimestral, sin corregir quiebre | variación del parque MIVAU (neta) | implícitas en el parque | 2021T1 a 2025T4 | 559.752 |
| v3_max | Censo 2021 + ECP | media trimestral | fin de obra libres + protegida | 0,2 % anual del parque | 2021T1 a 2025T4 | 969.059 |
| bde_ia | no nombrada (inferencia: ECP) | no declarada | terminadas (no declara si incluye protegida) | no declaradas | 2021 a 2025 | 750.000 |
| bde_ief | no nombrada | no declarada | terminadas | no declaradas | 2021 a 1S 2025 (inferencia) | 700.000 |

## Descomposición aditiva (v1 principal a referencia v3 y BdE)

| paso | Δ déficit | nivel | componente |
|---|---|---|---|
| v1 principal (EPA corregida, libres) | 866.100 | 866.100 | nan |
| fuente de hogares: EPA corregida -> ECP (ambas con stock 1 de enero) | -55.164 | 810.936 | hogares |
| medida de hogares: stock 1 de enero -> media trimestral 2021T1-2025T4 | -53.679 | 757.257 | hogares/fechas |
| protegida: añadir calificaciones definitivas (no incluidas en v1) | -56.323 | 700.934 | protegida |
| bajas del parque (v1 y referencia v3: 0) | 0 | 700.934 | bajas |
| periodo (ambos 2021-2025) | 0 | 700.934 | periodo |
| v1 principal -> v1 ECP | -55.164 | 810.936 | hogares |
| v1 principal -> v1 Δparque (protegida 56.323 + residual neto de bajas −7.625) | -63.948 | 802.152 | protegida y bajas |
| quiebre EPA 2021T1 (corregida -> sin corregir) | -242.400 | 623.700 | hogares (corrección) |
| referencia v3 -> BdE IA (residuo no atribuible) | 49.066 | 750.000 | residuo/redondeo/no declarado |
| BdE IA -> BdE IEF (periodo hasta 1S 2025: inferencia) | -50.000 | 700.000 | periodo (no verificable) |
| sensibilidad: bajas +0,1 % anual del parque | 134.063 |  | bajas |

## Lectura
- De 866.100 (v1) a 700.934 (referencia v3) hay −165.166: hogares −55.164 (fuente), −53.679 (medida: stock 1 de enero frente a media trimestral), protegida −56.323; bajas y periodo 0 por construcción. La suma cierra exacta.
- La protegida medida con calificaciones definitivas de MIVAU (56.323) es coherente con el residuo de 60.936 que v1 atribuyó a la protegida (diferencia de 4.613; v1 lo obtuvo como BdE implícito menos terminadas).
- La única fuente con efecto grande no resuelto es la corrección del quiebre EPA 2021T1 (242.400): con ella 866.100, sin ella 623.700. Es una elección de medida, no un dato.
- Las bajas del parque no están medidas: cada 0,1 % anual del parque suma 134.063 al déficit. Es la mayor incertidumbre de v3 (rango 559.752-969.059) y no la reduce ninguna fuente disponible.
- Frente al BdE (≈750.000): la referencia v3 queda 49.066 por debajo y v1 116.100 por encima. El BdE no declara fuente de hogares, protegida ni bajas, así que ese residuo no se puede descomponer; la fuente de hogares ECP es inferencia. 700.000 (IEF) es compatible en signo con un periodo más corto, sin verificar.
- Conclusión: las cifras 700.000-866.100 difieren por la medida de hogares (≈109.000) y la protegida (≈56.000), no por el periodo. El déficit en niveles, con bajas, queda en el rango de v3 (C2). La cifra del BdE es una referencia externa NO VERIFICADA en su método.

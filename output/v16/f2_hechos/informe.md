# V16 · Fase 2.1 · Hechos actualizados (informe)

Generado por `python3 src/v16/f2_hechos.py`. Sin estimar efectos y sin lectura causal. Cifras en `hechos.json`; una ficha por cifra en `fichas.md`.

## 1. Resumen

- **56 cifras:** 3 en C1, 0 en C2 y 53 en C4. No hay C2: ningún hecho de esta fase es una cota con supuestos explícitos (Manski).
- **Regla de capa.** C1 solo con al menos dos fuentes de grupos distintos (misma fuente primaria = un grupo) cuyas cifras coinciden dentro de una tolerancia fijada antes de mirar las parejas nuevas: ±3.0 p.p. en cambios acumulados y ±15% en recuentos. Es la vara de las 11 bajadas de `docs/v15/bajadas_capa.csv`.
- **Grupos.** IPV del INE y Notariado: notarial. MIVAU valor tasado: tasación. Registradores: registral. IPC alquiler: encuesta INE. IPVA y SERPAVI: AEAT-IRPF (un grupo). Fianzas Incasòl y GVA: un grupo cada una. OCDE, Eurostat y BIS para el precio de España: derivados del IPV del INE (K6).
- **Controles con la 1.0.** El cambio 2015-2025 reproduce A23-P1 (79,9) y los extremos de A23-P2 (44,2; 47,2; 56,1); el IPVA nuevo y las fianzas 2021-2024 caen dentro de los rangos de A23-A9 y A23-A10; el aumento de hogares ECP reproduce el extremo inferior de dh_2125. Discrepancias: ver `discrepancias.md`.

## 2. Cifras C1

| id | indicador | valor | rango entre fuentes | capa |
|---|---|---|---|---|
| V16-HEC-PRECIO-NOM-2019-2025 | Precio de compra, cambio acumulado nominales 2019-2025 (media anual), España; medida: precio medio por m² sin ajuste de calidad (MIVAU valor tasado, Notariado, Registradores); el IPV del INE, ajustado por calidad, da 44.4 % | 30.351 | 29.635 a 31.702 | C1 |
| V16-HEC-PRECIO-REAL-2019-2025 | Precio de compra, cambio acumulado reales (deflactor IPC general) 2019-2025 (media anual), España; medida: precio medio por m² sin ajuste de calidad (MIVAU valor tasado, Notariado, Registradores); el IPV del INE, ajustado por calidad, da 18.7 % | 7.123 | 6.534 a 8.232 | C1 |
| V16-HEC-ALQ-BRECHA-2124-CAT | Brecha de crecimiento contratos nuevos menos vigentes 2021-2024, Cataluña | 10.785 | 9.718 a 11.852 | C1 |

## 3. Lectura por tema

- **Precios de compra.** En términos reales (IPC general) 2019-2025 el cambio es 6.534 a 8.232 % según la medida (C1); 2013-2025, 12.972 a 48.388 % (C4); 2007-2025, -31.253 a -15.693 % (C4). Las medidas notarial (IPV), de tasación y registral difieren en la cuantía en varias ventanas: se publican todas y, si no coinciden, no se elige una. Por CCAA, `precios_ccaa.csv` (el deflactor es nacional: no hay IPC autonómico en el repositorio).
- **Alquiler.** El IPC de alquiler (stock) llega a 2025; IPVA y SERPAVI acaban en 2024, así que en 2025 no hay segunda fuente (C4). Las brechas nuevo/vigente 2021-2024 se calculan con dos estimaciones independientes (IPVA frente a fianzas menos IPC) en Cataluña y la Comunitat Valenciana; solo Cataluña supera la vara. IPVA y SERPAVI comparten fuente primaria. Inside Airbnb queda fuera (turístico).
- **Parque y vacías.** La tabla 59531 (vacías y uso esporádico por consumo eléctrico) es una tabla del propio Censo 2021 con el mismo universo de viviendas: las «vacías del Censo» y las «vacías por consumo» son la misma cifra, no dos fuentes (C4). El Catastro y el Censo difieren en -5.23 % en el territorio común, pero se mantiene C4 por no estar demostrada la independencia. Nivel nacional y CCAA (`parque_ccaa.csv`); lo municipal queda para el atlas (fase 3) con el filtro de la muestra sellada v6.
- **Obra nueva frente a hogares.** Libres terminadas MIVAU 2021-2025 y hogares ECP: ampliación a 2025 con ids nuevos; no sustituye a terminadas_1924 ni a dh_2125. Las terminadas de la 1.0 incluyen protegidas en V12; aquí solo libres.
- **Vivienda pública por habitante frente a la UE.** Vivienda pública por habitante frente a la UE: no hay dato descargado (OCDE Affordable Housing Database, PH4.2). Se deja la cifra pendiente en tareas del autor; no se estima ni se aproxima con otra fuente.
- **Lanzamientos (CGPJ).** Una sola fuente: C4. Serie nacional y por TSJ (`lanzamientos_ccaa.csv`); agregado propio, la serie no se redistribuye (terceros_1_0: agregados). El total nacional es el de los TSJ, no la suma de provincias, para no depender de la muestra sellada.
- **Comparación internacional.** España frente a la mediana UE y OCDE en precio real, precio/alquiler y precio/renta (OCDE) y sobrecarga (Eurostat ECV): C4, porque no hay segunda fuente independiente para España.

## 4. Límites

- Medias anuales de 4 trimestres; el último año es 2025. Los cambios 2007, 2013 y 2019 usan la misma metodología que la 1.0.
- Registradores: agregado propio de datos abiertos (ODbL); Notariado: agregado propio. No se publican las series.
- Sin pruebas de hipótesis: el control de falsos descubrimientos (Holm o BH) no se aplica; cada cifra va al Registry (`registro.csv`).

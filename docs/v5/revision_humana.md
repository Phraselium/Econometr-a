# Revisión humana de las cifras más citables (v5, E9)

Las 15 cifras de output/v5/cifras_clave.csv con más marcadores en las plantillas de docs/v5/plantillas (recuento de usos, octubre de 2026). Para cada una: valor renderizado, capa, script y línea que la produce, fichero de salida, comando de réplica y casilla para el autor. Tras cualquier réplica se ejecuta `python3 src/v5/cifras_clave.py && python3 src/v5/render.py`. <!-- check:cifra-libre -->

Nota: B4-v3-vut-cantidad tiene su valor escrito en el script de v5 a partir de una tabla de v3; conviene comprobarlo contra `output/v3/PB/tablas/b2_nacional_sensibilidad.csv`.

## 1. A23-A2

- **Indicador:** Alquiler stock 2015-2024: núcleo IPC de alquiler e IPVA (contratos existentes y total; tolerancia ±15 % en nivel)
- **Valor renderizado:** — % (10,9-22,9 %) (2015-2024)
- **Capa:** C1
- **Script y línea:** `src/v5/a23_run.py:567`
- **Origen registrado en cifras_clave:** `output/v5/A23/hechos.json:A23-A2`
- **Fichero de salida:** `output/v5/A23/hechos.json`
- **Comando:** `python3 src/v5/a23_run.py`
- **Replicado por el autor (fecha, firma):** ☐ ____________________

## 2. terminadas_1924

- **Indicador:** Viviendas terminadas al año (territorio común: sin País Vasco ni Navarra)
- **Valor renderizado:** — viviendas/año (72.264-94.426 viviendas/año) (2019-2024)
- **Capa:** C1
- **Script y línea:** `src/v5/cifras_clave.py:42`
- **Origen registrado en cifras_clave:** `output/v4/M0/terminadas_triangulacion.csv:comun_mivau_bruto_sin_PV_NA`
- **Script de origen (adaptador de v4/v3):** `src/v4/m0_run.py:181` (columna comun_mivau_bruto_sin_PV_NA → output/v4/M0/terminadas_triangulacion.csv)
- **Fichero de salida:** `output/v5/cifras_clave.csv`
- **Comando:** `python3 src/v4/m0_run.py && python3 src/v5/cifras_clave.py`
- **Replicado por el autor (fecha, firma):** ☐ ____________________

## 3. deficit_2124_c1

- **Indicador:** Déficit acumulado: aumento de hogares menos viviendas terminadas, sin bajas
- **Valor renderizado:** — viviendas (562.692-688.692 viviendas) (2021-2024)
- **Capa:** C1
- **Script y línea:** `src/v5/cifras_clave.py:28`
- **Origen registrado en cifras_clave:** `output/v4/M0/resultado.json:deficit_2021_2024.c1_sin_bajas`
- **Script de origen (adaptador de v4/v3):** `src/v4/m0_run.py:367` (c1_sin_bajas, en deficit_2021_2024, línea 326 → output/v4/M0/resultado.json)
- **Fichero de salida:** `output/v5/cifras_clave.csv`
- **Comando:** `python3 src/v4/m0_run.py && python3 src/v5/cifras_clave.py`
- **Replicado por el autor (fecha, firma):** ☐ ____________________

## 4. deficit_2124_c2

- **Indicador:** Déficit acumulado con bajas del parque supuestas del 0,1-0,2 % anual (cota)
- **Valor renderizado:** — viviendas (562.692-902.808 viviendas) (2021-2024)
- **Capa:** C2
- **Script y línea:** `src/v5/cifras_clave.py:33`
- **Origen registrado en cifras_clave:** `output/v4/M0/resultado.json:deficit_2021_2024.c2_con_bajas`
- **Script de origen (adaptador de v4/v3):** `src/v4/m0_run.py:367` (c2_con_bajas → output/v4/M0/resultado.json)
- **Fichero de salida:** `output/v5/cifras_clave.csv`
- **Comando:** `python3 src/v4/m0_run.py && python3 src/v5/cifras_clave.py`
- **Replicado por el autor (fecha, firma):** ☐ ____________________

## 5. dh_2125

- **Indicador:** Aumento del número de hogares
- **Valor renderizado:** 997.586 hogares (981.823-1.013.350 hogares) (2021-2025)
- **Capa:** C1
- **Script y línea:** `src/v5/cifras_clave.py:38`
- **Origen registrado en cifras_clave:** `output/v4/M2/hechos.json:M2-H0`
- **Script de origen (adaptador de v4/v3):** `src/v4/m2_run.py:348` (M2-H0 → output/v4/M2/hechos.json)
- **Fichero de salida:** `output/v5/cifras_clave.csv`
- **Comando:** `python3 src/v4/m2_run.py && python3 src/v5/cifras_clave.py`
- **Replicado por el autor (fecha, firma):** ☐ ____________________

## 6. D1-H11

- **Indicador:** Parte de una ayuda general que se traslada al precio, clase A4 1 (método A)
- **Valor renderizado:** 58,4 % (27,8-81,8 %) (rejilla εd 0,3-1,5)
- **Capa:** C4
- **Script y línea:** `src/v5/d1_run.py:234`
- **Origen registrado en cifras_clave:** `output/v5/D1/hechos.json:D1-H11`
- **Fichero de salida:** `output/v5/D1/hechos.json`
- **Comando:** `python3 src/v5/d1_run.py`
- **Replicado por el autor (fecha, firma):** ☐ ____________________

## 7. A23-P2

- **Indicador:** Precio de compra, núcleo MIVAU/Notariado/Registradores 2015-2025
- **Valor renderizado:** 47,2 % (44,2-56,1 %) (2015-2025 (media anual))
- **Capa:** C1
- **Script y línea:** `src/v5/a23_run.py:552`
- **Origen registrado en cifras_clave:** `output/v5/A23/hechos.json:A23-P2`
- **Fichero de salida:** `output/v5/A23/hechos.json`
- **Comando:** `python3 src/v5/a23_run.py`
- **Replicado por el autor (fecha, firma):** ☐ ____________________

## 8. B4-v3-vut-cantidad

- **Indicador:** Máximo de stock de alquiler desplazado por viviendas turísticas
- **Valor renderizado:** 2,7 % del stock de alquiler (2,4-2,7 % del stock de alquiler) (2020M08-2024M08)
- **Capa:** C2
- **Script y línea:** `src/v5/b4_run.py:310` (valor fijado en el script, tomado de v3: revisar)
- **Origen registrado en cifras_clave:** `output/v5/B4/hechos.json:B4-v3-vut-cantidad`
- **Script de origen (adaptador de v4/v3):** `src/v3/pb_run.py:379` (output/v3/PB/tablas/b2_nacional_sensibilidad.csv; heredado de v3, no de v4)
- **Fichero de salida:** `output/v5/B4/hechos.json`
- **Comando:** `python3 src/v3/pb_run.py && python3 src/v5/b4_run.py`
- **Replicado por el autor (fecha, firma):** ☐ ____________________

## 9. D1-H12

- **Indicador:** Parte de una ayuda general que se traslada al precio, clase A4 2 (método A)
- **Valor renderizado:** 100,0 % (88,1-100,0 %) (rejilla εd 0,3-1,5)
- **Capa:** C4
- **Script y línea:** `src/v5/d1_run.py:234` (bucle por clase, c=2)
- **Origen registrado en cifras_clave:** `output/v5/D1/hechos.json:D1-H12`
- **Fichero de salida:** `output/v5/D1/hechos.json`
- **Comando:** `python3 src/v5/d1_run.py`
- **Replicado por el autor (fecha, firma):** ☐ ____________________

## 10. A23-A10

- **Indicador:** Contratos nuevos Comunitat Valenciana 2021-2024: IPVA nuevo y fianzas GVA
- **Valor renderizado:** 26,6 % (22,4-30,8 %) (2021-2024)
- **Capa:** C1
- **Script y línea:** `src/v5/a23_run.py:597`
- **Origen registrado en cifras_clave:** `output/v5/A23/hechos.json:A23-A10`
- **Fichero de salida:** `output/v5/A23/hechos.json`
- **Comando:** `python3 src/v5/a23_run.py`
- **Replicado por el autor (fecha, firma):** ☐ ____________________

## 11. E-B1-F

- **Indicador:** Crecimiento de hogares proyectado (componente F, 10 años)
- **Valor renderizado:** 1.720.540 viviendas (1.308.530-1.772.410 viviendas) (2026-2035)
- **Capa:** C2
- **Script y línea:** `src/v5/e_hechos_e2.py:38` (fila F de la lista de la línea 33)
- **Origen registrado en cifras_clave:** `output/v5/E/hechos.json:E-B1-F`
- **Fichero de salida:** `output/v5/E/hechos.json`
- **Comando:** `python3 src/v5/b1_run.py && python3 src/v5/e_hechos.py && python3 src/v5/cifras_clave.py`
- **Replicado por el autor (fecha, firma):** ☐ ____________________

## 12. latente_convivencia

- **Indicador:** Demanda latente de jóvenes por convivencia con los padres (frente a 2008)
- **Valor renderizado:** — hogares (188.000-506.000 hogares) (2008-2025)
- **Capa:** C2
- **Script y línea:** `src/v5/cifras_clave.py:50`
- **Origen registrado en cifras_clave:** `output/v4/M2/hechos.json:M2-C1 (magnitud, «convivencia con padres»)`
- **Script de origen (adaptador de v4/v3):** `src/v4/m2_run.py:374` (M2-C1 → output/v4/M2/hechos.json)
- **Fichero de salida:** `output/v5/cifras_clave.csv`
- **Comando:** `python3 src/v4/m2_run.py && python3 src/v5/cifras_clave.py`
- **Replicado por el autor (fecha, firma):** ☐ ____________________

## 13. B1-H1

- **Indicador:** Necesidad total de vivienda por año (A+R+V+F-M-K), suma de 52 provincias
- **Valor renderizado:** 214.868 viviendas/año (93.628-309.921 viviendas/año) (2026-2035)
- **Capa:** C4
- **Script y línea:** `src/v5/b1_run.py:433`
- **Origen registrado en cifras_clave:** `output/v5/B1/hechos.json:B1-H1`
- **Fichero de salida:** `output/v5/B1/hechos.json`
- **Comando:** `python3 src/v5/b1_run.py`
- **Replicado por el autor (fecha, firma):** ☐ ____________________

## 14. B1-H4

- **Indicador:** Crecimiento de hogares proyectado (INE, 10 años)
- **Valor renderizado:** 1.720.540 hogares (1.308.530-1.772.410 hogares) (2026-2035)
- **Capa:** C2
- **Script y línea:** `src/v5/b1_run.py:439`
- **Origen registrado en cifras_clave:** `output/v5/B1/hechos.json:B1-H4`
- **Fichero de salida:** `output/v5/B1/hechos.json`
- **Comando:** `python3 src/v5/b1_run.py`
- **Replicado por el autor (fecha, firma):** ☐ ____________________

## 15. R1C-001

- **Indicador:** Hogares con vivienda principal en propiedad
- **Valor renderizado:** 74,5 % de hogares (72,1-75,9 % de hogares) (2021-2022)
- **Capa:** C1
- **Script y línea:** `src/v5/r1c_run.py:130`
- **Origen registrado en cifras_clave:** `output/v5/R1C/hechos.json:R1C-001`
- **Fichero de salida:** `output/v5/R1C/hechos.json`
- **Comando:** `python3 src/v5/r1c_run.py`
- **Replicado por el autor (fecha, firma):** ☐ ____________________

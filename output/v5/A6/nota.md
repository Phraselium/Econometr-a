# A6 · Topes fuera de C3 y no replicación de García-López (consolidación de v4)

## Topes al alquiler (H3-3): fuera de C3 de forma definitiva
- **Motivo: contaminación de la validación.**
  - El cálculo de potencia de v3 usó municipios que luego quedaron en la muestra sellada.
  - La validación por fuente (SERPAVI) mide el mismo mercado en los mismos municipios.
  - Por eso no es una prueba independiente (docs/v4/decisiones.md, M0).
- **Estado.**
  - Las estimaciones de v3 (−5,4 % de renta en Cataluña 2020-2022; contratos −4,9 % [−9,9; +0,5]) se reportan como C4.
  - Ninguna ficha del verificador ni ningún entregable las presenta como C3. Las fichas V06 y V07 lo dicen.
  - `src/v5/check_v5.py` comprueba que ningún texto asocie «topes» a C3.

## García-López et al. (2020): por qué no se replica
Fuente: output/v4/M0/gl_no_replica.md.

| Fuente de la discrepancia | García-López | Réplica propia | Cuantificable |
|---|---|---|---|
| Datos de alquiler | Precio de oferta (flujo) | SERPAVI, stock de contratos | Sí: el stock recoge el 55-75 % de la variación del flujo (Barcelona) |
| Datos de turismo | Anuncios de Airbnb | VUT del INE (unidades) | Parcial: razón VUT/anuncios 0,11-0,42 (2025) |
| Periodo | 2012-2016 | 2021-2024 | No: el VUT del INE no existe antes de 2021 |
| Método | Variable instrumental | Efectos fijos sin instrumento | No: falta el instrumento |

**Resultado**
- La estimación propia (−0,0042; IC95 [−0,0078; −0,0005]; p Holm 0,27) no es distinguible de 0 tras Holm.
- La atenuación de stock frente a flujo explica una magnitud menor, pero no un signo negativo.
- El periodo y el método no se pueden contrastar con los datos disponibles.

**Capa: C4.** No se afirma que el resultado de García-López esté refutado ni confirmado para España en 2021-2024.

**Qué falta:** la serie VUT/anuncios de 2012-2016 y un instrumento (backlog).

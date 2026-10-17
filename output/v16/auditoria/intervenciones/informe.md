# Auditoría V16 fase 1: intervenciones (C4, descriptivo)

Script: `src/v16/auditoria/intervenciones.py`. Entrada: `output/v16/f1/intervenciones.csv` (476 filas: 158 propias + 318 zonas tensionadas). Salidas: `resultado.json` y `prioridad_verificacion.csv` (108 filas SECUNDARIA o NO VERIFICADA con puntuación explícita; es un criterio de orden de trabajo).

## Hallazgos
1. **Lectura del código INE.** `cod_ine` debe leerse como texto: con `pandas.read_csv` por defecto, «01» pasa a 1 (columna int64) y los cruces por código INE fallan. La longitud es coherente con el ámbito en las 476 filas (estatal «00», CCAA 2 dígitos, municipio 5).
2. **Solapes y huecos de tramos (ITP, AJD, 105 filas).** Ninguno: sin solapes ni huecos de días en ninguna serie de las 15 CCAA de régimen común (más Navarra y País Vasco como fila «foral» sin tipo numérico). Cobertura 2010-01-01 a 2026 completa para AJD y para el tipo general/mínimo de ITP en todas. El tipo máximo del ITP solo existe en los periodos con escala (p. ej. Cataluña desde 2017, Aragón desde 2016, Cantabria hasta 2018); no es un hueco. Hay 11 pares de tramos consecutivos con igual valor (Baleares 5, Cantabria 2, Cataluña 2, C. Valenciana, Extremadura): particiones por edición o escala, inocuas pero conviene fusionarlas o marcarlas si se usan para contar «cambios de tipo».
3. **Fechas de efecto aproximadas.** 85 de 105 filas fiscales llevan efecto el 1 de enero y 78 lo declaran «aproximada» (primera edición que recoge el valor): el cambio real puede estar hasta 12 meses antes. Cualquier diseño de evento sobre ITP/AJD debe tratar esas fechas como intervalo, no como instante. Ninguna fila fiscal tiene fecha de publicación.
4. **Efecto frente a publicación.** Sin `fecha_fin` anterior al efecto; ningún efecto posterior al 2026-10-17. Efecto anterior a la publicación en 4 filas: VUT-BAL-DL4-2025 (-89 días), VUT-CAN-L6-2025 (-10), VUT-CAT-DL3-2023 (-57), que sugieren que la publicación recogida es la de la convalidación o el texto refundido y no la inicial; y VP-ENTREGA-CD-2024 (-550, dato anual publicado después, esperable). Retrasos efecto-publicación >30 días: GOLDEN-LO1-2025 y su DT1 (+90), VUT-RD1312-2024 (+189) y TOPE-L12-2023-2024 (+221): son vacatio legis, correctos. Mediana 1 día.
5. **Zonas tensionadas (318).** Duración homogénea de 3 años, publicación a efecto <=1 día, sin solapes salvo Llanes (33036): dos declaraciones con la misma fecha 2026-07-30 (ids con sufijo «-2»); 317 municipios distintos. Revisar si son dos ámbitos distintos o un duplicado.
6. **Valores.** Sin AJD fuera de 0,25-2,5 %. ITP máximo >11 % en Baleares 2022-2023 y Cataluña 2025 (escalas progresivas; plausible, a contrastar con la ley).

## Prioridad para verificar (106 SECUNDARIA + 2 NO VERIFICADAS)
1. NO VERIFICADAS: VUT-MAD-RESIDE-2025 (nota de un despacho; BOCM sin consultar) y VUT-VAL-MORATORIA-2024 (sin fecha de publicación).
2. SECUNDARIA no fiscal: VUT-BCN-PEUAT-2017.
3. ITP/AJD en las CCAA con más compraventas y con cambio de tipo: Cataluña (AJD-09-2012, ITP-09-2017, ITP-09-2025 y su máximo), Madrid (AJD-13-2014, ITP-13-2014), Andalucía (AJD/ITP-01-2012), C. Valenciana (AJD-10-2012, ITP-10-2013 y 2023), Baleares (2013, 2016, 2022, 2023). Ordenación completa en `prioridad_verificacion.csv`.
4. Contrastar con la ley autonómica el día exacto de las 78 fechas aproximadas.

Nivel de evidencia: DESCRIPTIVO. No se estima ningún efecto.

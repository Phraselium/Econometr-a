# Estado v4

| Tarea | Oleada | Estado | Capa | Resultado principal | Tokens subagentes |
|---|---|---|---|---|---|
| Setup | 0 | hecho | — | — | 0 |
| M0 verificador (veredictos separados, convenciones A/B), topes fuera de C3 | A | hecho, corregido (A2, A7) | — | 14 fichas reclasificadas; convención B comparada con la subida observada | 0 (orquestador) |
| M0 conciliación, terminadas, GL | A | hecho, corregido (A6, A8, A9) | C1/C2/C4 | Cadena v1→v3 exacta; terminadas C1 2019-2024 (independencia parcial); GL no distinguible de 0 tras Holm | 93.084 |
| M2 descomposición de hogares | A | hecho, corregido | C1 (ΔH 2021-25)/C4/C2 | ΔH 2021-25 ≈ +1,01 M (ECP 982 mil; EPA corregida 1.013 mil); componente de nacionalidad extranjera 56-58 % (C4); latente 16-34 +23 mil (C2) | 98.619 |
| M1 geografía del déficit | A | hecho, corregido (bug A1) | C2 (13 prov.)/C4 | 2021-25: 701-967 mil (52 prov.); 7 provincias = 50 %; 19 = 80 %; sin excedentes provinciales | 102.671 |
| Revisión oleada A | A | REHACER → correcciones hechas | — | docs/v4/revision_oleadaA.md | 114.224 |
| M3 ¿se puede construir? | B | hecho (reejecutado con M1 corregido) | C4 | Coste en nivel sin fuente verificable → brecha y clases C4; solares del Catastro extraídos | 111.803 |
| M4 parque frente a mercado | B | hecho | C1/C4 | Compradores extranjeros 2025: MIVAU 16,9 %, Notariado 18,8 % (C1); personas jurídicas: 11,3 % compradores (C4, ETDP); titularidad del stock: sin datos | 128.323 |

| Revisión oleada B (REHACER → correcciones; it. 2 REHACER acotado → corregido) | B | APROBADA | — | reglas B4/B5; déficit 2021-24 C1 sin bajas 563-689 mil | 80.288 + 15.330 |
| M7 índice de precios triangulado y GSADF | B | hecho (C6 aplicado) | C1/C4 | Compra 2015-25: núcleo +44 % a +56 % (cuantía C1; INE IPV +80 %, discrepante); 2021-25 +24 % a +36 % (C1); alquiler 2015-24 dirección C1, cuantía C4; 2021-24 +6 % a +15 % (C1); 15/17 CCAA cuantía C1; GSADF C4 | 93.179 + 10.963 |
| M5a medidas por instrumento y literatura | C | parcial (pasada 2: 1 programa añadido por copia no oficial; 2 no accesibles) | — | 89 medidas (71 + 18), 27+2 instrumentos (I28, I29 nuevos), 5 VERIFICADA / 7 NO VERIFICADA; recuentos de tabla A pendientes | 245.499 + ~45.000 (pasada 2) |
| M6 preguntas abiertas y solicitudes | C | hecho | — | 10 preguntas; S3-S10 redactadas | 0 (orquestador) |

| M5a pasada 2 (programas adicionales) | C | hecho | — | 88 medidas, 9 documentos; 2 no accesibles | 86.270 |
| M5b matriz de instrumentos y fichas | C | hecho | C2/C4 | signo estable: construcción y vacías; débil: vivienda pública; no estable: topes, VUT y ayudas a la demanda (15-100 % al precio) | 0 (orquestador; M5 al 83 % del límite) |
| Entregables (WP, informe técnico, brief, lo_que_sabemos, README) | C | hecho (borrador) | — | — | 0 (orquestador) |
| Revisión oleada C | C | REHACER (14 cambios) → corregido; it. 2 REHACER acotado → corregido; APROBADA | — | docs/v4/revision_oleadaC.md, revision_oleadaC_it2.md | 147.305 + 47.741 |
| M5a corrección C2/C7/C8/C13 | C | hecho (C8 parcial: sin búsqueda por palabras clave; 11 instrumentos sin búsqueda bibliográfica) | — | columna `direccion`; I01 3 a favor / 3 en contra; 4 de 9 en copia no oficial; 7 referencias nuevas VERIFICADA | 62.904 |

**Hecho:** M0-M7; revisiones A, B y C aprobadas; entregables actualizados.
**Siguiente:** v4 CERRADA. `make all` ×2 sin red en clon limpio: rc=0 y md5 idénticos salvo tiempos.json. Pendiente externo: presentar las solicitudes S3-S10.
**Tokens de subagentes v4:** 1.475.500 / 2.500.000 (59 %; cierre al 80 %: 2.000.000). Por oleada: A 408.598; B 439.886 (incluye M7); C 589.719 (incluye M5a 394.673, el 99 % del límite del módulo); sin asignar a fila 37.297 (ya en el total previo).

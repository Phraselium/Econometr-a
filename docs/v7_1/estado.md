# Estado V7.1

## Hecho
- Rama r7.1/main creada desde r7/main (3d1170c). Plan escrito en docs/v7_1/plan.md.
- **S1 (dosis y coste).** src/v7_1/s1_dosis_coste.py reproduce las extracciones de R6, con una comprobación < 1e-3 frente a impactos.csv. Escribe output/v7_1/S1/{dosis_coste.csv, resumen.md, hechos.json (17 cifras), resultado.json}.
- **S1, entregables.** src/v7_1/s1_atlas.py escribe:
  - el atlas v7.1, con una sección 6 bis por CCAA;
  - el Excel con 3 hojas DC (azul, negro, verde, sin paneles inmovilizados);
  - el verificador v7.1 (V7-V2 con dosis y coste).
- **cifras_clave.** Incorpora V7 y V7.1 (W2); `make v7_1` añadido. `make check` en verde (tras ajustar test_k4a, W2), más tests/v7_1/test_s1.py.
- **S2.** Literatura verificada (lit-researcher): 0 referencias VERIFICADAS completas porque Scimago devolvió 403 (W6). Nota metodológica escrita como plantilla (docs/v5/plantillas/nota_metodologica.md), renderizada en output/v5/nota_metodologica.md (unas 4.350 palabras), con todas las cifras de resultado tomadas de cifras_clave (W7, W8).
- **S3 (cifras).** src/v7_1/s3_hechos.py lleva a cifras_clave el componente común, los recuentos de V7, el Monte Carlo y el precio de mercado de R6.

- **S3 (entregables).** Plantillas actualizadas: una_pagina, lo_que_sabemos, policy_brief, informe_tecnico, working_paper (con resumen en inglés), ponencia, LinkedIn 11 y nota para el autor en el artículo del Colegio. Contenido nuevo: componente común, ningún largo plazo, traslado de las ayudas e ITP/IVA (C4, nota S1), dosis y coste. Sección única que_cambio.md; los bloques duplicados de v6.1 se sustituyen por un enlace. Versión de referencia v7.1 en los títulos. Pendientes de auditoría en docs/v7_1/pendientes_auditoria.md (10 resueltos, 12 al backlog con coste).
- **S4.** src/v7_1/s4_ensayo.py recorre el camino real de evaluate_v7 con datos futuros simulados: SUPERADO (formatos, sha256, apertura, negativa a repetir, sha alterado, sin datos nuevos; el registro real queda intacto). Protocolo en docs/v7_1/evaluacion_2027.md, con el calendario oficial del INE de 2026 y 2027 estimado. Desviación declarada antes de la apertura: alquiler 2026T3.
- **make check tras S3.** Dos fallos corregidos: cifras huérfanas «10.000» (normalización en palabras) y cifras_publicables desactualizado (l5_publicables pasa a `make v7_1`).

## Siguiente
- S5: generar publicacion/, metodologia/, reproducir/ e historico/; LEEME_PRIMERO, README y MAPA; tests de publicación y de enlaces.

## Tokens de subagentes (de 0,65 M)

| Módulo | Tokens |
|---|---|
| S2 lit-researcher | 29.834 |
| **Total** | **29.834** |

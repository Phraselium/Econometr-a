# Estado V7.1

## Hecho
- Rama r7.1/main creada desde r7/main (3d1170c). Plan escrito en docs/v7_1/plan.md.
- **S1 (dosis y coste).** src/v7_1/s1_dosis_coste.py reproduce las extracciones de R6, con una comprobación < 1e-3 frente a impactos.csv. Escribe output/v7_1/S1/{dosis_coste.csv, resumen.md, hechos.json (17 cifras), resultado.json}.
- **S1, entregables.** src/v7_1/s1_atlas.py escribe:
  - el atlas v7.1, con una sección 6 bis por CCAA;
  - el Excel con 3 hojas DC (azul, negro, verde, sin paneles inmovilizados);
  - el verificador v7.1 (V7-V2 con dosis y coste).
- **cifras_clave.** Incorpora V7 y V7.1 (W2); `make v7_1` añadido. `make check` en verde (tras ajustar test_k4a, W2), más tests/v7_1/test_s1.py.
- **S2.** Verificación de literatura hecha (lit-researcher): 0 referencias VERIFICADAS completas porque Scimago devolvió 403 (W6).

## Siguiente
- S2: redactar output/v7_1/nota_metodologica.md.

## Tokens de subagentes (de 0,65 M)

| Módulo | Tokens |
|---|---|
| S2 lit-researcher | 29.834 |
| **Total** | **29.834** |

# B3 · desviaciones del pre-registro (todas EXPLORATORIAS)
1. F5 renta: PIB per cápita provincial (CRE/Padrón) en lugar de renta por hogar ADRH. Las tablas ADRH del INE son municipales/seccionales (volumen excedido en la API; local solo 2019-2023, sin 2015). La CRE llega a 2024 para las 50 provincias.
2. Ventanas: Y2 (SERPAVI) 2015-2024 y 2021-2024; Y3 y crecimiento de renta hasta 2024. Y2 P1 tiene N=46 (sin Araba, Gipuzkoa, Bizkaia ni Navarra: SERPAVI no las cubre en 2015).
3. F2 con variación de padrón (total y extranjera); los flujos migratorios del INE terminan en 2022.
4. F7: hipotecas sobre vivienda por 1.000 habitantes (no por hogar: no hay hogares provinciales antes de 2021).
5. F4 (A4) está medida en 2021-2025 y usa precios: no es valor inicial y su asociación con Y1 puede ser en parte mecánica.
6. F6 en P2 usa el precio de 2021 (inicio del periodo). F3 es valor de 2021 (C4).
7. Holm: 8 familias x Y1 x P1 (texto del pre-registro); en F1, F2 y F6 se usa el coeficiente líder; en el resto el Wald conjunto. Se informa también Holm sobre las 3 confirmatorias.
8. Validación AR(4)/ECM v1 y bloques con embargo no aplican a un corte transversal: LOO-CV frente a modelo de media, DM con HLN.
9. Ceuta y Melilla excluidas. Conley con centroides municipales ponderados por secciones (Canarias en UTM30, distancia aproximada).
10. Añadido: control de error de medida de F6 (precio inicial de Registradores).

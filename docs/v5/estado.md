# Estado v5

| Tarea | Módulo | Estado | Capa | Resultado principal | Tokens subagentes |
|---|---|---|---|---|---|
| Setup (rama r5/main, CLAUDE.md v5, plan) | — | hecho | — | — | 0 |
| R0 barrido del backlog | R | hecho | — | 54 ítems (16 altos, 28 medios, 10 bajos); 18 no cubiertos por A-E | 183.084 |
| R1 técnico (LFS/.gz, Notariado, distritos SERPAVI, ERRATA) | R | hecho | — | BK-044/045/046/047 | 0 (orquestador) |
| R1c titularidad por edad, capacidad de construcción, vacías municipales | R | hecho | C1 (tenencia en propiedad 72-76 %, 3 fuentes)/C4 | tramos de edad C4; PJ compradores 11,3 % (C4); empleo/iniciadas 12,6 en 2025; vacías por municipio (INE 59531, C4) | 92.804 |
| R1a no residentes, VUT INE/GVA, temporada | R | hecho | C4 | no residentes 9,9 % (2015) → 6,8 % (2025); con controles la asociación con el precio no se distingue de cero (IC95 compatible con hasta el 60 % de la bivariada); VUT GVA/INE 1,41-1,75 (definición ≤74 % del log); temporada NO ANALIZADA | 88.711 |
| A2-A3 conciliación de precio y alquiler | A | hecho (ficha A23-V2 ajustada a B5 por el orquestador) | C1/C2/C4 | IPV +79,9 % vs núcleo +44-56 % (C1); puente: pesos CCAA +0,6 pp, nueva/usada ≈0, desfase ±7 pp, residuo C4 −30,9 pp (método/calidad); alquiler stock +11 % a +43 %, nuevos +37 % a +58 % (dirección C1 en CAT y CV); «se ha duplicado»: stock CONTRADICHA (C1), nuevos ANALIZADA (C4 nacional) | 135.674 |
| R1b donut, sensibilidad v2, GSADF con tamaño corregido | R | hecho | C4 | donut: periferia gana en 77 % (SERPAVI) y 55 % (tasado) de 320 specs, nada tras Holm; BI Bartik Oster δ=8,8, RV=0,35; GSADF: ningún episodio nacional sobrevive a BH; frente a fundamentales, sin exuberancia | 153.673 |
| A4 coste oficial y reclasificación | A | hecho parcial (1 de 3 fuentes de coste; corrección del orquestador) | C2 (11 provincias)/C4 | coste MBC 1993 actualizado 422-932 €/m²; provincias 2021-25: clase 1 = 37 (8 C2), 2 = 11 (3 C2), 3 = 2, 4 = 0, 9 = 2; concentración 6 provincias = 50 %, 18 = 80 % | 125.446 |
| A6 topes y García-López | A | hecho (consolidación) | C4 | output/v5/A6/nota.md | 0 (orquestador) |
| A5 programas oficiales y palabras clave | A | hecho | C4 (cotas) | 25 documentos oficiales; 3 de v4 excluidos (no oficiales); 631 coincidencias; precisión 50 % (medida) / 78 % (medida o mención) | 125.013 |
| Revisión módulo R | R | REHACER (B1-B3) → corregido; APROBADO | — | docs/v5/revision_R.md | 82.937 |
| Revisión módulo A | A | REHACER (B1-B4) → corregido; APROBADO | — | docs/v5/revision_A.md; clases territoriales y fuentes únicas pasan a C4 | 85.520 |
| B1 necesidad por provincia 2026-2035 | B | hecho | C4 (F en C2) | 94 mil-310 mil viviendas/año (central 215 mil); atraso 83-147 mil/año; F 172 mil/año; L 80-217 mil/año (no se resta: F ya es neta) | 130.132 |
| B3 diferencias entre provincias (pre-registrado) | B | hecho | C4 (descriptivo honesto) | MDE 0,62 DT; solo convergencia (−16 pp/DT, Holm 0,0013); Bartik y población no rechazadas; Shapley no coincide entre fuentes | 141.302 |
| B2 proyección del déficit 2026-2030 | B | hecho | C4 (F en C2) | nacional empeora en los 3 escenarios: 0,70 M (2025) → 1,30 M central (0,87-1,45 M) en 2030; provincias: 20 empeoran, 5 mejoran, 27 indeterminadas | 63.642 |
| B4 contribuciones a la subida (triangulación) | B | hecho | C2 (cotas v3)/C4 | «contribuciones no estables»: solo el 22 % de 37 comparaciones de orden con τ≥0,67; B3 pone la oferta primera, v2 ≈0; contratos nuevos sin descomposición; inversión sin dato | 102.139 |
| Revisión módulo B | B | REHACER (1-3) → corregido; APROBADO | — | docs/v5/revision_B.md | 86.262 |
| C-a Europa (C4), crédito a promotores (C1), contado (C3) | C | hecho | C4 | España: precio real +42,6 % vs mediana UE +37,4 % (P65); alquiler real −10,3 %; emancipación fuera del IQR; crédito a promotores 470 → 98 mm €; contado 30-58 % | 139.510 |
| C-b seguridad jurídica (C5), fiscalidad (C6), empresas (C8) | C | hecho | C4 | usurpación y cuota de alquiler: rho +0,57/+0,66 (signo contrario a la afirmación; urbanización); AEAT no publica por número de inmuebles (sin dato); PJ: 11,3 % de compradores; residual de stock no persona física 16,9-38,1 % | 130.684 |

**Hecho:** módulos R, A y B aprobados; C-a; check_v5 en make check.
**Siguiente:** C-b y C-c (en curso) → revisión C → D.
**Tokens de subagentes v5:** 1.866.533 / 4.200.000 (R: 601.209 / 900.000; A: 471.653 / 700.000; B: 523.477 / 1.000.000; C: 270.194 / 700.000) (corte global al 80 %: 3.360.000; reserva 420.000).

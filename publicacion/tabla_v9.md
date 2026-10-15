<!-- Generado por `make publicacion` desde output/v9/f3/tabla_revista.md. No editar a mano: se regenera y un test lo comprueba. -->

# Tabla V9 · resultados de los diseños D1-D5 (estilo revista)

β: efecto o asociación en log (≈ proporción). IC 95 %. p: bootstrap salvaje por conglomerados (D1, D2), normal (D3-D5).
p ajustado: Holm en la familia confirmatoria {H1a-renta, H1b-renta}; BH (q = 0,10) en las exploratorias.
Capa según las reglas pre-registradas (docs/v9/hipotesis.md y addendum A1). Sin lenguaje causal por debajo de C3/C3s.

| Diseño | Hipótesis | Resultado | β | EE | IC 95 % | p | p ajustado | N | Diagnósticos | Capa |
|---|---|---|---|---|---|---|---|---|---|---|
| D1a | H1a-renta | log renta media de contratos nuevos | -0,058 | 0,014 | [-0,085; -0,032] | < 0,001 | < 0,001 | 231 | pretend. p = < 0,001; placebo fecha p = 0,007; Honest M̄=1 [-0,275; 0,153], M̄ ruptura 0,20; permutación p = < 0,001 | C4: confirmatoria; no cumple: pretendencias p > 0,10; placebo de fecha p > 0,10; Honest DiD M̄ = 1 excluye 0 |
| D1a | H1a-contratos (exploratoria) | log contratos nuevos | -0,062 | 0,035 | [-0,132; 0,007] | 0,072 | 0,235 | 394 | pretend. p = 0,031; placebo fecha p = 0,613; Honest M̄=1 [-0,353; 0,218], M̄ ruptura 0,00; permutación p = 0,040 | C4: exploratoria: no detectada (BH ≥ 0,10) |
| D1b | H1b-renta | log renta media de contratos nuevos | -0,059 | 0,008 | [-0,073; -0,044] | < 0,001 | < 0,001 | 241 | pretend. p = 0,282; placebo fecha p = 0,408; Honest M̄=1 [-0,129; 0,012], M̄ ruptura 0,80; permutación p = < 0,001 | C4: confirmatoria; no cumple: Honest DiD M̄ = 1 excluye 0 |
| D1b | H1b-contratos (exploratoria) | log contratos nuevos | -0,013 | 0,029 | [-0,070; 0,044] | 0,645 | 0,725 | 416 | pretend. p = 0,280; placebo fecha p = 0,156; Honest M̄=1 [-0,349; 0,323], M̄ ruptura 0,00; permutación p = 0,826 | C4: exploratoria: no detectada (BH ≥ 0,10) |
| D1c | exploratoria | log renta media de contratos nuevos | -0,025 | 0,005 | [-0,035; -0,014] | < 0,001 | < 0,001 | 13 | — | C4: exploratoria: asociación (BH < 0,10) |
| D1c | exploratoria | log contratos nuevos | -0,062 | 0,030 | [-0,119; -0,004] | 0,030 | 0,135 | 20 | — | C4: exploratoria: no detectada (BH ≥ 0,10) |
| D2 | H2-renta-covid (exploratoria) | log renta media de contratos nuevos (covid; por 1 DE de dosis) | 0,002 | 0,004 | [-0,005; 0,010] | 0,617 | 0,725 | 428 | pretend. p = < 0,001; placebo fecha p = 0,476; permutación p = 0,636 | C4: exploratoria: no detectada (BH ≥ 0,10); pretendencias rechazadas |
| D2 | H2-renta-reapertura (exploratoria) | log renta media de contratos nuevos (reapertura; por 1 DE de dosis) | 0,010 | 0,003 | [0,004; 0,017] | 0,006 | 0,036 | 428 | pretend. p = < 0,001; placebo fecha p = 0,476; permutación p = 0,044 | C4: exploratoria: asociación (BH < 0,10); pretendencias rechazadas |
| D2 | H2-contratos-covid (exploratoria) | log contratos nuevos (covid; por 1 DE de dosis) | 0,010 | 0,015 | [-0,020; 0,040] | 0,537 | 0,725 | 644 | pretend. p = 0,630; placebo fecha p = 0,789; permutación p = 0,568 | C4: exploratoria: no detectada (BH ≥ 0,10) |
| D2 | H2-contratos-reapertura (exploratoria) | log contratos nuevos (reapertura; por 1 DE de dosis) | 0,013 | 0,021 | [-0,029; 0,054] | 0,642 | 0,725 | 644 | pretend. p = 0,630; placebo fecha p = 0,789; permutación p = 0,398 | C4: exploratoria: no detectada (BH ≥ 0,10) |
| D3 | descriptiva | d_cuota ~ ΔVUT por 100 viviendas | 0,002 | 0,002 | [-0,002; 0,006] | 0,340 | — | 192 | — | C4: descriptivo (sin potencia) |
| D3 | descriptiva | d_lmedia ~ ΔVUT por 100 viviendas | -0,002 | 0,001 | [-0,004; 0,000] | 0,080 | — | 192 | — | C4: descriptivo (sin potencia) |
| D4 | H4-réplica-alquiler (exploratoria) | Δ log IPC de alquiler (principal (réplica 2003-2012)) | 0,007 | 0,008 | [-0,008; 0,023] | 0,357 | 0,584 | 50 | F ef. = 4,6; AR [-0,137; 0,018]; EE AKM 0,006 | C4: exploratoria: no detectada (BH ≥ 0,10); instrumento débil (F efectiva 4.6 < 23,1): solo IC de Anderson-Rubin |
| D4 | H4-réplica-alquiler (exploratoria) (efecto total) | Δ log IPC de alquiler (principal (réplica 2003-2012) · endógena = Δ población total) | 0,004 | 0,004 | [-0,004; 0,013] | 0,326 | 0,584 | 50 | F ef. = 2,1; AR [-0,300; 0,300]; EE AKM 0,004 | C4: exploratoria: no detectada (BH ≥ 0,10); instrumento débil (F efectiva 2.1 < 23,1): solo IC de Anderson-Rubin |
| D4 | exploratoria | Δ log valor tasado (principal (réplica 2003-2012)) | -0,003 | 0,012 | [-0,027; 0,021] | 0,818 | 0,818 | 43 | F ef. = 3,7; AR [-0,300; 0,300]; EE AKM 0,014 | C4: exploratoria: no detectada (BH ≥ 0,10); instrumento débil (F efectiva 3.7 < 23,1): solo IC de Anderson-Rubin |
| D4 | exploratoria (efecto total) | Δ log valor tasado (principal (réplica 2003-2012) · endógena = Δ población total) | -0,002 | 0,007 | [-0,015; 0,012] | 0,810 | 0,818 | 43 | F ef. = 1,5; AR [-0,300; 0,300]; EE AKM 0,008 | C4: exploratoria: no detectada (BH ≥ 0,10); instrumento débil (F efectiva 1.5 < 23,1): solo IC de Anderson-Rubin |
| D4 | H4-réplica-alquiler (exploratoria) | Δ log IPC de alquiler (ampliación 2015-2022) | 0,015 | 0,015 | [-0,014; 0,044] | 0,301 | 0,584 | 50 | F ef. = 2,8; AR [-0,300; 0,300]; EE AKM 0,008 | C4: exploratoria: no detectada (BH ≥ 0,10); instrumento débil (F efectiva 2.8 < 23,1): solo IC de Anderson-Rubin |
| D4 | exploratoria | Δ log valor tasado (ampliación 2015-2022) | 0,129 | 0,073 | [-0,015; 0,272] | 0,078 | 0,235 | 49 | F ef. = 3,4; AR [0,042; 0,300]; EE AKM 0,065 | C4: exploratoria: no detectada (BH ≥ 0,10); instrumento débil (F efectiva 3.4 < 23,1): solo IC de Anderson-Rubin |
| D5 | exploratoria | Δ log precio (h = 4) por shock × 1 DE de exposición | -0,053 | 0,053 | [-0,156; 0,051] | 0,322 | 0,584 | 18 | — | C4: exploratoria: no detectada (BH ≥ 0,10) |
| D5 | exploratoria | Δ log precio (h = 8) por shock × 1 DE de exposición | -0,044 | 0,067 | [-0,175; 0,088] | 0,513 | 0,725 | 18 | — | C4: exploratoria: no detectada (BH ≥ 0,10) |
| D5 | exploratoria | Δ log alquiler (h = 4) por shock × 1 DE de exposición | -0,117 | 0,029 | [-0,174; -0,060] | < 0,001 | < 0,001 | 17 | — | C4: exploratoria: asociación (BH < 0,10) |
| D5 | exploratoria | Δ log alquiler (h = 8) por shock × 1 DE de exposición | -0,066 | 0,068 | [-0,198; 0,067] | 0,332 | 0,584 | 17 | — | C4: exploratoria: no detectada (BH ≥ 0,10) |

Fuentes: Incasòl (no redistribuible; solo agregados), EMAL, IDESCAT, GVA, INE, MIVAU, BIS, Eurostat, BCE, Jarociński-Karadi. Elaboración propia. D6 no se estima (sin edad exacta); D7 es contable (output/v9/d7).

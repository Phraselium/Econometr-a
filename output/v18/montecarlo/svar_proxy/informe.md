# V18 · Monte Carlo · SVAR con proxy y bandas robustas a la debilidad (E7-R2)

**Veredicto: AR_delta_NeweyWest4 (h = 8, todas las fuerzas): NO APTO; Wald_delta (h = 8, F >= 10): NO APTO.** Condición en que falla: AR: fuerte|rho090|h8: cobertura 0.9027 fuera de [0,92; 0,97] (insuficiente); AR: fuerte|rho097|h8: cobertura 0.8733 fuera de [0,92; 0,97] (insuficiente); AR: debil|rho090|h8: tamaño 0.0137 fuera de [0,03; 0,08] (conservador) / cobertura 0.9863 fuera de [0,92; 0,97] (conservadora) / cobertura 0.9747 fuera de [0,92; 0,97] (conservadora); AR: debil|rho097|h8: tamaño 0.0190 fuera de [0,03; 0,08] (conservador) / cobertura 0.9810 fuera de [0,92; 0,97] (conservadora); Wald: fuerte|rho090|h8: cobertura 0.8840 fuera de [0,92; 0,97] (insuficiente); Wald: fuerte|rho097|h8: tamaño 0.0873 fuera de [0,03; 0,08] (liberal) / cobertura 0.9127 fuera de [0,92; 0,97] (insuficiente) / cobertura 0.8557 fuera de [0,92; 0,97] (insuficiente).

## Proceso generador (declarado antes de simular)

Estructura (declarada; ningún dato real): VAR trimestral de 6 variables [tipo hipotecario, ln precio real, ln compraventas, ln PIB, IPCA, euríbor] (E7-R2), T = 108 trimestres (1999T1-2025T4), con
el proxy construido desde una sorpresa MENSUAL de 324 meses (suma de 3 meses por trimestre, t de Student 5 gl, 15 % de meses sin reunión).
Proceso verdadero: VAR(2) con matrices de coeficientes fijadas con SEED 20261010 (diagonal 0,5 y 0,2 más cruces N(0; 0,06²), reescaladas para que la mayor raíz de la companion sea ρ = 0,90 o 0,97);
u_t = B0 ε_t con B0 triangular inferior: primera columna (choque monetario) b = (1; −0,15; −0,3; −0,1; 0,05; 0,6) y resto N(0; 0,5²) con diagonal 1. El proxy es z_t = φ ε_{1t} + ν_t, ν_t la suma trimestral
de la sorpresa mensual con error de medida; φ se calibra para que la F robusta de la primera etapa (u_1 sobre z) medida valga ≈ 50, 10 o 3 con T_eff = 104 (la F de Q5 fue 2,1-2,9); la F medida se informa en la tabla.
Nulo (θ = 0): la ecuación del precio solo depende de su propio pasado y no responde al choque monetario (b_precio = 0), de modo que su IRF al choque es 0 a todo horizonte; alternativa: el precio depende del tipo (−0,15 y −0,05 en los rezagos 1 y 2) y de las compraventas (+0,1), con b_precio = −0,15.
Estimación: VAR(4) por MCO (constante incluida; uno o dos rezagos más que el verdadero), m̂ = E[z û], θ̂_{h,precio} = Ψ_h[precio, :] m̂ / m̂[tipo] a h = 4 y 8 (principal: 8; «a 8 trimestres escalada a +100 pb»).
Variantes: (1) AR por método delta con varianza de largo plazo Newey-West de 4 rezagos sobre las influencias conjuntas de (A, m) (robusta a proxy débil; conjunto por forma cerrada); (2) Wald de método delta (θ̂ ± 1,96 EE);
(3) bootstrap de bloques móviles (longitud 8, 199 réplicas, percentil) sobre las filas (Y, z), en el 20 % de las réplicas (R_bb). Cobertura = 1 − rechazo del contraste en θ verdadero (inversión; AR por forma cerrada).

## Qué falló en V16 y qué se hace distinto

No hay Monte Carlo previo del SVAR con proxy en V15 ni en V16 (el plan lo marca «Sin validar»). Se reutiliza la lección de V16 sobre series (lp_newey_west_b NO APTO: ancho de banda y persistencia) midiendo con persistencia alta (ρ = 0,97)
y se separa la fuerza del proxy. Con F ≈ 3 el Wald de método delta no es válido por construcción; el AR es el que se evalúa para el veredicto en todas las fuerzas.

## Criterio

Criterio del encargo: APTO si el tamaño al 5 % está en [0,03; 0,08] y la cobertura al 95 % (bajo el nulo y bajo la alternativa) en [0,92; 0,97], con R >= 2.000 (o >= 1.000 si se declara). Bandas de la adenda 1.12: apta (tamaño [0,04; 0,06], cobertura [0,93; 0,97], R >= 2.000); con valor crítico corregido (tamaño [0,02; 0,04) o (0,06; 0,15]); no fiable (tamaño > 0,15 o < 0,02). SEED = 20261010. Resultados simulados: ningún dato real de resultado ni muestra sellada.

## Resultados

| escenario | variante | R | tamano_5pct | cobertura_nulo | cobertura_alt | potencia | veredicto | banda_112 | F_robusta_media |
|---|---|---|---|---|---|---|---|---|---|
| fuerte|rho090|h4 | AR_delta_NeweyWest4 | 3000 | 0.0867 | 0.9133 | 0.9153 | 0.2530 | NO APTO | con valor crítico corregido | 27.1782 |
| fuerte|rho090|h4 | Wald_delta | 3000 | 0.1010 | 0.8990 | 0.8987 | 0.2840 | NO APTO | con valor crítico corregido | 27.1782 |
| fuerte|rho090|h4 | bootstrap_bloques_percentil (R_bb ≈ 20 %) | 579 | 0.0000 | 1.0000 | 0.9850 | 0.0017 | NO EVALUABLE (R < 2.000) | no fiable (R < 2.000: informativo) | 27.1782 |
| fuerte|rho090|h8 | AR_delta_NeweyWest4 | 3000 | 0.0573 | 0.9427 | 0.9027 | 0.0803 | NO APTO | con valor crítico corregido | 27.1782 |
| fuerte|rho090|h8 | Wald_delta | 3000 | 0.0713 | 0.9287 | 0.8840 | 0.1023 | NO APTO | con valor crítico corregido | 27.1782 |
| fuerte|rho090|h8 | bootstrap_bloques_percentil (R_bb ≈ 20 %) | 579 | 0.0000 | 1.0000 | 0.9500 | 0.0000 | NO EVALUABLE (R < 2.000) | no fiable (R < 2.000: informativo) | 27.1782 |
| fuerte|rho097|h4 | AR_delta_NeweyWest4 | 3000 | 0.0920 | 0.9080 | 0.9010 | 0.3047 | NO APTO | con valor crítico corregido | 27.3594 |
| fuerte|rho097|h4 | Wald_delta | 3000 | 0.1087 | 0.8913 | 0.8807 | 0.3423 | NO APTO | con valor crítico corregido | 27.3594 |
| fuerte|rho097|h4 | bootstrap_bloques_percentil (R_bb ≈ 20 %) | 627 | 0.0000 | 1.0000 | 0.9742 | 0.0017 | NO EVALUABLE (R < 2.000) | no fiable (R < 2.000: informativo) | 27.3594 |
| fuerte|rho097|h8 | AR_delta_NeweyWest4 | 3000 | 0.0723 | 0.9277 | 0.8733 | 0.1173 | NO APTO | con valor crítico corregido | 27.3594 |
| fuerte|rho097|h8 | Wald_delta | 3000 | 0.0873 | 0.9127 | 0.8557 | 0.1417 | NO APTO | con valor crítico corregido | 27.3594 |
| fuerte|rho097|h8 | bootstrap_bloques_percentil (R_bb ≈ 20 %) | 627 | 0.0000 | 1.0000 | 0.8643 | 0.0000 | NO EVALUABLE (R < 2.000) | no fiable (R < 2.000: informativo) | 27.3594 |
| moderada|rho090|h4 | AR_delta_NeweyWest4 | 3000 | 0.0460 | 0.9540 | 0.9447 | 0.1230 | APTO | apta | 9.8588 |
| moderada|rho090|h4 | Wald_delta | 3000 | 0.0513 | 0.9487 | 0.9413 | 0.1433 | APTO | apta | 9.8588 |
| moderada|rho090|h4 | bootstrap_bloques_percentil (R_bb ≈ 20 %) | 602 | 0.0000 | 1.0000 | 0.9983 | 0.0017 | NO EVALUABLE (R < 2.000) | no fiable (R < 2.000: informativo) | 9.8588 |
| moderada|rho090|h8 | AR_delta_NeweyWest4 | 3000 | 0.0317 | 0.9683 | 0.9553 | 0.0450 | APTO | con valor crítico corregido | 9.8588 |
| moderada|rho090|h8 | Wald_delta | 3000 | 0.0377 | 0.9623 | 0.9380 | 0.0510 | APTO | con valor crítico corregido | 9.8588 |
| moderada|rho090|h8 | bootstrap_bloques_percentil (R_bb ≈ 20 %) | 602 | 0.0000 | 1.0000 | 0.9983 | 0.0000 | NO EVALUABLE (R < 2.000) | no fiable (R < 2.000: informativo) | 9.8588 |
| moderada|rho097|h4 | AR_delta_NeweyWest4 | 3000 | 0.0597 | 0.9403 | 0.9347 | 0.1513 | APTO | apta | 9.8867 |
| moderada|rho097|h4 | Wald_delta | 3000 | 0.0533 | 0.9467 | 0.9353 | 0.1847 | APTO | apta | 9.8867 |
| moderada|rho097|h4 | bootstrap_bloques_percentil (R_bb ≈ 20 %) | 635 | 0.0000 | 1.0000 | 0.9967 | 0.0000 | NO EVALUABLE (R < 2.000) | no fiable (R < 2.000: informativo) | 9.8867 |
| moderada|rho097|h8 | AR_delta_NeweyWest4 | 3000 | 0.0400 | 0.9600 | 0.9393 | 0.0607 | APTO | apta | 9.8867 |
| moderada|rho097|h8 | Wald_delta | 3000 | 0.0453 | 0.9547 | 0.9207 | 0.0750 | APTO | con valor crítico corregido | 9.8867 |
| moderada|rho097|h8 | bootstrap_bloques_percentil (R_bb ≈ 20 %) | 635 | 0.0000 | 1.0000 | 0.9805 | 0.0000 | NO EVALUABLE (R < 2.000) | no fiable (R < 2.000: informativo) | 9.8867 |
| debil|rho090|h4 | AR_delta_NeweyWest4 | 3000 | 0.0320 | 0.9680 | 0.9660 | 0.0627 | APTO | con valor crítico corregido | 4.1578 |
| debil|rho090|h4 | Wald_delta | 3000 | 0.0173 | 0.9827 | 0.9783 | 0.0617 | NO APTO | no fiable | 4.1578 |
| debil|rho090|h4 | bootstrap_bloques_percentil (R_bb ≈ 20 %) | 601 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO EVALUABLE (R < 2.000) | no fiable (R < 2.000: informativo) | 4.1578 |
| debil|rho090|h8 | AR_delta_NeweyWest4 | 3000 | 0.0137 | 0.9863 | 0.9747 | 0.0257 | NO APTO | no fiable | 4.1578 |
| debil|rho090|h8 | Wald_delta | 3000 | 0.0127 | 0.9873 | 0.9757 | 0.0223 | NO APTO | no fiable | 4.1578 |
| debil|rho090|h8 | bootstrap_bloques_percentil (R_bb ≈ 20 %) | 601 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO EVALUABLE (R < 2.000) | no fiable (R < 2.000: informativo) | 4.1578 |
| debil|rho097|h4 | AR_delta_NeweyWest4 | 3000 | 0.0377 | 0.9623 | 0.9630 | 0.0690 | APTO | con valor crítico corregido | 4.0524 |
| debil|rho097|h4 | Wald_delta | 3000 | 0.0213 | 0.9787 | 0.9737 | 0.0743 | NO APTO | con valor crítico corregido | 4.0524 |
| debil|rho097|h4 | bootstrap_bloques_percentil (R_bb ≈ 20 %) | 634 | 0.0000 | 1.0000 | 0.9967 | 0.0000 | NO EVALUABLE (R < 2.000) | no fiable (R < 2.000: informativo) | 4.0524 |
| debil|rho097|h8 | AR_delta_NeweyWest4 | 3000 | 0.0190 | 0.9810 | 0.9627 | 0.0303 | NO APTO | no fiable | 4.0524 |
| debil|rho097|h8 | Wald_delta | 3000 | 0.0133 | 0.9867 | 0.9623 | 0.0310 | NO APTO | no fiable | 4.0524 |
| debil|rho097|h8 | bootstrap_bloques_percentil (R_bb ≈ 20 %) | 634 | 0.0000 | 1.0000 | 0.9967 | 0.0000 | NO EVALUABLE (R < 2.000) | no fiable (R < 2.000: informativo) | 4.0524 |

## Notas

- El veredicto es sobre h = 8. El bootstrap de bloques se mide solo en ≈ 20 % de las réplicas (coste): es información, no decide.
- θ está normalizado a un cambio unitario del tipo en el impacto; la verdad sale de las matrices del VAR verdadero.

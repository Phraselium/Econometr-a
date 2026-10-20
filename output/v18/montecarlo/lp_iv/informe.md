# V18 · Monte Carlo · Proyección local con instrumento (E7-R1)

**Veredicto: AR_aumentado_EHW (h = 8, todas las fuerzas): NO APTO; 2SLS_NeweyWest_h+1 (h = 8, F >= 10): NO APTO; 2SLS_aumentado_EHW (h = 8, F >= 10): NO APTO.** Condición en que falla: AR_aumentado_EHW: fuerte|rho095|h8: cobertura 0.8724 fuera de [0,92; 0,97] (insuficiente); fuerte|rho099|h8: cobertura 0.8210 fuera de [0,92; 0,97] (insuficiente); moderada|rho099|h8: cobertura 0.9108 fuera de [0,92; 0,97] (insuficiente); 2SLS_NeweyWest_h+1: fuerte|rho095|h8: tamaño 0.1154 fuera de [0,03; 0,08] (liberal) / cobertura 0.8846 fuera de [0,92; 0,97] (insuficiente) / cobertura 0.7914 fuera de [0,92; 0,97] (insuficiente); fuerte|rho099|h8: tamaño 0.1110 fuera de [0,03; 0,08] (liberal) / cobertura 0.8890 fuera de [0,92; 0,97] (insuficiente) / cobertura 0.7192 fuera de [0,92; 0,97] (insuficiente); moderada|rho095|h8: cobertura 0.8570 fuera de [0,92; 0,97] (insuficiente); moderada|rho099|h8: cobertura 0.8224 fuera de [0,92; 0,97] (insuficiente); 2SLS_aumentado_EHW: fuerte|rho095|h8: cobertura 0.8400 fuera de [0,92; 0,97] (insuficiente); fuerte|rho099|h8: cobertura 0.7726 fuera de [0,92; 0,97] (insuficiente); moderada|rho095|h8: cobertura 0.9066 fuera de [0,92; 0,97] (insuficiente); moderada|rho099|h8: cobertura 0.8670 fuera de [0,92; 0,97] (insuficiente).

## Proceso generador (declarado antes de simular)

Estructura (declarada; ningún dato real): serie trimestral 1999T1-2025T4 (T = 108 trimestres = 324 meses). La sorpresa se genera MENSUAL (324 meses más 300 de calentamiento): s_m = 0 en el
15 % de los meses (sin reunión) y en el resto t de Student con 5 gl, escalada para que la suma trimestral (3 meses) tenga varianza 1; z_t = suma de los 3 meses (como en E7).
Modelo: Δi_t = 0,4 Δi_{t−1} + π z_t + u^i_t ;  y_t = r1 y_{t−1} + r2 y_{t−2} + κ Δi_t + γ Δi_{t−1} + u^y_t ;  u^y = 0,8 u^i + w, u^i ~ N(0,1), w ~ N(0; 0,5²) (endogeneidad: el 2SLS es necesario).
r2 = −0,25, r1 = ρ + 0,25 con ρ = r1 + r2 = 0,95 o 0,99 (persistencia alta; el plan exige robustez a ella). Fuerza del instrumento: π = 1,00 (F efectiva robusta medida ≈ 23), 0,40 (≈ 10), 0,17 (≈ 3; Q5 dio 2,1 a 2,9); la F medida se informa en la tabla.
Respuesta verdadera: β_h = IRF_y(h)/π (por unidad de cambio contemporáneo de Δi_t), por recursión determinista; nulo: κ = γ = 0 (β_h = 0); alternativa: κ = −0,5, γ = 0,1.
Estimación (E7-R1): y_{t+h} − y_{t−1} sobre Δi_t, instrumentado por z_t, con constante y 4 rezagos de y (niveles) y de Δi (n = 104 − h observaciones), h = 4, 8 (contraste principal) y 12.
Variantes: (1) 2SLS con Newey-West de ancho h + 1 (la del plan; contraste t normal); (2) 2SLS aumentado (5 rezagos, uno más que la especificación) con EHW; (3) AR con Newey-West de ancho h + 1;
(4) AR aumentado con EHW. Diagnóstico: sorpresa gaussiana sin meses vacíos (ρ = 0,95). Cobertura = 1 − rechazo del contraste en β_h verdadero (inversión; el conjunto AR es una desigualdad cuadrática, posiblemente no acotada).

## Qué falló en V16 y qué se hace distinto

V16 (lp_newey_west_b): Newey-West con b fija NO APTO (tamaño 0,0642-0,0925, cobertura 0,813-0,9313) con T = 100, h = 1-12 y persistencia 0,90-0,98: el sobre-rechazo crecía con h y con la persistencia,
y el diseño no tenía instrumento ni variación de fuerza. Aquí se estima el 2SLS (que no existe en V16), se evalúa la versión aumentada con EHW que propone el plan y se separa el efecto de la fuerza
del instrumento (con F ≈ 3 el contraste t de 2SLS no es válido por construcción: decide el AR). No se vuelve a probar «b fija».

## Criterio

Criterio del encargo: APTO si el tamaño al 5 % está en [0,03; 0,08] y la cobertura al 95 % (bajo el nulo y bajo la alternativa) en [0,92; 0,97], con R >= 2.000 (o >= 1.000 si se declara). Bandas de la adenda 1.12: apta (tamaño [0,04; 0,06], cobertura [0,93; 0,97], R >= 2.000); con valor crítico corregido (tamaño [0,02; 0,04) o (0,06; 0,15]); no fiable (tamaño > 0,15 o < 0,02). SEED = 20261010. Resultados simulados: ningún dato real de resultado ni muestra sellada.

## Resultados

| escenario | variante | R | tamano_5pct | cobertura_nulo | cobertura_alt | potencia | veredicto | banda_112 | F_efectiva_media |
|---|---|---|---|---|---|---|---|---|---|
| fuerte|rho095|h4 | 2SLS_NeweyWest_h+1 | 5000 | 0.0996 | 0.9004 | 0.8660 | 0.9328 | NO APTO | con valor crítico corregido | 24.1458 |
| fuerte|rho095|h4 | 2SLS_aumentado_EHW | 5000 | 0.0802 | 0.9198 | 0.8864 | 0.9088 | NO APTO | con valor crítico corregido | 24.1458 |
| fuerte|rho095|h4 | AR_NeweyWest_h+1 | 5000 | 0.0878 | 0.9122 | 0.8990 | 0.9276 | NO APTO | con valor crítico corregido | 24.1458 |
| fuerte|rho095|h4 | AR_aumentado_EHW | 5000 | 0.0688 | 0.9312 | 0.9178 | 0.8884 | NO APTO | con valor crítico corregido | 24.1458 |
| fuerte|rho095|h8 | 2SLS_NeweyWest_h+1 | 5000 | 0.1154 | 0.8846 | 0.7914 | 0.5138 | NO APTO | con valor crítico corregido | 23.1938 |
| fuerte|rho095|h8 | 2SLS_aumentado_EHW | 5000 | 0.0788 | 0.9212 | 0.8400 | 0.4068 | NO APTO | con valor crítico corregido | 23.1938 |
| fuerte|rho095|h8 | AR_NeweyWest_h+1 | 5000 | 0.1084 | 0.8916 | 0.8246 | 0.4840 | NO APTO | con valor crítico corregido | 23.1938 |
| fuerte|rho095|h8 | AR_aumentado_EHW | 5000 | 0.0690 | 0.9310 | 0.8724 | 0.3700 | NO APTO | con valor crítico corregido | 23.1938 |
| fuerte|rho095|h12 | 2SLS_NeweyWest_h+1 | 5000 | 0.1322 | 0.8678 | 0.7504 | 0.2634 | NO APTO | con valor crítico corregido | 22.2958 |
| fuerte|rho095|h12 | 2SLS_aumentado_EHW | 5000 | 0.0808 | 0.9192 | 0.8268 | 0.1614 | NO APTO | con valor crítico corregido | 22.2958 |
| fuerte|rho095|h12 | AR_NeweyWest_h+1 | 5000 | 0.1248 | 0.8752 | 0.7838 | 0.2512 | NO APTO | con valor crítico corregido | 22.2958 |
| fuerte|rho095|h12 | AR_aumentado_EHW | 5000 | 0.0658 | 0.9342 | 0.8552 | 0.1368 | NO APTO | con valor crítico corregido | 22.2958 |
| fuerte|rho099|h4 | 2SLS_NeweyWest_h+1 | 5000 | 0.0848 | 0.9152 | 0.8214 | 0.9584 | NO APTO | con valor crítico corregido | 24.0238 |
| fuerte|rho099|h4 | 2SLS_aumentado_EHW | 5000 | 0.0674 | 0.9326 | 0.8462 | 0.9372 | NO APTO | con valor crítico corregido | 24.0238 |
| fuerte|rho099|h4 | AR_NeweyWest_h+1 | 5000 | 0.0712 | 0.9288 | 0.8676 | 0.9544 | NO APTO | con valor crítico corregido | 24.0238 |
| fuerte|rho099|h4 | AR_aumentado_EHW | 5000 | 0.0538 | 0.9462 | 0.8858 | 0.9268 | NO APTO | con valor crítico corregido | 24.0238 |
| fuerte|rho099|h8 | 2SLS_NeweyWest_h+1 | 5000 | 0.1110 | 0.8890 | 0.7192 | 0.6554 | NO APTO | con valor crítico corregido | 23.0935 |
| fuerte|rho099|h8 | 2SLS_aumentado_EHW | 5000 | 0.0768 | 0.9232 | 0.7726 | 0.5660 | NO APTO | con valor crítico corregido | 23.0935 |
| fuerte|rho099|h8 | AR_NeweyWest_h+1 | 5000 | 0.1020 | 0.8980 | 0.7676 | 0.6434 | NO APTO | con valor crítico corregido | 23.0935 |
| fuerte|rho099|h8 | AR_aumentado_EHW | 5000 | 0.0632 | 0.9368 | 0.8210 | 0.5260 | NO APTO | con valor crítico corregido | 23.0935 |
| fuerte|rho099|h12 | 2SLS_NeweyWest_h+1 | 5000 | 0.1310 | 0.8690 | 0.6356 | 0.4462 | NO APTO | con valor crítico corregido | 22.1792 |
| fuerte|rho099|h12 | 2SLS_aumentado_EHW | 5000 | 0.0774 | 0.9226 | 0.7164 | 0.3148 | NO APTO | con valor crítico corregido | 22.1792 |
| fuerte|rho099|h12 | AR_NeweyWest_h+1 | 5000 | 0.1198 | 0.8802 | 0.6852 | 0.4282 | NO APTO | con valor crítico corregido | 22.1792 |
| fuerte|rho099|h12 | AR_aumentado_EHW | 5000 | 0.0644 | 0.9356 | 0.7652 | 0.2774 | NO APTO | con valor crítico corregido | 22.1792 |
| moderada|rho095|h4 | 2SLS_NeweyWest_h+1 | 5000 | 0.0622 | 0.9378 | 0.8838 | 0.3338 | NO APTO | con valor crítico corregido | 10.1896 |
| moderada|rho095|h4 | 2SLS_aumentado_EHW | 5000 | 0.0518 | 0.9482 | 0.9106 | 0.2728 | NO APTO | con valor crítico corregido | 10.1896 |
| moderada|rho095|h4 | AR_NeweyWest_h+1 | 5000 | 0.0710 | 0.9290 | 0.9216 | 0.4562 | APTO | con valor crítico corregido | 10.1896 |
| moderada|rho095|h4 | AR_aumentado_EHW | 5000 | 0.0570 | 0.9430 | 0.9404 | 0.3854 | APTO | apta | 10.1896 |
| moderada|rho095|h8 | 2SLS_NeweyWest_h+1 | 5000 | 0.0704 | 0.9296 | 0.8570 | 0.1594 | NO APTO | con valor crítico corregido | 9.7876 |
| moderada|rho095|h8 | 2SLS_aumentado_EHW | 5000 | 0.0406 | 0.9594 | 0.9066 | 0.1012 | NO APTO | con valor crítico corregido | 9.7876 |
| moderada|rho095|h8 | AR_NeweyWest_h+1 | 5000 | 0.0920 | 0.9080 | 0.8770 | 0.2110 | NO APTO | con valor crítico corregido | 9.7876 |
| moderada|rho095|h8 | AR_aumentado_EHW | 5000 | 0.0564 | 0.9436 | 0.9258 | 0.1502 | APTO | con valor crítico corregido | 9.7876 |
| moderada|rho095|h12 | 2SLS_NeweyWest_h+1 | 5000 | 0.0868 | 0.9132 | 0.8504 | 0.1220 | NO APTO | con valor crítico corregido | 9.3765 |
| moderada|rho095|h12 | 2SLS_aumentado_EHW | 5000 | 0.0418 | 0.9582 | 0.9120 | 0.0608 | NO APTO | con valor crítico corregido | 9.3765 |
| moderada|rho095|h12 | AR_NeweyWest_h+1 | 5000 | 0.1116 | 0.8884 | 0.8610 | 0.1568 | NO APTO | con valor crítico corregido | 9.3765 |
| moderada|rho095|h12 | AR_aumentado_EHW | 5000 | 0.0562 | 0.9438 | 0.9236 | 0.0870 | APTO | con valor crítico corregido | 9.3765 |
| moderada|rho099|h4 | 2SLS_NeweyWest_h+1 | 5000 | 0.0652 | 0.9348 | 0.8682 | 0.3592 | NO APTO | con valor crítico corregido | 10.3567 |
| moderada|rho099|h4 | 2SLS_aumentado_EHW | 5000 | 0.0504 | 0.9496 | 0.8936 | 0.2878 | NO APTO | con valor crítico corregido | 10.3567 |
| moderada|rho099|h4 | AR_NeweyWest_h+1 | 5000 | 0.0760 | 0.9240 | 0.9132 | 0.5000 | NO APTO | con valor crítico corregido | 10.3567 |
| moderada|rho099|h4 | AR_aumentado_EHW | 5000 | 0.0608 | 0.9392 | 0.9328 | 0.4316 | APTO | con valor crítico corregido | 10.3567 |
| moderada|rho099|h8 | 2SLS_NeweyWest_h+1 | 5000 | 0.0728 | 0.9272 | 0.8224 | 0.2110 | NO APTO | con valor crítico corregido | 9.9346 |
| moderada|rho099|h8 | 2SLS_aumentado_EHW | 5000 | 0.0448 | 0.9552 | 0.8670 | 0.1376 | NO APTO | con valor crítico corregido | 9.9346 |
| moderada|rho099|h8 | AR_NeweyWest_h+1 | 5000 | 0.0946 | 0.9054 | 0.8636 | 0.2940 | NO APTO | con valor crítico corregido | 9.9346 |
| moderada|rho099|h8 | AR_aumentado_EHW | 5000 | 0.0546 | 0.9454 | 0.9108 | 0.2080 | NO APTO | con valor crítico corregido | 9.9346 |
| moderada|rho099|h12 | 2SLS_NeweyWest_h+1 | 5000 | 0.0900 | 0.9100 | 0.7638 | 0.1628 | NO APTO | con valor crítico corregido | 9.4993 |
| moderada|rho099|h12 | 2SLS_aumentado_EHW | 5000 | 0.0430 | 0.9570 | 0.8426 | 0.0832 | NO APTO | con valor crítico corregido | 9.4993 |
| moderada|rho099|h12 | AR_NeweyWest_h+1 | 5000 | 0.1114 | 0.8886 | 0.8088 | 0.2140 | NO APTO | con valor crítico corregido | 9.4993 |
| moderada|rho099|h12 | AR_aumentado_EHW | 5000 | 0.0602 | 0.9398 | 0.8862 | 0.1228 | NO APTO | con valor crítico corregido | 9.4993 |
| debil|rho095|h4 | 2SLS_NeweyWest_h+1 | 5000 | 0.0310 | 0.9690 | 0.9174 | 0.0230 | NO APTO | con valor crítico corregido | 3.1434 |
| debil|rho095|h4 | 2SLS_aumentado_EHW | 5000 | 0.0202 | 0.9798 | 0.9348 | 0.0132 | NO APTO | con valor crítico corregido | 3.1434 |
| debil|rho095|h4 | AR_NeweyWest_h+1 | 5000 | 0.0694 | 0.9306 | 0.9272 | 0.1390 | APTO | con valor crítico corregido | 3.1434 |
| debil|rho095|h4 | AR_aumentado_EHW | 5000 | 0.0506 | 0.9494 | 0.9464 | 0.1132 | APTO | apta | 3.1434 |
| debil|rho095|h8 | 2SLS_NeweyWest_h+1 | 5000 | 0.0216 | 0.9784 | 0.9304 | 0.0210 | NO APTO | con valor crítico corregido | 3.0333 |
| debil|rho095|h8 | 2SLS_aumentado_EHW | 5000 | 0.0118 | 0.9882 | 0.9592 | 0.0078 | NO APTO | no fiable | 3.0333 |
| debil|rho095|h8 | AR_NeweyWest_h+1 | 5000 | 0.0866 | 0.9134 | 0.9058 | 0.1142 | NO APTO | con valor crítico corregido | 3.0333 |
| debil|rho095|h8 | AR_aumentado_EHW | 5000 | 0.0558 | 0.9442 | 0.9408 | 0.0738 | APTO | apta | 3.0333 |
| debil|rho095|h12 | 2SLS_NeweyWest_h+1 | 5000 | 0.0284 | 0.9716 | 0.9380 | 0.0288 | NO APTO | con valor crítico corregido | 2.9354 |
| debil|rho095|h12 | 2SLS_aumentado_EHW | 5000 | 0.0052 | 0.9948 | 0.9732 | 0.0062 | NO APTO | no fiable | 2.9354 |
| debil|rho095|h12 | AR_NeweyWest_h+1 | 5000 | 0.1068 | 0.8932 | 0.8786 | 0.1124 | NO APTO | con valor crítico corregido | 2.9354 |
| debil|rho095|h12 | AR_aumentado_EHW | 5000 | 0.0518 | 0.9482 | 0.9418 | 0.0604 | APTO | apta | 2.9354 |
| debil|rho099|h4 | 2SLS_NeweyWest_h+1 | 5000 | 0.0348 | 0.9652 | 0.9026 | 0.0210 | NO APTO | con valor crítico corregido | 3.2342 |
| debil|rho099|h4 | 2SLS_aumentado_EHW | 5000 | 0.0268 | 0.9732 | 0.9178 | 0.0124 | NO APTO | con valor crítico corregido | 3.2342 |
| debil|rho099|h4 | AR_NeweyWest_h+1 | 5000 | 0.0714 | 0.9286 | 0.9280 | 0.1496 | APTO | con valor crítico corregido | 3.2342 |
| debil|rho099|h4 | AR_aumentado_EHW | 5000 | 0.0548 | 0.9452 | 0.9432 | 0.1182 | APTO | apta | 3.2342 |
| debil|rho099|h8 | 2SLS_NeweyWest_h+1 | 5000 | 0.0304 | 0.9696 | 0.8950 | 0.0232 | NO APTO | con valor crítico corregido | 3.1338 |
| debil|rho099|h8 | 2SLS_aumentado_EHW | 5000 | 0.0136 | 0.9864 | 0.9358 | 0.0072 | NO APTO | no fiable | 3.1338 |
| debil|rho099|h8 | AR_NeweyWest_h+1 | 5000 | 0.0842 | 0.9158 | 0.9088 | 0.1186 | NO APTO | con valor crítico corregido | 3.1338 |
| debil|rho099|h8 | AR_aumentado_EHW | 5000 | 0.0490 | 0.9510 | 0.9402 | 0.0750 | APTO | apta | 3.1338 |
| debil|rho099|h12 | 2SLS_NeweyWest_h+1 | 5000 | 0.0340 | 0.9660 | 0.8812 | 0.0276 | NO APTO | con valor crítico corregido | 3.0264 |
| debil|rho099|h12 | 2SLS_aumentado_EHW | 5000 | 0.0106 | 0.9894 | 0.9336 | 0.0066 | NO APTO | no fiable | 3.0264 |
| debil|rho099|h12 | AR_NeweyWest_h+1 | 5000 | 0.1112 | 0.8888 | 0.8748 | 0.1208 | NO APTO | con valor crítico corregido | 3.0264 |
| debil|rho099|h12 | AR_aumentado_EHW | 5000 | 0.0546 | 0.9454 | 0.9342 | 0.0642 | APTO | apta | 3.0264 |
| fuerte|rho095_gauss|h4 | 2SLS_NeweyWest_h+1 | 5000 | 0.0840 | 0.9160 | 0.8528 | 0.9420 | NO APTO | con valor crítico corregido | 30.9704 |
| fuerte|rho095_gauss|h4 | 2SLS_aumentado_EHW | 5000 | 0.0692 | 0.9308 | 0.8850 | 0.9100 | NO APTO | con valor crítico corregido | 30.9704 |
| fuerte|rho095_gauss|h4 | AR_NeweyWest_h+1 | 5000 | 0.0780 | 0.9220 | 0.8826 | 0.9418 | NO APTO | con valor crítico corregido | 30.9704 |
| fuerte|rho095_gauss|h4 | AR_aumentado_EHW | 5000 | 0.0618 | 0.9382 | 0.9090 | 0.9092 | NO APTO | con valor crítico corregido | 30.9704 |
| fuerte|rho095_gauss|h8 | 2SLS_NeweyWest_h+1 | 5000 | 0.1176 | 0.8824 | 0.7904 | 0.4912 | NO APTO | con valor crítico corregido | 29.5920 |
| fuerte|rho095_gauss|h8 | 2SLS_aumentado_EHW | 5000 | 0.0760 | 0.9240 | 0.8444 | 0.3824 | NO APTO | con valor crítico corregido | 29.5920 |
| fuerte|rho095_gauss|h8 | AR_NeweyWest_h+1 | 5000 | 0.1088 | 0.8912 | 0.8092 | 0.4798 | NO APTO | con valor crítico corregido | 29.5920 |
| fuerte|rho095_gauss|h8 | AR_aumentado_EHW | 5000 | 0.0644 | 0.9356 | 0.8710 | 0.3664 | NO APTO | con valor crítico corregido | 29.5920 |
| fuerte|rho095_gauss|h12 | 2SLS_NeweyWest_h+1 | 5000 | 0.1380 | 0.8620 | 0.7516 | 0.2746 | NO APTO | con valor crítico corregido | 28.2571 |
| fuerte|rho095_gauss|h12 | 2SLS_aumentado_EHW | 5000 | 0.0796 | 0.9204 | 0.8282 | 0.1654 | NO APTO | con valor crítico corregido | 28.2571 |
| fuerte|rho095_gauss|h12 | AR_NeweyWest_h+1 | 5000 | 0.1316 | 0.8684 | 0.7728 | 0.2678 | NO APTO | con valor crítico corregido | 28.2571 |
| fuerte|rho095_gauss|h12 | AR_aumentado_EHW | 5000 | 0.0742 | 0.9258 | 0.8454 | 0.1526 | NO APTO | con valor crítico corregido | 28.2571 |
| moderada|rho095_gauss|h4 | 2SLS_NeweyWest_h+1 | 5000 | 0.0608 | 0.9392 | 0.8878 | 0.3102 | NO APTO | con valor crítico corregido | 11.4075 |
| moderada|rho095_gauss|h4 | 2SLS_aumentado_EHW | 5000 | 0.0442 | 0.9558 | 0.9096 | 0.2450 | NO APTO | con valor crítico corregido | 11.4075 |
| moderada|rho095_gauss|h4 | AR_NeweyWest_h+1 | 5000 | 0.0762 | 0.9238 | 0.9126 | 0.4540 | NO APTO | con valor crítico corregido | 11.4075 |
| moderada|rho095_gauss|h4 | AR_aumentado_EHW | 5000 | 0.0584 | 0.9416 | 0.9374 | 0.3912 | APTO | apta | 11.4075 |
| moderada|rho095_gauss|h8 | 2SLS_NeweyWest_h+1 | 5000 | 0.0692 | 0.9308 | 0.8636 | 0.1508 | NO APTO | con valor crítico corregido | 10.9059 |
| moderada|rho095_gauss|h8 | 2SLS_aumentado_EHW | 5000 | 0.0362 | 0.9638 | 0.9030 | 0.0938 | NO APTO | con valor crítico corregido | 10.9059 |
| moderada|rho095_gauss|h8 | AR_NeweyWest_h+1 | 5000 | 0.0950 | 0.9050 | 0.8784 | 0.2160 | NO APTO | con valor crítico corregido | 10.9059 |
| moderada|rho095_gauss|h8 | AR_aumentado_EHW | 5000 | 0.0554 | 0.9446 | 0.9194 | 0.1528 | NO APTO | con valor crítico corregido | 10.9059 |
| moderada|rho095_gauss|h12 | 2SLS_NeweyWest_h+1 | 5000 | 0.0842 | 0.9158 | 0.8446 | 0.1174 | NO APTO | con valor crítico corregido | 10.4121 |
| moderada|rho095_gauss|h12 | 2SLS_aumentado_EHW | 5000 | 0.0374 | 0.9626 | 0.9046 | 0.0552 | NO APTO | con valor crítico corregido | 10.4121 |
| moderada|rho095_gauss|h12 | AR_NeweyWest_h+1 | 5000 | 0.1154 | 0.8846 | 0.8448 | 0.1630 | NO APTO | con valor crítico corregido | 10.4121 |
| moderada|rho095_gauss|h12 | AR_aumentado_EHW | 5000 | 0.0604 | 0.9396 | 0.9062 | 0.0938 | NO APTO | con valor crítico corregido | 10.4121 |
| debil|rho095_gauss|h4 | 2SLS_NeweyWest_h+1 | 5000 | 0.0250 | 0.9750 | 0.9184 | 0.0208 | NO APTO | con valor crítico corregido | 3.3792 |
| debil|rho095_gauss|h4 | 2SLS_aumentado_EHW | 5000 | 0.0202 | 0.9798 | 0.9386 | 0.0098 | NO APTO | con valor crítico corregido | 3.3792 |
| debil|rho095_gauss|h4 | AR_NeweyWest_h+1 | 5000 | 0.0646 | 0.9354 | 0.9234 | 0.1618 | APTO | con valor crítico corregido | 3.3792 |
| debil|rho095_gauss|h4 | AR_aumentado_EHW | 5000 | 0.0520 | 0.9480 | 0.9378 | 0.1322 | APTO | apta | 3.3792 |
| debil|rho095_gauss|h8 | 2SLS_NeweyWest_h+1 | 5000 | 0.0234 | 0.9766 | 0.9320 | 0.0212 | NO APTO | con valor crítico corregido | 3.2546 |
| debil|rho095_gauss|h8 | 2SLS_aumentado_EHW | 5000 | 0.0104 | 0.9896 | 0.9612 | 0.0062 | NO APTO | no fiable | 3.2546 |
| debil|rho095_gauss|h8 | AR_NeweyWest_h+1 | 5000 | 0.0874 | 0.9126 | 0.8998 | 0.1144 | NO APTO | con valor crítico corregido | 3.2546 |
| debil|rho095_gauss|h8 | AR_aumentado_EHW | 5000 | 0.0550 | 0.9450 | 0.9374 | 0.0748 | APTO | apta | 3.2546 |
| debil|rho095_gauss|h12 | 2SLS_NeweyWest_h+1 | 5000 | 0.0256 | 0.9744 | 0.9424 | 0.0278 | NO APTO | con valor crítico corregido | 3.1360 |
| debil|rho095_gauss|h12 | 2SLS_aumentado_EHW | 5000 | 0.0076 | 0.9924 | 0.9748 | 0.0058 | NO APTO | no fiable | 3.1360 |
| debil|rho095_gauss|h12 | AR_NeweyWest_h+1 | 5000 | 0.1070 | 0.8930 | 0.8840 | 0.1152 | NO APTO | con valor crítico corregido | 3.1360 |
| debil|rho095_gauss|h12 | AR_aumentado_EHW | 5000 | 0.0520 | 0.9480 | 0.9418 | 0.0578 | APTO | apta | 3.1360 |

## Notas

- El contraste principal de E7-R1 es h = 8; h = 4 y 12 están en la tabla (columna h). Las filas «rho095_gauss» (sorpresa gaussiana) son diagnóstico y no entran en el veredicto.
- El 2SLS (t) no es válido con instrumento débil (F ≈ 3): se evalúa solo con F >= 10 para el veredicto; el AR es el que decide con F < 10.
- AR_acotado: proporción de réplicas con conjunto AR acotado (informativo) bajo la alternativa.
- Sesgo de muestra finita de la LP (T = 108): con la alternativa, la mediana del estimador queda un 10 %, 22 % y 38 % por debajo de la verdad en valor absoluto a h = 4, 8 y 12 con instrumento fuerte (un 24-53 % con F ≈ 3), y es casi nulo con T = 1.000; es el mismo atenuamiento de la LP con series persistentes que describe la literatura (Herbst y Johannsen), y explica que la cobertura bajo la alternativa (0,72-0,93) sea peor que bajo el nulo (0,91-0,95 con el AR aumentado). Con la sorpresa gaussiana sin meses vacíos los resultados son los mismos: las colas pesadas no son la causa.

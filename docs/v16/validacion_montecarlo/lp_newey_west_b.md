# lp_newey_west_b · Q5-p y Q5-a (proyección local nacional, Newey-West con b fija)

## Proceso generador (declarado antes de simular)
- **Estructura real (solo estructura):** serie nacional trimestral, T = 100 (la ventana de Q5 es 1999T1/2002T1-2026T2, 98-110 trimestres); horizontes h = [1, 4, 8, 12].
- **Choque:** ε_t i.i.d. N(0,1), exógeno (equivale a la sorpresa estandarizada de Jarociński-Karadi agregada a trimestre; sin autocorrelación ni heterocedasticidad).
- **Resultado:** y_t = ρ·y_(t-1) + θ·ε_t + σ_u·u_t, u_t i.i.d. N(0,1), σ_u = 0.01 (log, trimestral), con 100 periodos de calentamiento. ρ ∈ [0.9, 0.95, 0.98] (persistencia alta, intervalo 0,90-0,98 de la tarea).
  Respuesta verdadera a h: β_h = θ·ρ^h. Nulo: θ = 0. Alternativa: θ = -0.006/ρ^4, de modo que β_4 = -0.006 (−0,6 % por DT, magnitud de referencia de Q5-p) y β_h = θρ^h para el resto.
- **Estimación:** para cada h, MCO de y_(t+h) sobre constante, ε_t, 4 rezagos de ε y 4 rezagos de y (n = T − h − 4 observaciones). Coeficiente de interés: el de ε_t.
- **Inferencia principal:** Newey-West con núcleo de Bartlett y ancho de banda fijo M = b·n con b = 0.2 (Kiefer-Vogelsang), valor crítico bilateral al 5 % de la distribución límite de b fija
  simulada (b = 0.2: 2.538). Declarado antes de simular; se informa también b = 1,0 (valor crítico 4.793) y Newey-West convencional (M = 4, normal) como referencias, no candidatas.
- **Pocos clusters / dependencia transversal:** no aplica (serie nacional única). **T corto:** n entre 84 y 95.
- **Alternativa nombrada en el punto 3:** ninguna distinta (b fija es la principal). Si algún (ρ, h) falla, el veredicto es «NO APTO» para la combinación; con fallos «NO APTO → diseño solo descriptivo».
- **Criterio:** en cada una de las 12 combinaciones (ρ, h): tamaño en [0,04; 0,06] con R ≥ 2.000 (aquí R = 10.000, para que el error Monte Carlo ≈ 0,002 no domine el intervalo) y cobertura en [0,92; 0,97] bajo la alternativa.
  El veredicto global es APTO solo si pasan las 12 combinaciones.

<!-- RESULTADOS -->
## Resultados (R = 10000 por ρ; semilla 20261010, k = 34)

| rho | h | inferencia | R | tamano_5pct | tamano_ic95 | cobertura_95 | potencia | sesgo | rmse | beta_verdadero |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.9000 | 1 | b=0.2 | 10000 | 0.0698 | [0.0648, 0.0748] | 0.9270 | 0.9830 | 0.0002 | 0.0018 | -0.0082 |
| 0.9000 | 1 | b=1.0 | 10000 | 0.0653 | [0.0605, 0.0701] | 0.9301 | 0.9334 | 0.0002 | 0.0018 | -0.0082 |
| 0.9000 | 1 | NW M=4 normal | 10000 | 0.0883 | [0.0827, 0.0939] | 0.9030 | 0.9960 | 0.0002 | 0.0018 | -0.0082 |
| 0.9000 | 4 | b=0.2 | 10000 | 0.0834 | [0.078, 0.0888] | 0.8941 | 0.5313 | 0.0007 | 0.0028 | -0.0060 |
| 0.9000 | 4 | b=1.0 | 10000 | 0.0780 | [0.0727, 0.0833] | 0.9002 | 0.4543 | 0.0007 | 0.0028 | -0.0060 |
| 0.9000 | 4 | NW M=4 normal | 10000 | 0.1081 | [0.102, 0.1142] | 0.8725 | 0.6271 | 0.0007 | 0.0028 | -0.0060 |
| 0.9000 | 8 | b=0.2 | 10000 | 0.0871 | [0.0816, 0.0926] | 0.8643 | 0.1833 | 0.0010 | 0.0033 | -0.0039 |
| 0.9000 | 8 | b=1.0 | 10000 | 0.0828 | [0.0774, 0.0882] | 0.8778 | 0.1663 | 0.0010 | 0.0033 | -0.0039 |
| 0.9000 | 8 | NW M=4 normal | 10000 | 0.1111 | [0.1049, 0.1173] | 0.8356 | 0.2395 | 0.0010 | 0.0033 | -0.0039 |
| 0.9000 | 12 | b=0.2 | 10000 | 0.0894 | [0.0838, 0.095] | 0.8772 | 0.1087 | 0.0011 | 0.0035 | -0.0026 |
| 0.9000 | 12 | b=1.0 | 10000 | 0.0800 | [0.0747, 0.0853] | 0.8862 | 0.0990 | 0.0011 | 0.0035 | -0.0026 |
| 0.9000 | 12 | NW M=4 normal | 10000 | 0.1160 | [0.1097, 0.1223] | 0.8418 | 0.1430 | 0.0011 | 0.0035 | -0.0026 |
| 0.9500 | 1 | b=0.2 | 10000 | 0.0642 | [0.0594, 0.069] | 0.9313 | 0.9560 | 0.0002 | 0.0017 | -0.0070 |
| 0.9500 | 1 | b=1.0 | 10000 | 0.0601 | [0.0554, 0.0648] | 0.9372 | 0.8769 | 0.0002 | 0.0017 | -0.0070 |
| 0.9500 | 1 | NW M=4 normal | 10000 | 0.0843 | [0.0789, 0.0897] | 0.9095 | 0.9829 | 0.0002 | 0.0017 | -0.0070 |
| 0.9500 | 4 | b=0.2 | 10000 | 0.0749 | [0.0697, 0.0801] | 0.8962 | 0.5220 | 0.0007 | 0.0028 | -0.0060 |
| 0.9500 | 4 | b=1.0 | 10000 | 0.0721 | [0.067, 0.0772] | 0.9032 | 0.4461 | 0.0007 | 0.0028 | -0.0060 |
| 0.9500 | 4 | NW M=4 normal | 10000 | 0.1014 | [0.0955, 0.1073] | 0.8719 | 0.6193 | 0.0007 | 0.0028 | -0.0060 |
| 0.9500 | 8 | b=0.2 | 10000 | 0.0829 | [0.0775, 0.0883] | 0.8632 | 0.2373 | 0.0012 | 0.0035 | -0.0049 |
| 0.9500 | 8 | b=1.0 | 10000 | 0.0784 | [0.0731, 0.0837] | 0.8790 | 0.2078 | 0.0012 | 0.0035 | -0.0049 |
| 0.9500 | 8 | NW M=4 normal | 10000 | 0.1102 | [0.1041, 0.1163] | 0.8359 | 0.3008 | 0.0012 | 0.0035 | -0.0049 |
| 0.9500 | 12 | b=0.2 | 10000 | 0.0876 | [0.0821, 0.0931] | 0.8457 | 0.1429 | 0.0015 | 0.0040 | -0.0040 |
| 0.9500 | 12 | b=1.0 | 10000 | 0.0808 | [0.0755, 0.0861] | 0.8576 | 0.1279 | 0.0015 | 0.0040 | -0.0040 |
| 0.9500 | 12 | NW M=4 normal | 10000 | 0.1155 | [0.1092, 0.1218] | 0.8094 | 0.1839 | 0.0015 | 0.0040 | -0.0040 |
| 0.9800 | 1 | b=0.2 | 10000 | 0.0686 | [0.0636, 0.0736] | 0.9240 | 0.9203 | 0.0003 | 0.0017 | -0.0064 |
| 0.9800 | 1 | b=1.0 | 10000 | 0.0643 | [0.0595, 0.0691] | 0.9281 | 0.8340 | 0.0003 | 0.0017 | -0.0064 |
| 0.9800 | 1 | NW M=4 normal | 10000 | 0.0884 | [0.0828, 0.094] | 0.9016 | 0.9634 | 0.0003 | 0.0017 | -0.0064 |
| 0.9800 | 4 | b=0.2 | 10000 | 0.0788 | [0.0735, 0.0841] | 0.8894 | 0.5035 | 0.0008 | 0.0029 | -0.0060 |
| 0.9800 | 4 | b=1.0 | 10000 | 0.0725 | [0.0674, 0.0776] | 0.8964 | 0.4236 | 0.0008 | 0.0029 | -0.0060 |
| 0.9800 | 4 | NW M=4 normal | 10000 | 0.1060 | [0.1, 0.112] | 0.8638 | 0.6063 | 0.0008 | 0.0029 | -0.0060 |
| 0.9800 | 8 | b=0.2 | 10000 | 0.0874 | [0.0819, 0.0929] | 0.8472 | 0.2594 | 0.0015 | 0.0038 | -0.0055 |
| 0.9800 | 8 | b=1.0 | 10000 | 0.0787 | [0.0734, 0.084] | 0.8601 | 0.2298 | 0.0015 | 0.0038 | -0.0055 |
| 0.9800 | 8 | NW M=4 normal | 10000 | 0.1116 | [0.1054, 0.1178] | 0.8143 | 0.3270 | 0.0015 | 0.0038 | -0.0055 |
| 0.9800 | 12 | b=0.2 | 10000 | 0.0925 | [0.0868, 0.0982] | 0.8130 | 0.1739 | 0.0020 | 0.0045 | -0.0051 |
| 0.9800 | 12 | b=1.0 | 10000 | 0.0856 | [0.0801, 0.0911] | 0.8308 | 0.1507 | 0.0020 | 0.0045 | -0.0051 |
| 0.9800 | 12 | NW M=4 normal | 10000 | 0.1217 | [0.1153, 0.1281] | 0.7750 | 0.2171 | 0.0020 | 0.0045 | -0.0051 |


**Veredicto: NO APTO → diseño solo descriptivo.**

Combinaciones (ρ, h) que fallan con b = 0,2:
- rho=0.9, h=1: tamaño 0.0698 fuera de [0.04; 0.06]
- rho=0.9, h=4: tamaño 0.0834 fuera de [0.04; 0.06]; cobertura 0.8941 fuera de [0.92; 0.97]
- rho=0.9, h=8: tamaño 0.0871 fuera de [0.04; 0.06]; cobertura 0.8643 fuera de [0.92; 0.97]
- rho=0.9, h=12: tamaño 0.0894 fuera de [0.04; 0.06]; cobertura 0.8772 fuera de [0.92; 0.97]
- rho=0.95, h=1: tamaño 0.0642 fuera de [0.04; 0.06]
- rho=0.95, h=4: tamaño 0.0749 fuera de [0.04; 0.06]; cobertura 0.8962 fuera de [0.92; 0.97]
- rho=0.95, h=8: tamaño 0.0829 fuera de [0.04; 0.06]; cobertura 0.8632 fuera de [0.92; 0.97]
- rho=0.95, h=12: tamaño 0.0876 fuera de [0.04; 0.06]; cobertura 0.8457 fuera de [0.92; 0.97]
- rho=0.98, h=1: tamaño 0.0686 fuera de [0.04; 0.06]
- rho=0.98, h=4: tamaño 0.0788 fuera de [0.04; 0.06]; cobertura 0.8894 fuera de [0.92; 0.97]
- rho=0.98, h=8: tamaño 0.0874 fuera de [0.04; 0.06]; cobertura 0.8472 fuera de [0.92; 0.97]
- rho=0.98, h=12: tamaño 0.0925 fuera de [0.04; 0.06]; cobertura 0.8130 fuera de [0.92; 0.97]

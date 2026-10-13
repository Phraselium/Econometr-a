# M5: instrumentos externos (IV1 JK, IV2 migratorio, IV3 Bartik)

Capa: C3 solo donde se cumplen los cuatro requisitos de §6; si no, C4 (asociacion, sin lenguaje causal).

## Hipotesis (Holm, familia {H8-5, H8-6, H8-7})

p AR unilateral con el signo A PRIORI de la primera etapa (pi > 0); beta (cociente de dos estimaciones) no se lee como evidencia.

| id | pi (t) | F | forma reducida: signo (t) | AR p unilateral | p Holm | F>=10 | AR excl. 0 | pretend. | permutacion instr. | capa |
|---|---|---|---|---|---|---|---|---|---|---|
| H8-5 | -0.930 (-1.35) | 1.83 | + (0.60; esperado -) | 0.724 | 1.000 | no | no | si | no | C4 |
| H8-6 | -0.486 (-0.88) | 0.77 | + (0.34; esperado -) | 0.635 | 1.000 | no | no | si | no | C4 |
| H8-7 | 0.265 (0.22) | 0.05 | - (-0.09; esperado +) | 0.536 | 1.000 | no | no | si | no | C4 |

Detalle por hipotesis: H8-5: regresion agregada h=4-8 (la de F y AR): pi=-0.930 (t=-1.35; esperado > 0), F=1.83; forma reducida t_AR(0)=0.60 (signo esperado negativo); n=102; p_perm=0.610; AR acotado=False; no respaldada tras Holm (instrumento no supera C3) / H8-6: regresion agregada h=4-8 (la de F y AR): pi=-0.486 (t=-0.88; esperado > 0), F=0.77; forma reducida t_AR(0)=0.34 (signo esperado negativo); n=88; p_perm=0.798; AR acotado=False; no respaldada tras Holm (instrumento no supera C3) / H8-7: regresion agregada anual h=1-2: pi=0.265 (t=0.22; esperado > 0), F=0.05; forma reducida t_AR(0)=-0.09 (signo esperado positivo); n=20; p_perm=1.000; AR acotado=False; no respaldada tras Holm (instrumento no supera C3)

## IV3 (Bartik, panel 17 CCAA, exploratorio; BH)

- Alquiler h=1-2: beta=-0.425, AR95=[-46856.54, 46855.69], F=1.0, p AR=0.197, cumple C3=False.
- Precio h=1-2: beta=-1.413, AR95=[-310875.88, 310873.05], F=0.6, p AR=0.649, cumple C3=False.
- Rotemberg (pesos principales): B-E 1.75; G-I -0.41; F -0.30; A -0.25.

## IV2b (instrumento sin normalizar; exploratoria, ANADIDA TRAS CONSTRUIR EL INSTRUMENTO)

- Alquiler h=1-2: beta=-1.007, F=2.1, p AR unilateral (signo a priori)=0.730, AR acotado=False, cumple C3=False. Fuera de Holm.

## Atribucion lpiv y regla de §9

Las filas `lpiv` de atribucion.csv son C4 informativas: `vota_s9` = no cuando F < 10 y el AR 68 % no esta acotado (se abstiene) y siempre en IV3 (efecto relativo entre CCAA). `pct_total` queda vacio si |variacion observada| < 1 pp.

## Limites

- Instrumento valido solo si es exogeno (no verificable): los shocks JK pueden contener informacion del BCE sobre la economia (JK los depuran con signos).
- IV2: shocks comunes a la UE (ciclo) pueden afectar a Espana; llegadas = total Eurostat; cuotas = stock 2002; frecuencia anual (n pequeno).
- IV3: efectos relativos entre CCAA, no nacionales; posibles rupturas de serie en la EPA/LFS.
- Atribucion lpiv: multiplicador constante extrapolado a toda la variacion de la endogena; bandas AR.
- Fuera de muestra: no aplica.
- La permutacion del instrumento (antes «placebo») contrasta la significacion de la forma reducida; no es una prueba independiente de validez del instrumento. Las pretendencias tampoco lo son (baja potencia).


# M5: instrumentos externos (IV1 JK, IV2 migratorio, IV3 Bartik)

Capa: C3 solo donde se cumplen los cuatro requisitos de §6; si no, C4 (asociacion, sin lenguaje causal).

## Hipotesis (Holm, familia {H8-5, H8-6, H8-7})

| id | estimacion | AR p unilateral | p Holm | F | AR excl. 0 | pretend. | placebo | capa |
|---|---|---|---|---|---|---|---|---|
| H8-5 | -8.776 | 0.276 | 0.827 | no | no | si | no | C4 |
| H8-6 | -2.912 | 0.365 | 0.827 | no | no | si | no | C4 |
| H8-7 | -0.511 | 0.536 | 0.827 | no | no | si | no | C4 |

Detalle por hipotesis: H8-5: pi_1a_etapa=-1.402 (t=-1.66; esperado > 0); F=1.83; n=102; p_perm=0.610; AR acotado=False; no respaldada tras Holm (instrumento no supera C3) / H8-6: pi_1a_etapa=-1.402 (t=-1.66; esperado > 0); F=0.77; n=88; p_perm=0.798; AR acotado=False; no respaldada tras Holm (instrumento no supera C3) / H8-7: F=0.05; n=20; p_perm=1.000; AR acotado=False; anual, h=1-2; no respaldada tras Holm (instrumento no supera C3)

## IV3 (Bartik, panel 17 CCAA, exploratorio; BH)

- Alquiler h=1-2: beta=-0.425, AR95=[-46856.54, 46855.69], F=1.0, p AR=0.197, cumple C3=False.
- Precio h=1-2: beta=-1.413, AR95=[-310875.88, 310873.05], F=0.6, p AR=0.649, cumple C3=False.
- Rotemberg (pesos principales): B-E 1.75; G-I -0.41; F -0.30; A -0.25.

## Limites

- Instrumento valido solo si es exogeno (no verificable): los shocks JK pueden contener informacion del BCE sobre la economia (JK los depuran con signos).
- IV2: shocks comunes a la UE (ciclo) pueden afectar a Espana; llegadas = total Eurostat; cuotas = stock 2002; frecuencia anual (n pequeno).
- IV3: efectos relativos entre CCAA, no nacionales; posibles rupturas de serie en la EPA/LFS.
- Atribucion lpiv: multiplicador constante extrapolado a toda la variacion de la endogena; bandas AR.
- Fuera de muestra: no aplica.

Tiempo de ejecucion: 52 s.

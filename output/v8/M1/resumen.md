# M1: factor comun de las 17 CCAA (C4, EXPLORATORIO (C4))

**H8-8** (cuota del 1.er componente > 50 % en cada periodo; PCA, bootstrap por bloques; IUT): cuotas {'P1': 0.6474, 'P2': 0.4527, 'P3': 0.5958, 'P4': 0.455, 'P5': 0.9279}; p max = 0.6690; **p Holm = 0.6690**. DFM-ML coincide en >50 %: False. Con N=17 y T pequeno la cuota esta sesgada al alza; ver `cuota_azar_media` y `p_vs_azar` en `cuota_varianza.csv`.

**H8-9** (corr. factor comun - HPI EA19 interanual, 2006T1+): r = 0.598 (IC95 0.14 a 0.86); p = 0.0100; **p Holm = 0.0200**. EA19 incluye Espana (sesgo al alza); proxy sin ES (DE, FR, IT, NL, PT) y EA19 real en `correlaciones_h89.csv`.

Cuota en ventanas de 40 trimestres: 0.48-0.92 (`evolucion_ventanas.csv`). Correlaciones por periodo (exploratorio, BH q=0,10): `correlaciones_periodo.csv`.

**Parte europea del crecimiento nacional** (`atribucion.csv`, metodo factor_comun, C4, con bandas): P1 7.4 pp [-16.7, 11.0]; P2 -15.3 pp [-27.9, -5.0]; P3 0.8 pp [-8.4, 6.6]; P4 1.4 pp [-5.3, 8.1]; P5 -3.3 pp [-9.8, 5.1].

**Limites.** C4: asociacion estadistica; el factor es un resumen de comovimiento, sin interpretacion causal ni estructural. Muestras por periodo cortas (P4 = 9 trimestres): con N = 17 y T pequeno la cuota del 1.er componente esta sesgada al alza incluso sin factor comun real.
Alquiler por CCAA: IPC alquiler desde 2007 (sin P1). Fuera de muestra no aplica.

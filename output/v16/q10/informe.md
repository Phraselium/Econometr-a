# Q10 · Predicción nacional frente a AR(4) y ECM v1 (C4, pendiente de evaluación sellada)

**Capa.** C4. Predicción, no causalidad. DM-HLN y Clark-West son NO APTOS (tamaño 0,002 y 0,033): se publica **solo la reducción puntual del ECM**, sin p-valor ni IC; GW y MCS no están validados y no se usan. Ventana expansiva (30 trimestres iniciales), misma muestra de objetivos para todos los modelos; objetivos directos con información hasta el origen. Indicadores mensuales en su última edición (límite declarado): el nowcasting puede parecer mejor de lo que sería en directo.

## Q10-1 · Δlog IPV nacional (h = 1)
<a id="q10-1"></a>Modelo MIDAS frente a AR(4): reducción puntual del ECM **-18,3 %** (2016Q1-2026Q2, n = 38); relevancia mínima del 10 %: no alcanzada (descriptivo).
RMSE: AR4 0,01127; RW_deriva 0,02273; AR4_S 0,01356; MIDAS 0,01225; ECM_v1 0,01727.
Reducción frente al AR(4): RW_deriva -307,3 %; AR4_S -44,9 %; MIDAS -18,3 %; ECM_v1 -134,9 %.
Misma muestra frente al ECM v1: AR4 57,4 %; RW_deriva -73,3 %; AR4_S 38,3 %; MIDAS 49,7 %.
- h1_sin2020: n = 32; RW_deriva -349,4 %; AR4_S -50,1 %; MIDAS -2,4 %; ECM_v1 -142,0 %
- h4: n = 35; RW_deriva -280,0 %; AR4_S -1,3 %; MIDAS -9,1 %; ECM_v1 -153,5 %
- h4_sin2020: n = 29; RW_deriva -276,4 %; AR4_S 2,8 %; MIDAS 0,5 %; ECM_v1 -154,0 %
Intervalos conformes 90 % (h = 1): cobertura empírica 0,77 (n = 26).

## Q10-2 · Δlog IPC de alquiler nacional (h = 1)
<a id="q10-2"></a>Modelo NOWCAST frente a AR(4): reducción puntual del ECM **-30,3 %** (2011Q1-2026Q2, n = 58); relevancia mínima del 10 %: no alcanzada (descriptivo).
RMSE: AR4 0,00115; RW_deriva 0,00451; AR4_S 0,00133; NOWCAST 0,00131.
Reducción frente al AR(4): RW_deriva -1446,9 %; AR4_S -34,5 %; NOWCAST -30,3 %.
No existe ECM v1 para esta variable.
- h1_sin2020: n = 52; RW_deriva -1576,2 %; AR4_S -25,2 %; NOWCAST -34,3 %
- h4: n = 55; RW_deriva -1145,4 %; AR4_S 10,9 %; NOWCAST -5,4 %
- h4_sin2020: n = 49; RW_deriva -1171,3 %; AR4_S 12,3 %; NOWCAST -5,3 %
Intervalos conformes 90 % (h = 1): cobertura empírica 0,89 (n = 46).

## Q10-3 · Δlog compraventas nacional (h = 1)
<a id="q10-3"></a>Modelo MIDAS frente a AR(4): reducción puntual del ECM **40,6 %** (2016Q1-2026Q2, n = 42); relevancia mínima del 10 %: alcanzada (descriptivo).
RMSE: AR4 0,13091; RW_deriva 0,13003; AR4_S 0,13266; MIDAS 0,10086.
Reducción frente al AR(4): RW_deriva 1,3 %; AR4_S -2,7 %; MIDAS 40,6 %.
No existe ECM v1 para esta variable.
- h1_sin2020: n = 36; RW_deriva -77,2 %; AR4_S -28,1 %; MIDAS -3,0 %
- h4: n = 39; RW_deriva 6,8 %; AR4_S -1,6 %; MIDAS 3,2 %
- h4_sin2020: n = 33; RW_deriva 1,7 %; AR4_S -5,4 %; MIDAS 11,0 %
Intervalos conformes 90 % (h = 1): cobertura empírica 0,83 (n = 30).

## Regla de hallazgo
(a) sin p-valor (NO APTO): no evaluable; (b) sin magnitud inferencial: la reducción puntual se compara con la relevancia mínima del 10 %, solo descriptiva; (c) sellada: pendiente (H5 de V15 sigue siendo la confirmatoria). Resultado: C4 descriptivo.

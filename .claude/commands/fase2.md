---
description: F2 Nacional — raíces unitarias, cointegración (EG, Johansen, ARDL bounds), ECM, diagnósticos y fuera de muestra; para en la puerta.
---
Fase 2. Delega en `econometrician` (src/f2_nacional.py): ADF/KPSS/Zivot-Andrews; Engle-Granger, Johansen, ARDL-bounds (PSS 2001);
ECM replicando el punto de partida (2008T1-2025T4) y ampliado; búsqueda por R2aj con HAC(4), AIC/BIC y RMSE en ventana expansiva, todos en la MISMA muestra;
DW, BG, BP, JB, RESET, CUSUM, Chow (2014T1, 2020T1, 2022T3), Bai-Perron, VIF. Registro de búsqueda y corrección. Para en la puerta y propone `/revisar`.
$ARGUMENTS

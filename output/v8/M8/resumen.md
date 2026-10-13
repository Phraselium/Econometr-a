# M8: descomposicion regional (C4, exploratorio)

**17 CCAA, cuota comun** (R2 de y sobre el factor comun; mediana entre CCAA): {"alquiler": {"P1": NaN, "P2": 0.961, "P3": 0.858, "P4": 0.998, "P5": 0.982}, "compra": {"P1": 0.685, "P2": 0.462, "P3": 0.619, "P4": 0.465, "P5": 0.936}}. Coeficientes del factor por CCAA con p BH<0,10: 145 de 153. Detalle por CCAA/periodo en `cuota_ccaa.csv` (con bandas).

**Panel FE (Driscoll-Kraay)** por periodo con covariables regionales disponibles (`paneles_resumen.csv`, `coeficientes.csv`); beta del factor comun: {'compra_P1': 1.009, 'compra_P2': 0.894, 'compra_P3': 0.973, 'compra_P4': 1.177, 'compra_P5': 0.977, 'alquiler_P2': 0.961, 'alquiler_P3': 0.988, 'alquiler_P4': 1.003, 'alquiler_P5': 1.0}. Contribuciones por CCAA con bandas bootstrap en `atribucion.csv` (metodo regional_panel; factores demografia, empleo_renta, oferta, demanda_externa, factor_comun, residuo). LP panel: 118 de 269 coeficientes (impulso x periodo x h) con p BH < 0,10.

**Comunitat Valenciana** (03, 12, 46) y **Valencia ciudad**: `cuota_cv.csv` (parte asociada al factor nacional y aporte adicional de la serie CV, cota superior porque incluye a la propia provincia), `cadena_territorial.csv` (identidad aritmetica Espana -> CV -> provincia -> ciudad), `descriptivo_cv.csv` (C1 solo con 2 fuentes concordantes). Muestras cortas (P4, P1 de Valencia ciudad desde 2006): C4 con aviso.

**Factor comun (J23).** La pendiente ~1 del factor comun es mecanica (el factor es la media transversal reescalada e incluye a la propia CCAA, 1/17) y los 'significativos tras BH' del factor comun tambien: es un resumen de comovimiento, no compite con los 7 factores en s9 (vota_s9 = no). contribucion_pp = media interanual x T/4, aproximacion de la variacion acumulada (suma de tasas trimestrales reales, log x100) del periodo; pct_total en %.

**Limites.** C4: asociacion estadistica condicional; sin lectura causal. Ecuaciones por CCAA y periodo con pocos trimestres (P4 = 9): bandas aproximadas. El factor comun y las covariables regionales son colineales por construccion (VIF en coeficientes.csv).
Turismo: 6 CCAA desde 2015T4 (sensibilidad). Alquiler por CCAA desde 2008 (sin P1).

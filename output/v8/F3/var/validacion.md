# V8-F3 grupo A (familia VAR): validacion por Monte Carlo (version corregida tras la revision F3)

Capa C4 (metodologico). Solo datos simulados; ningun dato real ni sellado. SEED = 20261010, un hilo, determinista (montecarlo.csv reproducible; los tiempos de computo van aparte en tiempos.json porque dependen de la maquina). Computo total de la ejecucion: 1621 s (27.0 min). Reproducir: `python3 src/v8/f3_montecarlo_var.py`. Resultados completos: `montecarlo.csv`. Referencias de metodo NO VERIFICADAS (sin acceso a Crossref). Las etiquetas se derivan de las cifras con reglas explicitas en `etiquetas()` (f3_montecarlo_var.py).

## Veredicto por herramienta

| Herramienta / componente | Etiqueta |
|---|---|
| BVAR-GLP (6 celdas GLP + 2 delta mixto) | **no apta** |
| BVAR-GLP (direccion del sesgo de las IRF) | **atenuadas hacia cero (atenuacion firmada > 0 en todas las celdas GLP)** |
| signos/ceros (mecanica: restricciones, FEVD, descomposicion historica) | **apta** |
| pesos de importancia propios (Haar condicionado a los ceros; no se afirman iguales a ARW) | **apta (invariancia al orden)** |
| signos/ceros, 4 variables solo impacto (inferencia: bandas y signo del impacto) | **apta** |
| signos/ceros PRE-REGISTRADO (7 var, T=88, h=0-1, 4 ceros): principal | **no apta (signo del impacto 0.78 o cobertura de la DH 0.92 fuera de reglas)** |
| signos/ceros PRE-REGISTRADO: variante V3 (solo impacto, sin q) | **no apta (signo del impacto 0.65 o cobertura de la DH 0.90 fuera de reglas)** |
| TVP-VAR-SV (convergencia y volatilidad) | **con reservas** |
| TVP-VAR-SV (deteccion de un cambio de coeficiente con T efectivo = 88) | **no apta (potencia y cobertura insuficientes con T efectivo = 88; ver kQ=0,10 y 0,30)** |
| VAR por regimenes, 2 regimenes de 59 obs. (ruptura CONOCIDA) | **no apta** |
| VAR por regimenes, 5 tramos reales (16, 22, 24, 9, 15; n=4, p=2; con huecos) | **no apta** |

Reglas (definidas por el ejecutor, algunas DESPUES de ver las cifras de F3; ver docs/v8/decisiones.md): cobertura 90 % en [0,85; 0,98] = nominal; [0,80; 0,99] = con reservas (BVAR) o >= 0,85 (signos); sesgo relativo IRF <= 10 % apta, <= 30 % con reservas; recuperacion del signo del impacto >= 90 %; deteccion >= 80 % y falsos positivos <= 15 %; viabilidad del muestreo: fraccion de theta con alguna rotacion aceptada >= 1 % y ESS >= 30.

## Cambios respecto a la primera version (revision F3: H1, H2, H4, H9, H10, H12)

- H4: `exog` (ficticias deterministas) en `retardos`, `estimar`, `logml`, `prediccion` y `descomposicion_historica`; varianza a priori laxa (1e6), igual que la constante; la parte determinista de la DH incluye las exogenas (`det_exog` las aísla). Test de identidad con exogenas; la configuracion pre-registrada se valida con ficticias de COVID y EPA 2021T1.
- H10: `delta` por variable (vector), por defecto 0 (antes 1). Las dummies de suma de coeficientes y de observacion inicial usan la media de las p primeras observaciones sin escalar por delta. Celdas con delta = 0 (por defecto), delta = 1 (sensibilidad) y mixto (0 en tasas, 1 en el nivel) en un DGP de tasas.
- H2: para cada theta se prueba un numero FIJO `rotaciones` de rotaciones y se conservan TODAS las aceptadas (nunca se reintenta hasta aceptar); asi la distribucion de theta entre las aceptadas es proporcional a p(theta) P(S|theta).
- H1/H16: validacion de la configuracion pre-registrada (7 variables, T = 88, p = 2, signos en h = 0-1, 4 ceros en la fila de poblacion, 2 shocks sin identificar) y de la variante V3 (solo impacto).
- H9: `var_regimenes` admite tramos no contiguos (`tramos=[(ini, fin), ...]`) y se valida con 5 tramos de 16, 22, 24, 9 y 15 trimestres y huecos de transicion.
- H12: sesgo firmado relativo (atenuacion) de las IRF del BVAR por celda.

## Replicas

| Herramienta | Escenario | T | Replicas |
|---|---|---|---|
| BVAR | casi_RW / GLP | 60 | 500 |
| BVAR | casi_RW / GLP | 120 | 500 |
| BVAR | casi_RW / GLP_delta1 | 60 | 500 |
| BVAR | casi_RW / GLP_delta1 | 120 | 500 |
| BVAR | casi_RW / plano_lam100 | 60 | 500 |
| BVAR | casi_RW / plano_lam100 | 120 | 500 |
| BVAR | denso / GLP | 60 | 500 |
| BVAR | denso / GLP | 120 | 500 |
| BVAR | denso / GLP_delta1 | 60 | 500 |
| BVAR | denso / GLP_delta1 | 120 | 500 |
| BVAR | denso / plano_lam100 | 60 | 500 |
| BVAR | denso / plano_lam100 | 120 | 500 |
| BVAR | logml_vs_cadena_predictiva_n3_dummies |  | 1 |
| BVAR | logml_vs_cuadratura_n1 |  | 1 |
| BVAR | tasas / GLP | 60 | 500 |
| BVAR | tasas / GLP | 120 | 500 |
| BVAR | tasas / GLP_delta1 | 60 | 500 |
| BVAR | tasas / GLP_delta1 | 120 | 500 |
| BVAR | tasas / GLP_delta_mixto | 60 | 500 |
| BVAR | tasas / GLP_delta_mixto | 120 | 500 |
| BVAR | tasas / plano_lam100 | 60 | 500 |
| BVAR | tasas / plano_lam100 | 120 | 500 |
| TVP | ruptura_kQ0.01 | 120 | 8 |
| TVP | ruptura_kQ0.10 | 120 | 30 |
| TVP | ruptura_kQ0.30 | 120 | 12 |
| TVP | sin_ruptura_kQ0.10 | 120 | 12 |
| TVP | sin_ruptura_kQ0.30 | 120 | 10 |
| prereg | V3_solo_impacto | 88 | 30 |
| prereg | principal | 88 | 30 |
| prereg_M | M10000 | 88 | 5 |
| prereg_M | M1500 | 88 | 5 |
| prereg_M | M3000 | 88 | 5 |
| prereg_M | M500 | 88 | 5 |
| regimenes | ruptura | 120 | 300 |
| regimenes | sin_ruptura | 120 | 300 |
| regimenes5 | cambios / GLP | 88 | 300 |
| regimenes5 | cambios / lam1 | 88 | 300 |
| regimenes5 | cambios / plano_lam5 | 88 | 300 |
| regimenes5 | sin_cambio / GLP | 88 | 300 |
| regimenes5 | sin_cambio / lam1 | 88 | 300 |
| regimenes5 | sin_cambio / plano_lam5 | 88 | 300 |
| signos | ARW_invariancia_al_orden |  | 100000 |
| signos | signos+ceros / T120 | 120 | 80 |
| signos | signos / T120 | 120 | 100 |
| signos | signos / T60 | 60 | 80 |

## 1. BVAR normal-Wishart inversa (GLP)

DGP: VAR(2) de 4 variables. «denso»: radio espectral 0.65; «casi_RW»: 0,9 por variable; «tasas»: tres tasas poco persistentes (0,25-0,35) y una variable en nivel muy persistente (0,95), como el tipo. IRF de Cholesky; 300 sorteos de la posterior por replica; cobertura medida sobre las celdas no triviales (se excluyen los ceros estructurales del impacto). Modos: `GLP` = delta 0 (por defecto); `GLP_delta1` = delta 1 en todas (sensibilidad); `GLP_delta_mixto` = delta (0, 0, 0, 1) (solo «tasas»; configuracion de desviaciones.md); `plano_lam100` = referencia sin contraccion. Atenuacion firmada = -sum(signo(verdad)·(media de la mediana - verdad)) / sum|verdad| sobre h = 1-12 (positiva = IRF media mas cerca de 0 que la verdad).

| Escenario / modo | T | cob. 68 % | cob. 90 % | sesgo abs. rel. h=1-12 | atenuacion firmada h=1-12 | frac. celdas atenuadas | lambda mediana |
|---|---|---|---|---|---|---|---|
| denso / GLP | 120 | 0.670 | 0.902 | 0.211 | +0.197 | 0.92 | 0.21 |
| denso / GLP_delta1 | 120 | 0.775 | 0.956 | 0.137 | +0.107 | 0.81 | 0.30 |
| denso / plano_lam100 | 120 | 0.749 | 0.939 | 0.146 | +0.137 | 1.00 | 100 (fijo) |
| denso / GLP | 60 | 0.636 | 0.873 | 0.351 | +0.341 | 0.94 | 0.22 |
| denso / GLP_delta1 | 60 | 0.849 | 0.966 | 0.233 | +0.181 | 0.89 | 0.33 |
| denso / plano_lam100 | 60 | 0.814 | 0.944 | 0.256 | +0.229 | 1.00 | 100 (fijo) |
| casi_RW / GLP | 120 | 0.553 | 0.794 | 0.319 | +0.309 | 1.00 | 0.38 |
| casi_RW / GLP_delta1 | 120 | 0.734 | 0.930 | 0.144 | +0.087 | 0.99 | 0.07 |
| casi_RW / plano_lam100 | 120 | 0.564 | 0.806 | 0.305 | +0.293 | 1.00 | 100 (fijo) |
| casi_RW / GLP | 60 | 0.495 | 0.744 | 0.519 | +0.502 | 1.00 | 0.39 |
| casi_RW / GLP_delta1 | 60 | 0.723 | 0.908 | 0.210 | +0.149 | 0.97 | 0.09 |
| casi_RW / plano_lam100 | 60 | 0.517 | 0.765 | 0.498 | +0.489 | 1.00 | 100 (fijo) |
| tasas / GLP | 120 | 0.655 | 0.879 | 0.288 | +0.284 | 0.98 | 0.25 |
| tasas / GLP_delta1 | 120 | 0.713 | 0.917 | 0.263 | +0.240 | 0.91 | 0.30 |
| tasas / GLP_delta_mixto | 120 | 0.649 | 0.883 | 0.254 | +0.251 | 1.00 | 0.11 |
| tasas / plano_lam100 | 120 | 0.678 | 0.892 | 0.261 | +0.255 | 0.98 | 100 (fijo) |
| tasas / GLP | 60 | 0.646 | 0.856 | 0.459 | +0.454 | 1.00 | 0.27 |
| tasas / GLP_delta1 | 60 | 0.753 | 0.923 | 0.421 | +0.384 | 0.91 | 0.33 |
| tasas / GLP_delta_mixto | 60 | 0.633 | 0.862 | 0.360 | +0.358 | 1.00 | 0.11 |
| tasas / plano_lam100 | 60 | 0.707 | 0.891 | 0.423 | +0.413 | 1.00 | 100 (fijo) |

Atenuacion firmada por horizonte (modo GLP):

| Escenario | T | h=1 | h=4 | h=8 | h=12 |
|---|---|---|---|---|---|
| denso | 120 | +0.148 | +0.267 | +0.217 | -0.034 |
| denso | 60 | +0.270 | +0.435 | +0.382 | +0.097 |
| casi_RW | 120 | +0.132 | +0.287 | +0.415 | +0.489 |
| casi_RW | 60 | +0.270 | +0.489 | +0.629 | +0.698 |
| tasas | 120 | +0.149 | +0.242 | +0.369 | +0.448 |
| tasas | 60 | +0.282 | +0.407 | +0.563 | +0.638 |

Verosimilitud marginal frente a fuerza bruta: error absoluto en log = 5.7e-10 (cuadratura 2-D, n=1, p=1) y 5.7e-14 (cadena predictiva t multivariante, n=3, p=2, con dummies de suma de coeficientes y de observacion inicial).

Lectura (cifras del csv, modo GLP con delta = 0, seis celdas): cobertura del 90 % entre 0.744 a 0.902 y del 68 % entre 0.495 a 0.670; sesgo absoluto relativo entre 0.211 a 0.519; atenuacion firmada entre +0.197 a +0.502 (celdas atenuadas: 0.92 a 1.00). El sesgo absoluto de GLP es menor que el del prior casi plano en 0 de 6 celdas y menor que el de GLP con delta = 1 en 0 de 6. La atenuacion firmada separa el sesgo sistematico (hacia cero) del error de Monte Carlo por celda, que si se promedia en valor absoluto lo infla.

## 2. Signos y ceros (RWZ / ARW): DGP de 4 variables, solo impacto

DGP estructural de 4 shocks (oferta, demanda, credito, monetario) sobre 4 variables (y, pi, cred, tipo). Restricciones de signo en el impacto: oferta (y+, pi-); demanda (y+, pi+, tipo+); credito (cred+, y+, pi+); monetario (tipo+, pi-, cred-, y-). Variante con ceros: el shock monetario no mueve y en el impacto y el de oferta no mueve el tipo (sustituyen a la restriccion y- del monetario). 400 sorteos de la posterior, 800 rotaciones por theta (todas las aceptadas se conservan; se para al llegar a 150 aceptadas). Cobertura medida en h = 0, 1, 4, 8. «Restringidas» = celdas con restriccion de signo; «no restringidas» = el resto (con verdad no nula).

| Escenario | T | replicas | aceptacion/rotacion | frac. theta con aceptada | ESS | cob. 68 % restr. | cob. 68 % no restr. | cob. 90 % restr. | cob. 90 % no restr. | signo impacto (no restr.) | banda 90 % excluye 0 con signo correcto | HD error max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| signos | 120 | 100 | 0.0014 | 0.66 | 151 | 0.822 | 0.881 | 0.973 | 0.971 | 0.927 | 0.000 | 2.7e-15 |
| signos | 60 | 80 | 0.0012 | 0.60 | 150 | 0.789 | 0.857 | 0.951 | 0.955 | 0.904 | 0.000 | 6.2e-15 |
| signos+ceros | 120 | 80 | 0.0047 | 0.96 | 139 | 0.828 | 0.852 | 0.968 | 0.962 | 0.992 | 0.000 | 2.7e-15 |

Ceros: maximo |IRF| en las restricciones de cero = 1.6e-14. Descomposicion historica: error maximo < 1e-8 en las replicas comprobadas (6 por escenario, 20 sorteos cada una). Las filas de la FEVD (h = 4, 8, 12, 20) suman 1.

Pesos de importancia PROPIOS (no se afirma que coincidan con los de ARW; revision F3 H3): derivacion por coarea en el espacio (forma reducida, Q), objetivo p(theta)·Haar(Q) condicionado a los ceros. Diagnostico: la distribucion ponderada de Q debe ser invariante al orden de los shocks. Con 100000 rotaciones en un theta, la diferencia maxima en E[Q^2] entre ordenes es 0.004 con pesos frente a 0.104 sin pesos; suelo de ruido 0.005; ESS medio 73983.

Lectura: la cobertura del 90 % de las celdas no restringidas esta en 0.955 a 0.971 y el signo del impacto de los elementos no restringidos se recupera (por la mediana) en 0.904 a 0.992 de las replicas; la banda del 90 % de esos elementos excluye el cero con el signo correcto en 0.000 de las celdas. Con un conjunto identificado la banda mezcla incertidumbre de parametros e identificacion; la «cobertura» no tiene el significado frecuentista habitual.

## 2b. Configuracion PRE-REGISTRADA (hipotesis.md §5): 7 variables, T = 88, p = 2, h = 0-1, 4 ceros

DGP fijo (VAR(2) de 7 variables p, r, q, c, i, e, n) cuya matriz de impacto cumple exactamente la tabla (signos en h = 0 y h = 1; cero en el impacto de la poblacion ante los shocks de actividad, demanda, oferta y credito; dos shocks sin identificar). Incluye las ficticias exogenas de COVID (3 trimestres) y de EPA 2021T1 (efectos verdaderos sobre e: -2,0 y +1,5), estimadas con varianza a priori laxa. BVAR-GLP con delta = 1 en el tipo y 0 en el resto (desviaciones.md). Principal = signos en h = 0-1 con q en demanda y oferta; V3 = solo h = 0 y sin la restriccion de q (hipotesis.md V3). Por theta se prueban M rotaciones y se conservan todas las aceptadas. La DH se evalua por tramos (suma de contribuciones en los trimestres del tramo) contra la contribucion verdadera, solo para los 5 shocks identificados (los 2 libres son intercambiables). «Cobertura DH» = fraccion de celdas (tramo x variable x shock) cuya contribucion verdadera cae en la banda ponderada.

| Metrica | Principal (h = 0-1, con q) | V3 (solo impacto, sin q) |
|---|---|---|
| replicas (de las simuladas) con >= 20 aceptadas | 30 | 30 |
| aceptacion por rotacion | 9.94e-05 | 2.89e-03 |
| fraccion de theta con alguna rotacion aceptada (media) | 0.222 | 1.000 |
| fraccion de theta con aceptada (minimo entre replicas) | 0.038 | 1.000 |
| rotaciones probadas por aceptada | 20325 | 357 |
| aceptadas por replica | 160 | 304 |
| ESS medio de los pesos | 147.3 | 276.1 |
| ESS minimo | 22.1 | 254.9 |
| max |IRF| en los ceros | 3.7e-15 | 4.5e-15 |
| error maximo de la DH con exogenas | 1.6e-12 | 2.2e-12 |
| signo del impacto recuperado (no restr.) | 0.780 | 0.650 |
| banda 90 % del impacto excluye 0 con signo correcto | 0.010 | 0.000 |
| cobertura 90 % IRF restringidas | 0.926 | 0.924 |
| cobertura 90 % IRF no restringidas | 0.927 | 0.922 |
| cobertura DH 68 % (total) | 0.725 | 0.677 |
| cobertura DH 90 % (total) | 0.917 | 0.900 |
| DH: signo del tramo correcto (|contrib| >= 0,5) | 0.673 | 0.637 |
| DH: banda 90 % excluye 0 con signo correcto | 0.001 | 0.000 |
| DH: banda 90 % excluye 0 con signo ERRONEO | 0.000 | 0.000 |
| coef. COVID sobre e estimado (verdad -2,0) | -2.42 | -2.70 |
| coef. EPA sobre e estimado (verdad +1,5) | +0.85 | +0.90 |

Cobertura de la descomposicion historica por tramos (solo shocks identificados):

| Tramo (trimestres) | Principal: cob. 68 % / 90 % | V3: cob. 68 % / 90 % |
|---|---|---|
| P0 (14) | 0.690 / 0.905 | 0.707 / 0.904 |
| P2 (22) | 0.751 / 0.920 | 0.661 / 0.901 |
| P3 (24) | 0.735 / 0.931 | 0.698 / 0.910 |
| P4 (9) | 0.717 / 0.910 | 0.656 / 0.887 |
| P5 (14) | 0.731 / 0.920 | 0.663 / 0.900 |

Coste (tiempo de pared de la identificacion por replica, un hilo; depende de la maquina): principal 17.1 s, V3 1.3 s.

Rotaciones por theta (M) frente a coste y rendimiento, configuracion principal (pocas replicas, sorteos de theta fijos):

| M | frac. theta con aceptada | aceptadas por replica | ESS medio | aceptacion por rotacion | s por replica |
|---|---|---|---|---|---|
| 500 | 0.055 | 12 | 10.8 | 1.16e-04 | 1.2 |
| 1500 | 0.166 | 38 | 34.6 | 1.25e-04 | 3.4 |
| 3000 | 0.277 | 72 | 66.0 | 1.19e-04 | 6.5 |
| 10000 | 0.547 | 224 | 204.8 | 1.12e-04 | 21.8 |

Viabilidad de la principal: con M = 3000 la fraccion de theta con alguna rotacion aceptada es 0.222 (>= 1 %, regla de viabilidad) y el ESS medio 147.3. Se reportan ambas configuraciones (principal y V3) con cifras; la eleccion entre ellas y la fijacion de M y del numero de sorteos de theta corresponden al orquestador.

## 3. TVP-VAR con volatilidad estocastica

DGP: VAR(2) de 3 variables, un coeficiente (primer retardo propio de la ecuacion 1) pasa de 0,4 a 0,8 a mitad de la muestra efectiva; volatilidad 0,5 constante. T = 120 con 30 observaciones de entrenamiento del prior (T efectivo = 88). Gibbs de 1200 iteraciones, 400 de calentamiento, adelgazado 4 (200 sorteos). kQ es la escala del prior de Q (Primiceri usa 0,01). Control = coeficiente constante de otra ecuacion. «Deteccion» = la banda del 90 % de (media del ultimo cuarto - media del primer cuarto) excluye 0 por arriba.

| Escenario | replicas | cob. 68 % coef. | cob. 90 % coef. | cob. 90 % control | deteccion / falsos positivos | cambio estimado (verdad 0,4) | RMSE senda | sigma est./verdad |
|---|---|---|---|---|---|---|---|---|
| ruptura_kQ0.10 | 30 | 0.545 | 0.766 | 0.995 | 0.17 | 0.19 | 0.179 | 0.96 |
| sin_ruptura_kQ0.10 | 12 | 0.802 | 0.902 | 0.950 | 0.00 | - | 0.099 | 0.98 |
| ruptura_kQ0.30 | 12 | 0.790 | 0.950 | 0.996 | 0.17 | 0.27 | 0.176 | 0.89 |
| sin_ruptura_kQ0.30 | 10 | 0.735 | 0.940 | 0.969 | 0.00 | - | 0.186 | 0.87 |
| ruptura_kQ0.01 | 8 | 0.125 | 0.453 | 1.000 | 0.00 | 0.01 | 0.218 | 1.04 |

Lectura (cifras del csv): deteccion con kQ = 0,01 / 0,10 / 0,30: 0.00 / 0.17 / 0.17; cobertura del 90 % del coeficiente con ruptura: 0.45 / 0.77 / 0.95; falsos positivos sin ruptura (kQ 0,10 / 0,30): 0.00 / 0.00. No se recomienda para fechar o atribuir cambios de coeficientes con muestras de este tamano; como descripcion exploratoria de la volatilidad, la sigma estimada sobre la verdadera esta en la tabla.

### Alternativa: VAR por regimenes (prior comun, ruptura conocida), 2 regimenes

Misma DGP; coeficientes distintos por tramo con el mismo prior Minnesota (delta = 0; lambda comun por verosimilitud marginal). La fecha de ruptura se SUPONE conocida.

| Escenario | replicas | cob. 68 % | cob. 90 % | deteccion / falsos positivos | cambio estimado |
|---|---|---|---|---|---|
| ruptura | 300 | 0.273 | 0.502 | 0.66 | 0.30 |
| sin_ruptura | 300 | 0.275 | 0.560 | 0.03 | - |

### Alternativa: VAR por regimenes con los 5 tramos reales (H9)

DGP: VAR(2) de n = 4 variables, 5 tramos de 16, 22, 24, 9, 15 trimestres con huecos de transicion de 2 (tras el 1.o) y 1 (tras el 3.o) trimestres, que no entran como variable dependiente (`tramos` no contiguos). Parametro: primer retardo propio de la ecuacion 1: 0.2, 0.6, 0.3, 0.7, 0.4 en los tramos («cambios») o 0,4 constante («sin_cambio»). Ancho prior = ancho de la banda 90 % del coeficiente bajo el prior. Modos: `GLP` (lambda por verosimilitud marginal), `lam1` (lambda = 1), `plano_lam5` (lambda = 5, casi plano).

**cambios / GLP** (lambda mediana 0.26; replicas 300):

| Tramo | cob. 68 % | cob. 90 % | sesgo | RMSE | ancho 90 % posterior | ancho posterior / prior |
|---|---|---|---|---|---|---|
| T1 (16) | 0.48 | 0.83 | -0.149 | 0.192 | 0.545 | 0.75 |
| T2 (22) | 0.09 | 0.25 | -0.346 | 0.374 | 0.503 | 0.70 |
| T3 (24) | 0.39 | 0.66 | -0.169 | 0.218 | 0.488 | 0.67 |
| T4 (9) | 0.01 | 0.08 | -0.578 | 0.593 | 0.587 | 0.81 |
| T5 (15) | 0.18 | 0.46 | -0.282 | 0.308 | 0.544 | 0.75 |

deteccion T1->T2 (cambio +0.4) = 0.18; deteccion T2->T3 (cambio -0.3) = 0.09; deteccion T3->T4 (cambio +0.4) = 0.02; deteccion T4->T5 (cambio -0.3) = 0.00

**cambios / lam1** (lambda mediana 1.00; replicas 300):

| Tramo | cob. 68 % | cob. 90 % | sesgo | RMSE | ancho 90 % posterior | ancho posterior / prior |
|---|---|---|---|---|---|---|
| T1 (16) | 0.55 | 0.80 | -0.134 | 0.299 | 0.777 | 0.29 |
| T2 (22) | 0.48 | 0.72 | -0.195 | 0.300 | 0.656 | 0.24 |
| T3 (24) | 0.50 | 0.75 | -0.095 | 0.260 | 0.627 | 0.23 |
| T4 (9) | 0.27 | 0.46 | -0.487 | 0.581 | 0.962 | 0.36 |
| T5 (15) | 0.46 | 0.71 | -0.211 | 0.346 | 0.774 | 0.29 |

deteccion T1->T2 (cambio +0.4) = 0.35; deteccion T2->T3 (cambio -0.3) = 0.21; deteccion T3->T4 (cambio +0.4) = 0.09; deteccion T4->T5 (cambio -0.3) = 0.09

**cambios / plano_lam5** (lambda mediana 5.00; replicas 300):

| Tramo | cob. 68 % | cob. 90 % | sesgo | RMSE | ancho 90 % posterior | ancho posterior / prior |
|---|---|---|---|---|---|---|
| T1 (16) | 0.49 | 0.73 | -0.143 | 0.386 | 0.826 | 0.06 |
| T2 (22) | 0.44 | 0.70 | -0.164 | 0.317 | 0.685 | 0.05 |
| T3 (24) | 0.48 | 0.69 | -0.081 | 0.287 | 0.646 | 0.05 |
| T4 (9) | 0.37 | 0.54 | -0.543 | 0.852 | 1.462 | 0.11 |
| T5 (15) | 0.38 | 0.63 | -0.214 | 0.442 | 0.835 | 0.06 |

deteccion T1->T2 (cambio +0.4) = 0.39; deteccion T2->T3 (cambio -0.3) = 0.24; deteccion T3->T4 (cambio +0.4) = 0.12; deteccion T4->T5 (cambio -0.3) = 0.12

**sin_cambio / GLP** (lambda mediana 0.27; replicas 300):

| Tramo | cob. 68 % | cob. 90 % | sesgo | RMSE | ancho 90 % posterior | ancho posterior / prior |
|---|---|---|---|---|---|---|
| T1 (16) | 0.22 | 0.50 | -0.267 | 0.297 | 0.540 | 0.75 |
| T2 (22) | 0.26 | 0.54 | -0.232 | 0.267 | 0.502 | 0.70 |
| T3 (24) | 0.25 | 0.55 | -0.230 | 0.257 | 0.499 | 0.69 |
| T4 (9) | 0.07 | 0.30 | -0.349 | 0.364 | 0.580 | 0.80 |
| T5 (15) | 0.15 | 0.39 | -0.294 | 0.326 | 0.546 | 0.76 |

falsos positivos T1->T2 (bilateral) = 0.04; falsos positivos T2->T3 (bilateral) = 0.03; falsos positivos T3->T4 (bilateral) = 0.04; falsos positivos T4->T5 (bilateral) = 0.04

**sin_cambio / lam1** (lambda mediana 1.00; replicas 300):

| Tramo | cob. 68 % | cob. 90 % | sesgo | RMSE | ancho 90 % posterior | ancho posterior / prior |
|---|---|---|---|---|---|---|
| T1 (16) | 0.48 | 0.72 | -0.191 | 0.330 | 0.749 | 0.28 |
| T2 (22) | 0.54 | 0.78 | -0.134 | 0.274 | 0.652 | 0.24 |
| T3 (24) | 0.51 | 0.81 | -0.144 | 0.240 | 0.637 | 0.23 |
| T4 (9) | 0.43 | 0.69 | -0.320 | 0.437 | 0.984 | 0.36 |
| T5 (15) | 0.43 | 0.67 | -0.233 | 0.382 | 0.782 | 0.29 |

falsos positivos T1->T2 (bilateral) = 0.15; falsos positivos T2->T3 (bilateral) = 0.12; falsos positivos T3->T4 (bilateral) = 0.17; falsos positivos T4->T5 (bilateral) = 0.15

**sin_cambio / plano_lam5** (lambda mediana 5.00; replicas 300):

| Tramo | cob. 68 % | cob. 90 % | sesgo | RMSE | ancho 90 % posterior | ancho posterior / prior |
|---|---|---|---|---|---|---|
| T1 (16) | 0.44 | 0.68 | -0.192 | 0.402 | 0.797 | 0.06 |
| T2 (22) | 0.54 | 0.74 | -0.117 | 0.301 | 0.679 | 0.05 |
| T3 (24) | 0.50 | 0.79 | -0.131 | 0.255 | 0.656 | 0.05 |
| T4 (9) | 0.38 | 0.63 | -0.329 | 0.753 | 1.499 | 0.11 |
| T5 (15) | 0.38 | 0.61 | -0.236 | 0.487 | 0.840 | 0.06 |

falsos positivos T1->T2 (bilateral) = 0.25; falsos positivos T2->T3 (bilateral) = 0.17; falsos positivos T3->T4 (bilateral) = 0.31; falsos positivos T4->T5 (bilateral) = 0.31

Lectura: en el tramo de 9 trimestres la cobertura del 90 % es 0.08 y el ancho de la posterior es 0.81 veces el del prior (modo GLP, «cambios»); regla de imprecision: ancho posterior/prior >= 0,75 -> tramo impreciso (posterior cercana al prior). Los demas tramos figuran en la tabla; la etiqueta global se deriva de las cobertura, la deteccion entre tramos contiguos y los falsos positivos.


## Limitaciones

- Un solo conjunto de DGP por herramienta; los resultados no se extrapolan a otras dinamicas.
- BVAR: psi de la muestra completa (no pre-muestra); no se imponen hiperpriors (maximo de la densidad marginal pura).
- Signos: cobertura de un conjunto identificado no es una propiedad frecuentista; pesos propios (ver arriba). El DGP pre-registrado es uno solo y cumple la tabla por construccion; la aceptacion real depende de la posterior de los datos reales.
- La DH por tramos usa tramos del calendario simulado (14, 22, 24, 9, 14 trimestres); P1 (1995-2007) no existe con 7 variables.
- TVP: sin truncamiento de estabilidad; prior de entrenamiento con 30 observaciones; ruptura unica; ESS de Gibbs no reportado.
- Replicas pocas en TVP (8-30) y en la configuracion pre-registrada (30) y la cuadricula de M (5): los porcentajes tienen error de muestreo de varios puntos.


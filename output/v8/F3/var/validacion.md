# V8-F3 grupo A (familia VAR): validacion por Monte Carlo

Capa C4 (metodologico). Solo datos simulados; ningun dato real ni sellado. SEED = 20261010, un hilo, determinista. Computo total de la ejecucion: 748 s (12.5 min). Reproducir: `python3 src/v8/f3_montecarlo_var.py`. Resultados completos: `montecarlo.csv`. Referencias de metodo NO VERIFICADAS (sin acceso a Crossref).

## Veredicto por herramienta

| Herramienta / componente | Etiqueta |
|---|---|
| BVAR-GLP | **con reservas** |
| signos/ceros (mecanica: restricciones, FEVD, descomposicion historica) | **apta** |
| pesos de importancia ARW (derivados aqui; formula del articulo NO contrastada) | **apta (invariancia al orden)** |
| signos/ceros (inferencia: bandas y signo del impacto) | **con reservas (bandas conservadoras: cobertura 90 % por encima de 0,98; set-identified)** |
| TVP-VAR-SV (convergencia y volatilidad) | **con reservas** |
| TVP-VAR-SV (deteccion de un cambio de coeficiente con T efectivo = 88) | **no apta (potencia y cobertura insuficientes con T efectivo = 88; ver kQ=0,10 y 0,30)** |
| VAR por regimenes (ruptura CONOCIDA) | **con reservas** |

Reglas declaradas. Criterios: sesgo relativo <= 10 % (IRF) o, en conjuntos identificados por signos, recuperacion del signo del impacto en >= 90 % de replicas; cobertura de las bandas del 90 % en [0,85; 0,98]. «Apta»: cumple todos. «Con reservas»: la mecanica es exacta y la cobertura 90 % esta en [0,80; 0,99] (BVAR; sesgo <= 30 %) o es conservadora (signos, >= 0,85). «No apta»: el resto. Deteccion de cambios (TVP y regimenes): potencia >= 80 % y falsos positivos <= 15 % (criterio anadido por el ejecutor).

## Replicas (las que caben en ~20 min)

| Herramienta | Escenario | T | Replicas |
|---|---|---|---|
| BVAR | casi_RW / GLP | 120 | 300 |
| BVAR | casi_RW / GLP | 60 | 300 |
| BVAR | casi_RW / plano_lam100 | 120 | 300 |
| BVAR | casi_RW / plano_lam100 | 60 | 300 |
| BVAR | denso / GLP | 120 | 300 |
| BVAR | denso / GLP | 60 | 300 |
| BVAR | denso / plano_lam100 | 120 | 300 |
| BVAR | denso / plano_lam100 | 60 | 300 |
| BVAR | logml_vs_cadena_predictiva_n3_dummies |  | 1 |
| BVAR | logml_vs_cuadratura_n1 |  | 1 |
| TVP | ruptura_kQ0.01 | 120 | 8 |
| TVP | ruptura_kQ0.10 | 120 | 30 |
| TVP | ruptura_kQ0.30 | 120 | 12 |
| TVP | sin_ruptura_kQ0.10 | 120 | 12 |
| TVP | sin_ruptura_kQ0.30 | 120 | 10 |
| regimenes | ruptura | 120 | 300 |
| regimenes | sin_ruptura | 120 | 300 |
| signos | ARW_invariancia_al_orden |  | 100000 |
| signos | signos+ceros / T120 | 120 | 80 |
| signos | signos / T120 | 120 | 100 |
| signos | signos / T60 | 60 | 80 |

## 1. BVAR normal-Wishart inversa (GLP)

DGP: VAR(2) de 4 variables («denso»: radio espectral 0.65; «casi_RW»: 0,9 por variable). IRF de Cholesky; 300 sorteos de la posterior por replica; cobertura medida sobre las celdas no triviales (se excluyen los ceros estructurales del impacto). `plano_lam100` es la referencia sin contraccion (prior casi plano).

| Escenario | T | cob. 68 % | cob. 90 % | sesgo rel. IRF h=1-12 | lambda mediana |
|---|---|---|---|---|---|
| denso / GLP | 120 | 0.781 | 0.958 | 0.138 | 0.30 |
| denso / plano_lam100 | 120 | 0.755 | 0.940 | 0.149 | 100 (fijo) |
| denso / GLP | 60 | 0.848 | 0.966 | 0.246 | 0.33 |
| denso / plano_lam100 | 60 | 0.815 | 0.942 | 0.270 | 100 (fijo) |
| casi_RW / GLP | 120 | 0.744 | 0.934 | 0.143 | 0.07 |
| casi_RW / plano_lam100 | 120 | 0.571 | 0.810 | 0.308 | 100 (fijo) |
| casi_RW / GLP | 60 | 0.721 | 0.907 | 0.224 | 0.09 |
| casi_RW / plano_lam100 | 60 | 0.513 | 0.758 | 0.509 | 100 (fijo) |

Verosimilitud marginal frente a fuerza bruta: error absoluto en log = 2.0e-09 (cuadratura 2-D, n=1, p=1) y 5.7e-14 (cadena predictiva t multivariante, n=3, p=2, con dummies de suma de coeficientes y de observacion inicial).

GLP elige lambda coherente con el DGP: menor en el paseo aleatorio (casi_RW) que en el VAR denso, y siempre dentro de [0,005; 20] sin tocar los limites.

Lectura: la cobertura del 90 % con GLP esta dentro de [0,85; 0,98] en las cuatro celdas (las bandas del 68 % son anchas: 0,72-0,85 frente a 0,68 nominal). El sesgo relativo agregado de la mediana de la IRF supera el 10 % (0,14 a 0,25). Ese sesgo aparece tambien con el prior casi plano (sesgo de muestra finita del VAR persistente), asi que no es atribuible a la contraccion; en el DGP casi_RW la contraccion GLP lo reduce a la mitad (0,14 frente a 0,31 con T=120) y corrige la cobertura (0,93 frente a 0,81). Por eso la etiqueta es «con reservas» y no «apta» segun el criterio de sesgo declarado (T=60: sesgo 0,22-0,25).

## 2. Signos y ceros (RWZ / ARW)

DGP estructural de 4 shocks (oferta, demanda, credito, monetario) sobre 4 variables (y, pi, cred, tipo). Restricciones de signo en el impacto: oferta (y+, pi-); demanda (y+, pi+, tipo+); credito (cred+, y+, pi+); monetario (tipo+, pi-, cred-, y-). Variante con ceros: el shock monetario no mueve y en el impacto y el de oferta no mueve el tipo (sustituyen a la restriccion y- del monetario). 400 sorteos de la posterior, 150 rotaciones aceptadas por replica. Cobertura medida en h = 0, 1, 4, 8. «Restringidas» = celdas con restriccion de signo; «no restringidas» = el resto (con verdad no nula).

| Escenario | T | replicas | aceptacion/rotacion | ESS (de 150) | cob. 68 % restr. | cob. 68 % no restr. | cob. 90 % restr. | cob. 90 % no restr. | signo impacto recuperado (no restr.) | HD error max |
|---|---|---|---|---|---|---|---|---|---|---|
| signos | 120 | 100 | 0.0013 | 150 | 0.820 | 0.943 | 0.971 | 0.993 | 0.933 | 3.3e-15 |
| signos | 60 | 80 | 0.0012 | 150 | 0.797 | 0.948 | 0.946 | 0.991 | 0.912 | 5.7e-14 |
| signos+ceros | 120 | 80 | 0.0046 | 136 | 0.823 | 0.924 | 0.972 | 0.990 | 0.996 | 2.7e-15 |

Ceros: maximo |IRF| en las restricciones de cero = 1.6e-14 (se cumplen exactamente). Descomposicion historica: y_t = componente determinista + suma de contribuciones con error maximo < 1e-8 en todas las replicas comprobadas (6 por escenario, 20 sorteos cada una). Las filas de la FEVD (h = 4, 8, 12, 20) suman 1 en todas las replicas.

Pesos ARW: la formula exacta del articulo NO se pudo contrastar (sin acceso). Los pesos usados son una derivacion propia por coarea en el espacio (forma reducida, Q) (ver cabecera de signos.py). Diagnostico: la distribucion ponderada de Q debe ser invariante al orden de los shocks. Con 100000 sorteos, la diferencia maxima en E[Q^2] entre ordenes es 0.016 con pesos frente a 0.105 sin pesos; el suelo de ruido (mismo orden, otra semilla) es 0.018 (ESS medio 2384 de 100000). La prueba rechaza pesos incorrectos pero no demuestra la igualdad con la formula de ARW.

Lectura: las bandas por signos son anchas (la verdad cae en ellas mas a menudo que lo nominal: con un conjunto identificado la banda mezcla incertidumbre de parametros y de identificacion, y la ‘cobertura’ no tiene el significado frecuentista habitual): la cobertura del 90 % de las celdas no restringidas es 0,99 (> 0,98) y la del 68 % es 0,92-0,95. El signo del impacto de los elementos no restringidos se recupera en el 91-93 % de las replicas con solo signos (T=120 y 60) y en el 99,6 % con dos ceros, pero la banda del 90 % de esos elementos no excluye nunca el cero (0 % de las celdas): el signo de un impacto no restringido se recupera por la mediana, no por la banda, y no debe afirmarse como resultado. Etiqueta «con reservas»: las bandas son cotas de credibilidad conservadoras, no calibradas al nivel nominal.

## 3. TVP-VAR con volatilidad estocastica

DGP: VAR(2) de 3 variables, un coeficiente (primer retardo propio de la ecuacion 1) pasa de 0,4 a 0,8 a mitad de la muestra efectiva; volatilidad 0,5 constante. T = 120 con 30 observaciones de entrenamiento del prior (T efectivo = 88). Gibbs de 1200 iteraciones, 400 de calentamiento, adelgazado 4 (200 sorteos). kQ es la escala del prior de Q (Primiceri usa 0,01). Control = coeficiente constante de otra ecuacion. «Deteccion» = la banda del 90 % de (media del ultimo cuarto - media del primer cuarto) excluye 0 por arriba.

| Escenario | replicas | cob. 68 % coef. | cob. 90 % coef. | cob. 90 % control | deteccion / falsos positivos | cambio estimado (verdad 0,4) | RMSE senda | sigma est./verdad |
|---|---|---|---|---|---|---|---|---|
| ruptura_kQ0.10 | 30 | 0.545 | 0.766 | 0.995 | 0.17 | 0.19 | 0.179 | 0.96 |
| sin_ruptura_kQ0.10 | 12 | 0.802 | 0.902 | 0.950 | 0.00 | nan | 0.099 | 0.98 |
| ruptura_kQ0.30 | 12 | 0.790 | 0.950 | 0.996 | 0.17 | 0.27 | 0.176 | 0.89 |
| sin_ruptura_kQ0.30 | 10 | 0.735 | 0.940 | 0.969 | 0.00 | nan | 0.186 | 0.87 |
| ruptura_kQ0.01 | 8 | 0.125 | 0.453 | 1.000 | 0.00 | 0.01 | 0.218 | 1.04 |

Lectura: el muestreador converge (la volatilidad se recupera y la senda sigue al coeficiente), pero un salto de 0,4 en un solo coeficiente con 88 observaciones efectivas se detecta con poca potencia: el paseo aleatorio suaviza el escalon y las bandas son anchas. kQ=0,01 (valor de Primiceri) ignora el cambio (cobertura 0,45). kQ=0,30 corrige la cobertura (0,95) pero no la potencia (deteccion 17 %; cambio estimado 0,27 frente a 0,4); kQ=0,10 queda en 0,77 de cobertura. Sin ruptura no hay falsos positivos. No se recomienda usarlo para fechar o atribuir cambios de coeficientes con muestras de este tamano; si sirve como descripcion exploratoria de la volatilidad.

### Alternativa documentada: VAR por regimenes (prior comun, ruptura conocida)

Misma DGP; coeficientes distintos por tramo con el mismo prior Minnesota (lambda comun por verosimilitud marginal). La fecha de ruptura se SUPONE conocida.

| Escenario | replicas | cob. 68 % | cob. 90 % | deteccion / falsos positivos | cambio estimado |
|---|---|---|---|---|---|
| ruptura | 300 | 0.658 | 0.900 | 0.64 | 0.31 |
| sin_ruptura | 300 | 0.702 | 0.925 | 0.04 | nan |

Lectura: con la ruptura conocida las bandas del 90 % cubren (0,90) y no hay falsos positivos relevantes (4 %), pero la potencia es 64 % y el cambio estimado (0,31 frente a 0,4) esta contraido por el prior; queda «con reservas». Sirve cuando el fechado de la ruptura viene de fuera; no la estima.


## Limitaciones

- Un solo conjunto de DGP por herramienta; los resultados no se extrapolan a otras dinamicas.
- BVAR: psi de la muestra completa (no pre-muestra); no se optimiza la prior de la matriz de escala ni se imponen hiperpriors (maximo de la densidad marginal pura).
- Signos: cobertura de un conjunto identificado no es una propiedad frecuentista; los pesos ARW son propios (ver arriba).
- TVP: sin truncamiento de estabilidad; prior de entrenamiento con 30 observaciones; ruptura unica; ESS de Gibbs no reportado.
- Replicas pocas en TVP (8-30): los porcentajes tienen error de muestreo de varios puntos.


<!-- Generado por `make publicacion` desde output/v5/nota_metodologica.md. No editar a mano: se regenera y un test lo comprueba. -->

# Estimadores de panel regional en vivienda con un factor común no estacionario: evidencia de simulación y aplicación a España

**Borja Romero, economista** (firma individual, independiente). Nota metodológica, versión v7.1. Fecha de los datos: 2026-10-12. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

*Capa de evidencia: C4 (metodológica y exploratoria). La nota no contiene resultados causales. Las cifras salen de output/v5/cifras_clave.csv y se pueden reconstruir con `make v7` (ver la sección 8).* <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

## Resumen

Los paneles regionales de precios de la vivienda suelen tener pocas unidades, unas decenas de trimestres y una tendencia común muy fuerte. Esta nota se pregunta si, en esas condiciones, los estimadores habituales de largo plazo en paneles dinámicos heterogéneos recuperan los parámetros y producen intervalos con la cobertura nominal. Se estudian el *mean group* (MG), el *pooled mean group* (PMG), los efectos fijos dinámicos (DFE), los estimadores con medias transversales CS-DL y CS-ARDL, un contraste de cointegración de tipo Westerlund y el contraste de raíz unitaria CIPS.

Un Monte Carlo con el tamaño del panel español (17 comunidades autónomas y 78 trimestres) muestra lo siguiente cuando hay un factor común no estacionario con cargas heterogéneas: <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- ningún estimador cumple a la vez un sesgo inferior al 10 % y una cobertura entre 0,90 y 0,98; <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- el MG sin ajuste llega a un sesgo relativo de 53,9 % y el PMG sin ajuste a 43,8 %;
- con medias transversales, el CS-DL baja a 10,9 %, pero su cobertura se queda en 0,88.

Aplicados al panel de las 17 comunidades (2007-2026), los tres estimadores de referencia no confirman ninguna de las siete hipótesis de largo plazo pre-registradas (0 confirmadas). La variación interanual de cada comunidad acompaña en gran medida a la media de las 17: el R² mediano es 93,6 % en compra y 86,1 % en alquiler. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

La conclusión es metodológica. Con este tamaño de panel, un coeficiente regional de largo plazo debe leerse como un rango entre estimadores. Su validez depende de cómo se trate el componente común.

## Abstract

Regional house-price panels typically combine few units, a few dozen quarters and a strong common trend. This note asks whether the usual long-run estimators for heterogeneous dynamic panels recover the parameters and deliver nominal coverage under those conditions. It covers mean group (MG), pooled mean group (PMG), dynamic fixed effects (DFE), the cross-sectionally augmented CS-DL and CS-ARDL, a Westerlund-type error-correction cointegration test and the CIPS unit-root test.

A Monte Carlo experiment sized like the Spanish panel (17 regions, 78 quarters) gives the following results when there is a non-stationary common factor with heterogeneous loadings: <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- no estimator meets both criteria (bias below 10 % and coverage between 0.90 and 0.98); <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- the unadjusted MG reaches a relative bias of 53,9 %;
- CS-DL lowers the bias to 10,9 %, but its coverage is 0,88.

In the application to the 17 Spanish regions (2007-2026), none of the seven pre-registered long-run hypotheses is confirmed by the three reference estimators. The median share of each region's year-on-year variance that moves with the cross-regional mean is 93,6 % for purchase prices and 86,1 % for rents. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

The implication is methodological. With panels of this size, regional long-run coefficients should be reported as ranges across estimators. Their validity depends on how the common component is handled. All results are exploratory (layer C4) and non-causal.

## 1. Introducción

La literatura sobre precios regionales de la vivienda estima con frecuencia relaciones de largo plazo con renta, empleo, población o crédito. Lo hace en paneles con pocas regiones y series de longitud media. Los estimadores de paneles dinámicos heterogéneos permiten que la dinámica de corto plazo difiera entre regiones y que el largo plazo sea común o específico de cada una:
- el MG de Pesaran y Smith (1995);
- el PMG de Pesaran, Shin y Smith (1999);
- los efectos fijos dinámicos.

La dependencia transversal se trata con medias transversales, siguiendo a Pesaran (2006), Kapetanios, Pesaran y Yamagata (2011), Chudik y Pesaran (2015) y Chudik, Mohaddes, Pesaran y Raissi (2016).

En los precios de la vivienda, el componente común no es un detalle técnico. Las condiciones de financiación, los ciclos del crédito y las expectativas son en gran parte nacionales. Holly, Pesaran y Yamagata (2010) y Bailey, Holly y Pesaran (2016) muestran, con datos de Estados Unidos, que la dependencia transversal fuerte y débil condiciona la especificación. Si el factor común es no estacionario y las cargas difieren entre regiones, un estimador que lo ignore puede atribuir a los regresores lo que es tendencia común. En España, con 17 comunidades autónomas, el número de unidades es pequeño para la teoría asintótica de los estimadores con medias transversales. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

Esta nota aporta dos cosas:
- **Una evaluación por simulación** de la aptitud de cada herramienta con el tamaño exacto del panel español, antes de aplicarla. Se fija un criterio declarado de antemano: sesgo relativo de como máximo el 10 % y cobertura del intervalo al 95 % entre 0,90 y 0,98. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- **La aplicación al panel español** con hipótesis pre-registradas y una regla de triangulación entre estimadores elegida a la vista de la simulación, no de los datos.

El resultado principal es negativo y se presenta como tal.

## 2. Marco: paneles dinámicos heterogéneos con un factor común

Para cada región $i=1,\dots,N$ y trimestre $t$, el modelo ARDL$(p,q)$ en forma de corrección de error es:

$$\Delta y_{it}=\phi_i\,(y_{i,t-1}-\theta_i' x_{i,t-1})+\sum_{j=1}^{p-1}\lambda_{ij}\Delta y_{i,t-j}+\sum_{j=0}^{q-1}\delta_{ij}'\Delta x_{i,t-j}+\mu_i+u_{it},$$

donde $\phi_i<0$ es la velocidad de ajuste y $\theta_i$ es el vector de coeficientes de largo plazo. Los estimadores se distinguen por las restricciones que imponen:
- **MG:** estima cada región por separado y promedia $\hat\theta_i$; su varianza procede de la dispersión entre regiones.
- **PMG:** impone $\theta_i=\theta$ y deja libres $\phi_i$ y la dinámica de corto plazo; se estima por máxima verosimilitud concentrada.
- **DFE:** impone homogeneidad en todos los coeficientes salvo $\mu_i$.
- **Hausman (1978):** el contraste entre MG y PMG valora la homogeneidad del largo plazo.

El componente común entra en el error: $u_{it}=\gamma_i f_t+\varepsilon_{it}$, con $f_t$ posiblemente I(1) y $\gamma_i$ heterogéneo y correlacionado con las cargas de los regresores. Hay dos formas de tratarlo:
- **Demeaning transversal:** restar la media de las $N$ regiones en cada periodo. Elimina $f_t$ solo si las cargas son homogéneas.
- **Medias transversales como regresores:** en CS-ARDL (Chudik y Pesaran, 2015) se añaden al ARDL; en CS-DL (Chudik, Mohaddes, Pesaran y Raissi, 2016) se estima directamente la relación de largo plazo con diferencias retardadas de los regresores, con $p_T$ retardos de las medias. Su justificación es asintótica en $N$ y $T$.

Para la cointegración se usan:
- una variante del contraste de corrección de error de Westerlund (2007), con remuestreo;
- los contrastes de Pedroni (1999, 2004).

Para la raíz unitaria con dependencia transversal se usa el CIPS de Pesaran (2007). La inferencia complementaria con pocas unidades emplea el *wild cluster bootstrap* (MacKinnon y Webb, 2017) y errores de Driscoll y Kraay (1998).

## 3. Diseño del Monte Carlo

**Tamaño.** $N=17$, $T=78$ y un periodo de calentamiento descartado. Coincide con el panel trimestral de las comunidades autónomas de 2007T1 a 2026T2.

**Proceso generador.**
- Dos regresores I(1) con deriva y coeficientes de largo plazo $\theta=(1;-0{,}5)$.
- Velocidad de ajuste $\phi_i\sim U(-0{,}4;-0{,}1)$.
- Efectos fijos en el nivel y corto plazo heterogéneo.
- Estimación con ARDL(2,1) en forma de corrección de error, el orden verdadero. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

**Escenarios.**

| Escenario | Descripción | Para qué sirve |
|---|---|---|
| A | cointegración, sin factor | caso de referencia |
| B | cointegración, factor común I(0) | factor estacionario |
| C | sin cointegración, sin factor | tamaño de los contrastes |
| D | sin cointegración, factor I(0) | tamaño con dependencia |
| E | $\theta_i$ heterogéneo | potencia del Hausman |
| F | factor común I(1) en el error, cargas heterogéneas y correlacionadas con las de los regresores | caso relevante para la vivienda |
| G | factor I(1) con cargas homogéneas | aísla la heterogeneidad de las cargas |
| J | ajuste lento, $\phi_i\sim U(-0{,}1;-0{,}02)$ | potencia de la cointegración |
| K | retroalimentación del desequilibrio hacia los regresores | exogeneidad débil violada |
| L | rotura en el nivel hacia $T/3$ | cambios estructurales |

**Réplicas.**
- quinientas en los escenarios A, C, D y F; doscientas en el resto. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- Bootstrap del PMG con ciento noventa y nueve remuestras. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- Contraste tipo Westerlund con 99 remuestras. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

**Criterio de aptitud** (declarado antes de ver los resultados):
- **apta:** sesgo relativo máximo de $\theta$ ≤ 10 % y cobertura del IC95 entre 0,90 y 0,98; <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- **con reservas:** sesgo correcto y cobertura fuera de ese intervalo;
- **no apta:** sesgo por encima del 10 %; <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- **tamaño de un contraste:** debe quedar entre 0,02 y 0,10. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

Semilla 20261010. Un solo hilo, para que el resultado sea idéntico entre ejecuciones. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

## 4. Resultados de la simulación

### 4.1 Sesgo y cobertura del largo plazo

Sin factor común (A) o con un factor estacionario (B), el MG con demeaning y el PMG con demeaning e intervalos por bootstrap son aptos. Los estimadores con medias transversales superan el umbral de sesgo y cubren por debajo del mínimo: su ventaja asintótica no se materializa con $N=17$.

El escenario F cambia el panorama:

| Estimador (escenario F) | Sesgo relativo máximo | Cobertura del IC95 (media; mín. y máx. entre θ₁ y θ₂) | <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
|---|---|---|
| MG sin ajuste | 53,9 % | 0,37 (0,34-0,40) |
| PMG sin ajuste | 43,8 % | 0,12 (0,11-0,14) |
| MG con demeaning | 20,3 % | 0,89 (0,85-0,93) |
| PMG con demeaning y bootstrap | 15,8 % | 0,92 (0,90-0,94) |
| CS-DL ($p_T$ = 4) | 10,9 % | 0,88 (0,86-0,90) | <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
| CS-ARDL ($p_T$ = 4) | 16,8 % | 0,86 (0,81-0,91) | <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

Ninguno es apto. Los estimadores sin tratamiento del componente común están muy sesgados y sus intervalos casi nunca contienen el valor verdadero. El demeaning reduce mucho el sesgo, pero no lo elimina, porque las cargas no son homogéneas. En el escenario G, con cargas homogéneas, el MG con demeaning sí es apto. Esto confirma que el problema es la heterogeneidad de las cargas, no la no estacionariedad en sí. El CS-DL es el menos sesgado, pero cubre por debajo del umbral. La corrección por *jackknife* de mitades reduce el sesgo en algunos casos a costa de hundir la cobertura.

**Otros escenarios.**
- **Ajuste lento (J), retroalimentación (K) y rotura (L):** el PMG es inestable y en algunos casos degenera numéricamente.
- **Rotura (L):** el MG con demeaning es apto.
- **Retroalimentación (K):** el MG con demeaning no es apto.
- **Selección de retardos:** el criterio bayesiano (SBC, con p y q ≤ 4) elige el orden verdadero en aproximadamente la mitad de las réplicas del escenario A. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

**Efectos fijos dinámicos.** El DFE se evaluó en la primera ronda de la simulación (escenarios A, B y E), no en F. Con un largo plazo homogéneo funciona bien:
- sesgo relativo máximo de 2,2 % sin factor y de 3,1 % con un factor estacionario;
- coberturas de 0,90 y 0,87.

Cuando $\theta_i$ es heterogéneo (E), su sesgo sube a 20,5 %. Es el precio de imponer homogeneidad donde no la hay. Como DFE comparte con PMG el supuesto de un largo plazo común y no trata el factor, no se usa en la regla de decisión. En la aplicación solo se reporta como contraste, con inferencia por *wild cluster bootstrap* y Driscoll-Kraay.

**CS-ARDL.** Con $p_T$ = 4 retardos de las medias transversales, en el escenario F tiene un sesgo de 16,8 % y una cobertura de 0,86: peor que el CS-DL en ambos criterios. Con menos retardos ($p_T$ = 1 o 2) no mejora de forma sistemática. Por eso el contraste con medias transversales de la regla de decisión es el CS-DL. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

### 4.2 Tamaño y potencia de los contrastes

**Cointegración.** El contraste tipo Westerlund rechaza menos de lo nominal: sin cointegración queda por debajo del límite inferior de tamaño. Con ajuste lento su potencia es baja: 0,14 de mediana entre las cuatro variantes (0,06-0,28). Por tanto, un no rechazo en datos reales no es evidencia de ausencia de cointegración. Los contrastes de Pedroni tienen tamaño correcto sin factor y potencia alta con ajuste rápido.

**Velocidad de ajuste media.** El estadístico t del MG para $\bar\phi$ no sigue una normal bajo no cointegración. Su distribución es de tipo Dickey-Fuller y está muy desplazada hacia valores negativos. El valor crítico simulado al 5 % es -8,83 estadístico t, frente al valor crítico de la distribución normal. Usar el valor normal llevaría a declarar ajuste hacia el equilibrio en paneles que no lo tienen. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

**Raíz unitaria.** El CIPS tiene tamaño correcto sobre un paseo aleatorio puro. Sobrerrechaza cuando la serie es I(1) con un componente I(0) grande: en el escenario con factor estacionario rechaza más de la mitad de las veces. En ese caso, un rechazo del CIPS no prueba estacionariedad.

**Homogeneidad.** La variante elegida del Hausman, con varianza no paramétrica del MG, tiene una potencia moderada frente a $\theta_i$ heterogéneo (docs/v7/validacion_herramientas.md). Sin cointegración rechaza alrededor de una de cada cuatro veces.

### 4.3 Lectura conjunta por estimador

| Herramienta | Sin factor o con factor estacionario | Factor I(1), cargas heterogéneas | Uso en la aplicación |
|---|---|---|---|
| MG | apto | no apto (sesgo muy alto) | no se usa sin ajuste |
| MG con demeaning | apto | no apto (sesgo moderado, cobertura cercana) | estimador principal de la regla |
| PMG | con reservas (cobertura baja) | no apto | no se usa sin ajuste |
| PMG con demeaning y bootstrap | apto | no apto (sesgo moderado, cobertura aceptable) | contraste de signo |
| DFE | apto si el largo plazo es homogéneo | no evaluado | solo como contraste |
| CS-DL | no apto con $N$ = 17 | el menos sesgado, cobertura baja | contraste de signo | <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
| CS-ARDL | no apto | no apto | no se usa en la regla |
| Tipo Westerlund | tamaño inferior al nominal | rechaza (cointegración conjunta con el factor) | diagnóstico; un no rechazo no es concluyente |
| Pedroni | tamaño correcto | — | diagnóstico |
| CIPS | tamaño correcto con paseo aleatorio; sobrerrechaza con I(1) + I(0) | — | diagnóstico, sin valor confirmatorio |
| Hausman (varianza del MG) | potencia moderada | rechaza a menudo sin cointegración | no basta para afirmar heterogeneidad |

La tabla resume las secciones 4.1 y 4.2. Las cifras completas están en docs/v7/validacion_herramientas.md. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

Hay dos lecturas. La primera: no existe un estimador dominante con este tamaño de panel. Cada uno falla en un escenario plausible, y por eso tiene sentido exigir coincidencia de signo entre estimadores con supuestos distintos. La segunda: los diagnósticos de integración y cointegración tienen tamaño o potencia insuficientes en los casos que importan. Sus resultados son condiciones necesarias para interpretar un largo plazo, no pruebas de que exista.

### 4.4 Regla de decisión derivada de la simulación

Como ningún estimador es apto en el escenario relevante, la aplicación usa una regla de triangulación fijada antes de estimar con datos reales. Una hipótesis de signo del largo plazo solo se confirma si se cumplen tres condiciones:
- la p ajustada por Holm del MG con demeaning es menor de 0,05; <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- el PMG con demeaning tiene el mismo signo;
- el CS-DL ($p_T$ = 4) tiene el mismo signo. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

La magnitud se publica como el rango entre los tres.

## 5. Aplicación a las 17 comunidades autónomas

**Datos.**
- Panel trimestral de las 17 comunidades autónomas, 2007T1-2026T2. Ceuta y Melilla quedan fuera. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- Variables dependientes: índice de precios de vivienda (IPV) del INE en compra y componente de alquiler del IPC por comunidad.
- Regresores de largo plazo: ocupados de la EPA, población, importe de hipotecas y tasa de paro.

Todos los cruces se hacen por código INE. El panel ya se había usado en la primera versión del proyecto, así que toda estimación se rotula «informativo, muestra ya vista». La validación limpia se reserva para datos publicados después del pre-registro (sección 8). <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

**Componente común.** Antes de estimar, una descripción. Se regresa la variación interanual de cada comunidad sobre la media de las 17. El R² mediano es 93,6 % en compra (rango entre comunidades: 81,0-97,8 %) y 86,1 % en alquiler (64,9-97,4 %). La correlación media entre pares de comunidades es 0,92 en compra y 0,86 en alquiler. Es contabilidad de varianza, no un modelo: la media incluye a la propia comunidad. Pero sitúa el panel español cerca del escenario F de la simulación. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

**Orden de integración.** No se descarta que la variable dependiente sea I(2) en 8 de 17 comunidades en compra y en 9 de 17 en alquiler. Si lo fuera, los estimadores ARDL y las cotas de Pesaran, Shin y Smith no serían válidos. Se añade una sensibilidad en diferencias, que no es confirmatoria. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

**Largo plazo.** De las siete hipótesis de signo pre-registradas, se confirman 0. Cuatro hipótesis son de compra (empleo, hipotecas, población y paro) y tres de alquiler (empleo, población y paro). En ninguna la p de Holm del MG con demeaning baja de 0,05. En varias, los tres estimadores discrepan en el signo. El signo del coeficiente cambia además con el orden de retardos en la mayoría de las combinaciones de especificación, variable y estimador. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

**Cointegración y ajuste.**
- La velocidad de ajuste media tiene el signo esperado, pero su t de MG no alcanza el valor crítico simulado en ninguna especificación (-0,17 por trimestre; t de MG = -6.56 frente al valor critico simulado -8,83 (no rechaza); sin IC valido en compra y -0,05 por trimestre; t de MG = -3.12 frente al valor critico simulado -8,83 (no rechaza); sin IC valido en alquiler, especificación A).
- El contraste tipo Westerlund no rechaza, aunque, dada su potencia, esto no prueba ausencia de cointegración.
- Pedroni rechaza solo en una especificación de compra.
- Las cotas ARDL por comunidad rechazan con frecuencia la ausencia de cointegración. Pero ese diagnóstico no está validado por la simulación y no es válido si hay I(2).

**Heterogeneidad.** El Hausman rechaza en una especificación de compra. Por la simulación, eso no basta para afirmar heterogeneidad del largo plazo: sin cointegración rechaza a menudo. Un modelo jerárquico bayesiano encoge las velocidades regionales hacia una media próxima a cero en alquiler (-0,00 coef. trimestral por trimestre, especificación A).

**Predicción.** En un ejercicio de predicción de origen móvil con selección en muestra (optimista), el mejor modelo por comunidad bate a la base más exigente en 6 de 17 comunidades en alquiler y en 5 de 17 en compra. El PMG no la bate en ninguna. Los modelos quedaron congelados con su huella sha256 antes de la evaluación diferida. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

## 6. Implicaciones para la literatura regional

**1. El componente común es el problema de primer orden.** La simulación muestra que el sesgo de los estimadores habituales con un factor no estacionario de cargas heterogéneas es del orden de la magnitud de los coeficientes que se quieren interpretar. Un estudio regional debería documentar: <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- cuánto pesa el componente común;
- si las cargas difieren entre regiones;
- qué hace el estimador con él.

**2. Los valores críticos deben ser los del diseño.** Con $N$ pequeño, los valores críticos asintóticos de la velocidad de ajuste, del CIPS o de los contrastes de cointegración pueden ser muy engañosos. El valor crítico de $\bar\phi$ simulado aquí es varias veces mayor, en valor absoluto, que el de la normal. Un Monte Carlo con el tamaño del panel, como el de esta nota, es barato y debería acompañar a la estimación. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

**3. Los coeficientes se publican como rangos.** Un único estimador, elegido a posteriori, transmite una precisión que el diseño no tiene. La regla de triangulación (signo coincidente entre estimadores con supuestos distintos y magnitud como rango) es exigente, pero honesta con lo que el panel puede decir. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

**4. Los resultados negativos son informativos.** Que ninguna hipótesis se confirme no prueba que el empleo o la población no estén relacionados con los precios a largo plazo. Indica que este panel no permite separar esa relación del componente común con la fiabilidad que exige el criterio. Es compatible con resultados positivos de otros trabajos con más unidades o más estructura. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

Para España, Álvarez-Román y García-Posada (2021) estudian la valoración de los precios con un enfoque regional. No se ha comprobado si su diseño es de panel, así que no se usa como término de comparación de estimadores.

## 7. Limitaciones

- **Proceso generador.** El de la simulación es una aproximación. Otros procesos (varios factores, cargas variables en el tiempo, rupturas en el largo plazo) pueden dar otro ranking de estimadores.
- **Contraste de Westerlund.** Es una variante con remuestreo, no el estadístico original. Sus resultados no se han comparado con las implementaciones de referencia (xtpmg o xtwest) por falta de esos programas en el entorno de trabajo.
- **Muestra ya vista.** El panel español se había usado antes. Las estimaciones de la sección 5 son informativas y la única validación limpia es la diferida. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- **Contabilidad de varianza.** El R² frente a la media transversal es descriptivo e incluye a la propia comunidad en la media. No mide la carga de un factor estructural.
- **Calidad de los regresores.** Son de fuente única (INE). La EPA tiene una ruptura en 2021, tratada con una variable ficticia. No hay deflactor regional.
- **Literatura.** Los DOI se han verificado en Crossref, pero no los cuartiles: Scimago no fue accesible desde el entorno de trabajo. Ninguna referencia figura como VERIFICADA completa.
- **Alcance.** Nada de esta nota es causal ni recomienda instrumentos de política.

## 8. Reproducibilidad

- **Código.**
  - Herramientas: src/v7/panel_tools.py.
  - Simulación: src/v7/r2_montecarlo.py y src/v7/r2_mc3.py. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
  - Aplicación: src/v7/r4a_run.py y src/v7/r4b_run.py. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
  - Cifras de esta nota: src/v7_1/s3_hechos.py. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- **Ejecución.** `make v7` reconstruye todo sin red y de forma determinista (semilla 20261010, un hilo); dos ejecuciones en un clon limpio dan ficheros idénticos. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- **Resultados.** Simulación completa en output/v7/R2/montecarlo_r3.csv y en docs/v7/validacion_herramientas.md. Pre-registro en docs/v7/hipotesis.md (etiqueta `prereg-v7`) y desviaciones en docs/v7/desviaciones.md. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- **Validación diferida.** `make evaluate_v7` evaluará una sola vez los modelos congelados con los datos de 2026T3-2027T2. El protocolo está en docs/v7_1/evaluacion_2027.md. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

## Referencias

Estado: «DOI verificado» significa que se ha comprobado en Crossref el 12 de octubre de 2026. Ningún cuartil está verificado en Scimago: todas figuran como «cuartil no verificado».

- Álvarez-Román, L. y García-Posada, M. (2021). Are house prices overvalued in Spain? A regional approach. *Economic Modelling*, 99, 105499. DOI 10.1016/j.econmod.2021.105499. DOI verificado; cuartil no verificado. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- Bailey, N., Holly, S. y Pesaran, M. H. (2016). A two-stage approach to spatio-temporal analysis with strong and weak cross-sectional dependence. *Journal of Applied Econometrics*, 31(1), 249-280. DOI 10.1002/jae.2468. DOI verificado; cuartil no verificado. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- Chudik, A., Mohaddes, K., Pesaran, M. H. y Raissi, M. (2016). Long-run effects in large heterogeneous panel data models with cross-sectionally correlated errors. En *Essays in Honor of Aman Ullah* (Advances in Econometrics, 36), 85-135. DOI 10.1108/S0731-905320160000036013. DOI verificado; volumen no devuelto por Crossref; cuartil no verificado. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- Chudik, A. y Pesaran, M. H. (2015). Common correlated effects estimation of heterogeneous dynamic panel data models with weakly exogenous regressors. *Journal of Econometrics*, 188(2), 393-420. DOI 10.1016/j.jeconom.2015.03.007. DOI verificado; cuartil no verificado. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- Driscoll, J. C. y Kraay, A. C. (1998). Consistent covariance matrix estimation with spatially dependent panel data. *Review of Economics and Statistics*, 80(4), 549-560. DOI 10.1162/003465398557825. DOI verificado; cuartil no verificado. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- Hausman, J. A. (1978). Specification tests in econometrics. *Econometrica*, 46(6). DOI 10.2307/1913827. DOI verificado; páginas por completar; cuartil no verificado. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- Holly, S., Pesaran, M. H. y Yamagata, T. (2010). A spatio-temporal model of house prices in the USA. *Journal of Econometrics*, 158(1), 160-173. DOI 10.1016/j.jeconom.2010.03.040. DOI verificado; cuartil no verificado. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- Kapetanios, G., Pesaran, M. H. y Yamagata, T. (2011). Panels with non-stationary multifactor error structures. *Journal of Econometrics*, 160(2), 326-348. DOI 10.1016/j.jeconom.2010.10.001. DOI verificado; cuartil no verificado. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- MacKinnon, J. G. y Webb, M. D. (2017). Wild bootstrap inference for wildly different cluster sizes. *Journal of Applied Econometrics*, 32(2), 233-254. DOI 10.1002/jae.2508. DOI verificado; cuartil no verificado. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- Pedroni, P. (1999). Critical values for cointegration tests in heterogeneous panels with multiple regressors. *Oxford Bulletin of Economics and Statistics*, 61(S1), 653-670. DOI 10.1111/1468-0084.61.s1.14. DOI verificado; cuartil no verificado. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- Pedroni, P. (2004). Panel cointegration: asymptotic and finite sample properties of pooled time series tests with an application to the PPP hypothesis. *Econometric Theory*, 20(3). DOI 10.1017/S0266466604203073. DOI verificado; páginas por completar; cuartil no verificado. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- Pesaran, M. H. (2006). Estimation and inference in large heterogeneous panels with a multifactor error structure. *Econometrica*, 74(4), 967-1012. DOI 10.1111/j.1468-0262.2006.00692.x. DOI verificado; cuartil no verificado. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- Pesaran, M. H. (2007). A simple panel unit root test in the presence of cross-section dependence. *Journal of Applied Econometrics*, 22(2), 265-312. DOI 10.1002/jae.951. DOI verificado; cuartil no verificado. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- Pesaran, M. H., Shin, Y. y Smith, R. P. (1999). Pooled mean group estimation of dynamic heterogeneous panels. *Journal of the American Statistical Association*, 94(446), 621-634. DOI 10.1080/01621459.1999.10474156. DOI verificado; cuartil no verificado. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- Pesaran, M. H. y Smith, R. (1995). Estimating long-run relationships from dynamic heterogeneous panels. *Journal of Econometrics*, 68(1), 79-113. DOI 10.1016/0304-4076(94)01644-F. DOI verificado; cuartil no verificado. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
- Westerlund, J. (2007). Testing for error correction in panel data. *Oxford Bulletin of Economics and Statistics*, 69(6), 709-748. DOI 10.1111/j.1468-0084.2007.00477.x. DOI verificado; cuartil no verificado. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

## Revistas propuestas para el envío

| Revista | Cuartil Scimago | Encaje |
|---|---|---|
| Journal of Housing Economics | cuartil no verificado | vivienda aplicada con paneles de precios | <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
| Regional Science and Urban Economics | cuartil no verificado | paneles regionales y dependencia espacial | <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->
| Empirical Economics | cuartil no verificado | metodología de panel y simulación | <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

Los ISSN, comprobados en Crossref, están en docs/v7_1/literatura_nota.md. El cuartil de las tres revistas está pendiente de lectura en Scimago (docs/v7_1/tareas_autor.md). No se debe enviar sin verificarlo. <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

*Declaración: el código y los textos se elaboraron con asistencia de una herramienta de IA bajo la dirección y la revisión del autor (ver docs/v7_1/tareas_autor.md, licencias y declaración de IA).* <!-- check:cifra-libre (parámetro del diseño, tamaño del panel, constante de referencia, ruta o referencia bibliográfica; no es una cifra de resultado) -->

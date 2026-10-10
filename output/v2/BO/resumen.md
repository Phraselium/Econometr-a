# Rama BO (oferta y suelo): resumen

Datos solo vía `v2_common.load`; sin muestra sellada. Dos ejecuciones con md5 idénticos (16 ficheros). Registro: `registro.csv` (todas las especificaciones). Elecciones no fijadas en el pre-registro: `desviaciones.md`.

## 1. H4 (confirmatoria) — nivel: EXPLORATORIO
Panel anual de 47 provincias, 2009-2023 (iniciadas desde 2008; sin datos de iniciadas en 2016-2017 para ninguna provincia; N=550). Δ ln iniciadas_t sobre Δ ln precio real_{t−1} y su interacción con ln p_suelo 2005-2007 centrado; FE provincia y año; cluster provincia; WCR Webb 9.999.

| | coef | EE | IC95 | p unilateral (bootstrap) |
|---|---|---|---|---|
| Δ ln precio real (t−1) | 1,040 | 0,507 | [0,02; 2,06] | 0,022 (H: >0) |
| × ln suelo centrado | −1,163 | 0,559 | [−2,29; −0,04] | 0,026 (H: <0) |

Signos como en la hipótesis; p_IUT = 0,026 sin ajustar. Elasticidad de iniciadas libres ~1 y menor con suelo más caro (en provincia con suelo un 10 % más caro que la media, la elasticidad baja ~0,12).

Por qué NO sube de nivel:
- **Submuestras (regla ex ante: 5 con signos correctos):** fallan 2009-2013 (β_precio = −1,81) y, en robustez, el precio en t−2 (β_precio ≈ 0). Pasan sin Madrid-Barcelona (p_IUT 0,077), 2014-2023 (β_inter = −0,59, p 0,31), 2009-2019 (p_IUT 0,21) y sin 2020-2021 (p 0,10). El resultado se apoya en 2014-2023 para el precio y en 2009-2019 para la interacción: no es estable.
- **Holm sobre las 7 lo aplica el orquestador.** Con p_IUT = 0,026, solo sobreviviría si fuera la menor de las 7 y ≤ 0,0071; no es el caso (0,026 > 0,0071), así que no sobrevive con la familia completa salvo que los demás p sean mayores y el corte aplicable sea 0,05/7 para el menor.
- **No es CAUSAL:** el precio es endógeno (la demanda y las expectativas mueven a la vez precio e iniciación). 2SLS con ocupados y población 20-34 (t−1): β_precio = 0,73 (EE 2,49), p_IUT = 0,64; F de primera etapa 5,9 (precio) y 20,8 (interacción); J de Hansen = 14,3, p = 0,0008 (rechaza validez conjunta). Con un solo instrumento: F = 2,5 (ocupados) o 10,8 (población); ni signos ni significación. El placebo de precio futuro (t+1) tiene coeficiente 0,90 (p 0,17), del mismo tamaño que el efecto principal: no descarta anticipación o endogeneidad.

## 2. Déficit (DESCRIPTIVO)
- **Nacional 2021Q1-2024Q2** (EPA corregida como v1): déficit 632.861 sin protegida; 598.157 con protegida (34.704 viviendas, reescaladas por cobertura 0,955; cota inferior 33.164 → 599.697). ECP (2021Q1-2024Q1, stock a día 1): 550.523 sin protegida; 518.074 con protegida (32.449).
- **Parte de la diferencia con el BdE atribuible a protegida.** Los 750.000 del BdE son 2021-2025 y nuestros paneles terminan en 2024Q2: no se reproduce la cifra del BdE. Ilustración aritmética (protegida a la media de 2.479 por trimestre durante los 6 trimestres que faltan, supuesto sin datos): ≈ 49.600 viviendas en 2021-2025, el 43 % del residuo de v1 con EPA (116.100) y el 81 % del residuo con ECP (60.936). Es una cota de orden de magnitud: la protegida es «calificaciones definitivas» (aproximación a terminadas), no hay protegida del 2024Q3 en adelante en entrenamiento.
- **Provincial:** sin hogares provinciales pre-2021, proxy = Δ población total / 2,53 − terminadas libres − protegida (2020-2022). Mayor déficit por 1.000 hab.: Tarragona (43), Almería (04), Girona (17), Castellón (12), Ourense (19). Proxy; no es un déficit medido (`deficit_provincial_proxy.csv`).

## 3. Suelo (EXPLORATORIO)
Proyecciones locales h=1..8 (FE provincia y trimestre, controles: variación propia a 4 trimestres). p_suelo trimestral es muy ruidoso (DE de Δ4 = 0,28 frente a 0,07 del precio): con la serie cruda no hay señal en ningún periodo (P1-P4) ni dirección (mín. p suelo→precio 0,07, precio→suelo 0,05, ningún BH<0,05). Con media móvil de 4 trimestres solo hay señal de que el suelo precede al precio en P4 (2022Q1-2024Q2): 3 horizontes con p<0,05, 1 con BH<0,05, con muestras pequeñas (n=94 a h=8). El precio nunca precede al suelo. Lectura: el suelo no anticipa de forma robusta el precio; la evidencia es compatible con una relación débil y con error de medida grande, no con «el suelo sigue al precio».

## 4. Panel UE (EXPLORATORIO)
Elasticidad de los permisos al precio real (t−1), anual: España 1,91 (EE 1,23) frente a la media de 26 países UE 0,99 (EE 0,21); España es la 5.ª más alta. Panel con FE país y año: 1,69 (España) frente a 0,62 (resto), diferencia 1,07 (p = 0,0004, cluster país con España como un único cluster: EE aproximado). Trimestral: 1,27 frente a 0,57. Alquiler: España −6,0 (EE 2,9), la más baja de 27, frente a +2,7 de media UE: resultado implausible (la serie de alquiler HICP de España casi no varía); no interpretar. Series de 11-18 años: elasticidades por país muy imprecisas.

## 5. Fuera de muestra (h=4, bloques con embargo, test 2014Q1-2024Q2, DM-HLN)
- **Precio real (26 periodos, 1.211 obs.; primaria P3 = AR(4) + iniciadas + suelo):** RMSE 0,0586 frente a AR(4) 0,0394 y ECM v1 0,0647; DM vs AR(4) −1,39 (p 0,18; peor), vs ECM v1 +0,33 (p 0,74). Ninguna de las 4 configuraciones mejora al AR(4); P2 (suelo) iguala (0,0404) y mejora al ECM v1 con p = 0,096.
- **Iniciadas (22 periodos, 1.025 obs.):** AR(4) + precio: RMSE 0,508 frente a 0,526 del AR(4), DM +2,29 (p 0,032; BH sobre 6 contrastes 0,097); + suelo: 0,506, DM +2,39 (p 0,026; BH 0,097). El suelo no aporta sobre el precio. Sin ECM v1 (no definido).
- Dos huecos de datos (iniciadas 2016-2017) reducen la muestra de iniciadas.

## Qué NO se puede afirmar
- Que la elasticidad de las iniciadas al precio sea causal ni que sea ~1 de forma estable (cambia de signo en 2009-2013; no hay instrumento válido).
- Que el suelo barato eleve la elasticidad (interacción significativa solo con el panel completo y 2009-2019).
- Que H4 sea ASOCIACIÓN ROBUSTA: falla submuestras y el IV no la respalda; Holm-7 pendiente (orquestador).
- Cifras de déficit comparables con el BdE (periodos distintos); la parte atribuida a protegida es una ilustración con supuestos.
- Que el suelo anticipe o siga al precio con la serie actual.
- La comparación de alquiler UE (España −6) ni las elasticidades por país individuales.
- Mejora fuera de muestra del precio con variables de oferta: no la hay frente al AR(4).

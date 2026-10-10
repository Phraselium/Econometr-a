# Rama BO (oferta y suelo): resumen

Datos solo vía `v2_common.load`; sin muestra sellada. Dos ejecuciones con md5 idénticos . Registro: `registro.csv` (todas las especificaciones; 250 filas). Elecciones no fijadas en el pre-registro: `desviaciones.md`.

## 1. H4 (confirmatoria) — nivel: EXPLORATORIO
Panel anual de 47 provincias, **2005-2023 (muestra pre-registrada)**, N=879, iniciadas libres de la tabla anual MIVAU 32200500 (libres, no totales: desviación 1b). Δ ln iniciadas_t sobre Δ ln precio real_{t−1} y su interacción con ln p_suelo 2005-2007 centrado; FE provincia y año; cluster provincia; WCR Webb 9.999. Estimada una vez.

| | coef | EE | IC95 | p unilateral (bootstrap) |
|---|---|---|---|---|
| Δ ln precio real (t−1) | 0,794 | 0,340 | [0,11; 1,48] | 0,011 (H: >0) |
| × ln suelo centrado | −0,616 | 0,336 | [−1,29; 0,06] | 0,059 (H: <0) |

Signos como en la hipótesis; p_IUT = 0,046 sin ajustar. Asociación (elasticidad estimada, no estructural) ~0,8 y algo menor con suelo más caro (suelo un 10 % más caro que la media: ≈ −0,06).

Por qué NO sube de nivel:
- **Submuestras (regla ex ante: S1-S5 con los dos signos):** fallan 2005-2013 (β_precio = −0,49) y 2014-2023 (β_interacción = +0,37); en robustez el precio en t−2 da β_precio ≈ −0,17. Pasan sin Madrid-Barcelona (p_IUT 0,17), 2005-2019 (0,058) y sin 2020-2021 (0,060). El precio solo es claramente positivo en 2014-2023 (2,60).
- **Holm sobre las 7 lo aplica el orquestador.** p_IUT = 0,046 sin ajustar; con la familia completa solo sobreviviría si fuera el menor y ≤ 0,0071: no se cumple.
- **No es CAUSAL:** el precio es endógeno. 2SLS (ocupados y población 20-34, t−1): β_precio = 2,48 (EE 1,77), p_IUT = 0,25; F de primera etapa 5,3 (precio) y 48,4 (interacción); J de Hansen = 16,5, p = 0,0003. Con un solo instrumento F = 4,2 o 9,1. El placebo de precio futuro (t+1) tiene coeficiente 1,27 (p = 0,012): significativo y mayor que el efecto principal, es decir, hay anticipación o endogeneidad.
- Robustez R0 (estimación previa vista antes, 2009-2023 con suma mensual, N=550): β_precio 1,04; β_interacción −1,16; p_IUT 0,026; no se usa como principal.

## 2. Déficit (DESCRIPTIVO)
- **Nacional 2021Q1-2024Q2** (EPA corregida como v1): 632.861 sin protegida; 598.157 con protegida (34.704 viviendas OBSERVADAS, reescaladas por cobertura 0,955; cota inferior 33.164 → 599.697). ECP (2021Q1-2024Q1): 550.523 sin; 518.074 con (32.449).
- **Comparación con el BdE.** Los 750.000 del BdE son 2021-2025; los paneles de entrenamiento terminan en 2024Q2, no se reproduce esa cifra. La ilustración ≈ 49.600 se descompone en **34.704 observados (2021Q1-2024Q2)** + **14.873 SUPUESTOS (2024Q3-2025Q4: 6 trimestres a la media observada de 2.479; sin datos)**. Frente a los residuos de v1 (116.100 EPA; 60.936 ECP, calculados por v1 con datos de 2024Q3-2025Q4, cifras publicadas), lo observado equivale al 30 % y al 57 %, y con el supuesto al 43 % y 81 %. Orden de magnitud, no estimación. La protegida son calificaciones definitivas (aproximación a terminadas).
- **Provincial:** sin hogares provinciales pre-2021, proxy = Δ población total / 2,53 − terminadas libres − protegida (2020-2022), por 1.000 habitantes: Tarragona 12,5; Almería 12,4; Girona 11,4; Castellón 9,9; Guadalajara 9,5. Proxy, no déficit medido.

## 3. Suelo (EXPLORATORIO)
Proyecciones locales h=1..8 (FE provincia y trimestre; control: variación propia a 4 trimestres), 160 contrastes; BH y Holm sobre los 160. La serie cruda es muy ruidosa (DE de Δ4 = 0,28 frente a 0,07 del precio): sin señal. La variante «media4T» (media móvil de 4 trimestres) se añadió a posteriori, tras ver la cruda. Con ella, el suelo precede al precio solo en P4 (2022Q1-2024Q2; h=6 coef 0,028, p=1,3·10⁻⁴, BH=Holm=0,021 sobre 160), con muestra pequeña (n=186). El precio nunca precede al suelo. El suelo no anticipa de forma robusta el precio.

## 4. Panel UE (EXPLORATORIO)
Elasticidad de los permisos al precio real (t−1), anual: España 1,91 (EE HAC 1,23) frente a 0,99 de media UE (26 países, EE 0,21); España es la 5.ª más alta de 27. Panel con FE país y año: 1,69 (España) frente a 0,62 (resto); no se dan p ni EE de la diferencia (España es un único clúster: inferencia cluster no válida). Trimestral: 1,27 frente a 0,57 (HICP general trimestral «anual_asignado»). Alquiler: España −6,0 frente a +2,7 de media UE, la más baja; el valor lo generan dos episodios en que el alquiler real y los permisos se mueven en sentido contrario (2008-2010 y 2021-2023, con la inflación general alta); no interpretar. Series de 11-18 años: elasticidades por país imprecisas.

## 5. Fuera de muestra (h=4, bloques con embargo, test 2014Q1-2024Q2, DM-HLN)
- **Precio real (26 periodos, 1.211 obs.; primaria P3 = AR(4) + iniciadas + suelo):** RMSE 0,0586 frente a AR(4) 0,0394 y ECM v1 0,0647; DM vs AR(4) −1,39 (p 0,18; peor), vs ECM v1 +0,33 (p 0,74). Ninguna de las 4 configuraciones mejora al AR(4); P2 (suelo) iguala (0,0404) y mejora al ECM v1 con p = 0,096.
- **Iniciadas (22 periodos, 1.025 obs.):** AR(4) + precio: RMSE 0,508 frente a 0,526 del AR(4), DM +2,29 (p 0,032; BH sobre 6 contrastes 0,097); + suelo: 0,506, DM +2,39 (p 0,026; BH 0,097). El suelo no aporta sobre el precio. Sin ECM v1 (no definido).
- El OOS de iniciadas usa la suma trimestral (faltan 2016Q2 y 2017Q2): reduce la muestra; no se rehízo con la serie anual. Δ4 ln iniciadas no está escalado y tiene colas grandes en provincias pequeñas; puede explicar que empeore el precio.

## Qué NO se puede afirmar
- Que la elasticidad de las iniciadas al precio sea causal ni que sea ~1 de forma estable (cambia de signo en 2005-2013; no hay instrumento válido).
- Que el suelo barato eleve la elasticidad (la interacción cambia de signo en 2014-2023 y su p unilateral es 0,059).
- Que H4 sea ASOCIACIÓN ROBUSTA: falla submuestras y el IV no la respalda; Holm-7 pendiente (orquestador).
- Cifras de déficit comparables con el BdE (periodos distintos); la parte atribuida a protegida es una ilustración con supuestos.
- Que el suelo anticipe o siga al precio con la serie actual.
- Diferencias significativas España-UE (sin inferencia válida), el alquiler UE (España −6) ni elasticidades por país individuales.
- Mejora fuera de muestra del precio con variables de oferta: no la hay frente al AR(4).

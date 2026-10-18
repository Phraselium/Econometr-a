# V16 · Revisión adversarial (fase 6.5): objeciones y respuesta

Tres revisiones de abogado-del-diablo (solo lectura, 2026-10-18) sobre los resultados y pistas que se citarán en el informe.

Cada objeción se resuelve de una de tres maneras:
- **Corregida**: era un error frente a la ficha y se arregla (decisión K17 de docs/v16/decisiones.md).
- **Contrastada**: se comprueba con datos del repositorio.
- **Limitación**: se declara en el informe, en la ficha del resultado y en la Parte VII.

Ninguna objeción sube la capa de nada: todo sigue en C4 y la mayoría es solo estimación puntual. No se ha abierto ninguna muestra sellada.

## A. Inmigración y exuberancia (Q9-g, Q3-b, H4)

| # | Resultado | Gravedad | Objeción (resumen) | Respuesta |
|---|---|---|---|---|
| 1 | Q9-g | alta | La mayoría de las fechas marcadas caen cuando el cociente baja o está plano | **Limitación** (Parte VII). Se lee como artefacto probable, no como exuberancia. |
| 2 | Q9-g | alta | Tasación suavizada; un ADF sin rezagos y un bootstrap salvaje que rompe la autocorrelación de Δy no están validados para Δy persistente | **Limitación**. Es la segunda advertencia del autor (K15). El APTO de la fase 5 no cubre este proceso generador. |
| 3 | Q9-g | alta | La potencia validada frente a burbujas es baja: un p de 0,004 apunta a error de especificación | **Limitación**, junto con la 2. |
| 4 | Q9-g | alta | Tendencia sin modelar; nulo sin deriva | **Limitación** (ya estaba en la ficha). |
| 5 | Q9-g | alta | Una exuberancia estadística no identifica una burbuja; con tipos de interés, V7.2 no rechaza | **Limitación**. Es la tercera advertencia del autor (K15). |
| 6 | Q9-g | media | El IPC de alquiler es un stock; la alternativa SERPAVI no rechaza | **Limitación**. Se cita la alternativa. |
| 7 | Q9-g | media | El factor por componentes principales en niveles puede mezclar tendencias | **Limitación**. |
| 8 | Q9-g | media | Sensibilidad a la ventana y a r0 | **Limitación**. Con la ventana de V7.2 no hay rechazo tras BH (lo ya visto). |
| 9 | Q9-g | media | BY en lugar de BH | **Contrastada**. La adenda (punto 2) obliga a usar BY si el Monte Carlo no apoya la dependencia positiva. El BH jerárquico dio una FDR máxima de 0,122 > 0,10 (fase 5, bh_jerarquico): se aplica BY (K12). El q vigente es 0,306 (K16); el 0,153 de K15 y de B-2 queda como histórico. |
| 10 | Q3-b | alta | La pretendencia es más de la mitad del coeficiente | **Limitación**. Ya figuraba como prueba fallida. Se cita como correlación con pretendencia del mismo orden. |
| 11 | Q3-b | alta | Reversión a la media o convergencia; desbalance de renta | **Limitación**. |
| 12 | Q3-b | media | Exposición de 2022 dentro de la ventana del resultado | **Limitación**. Viene del diseño pre-registrado. |
| 13 | Q3-b | media | Confusor turístico; la cuota no europea da menos | **Limitación**. |
| 14 | Q3-b | media | La principal es la mayor de las seis variantes | **Limitación**. Se cita con su rango. Estaba pre-registrada, no se eligió. |
| 15 | Q3-b | baja | Placebo contaminado por la COVID | **Limitación**. |
| 16 | H4 | alta | Principal en la cola alta del multiverso; cambia de signo sin los 5 orígenes principales | **Limitación**. Se cita como frágil, con mediana y rango. |
| 17 | H4 | alta | Pocos orígenes efectivos (Colombia, Bulgaria, Ecuador, Marruecos) | **Limitación**. |
| 18 | H4 | media | El padrón por nacionalidad no recoge las nacionalizaciones | **Limitación**. El país de nacimiento no está en el entrenamiento de V15. |
| 19 | H4 | media | 2SLS 4,5 veces el MCO | **Limitación**. |

## B. Regulación y turismo (H1, H2, Q1c, H3, Q2)

| # | Resultado | Gravedad | Objeción (resumen) | Respuesta |
|---|---|---|---|---|
| 1 | H1 | alta | Placebo y pretendencias del tamaño del efecto | **Limitación**. Ya eran pruebas fallidas. H1 solo se cita en el signo, sin magnitud. |
| 2 | H1 | alta | Anticipación por la Ley 12/2023; reversión tras la STC 37/2022 | **Limitación**. |
| 3 | H1 | alta | Composición por tramos y paso a contratos de temporada | **Limitación**. |
| 4 | H1 | alta | Selección y falta de soporte común; la cota de Lee llega a 0 | **Limitación**. |
| 5 | H1 | media | El control sintético de los grandes municipios da signo contrario | **Limitación**. |
| 6 | H1 | media | Citar el rango, no el extremo | **Aceptada**. El informe cita el rango CS-SDID. |
| 7 | H2 | alta | Sin señal estable | **Limitación**. H2 no se cita como pista. |
| 8 | H2 | media | Ceros imputados | **Limitación**. |
| 9 | Q1c | alta | No se distingue del ruido previo | **Limitación**. Q1c no se cita como pista. |
| 10 | Q1c | alta | Provincias distintas; cambios del ITP | **Limitación**. |
| 11 | Q1c | media | Tratamiento diluido y fechas de cohorte | **Limitación**. |
| 12 | H3 | alta | La principal es el mínimo del multiverso; «preciso» sin un EE válido | **Corregida en el texto**. Se quita «preciso» y H3 queda «no concluyente», no «nula»; se cita la mediana. |
| 13 | H3/Q2 | alta | Sesgo hacia cero por la medida (poca variación, stock, topes) | **Limitación**. |
| 14 | H3 | media | Los efectos de municipio × año absorben parte del efecto; quedan fuera los mercados más turísticos | **Limitación**. |
| 15 | Q2a | media | Depende de los controles y de la fecha de la exposición | **Limitación**. |
| 16 | Q2c | media | La principal no era la de la adenda (Δlog y exposición estandarizada en nivel) | **Corregida** (K17). La principal pasa a ser la de la adenda; la versión anterior queda como variante. |
| 17 | H3/Q2 | media | Las escalas «por DT» no son comparables | **Limitación**. El informe no compara magnitudes entre diseños. |

## C. Macro, predicción y fiscalidad (H5, Q10, E3, Q6, Q5)

| # | Resultado | Gravedad | Objeción (resumen) | Respuesta |
|---|---|---|---|---|
| 1.1 | H5 | media | 1,51 es la peor de tres cifras; la serie se eligió con las cifras a la vista | **Aceptada**. Se cita el rango [1,15; 1,51] entre implementaciones. La STL por origen se eligió por la regla «sin datos posteriores al origen», no por su valor; se declara que se decidió después de ver la reconciliación. |
| 1.2 | H5 | media | El ECM del AR(4) no cuadra con la reconciliación | **Contrastada**. Ninguna fila posterior al origen entra en la estimación (comprobado en t = 60). La diferencia viene de una convención: si los rezagos pueden ser anteriores a 2003. Permitiéndolo, el ECM coincide con el de la reconciliación (9,83e-5). |
| 1.3 | H5 | media | DM-HLN es APTO en V15 y NO APTO en V16 (otro proceso generador) | **Limitación**. El p no se cita como prueba. La conclusión (razón > 1 en todas las implementaciones) no depende de él. |
| 1.4 | H5 | baja | El LASSO está roto; no decir «el AR(4) es mejor» | **Aceptada**. Se dice «la combinación no supera al AR(4)». |
| 1.5 | lo ya visto | baja-media | «Ningún modelo predice mejor» frente a K1-N-MEJOR = 6 de 9 | **Pendiente**. Coherencia de la 1.0: se revisa en la fase 7 sin cambiar ninguna cifra 1.0. |
| 2.1 | Q10 | alta | «−18 %» y «−30 %» son empeoramientos | **Aceptada**. El informe dirá «empeora» o «mejora». |
| 2.2 | Q10-3 | alta | El +41 % sale entero de 2020-2021 | **Limitación**. Q10-3 no se cita como pista: «sin mejora fuera de 2020». |
| 2.3 | Q10 | media | Datos revisados, no en tiempo real | **Limitación** (ya declarada en la adenda). |
| 2.4 | Q10 | media | El «ECM v1» es una versión reducida | **Aceptada**. Se dirá «ECM v1 reducido». |
| 2.5 | Q10, Q5, H5 | baja | AR4_S añadido después; las series nacionales incluyen CCAA selladas de v6 | **Limitación**. Las series nacionales no son filas marcadas muestra_sellada_v6; se declara. |
| 3.1 | E3 | alta | ρ puede ser una tendencia regional común | **Limitación**. Se lee como correlación espacial descriptiva, no como contagio. |
| 3.2 | E3 | media-alta | El IC subestima la incertidumbre de especificación | **Aceptada**. Se cita el rango del multiverso junto al IC. |
| 3.3 | E3 | media | Selección de la muestra por vecinos | **Limitación**. |
| 4.1 | Q6-v | alta | El placebo es mayor que el efecto y de signo contrario | **Limitación**. Q6-v queda DESCRIPTIVO (triangulación). |
| 4.2 | Q6 | media-alta | El multiverso incluía el placebo | **Corregida** (K17). Se quitan las 2 dCDH con fecha adelantada. |
| 4.3 | Q6 | media-alta | Pocas unidades efectivas | **Limitación**. |
| 4.4 | Q6 | media | Total de vivienda en lugar de usada | **Limitación** (D2). |
| 4.5 | varios | media | Principales en los extremos de sus multiversos | **Aceptada**. Se cita siempre la mediana y el rango. |
| 4.6 | Q6 | baja-media | Controles contaminados por cambios pasados | **Limitación**. |
| 5.1 | Q5 | alta | Primera etapa de signo equivocado | **Limitación**. Q5 no se cita como pista. |
| 5.2 | Q5 | alta | Placebo comparable; la respuesta cambia de signo; autocorrelación | **Limitación**. |
| 5.3 | Q5 | media | El multiverso no apoya el signo; «63 restantes» frente a n = 15 | **Corregida en el texto**: el informe de Q5 da el número real de especificaciones del resumen. El signo sigue sin apoyo: **limitación**. |
| 5.4 | Q5 | media | La inflación no es un control negativo; ventana más corta | **Limitación**. |

## Qué sobrevive como pista citable

Siempre en C4, sin lenguaje causal y con sus limitaciones:
- H1, solo en el signo;
- H5 («la combinación no supera al AR(4)», en todas las implementaciones);
- E3, como correlación espacial descriptiva.

Q6-p deja de ser pista tras su réplica ciega (K18: era un error de diferencias entre años no consecutivos). Ahora es −0,0020 y queda «no concluyente».

**Q9-g** va solo a la Parte VII, por decisión del autor (K15), con p = 0,004, q = 0,306 y las advertencias.

**No se citan como pista:**
- H2 y Q1c, por ruido previo;
- Q6-v, Q5 y Q10-3;
- Q2c, que tiene signo inestable;
- H3 y Q2a, que son «no concluyentes».

Q3-b y H4 se citan como correlaciones frágiles, con su rango.

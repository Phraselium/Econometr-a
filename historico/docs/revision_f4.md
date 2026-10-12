# Revisión independiente, puerta de la FASE 4 (Oferta, P3)

Fecha: 2026-10-09. Revisor independiente. No he hecho el trabajo de F4 y lo he comprobado todo por mi cuenta.

**Material revisado**
- `docs/decisiones.md` (sección F4, fijada antes de estimar).
- `src/f4_oferta.py` y `src/econ_utils.py` (`dols`, `diagnostics`).
- `output/f4/*` y `output/registro_busqueda_f4.csv`.
- `docs/literatura.md` y `docs/diccionario_variables.md`.
- El PDF oficial del **Informe Anual 2025** del BdE, en castellano: repositorio.bde.es, handle 123456789/43565, `InfAnual_2025.pdf`. Lo descargué para esta revisión y lo leí en las pp. 147-157.

No he modificado `src/`, `data/` ni las salidas de F4. Lo único que escribo es este fichero.

**Aviso: mi ejecución de `make all` regeneró salidas de otras fases.** Ver §1.

## Veredicto: **REHACER** (acotado: texto y una variante; nada de re-estimación de fondo salvo el bootstrap del panel)

**Lo que está bien**
- La cifra principal del déficit es correcta. La he recalculado: **866.100**.
- La conversión de miles es correcta, y también la corrección de 2021T1 y las terminadas libres.
- La ejecución es reproducible y no usa red.
- Las referencias están bien etiquetadas.

**Lo que hay que corregir (cinco problemas)**
1. Un **error de alineación temporal en la variante ECP**. Hace falsa la afirmación de que «2021 solo tiene 3 trimestres».
2. La explicación de la diferencia con el BdE se presenta como «no verificada», pero **se puede reproducir casi exactamente** con datos que ya están en `data/raw`.
3. Una **contradicción interna** en la interpretación de las elasticidades (el papel del colapso 2008-2013).
4. Dos lecturas que van más allá de la evidencia:
   - el panel con efectos de tiempo;
   - los 88 coeficientes que «sobreviven» a Bonferroni.
5. Falta el **wild cluster bootstrap** del panel. Estaba pre-registrado con carácter general ("todas", decisiones.md, l. 10).

---

## 1. Reproducibilidad

| Prueba | Resultado |
|---|---|
| `make all` con la red bloqueada (`HTTP(S)_PROXY=http://127.0.0.1:9`, FORCE sin definir) | exit 0. Todos los fetch salen por caché. F4 tarda 10,1 s. |
| `output/f4/*` y `registro_busqueda_f4.csv` tras `make all`, frente a lo versionado en git | **idénticos** (`git diff` vacío) |
| Segunda ejecución de `src/f4_oferta.py` (sin red): md5 de las 41 salidas de F4 y del registro | **idénticos** a la primera ejecución |
| `data/processed/nacional_q.csv` y `panel_ccaa_q.csv` (entradas de F4) | sin cambios respecto a git |

**Fuera del alcance de F4, pero lo anoto:**
- `make all` también reescribe salidas de F2, F3, F5 y F6 que no coinciden con lo versionado:
  - las salidas versionadas de F3 están desfasadas respecto a su código (126 frente a 218 especificaciones);
  - `resumen_f5.md` incluye el tiempo de ejecución ("31 s" frente a "34 s"), así que su md5 nunca es estable;
  - `data/processed/valencia.csv` cambia.
- Esos ficheros quedan modificados en el árbol de trabajo por mi ejecución. No los he revertido porque podría haber trabajo concurrente de otras fases.
- En la consolidación de F7 conviene eliminar las marcas de tiempo de los resúmenes.

## 2. Datos

**Cifras contrastadas con `data/raw`**

| Cifra | En F4 | En raw | Resultado |
|---|---|---|---|
| Terminadas libres 2021…2025 (`mivau_fin_obra.csv`, `viv_libres_terminadas_nacional`, suma de 12 meses) | — | 84.091 / 79.935 / 80.473 / 86.609 / **80.792** | ✔ coinciden |
| Hogares EPA (`ine_epa_hogares.csv`, EPA430446, miles) | ×1.000 bien aplicado | 18.817,8 (2020T4), 18.610,0 (2021T1), 19.853,4 (2025T4) | ✔ |
| Iniciadas libres 2025 (`mivau_visados.csv`) | — | 121.827 | ✔ coherente con «~140.000 iniciadas o visados» del BdE, que incluye protegidas o visados |

**Recálculo del déficit principal desde `data/processed/nacional_q.csv`**
- Δhogares 2021T1-2025T4 sin corregir = 19.853,4 − 18.817,8 = 1.035.600.
- Δ2021T1 = −207.800. Se sustituye por la media de Δ en 2020T2, 2020T3, 2020T4 y 2021T2 = (10.500 + 15.000 + 18.400 + 94.500)/4 = 34.600.
- Δhogares corregido = 1.278.000.
- Menos las terminadas, 411.900: **déficit = 866.100**. ✔ Exacto.
- Las variantes (a') 831.500, (a'') 623.700 y (c) 802.152 también cuadran.

**Corrección del salto de la EPA de 2021T1: se ajusta al pre-registro, pero con una interpretación discutible**
- decisiones.md dice «media de Δ de los **4 trimestres adyacentes**». El código toma 3 trimestres anteriores y 1 posterior, e incluye 2020T2, el trimestre del confinamiento.
- Sensibilidad que he calculado:

| Ventana de la media | Δ imputado | Déficit |
|---|---|---|
| Simétrica 2+2 (2020T3, 2020T4, 2021T2, 2021T3) | 52.575 | **884.075** |
| 4 posteriores (2021T2-2022T1) | 88.325 | **919.825** |
| La usada (3 anteriores + 1 posterior) | 34.600 | 866.100 |

- No pido cambiar la cifra principal. Sí pido documentar la interpretación y esta sensibilidad: la cifra principal queda en el extremo bajo del rango.

**Terminadas: solo vivienda libre.** Está bien documentado: 80.792 en 2025 frente a 92.000 del BdE.

**ECP (60131): ERROR de alineación (bloqueante para la variante b/b')**
- En raw, la ECP es un **stock a día 1 del trimestre**: `fecha` 2021-01-01 para 2021T1. Por tanto:
  - ECP 2021T1 es el stock a 1-ene-2021, es decir, a final de 2020;
  - la creación de hogares del año natural *t* es H(1-ene-*t*+1) − H(1-ene-*t*).
- Afirmaciones de F4 que son falsas:
  - «ECP existe desde 2021T1: el primer Δ es 2021T2, así que 2021 solo tiene 3 trimestres»;
  - «(b) periodo consistente 2021T2-2025T4».
- Qué hace en realidad la variante (b) actual:
  - mide los hogares de 1-ene-2021 a 1-oct-2025, es decir, de ene-2021 a sep-2025;
  - los empareja con las terminadas de abr-2021 a dic-2025, es decir, con un trimestre de desfase;
  - la imputación (b') sobra.
- Cálculo correcto:
  - ECP de 1-ene-2021 a 1-ene-2026 = 19.762.059 − 18.539.223 = **1.222.836** hogares, el año 2021-2025 completo y sin imputar;
  - déficit con ECP y terminadas libres = 1.222.836 − 411.900 = **810.936**.

## 3. Por qué difiere el BdE (750.000; 700.000 en el IEF): se puede explicar

Lo que dice el **IA 2025**, verificado en el PDF:
- **Gráfico 2.10 (p. 155)**
  - Fuente: «Banco de España con datos del Instituto Nacional de Estadística y el Ministerio de Transportes y Movilidad Sostenible».
  - Nota (a): «diferencia entre el número de viviendas residenciales terminadas y el cambio en el número de hogares residentes».
- **Gráfico 2.11 (p. 157)**, nota (b), para España: «suma entre 2021 y 2025 de la diferencia acumulada entre el número de viviendas residenciales terminadas y la creación neta de hogares».
- **Texto de la p. 157**
  - «creación neta de hogares (240.000, en línea con el promedio anual de 245.000 entre 2021 y 2024)»;
  - «92.000 nuevas viviendas terminadas en 2025», con una reducción del 9 %;
  - déficit del 3,7 % de los hogares residentes en 2025.
- **El BdE no nombra la operación estadística concreta.** No dice si los hogares son ECP o EPA, ni si las terminadas son libres más protegidas o certificados de fin de obra. Eso **no lo he encontrado escrito**.

**Hogares: inferencia mía, con una coincidencia numérica fuerte.** Con ECP 60131 a 1 de enero:
- 2025 = H(1-ene-2026) − H(1-ene-2025) = **241.013**. El BdE da 240.000.
- Media 2021-2024 = (19.521.046 − 18.539.223)/4 = **245.456**. El BdE da 245.000.
- Todo apunta a que el BdE usa la ECP de hogares del INE a 1 de enero. La EPA corregida da 258.200 en 2025.

**Terminadas: inferencia mía.**
- Según prensa, el boletín anual 2024 del Observatorio de Vivienda y Suelo (MIVAU) da **100.980** terminadas en 2024, libres y protegidas.
- 100.980 × 0,91 ≈ 91.900, que encaja con «92.000, −9 %».
- Nuestras libres de 2024 son 86.609, lo que implica unas 14.400 protegidas en 2024.
- La cifra de 100.980 **no está en `data/raw`**: viene de la búsqueda web y queda **pendiente de verificación** en la fuente primaria.

**Descomposición de la diferencia de 116.100 (866.100 − 750.000)**

| Componente | Nuestro | BdE (implícito) | Diferencia |
|---|---|---|---|
| Δhogares 2021-2025 | 1.278.000 (EPA corregida) | 1.222.836 (ECP a 1-ene) | **+55.164** |
| Terminadas 2021-2025 | 411.900 (libres) | ≈ 472.800 (= 1.222.836 − 750.000) | **+60.936** (≈12.000/año: protegidas y redondeo) |

- El 3,7 % de 19,76 millones de hogares (ECP a 1-ene-2026) daría unos 731.000. Por tanto «unas 750.000» lleva un redondeo de unas ±20.000.
- El **IEF de otoño de 2025 (700.000)** usa datos hasta el primer semestre de 2025: se trata de un periodo distinto.
- Conclusión: la diferencia **se explica por la fuente de hogares (mitad) y por la cobertura de las terminadas (mitad)**. No hace falta ajustar nada; basta con documentarlo. Esto sustituye al punto 2 de «Problemas abiertos».

## 4. Econometría de la elasticidad

**Estacionariedad y cointegración**
- Para la especificación principal (iniciadas, k=4), solo 1 de 3 contrastes rechaza: EG p=0,077; Johansen sí rechaza; ARDL F=3,77 en zona inconclusa.
- Con la regla pre-registrada (al menos 2 de 3) **no hay cointegración**. Entonces el DOLS en niveles **no es legítimo como estimador de un vector de cointegración**: sus estadísticos t no tienen la distribución supuesta (riesgo de regresión espuria).
- Lo confirma el ECM: la velocidad de ajuste de iniciadas k=4 no es significativa (p=0,21).
- Las especificaciones k=0 (3/3) y k=2 (2/3) sí cointegran. No se puede cambiar la principal a posteriori, pero sí presentarlas como robustez, y dan β = 2,05 y 1,81.
- Los contrastes de cointegración usan otra muestra que el DOLS: 2008Q1-2026Q2 con huecos interpolados, frente a 2009Q4-2025Q4. Además, Johansen se estima sin dummies estacionales. Está documentado; es un defecto menor.

**Autocorrelación**
- Los DOLS principales fallan BG(4): p=0,0009 en iniciadas. DW = 0,83 / 1,07 / 0,52.
- He comprobado que el EE de iniciadas k=4 apenas cambia con el ancho de banda HAC: 0,206 / 0,187 / 0,178 / 0,167 con 4 / 8 / 12 / 16 retardos. El problema no es el ancho de banda, sino que no hay cointegración.
- Comprobación mía en diferencias, válida sea cual sea el orden de integración:
  - especificación: OLS de Δ4 ln iniciadas sobre Δ4 P_l4, Δ4 costes reales y Δ4 tipo, HAC(8), 2010Q1-2025Q4, n=61;
  - resultado: **β = 1,39 (EE 0,63)**.
  - El IV en Δ4 da 1,06 (EE 0,89; n.s.).
  - **El orden de magnitud (>1) no es solo un artefacto de los niveles**, pero en diferencias la precisión es mucho menor.

**Quiebres**
- Chow rechaza la estabilidad en **todas** las fechas para iniciadas (2014, 2020 y 2022) y Bai-Perron encuentra 3 quiebres.
- Con residuos posiblemente I(1), el F de Chow tampoco tiene su distribución nominal. Aun así, la lectura correcta es que **no hay un parámetro estable que estimar en 2009-2025**: «largo plazo» con un solo ciclo y 63 trimestres.

**Misma muestra y EE HAC.** ✔ N=63 común en DOLS, OLS e IV en niveles; HAC(4) en todos.
- Detalle menor: los dos huecos (2016T2 y 2017T2) se eliminan y el HAC trata la serie como contigua.
- **Contradicción interna en `resumen_f4.md`**
  - Las razones (ii) y «reflejan sobre todo el co-movimiento del ciclo 2008-2025» atribuyen las elasticidades altas al colapso de 2008-2013.
  - Pero con 2014T1+ la elasticidad de iniciadas **sube**: DOLS 2,36, OLS 3,23, IV 3,47.
  - El argumento del colapso solo vale para las terminadas, que bajan de 4,26 a 2,86.
  - Hay que corregir el texto.
- **Etiqueta errónea:** «Rango de las 9 especificaciones DOLS (ipv, sin tendencia)». El rango 4,12-4,29 de terminadas incluye las de tendencia: son 18 especificaciones.

**Endogeneidad e instrumentos**
- Los instrumentos son ln ocupados, ln población extranjera y ln renta real, retardados. Usar desplazadores de demanda para identificar la curva de oferta es correcto *en principio*. Aquí la exclusión **no es creíble para dos de los tres**:
  - **ocupados** incluye el empleo de la construcción, que comove mecánicamente con las iniciadas;
  - **población extranjera** es oferta de mano de obra para la construcción, es decir, desplaza los costes y por tanto la oferta;
  - solo la **renta** es defendible.
- Problemas adicionales:
  - en niveles, los instrumentos tendenciales inflan la F de primera etapa;
  - el J tiene poca potencia con instrumentos de la misma familia y rechaza con tendencia;
  - el precio está retardado, pero con residuos autocorrelacionados no es predeterminado.
- El resumen ya lo dice («no se afirma elasticidad identificada»). Correcto.

**Búsqueda (119 modelos; 105 en la familia de elasticidad)**
- Composición de la familia: 39 DOLS, 36 IV, 18 OLS y 12 panel.
- Que 88 sobrevivan a Bonferroni con H0: β=0 **solo** significa que, *si los p-valores fueran válidos*, el signo positivo no se debe a haber probado muchos modelos. No lo son en los modelos en niveles sin cointegración: ahí los t crecen con la muestra. Y β=0 no es la hipótesis relevante.
- Lo informativo es esto:
  - **las 93 estimaciones nacionales están todas entre 1,04 y 6,66**;
  - con efectos de tiempo, el panel da entre −1,63 y 2,49.
- La corrección debería hacerse sobre H0: β=0,45 y acompañarse de la dispersión. Romano-Wolf no es necesario.

**Panel CCAA**
- Con efectos de tiempo, la asociación desaparece (L4, L8) o cambia de signo (iniciadas L4: −1,63, p_cluster=0,025, p_DK=0,013).
- La frase «la asociación positiva del agregado nacional procede del ciclo común, no de diferencias entre CCAA» **va más allá de lo estimado**:
  - con efectos de tiempo, la identificación sale de desviaciones regionales del precio, más ruidosas (sesgo de atenuación);
  - hay efectos derrame entre CCAA y Δ4 solapadas.
- Afirmación aceptable: «no hay evidencia de que las CCAA con mayor subida relativa de precios construyan relativamente más».
- Con 16-17 clústeres falta el **wild cluster bootstrap** (Webb, pre-registrado). Es necesario, sobre todo para el único coeficiente «significativo» (−1,63).

## 5. Signos y magnitudes frente a `docs/literatura.md`

**Signos**

| Coeficiente | Signo obtenido | Lectura |
|---|---|---|
| Precio | + en todas las nacionales | ✔ esperado |
| Costes reales en iniciadas y terminadas | − | ✔ |
| Costes reales en **permisos** | **+** (DOLS de +1,6 a +5,3) | ✘ **discrepancia no comentada**; debe marcarse |
| Tipo real en iniciadas | − | ✔ |

**Magnitudes frente al 0,45 del BdE**
- Nuestras elasticidades (1,4-4,3) multiplican el 0,45 por entre 3 y 10.
- Sobre el concepto:
  - el texto del BdE (p. 156) habla de «elasticidad de la oferta a largo plazo» estimada con «modelos macroeconómicos de largo plazo», entre países, como **cota superior**;
  - que sea la elasticidad de la *inversión residencial* es una inferencia de decisiones.md a partir del contexto («La inversión residencial en España aumenta en 2025…», misma página) y de las fuentes, que no están verificadas. Debe decirse así.
- Ayuda interpretativa que falta y conviene añadir (aritmética, sin estimar nada):
  - una elasticidad de **flujo** de 1,44 implica que un +10 % de precio real va con unas +17.500 iniciadas/año sobre 122.000;
  - eso es ≈0,07 % del parque (~26-27 millones de viviendas);
  - es decir, una elasticidad alta de flujo es compatible con una **oferta de stock muy inelástica**.
  - Tampoco se puede contrastar el 0,45 como estimación de la misma cosa.

## 6. Referencias

| Referencia | Comprobación |
|---|---|
| BdE IA 2025, p. 156 | Cita literal de `literatura.md` **verificada** en el PDF. Texto: «España presentaría una elasticidad de la oferta a largo plazo aproximadamente de 0,45 […] pueden considerarse una cota superior de la respuesta actual». Nota 39: «Caldera y Johansson (2013) y Cavalleri, Cournède y Özsöğüt (2019)». |
| BdE IA 2025, p. 157 | 750.000, 240.000, 92.000 y 3,7 % **verificados**. |
| Caldera y Johansson (2013); Cavalleri et al. (2019) | Figuran como **NO VERIFICADA** en `resumen_f4.md` (§3 y problemas abiertos), en la leyenda de `elasticidades_vs_bde.png` y en `literatura.md`. ✔ |
| IEF otoño 2025 (700.000) | No lo he verificado en esta revisión; ya consta en `literatura.md`. |
| Cifra de 100.980 terminadas en 2024 (OVS/MIVAU) | Solo prensa y búsqueda web: **NO VERIFICADA** en fuente primaria. Si se cita, con esa etiqueta. |

## 7. Qué puede afirmarse de P3 y con qué nivel de evidencia

1. **Déficit (contable; confianza alta en el signo y el orden de magnitud)**
   - De 2021 a 2025, la creación neta de hogares superó a las viviendas terminadas en unas **0,8-0,9 millones** con terminadas libres:
     - 810.936 con ECP alineada;
     - entre 866.100 y 919.825 con EPA corregida, según la ventana de corrección.
   - Añadiendo las protegidas (≈60.000), el resultado converge con los ~750.000 del BdE, que se reproduce con ECP a 1 de enero.
   - Es un flujo acumulado, no un déficit en niveles.
2. **Respuesta de la oferta (asociación descriptiva; evidencia débil)**
   - A escala nacional, las iniciadas libres co-varían positivamente y con elasticidad >1 con el precio real retardado en todas las especificaciones; en Δ4 da 1,39 (EE 0,63).
   - No hay cointegración robusta, el parámetro es inestable, no hay identificación creíble y el panel con efectos de tiempo no lo confirma.
   - **No puede afirmarse una elasticidad estructural.** Tampoco que el 0,45 del BdE sea erróneo: son conceptos distintos y su fuente primaria no está verificada.

## 8. Cambios requeridos (por prioridad; todos acotados)

1. **Variante ECP**
   - Corregir la alineación: stock a 1 del trimestre; Δ2021-2025 = H(2026T1) − H(2021T1).
   - Eliminar la imputación (b') y la frase de los «3 trimestres».
   - Recalcular (b): 810.936 y la extensión.
2. **Contraste con el BdE**
   - Sustituir «fuente no verificada» por la evidencia de §3: notas de los gráficos 2.10 y 2.11, la coincidencia 241.013/245.456 con ECP a 1 de enero y la descomposición +55.164 / +60.936.
   - Marcar como inferencia la identificación de las fuentes, y como NO VERIFICADA la cifra de 100.980.
   - Actualizar `comparacion_bde_deficit.*` y el punto 2 de problemas abiertos.
3. **Estatus del DOLS**
   - Declarar el DOLS principal como **descriptivo**: sin cointegración por la regla pre-registrada, los t no son válidos.
   - Añadir como robustez la regresión en Δ4 (OLS-HAC, misma muestra que el IV en Δ4) y los DOLS k=0/k=2 con cointegración.
   - Corregir la contradicción del colapso 2008-2013 (iniciadas sube con 2014+) y la etiqueta «9 especificaciones, sin tendencia».
4. **Panel**
   - Añadir el wild cluster bootstrap (Webb, 9.999, semilla 20261009) a las 12 especificaciones.
   - Reformular la conclusión del «ciclo común» (§4).
5. **Corrección por búsqueda**
   - Reinterpretar los «88 tras Bonferroni»: válido solo para el signo y condicional a p-valores válidos.
   - Añadir Holm/Bonferroni sobre H0: β=0,45 y el rango nacional de 1,04 a 6,66 como medida de sensibilidad.
6. **Otros cambios menores**
   - Documentar la interpretación de «4 trimestres adyacentes» y la sensibilidad 866.100 / 884.075 / 919.825.
   - Marcar el signo positivo de los costes en la ecuación de permisos.
   - Añadir la traducción de flujo a stock de la elasticidad (§5).
   - En el IV, señalar expresamente qué instrumento es defendible (la renta) y por qué fallan ocupados y población extranjera.

Ninguno de estos cambios exige descargar datos nuevos ni alterar la especificación principal pre-registrada.

---

## Re-revisión (iteración 2 de 2), 2026-10-09 — commit 9be1b66

**Veredicto final: APROBAR.**

**Cómo lo he verificado**
- Clon aislado del repositorio, con la red bloqueada.
- `make data clean` y luego dos ejecuciones de `src/f4_oferta.py`.
- Resultado: md5 de `output/f4/*` y de `registro_busqueda_f4.csv` **idénticos** entre las dos ejecuciones e idénticos a lo versionado (`git status` limpio).
- El registro tiene 128 modelos (114 en la familia de elasticidad).

**Cambios 1-5: aplicados correctamente**

| Cambio | Comprobación |
|---|---|
| 1. Variante ECP | Stock a 1 de enero: 1.222.836 hogares y déficit 810.936. La variante (b') ya no existe. |
| 2. Contraste con el BdE | Descomposición +55.164 / +60.936. La fuente del BdE está marcada como INFERENCIA y la cifra de 100.980 como NO VERIFICADA. |
| 3. Estatus del DOLS | Declarado descriptivo. Δ4: 1,39 (EE 0,63). La contradicción sobre 2014 está corregida. |
| 4. Panel | Wild cluster bootstrap (Webb) añadido. La frase del «ciclo común» está reformulada. Con 17 CCAA, terminadas L0 con efectos de tiempo da 2,42 (p WCB 0,020). |
| 5. Corrección por búsqueda | Bonferroni se lee solo para el signo. Holm sobre H0: β=0,45 en 15 especificaciones; el rango es 1,04-6,66. |

**Lectura nueva y relevante.** En diferencias (Δ4), que es la especificación válida sea cual sea el orden de integración, **no se rechaza β=0,45 para las iniciadas** (p Holm = 0,27; IV Δ4 p = 0,49). Esto debería figurar en las conclusiones de P3.

**Pendientes menores (para F7; no bloquean)**
- En `comparacion_bde_deficit` sigue la fila antigua «fuente no verificada (¿ECP?)».
- No se ha añadido ninguno de los cambios menores del punto 6 de la primera revisión:
  - presentar «inversión residencial» como una inferencia;
  - señalar el signo positivo de los costes en la ecuación de permisos;
  - incluir la traducción de flujo a stock;
  - indicar que la renta es el único instrumento defendible.

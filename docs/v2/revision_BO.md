# Revisión de la puerta · rama BO (oferta y suelo, H4)

Revisor independiente (opus) · 2026-10-10 · rama `r2/BO` en 3c8ffa1 (base r2/main 58e460b) · pre-registro: `docs/v2/hipotesis.md` en 910c42a · criterio uniforme: `docs/v2/decisiones.md` (r2/main). H4 no tiene evaluación sellada.

## Veredicto: **REHACER**

Hay un motivo bloqueante. La muestra de H4 no es la pre-registrada (2005-2023), y la rama justifica el cambio con una afirmación falsa sobre los datos. Los datos que permiten la especificación pre-registrada completa ya están en `data/raw` y cuadran exactamente con la serie mensual. Todo lo demás (reproducción, ausencia de fuga, presupuesto, comparaciones fuera de muestra y nivel EXPLORATORIO con la muestra actual) es correcto o necesita solo correcciones de texto.

---

## 1. Reproducción (clon aislado, sin red)

- Hice `git clone --no-hardlinks -b r2/BO` en el scratchpad. El clon no tiene `data/sealed`. Ejecuté con `HTTPS_PROXY=HTTP_PROXY=http://127.0.0.1:9` y `python3 src/v2/bo_run.py` dos veces.
- Las dos ejecuciones salen con exit 0 (≈10 s cada una). Los 15 ficheros csv/json de `output/v2/BO/` tienen **md5 idénticos entre ejecuciones y respecto a lo versionado** (`git status` limpio). Ejemplos: `resultado.json` 999dca0f…, `registro.csv` ab63c1d2…, `h4_principal.csv` e7527f3d…
- `make models` recoge `src/v2/bo_lib.py` (sin efectos al importarse) y `bo_run.py`. **OK.**

## 2. Fuga de información

- **Lecturas.** `bo_*.py` solo usa `vc.load` (→ `holdout.load_train`) para `panel_prov_a`, `panel_prov_q`, `nacional_q_v2`, `panel_ue_a` y `panel_ue_q`. No hay `read_csv`, ni `data/raw`, ni `data/sealed`. No modifica `holdout.py` ni `v2_common.py`. **OK.**
- **Log de accesos.** `docs/v2/holdout_accesos.md` solo contiene H1 (BA) y H2 (BV). BO no tiene ninguna apertura. **OK.**
- **Periodo.** El panel anual llega a 2023 (2024 en embargo). El trimestral y el nacional llegan a 2024Q2. El placebo de precio futuro se limita a t ≤ 2022 (adelanto ≤ 2023). En las proyecciones locales, los adelantos más allá de 2024Q2 son NaN. **OK.**
- **Suelo 2005-2007 y centrado.** Es la media de p_suelo anual 2005-2007 (se exigen los 3 años), en logaritmo, centrada con la media de las 47 provincias de entrenamiento que tienen dato (5,344). No usa ninguna información posterior a 2007 ni las provincias selladas (11, 16 y 45 no están en el panel). **OK.**
- **Fuera de muestra.** Bloques de 4 con embargo 4 = h y ventana expansiva (`v2_common.block_splits`). La muestra común es la intersección exacta con AR(4) y ECM v1. La rama avisa de que los regresores de t (MIVAU, valor tasado) se publican con retraso, así que es un pseudo-pronóstico. **OK.**

## 3. Fidelidad de H4 al pre-registro

| Elemento | Pre-registro | Código | Juicio |
|---|---|---|---|
| Muestra | panel anual **2005-2023** | 2009-2023 sin 2016-2018 (N = 550, 47 prov.) | **NO CONFORME (bloqueante, ver 3.1)** |
| Dependiente | Δ ln iniciadas | Δ ln iniciadas **libres** | Desviación no declarada (no hay iniciadas protegidas). Anotarla |
| Regresores | Δ ln precio real (t−1) e interacción con ln p_suelo 2005-2007 | `d_ln_pr_l1`, `d_ln_pr_l1 × suelo_c` | OK (el efecto principal del suelo queda absorbido por la FE de provincia) |
| FE / EE | provincia y año; cluster + wild bootstrap | FE prov. y año; CR1 t(G−1); WCR Webb, B = 9.999 | OK. He comprobado el WCR: restringido, FE parcializadas en Y*, t* con la misma corrección |
| Contraste conjunto | IUT (criterio a) | p_IUT = máx(0,022; 0,026) = 0,026 | OK |

### 3.1 El hueco 2016-2017 y el inicio en 2008 no son limitaciones de la fuente

- **Cómo se trató.** En el panel trimestral faltan **solo 2016Q2 y 2017Q2** (los meses 04-06 de 2016 y de 2017 no están en la tabla mensual 32100500). Son NaN, no ceros. El total anual exige 4 trimestres, así que 2016 y 2017 quedan como NaN. Como las filas de esos años existen en el panel, `groupby.diff()` da NaN en 2016, 2017 y 2018. **No se calcula ningún Δ ln a través del hueco.** El tratamiento mecánico es correcto.
- **Pero la justificación es falsa.** `desviaciones.md` §1 dice que «las iniciadas MIVAU empiezan en 2008» y que «la fuente no trae iniciadas en 2016 y 2017». `data/raw/mivau_v2_iniciadas_terminadas_prov.csv` contiene además la **tabla anual 32200500** (viviendas libres iniciadas, nivel provincia y ciudad autónoma, más CCAA para las uniprovinciales). Cubre **1991-2025** e **incluye 2016 y 2017** para las 43 provincias pluriprovinciales.
- **Validación (cuadre).** Para 2008-2015 y 2018-2025, la suma de los 12 meses de la tabla mensual coincide con la tabla anual en las 43 provincias: diferencia relativa **0,0 % exacta en todos los años**. Es la misma fuente oficial, ya validada, y por tanto válida para el modelo principal (no es OCR ni interpolación).
- **Consecuencia.** La especificación pre-registrada (2005-2023, sin huecos; unos 47 × 19 ≈ 890 observaciones antes de pérdidas por p_tasado) era estimable. Con la muestra actual se pierden el auge y el desplome (2005-2008) y 2016-2018, es decir, 7 de 19 años. Las submuestras quedan deformadas: S3 «2014-2023» solo tiene 7 años. Es precisamente el periodo que más puede mover un resultado frágil (β_precio = −1,81 en 2009-2013). No he estimado la especificación con la serie anual, para no contaminar la prueba confirmatoria: debe hacerla la rama, una vez.

### 3.2 Evidencia con la muestra actual (coherente)

- p_IUT = 0,026. Fallan las submuestras de la regla ex ante: S2 2009-2013 con β_precio = −1,81 y p_IUT 0,92. Las demás tienen p_IUT entre 0,08 y 0,31. R2 (t−2) da β_precio ≈ 0.
- **IV**: F de primera etapa 5,9 para el precio y J = 14,3 (p = 0,0008). Con un solo instrumento, F = 2,5 o 10,8 y no aparecen los signos. La rama reconoce que el F es un Wald cluster por endógeno, no el de Sanderson-Windmeijer ni el de Kleibergen-Paap.
- **Placebo de precio futuro**: 0,90 (p = 0,17), del mismo tamaño que el efecto.
- Con el criterio uniforme (c), el nivel **EXPLORATORIO** es correcto, y el lenguaje no es causal. Holm sobre las 7 hipótesis queda para BS, como corresponde.

## 4. Déficit (DESCRIPTIVO)

- Recalculado a partir de `deficit_nacional.csv`. **EPA corregida, 2021Q1-2024Q2**: 919.400 − 286.539 = **632.861** sin protegida y **598.157** con la protegida reescalada (34.704; cota inferior 599.697). **ECP, 2021Q1-2024Q1** (stock a día 1, ventana coherente con terminadas 2021Q1-2024Q1): **550.523 / 518.074**. La corrección de Δ2021Q1 replica la de v1. **OK.**
- **Extrapolación de ≈ 49.600.** Es 34.704 observado (2021Q1-2024Q2) más **14.873 supuesto** (6 trimestres × 2.479, de 2024Q3 a 2025Q4). El resumen sí la llama «ilustración aritmética… supuesto sin datos», pero da una sola cifra y no separa lo observado de lo supuesto. Además no aparece en `resultado.json` (solo en `resultados_internos.json`, como `ilustracion_2021_2025`). Las proporciones 43 % y 81 % comparan esa cifra mixta con residuos de v1 que se calcularon con datos de 2024Q3-2025Q4 (hoy periodo sellado; son cifras publicadas de v1, no una lectura de datos sellados). Debe decirse.
- **Error en el resumen (proxy provincial).** «Tarragona (43), Almería (04), Girona (17), Castellón (12), Ourense (19)»: el código **19 es Guadalajara**, no Ourense (32). Además, poner los códigos entre paréntesis se lee como si fuera el valor. Los valores reales están entre 12,5 y 9,5 por cada 1.000 habitantes.

## 5. Suelo, panel UE y fuera de muestra

- **Proyecciones locales.** Hay 160 contrastes registrados (2 variantes × 5 periodos × 8 horizontes × 2 direcciones). BH y Holm se aplican por variante, con m = 80. La variante «media4T» se añadió **después de ver** la cruda; está declarada y registrada. El único contraste con BH < 0,05 (media4T, P4, suelo→precio, h = 6, p = 1,3·10⁻⁴) también sobreviviría a Holm sobre las 160 (≈ 0,021). La lectura «el suelo no anticipa de forma robusta» es correcta. **OK**, pero la corrección debe hacerse sobre las 160, porque la segunda variante no es independiente de la decisión.
- **Panel UE, alquiler −6.** No es un error de datos ni de unidades. Los permisos de ES están en la misma escala que los de los demás países (FR, por ejemplo). Mi diagnóstico con la serie de ES (fuera del registro de la rama, solo como comprobación) es que el coeficiente lo generan dos episodios en los que el alquiler real del HICP y los permisos se mueven en sentidos opuestos:
  - 2008-2010: desplome de permisos con alquiler real al alza, por la deflación de 2009.
  - 2021-2023: alquiler real −2,4 % y −6,7 % por la inflación general, con permisos al alza. Las actualizaciones de renta estuvieron limitadas en 2022-2023 (tope del 2 % del RDL 6/2022 y sus prórrogas; **NO VERIFICADO** en esta revisión, hay que comprobarlo en el BOE).
  
  Si la serie empieza en 2012, sale −1,4 (n = 12). La explicación de la rama («la serie casi no varía») es incompleta.
- **Inferencia con España como un único clúster.** `p_dif` = 0,0004 (precio) y ≈ 0 (alquiler) usan un EE cluster en el que España es un solo clúster. Ese EE no es válido (MacKinnon y Webb, 2017: con un único clúster tratado, el CRVE subestima mucho). No basta con llamarlo «EE aproximado»: hay que retirar esos p o sustituirlos por inferencia de aleatorización o por rango (ES es 5.ª de 27, p ≈ 0,19). El panel UE trimestral usa `hicp_general` como «anual_asignado»: hay que declararlo.
- **Fuera de muestra.** Hay 6 configuraciones, dentro del presupuesto declarado (`Presupuesto` con n_max = 6 y la primaria P3 fijada en el registro antes de los resultados). Se comparan en la misma muestra que AR(4) y ECM v1, con DM-HLN de panel. La primaria P3 es peor que el AR(4): 0,0586 frente a 0,0394, p = 0,18. En iniciadas, AR(4) + precio da p = 0,032 (bilateral) y BH(6) = 0,097: no sobrevive, y el texto lo dice. No hay ECM v1 para iniciadas, y está declarado. **OK.** El comentario del código dice «p unilateral» pero `evaluar` devuelve un p bilateral: hay que corregir el comentario. Las 4 configuraciones de precio empeoran mucho con Δ4 ln iniciadas, que tiene colas grandes en provincias pequeñas y no está escalado. Conviene comentarlo; no es fuga.

## 6. Registro, especificaciones y lenguaje

- **Registro.** `registro.csv` tiene **249** filas: H4 12, SUELO 160, UE 62, OOS 13, DEFICIT 2. `bo_run` imprime 242 porque las 7 filas de `Presupuesto` no pasan por `LOG.n`. Cuadra con el código, y no encuentro ningún `fe_ols`/`fe_2sls` sin registrar. Hay que corregir la cifra donde se cite.
- **Lenguaje.** No hay lenguaje causal. Tres retoques:
  - Cambiar «elasticidad de iniciadas libres ~1» por «asociación (elasticidad estimada, no estructural)».
  - «10 % más caro → baja ~0,12»: con ln(1,1) = 0,095 sale ~0,11.
  - En `h4_principal`, la nota «PRE-REGISTRADA» describe una muestra que no es la pre-registrada.
- **Referencias.** BO no cita literatura, salvo las cifras del BdE (Informe Anual 2025, VERIFICADA en PDF según `docs/literatura.md`; sin cuartil porque no es revista). Si el resumen compara la elasticidad con BdE 0,45 o con Saiz (2010, QJE, Q1; VERIFICADA por DOI), debe indicar el estado y el cuartil.

## 7. Cambios exigidos (por prioridad)

1. **[Bloqueante] Muestra pre-registrada de H4.** El data-cleaner debe añadir a `panel_prov_a` la serie anual MIVAU 32200500: provincias, uniprovinciales desde el nivel CCAA, y Ceuta y Melilla. Se hace en `build_dataset_v2.py`, con nota de cuadre (0,0 % frente a la suma mensual 2008-2025), y después hay que pasar `holdout.py build` (2024 en embargo, 2025 sellado). Luego se estima **una sola vez** la principal de H4 con 2005-2023 (Δ desde 2005 con el nivel de 2004), con la misma especificación, el mismo bootstrap y la misma regla de submuestras S1-S5 (sin añadir submuestras nuevas). Por último hay que recalcular el nivel según el criterio uniforme. La estimación 2009-2023 actual se conserva como robustez registrada, etiquetada «vista antes».
2. Corregir `desviaciones.md` §1 (eliminar «la fuente no trae 2016-2017» y «empiezan en 2008»), así como `resultado.json` (`datos`, `iniciadas_desde`) y el resumen. Declarar la desviación «iniciadas libres en lugar de totales».
3. *(Opcional, OOS)* Recuperar 2016Q2 y 2017Q2 como anual − (Q1 + Q3 + Q4), etiquetado como «derivado». Si se hace, rehacer el OOS de iniciadas dentro del mismo presupuesto.
4. **UE:** retirar los p de la diferencia ES − resto con un único clúster, o sustituirlos por rango o permutación. Explicar el −6 del alquiler (los dos episodios; verificar el tope del 2 % en el BOE) y declarar el HICP «anual_asignado» del panel trimestral.
5. **Déficit:** separar en el resumen y en `resultado.json` lo observado (34.704, 2021Q1-2024Q2) de lo supuesto (14.873, 2024Q3-2025Q4, etiquetado SUPUESTO). Indicar que los residuos de v1 usan datos de 2024Q3-2025Q4. Corregir el código 19 → Guadalajara y dar los valores por cada 1.000 habitantes en lugar de los códigos.
6. **Suelo:** aplicar BH y Holm sobre los 160 contrastes (las dos variantes juntas) y dejar claro que «media4T» se añadió a posteriori.
7. **Textos menores:** número de filas del registro (249), comentario «p unilateral» en el OOS, ~0,11 en lugar de ~0,12, nota «PRE-REGISTRADA» y estado y cuartil de las referencias si se compara con BdE o Saiz.

Tras los puntos 1, 2, 4 y 5, una re-revisión acotada bastaría: reproducir, comprobar el nuevo panel y su cuadre, revisar la H4 única y su nivel y revisar los textos.

---

# Re-revisión (iteración 2 de 2) · r2/BO en a94ee9a (con r2/main 3b23781 fusionado)

## Veredicto final: **APROBAR**

**Reproducción.** He hecho un clon aislado nuevo de r2/BO (a94ee9a), sin `data/sealed` y con el proxy a 127.0.0.1:9. Lo ejecuté dos veces: exit 0 en ambas (~10 s). Los 15 ficheros csv/json tienen md5 idénticos entre ejecuciones y respecto a lo versionado (`git status` limpio). Ejemplos: `resultado.json` 1d179baf…, `registro.csv` 18ed87b8…, `h4_principal.csv` 27ee1331….

**Datos.** `iniciadas_libres_anual` (MIVAU 32200500) está en `panel_prov_a` de entrenamiento: 49 provincias, 2002-2023, sin huecos. El panel de entrenamiento termina en 2023 (2024 en embargo) y no contiene las provincias 11, 16 ni 45. He comprobado el cuadre con la suma mensual en las 658 observaciones donde coexisten: diferencia máxima 0,0. El build añade un `check` (Albacete 2019). Es una fuente oficial validada y es válida para el modelo principal. `bo_*.py` sigue leyendo solo con `vc.load`.

**H4 pre-registrada y única.**
- Muestra 2005-2023, 47 provincias, N = 879 (47 × 19 menos los huecos de p_tasado). La especificación, el bootstrap y la regla de submuestras no cambian: S2 y S4 conservan su definición en el código (≤2013 y ≤2019), y solo se renombran porque la muestra ahora empieza en 2005.
- `registro.csv` contiene una sola fila `H4_principal`. La estimación previa queda como `R0_vista_antes_2009-2023_mensual`. Entre 3c8ffa1 y a94ee9a no hay ningún commit intermedio con otra principal. Más allá del registro y del historial, no puedo verificar que no hubiera ejecuciones sin registrar.

**Resultados de H4.**
- β_precio = 0,79 (EE 0,34) y β_inter = −0,62 (EE 0,34). p unilaterales bootstrap: 0,011 y 0,046, así que p_IUT = 0,046.
- Falla la regla de submuestras: en S2 2005-2013, β_precio = −0,49; en S3 2014-2023, β_inter = +0,37.
- 2SLS: p_IUT = 0,25, F = 5,3 y J con p = 0,0003.
- El placebo de precio futuro es significativo: 1,27 (p = 0,012).
- Con el criterio uniforme (c) el nivel es **EXPLORATORIO**, que es coherente. El texto no usa lenguaje causal.
- Resto de cifras del texto: ≈ −0,06 con ln(1,1) es correcto; el registro tiene 250 filas.

**Demás puntos, todos corregidos:**
- Déficit: 34.704 OBSERVADAS frente a 14.873 SUPUESTAS, separadas en el resumen y en `resultado.json`.
- El código 19 es Guadalajara y ahora se dan los valores por cada 1.000 habitantes.
- Panel UE: ya no hay p ni EE de un único clúster; el HICP «anual_asignado» está declarado; el −6 se explica por los dos episodios.
- Suelo: BH y Holm sobre los 160 contrastes.
- El comentario «p bilateral» y la desviación 1b (iniciadas libres) están declarados.

**Pasa a `docs/v2/limitaciones.md` (BO):**
1. H4 es EXPLORATORIO. La asociación precio→iniciadas no es estable (negativa en 2005-2013; claramente positiva solo en 2014-2023). La interacción con el suelo cambia de signo en 2014-2023. El placebo de precio futuro significativo indica anticipación o endogeneidad. No hay instrumento válido (F < 10 en el precio; J rechaza).
2. Iniciadas libres, no totales (no hay iniciadas protegidas comparables por provincia). Protegida = calificaciones definitivas, como aproximación a terminadas.
3. Déficit 2021Q1-2024Q2 (EPA 632.861 / 598.157; ECP 550.523 / 518.074). No es comparable con el BdE (2021-2025). Los ≈ 49.600 de protegida incluyen 14.873 SUPUESTAS. Los residuos de v1 usan datos de 2024Q3-2025Q4. El déficit provincial es un proxy, con el tamaño medio del hogar nacional.
4. El p_suelo trimestral es muy ruidoso. La señal suelo→precio (P4, h = 6, variante «media4T» añadida a posteriori) es aislada.
5. Panel UE: España es un único clúster y no hay inferencia válida de la diferencia ES − resto. El −6 del alquiler está dominado por 2008-2010 y 2021-2023. El tope del 2 % a la actualización de rentas (RDL 6/2022) está NO VERIFICADO aquí. Series cortas.
6. OOS: las variables de oferta no mejoran al AR(4) en precio. En iniciadas, la mejora (p = 0,03) no sobrevive a BH (0,097) ni hay ECM v1 con el que comparar. El OOS de iniciadas sigue usando la suma trimestral (sin 2016Q2 ni 2017Q2). Es un pseudo-pronóstico con retraso de publicación.

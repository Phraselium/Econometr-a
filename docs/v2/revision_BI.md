# Revisión de la puerta · rama BI (inmigración, H3)

Revisor independiente (opus) · 2026-10-10 · rama `r2/BI` en 84fed09 (fusión de r2/main 28fad4e) · pre-registro: `docs/v2/hipotesis.md` en 910c42a (sin cambios posteriores) · criterio uniforme de evidencia: `docs/v2/decisiones.md` de r2/main (d014dee).

## Veredicto: **REHACER** (acotado: identificación, etiquetas de evidencia y lenguaje; no hay fuga ni problema de reproducción)

H3 tal como se registró (conjunción β_alq > 0 y β_alq > β_compra) queda en **EXPLORATORIO**. Además el contraste no solo es débil: **cambia de signo** con elecciones razonables y no fijadas en el pre-registro. El componente β_alq > 0 **no es CAUSAL**. Dictamen: **ASOCIACIÓN ROBUSTA en el signo, no en la magnitud**, como componente secundario: no es una hipótesis pre-registrada por separado. La rama lo declara «CAUSAL (regla mecánica)». Esa regla se la ha inventado la rama, omite los placebos que exige la escala y no resiste los placebos ni los controles de GPSS que he ejecutado (sección 4).

---

## 1. Reproducción (clon aislado, sin red)

- Hice un `git clone --no-local` de r2/BI en el scratchpad. El clon no tiene `data/sealed`. Ejecuté con `HTTPS_PROXY=HTTP_PROXY=http://127.0.0.1:9` y `python3 src/v2/bi_run.py` dos veces.
- Las dos ejecuciones salen con exit 0 (92 s y 94 s). Los **26 ficheros de `output/v2/BI/` tienen md5 idénticos** entre las dos ejecuciones **y respecto a lo versionado** (p. ej. `resultado.json` ec12f0b9…, `registro.csv` 8884d79d…).
- `make models` recoge `src/v2/bi_*.py`. Solo `bi_run.py` tiene `__main__`; los demás son no-op al importarse. **OK.**

## 2. Fuga de información

- **Lecturas de datos.** La rama solo carga datos mediante `vc.load` (→ `holdout.load_train`): `panel_prov_a`, `nacional_q_v2` y `panel_prov_q` (este último para el ECM v1). No hay `read_csv`, `data/raw` ni `data/sealed` en `src/v2/bi_*.py`. La rama no modifica `holdout.py` ni `v2_common.py` (diff contra la base de fusión). **OK.**
- **Provincias selladas.** 11, 16 y 45 no aparecen en el panel. Las cuotas 2002 se calculan sobre las 49 de entrenamiento, y el shock nacional y su leave-one-out son `Σ_{49} ΔS − ΔS_i`, es decir, **49 provincias, no el total nacional publicado**. Dictamen: es la opción conservadora y es correcta. Usar el total nacional publicado (52) también sería **aceptable** para H3, porque H3 no tiene evaluación sellada y el agregado nacional ya entra en entrenamiento en otras series. Pero la opción de la rama evita cualquier discusión y debe mantenerse.
- **Años.** El panel llega hasta 2023 (2024 en embargo). El instrumento alineado usa S(1-ene-2022) para t = 2021, que es entrenamiento. No hay información ≥ 2024. **OK.**
- **Muestra sellada.** H3 no tiene evaluación sellada. BI no llama a `holdout.evaluate`. No existe `docs/v2/holdout_accesos.md` (no ha habido ninguna evaluación). Por diseño, no tengo permiso de lectura sobre `data/sealed/_accesos.log`. **OK.**
- **CV/OOS.** Bloques expansivos con embargo de 1 año y h = 1. El entrenamiento exige `pos+h ≤ último`, así que no hay solapamiento de objetivos. Las FE de provincia se estiman solo en entrenamiento. El DML y el causal forest usan pliegues por bloques de provincias. Matiz menor: en «AR4+flujo_t (observado)», el flujo del año t se publica a mitad de t+1. Es un pseudo-pronóstico con una pequeña anticipación de publicación y debe decirse.

## 3. Fidelidad al pre-registro (H3)

| Elemento | Pre-registro | Código | Juicio |
|---|---|---|---|
| Panel | provincial anual 2009-2021 | 621 obs. = 49 × 13, 2009-2021 | OK |
| x_it | «flujo/población t−1» | `100·inmig_flujo_t / pob(1-ene t−1)` | Lectura literal admisible, pero **ambigua**. «Flujos 2008-2021» en la tabla también admite flujo_{t−1}, que da β_alq = 0,80 (p = 0,16). Hay que documentarlo en decisiones.md como interpretación |
| Cuotas 2002 | sí | stocks por nacionalidad a 1-ene-2002, 8 grupos | OK |
| Leave-one-out | implícito (shift-share) | sí, sobre 49 provincias | OK |
| Momento del shock | **no fijado** | principal: ΔS_t = S(1-ene t) − S(1-ene t−1), es decir, la variación del año **t−1** frente al flujo del año t (desalineado) | Grado de libertad no pre-registrado del que depende el signo del contraste (sección 4) |
| Resultados | Δ ln IPC alquiler, Δ ln p_tasado | IPC alquiler en media anual; p_tasado **deflactado** (real) | La deflación no figura en el pre-registro. Con FE de año es inocua para β (el deflactor es nacional), pero hay que anotarlo |
| FE, EE | provincia y año; cluster provincia | sí; CR1 + WCB WRE Webb B = 9999; conjunto AR | OK |
| Sistema apilado / contraste | β_alq − β_compra | covarianza entre ecuaciones cluster = regresión de la diferencia (EE 2,2019 idéntico) | OK |
| Conjunción | IUT (criterio uniforme a) | p_IUT = máx(0,001; 0,0294) = 0,0294 | OK |

## 4. Identificación (criterio GPSS / BHJ / AKM) y comprobaciones propias del revisor

Las comprobaciones son mías, con `bi_core.construir_panel` sin modificar, la misma muestra (N = 621) y EE cluster provincia. No están en la rama.

| Especificación | F | β_alq (EE, p) | β_compra (EE, p) | β_alq − β_compra (p) |
|---|---|---|---|---|
| Principal (rama) | 14,4 | 3,06 (0,95; 0,002) | −1,04 (2,51; 0,68) | **+4,10** (0,069) |
| + extranjeros 2002 × año (GPSS) | 15,0 | 1,95 (1,21; **0,115**) | 8,70 (4,34; 0,051) | **−6,75** (0,115) |
| + ln pob 2002 × año | 9,0 | 3,17 (0,019) | −2,19 | +5,36 (0,045) |
| + ln p 2002 × año | 9,9 | 3,11 (0,005) | −0,97 | +4,08 (0,094) |
| + paro 2002 × año | 13,1 | 3,70 (0,001) | −0,33 | +4,03 (0,157) |
| + las cuatro (y costa) × año | **4,3** | 4,99 (3,60; 0,17) | 10,27 | **−5,27** (0,56) |
| Instrumento solo Sudamérica (68 % del peso de Rotemberg) | 52,5 | 2,45 (0,63; <0,001) | **2,98 (1,34; 0,031)** | **−0,53** (0,68) |
| Instrumento sin Sudamérica | **1,7** | 4,34 (0,11) | −9,50 | +13,84 (0,08) |
| Instrumento alineado ΔS_{t+1} (rama, robustez) | 29,9 | 2,37 (0,59; <0,001) | **4,46 (1,64; 0,009)** | **−2,09** (0,175) |
| Sin Madrid y Barcelona | 11,6 | 3,13 (0,006) | −1,55 | +4,68 (0,060) |
| Sin 28, 08, 46, 03 | 9,3 | 3,41 (0,006) | −0,28 | +3,69 (0,126) |
| Submuestra 2009-2014 | **0,7** | sin información | — | — |
| Submuestra 2015-2021 | 7,6 | 2,50 (1,36; 0,073) | −1,80 | +4,29 (0,139) |
| **Placebo: y_alq(t−1) sobre x_t instrumentado** | 14,4 | **4,11 (1,15; 0,001)** | — | — |
| **Placebo: y_alq(t−2) sobre x_t instrumentado** | 8,5 | **4,00 (0,85; <0,001)** | — | — |
| Pretendencia 2003-07 con el instrumento Sudamérica (por DE) | — | −0,17 (0,105; p = 0,106) | 0,20 (p = 0,50) | — |

Lectura:

1. **Exogeneidad de las cuotas (GPSS).** La identificación descansa en las cuotas 2002 de Sudamérica (α = 0,68; F_g = 52). Esas cuotas correlacionan con ln población 2002 (r = 0,61; p < 0,001), ln precio 2002 (r = 0,43; p = 0,002) y extranjeros 2002 (r = 0,36). El instrumento medio correlaciona con extranjeros 2002 (r = 0,56), paro (−0,34) y población (−0,40). Es decir, el instrumento señala provincias grandes, caras y con enclave previo, que en 2015-2021 tuvieron su propio ciclo de alquiler. Con el control estándar de GPSS (características de las cuotas × año), β_alq pierde significación al controlar por extranjeros 2002, y con el conjunto completo el F cae a 4,3. **La exogeneidad de las cuotas no es creíble sin estos controles, y la rama no los estima.**
2. **Placebos.** La escala pre-registrada exige placebos para CAUSAL y la rama no ejecuta ninguno. El placebo natural (resultados pasados sobre x_t instrumentado) **rechaza con fuerza**: los coeficientes son del mismo tamaño que el principal. Con shocks persistentes (autocorrelación media de z intra-provincia 0,70; el shock de Sudamérica es negativo en 2010-2016 y positivo en 2018-2021) esto puede reflejar en parte efectos de flujos pasados. Es justamente el problema de Jaeger, Ruist y Stuhler (2018): el diseño no separa el efecto del flujo de t de ajustes acumulados ni de tendencias provinciales. Ese trabajo no figura en docs/literatura.md: si se cita, hay que verificarlo. En cualquier caso, β no puede leerse como «efecto del flujo del año t».
3. **Pretendencias.** La prueba de la rama regresa los resultados de 2003-2007 sobre el instrumento medio 2009-2021. Ese periodo **no es pre-tratamiento**: fueron los años de mayor entrada de inmigrantes a los mismos enclaves. Su «p = 0,93» no es informativa. Con el instrumento dominante (Sudamérica), el alquiler da p = 0,11.
4. **Sobreidentificación.** El J robusto no rechaza (p = 0,29 / 0,12), pero el Sargan rechaza en precio (p = 6e-6) y los β_g de Rotemberg del precio van de −36 a +37. Los grupos distintos de Sudamérica tienen F_g < 2 (África, Europa) o entre 5 y 10. La regla de la rama usa solo el J, el más indulgente de los dos.
5. **BHJ/AKM con 8 grupos.** Las inferencias t(7) tienen poca potencia y validez asintótica dudosa. La rama lo dice correctamente. No aportan evidencia a favor de la exogeneidad de los shocks: 8 shocks no son «muchos shocks cuasi-aleatorios».
6. **Naturaleza del shock.** ΔS es la variación del stock de **nacionales** del grupo. Para Sudamérica en 2010-2015 incluye nacionalizaciones masivas (no emigración), y el regresor x es el flujo **bruto** de entradas. Hay que discutirlo: el shock no mide entradas.
7. **Momento.** El principal usa la variación del stock del año t−1 frente al flujo del año t. La versión alineada tiene un F el doble de alto (29,9) y **da la vuelta al contraste** (−2,09). El pre-registro no fija esta elección. Si la versión desalineada se eligió tras ver resultados, eso no puede auditarse: la rama tiene un único commit.

**Magnitud.** 3,06 % de alquiler por cada 1 p.p. de población. Es unas 3 veces Saiz (2007, ≈1 %; VERIFICADA, JUE Q1), 3 veces el MCO (0,96) y 7 veces la v1 (0,44 con 17 CCAA, no significativa). Además, x es un flujo **bruto** y el de Saiz es un aumento neto de población inmigrante. Por inmigrante neto, la magnitud implícita sería aún mayor. Un IV 3 veces mayor que el MCO, con un F moderado y cuotas no balanceadas, es una señal de alarma, no un «LATE». El rango de estimaciones razonables (0,8-5,0) indica que **la magnitud no está identificada**. El signo positivo sí es estable: todas las variantes de la rama y mías dan β_alq > 0, y el MCO también.

**Dictamen de evidencia** (criterio uniforme c):
- **H3 (conjunción): EXPLORATORIO.** p_IUT = 0,029 (una cola). El IC95 del contraste incluye 0, la cota Holm-7 es 0,21 y el signo del contraste se invierte con el instrumento alineado, con el instrumento de Sudamérica y con los controles GPSS. En la práctica: **no hay evidencia de que la inmigración eleve más el alquiler que la compra.**
- **β_alq > 0 (componente, no pre-registrado por separado): ASOCIACIÓN ROBUSTA en el signo.** Sobrevive a la cota Holm-7 (0,007) y es positivo y significativo sin COVID, sin Madrid/Barcelona y con 3 de los 4 controles GPSS. En 2015-2021, p bilateral = 0,07. **No CAUSAL**: falla el placebo, el balance de cuotas y la robustez al control por extranjeros 2002, y el F con tendencias es 5,4.
- **β_compra:** no informativo (IC [−6; 4] y signo inestable).

## 5. Especificaciones, presupuesto y Holm

- `registro.csv` tiene 49 especificaciones más la fila de presupuesto, y concuerda con el código. Todas las estimaciones de `bi_h3.py`, `bi_het.py` y `bi_oos.py` se registran. No se registran como especificaciones: (a) los 16 β_g de Rotemberg (8 IV justamente identificados × 2 resultados), que solo están en los CSV; (b) el conjunto AR; (c) los CATE del bosque por terciles y la Spearman (6 características, incluida `vut20_pm`, que es de 2020 y por tanto posterior). Son diagnósticos y descriptivos, pero conviene una línea en el registro por cada familia. La ejecución de humo está aparte en `smoke_registro.csv`. Con un solo commit no puede auditarse lo que se probó y se descartó durante el desarrollo.
- **Presupuesto DML/causal forest.** Declarado 14, usados 10 (4 DML, 1 CausalForestDML y 5 interacciones IV). Los hiperparámetros son fijos (lasso α = 0,02; RF 300 árboles, hoja 10, max_features 0,5; bosque 500 árboles), sin búsqueda, y el presupuesto se declara en el código antes de usarse. **Dentro del presupuesto.** Holm interno sobre las 5 interacciones IV aplicado correctamente. PLR/PLIV sin FE de provincia y causal forest sin instrumento: ambos están bien etiquetados como EXPLORATORIOS.
- **Holm sobre las 7.** Implementación de Holm correcta. Para el rango k, el p de Holm cumple (8−k)·p ≤ p_Holm ≤ 7·p, así que 7p es una cota pesimista válida. La afirmación de que el contraste solo sobrevive si las otras seis rechazan es correcta. Pero **la unidad de la familia es H3 (p_IUT = 0,0294), no cada componente.** Aplicar Holm-7 a β_alq por separado y asignarle un nivel es tratar un componente como una hipótesis confirmatoria más, cosa que el pre-registro no hace. Además, `holm_2_componentes` en `resultado.json` sobra con IUT (la IUT no necesita corrección interna) y confunde. Según el criterio (d), la corrección final la hace el orquestador.

## 6. Fuera de muestra

- AR(4) de panel anual frente a AR(4) + flujo observado en t: **misma muestra** (392 obs., 8 orígenes, intersección exacta vía `vc.evaluar`) y DM-HLN con t(n−1) sobre la media transversal por periodo. RMSE 0,0094 frente a 0,0107, DM 1,43, p = 0,20: no mejora. Con 8 periodos la potencia es mínima. **Correcto.**
- El ECM v1 solo se compara en trimestral (orígenes T4, h = 4), así que **no es la misma muestra** que la comparación anual. La rama lo declara. Hay que hacer un análogo anual del ECM v1 sobre la misma muestra, o anotar en decisiones.md por qué no es posible.
- La variante con flujo t+1 está bien etiquetada como «NO es pronóstico».

## 7. Datos y referencias

- Todas las series son oficiales y observadas: ECP 1 de enero, EM semestral sumado, IPC alquiler en media anual y valor tasado MIVAU (CCAA = provincia en las uniprovinciales). No hay interpolaciones ni datos de PDF/OCR en el modelo principal. **OK.**
- `COSTA` está fijado en el código sin fuente y **omite Lugo (27)**, que tiene litoral. Afecta a una característica de heterogeneidad y a la correlación con costa. Hay que corregirlo y citar la fuente.
- Referencias usadas: GPSS 2020, BHJ 2022, AKM 2019 y Saiz 2007 están VERIFICADAS con cuartil (Q1) en docs/literatura.md. **No figuran** en docs/literatura.md: Andrews, Stock y Sun (2019) (citado en el código para el F efectivo), Roodman et al. (2019) (WCB) y Jaeger, Ruist y Stuhler (2018) (si se añade). Hay que añadirlas como VERIFICADA/NO VERIFICADA con cuartil o retirarlas.

## 8. Lenguaje (resumen.md)

Es incompatible con el dictamen:
- «beta_alq>0 → CAUSAL (regla mecánica)» y `"nivel": "CAUSAL"` en `resultado.json` → ASOCIACIÓN ROBUSTA (signo).
- «Debe leerse como efecto local (LATE) de la variación inducida por enclaves 2002» → eliminar: LATE presupone validez del instrumento.
- «El efecto sobre el alquiler es positivo en todas las variantes», «efecto mayor donde…», «el diseño estima el efecto reducido-forma» → «coeficiente/asociación».
- «Con 49 provincias … el efecto sobre el alquiler es más grande y significativo» → «el coeficiente es mayor; la diferencia con v1 y con MCO no está explicada».

## Cambios requeridos (por prioridad)

1. **[Bloqueante] Retirar la etiqueta CAUSAL** de β_alq en `bi_h3.py` (regla `base and wcb_ok and holm7`), `resultado.json` y `resumen.md`. La regla debe incluir placebos y balance de cuotas, como exige la escala pre-registrada. Niveles: H3 = EXPLORATORIO; β_alq > 0 = ASOCIACIÓN ROBUSTA (signo, componente no pre-registrado por separado); β_compra = no informativo.
2. **[Bloqueante] Añadir los diagnósticos de identificación que faltan** (EXPLORATORIOS y registrados), con WCB: (a) controles de GPSS, características 2002 × año (por separado y conjuntos); (b) placebo de resultados retardados (y_{t−1}, y_{t−2}) sobre x_t instrumentado; (c) pretendencias y balance **por grupo dominante** (Sudamérica) y estimación con el instrumento de Sudamérica solo y sin Sudamérica; (d) submuestras 2009-2014 y 2015-2021. Hay que informarlos en el resumen aunque sean desfavorables (lo son).
3. **[Bloqueante] Momento del instrumento y de x.** Documentar en decisiones.md, como desviación o interpretación, por qué el principal usa ΔS_t (variación del año t−1) y no ΔS_{t+1}, y la lectura de «flujo/población t−1». Mostrar el contraste con ambas versiones en la tabla principal y declarar que su signo se invierte.
4. **[Alto] Reescribir la sección de pretendencias.** La prueba de 2003-2007 no es pre-tratamiento (fueron los años del boom de entradas a los mismos enclaves). Declararla no informativa.
5. **[Alto] Lenguaje** según la sección 8: «asociación/coeficiente», sin LATE y sin «efecto». Discutir la magnitud: 3× MCO, 3× Saiz (flujo bruto frente a neto), 7× v1; magnitud no identificada (rango 0,8-5).
6. **[Medio] Discutir el shock**: variación del stock de nacionales, con nacionalizaciones de sudamericanos en 2010-2015, frente a x = flujo bruto.
7. **[Medio] Holm.** Quitar `holm_2_componentes` o explicar que con IUT no procede. La unidad de la familia de 7 es H3 con p_IUT = 0,0294. Las cotas por componente son informativas, no confirmatorias.
8. **[Medio] Fuera de muestra.** ECM v1 en la misma muestra anual (o justificación en decisiones.md). Advertir del retraso de publicación del flujo de t.
9. **[Bajo]** Corregir `COSTA` (añadir 27 Lugo) y citar la fuente. Registrar los β_g de Rotemberg y los CATE descriptivos como familias en `registro.csv`. Añadir Andrews-Stock-Sun 2019, Roodman et al. 2019 y Jaeger-Ruist-Stuhler 2018 a la literatura con su estado y cuartil.

Nada de lo anterior exige tocar la muestra sellada: H3 no la tiene.

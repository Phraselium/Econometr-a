# Revisión independiente: FASE 5 (panel CCAA, P4)

Fecha: 2026-10-09 · Revisor: reviewer (opus), puerta de F5 · Commit revisado: `759ab15` (árbol de trabajo con `src/build_dataset.py` modificado por F6, solo unidades del diccionario).

## Veredicto: **REHACER** (acotado)

El código es correcto en lo esencial: el FE se replica exactamente, el CCE está bien implementado y la ejecución es reproducible salvo una línea. Aun así hay **dos problemas que cambian la especificación principal** y, con ellos, la lectura de P4:

1. La exclusión de Extremadura se debe a un error de construcción de datos, no a un hueco de la fuente.
2. El coeficiente de la cuota extranjera (b2 ≈ 0) depende de cómo se alinea en el tiempo, y esa decisión no se ha documentado.

A esto se suman lecturas incorrectas de dos contrastes (CD y poolability) que el resumen presenta como evidencia. Los cambios son concretos y no exigen rediseñar la fase.

---

## 1. Reproducibilidad

- Ejecuté `make all` en una copia aislada del repositorio (scratchpad), sin red (proxy anulado y `FORCE` sin definir). Terminó con **exit 0** en 5 min 12 s: data → clean → F2…F6. `report` aún no existe, y está avisado.
- Comparé dos ejecuciones de `src/f5_panel.py` sobre los mismos `data/processed`. **Coinciden los md5 de los 32 ficheros de `output/f5/` (PNG incluido) y de `registro_busqueda_f5.csv`, salvo `resumen_f5.md`**. La única diferencia está en la línea 3, que incluye el tiempo de ejecución («31 s», «42 s», «32 s»). También coinciden con lo ya subido al repositorio, salvo esa línea.
- `panel_ccaa_a.csv` regenerado es idéntico a HEAD (md5 `e04d4db2…`).
- **Cambio C6**: sacar el tiempo de ejecución de `resumen_f5.md` (que vaya solo a stdout).

## 2. Datos

### 2.1 Contraste de cifras con data/raw (5 de 5 correctas)

| Cifra (panel_ccaa_a) | raw | panel |
|---|---|---|
| IPV C. Valenciana 2020 (media de 4 trimestres, base 2025; INE 80270) | 69,785 | 69,785 |
| Ocupados Madrid 2018 (media EPA, miles; 65302) | 2.990,9 | 2.990,9 |
| Terminadas Madrid 2019 (suma de 12 meses; MIVAU 32101000) | 18.174 | 18.174 |
| Población extranjera Cataluña, 1-1-2015 (77019) | 925.539 | 925.539 |
| Población total Illes Balears, 1-1-2020 (77019) | 1.176.816 | 1.176.816 |

Además, recalculé Δln IPV desde los niveles: la diferencia máxima con `d_ln_ipv` es de 1e-15. No hay cifras inventadas.

### 2.2 Extremadura: no falta en la fuente; se pierde al procesar (PRIORIDAD 1)

El resumen, `docs/diccionario_variables.md` (l. 193 y 200) y `revision_f1.md` dicen que «MIVAU 32101000 no tiene Extremadura en el Boletín». **Es falso.** En `data/raw/mivau_fin_obra.csv` la CCAA aparece como `territorio = "Extremadura (1)"`, con `nivel = provincia` y serie `viv_libres_terminadas_provincia_extremadura_1`: 222 meses, de 2008-01 a 2026-06. La llamada «(1)» de nota al pie en el XLS (fila 57) hace que el parser no la reconozca como CCAA.

Tiene validación de cuadre exacta:

- Badajoz + Cáceres coincide con esa serie en todos los años.
- Nacional − Σ(16 CCAA + Ceuta + Melilla) coincide con esa serie en todos los años, de 2008 a 2025. Por ejemplo, 2019: 1.325 y 2025: 1.337.

Por tanto:

- **No hay sesgo de selección en sentido estricto.** La pérdida es administrativa (un error de parseo) y no depende del precio. Pero se pierde una unidad sin necesidad y la documentación afirma algo falso.
- He re-estimado el FE principal con Extremadura (17 CCAA, 2009-2025, N=289): b2 = 0,0011 (EE 0,0041; p wild 0,79), b1 = −0,028, b4 = 0,0026. **Las conclusiones cualitativas no cambian**, pero el modelo principal debe ser el de 17 CCAA, como se fijó en `decisiones.md`.
- El robusto actual de «17 CCAA sin terminadas» no es comparable con el principal: cambia a la vez la muestra temporal (2008-2025 frente a 2009-2025) y el conjunto de regresores. Con la corrección deja de hacer falta.
- Desconozco qué significa la nota «(1)» (no está en el XLS descargado). Hay que documentarlo como nota de fuente no resuelta.

### 2.3 Alineación temporal de la cuota extranjera (PRIORIDAD 1)

La población es el stock a 1 de enero del año t (`fecha` = t-01-01, comprobado). Por tanto, `d_share_extr_t` = cuota(1-1-t) − cuota(1-1-(t−1)) mide la **entrada neta ocurrida durante el año t−1**. El IPV, en cambio, es la media del año t.

El resumen solo dice «desfase de timing». En la práctica, b2 está **retardado un año** sin que se haya decidido ni registrado así. Mis re-estimaciones, todas con FE bidireccional, EE cluster y wild bootstrap Webb con B=999:

| Especificación | N | b2 (Δln IPV por pp) | EE | p cluster | p wild |
|---|---|---|---|---|---|
| Principal F5 (flujo del año t−1), 16 CCAA | 272 | −0,0006 | 0,0040 | 0,87 | 0,86 |
| Igual, recortado a 2009-2024 | 256 | −0,0014 | 0,0046 | 0,76 | 0,75 |
| Cuota a mitad de año (media de 1-1-t y 1-1-t+1), 16 CCAA | 256 | 0,0083 | 0,0054 | 0,13 | 0,12 |
| Cuota a mitad de año, 17 CCAA (con terminadas de Extremadura) | 272 | 0,0118 | 0,0058 | 0,041 | 0,065 |
| Flujo del año t (adelanto), 16 CCAA | 256 | 0,0152 | 0,0060 | 0,012 | 0,019 |

Lectura:

- La afirmación «b2 ≈ 0 en FE» **no es robusta a la alineación temporal**. Con el flujo contemporáneo, b2 vale unos 1,5 % por pp, con p ≈ 0,01-0,02.
- Ninguna de estas variantes sobreviviría a Holm en una familia de más de 20 contrastes.
- El flujo contemporáneo es además el más expuesto a causalidad inversa (precio → llegadas en el mismo año).
- F3 ya encontró signos opuestos entre x_t y x_{t−1} (`output/f3/resumen_f3.md`, filas «FE, x_t y x_t-1»), lo que confirma que el timing es de primer orden.

### 2.4 Población solo en anual o en Δ4

Se cumple. En trimestral, la población solo entra en Δ4 (Q2, Q3) y como denominador de terminadas (Q3), con la advertencia de interpolación. La muestra se recorta a 2025Q1. Correcto.

## 3. Econometría

### 3.1 Re-estimación del FE principal

Con `statsmodels` (dummies de CCAA y de año, variables reconstruidas desde niveles) obtengo b1 = 0,05214, b2 = −0,000644, b3 = 1,5094 y b4 = 0,003386. Son **idénticos** a la tabla 1a. Los EE cluster difieren un 3 % (0,0798 frente a 0,0774 en b1) solo por la corrección de grados de libertad (G/(G−1)·(n−1)/(n−k) en statsmodels; solo G/(G−1) en linearmodels). La implementación numpy está validada con un `assert`.

Además, **el R² within ajustado es −0,016** (registro). Los cuatro regresores no explican nada de las desviaciones regionales respecto del ciclo común. El resumen debe decirlo.

### 3.2 Estacionariedad y CIPS

- La implementación de CIPS es correcta: regresión CADF con ȳ_{t−1}, Δȳ_t y retardos de Δy y Δȳ; truncado K1 = 6,19 y K2 = 2,61 (Pesaran 2007, caso con constante). La simulación usa raíz unitaria con un factor común y cargas U(0,1). Como la distribución del CIPS no depende asintóticamente de las cargas, el DGP es adecuado. Con 1.000 réplicas, los valores críticos al 5 % (≈ −2,18 a −2,27) son plausibles para N=16 y T=17-18. No los he contrastado cifra a cifra con las tablas del artículo. **Son fiables como referencia orientativa**; el límite real es la potencia con T=17.
- **Hallazgo no discutido en el resumen**: CIPS **no rechaza** la raíz unitaria en la **primera diferencia** de la cuota extranjera (p = 0,74 y 0,79) ni de ln población española (p = 0,37 y 0,46). Tampoco en Δln IPV con 1 retardo (p = 0,26).
  - Puede ser falta de potencia, pero también olas migratorias muy persistentes. Si Δshare es casi I(1), la regresión de un y I(0) sobre ella está desequilibrada: b2 tiende a cero y la inferencia no es estándar.
  - No es una regresión espuria (y no es I(1)), pero debe constar como limitación de b2 y b3.
- `term_pc` en niveles rechaza la raíz unitaria, así que entrar en niveles está bien.

### 3.3 Endogeneidad

- Empleo y cuota extranjera son contemporáneos y no hay instrumento. Se remite a F3 para la causalidad y la fase se etiqueta como «asociación». Esto es correcto.
- **b4 (terminadas por 1.000 hab., t−1) es positivo y el único significativo** (p wild 0,021). La literatura (`docs/literatura.md`, tabla de signos: «Oferta (licencias, terminadas): − sobre precio») predice signo negativo. El resumen **no comenta esta discrepancia**.
  - Es casi seguro simultaneidad o momentum: las terminadas de t−1 responden a precios pasados.
  - Al añadir Δln IPV_{t−1} (coeficiente 0,42, EE 0,08; sesgo de Nickell de orden 1/T), b4 baja a 0,0014 (EE 0,0008). En CCE pasa a ser negativo y no significativo.
  - Debe decirse explícitamente que **b4 no es un efecto de oferta**.

### 3.4 Autocorrelación (DW 1,39; AR(1) residual 0,33)

- Los EE cluster por CCAA y el wild cluster bootstrap son **robustos a cualquier correlación serial dentro de cada CCAA**, así que la autocorrelación no los invalida. El problema de esos EE es el número de clusters, no la autocorrelación. Driscoll-Kraay con bw 2-3 la recoge parcialmente, pero con T=17 es poco fiable, como ya se reconoce.
- El ρ residual de 0,33 está sesgado a la baja por la demeaning (≈ −1/(T−1) = −0,06), así que el ρ real ronda 0,4. Eso indica una **dinámica omitida** (inercia de precios), que contamina sobre todo a b4.
- Robustez sugerida: el modelo con y_{t−1}. Mis resultados: b2 = −0,005 (EE 0,004), b1 = 0,03 (EE 0,07).

### 3.5 Dependencia transversal: el CD está mal interpretado

- Los residuos de un FE con efectos de año tienen por construcción una correlación media ≈ −1/(N−1) = −0,067. La observada es −0,055 en FE y −0,049 en CCE-P. **El CD negativo «significativo» es un artefacto de los parámetros incidentales**, no dependencia remanente.
- Juodis y Reese (2022) demuestran que el CD no es N(0,1) sobre residuos de FE bidireccional ni de CCE, y proponen un CD ponderado (CDw). Por la misma razón, que CCE-MG «pase» el CD no valida el CCE.
- Indicio de dependencia remanente heterogénea: el |ρ| medio (0,31-0,35) supera lo esperable bajo independencia con T=17, que es √(2/(πT)) ≈ 0,20. El CD no lo detecta porque las correlaciones se compensan en signo.
- **Cambio C3**: reescribir 3a y el resumen. O bien se calcula el CDw de Juodis-Reese (implementación corta), o bien se declara que el CD sobre esos residuos no es interpretable.

### 3.6 Implementación de CCE-MG y CCE-P (revisión del código)

- Los promedios transversales de y y de las 4 X entran junto con la constante (`Zc = [1, ȳ, x̄]`). Hay cargas propias por unidad, tanto en MG (regresión por unidad) como en P (M̄ común aplicada a cada unidad). Es correcto según Pesaran (2006).
- La varianza de MG es no paramétrica: Σ(b_i − b_MG)(b_i − b_MG)'/(N(N−1)). Correcto.
- La varianza de CCE-P sigue la forma no paramétrica de Pesaran (2006) con pesos iguales: Ψ*⁻¹ R* Ψ*⁻¹ / N, con R* construido con X'M̄X/T. Correcto.
- Quedan 7 grados de libertad por unidad. Las estimaciones individuales son muy imprecisas, como ya se advierte.
- Las p de MG y P usan la normal. Con N=16 sería más prudente una t(N−1). Es un cambio menor que no altera las conclusiones (CCE-P b2: p pasaría de 0,052 a ≈ 0,07).

### 3.7 Errores estándar con 16-17 clusters

Usar el wild bootstrap Webb como referencia es correcto (Webb 2023). Pero **en las interacciones con una sola CCAA tratada el wild cluster bootstrap tampoco es válido**: MacKinnon y Webb (2018) muestran que, con muy pocos clusters tratados, tanto el CRVE como el wild bootstrap son poco fiables. Que los p_wild se agrupen en 0,33-0,55 para casi todas las regiones es síntoma de esa degeneración, no evidencia de homogeneidad.

### 3.8 Poolability (F = 2,69; p < 0,001) frente a interacciones no significativas

**No es una contradicción. Es un F clásico sobredimensionado frente a una inferencia sin potencia.**

- El F de poolability supone errores iid. Con heterocedasticidad entre CCAA y ρ ≈ 0,4, su tamaño se dispara. Lo mismo ocurre con el F conjunto de las 12 interacciones: p clásico 1e-6, pero p wild 0,08.
- Calculé un wild bootstrap restringido (Webb, B=999) del F de poolability: **p = 0,36**. Es orientativo, porque cada pendiente individual depende de un solo cluster.
- Inferencia por aleatorización (placebo: asignar la interacción a cada una de las 16 CCAA e interactuar una variable cada vez):

| Interacción con C. Valenciana | coef | p RI |
|---|---|---|
| empleo | −0,040 | 0,94 |
| cuota extranjera | −0,005 | 0,75 |

  Ninguna región alcanza p < 0,0625, que es el **mínimo alcanzable con 16 unidades** (1/16). Cataluña-empleo es la más extrema, con p = 0,0625.
- Conclusión: **no hay evidencia robusta de heterogeneidad de pendientes, ni tampoco evidencia de homogeneidad.** Con N=16 y T=17, el diseño no puede detectar diferencias por región al 5 %.
- **Cambio C4**: corregir el resumen, que hoy presenta la poolability (p = 2,6e-7) como evidencia de heterogeneidad. Añadir el p wild del F de poolability y la RI (dos bucles cortos).

### 3.9 Sobreajuste y corrección por búsqueda

- Hay 21 especificaciones registradas. Holm y Bonferroni se aplican a 19 p-valores de b2, y nada sobrevive. Correcto.
- Defectos:
  - Faltan en la familia los b2 trimestrales: Q2, b2 = 0,012 con p cluster 0,010 (DK 0,18); Q3, p = 0,063. Se registran con `coef_interes = NaN`.
  - Se mezclan hipótesis distintas: `H_F_wild` es la heterogeneidad conjunta, no b2; `H_conjunto` es el b2 de las 10 CCAA de referencia.
  - Hay que registrar las variantes de timing (C2) y añadirlas a la familia.

### 3.10 Misma muestra

La comparación 1d (FE, FE+tendencias, CCE-MG, CCE-P) usa la misma muestra: correcto. La tabla 1f mezcla muestras, cosa que está declarada, pero el robusto de 17 CCAA no es comparable (ver 2.2).

## 4. Signos y magnitudes frente a `docs/literatura.md`

| Coeficiente | F5 | Literatura / fases previas | Valoración |
|---|---|---|---|
| b2 cuota extranjera, FE | −0,06 % por pp (Δln×100) | Saiz (2007): entrada = 1 % de la población → ≈ +1 % en precios y alquileres. González y Ortega (2013): flujo del 17 % → precios +52 % (cociente implícito ≈ 3 % por pp, cálculo del revisor) | **DISCREPANCIA** de magnitud (≈ 0 frente a +1-3 %). Depende del timing (§2.3): con flujo contemporáneo, +1,5 %/pp, dentro del rango |
| b2, CCE-MG / CCE-P | +2,5 % / +2,0 % por pp | ídem | Signo y orden de magnitud coherentes con la literatura; no significativo tras la corrección |
| b2 frente a F3 | FE −0,06 %/pp | F3 OLS FE IPV: −0,45 %/pp (p 0,38); 2SLS −1,6 (p 0,15) | Coherentes (≈ 0, no significativos). Hay que expresar F5 en %/pp para que la comparación sea directa |
| b1 empleo, FE | 0,05 (p 0,50) | F2 LP DOLS 1,95, rango 0,84-2,67 y no robusto según F2 | Estimandos distintos: F2 es la elasticidad de largo plazo en niveles nacionales (incluye shocks comunes); F5 usa desviaciones regionales anuales respecto del ciclo común (los efectos de año absorben lo nacional), con atenuación probable por error muestral de la EPA regional en diferencias. Con valor tasado, b1 = 0,18-0,22 (p < 0,01): **b1 ≈ 0 no es robusto a la medida de precio.** Debe decirse |
| b4 terminadas (t−1) | + (p wild 0,02) | − (Saiz 2010; Hilber y Vermeulen 2016; BdE) | **DISCREPANCIA de signo** (simultaneidad o momentum, §3.3) |
| b3 Δln pob. española | 1,5 (p 0,07-0,15) | + (población → demanda) | Signo coherente; impreciso |

## 5. Referencias

Las referencias metodológicas que usa F5 **no figuraban en `docs/literatura.md`** (solo Pesaran 2006). Las he verificado en la web:

- Pesaran (2006), *Econometrica* 74(4), 967-1012: ya en literatura.md, verificada.
- Pesaran (2004), «General diagnostic tests for cross section dependence in panels», CESifo WP 1229 / IZA DP 1240; publicado en *Empirical Economics* 60, 13-50 (2021). VERIFICADA (IZA, CESifo).
- Pesaran (2007), «A simple panel unit root test in the presence of cross-section dependence», *Journal of Applied Econometrics* 22(2), 265-312. VERIFICADA (registros bibliográficos; no comprobé el DOI).
- Pesaran (2015), «Testing weak cross-sectional dependence in large panels», *Econometric Reviews* 34(6-10), 1089-1117. VERIFICADA (IDEAS).
- Driscoll y Kraay (1998), *Review of Economics and Statistics* 80(4), 549-560, DOI 10.1162/003465398557825. VERIFICADA (IDEAS).
- Webb (2023), «Reworking wild bootstrap-based inference for clustered errors», *Canadian Journal of Economics* 56(3), 839-858, DOI 10.1111/caje.12661 (WP Queen's 1315, 2014). VERIFICADA.
- Holm (1979), *Scandinavian Journal of Statistics* 6(2), 65-70. VERIFICADA (JSTOR 4615733 según la búsqueda).
- Citadas por el revisor: Juodis y Reese (2022), *Journal of Business & Economic Statistics* 40(3), 1191-1203, DOI 10.1080/07350015.2021.1906687, VERIFICADA; MacKinnon y Webb (2018), «The wild bootstrap for few (treated) clusters», *Econometrics Journal* 21(2), 114-135, DOI 10.1111/ectj.12107, VERIFICADA.
- NO VERIFICADA: el significado de la nota «(1)» de Extremadura en MIVAU 32101000.

**Cambio C7**: añadir estas referencias a `docs/literatura.md` (sección de métodos).

## 6. Qué puede afirmarse de P4 y con qué evidencia

1. **Diferencias entre CCAA en las pendientes (empleo y cuota extranjera)**: *no detectadas*.
   - Ni las interacciones (wild, Holm, RI), ni el F con inferencia robusta (p wild 0,08 y 0,36), ni el CCE por unidad dan evidencia robusta.
   - Tampoco puede afirmarse homogeneidad: la potencia es mínima (RI con p mínimo de 1/16; CCE individual con 7 gl).
   - Nivel: **ausencia de evidencia, no evidencia de ausencia.**
2. **Asociación media**: ni el empleo ni la cuota extranjera muestran una asociación distinguible de cero con el crecimiento relativo del IPV regional en la especificación actual.
   - b2 es sensible a la alineación temporal: entre ≈ 0 y ≈ +1,5 %/pp.
   - b1 es sensible a la medida de precio: IPV ≈ 0, valor tasado ≈ 0,2.
   - Nivel: **asociación condicional, frágil**. Sin lectura causal (remite a F3).
3. **C. Valenciana**:
   - Ninguna interacción es distinguible del resto (p wild 0,48-0,73; RI 0,75-0,94).
   - Su b2 individual en CCE (0,049, EE 0,016, 7 gl) es un valor aislado entre 64 coeficientes individuales y no sobrevive a la multiplicidad.
   - Lo único sólido es **descriptivo**, y depende de la medida de precio:
     - 2014Q1-2026Q2: con el IPV, la CV crece 14 pp menos que España; con el valor tasado, 12 pp más.
     - 2021Q1-2026Q2: la CV crece más que España con ambas medidas (+2,8 y +13,6 pp).
   - Nivel: **descriptivo**.

## 7. Cambios requeridos (priorizados, acotados)

1. **C1. Recuperar Extremadura** en `build_dataset.py`: mapear `"Extremadura (1)"` (nivel provincia en el raw) a la CCAA, con el cuadre «nacional − Σ CCAA = Extremadura = Badajoz + Cáceres» como `assert`. Corregir el diccionario (l. 193 y 200) y anotar el hallazgo en `decisiones.md`. Re-estimar F5 con **17 CCAA** como principal; el robusto de 17 CCAA sin terminadas deja de ser necesario. Avisar a F4 si usa terminadas del panel.
2. **C2. Alineación temporal de b2**:
   - Declarar en `decisiones.md` que la principal usa el flujo de t−1 (o pasar a la cuota a mitad de año, más coherente con el IPV medio anual) y justificarlo.
   - Reportar las dos alternativas (mitad de año y flujo de t) como robustez registrada, incluida en la familia Holm.
   - Reescribir el resumen: «b2 ≈ 0» → «b2 entre ≈ 0 y +1,5 %/pp según la alineación; ninguna sobrevive a la corrección por búsqueda».
3. **C3. CD**: retirar la lectura «CD rechaza en FE y CCE-P; CCE-MG la pasa». Calcular el CDw de Juodis-Reese (2022) o declarar el CD no interpretable sobre residuos de FE bidireccional y CCE. Mencionar el |ρ| medio frente a ≈ 0,20 esperado.
4. **C4. Heterogeneidad**:
   - Añadir el p wild del F de poolability y la inferencia por aleatorización (placebo por CCAA) para las interacciones de la CV y de las otras 5 regiones.
   - Advertir que el wild bootstrap con un solo cluster tratado no es fiable (MacKinnon y Webb 2018) y que el p mínimo de la RI es 1/16.
   - Reescribir la respuesta a P4 según §6.
5. **C5. Signos y magnitudes en el resumen**:
   - Comentar b4 > 0 como discrepancia con la literatura (no es efecto de oferta) y añadir la robustez con y_{t−1}.
   - Expresar b2 en %/pp y compararlo con Saiz (2007), González-Ortega (2013) y F3.
   - Reconciliar b1 con F2 (estimandos distintos) y señalar que b1 ≈ 0 no se mantiene con valor tasado.
   - Discutir que CIPS no rechaza en Δshare ni en Δln pob. española, y el R² within ajustado negativo.
6. **C6. Reproducibilidad**: quitar el tiempo de ejecución de `resumen_f5.md`.
7. **C7. Referencias**: añadir a `docs/literatura.md` las de §5. Familia Holm: incluir los b2 trimestrales y separar `H_F_wild` (otra hipótesis). Usar t(N−1) para MG y P (menor).

No hacen falta otros cambios. El CCE, el wild bootstrap Webb, el registro de búsqueda, el panel trimestral con Δ4 y la etiqueta de «asociación» están bien resueltos.

## Anexo: comprobaciones del revisor

Scripts en el scratchpad de la sesión (no forman parte del repositorio): `fe_check.py` (re-estimación con statsmodels, AR(1) de residuos, modelo con y_{t−1}), `fe_alt.py` (timing y 17 CCAA con terminadas de Extremadura desde el raw, wild Webb B=999) y `ri.py` (aleatorización por CCAA y wild bootstrap del F de poolability, B=999). Los resultados se transcriben en las tablas de arriba.

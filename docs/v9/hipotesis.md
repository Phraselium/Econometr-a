# Pre-registro V9 COMPLETO (F2) — hipótesis, especificaciones, pruebas y criterios por capa

Fecha: 2026-10-15. Escrito **antes de estimar ningún efecto** de los diseños D1-D7.

La potencia se calculó solo con placebos entre unidades nunca tratadas y con permutaciones de la exposición, nunca con la relación tratamiento-resultado de las unidades tratadas: src/v9/f2_potencia.py → output/v9/potencia/mde.csv.

El commit de este documento lleva la etiqueta local `prereg-v9`. Su hash figura al final (sección «Sellado»).

Reglas comunes:
- SEED = 20261010; B = 999 réplicas en todos los bootstrap salvo que se indique otra cosa.
- Filas con `posterior_prereg` (periodo desde 2026-07-01) excluidas.
- Cruces solo por código INE.
- Cada especificación estimada, principal o alternativa, se anota en el Registry (output/v9/registry.csv); ninguna se elige por su p-valor.
- Se publican todas las especificaciones de este documento, incluidas las que no salgan significativas.

## Capas, familias y ajuste

- **Confirmatoria.** Una hipótesis es confirmatoria solo si su MDE con Holm (80 % de potencia) es menor o igual que la magnitud de referencia de la literatura (tabla de potencia). Las demás se estiman como exploratorias.
- **Familias de Holm** (α = 0,05): las hipótesis confirmatorias de cada diseño.
  - D1: H1a-renta, H1a-contratos, H1b-renta.
  - D2: H2-covid-renta, H2-reapertura-renta.
  - D4: H4-réplica-alquiler.
- **Exploratorias.** Una única familia de Benjamini-Hochberg (q = 0,10) con todas las exploratorias de V9.
- **Criterio de capa.**
  - **C3**: hipótesis confirmatoria con p de Holm < 0,05 que además supera todas las pruebas exigidas de su diseño (abajo).
  - **C3s**: solo D5, si fuera confirmatorio (identificación del shock por restricciones de signo de Jarociński y Karadi). No lo es: ver potencia.
  - **C4** en cualquier otro caso: exploratoria, o confirmatoria que falla alguna prueba o no supera Holm. Se informa como «asociación» o «no detectado», con su intervalo.
  - Nada sube de capa por robustez.
  - Sin lenguaje causal por debajo de C3/C3s.
- **Bandas.** Toda atribución (F4) se da con bandas y como C2: efecto × exposición, con la advertencia de equilibrio general.

## Potencia y MDE (output/v9/potencia/mde.csv)

| Diseño | Resultado | N | MDE (α = 0,05) | MDE Holm | Referencia | ¿Confirmatorio? |
|---|---|---|---|---|---|---|
| D1a zonas tensionadas Cataluña | log renta media de contratos nuevos | 234 municipios (208 tratados) | 0,031 | 0,037 | 0,05 (LB01) | **sí** |
| D1a | log contratos nuevos | 397 (264 tratados) | 0,075 | 0,090 | 0,10 | **sí** |
| D1b Ley 11/2020 | log renta media | 241 (60 tratados) | 0,021 | 0,025 | 0,05 (LB01: −4 % a −6 %) | **sí** |
| D1b | log contratos | 416 (60 tratados) | 0,089 | 0,106 | 0,10 | no |
| D1c zonas tensionadas Euskadi (EMAL) | renta y contratos | 20 municipios (11 tratados con ≤ 5 trimestres posteriores; ≤ 9 controles) | — | — | — | no (sin potencia por construcción) |
| D2 HUT × COVID, 2020-2021 | log renta media por 1 DE de dosis | 428 | 0,0073 | 0,0087 | 0,019 (LA01) | **sí** |
| D2 HUT × reapertura, 2022-2025 | log renta media por 1 DE de dosis | 428 | 0,0083 | 0,0099 | 0,019 | **sí** |
| D2 (los dos periodos) | log contratos por 1 DE de dosis | 644 | 0,029-0,037 | 0,035-0,044 | 0,019 | no |
| D3 caída del registro VUT por CP | Δ log fianza media 2024→2026 | 179 CP | 0,020 | 0,022 | 0,019 | no → **descriptivo** |
| D3 | Δ log número de fianzas | 179 CP | 0,051 | 0,057 | 0,019 | no → **descriptivo** |
| D4 réplica 2003-2012 (forma reducida) | Δ log valor tasado por punto de Z | 43 provincias | 0,012 | 0,015 | 0,01 (LA09) | no |
| D4 réplica 2003-2012 | Δ log IPC de alquiler por punto de Z | 50 | 0,0062 | 0,0074 | 0,01 | **sí** |
| D4 ampliación 2015-2022 | Δ log valor tasado / Δ log IPC alquiler | 49 / 50 | 0,064 / 0,013 | 0,076 / 0,016 | 0,01 | no |
| D5 proyecciones locales, h = 4 y 8 | Δ log precio (BIS) por shock × 1 DE de exposición | 18 países | 0,107 / 0,139 | 0,117 / 0,152 | 0,05 (orden de magnitud, NO VERIFICADA) | no |

Tres consecuencias del cuadro:
- D3, D5 y las variantes sin potencia se estiman como **exploratorias (C4)**. D3 se presenta como **descriptivo**.
- D6 no se estima (ver D6).
- D7 es contable: no tiene contraste.

## D1 · Zonas tensionadas y topes (Cataluña y Euskadi)

**Pregunta.** ¿Cambian la renta de los contratos nuevos y el número de contratos en los municipios donde se aplica la contención de rentas, frente a los que no?

### D1a · Zonas tensionadas de Cataluña (Ley 12/2023; índice de referencia)
- **Datos.** Incasòl (fianzas), municipio × trimestre, 2022T2-2026T1. Panel equilibrado con resultado positivo en los 16 trimestres.
- **Tratamiento.** Primer trimestre de efecto según la resolución del BOE, en dos cohortes:
  - 140 municipios con efecto el 2024-03-16 → 2024T2;
  - 131 municipios con efecto el 2024-10-10 → 2024T4.
- **Control.** Municipios nunca tratados (fuera de las zonas tensionadas y de la Ley 11/2020).
- **Resultados principales.** log de la renta media de los contratos nuevos (H1a-renta) y log del número de contratos nuevos (H1a-contratos).
- **Especificación principal.**
  - Callaway y Sant'Anna con nunca tratados, sin covariables, ATT agregado ponderado por tamaño de cohorte.
  - Error estándar por conglomerados de municipio.
  - p del bootstrap salvaje por conglomerados (Rademacher, 999).
- **Alternativas** (todas se publican):
  - imputación de Borusyak, Jaravel y Spiess (BJS);
  - de Chaisemartin y D'Haultfœuille (dCDH), como robustez;
  - controles «aún no tratados»;
  - ventana que termina en 2025T4 (sin la Ley catalana 11/2025 de temporada);
  - ponderación por contratos;
  - sin Barcelona;
  - IPVA municipal anual (contratos nuevos, INE) como resultado de robustez.
- **Pruebas exigidas para C3.**
  1. Pretendencias: contraste conjunto de los ATT(e) con e ∈ [−8, −2]; se exige p > 0,10.
  2. Honest DiD (Rambachan y Roth), magnitudes relativas: el IC del ATT medio posterior con M̄ = 1 excluye el 0. Se informan también M̄ = 0,5 y el M̄ de ruptura.
  3. Placebo de fecha: falso tratamiento 4 trimestres antes en la muestra previa; se exige p > 0,10.
  4. Placebo de territorio: p de permutación del ATT real frente a 500 asignaciones aleatorias entre nunca tratados.
- **Heterogeneidad** (exploratoria): tamaño (población de 2022 por encima o por debajo de la mediana de los tratados) y cohorte.
- **Comparación.** Jofre-Monseny, Martínez-Mazza y Segú (2023, LB01) y Fedea (Pinto 2026, LB03, descriptivo).

### D1b · Ley catalana 11/2020 (topes de renta, 61 municipios)
- **Datos.** Incasòl trimestral, 2019T1-2022T1.
- **Tratamiento.** Desde 2020T4 (vigencia: 2020-09-22).
- **Fin del tratamiento.**
  - Principal: la publicación de la STC 37/2022 (2022-04-08), es decir, hasta 2022T1.
  - Alternativa: 2021T3. Es la fecha de fin registrada en data/raw/v3; las dos fechas discrepan y se informan ambas.
- **Control.** Municipios catalanes no sujetos a la Ley 11/2020.
- **Resultados.** H1b-renta (confirmatoria) y contratos (exploratoria).
- **Estimadores.** Los de D1a; con cohorte única, CS y BJS equivalen a un DiD con estudio de eventos e ∈ [−7, +5].
- **Pruebas.**
  - Las de D1a.
  - Además, robustez sin 2020T2-2020T3 (confinamiento).
  - Especificación anual 2014-2021: 2020 se excluye y 2021 es el año tratado; da 6 años de pretendencias.
- **Comparación.** LB01: entre −4 % y −6 % en la renta media pagada y sin caída de la oferta.

### D1c · Zonas tensionadas de Euskadi (EMAL)
- **Datos.** 20 municipios de más de 20.000 habitantes, 2016T1-2025T4.
- **Cohortes.** Escalonadas, de 2025T1 a 2026T3 (solo cuentan las tratadas antes de 2026T1).
- **Estado.** Exploratorio (C4): CS con «aún no tratados» y bootstrap salvaje.
- **Sin potencia.** Pocos trimestres posteriores (≤ 5) y ≤ 9 controles. Se publica el estudio de eventos sin inferencia confirmatoria.

## D2 · Pisos turísticos y shock COVID (Cataluña)

**Pregunta.** ¿Se movieron la renta y los contratos nuevos más en los municipios con más viviendas de uso turístico antes de 2020, cuando el COVID cortó la demanda turística (2020-2021) y cuando se reabrió (2022-2025)?

- **Datos.** Incasòl anual 2014-2025, municipio, panel equilibrado.
- **Dosis.** Plazas en HUT por cada 100 habitantes en 2019 (IDESCAT, a 31 de diciembre; padrón de 2019), estandarizada.
- **Especificación principal.**
  - y_it = a_i + g_t + Σ_{k≠2019} β_k (dosis_i × 1[t = k]) + controles de política + ε.
  - Controles de política: Ley 11/2020 × 2021 y zona tensionada × 2024-2025.
  - Parámetros: media de β en 2020-2021 (H2-covid-renta) y en 2022-2025 (H2-reapertura-renta).
- **Inferencia.** Error estándar por conglomerados de municipio; p del bootstrap salvaje.
- **Resultados.**
  - log renta media: confirmatorio.
  - log contratos: exploratorio.
- **Pruebas exigidas para C3.**
  1. Pretendencias: β_2014…β_2018 conjuntamente nulos (p > 0,10).
  2. Placebo de fecha: falso shock en 2017 con la muestra 2012-2019 (p > 0,10).
  3. Placebo de permutación de la dosis (500).
  4. Robustez sin los 61 municipios de la Ley 11/2020 y sin Barcelona.
- **Robustez** (todas se publican):
  - trimestral 2019T1-2023T4 (solo 4 trimestres previos);
  - dosis en viviendas HUT por cada 100 viviendas;
  - dosis por quintiles (figura dosis-respuesta).
- **Barcelona por barrios.** Aproximación por año de expediente; solo descriptiva, porque Incasòl no tiene resultado por barrio.
- **Signo esperado.**
  - COVID: β < 0, porque las HUT pasan al alquiler residencial.
  - Reapertura: reversión.
- **Comparación.** LA01 (Barcelona, +1,9 % el barrio medio) y LA02 a LA03.

## D3 · València 2025-2026: caída del registro de viviendas turísticas (descriptivo)

**Pregunta.** ¿Se asocia la caída de viviendas turísticas registradas por código postal entre 2025-01-26 y 2026-10-14 con la variación de la fianza media y del número de fianzas?

- **Unidad y muestra.** Códigos postales de la Comunitat Valenciana con al menos 20 fianzas en 2024 y en 2026. València ciudad, como heterogeneidad.
- **Exposición.** ΔVUT por cada 100 viviendas (registro de la GVA; viviendas del censo 2021 por sección, repartidas por CP con el callejero de 2025).
  - Alternativa: Δ de viviendas turísticas del INE por sección, asignadas al CP.
- **Resultados.**
  - Δ log de la fianza media 2024→2026 (con fianzas como aproximación de la renta mensual);
  - Δ log del número de fianzas.
- **Controles.**
  - ADRH, renta neta por persona de 2022 (sección → CP);
  - log de población y de viviendas (censo 2021);
  - distancia al centro de València (km, centroide del CP);
  - indicador de València ciudad.
- **Inferencia.** Errores de Conley con corte en 5 y en 10 km.
- **Placebo.** La misma regresión con el resultado 2021→2023.
- **Capa.** C4, descriptivo: el MDE (0,022) supera la referencia (0,019). Sin lenguaje causal.

## D4 · Inmigración (réplica de Sanchis-Guarner 2023 y ampliación)

**Pregunta.** ¿Cuánto suben los precios de la vivienda y los alquileres de una provincia cuando su población crece por inmigración predicha por las redes de origen?

### Diseño
- **Unidad.** Provincias peninsulares e insulares; se excluyen Ceuta y Melilla.
- **Endógena.** Δ de la población extranjera / población inicial × 100 (padrón por nacionalidad).
- **Instrumento** (shift-share de Card).
  - Z_p = Σ_c s_pc,t0 × ΔF_c,−p / Pop_p,t0 × 100.
  - Cuotas iniciales del padrón (26 países individuales de «principales nacionalidades»).
  - Crecimiento nacional por país excluyendo la propia provincia (leave-one-out).
  - Cuotas incompletas: se controla por la suma de cuotas (Borusyak, Hull y Jaravel).
- **Ventanas.**
  - Réplica: 2003→2012. La serie por país empieza en 2003 (no en 2001) y ese es el primer año disponible.
  - Ampliación: 2015→2022, último año del padrón por país. 2022-2025 solo como robustez, con los 22 grupos del censo anual.
- **Variantes de la ampliación** (exploratorias): instrumento con un solo país de origen (Venezuela, Colombia, Ucrania).

### Resultados
- **Confirmatoria (H4-réplica-alquiler).** Δ log del IPC de alquiler provincial 2003→2012.
- **Exploratorias.**
  - Δ log del valor tasado (MIVAU; 43 provincias con dato completo; las CCAA uniprovinciales toman el valor de la CCAA). Robustez con 50 provincias, interpolando 2012 con la media de 2011 y 2013; marcada.
  - Ampliación municipal: IPVA 2015→2022 con cuotas municipales.

### Especificación principal
- 2SLS: Δ log P_p = α + β ΔF_p/Pop_p + controles + ε, con instrumento Z_p.
- Controles: log de la población inicial y suma de cuotas.
- Se informan también:
  - la forma reducida;
  - la primera etapa con Δ de la población total (efecto total);
  - el desplazamiento de nativos: saldo interprovincial de los españoles 2008-2012 (EM 24385) / población sobre Z.

### Efecto parcial y total
- **Parcial** (por inmigrante): forma reducida / primera etapa de la población extranjera.
- **Total** (por habitante): forma reducida / primera etapa de la población total.
- **Brecha.** La diferencia entre ambos mide el ajuste vía migración interna. Solo se mide en 2008-2021, porque la EVR anterior a 2008 no está disponible.

### Diagnósticos exigidos para C3
1. F efectiva de Montiel Olea y Pflueger ≥ 23,1 (τ = 10 %). Si es menor, solo se interpreta el IC de Anderson-Rubin y la hipótesis no puede pasar de C4.
2. IC de Anderson-Rubin que excluye el 0.
3. Errores AKM (Adão, Kolesár y Morales) para shift-share.
4. Pesos de Rotemberg (GPSS): los cinco países de mayor peso, con contraste de pretendencia de sus cuotas sobre Δ log P 2002→2003.
5. Diagnóstico BHJ: número efectivo de shocks (1/HHI de los pesos de exposición) ≥ 10.

### Robustez y comparación
- **Robustez:**
  - sin las provincias de la muestra sellada de v6 (bandera informativa: no se lee data/sealed);
  - sin Madrid ni Barcelona;
  - ponderado por población.
- **Comparación.** LA07 (Sanchis-Guarner 2023), LA08 (González y Ortega 2013) y LA09 (Saiz 2007).

## D5 · Tipos de interés con exposición (panel de la zona euro; exploratorio)

**Pregunta.** ¿Responden más los precios de la vivienda a los shocks de política monetaria del BCE en los países con más hipotecas nuevas a tipo variable?

- **Datos.**
  - 18 países de la zona euro con precio BIS nominal y cuota RAI en 2003-2007.
  - Muestra 2008T1-2025T3.
  - Shock trimestral: suma de los shocks mensuales MP_median de Jarociński y Karadi.
- **Exposición.** Media de la cuota a tipo variable o con fijación ≤ 1 año en 2003-2007, estandarizada. Es fija y previa a la muestra.
- **Especificación.**
  - y_{i,t+h} − y_{i,t−1} = α_i + δ_t + β_h (shock_t × e_i) + Σ_{l=1..4} γ_l Δy_{i,t−l} + ε, para h = 0…12.
  - Errores de Driscoll y Kraay (ancho de banda h + 4).
- **Parámetros.**
  - β_4 y β_8 sobre log del precio BIS;
  - IPCA de alquiler (media trimestral) como resultado secundario.
- **Capa.** C4, exploratorio: el MDE con Holm (0,117 a 0,152) supera la referencia de 0,05. Se publican la figura de la proyección local y las bandas.
- **Robustez.**
  - Shock CBI (información del banco central) en lugar de MP.
  - Muestra 2008-2019.
  - Sin España.

## D6 · Bono Alquiler Joven: discontinuidad en los 35 años (NO se estima)

- La ECV publica el año de nacimiento (RB080) y el mes y año de la entrevista (PB100, PB110), pero **no el mes de nacimiento** (PB130 no figura en el fichero de usuario). La edad exacta en la fecha de solicitud no es observable: el error de edad es de hasta un año alrededor del umbral.
- La EPA solo publica tramos quinquenales de edad.
- Ninguna fuente identifica a los receptores del bono.
- Una discontinuidad con variable de asignación discreta y mal medida en el umbral no identifica el efecto. **No se estima.**
- Dato que lo resolvería: beneficiarios por edad en meses, CCAA y año (solicitud (d) de docs/v9/solicitudes_transparencia.md).

## D7 · Contabilidad hogares-viviendas por provincia (2011-2025; contable)

- **Descomposición del crecimiento de los hogares.**
  - ΔH = h̄ ΔP (efecto población) + P̄ Δh (efecto de la tasa de jefatura, h = H/P), con medias del periodo.
  - Periodos:
    - 2011→2021: censos (viviendas principales; 3457 y censo 2021 por municipio sumado a provincia);
    - 2021→2025: ECP de hogares por provincia (INE).
- **Descomposición de ΔP:**
  - saldo exterior por nacionalidad (EM y EMCR);
  - saldo interprovincial (EM y EMCR);
  - crecimiento natural más residuo (padrón y ECP).
- **Reconciliación del déficit 2021-2025.** Se comparan:
  - el proyecto (cifras_clave: L3-DEF-2125 y T1-H10, C4);
  - el Banco de España (Informe Anual 2025, unas 750.000; LA18);
  - la OCDE (unas 600.000 en 2022-2025; LA21, NO VERIFICADA).

  Para cada estimación se indican el periodo, la fuente de hogares y el tratamiento de las bajas.
- **Capa.**
  - C1 solo para recuentos con dos fuentes coincidentes: hogares del censo frente a la ECP en 2021.
  - C4 para las descomposiciones.
- Sin contraste ni p-valores. La regla v5.1 se mantiene: las viviendas liberadas por envejecimiento no se restan.

## F4 · Cotas de contribución (C2)

- **Qué se acota.** Solo los efectos C3 o C4 robustos, entendiendo por robusto que tenga el mismo signo y p de BH < 0,10 en la principal y en todas las alternativas.
- **Cálculo.** Contribución = efecto (extremos del IC 95 %) × exposición observada. Se calcula para la subida nacional y para la de la Comunitat Valenciana, con la medida de precio de cada resultado.
- **Advertencia.** Equilibrio parcial: los efectos se estiman entre territorios y no incluyen el desplazamiento entre ellos.
- **Tabla final.** Contribución mínima y máxima atribuible por factor.

## Sellado

- Commit del pre-registro: **2977349e3ed3092a51c8a3ad309140cf0b83dca8** (2026-10-15), subido a la rama remota designada. El hash se añade en el commit siguiente, porque un fichero no puede contener el hash de su propio commit. Todo cambio posterior a este documento se anota como desviación en docs/v9/decisiones.md.
- Etiqueta local: `prereg-v9`.

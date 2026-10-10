# ¿Qué se puede afirmar sobre el problema de la vivienda en España? Hechos, cotas y efectos con datos públicos (v3)

**Resumen.** Clasificamos la evidencia sobre el mercado de la vivienda en España en cuatro capas:
- C1, hechos con ≥2 fuentes;
- C2, cotas de identificación parcial;
- C3, efectos identificados;
- C4, exploratorio.

Sobre esa base examinamos los factores más citados en el debate y simulamos soluciones con rangos de parámetros.
- **Hechos (C1).** Entre 2021 y 2025 los hogares crecieron en 560.000-969.000 más que las viviendas nuevas. La propiedad de los hogares menores de 35 años cayó 24,2-34,0 puntos desde 2008. Entre el 27,5 % y el 40,3 % de las viviendas vacías de los 277 municipios con dato está en el tercil de mayor presión de precios.
- **Cotas (C2).** El aumento de viviendas turísticas de 2020 a 2024 equivale como máximo al 2,7 % del stock de alquiler.
- **Efectos.** Ningún diseño alcanzó C3. Los topes de alquiler de Cataluña (2020-2022) se asocian a rentas un 5,4 % menores en los contratos nuevos (C4), en línea con la literatura replicada, sin alcanzar C3. La asociación entre viviendas turísticas y alquiler por sección censal es de +0,0010 log-puntos por punto de VUT en la muestra sellada (IC95 −0,0007 a +0,0028), sin distinguirse de cero. En la simulación, solo las medidas que añaden viviendas donde hay demanda tienen un signo estable en toda la rejilla de supuestos; la simulación no incluye costes.

## 1. Introducción y estándar epistémico
El proyecto parte de dos versiones previas: v1, un modelo nacional; y v2, con paneles provinciales, una muestra sellada y Holm sobre 7 hipótesis, sin ninguna confirmada. La v3 cambia la pregunta: ya no busca «qué explica la subida», sino **qué puede afirmarse con seguridad y qué no**.

Cada resultado se asigna a una capa y nunca se promueve:
- **C1** exige ≥2 fuentes independientes y un rango de medida.
- **C2** exige supuestos débiles y explícitos.
- **C3** exige cinco condiciones, todas fijadas en el pre-registro (docs/v3/hipotesis.md, ancla 204c073):
  - (a) pretendencias, con Rambachan-Roth y M̄ = 1;
  - (b) placebos de tratamiento y de resultado;
  - (c) sensibilidad de Oster y Cinelli-Hazlett;
  - (d) validación sellada;
  - (e) Holm.

## 2. Datos
Todas las fuentes son públicas (data/raw/_manifest.csv):
- **INE:** viviendas turísticas por sección censal, 12 oleadas entre 2021M02 y 2026M05, obtenidas de sus servicios cartográficos; censo 2021 y censos anuales 2021-2025 por sección; Atlas de renta 2019-2023; ECV.
- **MIVAU:** SERPAVI por sección 2011-2024 (stock de contratos declarados en el IRPF); viviendas terminadas; parque.
- **Banco de España:** EFF 2002-2022, con tablas validadas contra el texto de cada oleada.
- **Otras:** fianzas de Incasòl (Cataluña, contratos nuevos, 2007-2026); Eurostat; Inside Airbnb (9 ciudades, desde 2025-12); Registradores y Notariado.
- **Fallos y pendientes:**
  - No se pudieron descargar el SIU, las fianzas de la GVA, los barrios de Barcelona (opendata con bloqueo anti-bot), el histórico de Airbnb ni Google Trends (docs/v3/fuentes_fallidas.md).
  - Las solicitudes de transparencia sobre grandes tenedores y suelo están redactadas y pendientes de presentar (docs/v3/solicitudes_transparencia.md).

**Muestra sellada v3.** La forman el 20 % de los distritos censales (2.136 de 10.460), en bloques de distritos contiguos estratificados por gran ciudad o provincia, más la última oleada. Se fijó antes de estimar y se abre una vez por hipótesis con `holdout.evaluate_v3`.

Hubo dos incidencias, ambas declaradas (docs/v3/decisiones.md, O1):
- Un cálculo de potencia de P-C3 incluyó municipios sellados. Por eso la validación de P-C3 se hizo por fuente (SERPAVI), no espacialmente.
- Se hizo un `describe()` del tratamiento antes de fijar el sellado.

## 3. Hechos (C1) y cotas (C2)
Fuentes: output/v3/PA y output/v3/PB.

| Hecho o cota | Valor (rango) | Capa |
|---|---|---|
| Balance hogares − viviendas nuevas 2021-2025 | +701.000 (560.000-969.000) | C1 |
| El mismo balance desde 2012 | signo no determinado (−436.000 a +1.501.000) | C1 (rango) |
| Terminadas por año 2021-2025 | 89.000-101.000 | C4 (fuente única: fin de obra MIVAU) |
| Personas de 25-34 años que viven con sus padres | 40-50 % | C1 |
| Hogares que se formarían con la emancipación de referencia | 188.000-748.000 | C2 |
| Propiedad de hogares de menos de 35 años (2022) | 30,7-31,8 %; −24 a −34 puntos frente a 2008 | C1 |
| Precio/renta (80 m², 2023) | 3,0-4,1 años | C1 |
| Vacías en el tercil alto de presión (277 municipios con dato; dos medidas) | 27,5-40,3 % (tercil bajo 20,7-28,3 %) | C1 |
| Viviendas vacías, total (Censo 2021, consumo eléctrico) | 3,8 millones | C4 (fuente única) |
| Razón precio/alquiler 2015-2024 | dirección no establecida (−9 % a +44 %) | C1 (rango) |
| Compraventas por personas de nacionalidad extranjera, 2023-2025 (output/v3/verificador/fichas/V14.json) | 9,6-15,0 % | C1 |
| Desplazamiento máximo de la oferta de alquiler por VUT 2020-2024 | ≤2,4-2,7 % del stock | C2 |
| Parte de la subida municipal del alquiler donde las VUT apenas crecieron | 25 % | C2 |
| Hogares extranjeros en la creación neta de hogares 2014-2019 | ≤45 % | C2 |
| Coste de uso 2014-2021 frente a 2021-2025 (con P/R = 1/uc) | compatible con toda la subida / signo contrario | C4 (supuesto estructural) |

Las traducciones a precio de las cotas de viviendas turísticas e inmigración dependen de una elasticidad de demanda sin estimación española verificada. La del coste de uso depende del supuesto estructural P/R = 1/uc. Las tres se presentan en C4, con el mismo estándar; las de VUT e inmigración, como tablas condicionales («si |ε| = x, como máximo y»).

## 4. Replicación y extensión

| Trabajo | Objetivo | Resultado propio | Clasificación |
|---|---|---|---|
| García-López et al. (2020, JUE), Barcelona 2012-2016, alquiler | 0,035 log-p por 100 anuncios ⇒ T = 0,012 log-p por pp de VUT (rango 0,012-0,117 por la razón VUT/anuncios) | Barcelona 2021-2024, sección: −0,0042 [−0,0078; −0,0005] | NO REPLICADO (signo contrario) |
| — extensión: València | T | +0,0050 [0,0001; 0,0099] | PARCIAL (magnitud menor) |
| — extensión: Madrid, Málaga, España | T | IC95 incluye 0 y excluye T | NO REPLICADO |
| — extensión: Sevilla | T | −0,0027 [−0,0045; −0,0009] | NO REPLICADO (signo contrario) |
| MESVAL-UV (2022), València, Madrid y Barcelona | +0,87 % por 100 anuncios | datos propietarios (Fotocasa) | NO REPLICABLE |
| Jofre-Monseny et al. (2023), topes de Cataluña, renta | −0,045 (0,006) | trimestral, Callaway-Sant'Anna, control tenso de menos de 20.000 hab.: −0,045 [−0,065; −0,026] | REPLICADO |
| — misma réplica, TWFE | −0,045 | −0,035 [−0,047; −0,023] | REPLICADO |
| — anual 2017-2022 | −0,045 | −0,030 [−0,044; −0,016] | PARCIAL |
| — contratos, TWFE | −0,003 (0,021) | +0,030 [−0,009; 0,070] | PARCIAL (IC incluye T y 0) |
| — contratos, Callaway-Sant'Anna | −0,003 (0,021) | −0,020 [−0,083; +0,042] | PARCIAL (IC incluye T y 0) |

**Qué cambia cada mejora:**
- *García-López.* Barcelona, por pasos:
  1. Unidad del artículo, por 100 VUT y por sección: −0,042 [−0,072; −0,012]. Unidad no homogénea con el objetivo.
  2. Ponderado por viviendas: −0,041 [−0,062; −0,019].
  3. Por punto porcentual de VUT sobre el parque, por sección: −0,0042 [−0,0078; −0,0005]. Por distrito: −0,0054 [−0,0093; −0,0014].
  4. Objetivo homogeneizado: pasa de 0,039 (con 73 barrios) a 0,012 (con las 233 áreas básicas del artículo); el rango es 0,012-0,117 según la razón VUT/anuncios.
  5. Excluir los distritos sellados se hizo antes de estimar, así que no hay estimación previa con la que comparar.
  6. Placebo por permutación de clústeres: p = 0,026.

  Ningún paso cambia la clasificación (NO REPLICADO).
- *Jofre-Monseny et al.* Renta, por pasos:
  1. TWFE trimestral 2019Q1-2022Q4, control de municipios tensos de menos de 20.000 habitantes, sin Barcelona: −0,035.
  2. Callaway-Sant'Anna con la misma muestra: −0,045.
  3. Frecuencia anual 2017-2022, mismo control: −0,030.
  4. Control con todos los municipios no sujetos y periodo hasta 2023Q4 (trimestral): −0,033.
  5. Lo mismo en anual 2017-2023: −0,026.

  En los pasos 4 y 5 cambian a la vez el grupo de control y el fin del periodo: con las especificaciones estimadas no se pueden separar ambos efectos. Es una limitación.

Diferencias de fondo con García-López et al.: el periodo (2021-2024 frente a 2012-2016), la medida del alquiler (SERPAVI, un stock que amortigua, frente al precio de oferta) y la ausencia de instrumento.

## 5. Efectos (diseños de la oleada 2)
**Potencia.** Antes de estimar se calculó el EMD con t(G−1) y wild cluster bootstrap:
- No se estimaron, por no ser detectables: la caída de anuncios de 2025-2026 (no hay alquiler a escala fina después de 2024) y el suelo como moderador.
- Las ciudades sueltas, con menos de 20 clústeres, no son concluyentes.

**H3-1 y H3-2, VUT → alquiler por sección.**
- *Estimaciones.*
  - H3-1 nacional con efectos fijos: β de entrenamiento +0,00026 [−0,0007; 0,0013] y sellada +0,00105 [−0,0007; 0,0028] (p = 0,23).
  - Con un aumento típico de 1,37 pp de VUT, la sellada equivale a +0,14 % (+0,8 €/mes).
  - H3-2, shift-share leave-one-out, 6 ciudades: β sellada +0,0042 [−0,0086; 0,0170] (F = 60).
- *Criterios de C3.* Fallan el test de adelanto, la sensibilidad y la validación sellada. El placebo de tratamiento (permutación dentro del municipio) pasa. El placebo de resultado (ADRH) es significativo (p = 0,0003) y se informa sin invalidar automáticamente, según P3. Capa C4. Holm: 0,47 y 0,50.
- *Sellado de H3-1 en las 6 ciudades.* β = −0,0013 [−0,0034; 0,0008], p = 0,20: signo opuesto al nacional. Solo el nacional era el contraste confirmatorio, una elección declarada como desviación.
- *Multiverso H3-1.* 96 especificaciones; nacional: 75 % con el mismo signo y 10 % significativas.
- *Hallazgo del test de adelanto (C4).* El crecimiento futuro de las VUT se asocia con el crecimiento pasado del alquiler en 2016-2020 (+0,0017 por pp, p < 0,001), un valor mayor que la estimación principal. Las VUT crecieron donde el alquiler ya subía. Si ese sesgo de selección es no negativo (supuesto no pre-registrado), la estimación sellada sería un límite superior del efecto medio. No se usa para ningún veredicto.

**H3-3, topes de la Ley 11/2020.**
- *H3-3a, renta de los contratos nuevos.* Callaway-Sant'Anna: −5,4 % [−7,1; −3,7], −37 €/mes. Validación sellada por fuente (SERPAVI): −0,77 % [−1,39; −0,14], p = 0,016 (Holm 0,048). Multiverso: 100 % con el mismo signo y 89 % significativas. Falla Rambachan-Roth (el IC con M̄ = 1 incluye 0) y la sensibilidad (RV 0,21 < R² 0,28). Capa C4.
- *H3-3b, número de contratos.* −4,9 % [−9,9; +0,5], p = 0,07. Fallan las pretendencias, el placebo de fecha y la sensibilidad. Capa C4.

## 6. Soluciones (P-D, simulación con rangos)
Ver output/v3/PD.
- Estabilizar el esfuerzo de acceso en 2026-2035 requiere 104.000-413.000 viviendas al año. La brecha frente a las terminadas es positiva en todo el rango (C2).
- Con signo estable en toda la rejilla, sin reducir la oferta: construir +25.000 a +100.000 viviendas al año, y movilizar el 10-30 % de las vacías del tercil alto de presión, que aporta el 4,6-51 % de la brecha (C2).
- Vivienda pública: dominancia débil, con efecto ≤ 0 y nulo si desplaza.
- Retirada de VUT: signo no estable con H3-1 sellado.
- Los costes no se modelan: la ordenación no es coste-beneficio.
- La opción de mínimo arrepentimiento máximo depende de la dosis supuesta (C4).
- Topes: reducción de renta de 148-598 €/año por inquilino cubierto; efecto sobre el esfuerzo medio de los inquilinos de −2,9 % a +7,3 % según la respuesta de la oferta (C4).

## 7. Verificador
Hay 14 afirmaciones del debate en output/v3/verificador/:
Las afirmaciones de atribución (turísticos, inmigración, oferta y suelo, tipos) se juzgan con una regla común:
- «causa principal» exige ≥50 % de la subida;
- una cota de cantidad no es respaldo;
- la evidencia C4 no decide.

Resultado:
- RESPALDADA (0).
- PARCIALMENTE (3): «faltan cientos de miles de viviendas» (respaldada en 2021-2025 y no determinada con 2012 como base), vacías movilizables y vivienda pública (según supuestos).
- SIN EVIDENCIA SUFICIENTE (11): turísticos, grandes tenedores, inmigración, oferta y suelo, tipos de interés como causa principal, topes (alquiler y oferta), ocupación ilegal, ITP/IVA, burbuja y compradores extranjeros.

Con el supuesto estructural P/R = 1/uc (C4), la afirmación sobre los tipos sería incompatible con 2021-2025 y no descartada en 2014-2021.

Ninguna afirmación queda NO RESPALDADA ni CONTRADICHA en su conjunto.

## 8. Limitaciones
Ver docs/v3/limitaciones.md. Las principales:
- ningún efecto C3;
- validación de P-C3 por fuente, no independiente;
- elasticidades sin estimación española;
- SERPAVI amortigua;
- las ventanas C1 de A1 se añadieron tras ver la disponibilidad de fuentes;
- secciones censales armonizadas solo por código estable.

## 9. Reproducibilidad
`make all` reconstruye todo sin red: datos en caché, paneles, modelos (v1, v2, v3) e informes, en un solo hilo y con SEED = 20261010. `make check` ejecuta ruff, los tests y el control de texto (neutralidad y capas). `make verificador` regenera las fichas. Los accesos a la muestra sellada se registran en docs/v2/holdout_accesos.md.

## 10. Declaración de uso de IA
El proyecto se ejecutó con agentes de IA (Claude): un orquestador y subagentes de datos, literatura, econometría y revisión independiente por oleadas. Todas las cifras proceden del código del repositorio y de fuentes públicas citadas. Las referencias se verificaron con DOI o se marcan como NO VERIFICADA. Las decisiones, desviaciones e incidencias están en docs/v3/decisiones.md.

## 11. Referencias (estado de verificación y cuartil Scimago)
| Referencia | DOI | Estado | Cuartil |
|---|---|---|---|
| García-López, Jofre-Monseny, Martínez-Mazza y Segú (2020), *Journal of Urban Economics* | 10.1016/j.jue.2020.103278 | VERIFICADA | Q1 |
| Jofre-Monseny, Martínez-Mazza y Segú (2023), *Regional Science and Urban Economics* | 10.1016/j.regsciurbeco.2023.103916 | VERIFICADA | Q1 |
| MESVAL-UV (2022), documento de trabajo 05/2022 | sin DOI en Crossref/DataCite | NO VERIFICADA | n/a |
| Saiz (2007), *Journal of Urban Economics* | 10.1016/j.jue.2006.07.004 | VERIFICADA | Q1 (año no comprobado) |
| Saiz (2010), *Quarterly Journal of Economics* | 10.1162/qjec.2010.125.3.1253 | VERIFICADA | cuartil no verificado |
| Sá (2015), *Economic Journal* | 10.1111/ecoj.12158 | VERIFICADA | Q1 |
| González y Ortega (2013), *Journal of Regional Science* | 10.1111/jors.12010 | VERIFICADA | cuartil no verificado |
| Glaeser y Gyourko (2018), *Journal of Economic Perspectives* | 10.1257/jep.32.1.3 | VERIFICADA | cuartil no verificado |
| Barron, Kung y Proserpio (2021), *Marketing Science* | 10.1287/mksc.2020.1227 | VERIFICADA | Q1 |
| Diamond, McQuade y Qian (2019), *American Economic Review* | 10.1257/aer.20181289 | VERIFICADA | Q1 |
| Kholodilin (2024), *Journal of Housing Economics* | 10.1016/j.jhe.2024.101983 | VERIFICADA | Q2 (año no comprobado) |
| Poterba (1984), *Quarterly Journal of Economics* | 10.2307/1883123 | VERIFICADA | Q1 |
| Khametshin et al. (2024), Banco de España, Documento Ocasional 2432 | 10.53479/37872 | VERIFICADA | sin cuartil (serie del BdE) |
| Banco de España (2026), Informe Anual 2025, cap. 2 | 10.53479/43565 | DOI no comprobado en Crossref | n/a |
| Manski (2003), *Partial Identification of Probability Distributions*, Springer | 10.1007/b97478 | VERIFICADA | libro |
| Oster (2019), *Journal of Business & Economic Statistics* | 10.1080/07350015.2016.1227711 | VERIFICADA | Q1 |
| Cinelli y Hazlett (2020), *JRSS-B* | 10.1111/rssb.12348 | VERIFICADA | Q1 |
| Rambachan y Roth (2023), *Review of Economic Studies* | 10.1093/restud/rdad018 | VERIFICADA | Q1 |
| Callaway y Sant'Anna (2021), *Journal of Econometrics* | 10.1016/j.jeconom.2020.12.001 | VERIFICADA | Q1 (año no comprobado) |
| de Chaisemartin y D'Haultfœuille (2020), *American Economic Review* | 10.1257/aer.20181169 | VERIFICADA | Q1 |
| Simonsohn, Simmons y Nelson (2020), *Nature Human Behaviour* | 10.1038/s41562-020-0912-z | VERIFICADA | cuartil no verificado |
| Conley (1999), *Journal of Econometrics* | 10.1016/s0304-4076(98)00084-0 | VERIFICADA | Q1 (año no comprobado) |
| Borusyak, Hull y Jaravel (2022), *Review of Economic Studies* | 10.1093/restud/rdab030 | VERIFICADA | Q1 |
| Goldsmith-Pinkham, Sorkin y Swift (2020), *American Economic Review* | 10.1257/aer.20181047 | VERIFICADA | Q1 |
| Adão, Kolesár y Morales (2019), *Quarterly Journal of Economics* | 10.1093/qje/qjz025 | VERIFICADA | Q1 (año no comprobado) |

Detalle y fuentes de la verificación: docs/v3/literatura_v3.md y docs/literatura.md (anexo v3).

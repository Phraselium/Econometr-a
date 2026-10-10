# Literatura v3 (verificación 2026-10-10)

Método: DOI comprobado en Crossref (api.crossref.org/works/<DOI> o consulta bibliográfica que devuelve el DOI). Cuartil: scimagojr.com devuelve 403; se reutiliza el cuartil ya registrado en docs/literatura.md (misma revista, años indicados) y, si no existe, «cuartil no verificado». Solo se verificaron las referencias que no estaban ya como VERIFICADA en docs/literatura.md; las demás se citan con su estado previo. Las cifras proceden del texto leído (PDF) salvo indicación; lo no leído se marca «no extraído».

Correcciones a la petición:
- El diseño de Jofre-Monseny et al. (2023) NO es una frontera por encima/debajo de un índice. Es DiD a nivel municipio-trimestre: municipios regulados (más de 20.000 habitantes y mercado tenso) frente a municipios no regulados que también tenían mercado tenso (crecimiento anual del alquiler 2014-2019 ≥ 4,15 %) pero no cumplían el criterio de población.
- El BdE DO 2432 trata del alquiler, no del déficit. Las cifras de déficit (≈ 750.000 viviendas 2021-2025; método: viviendas terminadas menos creación neta de hogares) están en el Informe Anual 2025 y, por provincias, en el DO 2433 (cifra literal no extraída).

---

## A. Protocolos de replicación

### A1. García-López, Jofre-Monseny, Martínez-Mazza y Segú (2020)
- Referencia: «Do short-term rental platforms affect housing markets? Evidence from Airbnb in Barcelona», *Journal of Urban Economics* 119, art. 103278. DOI 10.1016/j.jue.2020.103278. **VERIFICADA** (Crossref, v2). Cuartil: Q1 (SJR 2025; año de publicación no comprobado).
- Aviso de versión: las cifras y tablas siguientes se leyeron en el documento de trabajo IEB WP 2019/05 (versión de 2019, PDF ieb.ub.edu). La versión publicada da +4,6 % en precios de transacción en vez de +5,3 % (ver v2); los coeficientes de la versión publicada **no se leyeron**. Antes de replicar hay que fijar la versión objetivo.
- Pregunta: efecto de la actividad de Airbnb sobre alquileres y precios por barrio.
- Datos: unidad = área estadística básica (AEB, 233, media 7.122 habitantes). Airbnb: InsideAirbnb, 21 capturas abril 2015-febrero 2018; un anuncio está activo en un trimestre si recibe al menos una reseña. Alquileres: anuncios de Idealista, cada diciembre 2007-2017 (panel AEB-año). Precios de transacción: registros del ITP de la Agència Tributària de Catalunya, 2009-2016 (panel AEB-trimestre). Precios de oferta: Idealista. Controles demográficos anuales por AEB (edad media, log densidad, ocupación media del hogar, paro, renta relativa, % extranjeros).
- Ecuación (4): log(Y_nt) = β·AirbnbCount_nt + γ·X_nt + μ_n + τ_t + ε_nt. Y_nt es el residuo medio AEB-periodo de una regresión micro de log precio o alquiler sobre características de la vivienda y dummies temporales. Tratamiento: número de anuncios activos (en cientos). Ponderación por número de anuncios (alquiler y oferta) o de transacciones (ITP). Efectos fijos de AEB y de tiempo. Cluster: AEB.
- Instrumento (shift-share): TouristAmenities_n × GoogleTrends_t. Share: Σ_k (1/dist_nk)·Reviews_k (distancia en metros del centroide de la AEB a cada atractivo de TripAdvisor, ponderado por reseñas de Google; se excluyen zonas de restauración y ocio nocturno). Shift: búsquedas mundiales en Google Trends del término «Airbnb Barcelona», mensual, normalizado a 100. Validez: tendencias previas del instrumento (Figura 7) y event study con las AEB del decil superior (Figura 8).
- Coeficientes objetivo (WP 2019, coeficiente por 100 anuncios, EE entre paréntesis, cluster AEB):

| Resultado | Tabla/columna | Coef. (EE) | N |
|---|---|---|---|
| log alquiler, FE + controles (base) | Tabla 3, panel A, col. 2 | 0,035 (0,009) | 2.123 |
| log precio ITP, base | Tabla 3, panel B, col. 2 | 0,097 (0,019) | 7.005 |
| log precio de oferta, base | Tabla 3, panel C, col. 2 | 0,068 (0,009) | 2.229 |
| log alquiler, con tendencias lineales por AEB (destendenciado) | Tabla 3, panel A, col. 5 | 0,034 (0,018) | 2.123 |
| log alquiler, IV 2.ª etapa | Tabla 6, col. 2 | 0,022 (0,011); F 1.ª etapa 191,80 | 2.138 |
| log precio ITP, IV | Tabla 6, col. 4 | 0,158 (0,024); F 158,70 | 7.018 |
| log precio de oferta, IV | Tabla 6, col. 6 | 0,074 (0,014); F 158,61 | 2.247 |
| log hogares (mecanismo) | Tabla 5, col. 2 | −0,028 (0,006) | 1.827 |
| log alquiler, log-log | Tabla 4, col. 4 | 0,0098 (0,003) | 2.123 |

- Efectos implícitos: 54 anuncios (media 2012-2016) dan +1,89 % en alquiler, +5,24 % en ITP y +3,67 % en precio de oferta; 200 anuncios (decil superior) dan ≈ +7 %, +19-20 % y +14 %. La Tabla 6 imprime tres asteriscos en el alquiler IV (0,022 con EE 0,011); el cociente es ≈ 2, por lo que la significación al 1 % parece un error de impresión; replicar y comprobar.
- Datos abiertos actuales (no comprobada su disponibilidad en esta sesión): InsideAirbnb (capturas públicas; su cobertura histórica anterior a 2016 debe comprobarse y puede obligar a reconstruir la actividad con reseñas); Google Trends (público); demografía por AEB en Open Data BCN; fianzas de alquiler de Incasòl (Dades Obertes de Catalunya) como sustituto de los alquileres de Idealista (otra definición de variable). Los precios ITP de la ATC y los anuncios de Idealista no son abiertos. Reseñas de Google de los atractivos: sustituir por puntos de interés abiertos (OSM). **Réplica exacta: no. Réplica parcial del alquiler: viable.**

### A2. MESVAL-UV (2022)
- Referencia: Pastor, J. M., Morillas, F., Morala, J. F. y Serrano, L. (2022). *El impacto de los apartamentos turísticos en el precio de los alquileres en València: estudio comparado con Madrid y Barcelona*. Càtedra Model Econòmic Sostenible València i Entorn (MESVAL), Universitat de València, Documento de Trabajo DT 05/2022. PDF: uv.es/mesval/Informes-2022/MESVAL_2022_DT_05-AIRBNB.pdf.
- DOI: el PDF imprime «10.12842/MESVAL_DT2022_05», pero api.crossref.org/works/<DOI> y api.datacite.org devuelven 404. **NO VERIFICADA** (DOI impreso sin registro comprobado).
- Cuartil: no aplica (documento de trabajo de cátedra).
- Lectura: solo el resumen ejecutivo (pp. 7-16). Los capítulos de metodología (p. 69) y resultados (p. 77; Cuadros 4-6) **no se leyeron**; no se extraen coeficientes por tabla.
- Datos: más de 3,2 millones de registros de Fotocasa (alquiler y venta) y Airbnb, año 2021, València, Madrid y Barcelona; 2.030.403 registros de vivienda (806.045 en alquiler, 1.224.358 en venta); zonas = secciones censales o barrios; variables socioeconómicas resumidas en 4 componentes principales (renta, envejecimiento, desigualdad, fuerza de trabajo).
- Método: bietápico. Etapa 1: regresión hedónica del alquiler. Etapa 2: la parte no explicada se modela con las componentes y el número de anuncios Airbnb del barrio; modelos en niveles y en logaritmos; con y sin efectos fijos de distrito. Es un corte transversal de un solo año, sin diseño de identificación causal declarado en el resumen.
- Resultados cuantitativos (resumen ejecutivo):
  - +0,87 % del alquiler por cada 100 anuncios por barrio (conjunto de las tres ciudades); +0,82 % con controles por características no observables del barrio.
  - Por ciudad: València +3,2 % a +3,6 % por cada 100 anuncios (sin o con efectos fijos de distrito); Madrid y Barcelona entre +0,7 % y +0,9 %. No se rechaza la igualdad entre ciudades.
  - Elasticidad: +1 % de anuncios implica +0,056 % en el alquiler (0,057 % València; 0,05 % Madrid y Barcelona).
  - Contrafactual 2011-2021: el alquiler sería +3,3 % más alto por Airbnb en València, +2 % en Barcelona y +1,6 % en Madrid (texto de la p. 13); equivale a 8,4 % (València), 9,1 % (Madrid) y 10,5 % (Barcelona) del aumento acumulado; en euros por m² y mes, 0,29 (València), 0,28 y 0,21 (el texto no deja claro cuál es Madrid y cuál Barcelona).
  - Inconsistencia interna: la infografía de la p. 16 da +2 % para Madrid y +16 % (1,6 €/m²) para Barcelona, que no coincide con el texto de la p. 13. No usar esas cifras sin revisar los cuadros.
- Datos abiertos: Fotocasa es propietario; Airbnb (fuente no leída). **Réplica exacta: no.** Réplica aproximada con SERPAVI/fianzas, VUT del INE y InsideAirbnb.
- Nota de uso: la cifra de Valencia Plaza sobre «1,8 %» procede de un dictamen pericial de parte (Aptur CV) que cita este estudio; no es del informe.

### A3. Jofre-Monseny, Martínez-Mazza y Segú (2023), Ley 11/2020 de Cataluña
- Referencia: «Effectiveness and supply effects of high-coverage rent control policies», *Regional Science and Urban Economics* 101, art. 103916. DOI 10.1016/j.regsciurbeco.2023.103916. **VERIFICADA** (Crossref, v2; autores, revista, volumen, artículo y fecha de julio de 2023 releídos). Cuartil: Q1 (2019-2025, valor de la tabla v2 para esta misma revista; el cuartil propio del artículo no se comprobó por separado).
- Texto leído: preprint de julio de 2023 (repositorio UB, diposit.ub.edu); se asume que la tabla coincide con la publicada, sin comprobar.
- Datos: universo de contratos de alquiler firmados y finalizados en Cataluña 2016-2022 (registro administrativo; el preprint no nombra la fuente); ventas de IDESCAT; paro, contratos y ERTO de la Seguridad Social; flujos migratorios de la Estadística de Variaciones Residenciales. Agregación municipio-trimestre. Muestra: 58 municipios regulados y 90 de control (148, panel equilibrado, 3.698 observaciones); se excluye Barcelona.
- Tratamiento: RentControl_m × Post_t (primer trimestre tratado: 4.º trimestre de 2020; política en vigor desde el 21/09/2020, derogada en marzo de 2022). Ecuación (1): Y_mt = α + β(RentControl_m × Post_t) + γ_m + δ_t + X_mt + ε_mt, con X = paro, ERTO y contratos nuevos por 100 habitantes. Efectos fijos de municipio y trimestre. Cluster: municipio. Event study con base en 2019T4 (ecuación 2). Anticipación: tercer trimestre de 2020.
- Coeficientes objetivo (EE en paréntesis):

| Resultado | Tabla/columna | Coef. (EE) |
|---|---|---|
| log alquiler medio, preferida | Tabla 2, col. 3 | −0,045 (0,006) |
| log alquiler, sin controles | Tabla 2, col. 1 | −0,044 (0,006) |
| log contratos firmados por 1.000 hab. | Tabla 2, col. 6 | −0,003 (0,021) |
| anticipación en contratos | Tabla 2, col. 6 | +0,130 (0,029) |
| contratos finalizados | Tabla 3, col. 3 | −0,006 (0,023) |
| stock activo de viviendas alquiladas | Tabla 3, col. 4 | +0,002 (0,007) |
| precio de venta | Tabla 3, col. 5 | +0,015 (0,013) |
| número de ventas | Tabla 3, col. 6 | −0,071 (0,028); frágil según el texto |
| alquiler, viviendas ya alquiladas / nuevas | Tabla 4, cols. 2 y 1 | −0,056 (0,009) / −0,047 (0,008) |
| alquiler con tendencias propias por municipio | Tabla 5, col. 2 | −0,051 (0,007) |
| alquiler sin vecinos de regulados (contagio) | Tabla 5, col. 8 | −0,058 (0,007) |

- Lectura: alquileres −4 % a −6 % (≈ 30 euros al mes); sin caída de contratos firmados, finalizados ni del stock activo; la anticipación sube los contratos de 2020T3 (+13 %); los vecinos no regulados bajan ≈ 2,7 % (la estimación base sería una cota inferior).
- Datos abiertos actuales: la fuente microdatos del preprint no es pública; el diseño sí se puede reproducir a nivel municipio-trimestre con estadísticas agregadas de fianzas (Incasòl), IDESCAT, EVR del INE y paro registrado (disponibilidad por municipio-trimestre no comprobada en esta sesión). **Réplica: parcial, a nivel agregado.**
- Otro trabajo verificado (una línea): Monràs y García-Montalvo (2023), FRBSF WP 2023-28, DOI 10.24148/wp2023-28, **VERIFICADA** como documento de trabajo (sin cuartil; cifras inestables entre versiones, ver v2).

---

## B. Magnitudes para calibrar simulaciones (P-D), sin replicar

Todas las magnitudes proceden de abstracts o del texto indicado; IC/EE «no extraído» significa que no se leyó. Los estados son los de docs/literatura.md salvo los marcados.

| Referencia | DOI | Estado | Cuartil | Parámetro | Valor | IC/EE | Ámbito y periodo | Uso en P-D |
|---|---|---|---|---|---|---|---|---|
| BdE, Informe Anual 2025, cap. 2 (2026) | 10.53479/43565 | PDF oficial (v1); DOI no comprobado en Crossref | n/a | Déficit acumulado de viviendas (terminadas menos creación neta de hogares) | ≈ 750.000 (3,7 % de hogares); IEF otoño 2025: 700.000 | sin IC | España, 2021-2025 | Brecha de partida entre oferta y hogares |
| BdE, IA 2025 | idem | idem | n/a | Elasticidad de oferta a largo plazo | ≈ 0,45 (cota superior de la respuesta actual) | sin IC | España | Elasticidad de oferta, rango bajo |
| Khametshin et al. (2024), BdE DO 2432 | 10.53479/37872 | VERIFICADA | sin cuartil (serie BdE) | Descomposición de la subida del alquiler | solo cualitativa: demanda crece más que oferta desde 2015 | no extraído | España, desde 2015 | Contexto; no calibra |
| Lajer Baron et al. (2024), BdE DO 2433 | 10.53479/37873 | VERIFICADA (v1) | sin cuartil | Déficit provincial 2022-2025 | cifra total no extraída; Madrid y Barcelona ≈ 1/3 | no extraído | provincias | Reparto territorial |
| Saiz (2007) | 10.1016/j.jue.2006.07.004 | VERIFICADA | Q1 (SJR 2025; año no comprobado) | Inmigración sobre alquiler y valor | entrada del 1 % de la población → ≈ +1 % | EE no extraído | áreas metropolitanas EE. UU., censos | Elasticidad demanda-alquiler (IV) |
| Saiz (2010) | 10.1162/qjec.2010.125.3.1253 | VERIFICADA | cuartil no verificado | Elasticidad de oferta | 1,75 ponderada (2,5 sin ponderar); < 1 en ciudades restringidas | no extraído | EE. UU. | Rango de oferta |
| Sá (2015) | 10.1111/ecoj.12158 | VERIFICADA | Q1 (1999-2025) | Inmigración sobre precios | −1,6 % por 1 % de población (versión IZA DP 5893) | no extraído | Reino Unido | Escenario de signo opuesto |
| González y Ortega (2013) | 10.1111/jors.12010 | VERIFICADA | cuartil no verificado | Inmigración sobre precios y construcción | flujo del 17 % de la población en edad de trabajar → precios ≈ +52 %, construcción ≈ +37 % | no extraído | provincias de España, 1998-2008 | Calibración de demanda por inmigración en España (cota alta) |
| Glaeser y Gyourko (2018) | 10.1257/jep.32.1.3 | VERIFICADA | cuartil no verificado | Brecha precio-coste | sin cifra citable | n/a | EE. UU. | Solo marco conceptual |
| Barron, Kung y Proserpio (2021) | 10.1287/mksc.2020.1227 | VERIFICADA | Q1 (1999-2025) | Airbnb sobre alquileres y precios | +1 % de anuncios → +0,018 % alquiler y +0,026 % precio (versiones de trabajo y cita en García-López et al.; versión de la revista no confirmada) | EE no extraído | códigos postales EE. UU. | Elasticidad turística (límite inferior) |
| García-López et al. (2020), WP 2019 | 10.1016/j.jue.2020.103278 | VERIFICADA | Q1 (SJR 2025) | Airbnb sobre alquiler, ITP y precio de oferta | +0,035 / +0,097 / +0,068 por 100 anuncios; IV +0,022 / +0,158 / +0,074 | 0,009 / 0,019 / 0,009; IV 0,011 / 0,024 / 0,014 | AEB de Barcelona, 2007-2017 | Elasticidad turística en España |
| MESVAL (2022) | sin DOI verificado | **NO VERIFICADA** | n/a | Anuncios Airbnb sobre alquiler | +0,87 % por 100 anuncios; elasticidad 0,056 | no extraído | València, Madrid, Barcelona, 2021 | Solo robustez |
| Diamond, McQuade y Qian (2019) | 10.1257/aer.20181289 | VERIFICADA | Q1 (1999-2025) | Control de alquiler sobre oferta | −15 % de oferta de alquiler en los inmuebles afectados | no extraído | San Francisco, 1994 | Efecto de oferta de topes |
| Jofre-Monseny et al. (2023) | 10.1016/j.regsciurbeco.2023.103916 | VERIFICADA | Q1 (2019-2025) | Tope de alquiler sobre alquiler y contratos | −4,5 %; contratos −0,3 % | EE 0,006; 0,021 | municipios de Cataluña, 2016-2022 | Efecto tope sin caída de oferta a corto plazo |
| Kholodilin (2024) | 10.1016/j.jhe.2024.101983 | VERIFICADA | Q2 (SJR 2025; año no comprobado) | Revisión de efectos de topes | sin cifra extraída | n/a | revisión internacional | Contexto |
| Poterba (1984) | 10.2307/1883123 | VERIFICADA | Q1 (agregador de Scimago) | Inflación y coste de uso sobre precio real | hasta ≈ +30 % en el precio real (simulación) | n/a | EE. UU., años setenta | Orden de magnitud; no es semielasticidad estimada |
| Romero Jordán, Sanz Sanz y Pérez López (2006), Fundación de las Cajas de Ahorros DT 249/2006 | sin DOI | **NO VERIFICADA** | n/a | Elasticidad precio de la demanda de vivienda en España | «inferior a la unidad»; elasticidad renta y población ≈ 1; tipos de interés no relevantes (solo resumen visto en una búsqueda) | no extraído | España, 1885-2000 | Pista para el rango; no citar la cifra |

Lagunas de la tabla B: (1) semielasticidad del precio a los tipos hipotecarios o al coste de uso para España: no se localizó ninguna estimación verificable (Martínez Pagés y Maza 2003 existe en v1 pero sin elasticidad extraída); (2) elasticidad precio de la demanda: solo la pista de arriba; (3) EE de Saiz, Sá, González-Ortega y Diamond: no extraídos.

---

## C. Métodos (solo las no verificadas antes, más estado de las ya verificadas)

| Referencia | DOI | Estado | Cuartil |
|---|---|---|---|
| Manski, C. F. (2003). *Partial Identification of Probability Distributions*. Springer Series in Statistics. Libro | 10.1007/b97478 | VERIFICADA (Crossref: título, editorial Springer-Verlag, año 2003, tipo libro, ISBN 0387004548; el registro no lista autor, atribuido por conocimiento previo) | no aplica (libro). Artículo alternativo (Manski 1990, AER P&P 80(2)): no verificado, sin DOI localizado |
| Oster, E. (2019). Unobservable selection and coefficient stability: Theory and evidence. *JBES* 37(2), 187-204 | 10.1080/07350015.2016.1227711 (Crossref lo fecha en línea en 2017) | VERIFICADA | Q1 (agregador de Scimago; año no comprobado, de v2-B) |
| Cinelli, C. y Hazlett, C. (2020). Making sense of sensitivity: Extending omitted variable bias. *JRSS-B* 82(1), 39-67 | 10.1111/rssb.12348 (Crossref lo fecha en 2019, en línea) | VERIFICADA | Q1 (agregador de Scimago; año no comprobado, de v2-B para JRSS-B) |
| Rambachan, A. y Roth, J. (2023). A more credible approach to parallel trends. *REStud* 90(5), 2555-2591 | 10.1093/restud/rdad018 | VERIFICADA | Q1 (1999-2025, REStud en v2) |
| Callaway, B. y Sant'Anna, P. H. C. (2021). *J. Econometrics* 225(2), 200-230 | 10.1016/j.jeconom.2020.12.001 | VERIFICADA (v2) | Q1 (SJR 2025; año no comprobado) |
| de Chaisemartin, C. y D'Haultfœuille, X. (2020). *AER* 110(9), 2964-2996 | 10.1257/aer.20181169 | VERIFICADA (v2) | Q1 (1999-2025) |
| de Chaisemartin, C. y D'Haultfœuille, X. (2026). Difference-in-differences estimators of intertemporal treatment effects. *Review of Economics and Statistics* 108(4), 863-880 (Crossref fecha 2026) | 10.1162/rest_a_01414 | VERIFICADA | Q1 (1999-2025, REStat en v2) |
| de Chaisemartin, D'Haultfœuille, Pasquier, Sow y Vazquez-Bare, DiD para tratamientos continuos (arXiv 2201.06898; v6, agosto de 2025, «Difference-in-Differences for Continuous Treatments and Instruments with Stayers») | DOI de arXiv: Crossref devolvió 404 | **NO VERIFICADA** (sin DOI comprobado ni versión en revista) | n/a |
| Simonsohn, U., Simmons, J. P. y Nelson, L. D. (2020). Specification curve analysis. *Nature Human Behaviour* 4(11), 1208-1214 | 10.1038/s41562-020-0912-z | VERIFICADA | cuartil no verificado |
| Conley, T. G. (1999). GMM estimation with cross sectional dependence. *J. Econometrics* 92(1), 1-45 | 10.1016/s0304-4076(98)00084-0 | VERIFICADA | Q1 (SJR 2025 para la revista, de v2; año no comprobado) |
| Borusyak, Hull y Jaravel (2022), *REStud* 89(1), 181-213 | 10.1093/restud/rdab030 | VERIFICADA (v1) | Q1 (1999-2025) |
| Goldsmith-Pinkham, Sorkin y Swift (2020), *AER* 110(8), 2586-2624 | 10.1257/aer.20181047 | VERIFICADA (v1) | Q1 (1999-2025) |
| Adão, Kolesár y Morales (2019), *QJE* 134(4), 1949-2010 | 10.1093/qje/qjz025 | VERIFICADA (v1) | Q1 (agregador de Scimago; año no comprobado) |

Notas: (1) Oster: la versión de trabajo NBER w19054 (2013) tiene otro título («Theory and Validation»); se cita la de la revista. (2) Cinelli-Hazlett: no se confunda con su extensión a IV (SSRN 4217915, 2022), no verificada como artículo.

---

## Recuento

VERIFICADA: 25 referencias (A: García-López, Jofre-Monseny, Monràs-García-Montalvo [WP]; B: BdE DO 2432, BdE DO 2433, Saiz 2007, Saiz 2010, Sá, González-Ortega, Glaeser-Gyourko, Barron et al., Diamond et al., Kholodilin; C: Manski, Oster, Cinelli-Hazlett, Rambachan-Roth, Callaway-Sant'Anna, dCDH 2020, dCDH 2026, Simonsohn et al., Conley, BHJ, GPS, AKM). El Informe Anual 2025 del BdE y Poterba (1984) constan como verificados en v1 y no se cuentan de nuevo.
NO VERIFICADA: 3 (MESVAL DT 05/2022 por DOI impreso sin registro; Romero Jordán et al. 2006 sin DOI; dCDH et al. tratamiento continuo, arXiv).

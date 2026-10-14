# Literatura A (V9-prep, bloque 2A): fichas breves

Fecha: 2026-10-14. Tabla completa en `literatura_A.csv`; BibTeX de lo verificado en `literatura_A.bib`. Fuentes de verificación: Crossref (`api.crossref.org/works/<DOI>`), OpenAlex y, para BdE y OCDE, el registro del DOI. Scimago (scimagojr.com) devuelve 403: los cuartiles proceden de agregadores que replican Scimago o de lo ya anotado en `docs/literatura.md`; ninguno se leyó en scimagojr.com. Los números de abstract proceden de lo leído en Crossref/OpenAlex (parafraseado); donde no consta magnitud se dice «no extraída». Las fichas de think tank/prensa son hipótesis, no evidencia.

Recuento: 35 entradas; 34 con DOI verificado (LA35 NO VERIFICADA); 26 con cuartil con fuente (agregador/Scimago indirecto), 2 «cuartil no verificado» (LA05, LA26), 7 no aplica (BdE, OCDE, LA35).

## Actualiza docs/literatura.md

- **González y Ortega (2013)** (LA08): el abstract publicado (OpenAlex, 2026-10-14) dice periodo 2000-2010, población en edad de trabajar +1,5 % anual, precios ≈ +2 % anual, viviendas +1,2-1,5 %, y «un cuarto del aumento de precios y la mitad de la construcción». Las cifras de `docs/literatura.md` (17 %, +52 %, ~37 %, un tercio, 1998-2008) parecen de la versión de trabajo (IZA DP 4333). Verificar con el texto antes de usar cualquiera.
- **Torres-Téllez y Montero-Soler (2023)** (LA26): el abstract de Crossref indica efecto neto negativo en 2001-2019 (v2 de `docs/literatura.md` no lo recogía).

## Contradicciones y tensiones a vigilar

- **Signo de la inmigración**: positivo en EE. UU. (Saiz 2007) y España (González-Ortega 2013, Sanchis-Guarner 2023 componente directo); negativo en Reino Unido (Sá 2015) por salida de nativos; en España, Torres-Téllez y Montero-Soler dan efecto neto negativo del periodo completo (+2,5 % en la burbuja, -1,12 % tras la crisis). Las unidades no son comparables.
- **Magnitudes de Airbnb**: Barcelona +1,9 % en alquiler y +4,6 % en precio (García-López 2020); Madrid ≈ +2 % en precio por 100 anuncios (Chaves-Fonseca 2026); San Sebastián +49,45 euros/mes por anuncio por 100 viviendas (≈ +3,9 %, cálculo propio) y los autores lo consideran muy superior a las grandes ciudades; la cifra de la Cátedra de la Universitat de València (+0,056 % por +1 % de anuncios), solo vía prensa, es de otro tipo (elasticidad) y no verificada.
- **Déficit de vivienda**: 750.000 (BdE, 2021-2025) frente a ≈600.000 (OCDE 2025 según resumen de buscador, 2022-2025). Periodos y vintages distintos.
- **Convergencia europea/territorial**: Ghirelli et al. (2023) hallan convergencia entre ciudades españolas con máximo en 2009 y descenso posterior; Maynou et al. (2021) estudian clubes de convergencia en Europa (resultado no extraído). Posible tensión; sin comprobar.
- **Crédito vs expectativas**: Kaplan et al. (2020) priorizan creencias frente a crédito; Gimeno y Martínez-Carrascal (2010) y Martín et al. (2021) sitúan el crédito en el centro del boom español.

## Fichas

Formato: pregunta · datos · identificación · resultado con signo y magnitud · replicabilidad con los datos del proyecto.

### Pisos turísticos

- **LA01 García-López, Jofre-Monseny, Martínez-Mazza, Segú (2020), JUE 119, 103278.** Q1. Efecto de Airbnb en barrios de Barcelona · IV shift-share, event studies · alquileres +1,9 % (media), +7 % (decil superior); precio de transacción +4,6 % y +17 % (decil superior). Replicabilidad parcial: VUT GVA, fianzas y valor tasado en València ciudad, falta microdato Airbnb por barrio.
- **LA02 Chaves-Fonseca (2026), SERIEs (en línea).** Q2. Madrid 2010-2018 · panel barrio-año, IV shift-share · +100 anuncios de vivienda entera: ≈50 entradas residenciales menos al año (≈2 %), precios ≈ +2 %. Replicabilidad parcial.
- **LA03 Mozo Carollo et al. (2023), Urban Research & Practice 17(2), 260-279.** Q1. San Sebastián · +1 anuncio por 100 viviendas: +49,45 euros/mes sobre ≈1.284,20 · identificación no extraída. Replicabilidad parcial.
- **LA04 Hidalgo, Riccaboni, Velázquez (2024), J. Regional Science 64(3), 621-648.** Q1. Madrid, IV · resultado de amenidades (restaurantes), no de vivienda. Tangencial. No replicable.
- **LA05 García-Amaya et al. (2021), Int. J. Tourism Cities 7(2), 361-390.** Cuartil no verificado. València (Russafa, El Cabanyal) · descriptivo con trabajo de campo · sin magnitudes. Replicabilidad parcial (distribución espacial de VUT).
- **LA06 Taltavull de La Paz et al. (2023), Cities 134, 104148.** Q1. 39 ciudades europeas 2015-2020, VECM sobre alquiler turístico · co-movimiento oferta-demanda-precio · sin cifras. Replicabilidad parcial.
- **LA35 Cátedra Economía Colaborativa UV (2022) / pericial Aptur CV (vía prensa).** NO VERIFICADA, sin DOI; hipótesis: +0,056 % por +1 % de anuncios; ≈1,8 % del aumento del alquiler.

### Inmigración y demografía

- **LA07 Sanchis-Guarner (2023), RSUE 100, 103893.** Q1. España 2001-2012, IV · separa demanda directa de inmigrantes y reubicación de nativos · ignorar la reubicación cambia de forma sustancial el efecto total (magnitud no extraída). Replicabilidad parcial.
- **LA08 González y Ortega (2013), J. Regional Science 53(1), 37-59.** Q1. España 2000-2010, IV de asentamientos · ver «Actualiza» arriba. Replicabilidad sí (falta instrumento).
- **LA09 Saiz (2007), JUE 61(2), 345-371.** Q1. +1 % de población por inmigración: alquileres y valores ≈ +1 %.
- **LA34 Sá (2015), Economic J. 125(587), 1393-1424.** Q1. Reino Unido · IV · negativo (−1,6 % por +1 % de población según el DP IZA 5893, no comprobado en la versión publicada).
- **LA26 Torres-Téllez y Montero-Soler (2023), CyTET 55(215), 47-60.** Cuartil no verificado. 50 provincias 2001-2019, siguiendo a Saiz · +2,5 % en la burbuja, −1,12 % tras la crisis, neto negativo; inmigración 2010-2019: +5,9 % en alquiler.
- **LA28 Módenes, Marcos, García-García (2024), Estudios Geográficos 85(297), 1163.** Q3. Descomposición demográfica de los hogares · la oferta responde cada vez más a mínimos del ciclo demográfico.

### Formación de hogares y emancipación

- **LA27 Soler Montero, Torres-Téllez, García Ayala (2023), Panoeconomicus 70(3), 429-454.** Q2. VAR 1995-2017 · la emancipación cae unos dos trimestres tras un shock negativo y se recupera rápido; paro pesa más a corto plazo, temporalidad a largo plazo.
- **LA29 González-Val (2022), Sustainability 14(5), 2848.** Q1. 50 provincias (1995-2018) y 282 ciudades (2005-2018) · relación inversa fuerte entre precio y nupcialidad; coeficiente no extraído.
- **LA20 Khametshin, López Rodríguez, Pérez García (2024), BdE DO 2432.** Subida del alquiler desde 2015; expansión de la demanda concentrada en jóvenes y población de origen extranjero.
- **LA19 Lajer Baron, López Rodríguez, San Juan (2024), BdE DO 2433.** Déficits provinciales; Madrid y Barcelona ≈ un tercio.

### Oferta, suelo, licencias y costes

- **LA10 Saiz (2010), QJE 125(3), 1253-1296.** Elasticidad media 1,75 ponderada; < 1 en ciudades restringidas.
- **LA11 Glaeser y Gyourko (2018), JEP 32(1), 3-30.** Ensayo; brecha precio-coste como impuesto regulatorio; cifras no citadas.
- **LA16 San Juan (2023), BdE Boletín 2023/T2.** La demanda se recuperó antes que la oferta; precios más altos donde la escasez relativa es mayor.
- **LA18 BdE, Informe Anual 2025.** Elasticidad ≈0,45; déficit ≈750.000 (3,7 % de los hogares).
- **LA21 OCDE (2025), Economic Surveys: Spain.** DOI verificado; contenido de vivienda NO leído en el original (oecd.org 403); cifras de resumen de buscador: 345.000 licencias 2022-2024 frente a 604.000 hogares netos, licencias hasta 2 años, alquiler social ≈3 %.
- **LA30 Koumpias et al. (2021), Applied Economic Analysis 30(89), 132-150.** Q2 (fuentes discrepan). IV con cajas de ahorros; +1 % de precio: +3,9 p. p. en probabilidad de corrupción urbanística.
- **LA31 Solé-Ollé y Viladecans-Marsal (2012), J. Public Economics 96(1-2), 10-19.** Q1. Oferta local de suelo y lobbying (>2.000 municipios, 2003-2007).
- **LA32 Caldera y Johansson (2013), JHE 22(3), 231-249.** Q2. Origen de la elasticidad ≈0,45.

### Crédito, tipos y expectativas

- **LA12 Kaplan, Mitman, Violante (2020), JPE 128(9), 3285-3345.** Q1. El cambio de creencias es el principal impulsor.
- **LA15 Martín, Moral-Benito, Schmitz (2021), AER 111(3), 1013-1053.** Q1. España · el boom desplazó primero el crédito a empresas no inmobiliarias y luego lo estimuló.
- **LA25 Koeniger, Lennartz, Ramelet (2022), EER 145, 104107.** Q1. Alemania, Italia, Suiza · transmisión a hipotecas fijas ≈2 veces mayor en Alemania y Suiza que en Italia. España ausente.
- **LA33 Gimeno y Martínez-Carrascal (2010), J. Banking & Finance 34(8), 1849-1855.** Q1. VECM: solo los precios corrigen el desequilibrio.
- **LA24 Vansteenkiste y Hiebert (2011), JHE 20(4), 299-314.** Q2. GVAR de contagio en la zona euro (resultado no extraído; anterior a 2018).

### Burbujas y exuberancia

- **LA13 Phillips, Shi, Yu (2015), IER 56(4), 1043-1078.** Q1. GSADF; método.
- **LA14 Pavlidis et al. (2016), JREFE 53(4), 419-449.** Q1. GSADF aplicado a vivienda (cobertura y resultado no extraídos).
- **LA17 Cáceres (2024), BdE Economic Bulletin 2024/Q3.** Precios cercanos al equilibrio con datos hasta 3T2023; AUROC no extraído.

### Factor común europeo

- **LA22 Ghirelli, Leiva-León, Urtasun (2023), SERIEs 14(2), 165-187.** Q2. Convergencia de ciclos entre ciudades españolas, máximo en 2009.
- **LA23 Maynou, Monfort, Morley, Ordóñez (2021), Economic Modelling 103, 105595.** Q1. Clubes de convergencia en precios europeos; resultado no extraído.
- **LA24, LA25**: ver crédito.

## Lagunas

- Sin estudio revisado con identificación causal para Airbnb en la Comunitat Valenciana (solo LA05 descriptivo) ni evidencia revisada sobre la elasticidad en València.
- Sin trabajo revisado sobre transmisión de tipos a precios de vivienda con España en la zona euro (Koeniger et al. 2022 no la incluye); Albertazzi, Fringuellotti y Ongena (EER 161, 104643) y Benetton, Gavazza y Surico (AER 115(3)) localizados pero no leídos, no incluidos. Pica (BCE, ARM y propiedad en la zona euro, España entre los más sensibles, según un resumen de búsqueda) es presentación/póster: no verificado.
- Factor común europeo: sin artículo con un factor común explícito para precios europeos 2018-2026 verificado (OpenAlex dio 429 en la última consulta). Pendiente: BIS/BCE.
- Informe Anual 2024 del BdE y otros números del Boletín no consultados.
- Resultados numéricos de LA07, LA14, LA23, LA24, LA29 pendientes de leer el texto.

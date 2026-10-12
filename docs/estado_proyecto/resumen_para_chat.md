# Vivienda en España: estado del proyecto v1-v6.2 (resumen para diseñar la V7)

Proyecto reproducible de Borja Romero, economista, sobre precios, alquileres, oferta y necesidad de vivienda en España. El estado es el del 12-10-2026, en el commit 462ebf1 (cierre de v6.2).

Todo se reconstruye sin red con `make all`, que tarda unas 2 h 10 min en un solo hilo. Dos ejecuciones en un clon limpio dan md5 idénticos. `make check` tarda unos 6 min y pasa 89 tests más tres comprobadores:
- de texto: léxico valorativo y lenguaje causal;
- de cifras: fuera de marcador y sumas provinciales;
- de sellado.

Las cifras publicadas salen de una sola tabla, `output/v5/cifras_clave.csv`.

**Capas de evidencia.**

| Capa | Significado |
|---|---|
| C1 | Hecho con dos o más fuentes que coinciden (±15 %) |
| C2 | Cota con supuestos explícitos |
| C3 | Efecto identificado; **ninguno alcanzado** |
| C4 | Exploratorio |

Por debajo de C3 no se usa lenguaje causal, y las importancias de ML no se leen como efectos.

## 1. Repositorio y herramientas

| Elemento | Estado |
|---|---|
| Versiones cerradas (commit) | v4 9673a4c; v5.0 cc69e02; v5.1 bac2fda; v6.0 08d7629; v6.1 7a63f9f; v6.2 462ebf1 |
| Etiquetas | prereg-v2/v3/v5/v6 y v5.0-v6.2, **solo locales**: el remoto rechaza las etiquetas |
| Makefile | all = data → clean → models → report; check; verificador. Órdenes por versión: V3, V4, V5, V6, V6_2 y V6_1 |
| Utilidades | `econ_utils.py`: DOLS, HAC, Chow, Bai-Perron, DM, Holm y `Registry` (registro de especificaciones). `holdout.py`: sellado y apertura única registrada (`sellar_v6`, `evaluate_v6`). `check_texto`, `check_v5`, `check_v6` y `render` (plantillas → entregables) |
| Librerías | statsmodels 0.15, linearmodels 7.0, lightgbm 4.7, xgboost 3.4, shap 0.53, econml 0.17, doubleml 0.11, torch 2.14 (CPU), sklearn 1.9, pandas 3.0, Python 3.13 |
| No instaladas | pymc/arviz, numpyro/jax, arch, pysal/spreg, torch_geometric y bartpy. En v6, BART y el modelo jerárquico se sustituyeron por un bosque con bootstrap bayesiano y por MixedLM; la GNN, por una implementación propia |

## 2. Datos

**Fuentes principales** (unos 110 ficheros raw y 18.090 series del INE):
- **INE:**
  - IPV T 2007-2026T2 (nacional y CCAA);
  - EPA T 2002-2026T1 (nacional, CCAA y provincia);
  - ETDP M 2007-2026-07 (CCAA y provincia);
  - IPC alquiler M 2002-2026-08 (provincia);
  - IPVA A 2011-2024 (hasta municipio);
  - ECP y padrón A 2002-2026 (provincia), con hogares desde 2021;
  - Migraciones por provincia A 2008-2022;
  - CRE (PIB) A 2000-2025 (CCAA y provincia);
  - hipotecas M 2003-2026 (provincia);
  - VUT experimental M 2020-08 a 2026-05 (hasta sección).
- **MIVAU:**
  - valor tasado T 1995-2026T2 (hasta 309 municipios);
  - transacciones notariales, con las de extranjeros, T 2007-2026;
  - visados e iniciadas y terminadas M 2008-2026 (CCAA), A 1991-2026 (provincia).
- **SERPAVI** (MIVAU-AEAT): alquiler de stock A 2011-2024, de nacional a sección censal.
- **BCE y BdE:** tipo hipotecario, crédito nuevo y stock, Euribor (nacional, mensual).
- **Eurostat:** costes, permisos, renta y HPI (nacional).
- **Notariado y Registradores:** extraídos de PDF y XLSX; nacionales, más la Comunitat Valenciana en el caso del Notariado.
- **Catastro:** unidades residenciales A 2011-2025 (municipio).
- **Fianzas:** Incasòl (Cataluña, 2007-2026) y GVA (C. Valenciana, 2020-2026).
- **Eventos regulatorios:** 41 eventos y 318 declaraciones de zona tensionada, recogidos a mano.

**Panel trimestral por CCAA** (`data/processed/panel_ccaa_q.csv`, 17 CCAA, 1995T1-2026T2), desde 2007:

| Situación | Variables |
|---|---|
| Completas (0 % NaN) | IPV (general, nueva, usada), ocupados EPA, compraventas ETDP, transacciones de extranjeros, IPC alquiler, población EPA |
| Huecos menores | Valor tasado (1 %), transacciones totales (2 %, hasta 2026T1), terminadas (5 %, desde 2008), visados o iniciadas (8 %, desde 2008) |
| Interpoladas | Población total y extranjera: dato anual interpolado loglineal, hasta 2025T1 |
| **No existen en T por CCAA** | PIB y renta (solo anual); hogares (solo nacional, desde 2021); tipo hipotecario y crédito (nacional; hipotecas provinciales mensuales sin agregar); paro (derivable de la EPA, no integrado); costes y licencias; SERPAVI e IPVA (anual); compraventas al contado; VUT antes de 2020; llegada neta (semestral desde 2023); eventos regulatorios como dummy (hay que construirla) |

**Panel anual provincial.**
- v2: 2002-2023, con 49 provincias en los paneles de entrenamiento, porque excluyen las 3 selladas en v2.
- v6: 2015-2024, con 41 provincias, porque excluyen las 11 selladas en v6.
- Variables: valor tasado, IPC alquiler, ocupados, parados, población y extranjeros, hipotecas, PIB por habitante, VUT y SERPAVI.
- Con huecos: suelo (14 %), compraventas (23 %), terminadas libres (30 %), iniciadas (39 %).
- **Sin dato provincial:** renta, costes, licencias, Notariado (salvo la C. Valenciana) y Registradores.

**Fuentes fallidas o pendientes.** Licencias de obra (MIVAU), SIU (suelo), titularidad del Catastro, IRPF municipal, fianzas de Madrid, Euskadi y Baleares, Registro Único de Arrendamientos, renta trimestral y portales privados. Hay diez solicitudes de transparencia (S1-S10) redactadas y no presentadas.

## 3. Modelos estimados (resumen)

| Versión | Modelos principales | Nivel | Resultado clave | Estado |
|---|---|---|---|---|
| v1 | DOLS ±2, ECM, EG, Johansen, ARDL bounds (precio real) | nacional T 2008-2025 | Ocupados en el largo plazo +1,48 (p<0,001); el ECM no mejora al AR(4) (DM p 0,29-0,51) | matizado |
| v1 | Panel IV shift-share; FE; CCE-MG y CCE-P; CIPS | CCAA (17), 2008-2025 | IPC alquiler: MCO 0,53, 2SLS 0,44 (n.s.); cuota de extranjeros en IPV n.s.; CIPS: ln IPV I(1) | matizado |
| v1 | DOLS de oferta (iniciadas ~ precio real) | nacional | Elasticidad 1,44 [1,04; 1,85] | descriptivo |
| v2 | FE provincia (H1 demografía, H2 crédito y coste de uso, H3 inmigración 2SLS, H4 oferta, H5 SDiD del tope catalán, H6, H7 ML/TVP) | provincia (49), T 2002-2024 | Holm-7: solo H6 se acerca (0,098); H1 supera al AR(4) en el sellado; el ML no supera al AR(4) | matizado |
| v3 | FE y shift-share VUT (sección), DiD topes (municipio), réplica de García-López, Manski, simulación de políticas | sección, distrito, municipio | Ninguno C3; topes −5,4 % en contratos nuevos, con pretendencias fallidas; cota VUT de 2,4-2,7 % del stock | C4 / C2 |
| v4 | Conciliación del déficit, Shapley de hogares, brecha Glaeser-Gyourko, matriz de instrumentos, GSADF | nacional, CCAA y provincia | GSADF nacional rechaza; por CCAA, ninguna | C4 |
| v5 | Necesidad B1 (A+R+V+F−M−K), déficit B2, clases A4, B3 (8 familias), traslado D1, convergencia D3, R1A-C | provincia (52), nacional | Necesidad unos 210.000 viviendas al año (99.000-292.000, C4) | C4 |
| v5.1 | Bajas (T1), liberadas (T2), recálculo (T3), escenarios (T4) | provincia | Las liberadas nunca se restan | C4 |
| v6 | TWFE/CCE/SDM (M1), BMA, elastic net y PDS (M2), RF/GBM/MLP/GNN, bosque bayesiano y MixedLM (M3), sellado (M4), GSADF por CCAA, ADL, DOLS | provincia, municipio y distrito, 2015-2024 | Ningún coeficiente sobrevive al ajuste; ninguna hipótesis confirmatoria pasa Holm | C4 |
| v6.1 | K1: líneas base exigentes (DM-HLN más permutación exacta); K2: inmigración, una dimensión cada vez; K3: retardos y adelantos de iniciadas | sellado v6 | ML mejor que la base más exigente en 6 de 9 tareas (alquiler de stock, precio trimestral) | C4 |
| v6.2 | L3: déficit con 8 correcciones de la EPA × 3 fuentes de terminadas | nacional | Déficit 2021-2024: 389.361-710.542 (C2) | vigente |

**Qué no se ha estimado nunca.**
- PMG ni DFE.
- Cointegración de panel (Pedroni, Westerlund): en v6 se descartó porque T anual = 9.
- MG solo en v6, como robustez.
- CIPS solo en v1, como raíz unitaria por CCAA.
- Durbin espacial: solo un SDM en v6 M1B, sin conclusión.
- Ningún panel dinámico heterogéneo en el CCAA trimestral.

## 4. Validaciones y muestras contaminadas

| Sellado | Unidades | Periodos | Aperturas | Comentario |
|---|---|---|---|---|
| v2 | provincias 11, 16 y 45 (Cádiz, Cuenca, Toledo) y todas en el tramo temporal | 2024T3-2026T2; anual ≥2025 | 8 (H1-H7) | paneles provinciales, nacional y UE |
| v3 | 20 % de los distritos (bloques espaciales); última oleada VUT 2026M05 | 2026M05 | sin registro propio | P-C3 sin muestra espacial limpia |
| v6 | 11 provincias (07, 22, 26, 28, 30, 31, 33, 35, 38, 44 y 50: CCAA de Baleares, Aragón, Asturias, Canarias, Madrid, Murcia, Navarra y La Rioja) y sus municipios y distritos | compra 2025, alquiler 2024 | 80 (53 M4 y 27 K1, segunda mirada) | el último año cae en la ventana de v2 |

**Clave para V7.**
- El **panel CCAA trimestral nunca se selló y v1 lo usó entero**: no tiene muestra limpia.
- Las provincias no selladas estuvieron siempre en el entrenamiento.
- **Validación limpia:** solo **datos publicados después de pre-registrar V7** (2026T3 en adelante; 2026 en anuales).
- **Informativa pero no limpia:** dejar fuera CCAA nunca selladas (Cantabria, Castilla y León, Cataluña, C. Valenciana, Extremadura, Galicia, País Vasco), declarándolo como «ya visto en v1».

## 5. Resultados vigentes

**Cifras aptas para difusión** (v6.2):

| Cifra | Valor | Capa |
|---|---|---|
| Aumento de hogares 2021-2025 | 997.586 (981.823-1.013.350) | C1 |
| Viviendas terminadas al año 2019-2024 (territorio común) | 72.264-94.426 | C1 |
| Déficit 2021-2024 sin bajas | 389.361-710.542 (sin las variantes que conservan el salto de la EPA, 596.371-710.542) | C2 |
| Precio de compra 2015-2025 (MIVAU, Notariado, Registradores) | +47,2 % (44,2-56,1) | C1 |
| Alquiler de contratos vigentes 2015-2024 | +10,9 a 22,9 % | C1 |
| Contratos nuevos 2021-2024, C. Valenciana | +28,5 % (26,1-30,8) | C1 |
| Contratos nuevos 2021-2024, Cataluña | +16,9 % (16,6-17,2) | C1 |
| Hogares proyectados 2026-2035 (INE) | 1,31-1,77 M | C2 |
| Hogares propietarios | 74,5 % (72,1-75,9) | C1 |

**No citar fuera de contexto (C4).**
- Necesidad de unas 210.000 viviendas al año (99.000-292.000).
- Traslado de ayudas a precio: 58 % en la clase A4-1 y 100 % en la A4-2 (rejilla εd 0,3-1,5).
- Asociaciones de inmigración: total en compra +4,3 % por punto de cuota; directa, a igual población, −1,3 (IC −4,3 a 1,7). Controlar por población es un mal control.
- Déficit con bajas estimadas: 389.361-765.994.

**Conclusiones por tema** (capa vigente):

| Tema | Conclusión |
|---|---|
| Inmigración | El signo y el mercado dependen del método (2SLS frente a MCO), de la medida de alquiler y de los controles. C4, «analizada, no concluyente» |
| Empleo y renta | Positivos en algunas especificaciones, sin robustez (C4) |
| Oferta | Las iniciadas responden al precio (elasticidad 0,8-1,4, C4). Las iniciadas se asocian con el alquiler del mismo año, sin orden temporal (C4) |
| Turísticos | Signo inestable; cota máxima de stock desplazado del 2,4-2,7 % (C2) |
| Topes de alquiler | −5,4 % en contratos nuevos de Cataluña, con pretendencias fallidas (C4); en el stock, no concluyente |
| Tipos y crédito | Sin efecto de largo plazo detectable; sin valor predictivo en el sellado (C4) |
| Exuberancia | GSADF nacional rechaza; ninguna de 11 CCAA (C4) |
| Precio/alquiler | El ratio pasa de unos 20 años (2015) a unos 17 (2023), según la medida; elasticidad precio-alquiler 0,4-2,1 (C4) |
| Predicción | Los árboles superan a la base más exigente en alquiler de stock y en precio trimestral; ninguna variable es «relevante con seguridad» |

**Resultados regionales que ya existen.**
- **Por CCAA:** GSADF (11 CCAA), panel v1 (FE, CCE e IV, 17 CCAA) y conciliación de precios A23.
- **Por provincia:** clases A4 (52), necesidad B1, déficit B2/T3/T4, coeficientes M1A/M1B (n.s. tras ajuste), PIP de M2 y SHAP de M3B.
- Por municipio y distrito: alquiler SERPAVI y predicción.

## 6. Política

- **Método.** Rúbrica determinista: incidencia = |εd|/(εs+|εd|) por clase territorial A4, con εd en una rejilla de 0,3 a 1,5. εs procede de la respuesta de oferta de A4 (método A) o de la rejilla de P-D (método B), y se reportan ambos. Las elasticidades vienen de la literatura, en parte VERIFICADA.
- **Clases A4 por provincia** (2021-2025): 37 en la clase 1 (falta vivienda y es rentable construir), 11 en la 2 (la oferta no responde), 2 en la 3 y 2 en la 9.
- **Resultados.** Traslado al precio: clase 1, 28-82 %; clase 2, 88-100 %; clase 3, 50-90 %.
- **Instrumentos.** La matriz tiene 37 (I01-I29, N1-N9, P1). Signo estable en I02/N8, I06, I07, I08/N9, I10/N7, I27 y P1. 18 quedan sin signo evaluable, y I17 e I23 sin definición. No se han evaluado los impuestos a la construcción ni la rebaja del ITP o el IVA.

## 7. Calidad

- **ERRATA** (11 entradas). Las principales:
  - el déficit 2021-2024 pasó de C1 562.692-688.692 a C2;
  - A23-A10 pasó del 26,6 % al 28,5 % (fallo de cruce por nombre y de relleno);
  - recuentos redondeados a 6 cifras;
  - fianzas de Incasòl triplicadas;
  - ventana del Censo en B1.
- **Errores recurrentes:**
  - cruces por nombre con tildes («Valéncia»);
  - `fillna` silenciosos;
  - redondeos al escribir;
  - fechas tomadas como texto o fecha de ejecución dentro de las salidas;
  - ventanas desalineadas (stock a 1 de enero frente a media anual);
  - dobles conteos de agregados.
- **Pendientes medios:**
  - min y max con otro sentido en 48 filas de cifras_clave;
  - fianza media GVA bruta o truncada;
  - 26 cifras del verificador fuera de cifras_clave;
  - cuartiles de Scimago por verificar (50 «cuartil no verificado», 76 NO VERIFICADA);
  - D2 por recalcular con T3.
- **Objeciones de los árbitros simulados no resueltas:**
  - muestra futura nueva;
  - intervalos Anderson-Rubin en shift-share;
  - WCB en paneles municipales;
  - recuento de especificaciones entre versiones;
  - ecuaciones del método de traslado;
  - costes por euro.
- **Incidencias abiertas del inventario:**
  - el DM del ECM de v1 aparece con dos valores (0,29 y 0,51);
  - en v3 C3 H3-3b el IC incluye el 0 pero el p ajustado es 0,0002.

## 8. Consumo

Tokens de subagentes:

| Versión | Tokens |
|---|---|
| v2 | 4,9 M |
| v3 | 2,1 M |
| v4 | 1,5 M |
| v5 | 3,1 M |
| v5.1 | 0,66 M |
| v6 | 1,54 M |
| v6.1 | 1,13 M |
| v6.2 | 0,46 M |
| Inventario | 0,51 M (pedido: 0,25 M) |

Cada `make all` tarda unas 2 h 10 min; v6 M3 (ML) ocupa la mayor parte.

## 9. Recomendaciones para V7 (modelos regionales)

1. **CCAA trimestral, 2007T1-2026T2 (17 × unas 78 T).** Es la base natural. Con T larga son viables:
   - PMG, MG y DFE para la relación de largo plazo de precio y alquiler con fundamentales;
   - cointegración de panel (Westerlund con bootstrap, Pedroni);
   - CS-ARDL o CCE-ECM;
   - proyecciones locales de panel ante shocks nacionales de tipos y crédito.

   Antes hay que ampliar el panel con: paro CCAA de la EPA, hipotecas CCAA agregadas desde la serie provincial mensual, dummies regulatorias desde v2_eventos, y renta y PIB anuales repartidos solo como control.
2. **Provincia anual (52 × 2002-2024) y trimestral (2002-2024T2).** Paneles FE o CCE con flujos: padrón, EPA, ETDP, hipotecas, iniciadas y terminadas. SERPAVI solo desde 2011.
3. **Riesgos.**
   - Con 17 clusters hacen falta WCB (Webb), Driscoll-Kraay y CCE.
   - La potencia por CCAA en MG/PMG es baja.
   - La historia acumula miles de especificaciones: pre-registro, Registry y Holm/BH por familia.
   - Hay colinealidad entre población, extranjeros y empleo (cuota y población correlacionan 0,66).
   - Rupturas: EPA 2021, COVID, bases del IPV.
   - Dependencia transversal por shocks nacionales comunes.
4. **Validación nueva.** Pre-registrar V7 con fecha verificable (release o DOI) y evaluar con los datos que se publiquen después (2026T3-2027T2), en tiempo pseudorreal. Comparar siempre con AR(4), ECM v1 y las bases exigentes de K1.
5. **Presupuesto.** Entre 0,8 y 1,2 M tokens de subagentes:

   | Bloque | Tokens |
   |---|---|
   | Datos | 0,15 |
   | Pre-registro y potencia | 0,1 |
   | Panel CCAA (PMG/MG/DFE, cointegración, CS-ARDL) | 0,25 |
   | Provincia | 0,2 |
   | Predicción | 0,15 |
   | Revisión y cierre | 0,15 |

   No conviene confiar síntesis con tope estricto a subagentes pequeños.

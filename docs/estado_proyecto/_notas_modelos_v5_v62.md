# Notas de inventario: modelos v5, v5.1, v6, v6.1 y v6.2

Fecha de la lectura: 2026-10-12. Tarea de solo lectura. No se ha ejecutado ningún modelo, no se ha leído `data/sealed` y no se han modificado ficheros del proyecto. Fuentes: `output/*/resultado.json` (esquema común: rama, pregunta, capa, datos, N, metodo, estimacion, ic95, p_ajustado, nivel_evidencia, diagnosticos, fuera_muestra, notas) y los ficheros de tabla citados en cada apartado.

**Discrepancias con la lista pedida:**
- Existen `output/v5/A6`, `output/v5/R1T`, `output/v6/M0`, `output/v6_1/K4A-K4C` (K4D es carpeta sin `resultado.json`), `output/v6_2/L1` y `L2`. No se listan en la petición y se incluyen abajo.
- `output/v5_1` tiene T1, T2, T3, T4 y T6. **No existen T5 ni T7** (ni carpeta con `resultado.json`).
- Los ficheros pedidos `tabla_modelos.md`, `mejor_modelo.csv` existen en `output/v6/M4/`. `peso_variables.md` existe en `output/v6/M2/`.

---

## 1. Modelos por versión

Leyenda de «p»: p bruto / p ajustado (Holm, BH o wild bootstrap según indique el registro). «FM» = fuera de muestra.

### 1.1 v5 (entregables; `output/v5/*/resultado.json`)

| Familia | Pregunta | Mercado / nivel | N | Dependiente y transformación | Regresores / retardos | Estimador | EE | Coeficientes principales, p bruto / ajustado | Diagnósticos | FM (RMSE, base, DM) | Estado | Ruta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R1A | Peso inicial de no residentes extranjeros y subida de precio provincial 2015-2025; conciliación VUT | Compra; provincia (corte) | 50 unidades BK-002 (43 provincias) | Δln precio provincial | Peso no residentes (pp); controles en E2 | MCO corte transversal, 8 especificaciones, bootstrap 2000 | HC3 | Bivariada 0,0096 por pp, IC [0,0046; 0,0147], p ajustado Holm 0,0015. Con controles 0,0002, p ajustado 1,0. | R2 aj. 0,60; Pearson 0,56; Spearman 0,56 | No aplica (corte) | Cerrado; C4 | `output/v5/R1A/` |
| R1B | Donut post-COVID (BK-041); multiverso (BK-040); GSADF con tamaño corregido (BK-023) | Municipal (306 municipios >25k hab. tasado; 2.668 SERPAVI) | Donut 128 y 6; multiverso 320 | Crecimiento anual de precio; GSADF sobre ratio | Distancia a área (FE) | Diferencia de pendientes; GSADF | Agrupados por área | Multiverso: 77 % de especificaciones con diferencia positiva; ninguna significativa tras Holm (320 espec.) | Permutaciones B=200 | No aplica | Cerrado; C4 | `output/v5/R1B/` |
| R1C | Propiedad de la vivienda; capacidad de construcción | Nacional y CCAA (34 celdas) | 34 | Tabulación; ratio ocupados/iniciadas | No aplica | Descriptivo, Spearman entre CCAA | No aplica | Tenencia total 74,5 % (C1); Spearman Holm 0,0055 | 8 celdas sin dato | No aplica | Cerrado; C1 (tenencia) / C4 (resto) | `output/v5/R1C/` |
| R1T | Pendientes técnicos (cruce SERPAVI-distritos) | Valencia, distritos | 19 | No aplica | No aplica | Cruce de códigos | No aplica | No aplica | Supuesto: distritos censales = distritos municipales | No aplica | Técnico | `output/v5/R1T/` |
| A23 | Conciliación precio: IPV INE frente a núcleo MIVAU/Notariado/Registradores; alquiler (A2, A3) | Nacional, CCAA y provincia | 11 años de precio; 17 CCAA | Variación acumulada de medias anuales | No aplica (puente) | Puente en log con pesos Laspeyres | No aplica | IPV +79,9 %; núcleo +44,2 a +56,1 % (mediana 47,2 %); efecto nueva/usada 0,004 pp | Independencia entre fuentes documentada | No aplica (descriptivo) | Cerrado; C1 (núcleo) / C4 | `output/v5/A23/` |
| A4 | Dónde falta vivienda y es rentable construir con el coste oficial | Provincia (52) y municipio (703) | 52 / 703 | Clase por rejilla coste × margen × tipo × edificabilidad × suelo | No aplica | Clasificación determinista (MBC 1993 actualizado con Eurostat) | No aplica | Rango coste 421,8-932,1 €/m²; provincias 2021-2025 por clase: clase 1 = 37 (8 robustas), clase 2 = 11 (3), clase 3 = 2, clase 9 = 2 | Reconciliación provincia-nacional cuadra | No aplica | Cerrado; C4 (regla B5) | `output/v5/A4/` (`clasificacion_provincias.csv`, `clasificacion_municipios.csv`) |
| A5 | Instrumentos en documentos oficiales programáticos y normativos | Documentos (22) | 22 documentos, 1.099 coincidencias | Recuento de palabras clave | No aplica | Recuento con diccionario trilingüe | No aplica | No aplica (recuento, no medida validada) | Validación de precisión parcial | No aplica | Cerrado; C4 | `output/v5/A5/` |
| A6 | Topes fuera de C3; no replicación de García-López | Nacional | n/d | Stock frente a flujo | No aplica | Consolidación documental de v4 M0 | No aplica | Atenuación stock-flujo 0,55-0,75; β −0,0042, IC [−0,0078; −0,0005], p ajustado 0,27 | No aplica | No aplica | Cerrado; C4 | `output/v5/A6/` |
| B1 | Necesidad de vivienda 2026-2035 (A+R+V+F−M−K; L ya neta en F) | Provincia (52) y nacional | 52 | Necesidad anual en viviendas, rango min-central-max | Componentes de fuente | Suma por componentes | Rango, no EE | Central nacional 214.868 viviendas/año (93.628-309.921); 48 provincias con presión; 4 con R en un solo método | Control de sumas sin fallos | No aplica | Cerrado; C4 | `output/v5/B1/` |
| B2 | Déficit 2021-2030 por provincia (D2030 = D2025 + F − T + B) | Provincia (52) y nacional | 52 | Déficit en viviendas | F, T (3 escenarios), B | Proyección contable | Rango | Déficit 2025 nacional 700.934; 2030 central 1.296.672 (872.529-1.447.953) | Control de sumas | No aplica | Cerrado; C4 | `output/v5/B2/` |
| B3 | Ocho familias de determinantes a la vez (Bartik, población, etc.) | Transversal, provincia/municipio | 50 (principal Y1-P1); 46-47 otros | Δ log de precio por unidad de DT | 13 regresores estandarizados | MCO conjunto; Shapley | HC3 y Conley (100 y 200 km) | H-B3-1 (Bartik) b 0,0236 por DT; IC [−0,0006; 0,0479]; Holm 8 familias 0,335; Holm 3 confirmatorias 0,112 | R2 0,912; R2 aj. 0,880; LOO-CV RMSE 0,066 | LOO-CV (no aplica embargo) | Cerrado; C4 (descriptivo) | `output/v5/B3/` |
| B4 | Triangulación de salidas v2, B3 y otras (contribuciones) | Nacional y CCAA | 71 entradas, 29 huecos | Pp de Δln, cuotas de R2 | No aplica | Triangulación | No aplica | Contribuciones no estables entre ventanas | Ventanas desplazadas | No aplica | Cerrado; C4 | `output/v5/B4/` |
| CA | Posición de España en la UE-27 y regresiones descriptivas de precio; ADL(4) para predicción | Europa (10 indicadores), crédito (6 trimestres) | 10 / 6 | Percentil y desviación frente a la mediana | ADL(4) + crédito construcción + inmob. (retardo 4) | Descriptivo; ADL 1 paso, ventana expansiva, embargo 4 | No aplica | Holm sobre 36 pruebas, mínimo 0,032 | RMSE 0,141 frente a AR(4) | ADL frente a AR(4) (DM) | Cerrado; C4 | `output/v5/CA/` |
| CB | Correlación de usurpación con alquiler (Spearman, permutación 10.000) | CCAA (17) y secciones censales (36.333) | 17 | Spearman (ρ) | Usurpación por 100k; porcentaje de alquiler | Spearman con permutación | No aplica | C5-S2 ρ 0,66, p 0,006, p Holm 0,038; C5-S1 ρ 0,57, p Holm 0,074 | Seed 20261010; fechas distintas Censo/AEAT/ECV | No aplica | Cerrado; C4 | `output/v5/CB/` |
| CC | Sobrecarga de costes y cotas de salidas 2026-2035 (plazo-calificación) | Grupos de hogares | 11 años de sobrecarga | Cambio en pp 2015-2025; cota de salidas | No aplica | Descriptivo + convolución en 3 escenarios | No aplica | Cambio 2015-2025 pp: QU1 −13,2; RENT_MKT −16,5; OWN_L −5,3 | Cuadre suma CCAA-nacional máx. 6.024 | No aplica | Cerrado; C7 descriptivo, C2 cota | `output/v5/CC/` |
| D1 | Traslado a precio de ayudas por instrumento (36 instrumentos, 52 provincias) | Provincia por clase A4 | 36 × 52 | Incidencia \|εd\|/(εs+\|εd\|) | No aplica | Rúbrica determinista | No aplica | Traslado clase A1 min/central/max 27,8 / 58,4 / 81,8 %; clase A2 88,1 / 100 / 100 %; clase A3 50,1 / 76,4 / 89,8 % | Métodos A y B reportados ambos | No aplica | Cerrado; C4, signos en C2 | `output/v5/D1/` |
| D2 | Cruce de necesidad, déficit y política por territorio | Provincia y clase | 52 | Cobertura de P-D y vacías (%) | No aplica | Cruce de tablas; reparto por cuota de necesidad (supuesto) | No aplica | Clase 1: cobertura P-D 11,6-46,5 %; vacías 30,2 %. Necesidad anual 214.868 | Control de sumas: todo OK | No aplica | Cerrado; C4 | `output/v5/D2/` |
| D3 | Comparación de rangos con referencias externas | Nacional | 22 | Coincide / difiere | No aplica | Regla de solape o diferencia ≤15 % | No aplica | Coincide 2; difiere 1; comparable en parte 6; no comparable 9 | 4 referencias no localizadas | No aplica | Cerrado; descriptivo | `output/v5/D3/` |

### 1.2 v5.1 (`output/v5_1/T1-T6`; T5 y T7 sin fichero)

| Familia | Pregunta | Mercado / nivel | N | Dependiente | Regresores / retardos | Estimador | EE | Resultados principales | Diagnósticos | FM | Estado | Ruta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | Bajas netas del parque 2011-2025 (4 fuentes: identidad censal, Catastro, demoliciones) | Provincia (52) | 52 provincias; 13 años B | Tasa anual de bajas | No aplica | Cálculo contable; t de una muestra con Holm (solo descriptivo) | No aplica | Tasa nacional 2015-2024: central 2,56 %/año (rango 0,00-5,18 %); identidad censal −0,33 % (por discrepancia de signo, no concluyente) | Las fuentes no coinciden dentro del margen | No aplica (AR(4) y ECM no aplican) | C4 | `output/v5_1/T1/` |
| T2 | Viviendas liberadas por envejecimiento 2026-2035 (defunciones, residencias, traslado) | Provincia (52) | 52 | Liberadas por año | Parámetros de residencia (4-8 % de 75+), estancia 2,5-4 años, 30-60 % solos, sobremortalidad ×2 | Contabilidad de flujo por provincia | No aplica (rangos de supuestos) | Liberadas 2026-2035 central 1.856.431 (936.056-3.168.590); 185.643 por año | Control de sumas por tipos | No aplica | C4 | `output/v5_1/T2/` |
| T3 | Déficit 2021-2025 y necesidad 2026-2035 con bajas (T1) y liberadas no llegadas al mercado (T2) | Provincia (52) | 52 | Déficit y necesidad | Bajas T1 y liberadas X | Contabilidad con rangos | Rango | Déficit 2021-2024 sin bajas 562.692-688.692; con bajas T1 central 653.097 (562.692-744.144); máximo antiguo 902.808 | Control de sumas y de liberadas | No aplica | C4 (el déficit sin bajas es C1) | `output/v5_1/T3/` |
| T4 | Dirección del déficit 2026-2030 en todos los escenarios (rejilla 5 × 3 × 3 × 4) | Provincia (52) | 52; 180 escenarios por horizonte | Déficit 2030 | dD = F − T + B + X | Rejilla de escenarios | Rango | Déficit 2030 nacional central 1.349.025 (788.180-1.773.555); con X 1.516.129 | Recuento por etapas | No aplica | C4 en magnitud; dirección C2 | `output/v5_1/T4/` |
| T6 | ¿Hay datos abiertos de alquiler de temporada o por habitaciones (BK-014) y MESVAL (BK-017)? | Nacional | n/d | No aplica | No aplica | Prueba de fuentes | No aplica | Ninguna fuente probada contiene duración del contrato ni modalidad de temporada | Fecha de prueba 2026-10-11 | No aplica | Técnico | `output/v5_1/T6/` |

### 1.3 v6 (validación sellada v6; `output/v6/*`)

| Familia | Pregunta | Mercado / nivel | N | Dependiente y transformación | Regresores / retardos | Estimador | EE | Resultados principales (p bruto / ajustado) | Diagnósticos | FM (RMSE, base, DM) | Estado | Ruta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M0 | Construcción de paneles, sellado v6 y potencia (Fisher-z) | Compra, alquiler (provincia y municipio); índice tasado | 100.353 | No aplica | No aplica | Descriptivo | No aplica | No estima modelos. Validación sellada contaminada descriptivamente por usos v4-v5 | Sellado `sellar_v6` | No aplica | Cerrado; C4 | `output/v6/M0/` |
| M1A | Efecto de la cuota de extranjeros, de la población, del PIB y de la oferta sobre el alquiler SERPAVI (TWFE) | Alquiler de stock; provincia (105 obs, 35 unidades) y municipio (4.865) | 105 / 4.865 | Log del alquiler €/m²/mes | Regresores en t−1 | TWFE con y sin tendencias | Wild cluster bootstrap Webb (B=999), por CCAA; Driscoll-Kraay; Conley | ln_pob: b 0,875, p 0,026, p ajustado 0,182 (provincia); municipio b 0,972, p 0,023, p ajustado 0,161. Resto de variables p ajustado 1,0. | RMSE 0,023 frente a 0,092 del AR(4) | Frente a M1 y AR(4) (EF) | EXPLORATORIO (C4); ningún coeficiente significativo tras ajuste | `output/v6/M1A/` (`tabla_coeficientes.csv`, 121 filas) |
| M1B | Compra: precio, volumen y relación compra-alquiler; FE unidad+año (preregistrada) y unidad+tendencia | Compra; provincia y municipio; valor tasado MIVAU | 64 (S1 prereg) y otras | Log del precio tasado | Regresores en t−1; ln_pob, share_ext_pob | MCO con EF; SDM | WCB restringido por CCAA (B=999); CR1 | S1 Holm: ln_pob b 0,599, p wild 0,517, p Holm 1,0. Holm mín. 0,496; BH mín. 0,0 | Clusters: 8 CCAA (provincial) | M1b-ADL frente a AR(4) y ECM v1; orígenes 2018/2020/2022 | EXPLORATORIO; ningún contraste cumple | `output/v6/M1B/` |
| M2 | Peso predictivo de cada variable (BMA, elastic net, PDS) | Provincia; alquiler (106 obs. completas) y compra | 106 / más | Log, % de efecto | Variables en t−1 con FE | BMA (g = max(N, K²), uniforme y beta-binomial), elastic net + PDS, multiverso | Intervalo creíble 95 % | PIP alquiler: ln_pob 1,00; share_ext_pob 0,30. PIP compra núcleo de share_ext 0,77 (completo). BH q=0,10 sobre 4.586 contrastes | PIP = soporte asociativo, no causal | No aplica (FM en M4) | EXPLORATORIO; nada causal | `output/v6/M2/` (`peso_variables.md`, `peso_variables.csv`) |
| M3A | Predicción de alquiler con RF y LightGBM (30 configuraciones por familia y nivel) | Alquiler; provincia, municipio, distrito | 8.554 (distrito, muestra común) | Log del alquiler | AR por unidad (p por AIC 1-4) | RF y gradient boosting; búsqueda aleatoria | No aplica | Mejor provincia RF: RMSE 0,0105 (AR 0,0303; ECM v1 aprox. 0,0110) | Bloques espacio-temporal; DM-HLN Holm y BH en `dm_hln_validacion_interna.csv` | Validación interna; mejor provincia RF RMSE 0,0105 | EXPLORATORIO (predicción) | `output/v6/M3A/` |
| M3B | Predicción de compra: RF, LightGBM, BART sustituido por bosque bootstrap bayesiano, MixedLM (sustituto de PyMC), MLP y GCN (solo municipio) | Compra (precio y volumen); provincia trimestral y municipio anual | 1.476 (trimestral) | Log del precio tasado | Ver `registro_*.csv` | ML, BART sustituto, MLP y GCN | No aplica | MUN_PRECIO_ANUAL: mejor ML BBF, RMSE 4,98 % frente a 8,95 % del AR; DM −1,56, p 0,178. PROV_PRECIO_TRIM: RMSE 1,93 % | Top SHAP: tipo hipotecario t−1, crédito; SHAP descriptivo | Validación en bloques | EXPLORATORIO; SHAP sin lectura causal | `output/v6/M3B/` |
| M4 | Predicción a un paso con modelos ajustados en la validación sellada | Alquiler, compra precio y volumen; provincia y municipio | 53 modelos, 9 tareas | Log, RMSE en % | Modelos ya ajustados | Evaluación de 53 modelos; `evaluate_v6` | No aplica | Alquiler provincia GB: RMSE 1,61 % frente a persistencia 4,21 % (DM-HLN −9,39; p Holm en `tabla_modelos.md`); MUN_PRECIO_ANUAL: mejor = ECM v1, RMSE 3,93 %; persistencia 6,33 % | 0 variables relevantes con seguridad | DM-HLN en `dm_hln` y p Holm dentro de tarea | EXPLORATORIO; predicción | `output/v6/M4/` (`tabla_modelos.md`, `mejor_modelo.csv`) |

### 1.4 v6.1 (`output/v6_1/K1-K4C`)

| Familia | Pregunta | Mercado / nivel | N | Dependiente | Regresores / retardos | Estimador | EE | Resultados principales | Diagnósticos | FM | Estado | Ruta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | ¿Predice algún modelo mejor que la base más exigente? (K1) | 9 tareas (provincia, municipio) sellado v6 | 9 tareas; 11 provincias selladas | RMSE en % | Modelos de M1-M4, ECM v1 como base | DM-HLN y permutación por inversión de signo; Holm por tarea y grupo | No aplica | Predice mejor que la base en 6 tareas; no distinguible en 3. MUN_PRECIO_ANUAL: el mejor (bosque bayesiano) 4,13 % frente a ECM v1 3,93 %: no la supera | Clasificación de clases | Frente a ECM v1 y AR(4) | EXPLORATORIO (C4): predicción | `output/v6_1/K1/` (`tabla_modelos_k1.md/.csv`) |
| K2 | Inmigración y precio/alquiler: MCO/2SLS con EF provincia-año; cuota de extranjeros y población | Provincia y CCAA | 328 (compra), 1 familia de 137 especificaciones | % por +1 pp de cuota | Cuota (t−1), población, demanda externa | MCO/2SLS; BMA aproximado (BIC) | Agrupados | Cuota compra sin población 4,26 %/pp; con núcleo −1,31 % (IC [−4,31; 1,69]); p Holm 1,0. Primera etapa F 3,52 (38 provincias) | VIF 1,79 | No aplica | ANALIZADA, NO CONCLUYENTE; C4 | `output/v6_1/K2/` |
| K3 | Tipo de «ratio» de precio/alquiler: OLS con EF provincia-año | Provincia | 175 | Ratios precio/alquiler | Variables de precio inicial y rezagos | OLS, cluster por provincia | Cluster provincia | Coeficientes A_conjunta: p ajustado 1,0 (ini_l2, ini_l1); ini_1000 p ajustado 0,57 | Rango de ratio 2015 [18,9; 20,3] | No aplica | ANALIZADA; C4 | `output/v6_1/K3/` |
| K4A | Auditoría dirigida con consultas y tests | Proyecto | 11 | No aplica | No aplica | Auditoría | No aplica | 11 hallazgos: 0 críticos, 2 altos, 3 medios, 6 bajos | No aplica | No aplica | Técnico | `output/v6_1/K4A/` |
| K4B | Doble implementación independiente | Proyecto | 15 | No aplica | No aplica | Recalculo | No aplica | Coinciden 5; parciales 5; no reconstruibles 5; no coinciden 0 | No aplica | No aplica | Técnico | `output/v6_1/K4B/` |
| K4C | Extracción determinista de cifras y comprobación de enlaces | Entregables | 1.916 | No aplica | No aplica | Extracción | No aplica | Enlaces rotos 32 → 0; 5 contradicciones (corregidas) | No aplica | No aplica | Técnico | `output/v6_1/K4C/` |

### 1.5 v6.2 (`output/v6_2/L1-L3`)

| Familia | Pregunta | Mercado / nivel | N | Dependiente | Regresores / retardos | Estimador | EE | Resultados principales | Diagnósticos | FM | Estado | Ruta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L1 | Verificación de fichas y reproducción literal | Entregables | 17 fichas completas; 49 breves | No aplica | No aplica | Recálculo literal | No aplica | 17 fichas reproducidas; 15 de la revisión humana | ruff limpio, sin fallos | No aplica | Técnico | `output/v6_2/L1/` |
| L2 | Segunda doble implementación independiente (sin leer src) | Entregables | 15 | No aplica | No aplica | Recálculo | No aplica | Coinciden 15 de 15 | 11 huecos en anexo, ninguno bloquea | No aplica | Técnico | `output/v6_2/L2/` |
| L3 | Déficit 2021-2025 sin bajas bajo 8 correcciones de hogares × 3 fuentes de terminadas | Nacional | 288 combinaciones | Déficit en viviendas | No aplica | Contable determinista | No aplica | 2021-2024 sin bajas 389.361-710.542 (punto medio 549.952); 2021-2025 sin bajas 523.606-887.950 | Por año y corrección | No aplica | C2 (sin bajas) / C4 (con bajas) | `output/v6_2/L3/` (`deficit_alternativas.csv`) |

---

## 2. Resultados regionales disponibles

**Por CCAA**
- **GSADF (burbuja):** el ratio precio/alquiler por CCAA (11 CCAA, 2015T1-2024T4) se evaluó en v4 M7 y v6 M1B. Ninguna CCAA supera el valor crítico. Nacional: estadísticos 3,10-4,82, veredicto de la fuente, no reverificado en K2. Fuente: `docs/v6_1/historial_conclusiones.md`; R1B (GSADF con tamaño corregido, BH/Holm) en `output/v5/R1B/`.
- **Coeficientes M1A/M1B por CCAA:** la inferencia usa wild cluster bootstrap por CCAA (8 clusters en provincial, 7 en municipal, 11 en trimestral). Coeficientes en `output/v6/M1A/tabla_coeficientes.csv` y `output/v6/M1B/tablas/fe_prov.csv`. Ninguno significativo tras ajuste.
- **Peso de inmigración (K2) por CCAA:** `output/v6_1/K2/`. Sin conclusión.
- **Riesgo de conteo:** la muestra de CCAA es de 17 unidades; las estimaciones por CCAA no tienen potencia suficiente.

**Por provincia**
- **Clases A4 por provincia (52):** `output/v5/A4/clasificacion_provincias.csv`. Número de provincias por clase 2021-2025: clase 1 = 37 (8 robustas), clase 2 = 11 (3), clase 3 = 2 (0), clase 4 = 0, clase 9 = 2 (1). Significatividad: C4, sin contraste.
- **Necesidad por provincia (B1):** `output/v5/B1/tablas/`. 48 provincias con presión; 4 con R en un solo método. C4.
- **Déficit por provincia (B2, T3, T4):** `output/v5/B2/tablas/`, `output/v5_1/T3/`, `output/v5_1/T4/`. Proyección bajo supuestos. C4.
- **Déficit provincial tras bajas (T3):** rango por provincia en `output/v5_1/T3/`. C4.
- **Coeficientes M1A (provincia y municipio):** `output/v6/M1A/tabla_coeficientes.csv`. Ninguno significativo tras ajuste (ln_pob p 0,026 → p ajustado 0,182).
- **PIP y peso de variables por provincia (M2):** `output/v6/M2/peso_variables.csv`, `peso_alquiler_prov.csv`, `peso_compra_prov.csv`. Soporte asociativo, no causal.
- **SHAP y dependencia parcial (M3B):** `output/v6/M3B/`. Descriptivo, sin lectura causal.
- **Demanda (K2, K3):** sin conclusión.

---

## 3. Política (D1, D2 y documentos relacionados)

**Instrumentos evaluados:**
- `output/v4/M5/matriz_instrumentos.csv`: 23 filas (instrumentos agrupados, con columnas de mecanismo, evidencia, efecto, plazo, coste fiscal y riesgos).
- `output/v5/D1/matriz_instrumentos.csv`: 37 filas (I01-I29, N1-N9, P1). Incluye el campo `capa` por instrumento.
- Instrumentos con capa C2 en el signo y C4 en la magnitud: I02/N8, I06, I07, I08/N9, I10/N7, I27, P1.
- Instrumentos sin signo evaluable (D1, `sin_signo_evaluable`): I03, I04, I05, I09, I11, I13, I14, I15, I19, I20, I22, I24, I25, I26, N1, N3, N5, N6 (18 en total).

**Instrumentos sin evaluar:**
- I17 e I23 no tienen definición en v4 (`resultado.json` de D1 lo declara).

**Método de simulación (D1):**
- Incidencia = |εd| / (εs + |εd|), con εs por clase: clase A según la respuesta de oferta de A4; clase B según la rejilla P-D.
- Determinista, sin especificaciones econométricas nuevas (registro.csv vacío por diseño).
- Métodos A y B se reportan ambos cuando discrepan.

**Parámetros y rango de elasticidades:**
- Rejilla de elasticidad de demanda: εd entre 0,3 y 1,5 (`output/v5/D1/` y nota D1-H11).
- Rejilla de elasticidad de oferta εs: clase A por A4; clase B por rejilla P-D. Rango exacto de εs no extraído en esta lectura.
- **Origen de las elasticidades:** `output/v5/D1/literatura_instrumentos.csv`. Ejemplo verificado: Jofre-Monseny et al. (2023, Q1, VERIFICADA) para topes de renta. Otros: Baum-Snow y Marion (2009), Diamond y McQuade (2019), Eriksen y Rosenthal (2010), marcados VERIFICADA, con magnitud no extraída. Cualquier referencia sin verificar debe figurar como «NO VERIFICADA».

**Resultados por clase territorial A4 (D1, método A, traslado al precio):**

| Clase A4 | Min | Central | Max |
|---|---|---|---|
| 1 | 27,8 % | 58,4 % | 81,8 % |
| 2 | 88,1 % | 100 % | 100 % |
| 3 | 50,1 % | 76,4 % | 89,8 % |

- Clase A4 2: el 100 % se traslada al precio (un valor de tope, no un resultado de precisión).
- Clase 1 de D2: cobertura de P-D 11,6-46,5 %; vacías 30,2 %.
- Método B: rango por clase en `output/v5/D1/` (no extraído en esta lectura).

**Documentos relacionados:**
- `output/v5/D2/politica_territorio.md` y `output/v5/D2/resumen_por_clase.csv` (cruce de tablas, reparto de P-D por cuota de necesidad).
- `output/v5/D3/` (comparación con referencias externas: coincide 2, difiere 1, comparable en parte 6, no comparable 9).

---

## 4. Historial de conclusiones

### 4.1 Tabla compacta (fuente: `docs/v6_1/historial_conclusiones.md`, con adenda v6.2 L4)

| Tema | Conclusión vigente | Capa | Estado |
|---|---|---|---|
| Inmigración → alquiler (CCAA, v1) | Signo positivo, no robusto a todos los niveles | C4 | Se mantiene (asociación) |
| Inmigración → precio (CCAA, v1) | No concluyente | C4 | Se mantiene |
| Cuota de extranjeros → precio (CCAA, v1) | No concluyente | C4 | Se mantiene |
| Inmigración → alquiler y compra (provincia, v2/BI) | Alquiler +3,06 %/pp [1,14; 4,98]; compra n.s. | C4 | Se mantiene |
| Población extranjera → alquiler (v2/BA) | Negativo n.s. | C4 | Se mantiene |
| Cotas Manski de cantidad de hogares extranjeros (v3/PB) | Cota no informativa (100 %) | C2 | Se mantiene |
| Nacionalidad y hogares creados (v4/M2) | 53-76 % de ΔH según corrección EPA | C4 | Se mantiene (descriptivo) |
| Peso de no residentes y precio (v5/R1A) | No concluyente | C4 | Se mantiene |
| Cuota de extranjeros → alquiler/compra (v6/M1, v6/M2) | Cambia la lectura: PIP alta en compra con núcleo, baja en alquiler. K2 lo reclasifica como «analizada, no concluyente» | C4 | Cambia; K2 analizada |
| Inmigración → empleo (v1, v2/BV, v6) | Signo según método; no concluyente | C4 | Se mantiene |
| Renta → alquiler y compra (v1, v6) | Cero en alquiler, positivo en compra (p 0,13), sin concluir | C4 | Cambia de mercado; no concluyente |
| Oferta (iniciadas) → precio (v2/BO, v6) | Oferta responde al precio (β 0,79); otra dirección según medida | C4 | Se mantiene |
| Turísticos (VUT) → alquiler (v3/C1, v6) | Signo no estable; n.s. | C4 | Se mantiene (no concluyente) |
| Turísticos: cota de stock desplazado (v3/PB) | Máximo 2,4-2,75 % del stock de alquiler | C2 | Se mantiene |
| Topes de renta (v2/BP; v3/C3) | Efecto −5,4 % en contratos nuevos (fianzas); falla pretendencias | C4 | Cambia de mercado (contratos nuevos, no stock) |
| Zonas tensionadas (v2/BS) | τ −0,0117, Holm 0,098 | C4 | Se mantiene; no estimable en v6 |
| Tipos hipotecarios → precio (v1) | Sin efecto de largo plazo | C4 | Se mantiene |
| Crédito y coste de uso (v2/BV, v3/PB) | Sin valor predictivo en sellado | C4 / C2 | Se mantiene |
| Déficit acumulado 2021-2025 (v1) | Cambió: v5.1 sin bajas 700.934-757.257 (C1); con bajas C4 central 763.416 | C1/C4 | Cambia (v5.1) |
| Déficit 2021-2024 sin bajas (v6.2/L3) | 389.361-710.542 viviendas | C2 | Vigente |
| Bajas y déficit con bajas (v4→v5.1) | Supuesto de 902.808 (C2) → T1 hasta 744.144 (C4) | C2 → C4 | Cambia (corregido en v5.1) |
| Necesidad 2026-2035 (v5→v5.1) | 99.000-292.000 viviendas/año; dirección 2026-2030 «empeora» (C2) | C4 | Cambia; liberadas no se restan |
| Exuberancia GSADF (v4/M7, v6/M1B) | Ninguna CCAA supera el valor crítico | C4 | Se mantiene |
| Precio de compra: IPV frente a núcleo (v5/A23) | IPV +79,9 %; núcleo +44,2 a +56,1 % | C1 (núcleo) / C4 | Se mantiene |
| Elasticidad precio-alquiler (v6/M1B) | 0,43-1,33 (FE); 1,6-2,1 (DOLS); depende de la especificación | C4 | Se mantiene |
| Predicción frente a AR(4) (v1) | ECM no mejora al AR(4) (DM p 0,509) | C4 | Se mantiene (línea base) |
| Demografía 20-34 (v2/BA) | RMSE 0,0108 frente a 0,0122 del AR(4) | C4 | Se mantiene (predictivo, no robusto) |
| ML sellado (v6/M4, v6.1/K1) | Alquiler provincia: 1,61 % frente a 4,21 % (persistencia); 6 de 9 tareas predicen mejor que la base; ninguna variable relevante con seguridad | C4 | Se mantiene (predicción) |
| Inmigración (v6.2/L4): asociación total y directa | Total: compra +4,3 %/pp; directa (con población): compra −1,3 (IC −4,3; 1,7), alquiler 0,18 (IC −1,5; 1,8). Controlar población es mal control | C4 | Se mantiene K2: analizada, no concluyente |

### 4.2 Cifras publicables (`docs/v6_2/cifras_publicables.md`, generado por `src/v6_2/l5_publicables.py`)

**Aptas para difusión (C1 o cota C2):**

| id | Indicador | Valor (rango) | Capa | Periodo |
|---|---|---|---|---|
| dh_2125 | Aumento de hogares | 997.586 (981.823-1.013.350) | C1 | 2021-2025 |
| terminadas_1924 | Viviendas terminadas/año (territorio común) | 72.264-94.426 | C1 | 2019-2024 |
| L3-DEF-2124-SINBAJAS | Déficit 2021-2024 sin bajas | 389.361-710.542 | C2 | 2021-2024 |
| A23-P2 | Precio de compra, núcleo 2015-2025 | 47,2 % (44,2-56,1 %) | C1 | 2015-2025 |
| A23-A2 | Alquiler de stock 2015-2024 | 10,9-22,9 % | C1 | 2015-2024 |
| A23-A10 | Contratos nuevos Comunitat Valenciana 2021-2024 | 28,5 % (26,1-30,8 %) | C1 | 2021-2024 |
| A23-A9 | Contratos nuevos Cataluña 2021-2024 | 16,9 % (16,6-17,2 %) | C1 | 2021-2024 |
| E-B1-F | Crecimiento de hogares proyectado (10 años) | 1.308.531-1.772.410 | C2 | 2026-2035 |
| R1C-001 | Hogares propietarios de vivienda principal | 74,5 % (72,1-75,9 %) | C1 | 2021-2022 |

**No citar fuera de contexto (C4 o dependiente de supuestos):**

| id | Indicador | Valor (rango) | Capa |
|---|---|---|---|
| L3-DEF-2124-CONBAJAS | Déficit 2021-2024 con bajas 0,1-0,2 % | 389.361-924.658 | C2 |
| T3-H5b | Necesidad anual 2026-2035 (base sin X) | 210.424 (99.388-292.083) | C4 |
| T3-H5 | Necesidad anual 2026-2035 (con X) | 245.989 (123.936-338.663) | C4 |
| B1-H1 | Necesidad total por año (52 provincias) | 214.868 (93.628-309.921) | C4 |
| D1-H11 | Traslado a precio, clase A4 1 (método A) | 58,4 % (27,8-81,8 %) | C4 |
| D1-H12 | Traslado a precio, clase A4 2 (método A) | 100,0 % (88,1-100,0 %) | C4 |
| K2-CUOTA-COMPRA-SINPOB-SIN | Cuota de extranjeros (compra, sin población) | 4,3 % por pp (2,1-6,4 %) | C4 |
| K2-CUOTA-COMPRA-SIN | Cuota de extranjeros (compra, con núcleo) | −1,3 % por pp (−4,3 a 1,7 %) | C4 |
| K1-N-MEJOR | Tareas donde el mejor modelo supera la base exigente | 6 tareas | C4 |
| latente_convivencia | Demanda latente de jóvenes por convivencia | 188.000-506.000 hogares | C2 |
| B4-v3-vut-cantidad | Stock de alquiler desplazado por VUT (máximo) | 2,4-2,7 % | C2 |
| L3-DEF-2124-BAJAST1 | Déficit 2021-2024 con bajas T1 | 654.646 (389.361-765.994) | C4 |
| L3-DEF-2124-SENS | Sensibilidad sin variantes a y d1 | 596.371-710.542 | C2 |

**Históricas (no citar; sustituidas, ver ERRATA.md):**

| id | Indicador | Valor (rango) | Capa | Sustituida por |
|---|---|---|---|---|
| deficit_2124_c1 | Déficit 2021-2024 sin bajas | 562.692-688.692 | C1 | L3-DEF-2124-SINBAJAS |
| deficit_2124_c2 | Déficit 2021-2024 con bajas supuestas (cota) | 562.692-902.808 | C2 | L3-DEF-2124-CONBAJAS |
| T3-H2 | Déficit 2021-2024 con bajas T1 | 653.097 (562.692-744.144) | C4 | L3-DEF-2124-BAJAST1 |

---

## Lista de comprobaciones pendientes (no ejecutadas)

- Rango exacto de εs y εd por clase en D1 (método B): no extraído.
- p ajustado por coeficiente de M3B y M4 (DM por tarea): solo los valores resumen.
- Estado de verificación DOI/cuartil de cada referencia de `output/v5/D1/literatura_instrumentos.csv`: no verificado en esta lectura.
- `docs/v6_1/historial_conclusiones.md` se resumió a partir de la lectura de sus 120 primeras líneas truncadas a 260 caracteres; las filas se reproducen con su valor principal. Para cifras exactas, consultar el fichero original.

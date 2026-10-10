# Dónde falta vivienda en España, por qué y qué instrumentos funcionarían: hechos, cotas y efectos con datos públicos

*Documento de trabajo, v4. Proyecto reproducible: `make all` sin red.*

## Resumen
Combinamos registros públicos (INE, Ministerio de Vivienda, Catastro, Notariado, Registradores, Banco de España) para medir el déficit de vivienda en España, descomponer la creación de hogares, evaluar si construir es rentable donde falta vivienda, separar parque y mercado, y comparar instrumentos de política con una rúbrica idéntica. Cada resultado se clasifica en una de cuatro capas de evidencia: hechos confirmados por fuentes independientes, cotas, efectos identificados y exploratorio. Entre 2021 y 2024 los hogares crecieron entre 563.000 y 689.000 más que las viviendas nuevas, con dos fuentes independientes en cada componente. El precio de compra subió entre un 44 % y un 56 % en 2015-2025 según tres fuentes (el índice del INE da un 80 %). El déficit se concentra en pocas provincias. Ningún efecto causal supera nuestros criterios de identificación. Entre los instrumentos simulados, solo las medidas que añaden viviendas donde hay demanda tienen un signo estable sobre el esfuerzo de acceso en todo el rango de supuestos (C2; la magnitud es C4). Los topes, la regulación de viviendas turísticas y las ayudas a la demanda dependen de parámetros que los datos no fijan; otros siete grupos de instrumentos, algunos de oferta, no se evaluaron.

## 1. Introducción
**Pregunta.** ¿Qué se puede afirmar, con qué grado de seguridad, sobre dónde falta vivienda en España, por qué se forman tantos hogares, si se puede construir donde falta y qué instrumentos de política funcionarían?

**Contribución.**
1. **Una escala de capas de evidencia aplicada de forma uniforme.**
   - La escala tiene cuatro capas: C1 hechos (≥2 fuentes independientes, con todos los componentes en C1), C2 cotas de identificación parcial con supuestos explícitos (Manski 2003), C3 efectos y C4 exploratorio.
   - Regla: la capa de un hecho es la menor de las de sus componentes.
   - Por esa regla, cifras habituales en el debate (déficit 2021-2025, peso de compradores extranjeros, vacías) quedan en C4. Se identifica en qué ventana o con qué fuentes pasan a C1.
2. **Una conciliación de las cifras de déficit** de nuestras versiones anteriores y del Banco de España, con una cadena de pasos que cierra exactamente, y una cifra C1 para 2021-2024.
3. **Una descomposición contable de la creación de hogares** (población por nacionalidad, estructura por edad y jefatura), con la corrección de la ruptura de la EPA de 2021 y la declaración de qué componentes son de fuente única.
4. **Una evaluación de instrumentos con la misma rúbrica.** Las medidas proceden de 9 documentos de programas (4 leídos en copia no oficial alojada por un medio) y se agrupan por instrumento, no por partido. Incluye instrumentos no propuestos y un verificador de afirmaciones del debate con veredictos y convenciones explícitas.

Frente a la literatura:
- no estimamos efectos causales nuevos que superen criterios estrictos;
- documentamos por qué no se replican resultados conocidos con los datos abiertos actuales (García-López et al. 2020) y cuándo sí (Jofre-Monseny et al. 2023);
- mostramos qué afirmaciones resisten una exigencia homogénea de evidencia.

## 2. Contexto institucional y datos
**Marco normativo.**
- Ley 12/2023, por el derecho a la vivienda: zonas de mercado residencial tensionado, definición de gran tenedor.
- Ley 11/2020 de Cataluña, anulada por la STC 37/2022.
- Registro único de arrendamientos (RD 1312/2024).

**Datos.** Listado completo y licencias en README_REPLICACION.md.
- **INE:** IPV, IPC de alquiler, EPA, ECP, censos 2011 y 2021, censo anual por sección, viviendas turísticas por sección, ETDP.
- **Ministerio:** fin de obra, valor tasado, suelo urbano, transacciones por residencia, SERPAVI.
- **Catastro:** unidades urbanas por uso, solares.
- **Notariado y Registradores.**
- **Banco de España:** EFF.
- **Incasòl:** fianzas de Cataluña.
- **Eurostat.**
- **No accesibles:** SIU, titularidad catastral por tipo de titular, tipo de arrendador en las fianzas, coste de construcción en nivel. Ver docs/v4/fuentes_fallidas.md.

## 3. Marco conceptual: parque frente a mercado; cuentas de hogares y viviendas
- **Identidad contable del déficit:** D = ΔH − (terminadas − bajas). Es un balance de flujos, no una medida de demanda insatisfecha a cualquier precio.
- **Descomposición de los hogares:** H = Σ P(edad, nacionalidad) × h(edad). Se descompone con valores de Shapley en tamaño, estructura y jefatura.
- **Parque y mercado:**
  - parque: stock por uso y por titular;
  - mercado: flujos de compraventas, contratos nuevos y oferta anunciada.

  Una afirmación sobre «quién domina el mercado» requiere comparar el peso en el flujo con el peso en el stock.
- **Brecha precio-coste** (Glaeser y Gyourko 2018): precio − coste × (1 + margen) − suelo. Una brecha grande es compatible con restricciones a la oferta, pero no las identifica.

## 4. Métodos por capas
- **C1, hechos.** Al menos dos fuentes independientes, con un rango declarado de coincidencia (±15 % en niveles; en variaciones de precio, ±5 pp anuales es la regla de dirección y la cuantía exige ±15 % en nivel). Si dos fuentes comparten el documento de origen, la independencia es parcial y se declara.
- **C2, cotas.** Supuestos explícitos: bajas del parque, sustitución 1:1 de viviendas turísticas por alquiler, tasas de referencia.
- **C3, efectos.** Pre-registro (v3: ancla 204c073), pretendencias (Rambachan y Roth 2023), placebos, sensibilidad (Oster 2019; Cinelli y Hazlett 2020), validación sellada y Holm.
- **C4.** Todo lo demás. Las traducciones de cotas a precio que usan elasticidades sin estimación española se tratan como C4 (convención A). El verificador muestra también el veredicto con la convención B, en la que esas traducciones cuentan como C2.

## 5. Resultados
### 5.1 Hechos (C1)
| Hecho | Valor | Fuentes |
|---|---|---|
| Déficit 2021-2024, sin bajas | 563.000-689.000 viviendas | ECP y EPA corregida; Ministerio y Catastro |
| ΔH 2021-2025 | ≈1,0 M (982.000-1.013.000) | ECP y EPA corregida |
| Terminadas 2019-2024, territorio común | 72.000 (2019) a 94.000 (2024) al año | Ministerio y Catastro (independencia parcial; sin País Vasco ni Navarra) |
| Precio de compra 2015-2025 | +44 % a +56 % (INE IPV +80 %, discrepante); dirección C1 en 17 CCAA, cuantía C1 en 15 | Ministerio, Registradores, Notariado; INE aparte |
| Alquiler 2015-2024 | dirección C1 al alza; cuantía C4 (+11 % a +43 %); 2021-2024: +6 % a +15 % (C1) | IPC de alquiler y SERPAVI |
| Convivencia con los padres (25-34) | 40-50 % | Eurostat/ECV y EPA (v3) |
| Propiedad, menores de 35 (2022) | 30,7-31,8 %; −24 a −34 pp desde 2008 | EFF y ECV (v3) |

### 5.2 Cotas (C2)
- Déficit 2021-2024 con bajas supuestas: hasta 903.000.
- Demanda latente:
  - por jefatura de 2008 (C4 por la regla B5: jefatura de fuente única): 16-34 años, ±23.000; 20-34 años, +84.000 a +161.000; sin latente neta en el total;
  - por convivencia con los padres: 188.000-506.000.
- Viviendas turísticas: como máximo el 2,7 % del stock de alquiler (v3).
- Simulación P-D: más construcción y movilización de vacías reducen el esfuerzo de acceso en toda la rejilla.

### 5.3 Exploratorio relevante (C4)
- Componente de nacionalidad extranjera en ΔH 2021-2025: 56-58 % (53-76 %).
- Concentración del déficit: 7 provincias suman el 50 %.
- Compradores extranjeros: 16,9-18,8 % en 2025.
- Personas jurídicas: 11,3 % de los compradores.
- Censo 2021: 3,8 M de viviendas vacías.
- Exuberancia GSADF: 2011-13, 2017-19 y 2024-26.
- Clasificación territorial con coste supuesto: 16 provincias con brecha precio-coste elevada y 30 sin rentabilidad al coste supuesto.

### 5.4 Efectos y replicaciones
- **Viviendas turísticas → alquiler (v3, H3-1/H3-2).** C4. La estimación sellada es +0,0010 log-puntos por pp, con un IC95 de −0,0007 a 0,0028.
- **Topes de la Ley 11/2020 (v3, H3-3).** −5,4 % en la renta de los contratos nuevos. Queda fuera de C3 de forma definitiva por la contaminación de la validación.
- **Replicaciones:**

| Trabajo | Resultado | Explicación (M0) |
|---|---|---|
| García-López et al. (2020) | NO REPLICADO | El stock SERPAVI recoge el 55-75 % del flujo, lo que explica una magnitud menor pero no el signo. El método (sin IV) y el periodo no se pueden contrastar. Tras Holm, p = 0,27. |
| Jofre-Monseny et al. (2023) | REPLICADO en la especificación más cercana | — |
| MESVAL (2022) | NO REPLICABLE | — |

## 6. Evaluación de instrumentos
Se aplica la misma rúbrica a los 14 grupos de instrumentos (output/v4/M5/matriz_instrumentos.md): mecanismo, evidencia, efecto con rango, plazo, coste, riesgos, distribución y dónde funciona.

| Signo sobre el esfuerzo de acceso | Instrumentos |
|---|---|
| Estable | más construcción donde falta; movilización de vacías |
| Débil (nulo si hay desplazamiento) | vivienda pública |
| No estable (depende de parámetros) | topes al alquiler; regulación de viviendas turísticas; ayudas a la demanda (el 15-100 % se traslada al precio) |
| Sin evaluar | licencias, densidad, industrialización, fiscalidad del suelo, seguridad jurídica, límites a no residentes, rebajas fiscales a la construcción |

Ninguna simulación incluye costes.

## 7. Robustez y multiverso
- **M1:** combinaciones de fuentes de hogares y de altas, y bajas del 0 %, 0,1 % y 0,2 %.
- **M3:** 972 especificaciones por provincia (coste, margen, edificabilidad); estabilidad de la clase.
- **M7:** cuatro fuentes de precio (núcleo de tres más el IPV del INE) y dos de alquiler; GSADF con valores críticos simulados y de wild bootstrap, y una prueba de tamaño.
- **v3:** curvas de especificaciones para H3-1 (96) y H3-3 (36), con la mediana y la proporción con el mismo signo.

## 8. Limitaciones
Ver docs/v3/limitaciones.md, y para v4 docs/v4/decisiones.md y las revisiones. Las principales:
- **Fuente única:**
  - hogares provinciales (ECP);
  - jefatura por edad (EPA);
  - vacías (Censo);
  - personas jurídicas (ETDP).
- **Sin fuente verificable:**
  - coste de construcción en nivel;
  - titularidad del stock.
- **Independencia parcial** entre Ministerio y Catastro, y entre Ministerio y Notariado.
- **Programas analizados:** dos no fueron accesibles; 4 de los 9 documentos se leyeron en una copia no oficial alojada por un medio. Sin búsqueda por palabras clave sobre el texto completo, los recuentos son cotas inferiores (docs/v4/cobertura_programas.md). Once instrumentos no tienen búsqueda bibliográfica registrada (docs/v4/literatura_v4.md).
- **Convención en las traducciones a precio:** los veredictos dependen de cómo se traten. Se informan las dos convenciones.

## 9. Conclusiones
1. [C1] Hay un desfase entre hogares y viviendas nuevas desde 2021, confirmado con fuentes independientes. [C4] Está concentrado territorialmente.
2. Los precios de compra suben en todas las comunidades.
3. La explicación del crecimiento de los hogares en 2021-2025 está dominada contablemente por la población de nacionalidad extranjera. Este resultado es exploratorio y no causal.
4. Los efectos de los instrumentos debatidos no están identificados con los datos abiertos. Con la misma rúbrica y entre los instrumentos simulados, solo las medidas que añaden viviendas donde hay demanda tienen un signo estable (C2); las magnitudes son C4 y varios instrumentos de oferta no se evaluaron.
5. Las mayores lagunas son de datos: titularidad, coste de construcción, suelo urbanizable y contratos nuevos. Las solicitudes para cubrirlas están redactadas.

## Referencias (verificadas con DOI en Crossref; cuartil Scimago cuando consta)
- Carozzi, Hilber y Yu (2024), *Journal of Urban Economics* 139, 103611. DOI 10.1016/j.jue.2023.103611. VERIFICADA, Q1.
- Cinelli y Hazlett (2020), *JRSS-B* 82(1). DOI 10.1111/rssb.12348. VERIFICADA, Q1.
- Diamond, McQuade y Qian (2019), *American Economic Review*. DOI 10.1257/aer.20181289. VERIFICADA, Q1.
- García-López, Jofre-Monseny, Martínez-Mazza y Segú (2020), *Journal of Urban Economics*. DOI 10.1016/j.jue.2020.103278. VERIFICADA, Q1.
- Gibbons y Manning (2006), *Journal of Public Economics* 90(4-5). DOI 10.1016/j.jpubeco.2005.01.002. DOI verificado (Crossref); cuartil no verificado.
- Glaeser y Gyourko (2018), *Journal of Economic Perspectives*. DOI 10.1257/jep.32.1.3. DOI verificado (Crossref); cuartil no verificado.
- Hilber y Vermeulen (2016), *Economic Journal* 126(591). DOI 10.1111/ecoj.12213. VERIFICADA, Q1.
- Jofre-Monseny, Martínez-Mazza y Segú (2023), *Regional Science and Urban Economics*. DOI 10.1016/j.regsciurbeco.2023.103916. VERIFICADA, Q1.
- Manski (2003), *Partial Identification of Probability Distributions*, Springer. DOI 10.1007/b97478. VERIFICADA (libro).
- Oster (2019), *JBES* 37(2). DOI 10.1080/07350015.2016.1227711. VERIFICADA, Q1.
- Phillips, Shi y Yu (2015), *International Economic Review* (test GSADF). NO VERIFICADA en este proyecto (DOI no comprobado).
- Rambachan y Roth (2023), *Review of Economic Studies* 90(5). DOI 10.1093/restud/rdad018. VERIFICADA, Q1.
- Saiz (2010), *Quarterly Journal of Economics*. DOI 10.1162/qjec.2010.125.3.1253. DOI verificado (Crossref); cuartil no verificado.
- Segú (2020), *Journal of Public Economics* 185, 104079. DOI 10.1016/j.jpubeco.2019.104079. DOI verificado (Crossref); cuartil no verificado.
- Baum-Snow y Marion (2009), *Journal of Public Economics* 93(5-6). DOI 10.1016/j.jpubeco.2009.01.001. DOI verificado (Crossref); cuartil no verificado.
- Glaeser, Gyourko y Saks (2005), *Journal of Law and Economics* 48(2). DOI 10.1086/429979. DOI verificado (Crossref); cuartil no verificado.
- Jofre-Monseny et al. y Diamond et al.: arriba. Banco de España (2026), Informe Anual 2025. NO VERIFICADA (DOI no comprobado).
- Lista completa: docs/literatura.md (anexos v3 y v4) y output/v3/articulo.md §11.

## Apéndices
- **A. Datos.** README_REPLICACION.md (fuentes, licencias, fechas de descarga) y data/raw/_manifest.csv.
- **B. Replicación.** `make all` (≈20-21 minutos, un hilo), `make check` y `make verificador`. Registro de especificaciones: output/v4/M*/registro.csv.
- **C. Uso de IA.**
  - **Cómo se hizo.** El proyecto se ejecutó con agentes de IA (Claude): un orquestador y subagentes de datos, literatura, econometría y revisión independiente por oleadas (A, B y C). Todas las cifras proceden del código del repositorio y de fuentes públicas.
  - **Referencias.** Se verifican por DOI o se marcan NO VERIFICADA.
  - **Revisión.** El revisor encontró errores que se corrigieron:
    - un fallo de tipos que anulaba las terminadas en M1;
    - una comparación incorrecta en la convención B;
    - la asignación de capas sin la regla del componente más débil.

    Están documentados en docs/v4/revision_oleada*.md y docs/v4/decisiones.md.

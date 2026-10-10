# Informe técnico v4: dónde falta vivienda, por qué, si se puede construir allí, parque frente a mercado e instrumentos

**Alcance.** Este informe resume los módulos M0-M7 del proyecto v4 para un público técnico de las administraciones y de los organismos de análisis. Los resultados se clasifican en cuatro capas:

- **C1, hechos.** Requiere al menos dos fuentes independientes, y todos los componentes del hecho deben estar también en C1.
- **C2, cotas.** Valen bajo supuestos explícitos.
- **C3, efectos identificados.** Ningún resultado de este informe la alcanza.
- **C4, exploratorio o de fuente única.**

La capa de un hecho es la menor de las de sus componentes. Un hecho en C4 solo puede recibir como máximo el veredicto «no concluyente».

**Reproducibilidad y datos.** Todo se reproduce sin red con `make all`; el README_REPLICACION.md explica cómo. Las revisiones independientes de las oleadas A, B y C están en docs/v4/revision_oleada*.md. Las decisiones están en docs/v4/decisiones.md y las limitaciones, en docs/v3/limitaciones.md y docs/v4.

---

## 1. Diagnóstico nacional

### 1.1 Cuántas viviendas faltan: conciliación de cifras (M0)
| Cifra | Fuente de hogares | Oferta | Periodo | Viviendas | Capa |
|---|---|---|---|---|---|
| v1, principal | EPA corregida por la ruptura de 2021 | fin de obra, libres | 2021T1-2025T4 | 866.100 | C4 (una sola fuente de hogares) |
| v1, alternativa | ECP a 1 de enero | fin de obra, libres | 1-ene-2021 a 1-ene-2026 | 810.936 | C4 |
| v3 | EPA, ECP y censo | fin de obra con y sin protegida, bajas 0-0,2 % | 2021T1-2025T4 | 701.000 (560.000-969.000) | C1 en v3; C4 con la regla de v4, porque las terminadas de 2025 son frágiles |
| Banco de España | no declarada | no declarada | 2021-2025 | ≈750.000 (IEF: 700.000) | NO VERIFICADA (DOI no comprobado) |
| **v4** | ECP y EPA corregida (coinciden dentro del 8,4 %) | Ministerio y Catastro (dentro de ±15 %) | **2021-2024** | **563.000-689.000 sin bajas** | **C1** |
| v4, con bajas supuestas del 0,1-0,2 % | ídem | ídem | 2021-2024 | hasta 903.000 | C2 |

Del v1 al v3 la cifra baja por tres pasos, y la cadena cierra de forma exacta:
1. la fuente de hogares: −55.164;
2. la inclusión de la vivienda protegida: −56.323;
3. un desplazamiento de la ventana de un trimestre: −53.679.

Frente al Banco de España quedan +49.066 que no se pueden descomponer, porque su método no está publicado (output/v4/M0/conciliacion_deficit.md).

### 1.2 Viviendas terminadas (M0)
- [C1] En 2019-2024 se terminaron entre 91.000 y 101.000 viviendas al año. El Ministerio (certificados de fin de obra, libres y protegidas) y el Catastro (aumento neto de unidades residenciales) coinciden dentro de ±15 %.
- Las dos fuentes son independientes solo en parte, porque comparten documento de origen: el certificado final de obra.
- En 2012-2017 difieren entre 1,2 y 3 veces, por lo que esos años quedan en C4. 2018 y 2025 también son C4, por la fragilidad de los datos.

### 1.3 Por qué hay tantos hogares (M2)
Descomposición contable de la variación de hogares (ΔH) en tres efectos: tamaño de la población (nacionalidad española o extranjera), estructura por edad y tasa de jefatura. Los componentes se asignan con valores de Shapley, de modo que el resultado no depende del orden. La ruptura de la EPA en 2021 se corrige retirando el salto persistente.

| Periodo | ΔH (miles) | Población española | Población extranjera | Estructura por edad | Tasa de jefatura |
|---|---|---|---|---|---|
| 2008-2013 | 1.321 | 416 | −7 | 500 | 413 |
| 2014-2019 | 322 | 101 | 63 | 388 | −230 |
| 2021-2025 | 1.011 | 90 | 563 | 198 | 160 |

- [C1] El total de 2021-2025 es C1: la ECP da 982.000 y la EPA corregida, 1.013.000.
- [C4] Los componentes son C4, porque la jefatura por edad solo existe en la EPA (fuente única). La segunda fuente sería una tabulación censal a medida, pedida en la solicitud S7.
- [C4] La participación del componente de nacionalidad extranjera varía entre el 53 % y el 76 % de ΔH en 2020-2025, según cómo se corrija la ruptura de la EPA.
- Entre 2011 y 2021 el censo (+456.000) y la EPA corregida (+1.111.000) discrepan, y no se resuelve cuál es correcta.

**Demanda latente juvenil (C2).**
- Con la jefatura de 2008 aplicada a la población actual:
  - 16-34 años: entre −22.000 y +23.000 hogares, según la referencia;
  - 20-34 años: entre +84.000 y +161.000;
  - 35-44 años: −710.000, porque ya forman más hogares que en 2008.
- En el conjunto de edades no hay demanda latente neta.
- Con la tasa de convivencia con los padres, la demanda latente es de 188.000-506.000 hogares. Mide un concepto distinto (nota M2-C1).

### 1.4 Precios (M7)
| Medida | 2015-2025 | 2021-2025 | Capa |
|---|---|---|---|
| Precio de compra (INE IPV, valor tasado, Registradores, Notariado) | +44 % a +80 % | +24 % a +36 % | C1, en España y en las 17 CCAA |
| Alquiler (IPC de alquiler frente a SERPAVI) | +11 % a +43 % (2015-2024) | +6 % a +15 % (2021-2024) | C1 en dirección; cuantía no establecida (precio frente a stock de contratos) |

**Exuberancia (GSADF, C4).**
- Hay episodios explosivos en las dos medidas nacionales de precio/alquiler: 2011-13, 2017-19 y 2024-26. En las comunidades, 5 de 17 los muestran en ambas medidas.
- El test rechaza algo de más: un 12,7 % de rechazos con autocorrelación.
- Que un test detecte exuberancia no basta para identificar una burbuja.

Figuras:
- output/v4/M7/fig1_triangulacion.png
- output/v4/M7/fig2_bsadf_nacional.png

---

## 2. Geografía del déficit (M1)

### 2.1 Mapas y concentración
Figuras:
- déficit por provincia: output/v4/M1/figuras/M1_deficit_provincias_2021-2025.png;
- primeros municipios: M1_top20_municipios_2021-2025.png.

Todos los resultados provinciales y municipales son C4, porque los hogares provinciales salen de una sola fuente (la ECP).

- Déficit 2021-2025, suma de 52 provincias: 701.000-967.000 viviendas (Ministerio). Con Catastro, en las 48 provincias que cubre, 657.000-933.000.
- Concentración: 7 provincias acumulan el 50 % del déficit positivo (rango entre combinaciones 4-7) y 19 el 80 % (9-20). En municipios con datos del Catastro, 25 acumulan el 50 % y 133 el 80 %.
- Diez primeras provincias (mediana): Madrid 107.000, Barcelona 90.000, Valencia 69.000, Alicante 57.000, Murcia 39.000, Tarragona 28.000, Málaga 27.000, Baleares, Girona y Toledo.
- Excedentes: ninguna provincia en 2021-2025; 249 municipios, con 71.000 viviendas. En 2012-2025 hay excedente en 21 provincias (69.000 viviendas) y en 334 municipios (326.000).

### 2.2 Demanda latente por provincia (C2)
Se reparte por la población de 20-34 años de cada provincia, con la tasa de convivencia de 2008 como referencia: Madrid 50.000, Barcelona 42.000, Valencia 18.000, Sevilla 13.000, Alicante 13.000.

---

## 3. ¿Se puede construir donde falta? Clasificación territorial (M3)

### 3.1 Insumos
- Precio: valor tasado del Ministerio, por provincia y por municipio de más de 25.000 habitantes. En 415 municipios se usa el valor provincial.
- Suelo: precio del suelo urbano del Ministerio, repercutido con una edificabilidad supuesta (rango).
- Solares: Catastro, unidades urbanas de uso solar: 3,09 millones en 2026, frente a 24,3 millones residenciales. Sin territorios forales. El SIU no se pudo descargar.
- Coste de construcción en nivel: **sin fuente verificable**. Se suponen 900, 1.200 o 1.500 €/m², con un margen del 15-25 % (solicitud S5).

### 3.2 Brecha precio-coste
Se define como precio − coste × (1 + margen) − suelo repercutido.
- Por provincia va de −734 €/m² (Ciudad Real) a +2.208 €/m² (Madrid). Baleares está en +2.047 y Gipuzkoa en +1.667.
- Por depender de un coste supuesto, es C4.
- Glaeser y Gyourko interpretan una brecha grande como un posible «impuesto regulatorio implícito». Aquí no se afirma esa causa.

### 3.3 Clasificación (C4, coste supuesto)
| Clase | Provincias | Municipios (de 703) |
|---|---|---|
| 1. Falta y brecha positiva moderada, con solares | 0 | 0 |
| 2. Falta y precio > r·(coste + suelo): brecha precio-coste elevada | 16 | 298 |
| 3. Falta y brecha ≤ 0: no rentable al coste supuesto | 30 | 156 |
| 4. No falta | 0 | 247 |
| 9. Falta, sin dato de solares (forales) | 4 | — |

- La clase es estable en ≥80 % del multiverso en 22 de las 52 provincias.
- València ciudad está en la clase 2, con una estabilidad del 97 %.
- Los umbrales se fijaron en el código antes de clasificar, pero eso no puede comprobarse en git (limitación declarada).

**Lectura.** Donde la brecha es elevada (clase 2), que haya más oferta depende de que existan suelo, licencias y capacidad, no de la rentabilidad. Donde la brecha es negativa (clase 3), con el coste supuesto construir no sería rentable sin cambiar costes o suelo. Las dos lecturas dependen del coste supuesto.

---

## 4. Parque frente a mercado (M4)

### 4.1 Stock (Censo 2021, fuente única: C4)
| Uso | Viviendas | % |
|---|---|---|
| Principales | 18,54 M | 69,6 |
| Vacías (consumo eléctrico) | 3,83 M | 14,4 |
| Uso esporádico | 2,52 M | 9,5 |
| Turísticas (INE, mayo de 2026) | 0,34 M | 1,3 |

- Tenencia de las viviendas principales: propiedad 75,5 %, alquiler 16,1 %, cesión u otras 8,4 %.
- El 46,8 % de los hogares tiene otras propiedades inmobiliarias (EFF).
- Titularidad por tipo de titular (persona física o jurídica): **no hay datos** (solicitudes S1 y S3).

### 4.2 Flujos
**Compraventas por compradores extranjeros, 2025 (C4).** Las fuentes no son independientes, y Registradores usa otra definición.

| Fuente | Total | Residentes | No residentes |
|---|---|---|---|
| Ministerio | 16,9 % | 10,1 % | 6,8 % |
| Notariado | 18,8 % | 11,6 % | 7,2 % |
| Registradores (2023-2025) | 13,8-15,0 % | — | — |

Por zonas, el 72 % de las compras de extranjeros se hace en provincias de costa e islas, frente al 58 % del total de compraventas. La clasificación de costa e islas es un supuesto, con sensibilidad en tablas/.

**Personas jurídicas (INE ETDP, 2024, C4).** Son el 11,3 % de los compradores (5,6 % en 2007) y el 24,7 % de los vendedores. Los vendedores incluyen promotores y entidades financieras, así que esa cifra no mide el stock en manos de empresas.

**Contratos de alquiler.** Las fianzas de Incasòl (Cataluña) no informan del tipo de arrendador, de modo que el peso de las empresas en el alquiler no se puede medir (ficha M4-V2: NO ANALIZADA).

---

## 5. Matriz de instrumentos (M5)

**Procedencia.** Se recogieron 88 medidas de 9 documentos oficiales o de programas; uno se leyó en una copia no oficial y 2 programas no fueron accesibles. Están agrupadas en 29 instrumentos, más 4 no propuestos. Se evalúan instrumentos, no partidos; la procedencia está en data/raw/v4/medidas_programas.csv.

**Rúbrica.** Es idéntica para todos los instrumentos (output/v4/M5/matriz_instrumentos.md). Resumen:

| Instrumento | Documentos que lo proponen | Evidencia (capa) | Efecto sobre el esfuerzo de acceso | Plazo | Riesgo principal | Signo estable |
|---|---|---|---|---|---|---|
| Más construcción donde falta | transversal | C2 (P-D v3) | −24,4 % a −0,8 % (+50.000/año) | medio-largo | suelo, licencias, capacidad | sí |
| Movilización de vacías (incentivos, recargo) | 4 | C2 (P-D); Segú (2020): vacancia −13 % relativo en Francia | −4,5 % a −0,1 % (10 %); hasta el 51 % de la brecha (30 %) | corto-medio | vacías mal medidas | sí |
| Parque público o social | 7 | C2 (P-D, dominancia débil) | −13,1 % a 0 % (25.000/año) | largo | desplazamiento de la promoción privada; coste | ≤ 0 (posiblemente nulo) |
| Topes al alquiler | 6 | C4 propio; Jofre-Monseny et al. (2023): −4,5 %; Diamond et al. (2019): −15 % oferta | −2,9 % a +7,3 % (inquilinos) | inmediato | reducción o desvío de oferta | no |
| Regulación de turísticos | 3 | C2 cantidad, C4 precio | −1,7 % a 0 % nacional | corto | desvío a temporada | no |
| Ayudas a la demanda (avales, alquiler, fiscalidad de la compra) | 7 | C4; Gibbons y Manning (2006): 60-67 % a arrendadores; Carozzi et al. (2024): precio al alza sin más construcción con oferta rígida | el 13-88 % de la ayuda se traslada al precio | inmediato | capitalización | no |
| Suelo público y colaboración público-privada | 7 | sin evaluar | — | medio-largo | volumen de suelo | — |
| Licencias y seguridad urbanística | 2 | Hilber y Vermeulen (2016) (magnitud no extraída) | — | corto-medio | — | — |
| Densidad, industrialización, fiscalidad del suelo, rebajas fiscales a la construcción, seguridad jurídica frente a la ocupación ilegal, límites a no residentes | 0-3 | sin evaluar | — | — | — | — |

**Distribución**, es decir, quién gana y quién pierde: ver la columna correspondiente de la matriz.

**Dónde funciona cada uno** (clases de M3, C4):
- Las medidas de oferta tienen más margen en las clases 1 y 2.
- Las ayudas a la demanda se capitalizan más en las clases 2 y 3, donde la oferta es rígida.

**Lectura.** En la simulación, solo las medidas que añaden viviendas donde hay demanda tienen signo estable en toda la rejilla. Ninguna simulación incluye costes, por lo que la tabla no ordena por coste-beneficio.

---

## 6. Módulo València

| Indicador | València ciudad | Provincia de València | Capa |
|---|---|---|---|
| Déficit contable 2021-2025 (hogares por censo anual frente a altas en el Catastro) | 13.000 (fuente única) | 59.000-80.000 (mediana 69.000) | C4 |
| Componente de nacionalidad extranjera en ΔH 2021-2025 (provincia) | — | 69 % de 79.000 hogares | C4 |
| Clase M3 (coste supuesto) | 2: brecha precio-coste elevada (estabilidad 97 %) | 2 (estabilidad 42 %) | C4 |
| Brecha precio-coste central | +1.217 €/m² | +243 €/m² | C4 |
| Vacías / uso esporádico / turísticas (Censo 2021; VUT 2026) | 8,8 % / 7,3 % / 1,3 % | — | C4 |
| Viviendas turísticas, ciudad, oleadas de agosto (INE) | 6.899 (2020) → 7.976 (2024); mayo 2025-2026: 6.553 → 5.393 | — | C4 |
| Esfuerzo (2023): precio/renta; alquiler/renta | 3,8 años; 18,1 % | 3,0 años; 16,3 % | C4 |
| Precio de compra 2015-2025, Comunitat Valenciana | — | en el rango C1 de las 17 CCAA (output/v4/M7/tablas) | C1 |

**Lectura.**
- La provincia de València es la tercera en déficit contable 2021-2025.
- En la descomposición contable, el componente de nacionalidad extranjera tiene más peso que en el conjunto nacional.
- La ciudad está en la clase 2: con el coste supuesto, el precio supera holgadamente coste más suelo. Si hace falta más oferta, depende de suelo y licencias más que de la rentabilidad.
- Las viviendas turísticas de la ciudad están en 2026 por debajo del nivel de 2021 en la comparación del mismo mes.

---

## 7. Qué no se puede afirmar y qué datos faltan
Ver docs/v4/preguntas_abiertas.md, con 10 preguntas priorizadas, y docs/v4/solicitudes.md, con las solicitudes S3-S10.

Lo más relevante:
- titularidad del stock y del alquiler por tipo y tamaño de titular;
- coste de construcción en nivel;
- suelo urbanizable (SIU);
- alquiler de contratos nuevos desde 2025;
- jefatura por edad en los censos;
- plazos de licencias.

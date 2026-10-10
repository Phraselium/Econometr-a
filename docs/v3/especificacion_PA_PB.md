# Especificación P-A (hechos, C1) y P-B (cotas, C2) — fijada antes de calcular

Datos: paneles completos vía `holdout.load_full(nombre, uso)`. Todas las evaluaciones selladas de v2 ya se hicieron y cada lectura queda registrada. Datos v3 nuevos en data/raw/v3/. Magnitudes en viviendas, hogares, €/mes y %.

**Regla C1.** Cada hecho necesita ≥2 fuentes independientes. La incertidumbre de medida se da como el rango entre fuentes, con el error muestral cuando exista (EPA, ECV, EFF). Si solo hay una fuente, el hecho baja a C4 («hecho de fuente única») y se dice así.

## P-A (C1)

### A1 · Déficit acumulado y su geografía
Fórmula, años 2002-2025: D(t0,t1) = Σ Δhogares − Σ (terminadas − bajas del parque).
- **Hogares**, tres fuentes: ECP del INE (desde 2013); EPA (hogares, trimestral, con quiebre en 2021); Censos 2011 y 2021 (dos puntos).
- **Terminadas**, dos fuentes:
  - certificados de fin de obra del MIVAU, libres y protegidas;
  - variación del parque estimado del MIVAU, o de las unidades urbanas residenciales del Catastro.
- **Bajas del parque**: 0 %, 0,1 % y 0,2 % anual. Es un supuesto, y su efecto se informa por separado.
- **Variantes**: con y sin vivienda protegida, nacional y por provincia. Periodos: 2002-2007, 2008-2013, 2014-2019, 2020-2025 y acumulado 2014-2025.
- **Cifras que se informan**: el rango entre combinaciones de fuentes (es la incertidumbre de medida) y el rango con bajas. Se compara con la cifra del BdE DO 2432 (de docs/v3/literatura_v3.md).
- **Advertencia**: un «déficit» contable no equivale a demanda insatisfecha a cualquier precio.

### A2 · Demanda latente (jóvenes que viven con sus padres)
- **Tasa de jóvenes de 25-34 años que viven con sus padres**, tres fuentes: Eurostat ilc_lvps08, Censo 2021 y ECV o EPA.
- **Hogares implícitos** = (tasa observada − tasa de referencia) × población 25-34 / personas por hogar joven.
  - Tasas de referencia: España 2008 y media UE-27 del último año.
  - Personas por hogar joven: rango de 1,5 a 2,0. Si el Censo lo da, se usa el tamaño medio de los hogares con persona de referencia de 25-34 años.
- **Resultado**: un rango, en hogares y en viviendas, por CCAA donde haya datos.

### A3 · Desajuste de la vacancia
- **Medidas de vivienda vacía**, por municipio:
  - Censo 2021: vacías y de uso esporádico (estimadas por consumo eléctrico);
  - segunda medida: unidades residenciales del Catastro − hogares (padrón o censo) − viviendas turísticas.
- **Presión**: terciles municipales de Δ ln valor tasado 2015-2021 (y de 2021 a la última fecha) y de Δ ln alquiler SERPAVI. Se añade la marca de zona tensionada.
- **Resultado**:
  - % de las vacías del país situadas en municipios del tercil alto de presión, frente al tercil bajo;
  - vacías por cada 100 hogares nuevos, por tercil;
  - el mismo cálculo en municipios de más de 50.000 habitantes.

### A4 · Esfuerzo de acceso
- **Ratios** por provincia y, donde haya datos, por municipio:
  - precio/renta = valor tasado × 80 m² / renta neta media del hogar (Atlas de renta, ADRH);
  - alquiler/renta = alquiler SERPAVI (o fianzas, que es la fuente independiente) × 12 / renta;
  - cuota hipotecaria / renta, con el tipo hipotecario de cada año, plazo de 25 años y LTV del 80 %.
- **Por edad**: renta por edad de la ECV, o salario por edad de la EES. Si solo hay una fuente, se marca.
- **Segunda fuente de precio**: Notariado o Registradores, ya extraídos en v1 y v2.

### A5 · Tenencia por edad
Propiedad, alquiler y cesión por edad del cabeza de familia o de la persona de referencia. Fuentes: EFF (2002-2022, tablas publicadas), ECV o Eurostat ilc_lvho02, y Censo 2021. Este es el hecho sobre la pregunta original del proyecto: quién posee y quién alquila.

### A6 · Divergencia precio-alquiler y coste de uso
- **Ratio precio/alquiler** en dos versiones: índice IPV/IPC de alquiler, y niveles valor tasado/SERPAVI. Se comparan ambos.
- **Coste de uso de Poterba** (v2: coste_uso_aprox), con un rango de supuestos de depreciación y de ganancia esperada.

## P-B (C2) — cotas con supuestos débiles y explícitos

En cada factor se dan cuatro cosas:
1. la cota superior de su contribución a la subida, nacional y por zona, con el supuesto extremo que la produce;
2. qué parte de la subida NO puede explicar aunque se le atribuya todo;
3. la cota inferior cuando exista;
4. la sensibilidad a cada supuesto.

### B1 · Viviendas turísticas
- **Peso**: viviendas turísticas (INE) sobre el parque y sobre las viviendas en alquiler (hogares en alquiler del Censo 2021), por municipio y sección.
- **Cota de cantidad**: sustitución 1:1, es decir, cada vivienda turística nueva es una vivienda de alquiler menos. Desplazamiento máximo de la oferta de alquiler = ΔVUT / stock de alquiler.
- **Cota de precio**: Δ ln alquiler máximo = (ΔVUT/stock de alquiler) / |ε_d,min|, donde ε_d,min es la elasticidad-precio de la demanda de alquiler más baja del rango de la literatura (lit. v3, parte B); también con el valor central.
- **Lo que no puede explicar**: la parte de la subida nacional del alquiler (media ponderada por stock) que ocurre en municipios donde las viviendas turísticas apenas crecieron (ΔVUT/stock < 0,1 punto). Supuesto: sin efectos de desbordamiento más allá del municipio; se informa también con un radio provincial.

### B2 · Inmigración
- **Hogares netos creados** por población extranjera o nacida fuera (ECP por nacionalidad o padrón ÷ tamaño medio del hogar extranjero) frente a la oferta neta.
- **Cota superior**: el peso de esos hogares en Σ Δhogares es la máxima fracción del «déficit» A1 que puede atribuírsele.
- **Traducción a precio**: Δ ln p máximo = (hogares extranjeros netos / parque) / |ε_d,min|, en sus dos variantes: compra y alquiler.
- **Lo que no puede explicar**:
  - la subida en periodos y zonas con saldo extranjero nulo o negativo (2009-2014);
  - la parte de la demanda de la población nacional.

### B3 · Grandes tenedores
Queda **en espera** hasta recibir los datos de la solicitud de transparencia al Catastro. Ingesta preparada en `src/v3/ingesta_grandes_tenedores.py`. La cota se definirá con el mismo esquema que B1, sustituyendo el desplazamiento de oferta por la variación de la cuota de grandes tenedores en el alquiler.

### B4 · Tipos de interés (coste de uso)
- **Cota en el estado estacionario**: P/R = 1/uc. La contribución máxima de los tipos a Δ ln P es Δ ln(1/uc), con uc = tipo hipotecario (o tipo real) + depreciación + IBI − ganancia esperada, en el rango de supuestos.
- **Por periodo**: 2014-2021 (tipos a la baja) y 2022-2025 (tipos al alza).
- **Lo que no puede explicar**:
  - en 2022-2025 la subida de tipos predice una caída de P/R. La subida observada de precios no puede atribuirse a los tipos, porque el signo es el contrario;
  - la subida de los alquileres, sobre la que los tipos no actúan directamente.

## Potencia de P-C (oleada 1)
Para cada diseño P-C1 a P-C4 se calcula el efecto mínimo detectable (EMD, α = 0,05 bilateral, potencia del 80 %) con:
- el N de unidades;
- los periodos;
- la varianza intra-unidad del resultado;
- la correlación serial;
- la variación del tratamiento, después de quitar los efectos fijos.
El EMD se compara con el efecto económicamente relevante (EER) declarado aquí:
- P-C1, turísticos → alquiler: EER = +1 % de alquiler por cada punto porcentual de viviendas turísticas sobre el parque. Es el orden de magnitud de García-López et al. (2020); se ajustará con la parte A de la literatura.
- P-C2, caída de anuncios 2025-2026: EER = −1 % de alquiler por cada 10 % de caída de anuncios.
- P-C3, topes y zonas tensionadas sobre alquiler y cantidad: EER = −3 % de alquiler; −10 % de contratos.
- P-C4, suelo como moderador: EER = diferencia de 0,1 en la elasticidad del precio a un shock de demanda.

Regla: si EMD > EER, el diseño **no se estima** y se informa como «no detectable con los datos disponibles».

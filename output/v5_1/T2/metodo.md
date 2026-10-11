# T2 · método (viviendas liberadas por envejecimiento)

**La vivienda liberada NO se resta de la necesidad: la proyección de hogares del INE (tabla 54562) ya la descuenta.** Esta tabla da la cifra de oferta liberada y su llegada al mercado; no corrige B1.

Capa: C4 (parámetros de residencias y destino de la vivienda sin dato propio). Evidencia: EXPLORATORIO. Veredicto máximo: ANALIZADA, NO CONCLUYENTE. Los rangos son de supuestos, no intervalos de confianza.

## Definición
Una vivienda se libera al disolverse el último miembro del hogar: (i) fallecimiento del último miembro; (ii) traslado a residencia de quien vivía solo.

## Fórmula (por provincia, periodo)
1. Defunciones 75+: población proyectada por edad (INE 36726) × riesgo anual de muerte 2024 por tramo (INE 67235), como B1.
2. Fallecimiento: h65 × factor × disolución × D75 × (1 − s_res × solo). h65 = 0,5675 (v4/M2, 2025); factor 0,85/1/1,15 y disolución 0,5/0,75/1 (mismas ternas que B1). s_res = cuota de defunciones 75+ ocurridas en residencia = r·RR/(r·RR+1−r), con RR = 2. Sin la corrección, el resultado reproduce B1 (141.526/año).
3. Residencia: población 75+ × (r/estancia) × solo. r = 4/6/8 % de los 75+ en residencia; estancia 4/3/2,5 años; solo = 30/45/60 %. Los entrantes en pareja no disuelven el hogar hasta el fallecimiento del último.
4. Mínimo = ruta que menos libera en cada componente; máximo, al revés.
5. Parámetros de residencias (r, estancia, solo, RR): sin dato propio (Censo 2021 por edad en establecimientos colectivos e IMSERSO no accesibles; docs/v5_1/fuentes_fallidas.md). NO VERIFICADOS.
6. 2036-2040 es escenario: mortalidad de 2024 constante (sesgo al alza) y proyección INE corto plazo (2026-2041).

## Tipo de municipio (regla declarada)
Atlas de Áreas Urbanas no disponible (403). Regla: `capital` (capital de provincia); `entorno_grande` (resto de municipios con ≥50.000 habitantes, Censo 2021, de la misma provincia); `resto`. El reparto provincial → municipio usa la población 65+ del Censo 2021 (proxy de 75+). Los 142 municipios ≥50.000 son una aproximación del entorno metropolitano; no es área funcional.

## Tenencia
ECV 2025, hogares con persona de referencia 65+: propiedad 88,2 %, alquiler 7,8 %, cesión 4,1 %. Se escala por municipio con la estructura relativa de tenencia del Censo 2021 y se normaliza a 1.

## Qué parte llega al mercado
- Propiedad: 1 − X. X mínimo = viviendas vacías / parque total de la provincia (Censo 2021); X máximo = (vacías + secundarias)/parque. Supone que la vivienda liberada tiene la misma probabilidad de quedar fuera del mercado que el parque medio (C4; puede subestimar: vivienda más antigua, herencias indivisas, reforma).
- Alquiler: vuelve al titular, 80-100 %. Cesión: 30-80 %. (Supuestos C4.)
- Herencias (INE ETDP 6154): 203.393 viviendas/año (media 2023-2025), frente a 118.075/año de liberadas por fallecimiento en propiedad (modelo). Las inscripciones incluyen segundas viviendas y viviendas de personas menores de 75; sin seguimiento posterior de la vivienda heredada. Sin dato de venta o alquiler posterior: rango con supuestos.

## Desajuste territorial
Provincias A4 clase 1-2 (necesidad): 97 % de las liberadas. Municipios clase 1-2 (703 clasificados): 65 % de las liberadas en municipios con clase; 28 % de las liberadas cae en municipios sin clase (sin precio).

## Sensibilidad X
Como L no se resta de la necesidad, la parte que no llega al mercado (X × L) se lee como un **aumento posible de la necesidad efectiva** respecto a la que el INE da por absorbida: 24.548-46.580 viviendas/año (central 35.564), un 11-22 % de la necesidad central de B1 (214.868/año). Prueba de estrés X = 50 % (sin dato): 43 %.

## Fechas de datos
INE 54562 (mod. 2026-06-17); INE 36726 (2026-2041); INE 67235 (2024, mod. 2025-11); Censo 2021 (referencia 1-ene-2021); ECV 9994 (2025); ETDP 6154 (2014-2025). A4 y B1 de output/v5.

## Entregables
tablas/liberadas_provincia.csv (52 provincias × 3 tipos × 2 periodos; liberadas del periodo, no anuales), tablas/liberadas_detalle.csv, resultado.json, hechos.json, fichas_verificador.json, control_sumas.json, registro.csv (Registry; sin contrastes, p no aplica, Holm/BH no aplica).

# Cierre de V9 COMPLETO (2026-10-15)

## Qué se ha identificado y con qué capa

**Nada alcanza C3 ni C3s.** Las reglas se fijaron antes de estimar (docs/v9/hipotesis.md y docs/v9/hipotesis_addendum_a1.md) y no se relajaron después.

| Diseño | Resultado principal (cifras_clave) | Capa | Por qué no es C3 |
|---|---|---|---|
| D1b Ley catalana 11/2020 | Renta de contratos nuevos: diferencia de −5,9 % (V9-D1b-renta-att) | C4 | Supera pretendencias, placebo de fecha, permutación y Holm. No supera la robustez a desviaciones de tendencia: IC de Rambachan y Roth con M̄ = 1 que contiene el 0; M̄ de ruptura 0,5 |
| D1a Zonas tensionadas (Cataluña) | Renta: −5,8 % (V9-D1a-renta-att) | C4 | Pretendencias y placebo de fecha rechazados; M̄ de ruptura 0,2 |
| D1a/D1b Número de contratos | Sin diferencia detectable | C4 | Exploratorias, sin potencia |
| D1c Euskadi | Diferencia negativa, pocos trimestres | C4 | Exploratorio; pretendencias rechazadas |
| D2 Turísticos × COVID | Asociación positiva tras la reapertura | C4 | Exploratorio; pretendencias rechazadas; no se mantiene con tendencia por dosis |
| D3 Caída del registro VUT (CP) | Descriptivo | C4 | Sin potencia; el placebo 2021→2023 muestra una asociación del mismo signo |
| D4 Inmigración (shift-share) | No concluyente | C4 | Instrumento débil (F efectiva < 5); pretendencias de las cuotas con mayor peso de Rotemberg |
| D5 Tipos × tipo variable | Precio: no distinguible de 0; alquiler: asociación negativa a 4 trimestres | C4 | Exploratorio, sin potencia |
| D6 Bono Alquiler Joven | — | — | No estimable: sin edad exacta ni receptores |
| D7 Hogares (contable) | Componente población: 92 % en España y 112 % en la C. Valenciana (stocks 1-1-2022 → 1-1-2025) | C4 (contable); C1 en el contraste censo-ECP | Identidad, no atribución |

**Cotas de contribución a la subida (F4): vacías.** Sin C3/C3s, ningún factor tiene parte acotada de la subida nacional ni de la de la Comunitat Valenciana (publicacion/cotas_v9.md).

## Qué no se ha podido identificar y por qué

- **Regulación.** Los municipios con zonas tensionadas ya evolucionaban de otra forma, hay pocos controles completos y no hay garantía de robustez a desviaciones de tendencia.
- **Pisos turísticos.** No hay exposición fechada ni resultado por barrio o código postal con frecuencia suficiente.
- **Inmigración.** El instrumento de redes de origen es débil con 50 provincias.
- **Tipos de interés.** Con 18 países no hay potencia para la interacción.
- **Bono Alquiler Joven.** Falta la edad exacta y la identificación de los receptores.

## Datos que lo resolverían (solicitudes en docs/v9/solicitudes_transparencia.md)

1. **Fianzas por barrio o código postal y mes** (GVA y Incasòl): convertirían D3 en un evento mensual y darían más controles a D1.
2. **Registro de turismo con altas y bajas fechadas** (Generalitat de Catalunya; cortes de la GVA): exposición dinámica para D2 y D3.
3. **Titularidad agregada del Catastro:** concentración de la propiedad (pregunta abierta, fuera de D1-D7).
4. **Beneficiarios del Bono Alquiler Joven por edad en meses:** D6.

## Siguiente paso

El siguiente paso es **la revisión humana y la publicación**: publicar las etiquetas y la release del pre-registro, revisar la web y los textos, y depositar el DOI. **No** es otra versión de modelización, salvo que lleguen datos nuevos (fianzas por barrio, titularidad del Catastro o las otras solicitudes de arriba). Con los datos públicos actuales, V9 agota los diseños de identificación razonables. Repetir el ejercicio con otras especificaciones sería buscar significación.

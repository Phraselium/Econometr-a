# Plan v9: diseños prioritarios replicables con datos públicos (V9-PREP)

Fecha: 2026-10-14. v9 solo se abre si llegan datos nuevos (docs/v8/cierre_proyecto.md, punto 6). Estos diseños usan fuentes públicas del bloque 1 ([fuentes_datos.csv](fuentes_datos.csv)), métodos del bloque 3 ([metodos.csv](metodos.csv)) y literatura del bloque 2 ([literatura.csv](literatura.csv)).

Cada diseño exigiría su propio pre-registro, su validación por Monte Carlo de las herramientas nuevas, su validación diferida y su revisión independiente, como en V7-V8.

Los costes son estimaciones de tokens de subagentes, con los órdenes de V8 como referencia (un módulo con datos ya preparados costó entre 70.000 y 220.000).

## Orden de prioridad

| # | Diseño | Pregunta | Capa a la que aspira | Coste | Riesgo principal |
|---|---|---|---|---|---|
| 1 | Zonas tensionadas: DiD escalonado + Honest DiD | ¿Qué hizo la declaración de zona tensionada (Ley 12/2023) al alquiler y a la oferta de contratos? | C3 si pasan pretendencias y placebos | 0,6-0,9 M | Pocos municipios tratados fuera de Cataluña; medidas de oferta discutibles |
| 2 | Pisos turísticos en València por sección | ¿Cuánto se asocian las viviendas turísticas con el alquiler y con la población residente por sección? | C4, o C3 con un instrumento de licencias o moratorias | 0,5-0,8 M | Inside Airbnb no es oficial; ruptura de la serie VUT en 2024 |
| 3 | Réplica y ampliación de Sanchis-Guarner, 2015-2025 | ¿Cuál es el efecto directo de la inmigración sobre precios y alquileres y cuánto se compensa por la reubicación de nativos? | C3 si el shift-share supera los diagnósticos | 0,6-1,0 M | Instrumento débil (como en V8); cuotas iniciales endógenas |
| 4 | Bono Alquiler Joven: discontinuidad por edad | ¿Aumentó la emancipación o el alquiler pagado de los jóvenes elegibles? | C3 si la RD pasa densidad y placebos | 0,4-0,7 M | Muestra de la ECV pequeña en torno al corte; sin datos de beneficiarios |
| 5 | Reconciliación del déficit y descomposición de hogares | ¿Por qué difieren las cifras de déficit (BdE, OCDE, proyecto) y qué parte del crecimiento de hogares es población frente a tamaño del hogar? | C1/C4 (contable) | 0,2-0,3 M | Bajo; depende del acceso a las tasas de jefatura por edad |

## 1. Zonas tensionadas (Ley 12/2023): DiD escalonado con Honest DiD

- **Datos.**
  - Fianzas del Incasòl por municipio y trimestre, 2007-2026 (F06); los primeros municipios catalanes se declararon en 2024 (número y fechas por verificar en el DOGC y el BOE).
  - SERPAVI por sección y municipio, hasta 2024 (F04).
  - IPVA por municipio, nuevos y existentes (F03).
  - Fianzas de la GVA (F05), como control, si la Comunitat Valenciana sigue sin declarar zonas (verificar antes de usarla).
  - Las fechas de declaración por municipio se toman del BOE y los diarios oficiales.
- **Método.**
  - Callaway-Sant'Anna (M01) y Sun-Abraham (M02) para el efecto por cohorte de declaración.
  - Honest DiD (M08) para la sensibilidad a la tendencia previa.
  - Synthetic DiD (M05) como robustez.
  - Wild cluster bootstrap (M23), por los pocos clústeres de comunidades.
- **Resultados.**
  - Alquiler medio de los contratos nuevos.
  - Número de contratos nuevos (oferta efectiva).
  - Stock en SERPAVI.
  - Como contraste, anuncios de portales (F36, privado, no redistribuible).
- **Pregunta crítica.** Resolver la contradicción 1 (contradicciones.md): ¿caen los contratos o solo los anuncios?
- **Riesgo.**
  - Fuera de Cataluña hay pocos municipios declarados y muy recientes.
  - Los efectos de anticipación del anuncio de la ley.
  - El paso a contratos de temporada, invisible en las fianzas si no se desagregan.

## 2. Pisos turísticos en València: panel por sección

- **Datos.**
  - INE VUT por sección, semestral desde 2020 (F02).
  - Inside Airbnb València (F14; CC BY 4.0, no oficial, solo robustez).
  - Registro de turismo de la GVA (F20).
  - Censo anual de población por sección (F01).
  - Fianzas de la GVA por municipio o código postal (F05).
  - Datos abiertos del Ajuntament por barrio (F18-F19).
- **Método.**
  - Panel de secciones con efectos fijos y tendencias por distrito, con errores de Conley (M22).
  - Dos fuentes de variación posibles:
    - las moratorias o limitaciones municipales de nuevas licencias turísticas (DiD o RD espacial en la frontera de la zona afectada, M15);
    - un shift-share con la exposición turística previa.
  - Comparación con García-López et al. (2020, LA01) y Chaves-Fonseca (2026, LA02).
- **Riesgo.**
  - La serie VUT tiene una ruptura en 2024.
  - La nacionalidad por sección no está confirmada en el censo anual.
  - Las fianzas no están por sección.

## 3. Inmigración y precios 2015-2025: réplica de Sanchis-Guarner

- **Datos.**
  - Padrón continuo por nacionalidad y municipio (F32).
  - Valor tasado por provincia y municipios grandes, IPVA (F03) y SERPAVI (F04).
  - Flujos por país de origen (INE EVR) para las cuotas iniciales.
- **Método.**
  - Descomposición del efecto total en directo e inducido por la reubicación de nativos (M21, Sanchis-Guarner 2023, LA07).
  - Shift-share con los diagnósticos de Goldsmith-Pinkham, Sorkin y Swift y de Borusyak, Hull y Jaravel, e inferencia AKM (M09-M11).
- **Por qué.** Es la contradicción 4: el signo cambia según el periodo y la escala. Además, V8 tenía el empuje migratorio débil a nivel nacional; con municipios hay mucha más variación.
- **Riesgo.**
  - Instrumento débil.
  - Endogeneidad de las cuotas de 2002 si los inmigrantes eligen dónde asentarse por los precios.

## 4. Bono Alquiler Joven: discontinuidad por edad

- **Datos.**
  - ECV microdatos, con alquiler pagado, edad y régimen de tenencia (F29).
  - EPA microdatos para la emancipación (F29).
  - Estadística de beneficiarios del Ministerio y de las comunidades, si se publica: no localizada como abierta.
- **Método.**
  - RD por edad (corte en 35 años), con inferencia robusta (M12-M14).
  - Test de manipulación de la variable de asignación (M14).
  - DiD frente a hogares de 36 a 40 años como alternativa.
- **Literatura.** Aparicio-Fenoll y Oppedisano (2015, LB16) sobre la Renta Básica de Emancipación, con su efecto sobre la emancipación. Sobre capitalización, la contradicción 3: Francia y Reino Unido frente a Finlandia.
- **Riesgo.**
  - Muestra pequeña en torno al corte.
  - La edad es discreta (anual).
  - No hay una evaluación previa con la que comparar.

## 5. Reconciliación del déficit y descomposición del crecimiento de hogares

- **Datos.**
  - ECP y EPA por edad y CCAA.
  - Censo 2021 (F35).
  - Proyección de hogares 2026-2041 (F31).
  - Terminadas del Ministerio.
  - Bajas del parque (v5.1).
- **Método.**
  - Descomposición contable (shift-share demográfico) del crecimiento de hogares de 2021-2025: efecto población, efecto estructura por edad y efecto tasas de jefatura.
  - Reproducción con los mismos supuestos de las cifras del Banco de España (unas 750.000), de la OCDE (unas 600.000) y del proyecto (706.000-735.000).
- **Por qué.** Es barato, responde a la contradicción 6 y alimenta la pregunta de hogares_vs_viviendas.md. No exige identificación causal.

## Qué no se propone

- **Grandes tenedores e inversores (contradicción 2).** Sin datos de propiedad (registrales, no abiertos) no hay diseño creíble.
- **Alquiler de temporada y por habitaciones.** No hay datos oficiales; se pediría a la GVA y al Incasòl la desagregación de las fianzas por duración.
- **Expectativas frente a crédito (contradicción 7).** No hay una serie pública de expectativas de precios con la longitud necesaria.

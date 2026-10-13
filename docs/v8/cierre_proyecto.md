# Cierre del proyecto (V8)

Fecha: 2026-10-13. Autor: Borja Romero, economista (firma individual, independiente). Las cifras citadas llevan su identificador de `output/v5/cifras_clave.csv`; el detalle está en output/v8/por_que_ha_subido.md, output/v8/informe_econometrico.md y output/v8/F5/fichas.md.

## 1. Qué responde V8 y con qué capa

| Pregunta | Respuesta | Capa |
|---|---|---|
| Peso de cada factor por periodo y mercado | Descomposición histórica del SVAR con bandas del 68 % para cinco shocks (actividad y renta, demográfico, crédito y tipos, demanda de vivienda y oferta) en P1-P5; dominancia, LP-IV, contabilidad hogares-viviendas y SHAP como métodos adicionales o de contraste. Casi todas las bandas del SVAR incluyen el cero. | C3s (SVAR, condicionado a las restricciones de signo y de cero); C4 (resto) |
| Factor más relevante | **No se designa en ninguno de los diez casos** (`V8-REGLA-*`): el máximo de métodos coincidentes es dos de cuatro (`V8-VOTOS-*`). El caso más próximo, actividad y renta en la compra de 1995-2007, tiene banda que excluye el cero (`V8-SVAR-c-P1-empleo_renta-media`) y signo estable en el multiverso, pero un solo voto. | C3s / C4 |
| Ecuaciones significativas y robustas | Ningún modelo cumple a la vez la regla de periodo y la del multiverso. Dos combinaciones cumplen el multiverso (demografía en el alquiler, P2 y muestra completa; `V8-M7-cumplen`). Los efectos por periodo que cumplen la regla no sobreviven a BH (`V8-M0-cumplen`). | C4 |
| Componente común | La subida de 2022-2026 es la más común entre comunidades (`V8-M1-cuota-c-P5`); H8-8 (más de la mitad en cada periodo) no se sostiene. El factor común español covaría con la zona euro (H8-9, `V8-H8-9-est`, `V8-H8-9-pholm`). La parte europea solo es distinta de cero en la crisis (`V8-M1-eur-c-P2`). | C4 |
| Hipótesis confirmatorias | Solo H8-9 se sostiene tras Holm. H8-1 a H8-8, no. | C3s / C4 |
| Predicción | Ningún modelo mejora a un AR(4) en la muestra común (`V8-OOS-*`). Predicciones de 2026T3-2027T2 congeladas. | C4 |

## 2. Qué no pudo hacerse y por qué

- **Identificación principal del SVAR.** La tabla pre-registrada (signos en dos trimestres más cuatro ceros) no aceptó ninguna rotación con los datos reales; se usó la variante V3 pre-registrada (solo impacto). docs/v8/bloqueos.md.
- **Lectura causal externa (C3).** Los tres instrumentos son débiles (`V8-H8-5-F`, `V8-H8-6-F`, `V8-H8-7-F`; `V8-M5-c3`). La primera etapa de los shocks del BCE tiene el signo contrario al esperado.
- **Designar un factor.** Con LP-IV abstenido, solo la demografía podía reunir tres votos por construcción, y no los reúne.
- **Regla de periodo para el alquiler.** No hay medida alternativa trimestral nacional; queda «no evaluable».
- **Cointegración.** No se demuestra una relación de largo plazo estable (`V8-M4-ardl-rechaza`), así que la contabilidad de largo plazo no vota.
- **Nivel regional.** Sin SVAR regional, no se designa factor por comunidad, provincia ni para València ciudad; las cifras regionales son descriptivas.
- **ECM v1 canónico en cada módulo.** Se resolvió con una tabla común de predicción (F5); dentro de cada módulo la comparación es frente a AR(4).

## 3. Qué solo resolverían datos nuevos y quién los tiene

| Dato | Para qué | Quién lo tiene |
|---|---|---|
| Índice trimestral nacional de alquiler de contratos nuevos | Medida alternativa del alquiler (regla de periodo) y alquiler de mercado, no de parque | INE (índice de precios de vivienda en alquiler) y comunidades autónomas (depósito de fianzas) |
| Llegadas por país de origen y provincia de destino | Empuje migratorio con variación provincial (instrumento más fuerte) | INE (Estadística de Migraciones, explotación a medida) |
| Compras de vivienda por extranjeros por provincia y trimestre, serie larga | Demanda externa con datos suficientes | Consejo General del Notariado; Colegio de Registradores |
| Viviendas de uso turístico por municipio antes de 2020 y turismo antes de 2016 | Turismo con serie suficiente para separarlo del ciclo | INE (medición experimental), registros autonómicos |
| Crédito nuevo para vivienda por CCAA | Crédito y tipos en el nivel regional | Banco de España |
| Datos 2026T3-2027T2 | Evaluación limpia de las predicciones congeladas | INE, Ministerio de Vivienda (publicación ordinaria, 2027) |

## 4. Qué debe revisar un humano antes de difundir

1. La regla operativa del factor más relevante (docs/v8/desviaciones.md, R0-R8): se fijó tras la revisión de F4 y antes de calcular F5, pero cambia la forma de votar respecto al texto del pre-registro.
2. La corrección de la ficticia EPA (revisión F4, J1) y la publicación de las hipótesis retiradas (output/v8/M2/hipotesis_m2_retirada.csv).
3. La lectura de la parte no atribuida y de las colas largas de la posterior del SVAR (decisiones Y8-Y10): media y mediana discrepan en P5.
4. El contraste de turismo de M9: cifra alta, fuera de su banda, sin lectura causal. Comprobar que ningún texto derivado la presente como atribución.
5. Las referencias marcadas NO VERIFICADA y la neutralidad de las fichas del verificador V8 (output/v8/verificador_v8.md).
6. La release y la fecha verificable del pre-registro (docs/v8/tareas_autor.md).

## 5. Qué necesitará la fase posterior de propuestas y publicaciones

- Cifras: solo de `output/v5/cifras_clave.csv` (ids `V8-…`), con su capa y su banda. Las C3s, siempre «condicionado a las restricciones de signo y de cero».
- Mensajes que la evidencia sostiene: no hay un factor único designable; la subida reciente es muy común a todo el país; el precio español acompaña al europeo (asociación); el precio sigue su propia inercia a corto plazo.
- Mensajes que la evidencia no sostiene (output/v8/por_que_ha_subido.md, sección 8): que un único factor explique la subida, que la subida de tipos frenara el precio, que el turismo sea el motor, efectos causales de los instrumentos.
- Fichas del verificador V8 para evaluar afirmaciones concretas, siempre sobre la afirmación y nunca sobre quién la hace.
- Tablas en formato de revista (output/v8/tablas_modelos_destacados.md, output/v8/tablas_v8.xlsx).
- Fuera de V8 y no empezado: el análisis de propuestas de programas electorales y la divulgación (COEV, LinkedIn).

## 6. Declaración

**V8 es la última versión de modelización del proyecto.** Lo siguiente es solo:

- v8.x: correcciones tras revisión humana (cada error que cambie una cifra publicada va a ERRATA.md);
- la fase de propuestas y publicaciones, con las cifras de V8 y versiones anteriores vigentes;
- `make evaluate_v7` y `make evaluate_v8` en 2027, una sola vez cada uno;
- un v9 únicamente si llegan datos nuevos (punto 3).

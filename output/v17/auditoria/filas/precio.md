Análisis a posteriori (V17). Ficha de auditoría de la fila «precio» (D1, discurso político). Grupo demanda_precios. Capa de toda cifra nueva: C4. Ninguna cifra ni capa publicada cambia. Ids nuevos: V17-AUD-DP-PRE-*.

# «El precio ha subido un X %»

## 1. Texto auditado

> «El precio ha subido un X %»: de 2019 a 2025, +30 % nominal pero +7 % real por m²; con el índice del INE, +19 % real. Quien elige la cifra elige el mensaje.

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor.**
- **Las cifras son correctas** y salen de cifras_clave:
  - precio medio por m² de tres fuentes (MIVAU, Notariado y Registradores), +30,4 % nominal (29,6-31,7) y +7,1 % real (6,5-8,2) [C1];
  - IPV del INE, +44,4 % nominal y +18,7 % real [C4, fuente única] (informe integral, I.2).
- **La discrepancia es real.** Con medias anuales de la serie versionada, el valor tasado sube un 29,6 %, el Notariado un 29,7 % y los Registradores un 29,2 %, frente al 44,4 % del IPV.
- **La advertencia tiene sentido.** Elegir sin decirlo la medida que más conviene es un riesgo real de la divulgación.

**En contra.**
- **No es una elección entre equivalentes.** Las dos familias responden a preguntas distintas:
  - El IPV es un índice hedónico sobre las compraventas ante notario. Mide cuánto cuesta hoy, respecto a 2019, una vivienda de las MISMAS características. Es la base del índice armonizado de Eurostat para España, y la que usan para la variación del precio los informes del Banco de España leídos (IEF 2023-2026, IA2024 e IA2025; docs/v17/referencias/bde_informes.md).
  - El precio medio por m² mide cuánto se pagó, o se tasó, de media por m² de LO QUE SE VENDIÓ ese año, que no es lo mismo cada año.
  - El propio Banco de España advierte que los precios medios «no pueden considerarse índices de precios» (DO 2432, p. 17).
- **Para la pregunta «¿cuánto se ha encarecido la vivienda?», la respuesta de referencia es la del IPV.** La media por m² responde a otra pregunta: qué pagan de media los compradores, que ya han ajustado lo que compran.
- **«Real» frente a la renta, que es lo que mide el acceso, cambia el mensaje otra vez.**
  - Deflactado por la renta disponible bruta por hogar (+27,9 % en 2019-2025), el IPV sube un 12,9 % (12,0 % con la renta per cápita) (V17-AUD-DP-PRE-IPV-REAL-RENTA).
  - El valor tasado por m² sube un 1,4 % (V17-AUD-DP-PRE-TASADO-REAL-RENTA).
  - La vivienda de calidad constante pesa más en la renta del hogar que en 2019; la media de lo tasado, casi igual.

## 3. Pruebas mínimas (plan, fase 3, punto 2)

Script: src/v17/f3_demanda_precios.py.

**3.1 Por qué el IPV es la medida principal.** Controla por las características de la vivienda: localización, superficie, antigüedad y tipo. Así separa la variación del precio del cambio en lo que se vende. Los precios medios no lo hacen, y no son índices de calidad constante. La 1.0 da ambas sin elegir (informe integral, I.2: «no se elige una»). La lectura V17, según B5, toma el IPV como principal y la media por m² como complemento, con su sesgo explicado.

**3.2 Sesgo de composición, cuantificado en lo posible.**

| Prueba | Resultado 2019-2025 | Lectura |
|---|---|---|
| Valor unitario provincial (compraventas como pesos de cada año) frente a Laspeyres (pesos de 2019); 38 provincias sin muestra sellada | +24,4 % frente a +29,1 %: −4,8 pp (V17-AUD-DP-PRE-COMPOSICION-PROVINCIAS) | las compraventas se desplazan hacia provincias más baratas; una media ponderada por transacciones sube menos que el precio de cada provincia |
| Valor tasado por antigüedad (BdE SI 1.5) | total +29,6 %; hasta 5 años +31,4 %; más de 5 años +29,6 % (V17-AUD-DP-PRE-TASADO-ESTRATOS) | composición entre antigüedades: de 0 a −1,8 pp |
| IPV por tipo | nueva +60,3 %; usada +41,8 % | la vivienda nueva, poco del total, sube más |
| Brecha restante IPV − media por m² | ≈ 14-15 pp | composición DENTRO de cada provincia (barrio, tamaño, estado) y el propio ajuste hedónico del IPV. No es «tasación frente a transacción»: las tres medias por m² (tasación, Notariado y Registradores) coinciden. Con agregados no se separa: haría falta microdato notarial |

Conclusión:
- **Con agregados, la composición no explica la brecha.** El valor unitario ponderado por transacciones (+24,4 %) sube menos que el índice de pesos fijos (+29,1 %). Pero las medias publicadas (tasación +29,6 %, Notariado +29,7 %, Registradores +29,2 %) son casi iguales a ese índice de pesos fijos, no al valor unitario. Además, el cálculo excluye Madrid, Baleares y Canarias (bloques sellados v6). La brecha de ≈ 14-15 puntos con el IPV no se puede atribuir a la composición con estos datos.
- **El resto no se puede atribuir con estos datos.** No se afirma que todo sea composición.

**3.3 Variación real deflactada por renta y no solo por IPC.**

| Medida, 2019-2025 | Nominal | Real (IPC) | Real (renta por hogar) |
|---|---|---|---|
| IPV (INE) | +44,4 % | +18,7 % | +12,9 % |
| Valor tasado por m² (MIVAU) | +29,6 % | +6,5 % | +1,4 % |

Las medias anuales difieren ligeramente de las cifras publicadas (+30,4 % y +7,1 % son el núcleo de tres fuentes).

## 4. Literatura y documentos

| Referencia | Estado | Lectura |
|---|---|---|
| Khametshin, López Rodríguez y Pérez García (2024), BdE DO 2432, DOI 10.53479/37872 | VERIFICADA (Crossref) | parcial (p. 17, sobre los precios medios) |
| Lajer Baron, López Rodríguez y San Juan (2024), BdE DO 2433, DOI 10.53479/37873 | VERIFICADA (Crossref) | parcial (pp. 13-14: IPV como medida) |
| Banco de España, IEF primavera 2026 e IA2025 | NO VERIFICADA (sin DOI) | páginas citadas |
| INE, metodología del IPV (base 2015); Eurostat, Handbook on Residential Property Prices Indices (2013) | NO VERIFICADA (sin DOI comprobado) | no leídos en V17: se cita el principio general (índice de calidad constante), no una cifra |

## 5. Veredicto

**Se sostiene con matices.** Las cifras son correctas, y la advertencia contra elegir sin decirlo la cifra que conviene es legítima. El matiz: no es una elección entre equivalentes. Para la variación del precio de la vivienda hay una medida de referencia, el índice ajustado por calidad, y las medias por m² responden a otra pregunta, con un sesgo de composición que es medible en parte. La advertencia correcta no es «elegir», sino «decir qué pregunta responde cada cifra» y, para el acceso, deflactar también por la renta.

## 6. Texto corregido y confianza

> «El precio ha subido un X %»: una vivienda de las mismas características cuesta hoy un 44 % más que en 2019 (índice del INE), un 19 % más descontada la inflación y un 13 % más en relación con la renta de los hogares. El precio medio por m² sube menos (+30 % nominal, +7 % real). Mide lo que se vende cada año, sin ajustar por sus características; por qué sube menos no está medido. Para saber cuánto se ha encarecido la vivienda, la referencia es el índice. La media por m² dice cuánto pagan de media por m² los compradores de cada año.

Confianza:
- IPV como medida de referencia: **la evidencia indica** (práctica estadística estándar);
- que la brecha se deba a la composición: **la evidencia no permite concluir**.

## 7. Parada

No hay parada. Las cifras publicadas son correctas. La frase «quien elige la cifra elige el mensaje» no figura en publicacion/. La 1.0 dice «se dan ambas medidas y no se elige una» (I.2), que es una opción de presentación, no una afirmación falsa. Se señala al autor que el estándar del Banco de España (B5) da prioridad al IPV.

## 8. Respuesta a la ronda 1

- **Atribución a la composición: aplicado.** El texto corregido ya no la atribuye toda: «en parte», y «el resto no está medido».
- **Rótulo [C4] del IPV: se mantiene.** En la capa del proyecto el IPV es [C4] por ser de fuente única, y no cambia. En la lectura V17 (B1) es «OF»: estadística oficial. Se cita como referencia por método, no por capa.
- **«Tasación frente a transacción»: aplicado, se quita.** Las tres medias por m² coinciden (29,2-29,7 % con medias anuales).
- **Veredicto: aplicado.** Pasa a «se sostiene con matices». La falsa equivalencia queda como matiz: la advertencia es válida, pero para la variación del precio hay una medida de referencia.

## 9. Respuesta a la ronda 2

- **Atribución a la composición: aplicado.** Se retiran del texto corregido y de la conclusión de 3.2 «se vende más en provincias más baratas» y «en torno a un tercio». Las medias publicadas coinciden con el índice de pesos fijos, no con el valor unitario, y el cálculo excluye Madrid, Baleares y Canarias.
- **Confianza sobre la composición: aplicado.** Pasa a «la evidencia no permite concluir».
- **Hecho afectado.** V17-AUD-DP-PRE-COMPOSICION-PROVINCIAS se mantiene como cálculo descriptivo, sin cambio de valor; ya no se usa como explicación.
- **Veredicto: sin cambio.** Sigue «se sostiene con matices».

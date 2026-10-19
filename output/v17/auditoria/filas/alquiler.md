Análisis a posteriori (V17). Ficha de auditoría de la fila «alquiler» (D1, discurso político). Grupo demanda_precios. Capa de toda cifra nueva: C4. Ninguna cifra ni capa publicada cambia. Ids nuevos: V17-AUD-DP-ALQ-*.

# «El alquiler ha subido un X %»

## 1. Texto auditado

> «El alquiler ha subido un X %»: pregunta si son contratos vigentes o nuevos, y si es nominal o real.

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor.** Las dos preguntas separan cifras que difieren mucho con los mismos datos y el mismo periodo:
- **IPC de alquiler (contratos vigentes), 2019-2025:** +10,1 % nominal y −9,5 % real con el IPC general (informe integral, VI; ids de la 1.0, C4).
- **Contratos nuevos en Cataluña (Incasòl), 2019-2025:** mediana municipal de +24,8 % nominal, con un P10-P90 de +11,7 % a +48,9 % en 514 municipios sin muestra sellada (V17-AUD-DP-ALQ-INCASOL-NUEVOS).
- **Brecha publicada.** La brecha entre contratos nuevos y vigentes en Cataluña es de 10,8 puntos (2021-2024; 1.0, [C1]).
- **Banco de España (IA2025, p. 125).**
  - Contratos vigentes: +0,4 % real de media anual desde 2019.
  - Nuevos contratos: +4,6 % real interanual en 2024.
  - Precios de oferta en portales: +5 % real en 2025.

**En contra (lo que la frase omite).**
- **Falta una tercera pregunta: ¿precio de oferta o precio firmado?** Los portales miden anuncios: precio pedido, con la composición de lo que se anuncia, y sin las viviendas que se alquilan sin anuncio. Los registros de fianzas miden contratos firmados. Las dos son «nuevos» y no miden lo mismo. En los topes de Cataluña, la distinción decide el resultado (ver la ficha topes).
- **Falta una cuarta: ¿real respecto a qué?** El IPC dice cuánto pierde o gana el alquiler frente a los demás precios. Para el acceso, el Banco de España deflacta por la renta.
  - El IPC de alquiler deflactado por la renta disponible bruta por hogar cae un 13,9 % en 2019-2025 (V17-AUD-DP-ALQ-IPC-REAL-RENTA). Para el inquilino que sigue en su contrato, el alquiler pesa hoy menos en la renta media que en 2019.
  - Para quien firma ahora, en Cataluña, la renta media de los contratos nuevos (+24,8 %) sube 2,5 veces más que el IPC de alquiler, aunque algo menos que la renta disponible por hogar nacional (+27,9 %). La comparación con la renta mezcla ámbitos (Cataluña frente a España; mediana municipal frente a agregado) y es solo orientativa. El esfuerzo del primer quintil y de los jóvenes no se ve en una media.
- **Falta el ámbito y el desfase.** IPVA y SERPAVI (datos tributarios) bajan a municipio o distrito, pero llegan con unos dos años de retraso y miden el stock. El IPC es provincial como mucho. Una cifra nacional no describe Barcelona, y una de Barcelona no describe España.
- **Precios medios por m² frente a índices.** SERPAVI y las fianzas publican medias o medianas por m², con la composición de cada año. El propio Banco de España advierte que los precios medios «no pueden considerarse índices de precios» (DO 2432, p. 17).

## 3. Pruebas mínimas: medidas disponibles y cuál usar

Script: src/v17/f3_demanda_precios.py.

| Medida | Qué mide | Contratos | Ámbito y frecuencia | Desfase | Úsese para |
|---|---|---|---|---|---|
| IPC, subclase de alquiler (INE) | alquiler pagado por los inquilinos de vivienda principal | vigentes (stock) | nacional, CCAA, provincia; mensual | 1 mes | cuánto paga de más el inquilino medio; inflación |
| IPVA (INE, datos AEAT) | índice de alquiler declarado en IRPF | vigentes (stock) | hasta municipio o distrito; anual | ≈ 2 años | dónde sube más el alquiler del stock |
| SERPAVI (MIVAU, datos AEAT) | mediana de €/m² de los alquileres declarados | vigentes (stock) | sección, municipio; anual | ≈ 2 años | niveles locales; no es un índice (composición) |
| Registros de fianzas (Incasòl y otros registros autonómicos) | renta de los contratos registrados | nuevos (flujo) | municipio; trimestral | 1-2 trimestres | cuánto cuesta firmar hoy |
| Portales (idealista, Fotocasa y otros) | precio pedido en anuncios | nuevos, de oferta | barrio; mensual | ninguno | señal adelantada; con sesgo de composición y de precio pedido |
| Esfuerzo (ECV; BdE) | alquiler sobre la renta del hogar | vigentes | nacional, CCAA | 1 año | acceso: 26,7 % de la renta neta en 2024 (BdE IA2025, p. 140) |

Regla práctica:
- quien pregunta «¿me sube el alquiler?» (inquilino con contrato) → IPC o IPVA;
- quien pregunta «¿cuánto me costará alquilar?» (busca casa) → fianzas o portales;
- quien pregunta «¿es más difícil?» → alquiler sobre renta.

Siempre: nominal y real, y real frente al IPC y frente a la renta.

## 4. Literatura y documentos

| Referencia | Estado | Lectura |
|---|---|---|
| Khametshin, López Rodríguez y Pérez García (2024), BdE DO 2432, DOI 10.53479/37872 | VERIFICADA (Crossref) | parcial (pp. 16-19, 39-42) |
| Banco de España, IA2025, cap. 2 | NO VERIFICADA (sin DOI) | pp. 125 y 140 |
| INE, metodologías del IPC y del IPVA | NO VERIFICADA (documento metodológico; sin DOI) | no leídas en V17: la descripción de la tabla se apoya en la 1.0 y en DO 2432 |

## 5. Veredicto

**Se sostiene con matices.** Las dos preguntas son correctas y necesarias, pero no bastan. Faltan tres:
- ¿oferta (anuncio) o contrato firmado?
- ¿real frente al IPC o frente a la renta?
- ¿qué territorio?

## 6. Texto corregido y confianza

> «El alquiler ha subido un X %»: pregunte cuatro cosas. (1) ¿De contratos vigentes o de contratos nuevos? Entre 2019 y 2025, el alquiler de quien ya vivía de alquiler subió un 10 % nominal, menos que los precios y que la renta. El de los contratos nuevos en Cataluña subió en torno a un 25 %. (2) ¿Precio pedido en un portal o precio firmado? (3) ¿Nominal o real, y real frente a los precios o frente a la renta del hogar? (4) ¿De qué territorio? Cada cifra responde a una pregunta distinta: no se comparan entre sí.

Confianza:
- diferencias entre medidas: **la evidencia indica** (estadísticas oficiales);
- cifra de contratos nuevos fuera de Cataluña: **la evidencia no permite concluir** (no hay registro de fianzas en el repositorio para toda España).

## 7. Parada

No hay parada.

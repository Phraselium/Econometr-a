# Limitaciones registradas

Problemas que persisten tras las iteraciones de revisión, o restricciones de datos conocidas. Se trasladan al informe final.

## Datos (F1, aprobada)
- Población nacional antes de 2021: semestral (1 enero / 1 julio) interpolada log-linealmente a T2/T4 → Δ1 trimestral con MA mecánica.
- Población por CCAA: solo anual (1 enero) 2002-2025; en el panel trimestral está interpolada.
- No hay flujos de inmigración trimestrales útiles (INE EMCR desde 2023T2, muy dispersos); flujo anual nacional de Eurostat 1998-2024 con quiebre en 2021; sin flujos anuales por CCAA (tabla INE 69691 no descargada).
- Oferta: permisos (Eurostat) y viviendas libres iniciadas/terminadas (MIVAU) son proxies; no hay visados CSCAE ni certificados de fin de obra.
- Hogares: EPA trimestral 2002+ con quiebre metodológico en 2021T1 (−1,1 %); solo nacional.
- Precio largo: `p_bde` (BdE) = `p_tasado` (MIVAU); una única serie larga desde 1995.
- Deflactor: implícito del PIB (CNTR SA), no un deflactor de consumo.
- València: padrón por nacionalidad solo hasta 2022; varias series municipales con N corto (≤ 14 años).

## F2 (aprobada en re-revisión; pendientes trasladados)
- Cointegración con precio nominal: evidencia mixta (1/3: EG no rechaza, Johansen rechaza, ARDL no concluyente). Solo el precio real cointegra en los tres contrastes; la relación es estadística, no estructural (costes y tipo con signos no esperados en el DOLS real de control del revisor; inestable por subperiodos).
- Desde 2014Q1 el término de corrección del error deja de ser significativo (−0,068, EE 0,045; N=50) y el crédito desaparece: la dinámica de ajuste no es estable.
- El crédito nuevo contemporáneo es simultáneo con el precio (en t−1 cambia de signo); la variante con crédito en t−1 rechaza Breusch-Godfrey.
- Selección: el modelo preferido gana en solo el 1,5 % de las réplicas bootstrap; tras Bonferroni (K=1.728) ningún regresor es significativo al 5 %; fuera de muestra no mejora al AR(4) (selección hecha con la muestra completa).
- RESET rechaza en la ecuación preferida; quiebre en 2014Q1 (Chow p=0,012); Bai-Perron detecta 3 quiebres en el largo plazo.

## F3 (aprobada en re-revisión)
- Inmigración y precios: con el IV shift-share (Card, cuotas 2002), ningún efecto sobrevive al wild cluster bootstrap ni a Holm (150 especificaciones; p Holm mínimo 0,051). El IC95 % del IPV [−3,90; 0,67] excluye las magnitudes de Saiz (2007) y González-Ortega (2013); la diferencia se atribuye a diseño y periodo (2008+, peso de la cuota europea 2002 y de Baleares), no a un error.
- Pretendencias: significativas para el IPC alquiler (grupo América); la prueba 1996-2001 no es computable con data/processed (sin precios por CCAA antes de 2002; cálculo externo del revisor p=0,13).
- 17 clusters: J de Hansen con baja potencia; AKM solo simplificado (5 grupos); BHJ inviable con 5 grupos.
- Canal comprador (compras de extranjeros residentes): coeficiente 2SLS muy negativo incluso sin 2008-09 → posible violación de la exclusión; no se interpreta.
- Sin flujos de inmigración trimestrales; el flujo anual nacional (N≈17-27) no permite inferencia HAC fiable.

## F4 (aprobada en re-revisión)
- Déficit 2021-2025: 866.100 (EPA corregida, principal), 810.936 (ECP a 1 de enero), frente a ~750.000 del BdE. La diferencia (≈116.100) se descompone en +55.164 por la fuente de hogares y +60.936 por la vivienda protegida, ausente de nuestras terminadas (solo vivienda libre MIVAU). Que el BdE use la ECP es una inferencia; la cifra de 100.980 terminadas en 2024 (prensa) está NO VERIFICADA.
- Elasticidad de la oferta: los DOLS en niveles son descriptivos (cointegración 1/3, ECM no significativo, BG y RESET fallan, quiebre 2014). En Δ4, iniciadas β=1,39 (EE 0,63): no se rechaza β=0,45 (p Holm 0,27). El 0,45 del BdE (Caldera-Johansson 2013; Cavalleri et al. 2019, NO VERIFICADAS) mide previsiblemente otro concepto (inversión residencial / stock); la traducción flujo→stock no se ha hecho.
- Instrumentos del precio: solo la renta es defendible como desplazador de demanda excluido; ocupados y población pueden afectar a la oferta (exclusión dudosa).
- Pendientes menores trasladados a F7: fila antigua «¿ECP?» en comparacion_bde_deficit; signo de costes en la ecuación de permisos; «inversión residencial» como inferencia.

## F5 (aprobada en re-revisión)
- Panel anual de 17 CCAA (2009-2025): el efecto de la cuota extranjera depende de la alineación temporal (0,1 a 1,9 % por pp) y ninguno sobrevive a Holm (mínimo 0,151); asociación.
- No se detecta heterogeneidad entre CCAA (poolability p wild 0,363; límite de aleatorización 1/17), lo que no prueba homogeneidad; la C. Valenciana solo difiere en lo descriptivo y el signo depende de la medida de precio (IPV vs valor tasado).
- El test CD de Pesaran no es interpretable sobre residuos de FE bidireccional/CCE (Juodis y Reese 2022); no se calculó el CDw.
- 17 clusters: inferencia apoyada en wild cluster bootstrap; terminadas retardadas con signo positivo (contrario a lo esperado, p wild 0,075).
- Errata menor pendiente: la sección 1a de resumen_f5.md dice «16 clusters» (son 17).

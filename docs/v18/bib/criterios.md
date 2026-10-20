# V18 · Fase 1 · Criterios de búsqueda e inclusión (fijados antes de buscar, 2026-10-20)

Análisis de literatura de V18 (docs/v18/plan.md, fase 1). Estos criterios se escriben antes de la búsqueda sistemática y no se cambian a la vista de los resultados; cualquier cambio se anota abajo con fecha y motivo.

## Qué se busca
1. Todas las referencias citadas en la sección E del plan (E1-E12) y en la sección F (modelos de conjunto del Banco de España y del BCE).
2. Las referencias de docs/v15/literatura.md y docs/v16/literatura/ que tengan versión abierta legítima.
3. Búsqueda sistemática adicional por factor en OpenAlex y Crossref, y en las series de documentos del Banco de España, el BCE y los bancos centrales europeos.

## Criterios de inclusión (los tres)
- **Diseño:** cuasi experimental (diferencias en diferencias, estudio de eventos, variables instrumentales, shift-share, regresión discontinua, control sintético) o estructural con identificación declarada. Los descriptivos solo entran como contexto y se marcan así.
- **Datos:** España o mercados europeos comparables (UE, Reino Unido, Suiza, Noruega); EE. UU. solo para los estudios citados en el plan y para diseños sin equivalente europeo, marcados «validez externa limitada».
- **Publicación:** revista con revisión por pares, documento de banco central o working paper de una serie reconocida (NBER, CEPR, IZA, CESifo, series de universidades y bancos centrales).

## Términos por factor (OpenAlex «search» y Crossref «query.bibliographic»; 2000 en adelante)
- E1 vivienda turística: «short-term rental» OR Airbnb AND (rent OR house price).
- E2 topes al alquiler: «rent control» OR «rent cap» OR «rent regulation» AND (rent OR supply).
- E3 inmigración: immigration AND (house prices OR rents) AND (instrument OR shift-share OR «enclave»).
- E4 ayudas a la demanda: «housing allowance» OR «housing benefit» OR «rent subsidy» AND incidence.
- E5 oferta y suelo: «housing supply elasticity» OR «land use regulation» OR «geographic constraints».
- E6 obra nueva y alquileres cercanos: «new construction» AND (nearby rents OR «filtering» OR «spillover»).
- E7 tipos de interés: «monetary policy» AND (house prices OR housing) AND (euro area OR Spain).
- E8 fiscalidad de la compra: «transaction tax» OR «stamp duty» OR «property transfer tax».
- E9 compradores no residentes: «foreign buyers» OR «foreign demand» AND house prices.
- E10 grandes tenedores: «institutional investors» OR «large landlords» OR «corporate landlords» AND rents.
- E11 viviendas vacías: «vacancy tax» OR «empty homes» OR «vacant housing».
- E12 vivienda pública: «public housing» OR «social housing» AND (crowding out OR private construction OR prices).
- F modelos de conjunto: «house price» AND (overvaluation OR fundamentals OR «error correction») AND (Spain OR euro area).

## Límites
- Hasta 15 estudios nuevos por factor, por orden de relevancia de OpenAlex tras aplicar los criterios; si hay más, se anota cuántos se dejaron.
- Solo descargas de acceso abierto legítimo (plan, sección A); si no hay, «solo resumen».

## Cambios a estos criterios
(ninguno)

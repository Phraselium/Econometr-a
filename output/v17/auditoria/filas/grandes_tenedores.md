Análisis a posteriori (V17). Auditoría de la fase 3, grupo «oferta_titularidad». Capa C4; no cambia ninguna cifra ni capa publicada.

# Fila D1 · grandes_tenedores

## 1. Texto auditado
«Los grandes tenedores controlan el mercado»: no hay datos de titularidad para afirmarlo ni negarlo.

Dónde está en lo publicado: `publicacion/lo_que_sabemos.md` (línea 62: «no hay datos de titularidad»), `publicacion/una_pagina.md` (línea 56: «no hay datos de titularidad suficientes»), verificador de la 1.0, ficha V02 («NO ANALIZADA: FALTAN DATOS»). El informe integral (VII.7) ya da la cifra del Catastro, y el atlas de V12 (`publicacion/atlas_v12.md`, línea 43) también.

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor de la frase (prudencia).** No hay en España un registro de contratos de alquiler con el titular. Hay tres limitaciones reales:
- El Catastro cuenta el parque total, no el alquilado.
- El dato del Banco de España cubre solo a personas físicas.
- El del O-HB cubre solo Barcelona ciudad.

Además, el Catastro cuenta por NIF y por unidad catastral. Un grupo con varias sociedades aparece partido, y un edificio sin división horizontal cuenta como un inmueble. Las cuotas son, por tanto, cotas inferiores. Prueba propia: en Barcelona ciudad el Catastro da un 6,8 % del parque municipal en titulares con más de 10 inmuebles en el municipio (V17-AUD-OT-CAT-GT-BCN-2024, ediciones 2024-2026: 6,6-6,8 %). El O-HB, con otras fuentes y otra agregación, da un 17,1 % del parque total a 1-1-2021. La diferencia es de 2,5 veces. Con el Catastro solo no se puede medir bien la concentración en las ciudades.

**En contra (la frase es falsa en su primera mitad).** Sí hay datos de titularidad, y permiten negar la afirmación en su lectura nacional.
- **Parque total, España de régimen común (Catastro, cálculo propio con data/raw/v11).**
  - Titulares con más de 10 inmuebles residenciales: 4,16 % del parque en 2026 y 4,30 % en 2025 (V17-AUD-OT-CAT-GT-PARQUE-2026). Son 26.890 titulares (V17-AUD-OT-CAT-GT-TITULARES-2026).
  - Titulares con más de 100: 2,06 % (V17-AUD-OT-CAT-GT-MAS100-2026).
  - Sin las entidades públicas: 3,18 % (V17-AUD-OT-CAT-GT-SIN-PUBLICAS-2026).
  - Sociedades con más de 10: 2,18 %. Personas físicas con más de 10: 0,73 % (V17-AUD-OT-CAT-GT-SOCIEDADES-2026 y -FISICAS-2026).
  - Mediana provincial: 2,8 %, con P10 de 1,5 % y P90 de 5,0 %, en las 38 provincias sin muestra sellada v6. Es una cota inferior, porque el tramo se cuenta dentro de la provincia (V17-AUD-OT-CAT-GT-PROV-MEDIANA-2026).
- **Alquiler de vivienda habitual, España (Banco de España, Informe Anual 2025, cuadro 2.11, p. 169, datos AEAT 2024; consultado el 2026-10-19).**
  - Las personas físicas con 11 o más viviendas tienen el 2,4 % de las viviendas alquiladas por personas físicas.
  - Los particulares son «alrededor del 90 %» del alquiler.
- **Cota propia del peso de los grandes tenedores en el alquiler habitual nacional (V17-AUD-OT-COTA-GT-ALQUILER-NACIONAL): entre 2,2 % y 12,2 %.** Supuestos:
  - inferior: ninguna persona jurídica tiene más de 10 viviendas;
  - superior: todas las tienen.
  - Con particulares al 85 %, la cota es 2,0-17,0 %.
  - Es coherente con el residual PJ + público + no declarado del verificador de la 1.0 (ficha CB-V3: 16,9 % con el Censo y 38,1 % con la ECV, cotas superiores que discrepan entre sí).
- **Grandes ciudades.**
  - Barcelona ciudad: 36,1 % del alquiler habitual en grandes tenedores y 17,1 % del parque total, a 1-1-2021. Son 4.593 titulares, el 0,9 % de los propietarios (O-HB 2022, documento original). El 77,3 % de esas viviendas son de personas jurídicas, incluidas administraciones.
  - Multiarrendadores particulares (2 o más viviendas, que no es gran tenedor): 52,8 % de las viviendas alquiladas por particulares en España. En las ciudades va del 46,8 % de Sevilla al 64,9 % de Las Palmas (Ministerio de Derechos Sociales con IFS-CSIC, informe 1, abril de 2026).
- La cifra de partida del plan, un 15 % de la oferta de alquiler según el Ministerio de Vivienda, no se ha localizado en ninguna fuente primaria. No se usa (docs/v17/fuentes/titularidad.md).

## 3. Pruebas mínimas (src/v17/f3_oferta_titularidad.py)
- **Parque total frente a parque en alquiler.**
  - Parque total: 4,2 % (Catastro 2026).
  - Alquiler habitual: cota de 2,2-12,2 % (BdE más supuestos explícitos).
  - El dato del BdE de personas físicas (2,4 %) no es un techo, porque deja fuera a las personas jurídicas.
- **España frente a grandes ciudades.**
  - Nacional: entre 2 y 17 % del alquiler habitual con supuestos amplios.
  - Barcelona ciudad: 36,1 % (O-HB).
  - Catastro municipal de Barcelona: 6,8 % del parque, frente al 17,1 % del O-HB. La cuota catastral infraestima a los grandes tenedores donde hay edificios enteros sin división horizontal.
- **Concentración.** 26.890 NIF con más de 10 inmuebles en todo el territorio común. Con esa dispersión, «controlar el mercado» en el sentido de poder de mercado no es compatible con los datos nacionales. Que lo sea en mercados locales concretos no se puede descartar con estos datos, porque no hay cuotas por barrio ni por grupo empresarial.
- No hay en el repositorio datos de precios por tipo de titular. No se ha estimado ningún efecto.

## 4. Literatura
- **Gurun, Wu, Xiao y Xiao (2023).** «Do Wall Street Landlords Undermine Renters' Welfare?», *Review of Financial Studies* 36(1), 70-121. DOI 10.1093/rfs/hhac017, **VERIFICADA** (Crossref, consultado el 2026-10-19; cuartil no verificado).
  - Lectura: solo resumen (IDEAS/RePEc, vía buscador).
  - Diseño: fusiones de tres grandes inversores institucionales de vivienda unifamiliar en alquiler, 2015-2017, en EE. UU.
  - Según el resumen, el alquiler sube más donde coinciden las dos empresas fusionadas, y menos donde hay más competencia. La delincuencia baja en esos barrios.
  - Validez externa para España: baja. Es vivienda unifamiliar en EE. UU., con cuotas locales altas de pocas empresas. Identifica el efecto de un aumento de concentración local, no el de la presencia de grandes tenedores en general.
- **Bandoni, De Nora, Giuzio, Ryan y Storz (2025).** ECB Working Paper 3026, «Institutional investors and house prices». **NO VERIFICADA** (sin DOI). Lectura parcial: págs. 1-6, fase 0.
  - Diseño: VAR bayesiano y panel regional de la zona euro.
  - Resultado: un choque de demanda institucional se asocia con más crecimiento del precio agregado. Madrid figura entre las capitales con presencia alta.
  - Es un diseño de restricciones en un VAR, no un experimento. No da la magnitud en lo leído.
- **Localizados y no leídos, que no se usan:** McCarthy (Central Bank of Ireland, sobre inversores institucionales y alquiler; solo cita secundaria) y García Montalvo (2019, Funcas SEFO). Tampoco se localizó ningún estudio español con diseño causal sobre grandes tenedores y precios. El BdE (DO 2432) habla de una «escasa inversión institucional» (resumen). NO VERIFICADA como cifra.

## 5. Veredicto
**Incorrecta.** «No hay datos de titularidad» es falso. El Catastro publica la titularidad por tramos (y la 1.0 la usa en el atlas de V12). El Banco de España publica la distribución del alquiler de personas físicas por tamaño de cartera. Y el O-HB la tiene para Barcelona. Esos datos no son completos, pero permiten **negar** la afirmación en su lectura nacional: en torno al 4 % del parque y, con supuestos amplios, entre el 2 y el 12-17 % del alquiler habitual. Lo que no permiten es negar un peso alto en grandes ciudades: en Barcelona es el 36 % del alquiler habitual. Tampoco permiten saber si su presencia sube los alquileres en España.

## 6. Texto corregido y confianza
«Los grandes tenedores controlan el mercado»: en España no. Los titulares de más de 10 viviendas tienen en torno al 4 % del parque (Catastro, 2026), y entre el 2 y el 12 % del alquiler habitual según una cota con supuestos explícitos. En algunas grandes ciudades pesan mucho más: el 36 % del alquiler habitual en Barcelona (2021). Si su presencia encarece el alquiler no está medido en España. En EE. UU., más concentración local de grandes caseros se asocia con alquileres más altos.

Confianza:
- «La evidencia indica» que a escala nacional no tienen una cuota dominante del parque ni del alquiler habitual.
- «La evidencia es compatible con» un peso alto en grandes ciudades.
- «No permite concluir» nada sobre su efecto en los precios en España.

## 7. PARADA
**Conclusión de la 1.0 que la auditoría muestra falsa (plan, E).** `publicacion/lo_que_sabemos.md`, sección «No se puede afirmar con estos datos», dice, sobre qué parte del stock y del alquiler tienen las empresas o los grandes tenedores: «no hay datos de titularidad (solicitudes S1, S3 y S4)».

Prueba:
- La parte del **stock** sí tiene datos públicos: el Catastro, con titularidad por tramos y por tipo de titular. La propia 1.0 la publica en `publicacion/atlas_v12.md` (4,2 % en más de diez viviendas) y en el informe integral, VII.7 (4,2 % y 2,1 % [C4]).
- Reproducción: `src/v17/f3_oferta_titularidad.py` da 4,16 % (2026) y 4,30 % (2025).
- Lo mismo afecta a la ficha V02 del verificador («Sin datos de titularidad por tamaño de tenedor»), que el atlas declara sustituida por V12-V02.

`publicacion/una_pagina.md` («no hay datos de titularidad suficientes») es matizable, no falsa.

No se corrige ningún fichero publicado: lo decide el autor.

Análisis a posteriori (V17). Auditoría de la fase 3, grupo «oferta_titularidad». Capa C4; no cambia ninguna cifra ni capa publicada. Revisada tras la ronda 1 del abogado del diablo.

# Fila D1 · grandes_tenedores

## 1. Texto auditado
«Los grandes tenedores controlan el mercado»: no hay datos de titularidad para afirmarlo ni negarlo.

Dónde estaba en lo publicado (antes de la errata del 2026-10-19):
- `publicacion/lo_que_sabemos.md`;
- la ficha V02 del verificador;
- `publicacion/informe_tecnico.md`.

El informe integral (VII.7) y el atlas de V12 ya daban la cifra del Catastro.

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor de la frase (prudencia).** No hay en España un registro de contratos de alquiler con el titular. Hay tres limitaciones reales:
- El Catastro cuenta el parque total, no el alquilado.
- El dato del Banco de España cubre solo a personas físicas.
- El del O-HB cubre solo Barcelona ciudad.

Además, el Catastro cuenta por NIF y por unidad catastral. Un grupo con varias sociedades aparece partido, y un edificio sin división horizontal cuenta como un inmueble.
- **Cómo se cuenta el tramo.** Cada fichero cuenta el tramo «más de 10» por NIF dentro de su propio ámbito. Comprobación con la guarda v6, en las provincias no selladas: los ficheros provinciales dan 608.269 viviendas en titulares con más de 10 en 2026, un 21 % más que la suma de sus municipios (501.354) (V17-AUD-OT-CAT-GT-PROV-FRENTE-SUMA-MUN-2026). Por analogía, el fichero nacional cuenta por NIF en todo el territorio común. Es coherente con la cifra de transparencia publicada en prensa: 1.046.188, frente a 1.040.955 en la edición 2025. Las cuotas provinciales y municipales son cotas inferiores.
- **Barcelona, prueba propia.** El Catastro da un 6,8 % del parque municipal en titulares con más de 10 en el municipio (V17-AUD-OT-CAT-GT-BCN-2024; ediciones 2024-2026: 6,6-6,8 %). El O-HB, con otras fuentes y otra agregación, da un 17,1 % del parque total a 1-1-2021. Con el Catastro solo no se puede medir bien la concentración en las ciudades.

**En contra (la primera mitad de la frase es falsa).** Sí hay datos de titularidad. Con datos de stock permiten negar la afirmación a escala nacional.
- **Parque total, España de régimen común (Catastro; cálculo propio con data/raw/v11).**
  - Titulares con más de 10 viviendas: 4,16 % del parque en 2026 y 4,30 % en 2025. Son 26.890 NIF.
  - Titulares con más de 100: 2,06 %.
  - Sin las entidades públicas: 3,18 %. Sociedades: 2,18 %. Personas físicas: 0,73 % (V17-AUD-OT-CAT-GT-*).
  - Mediana provincial: 2,8 % (P10 1,5 %; P90 5,0 %), en 38 provincias sin muestra sellada v6. Es una cota inferior.
- **Alquiler habitual, España.**
  - Banco de España (Informe Anual 2025, cuadro 2.11 y p. 169, datos AEAT 2024; consultado el 2026-10-19): las personas físicas con 11 o más viviendas tienen el 2,4 % de las viviendas alquiladas por personas físicas. Los particulares son «alrededor del 90 %» del alquiler.
  - **Cota sin suelo público** (V17-AUD-OT-COTA-GT-ALQUILER-NACIONAL, la que cita la errata): 2,2-12,2 %, o 2,0-17,0 % con particulares del 85 al 95 %.
  - **Cota condicionada** (V17-AUD-OT-COTA-GT-ALQUILER-CON-PUBLICA): 10,2-12,2 % con particulares al 90 %, y 7,3-17,0 % con 85-95 %. **No es un suelo**: solo vale si toda la vivienda pública cuenta como alquiler de un gran tenedor dentro del mismo universo que el dato del BdE, lo que no está comprobado. La vivienda pública va del 8,0 % (Catastro, entidades públicas con más de 10) al 10,7 % (MIVAU, 318.000 viviendas) del alquiler censal (2.983.619 hogares en alquiler, Censo 2021).
  - **Titulares privados con más de 10, aparte** (V17-AUD-OT-COTA-GT-ALQUILER-PRIVADOS): 2,2-4,1 % con particulares al 90 % y **2-9 % con 85-95 %**. Con la misma condición de universos.
  - Con la cifra del MIVAU, la vivienda pública agota por sí sola el 10 % no particular. Los universos (AEAT frente a Censo, cesión incluida o no) no casan exactamente, y la cota con suelo público es menos sólida que la amplia.
- **Multiarrendadores (2 o más viviendas; no es gran tenedor).**
  - BdE, suma de tramos del cuadro 2.11: 49,3 % de las viviendas alquiladas por personas físicas (2024; V17-AUD-OT-BDE-MULTIARRENDADORES-2024).
  - Ministerio de Derechos Sociales con IFS-CSIC (informe 1, abril de 2026): 52,8 % (2023, Panel de Hogares de la AEAT).
  - La diferencia (3,5 puntos) se explica por fuente, año y universo distintos. No se reconcilia aquí.
- **Barcelona ciudad (O-HB 2022, documento original, figuras 3 a 5; datos a 1-1-2021). Solo vale para Barcelona.**
  - Grandes tenedores: 36,1 % del alquiler habitual estimado.
  - Las administraciones públicas son el 4,44 % del alquiler habitual y el 12,3 % del de los grandes tenedores.
  - **Sin administraciones: 31,7 %** (V17-AUD-OT-OHB-BCN-GT-SIN-ADMINISTRACIONES).
- La cifra de partida del plan, un 15 % de la oferta de alquiler según el Ministerio de Vivienda, no se ha localizado. No se usa.

## 3. Pruebas mínimas (src/v17/f3_oferta_titularidad.py)
- **Parque total frente a alquiler.** Arriba. Parque: 4,2 %. Alquiler nacional: cota amplia de 2-12 % y cota condicionada de 10-12 %. Privados: 2-4 % (2-9 % con 85-95 % de particulares).
- **España frente a grandes ciudades.** Nacional: 2-12 %. Barcelona: 36,1 %, o 31,7 % sin administraciones. El Catastro municipal infraestima en las ciudades con edificios enteros sin división horizontal.
- **Concentración.** 26.890 NIF con más de 10 en todo el territorio común. Con datos de stock nacionales no hay una cuota dominante. En mercados locales no se puede descartar, porque no hay cuotas por barrio ni por grupo empresarial.
- No hay datos de precios por tipo de titular. No se estima ningún efecto.

## 4. Literatura
- **Gurun, Wu, Xiao y Xiao (2023).** *Review of Financial Studies* 36(1), 70-121. DOI 10.1093/rfs/hhac017, **VERIFICADA** (Crossref, 2026-10-19; cuartil no verificado). Solo resumen (IDEAS, vía buscador).
  - Diseño: fusiones de grandes inversores de vivienda unifamiliar en alquiler en EE. UU.
  - Resultado: más alquiler donde coinciden las empresas fusionadas, y menos donde hay más competencia.
  - Validez externa baja: mide un aumento de concentración local, no la presencia de grandes tenedores en general.
- **Bandoni et al. (2025), ECB WP 3026.** **NO VERIFICADA**. Lectura parcial, págs. 1-6. VAR bayesiano y panel de la zona euro, con restricciones; no es un experimento.
- **Localizados y no leídos, que no se usan:** McCarthy (Central Bank of Ireland) y García Montalvo (2019, Funcas).
- No hay estudio español con diseño causal sobre grandes tenedores y precios.

## 5. Veredicto
**Incorrecta.** «No hay datos de titularidad» es falso: Catastro, Banco de España y O-HB. Con datos de stock, esos datos permiten negar el control a escala nacional:
- en torno al 4 % del parque;
- entre el 2 y el 12 % del alquiler habitual, con supuestos amplios (2-17 % con particulares del 85 al 95 %);
- entre el 2 y el 9 % en titulares privados, si la vivienda pública se descuenta del alquiler no particular.

No permiten negar un peso alto en grandes ciudades: un 32-36 % del alquiler habitual en Barcelona. Tampoco permiten saber si su presencia sube los alquileres en España.

## 6. Texto corregido y confianza
«Los grandes tenedores controlan el mercado»: a escala nacional, con datos de stock, no. Los titulares de más de 10 viviendas tienen en torno al 4 % del parque (Catastro, 2026), y entre el 2 y el 12 % del alquiler habitual según una cota con supuestos explícitos; si se descuenta la vivienda pública, los titulares privados tendrían entre el 2 y el 9 %. En Barcelona ciudad pesan mucho más: el 36 % del alquiler habitual en 2021, el 32 % sin las administraciones. Si su presencia encarece el alquiler no está medido en España. En EE. UU., más concentración local de grandes caseros se asocia con alquileres más altos.

Confianza:
- Peso nacional: «la evidencia indica».
- Peso alto en grandes ciudades: «la evidencia es compatible con».
- Efecto en precios: «no permite concluir».

## 7. PARADA
**Resuelta.** La parada P2 se elevó porque `publicacion/lo_que_sabemos.md` decía «no hay datos de titularidad» del parque y la ficha V02 del verificador decía «Sin datos de titularidad por tamaño de tenedor». El autor la decidió el 2026-10-19 y ya está aplicada (ERRATA.md):
- `lo_que_sabemos.md`, la ficha V02 y `informe_tecnico.md` (dos pasajes; el de la AEAT era correcto) separan ahora tres cosas:
  - el parque total, con dato (4,2 %);
  - el alquiler, con datos parciales (2,4 % del BdE, 36,1 % del O-HB y 2,2-12,2 % con supuestos, V17-AUD-OT-COTA-GT-ALQUILER-NACIONAL);
  - el efecto en precios, no medido.
- El veredicto de V02 («NO ANALIZADA: FALTAN DATOS») se mantiene con el motivo corregido.
- Ninguna cifra ni capa cambió.

## Respuesta a la ronda 1
- **Cota con la vivienda pública como suelo y privados aparte. Aplicado.** Nuevas V17-AUD-OT-COTA-GT-ALQUILER-CON-PUBLICA (10,2-12,2 %) y -PRIVADOS (2,2-4,1 %). Se conserva la cota amplia (2,2-12,2 %), que es la que cita la errata. Es más robusta porque no exige que el universo AEAT y el del Censo coincidan.
- **36,1 % sin administraciones. Aplicado.** El O-HB lo permite (figura 5): 31,7 %. Se dice que solo vale para Barcelona ciudad.
- **«A escala nacional, con datos de stock» en lugar de «en España no». Aplicado** en el texto corregido.
- **Tramo del Catastro, ¿NIF nacional o suma municipal? Documentado.** El fichero nacional cuenta por NIF en todo el territorio común: supera en un 8,4 % a la suma provincial. (Comprobación sustituida en la ronda 2 por la de provincias frente a municipios no sellados, para no sumar provincias selladas.) Los provinciales y municipales son cotas inferiores.
- **49,3 % frente a 52,8 %. Señalado.** Diferencia de fuente, año y universo.
- **PARADA. Actualizada:** resuelta por el autor.

## Respuesta a la ronda 2
- **La «cota con suelo público» no es un suelo. Aceptado:** se rotula como cota condicionada a que la vivienda pública cuente como gran tenedor en el mismo universo que el dato del BdE.
- **Rango privado del 2-9 % en el veredicto. Aplicado,** con su condicional.
- **Guarda v6.** La comprobación del NIF ya no suma provincias selladas. Se sustituye por la comparación entre los ficheros provinciales y municipales de las provincias no selladas (cociente 1,21). V17-AUD-OT-CAT-GT-TOTAL-FRENTE-SUMA-PROV-2026 queda retirada, porque sumaba las 11 provincias selladas. La distribución provincial y el dato de Barcelona pasan por holdout.excluir_sellados_v6.

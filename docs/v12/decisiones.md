# V12 · Decisiones (análisis descriptivo: población, propiedad y oferta)

Reglas generales:
- solo análisis descriptivo y contable; ningún modelo causal ni predictivo;
- capas C1 (≥2 fuentes coincidentes en ese nivel), C2 (cotas) y C4 (descriptivo o asociación);
- neutralidad: se describen flujos y condiciones, nunca se atribuyen responsabilidades;
- celdas pequeñas: se respeta «<5» de origen y no se publican cruces con < 10 casos ni con error relativo > 30 %.

## F0
1. **`make check` no escribe ficheros versionados**:
   - `src/v10/web.py` toma la ruta del resumen de `web.RESUMEN`; `tests/v10/test_web.py` construye la web y el resumen
     en un directorio temporal;
   - `src/v12/git_limpio.py` guarda `git status` al empezar `make check` y falla si cambia al terminar;
   - `tests/conftest.py` hace lo mismo para la sesión de pytest; `tests/v12/test_git_limpio.py` prueba el guardia.
2. **Titularidad del Catastro: dos series que NO se encadenan.**
   - **2012-2023 (JAXI):** titulares catastrales; cuenta todos los cotitulares y derechos.
   - **2024-2026 (CSV):** sujetos pasivos del IBI, un contribuyente por inmueble.
   - **Salto nacional 2023 → 2024:** −32,1 % en inmuebles urbanos (33,72 → 22,90 millones). Ratio municipal mediano 0,671 (p10-p90: 0,61-0,74). Es cambio de definición, no variación real. Va marcado en el diccionario de la base.
   - **Ámbito de los tramos:** el nº de inmuebles del titular se cuenta DENTRO de cada ámbito territorial.
     - Comprobación: la suma municipal de viviendas de personas jurídicas con > 100 inmuebles es 139.295 en 2025, frente a 290.427 en el fichero nacional.
     - Consecuencia: la concentración municipal es una cota inferior de la nacional, y los análisis de grandes tenedores usan también los ficheros nacional, autonómico y provincial.
3. **AEAT: declarantes aproximados con rentas de bienes inmuebles = importe ÷ media (2016-2024).**
   - **Error de redondeo:** ≤ 0,5/media (mediana 0,04 %).
   - **Qué incluye el concepto:** alquileres E imputación de rentas de inmuebles no alquilados, así que no mide «caseros». Cuotas > 1 (10 municipio-año) se marcan y no entran en la base.
   - **2013-2015:** otro diseño. Separa alquileres e imputaciones, pero sin media; unidades por verificar; no se usa en cálculos.

## B1 · De dónde viene la población (src/v12/b1_contabilidad.py → output/v12/b1)
1. **Identidad:** ΔP = vegetativo (MNP) + saldo exterior + saldo interior + residuo, con flujos del año natural t y
   población a 1 de enero de t y t+1. Capa C4: cada componente sale de una sola fuente; el residuo se publica siempre.
2. **Población:** padrón continuo para ΔP de 2003-2021 y censo anual para 2022-2024 (cada ΔP con la misma fuente en
   ambos extremos). Padrón y censo anual difieren +0,033 % (2021) y +0,024 % (2022) en el total nacional.
3. **Empalme EVR → EMCR en 2021:** se usa la EMCR desde 2021. En 2021 la EMCR da 887.960 inmigraciones exteriores y
   696.866 emigraciones, frente a 662.173 y 452.511 en la EVR (la EMCR estima omisiones y bajas que la EVR no registra);
   los movimientos interiores casi coinciden (1,671 frente a 1,679 millones). Las dos se guardan en empalme_2021.csv.
4. **Periodo inicial:** 2003-2007 (no 2002-2007): la población municipal por nacionalidad empieza el 1-1-2003.
5. **Residuo:** con la EVR (2003-2021) el residuo nacional es negativo (−0,60 millones en 2008-2013, −0,48 en
   2014-2019): la EVR registra peor las salidas al extranjero y el padrón da de baja por caducidad e inscripción
   indebida sin que conste como flujo. Con la EMCR (2022-2024) el residuo es casi nulo (+8.897). Por eso las
   comparaciones entre periodos usan las tasas de los componentes y se lee el residuo junto a ellas.
6. **Nacionalidad:** el residuo de cada grupo incluye las adquisiciones de nacionalidad española (pasan de EXT a ES
   sin ser flujo): residuo ES positivo y EXT negativo de magnitud parecida. No se interpreta como migración.
7. **Municipios:** solo ≥ 10.000 hab. (los menores llegan agregados como PP999 en los microdatos y solo cuentan en
   provincia, CCAA y España). Ficheros municipales comprimidos (gzip determinista).
8. **València por sección y barrio (2021-2025):**
   - No hay padrón por barrio con nacionalidad en data/raw. Se usa el censo anual por sección (deriva del padrón) y se
     pasa a barrio con la correspondencia sección-barrio: entera si ≥ 95 % del área cae en un barrio, por área si no
     (10,2 % de la población de 2025; supone densidad uniforme).
   - Solo hay cartografía del seccionado vigente y entre 2021 y 2025 se dividen o desaparecen secciones en 11 de 19
     distritos. La variación 2021→2025 es exacta por distrito (las secciones no cambian de distrito); por barrio se
     publica solo si su distrito no cambió de seccionado (37 barrios «comparables»); el resto queda en blanco.
   - Solo stocks por nacionalidad (no hay flujos por sección). Países con < 10 personas en la celda se suprimen.

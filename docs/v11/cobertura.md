# V11-DATOS · Cobertura por pregunta del canal demográfico (2026-10-15)

Qué datos hay ya en la base (`make base`) o en data/raw para cada pregunta, desde cuándo y con qué hueco. No hay
estimaciones: esto describe datos. Todas las series nuevas son C4 (descriptivo) hasta que un diseño las use.

## 1. Origen y destino de la población
Pregunta: de dónde llega la población que se instala en cada municipio y adónde se va.

**Hay:**
- **Flujos interiores municipio → municipio:**
  - EVR, 1988-2021, matrices OD anuales por nacionalidad (ES/EXT), sexo y edad;
  - EMCR, 2021-2024.
  - Origen y destino agregados en «resto de provincia» por debajo de 10.000 hab.
- **Llegadas desde el extranjero y salidas al extranjero por municipio y país de nacionalidad:**
  - EVR, 1988-2021; bajas al extranjero desde 2002;
  - EMCR, 2021-2024.
- **Todos los municipios:** saldos publicados de la EMCR (tabla 69767), 2021-2024.
- **Por provincia:** EM, 2008-2021 (v9).
- **Stocks:**
  - padrón por nacionalidad, 2003-2022 (v9);
  - censo anual por sección y nacionalidad, 2021-2025 (v9);
  - ECP trimestral por provincia y nacionalidad, 2002T1-2026T3. Las filas desde 2026T3 son posterior_prereg.

**Hueco:**
- municipios de menos de 10.000 hab. antes de 2021;
- país de nacimiento en los flujos interiores de la EVR (solo nacionalidad).

## 2. Desplazamiento interno
Pregunta: si la llegada de población a un municipio se acompaña de salidas de residentes hacia otros municipios, y por edad y nacionalidad.

**Hay:**
- **Altas, bajas y saldo interno por municipio × nacionalidad × grupo de edad:**
  - 1988-2021 (EVR);
  - 2021-2024 (EMCR).
- **OD completo:** permite seguir las salidas de València a su área metropolitana año a año.
- **Saldo vegetativo municipal (MNP), 1980-2024:** para separar el crecimiento natural del migratorio.
- **Contexto:**
  - afiliación por municipio (mensual desde 2022; diciembres 2011-2021);
  - paro SEPE (v9).

**Hueco:** sección o barrio. Los flujos submunicipales solo existen en la EMCR (área submunicipal, tabla 75690, 2021-2024) y como solicitud 7 (padrón por barrio).

## 3. Condiciones de vivienda por origen
Pregunta: tenencia, hacinamiento, superficie y coste de la vivienda según nacionalidad.

**Hay:**
- **Censo 2021 (microdatos, muestra del 10 %), por municipio:** tenencia, superficie, superficie por ocupante y tamaño y tipo de hogar, según la nacionalidad de la primera persona del hogar y el periodo de llegada a España. La base lleva la tenencia; el resto está en data/raw.
- **ECV 2018-2025 (microdatos), España y CCAA:** tenencia, alquiler pagado, habitaciones y tipo de hogar por nacionalidad o país de nacimiento (docs/v11/auditoria_microdatos_ecv_epa.md).
- **ECEPOV 2021 (microdatos, factor de elevación):** municipio solo en capitales y municipios de más de 50.000 hab.

**Hueco:**
- series anuales municipales por origen (no existen);
- superficie en la ECV.

## 4. Hogares por nacionalidad
Pregunta: cuántos hogares encabezan personas extranjeras y cómo cambian.

**Hay:**
- **Censo 2021 (microdatos):** hogares de la muestra por municipio y nacionalidad de la primera persona.
- **EPA 2018-2026 (microdatos):** hogares por nacionalidad de la persona de referencia, por provincia y trimestre (se puede construir; no calculado).
- **ECP:** hogares por tamaño, trimestral por provincia (sin nacionalidad).

**Hueco:**
- la ECP no publica hogares por nacionalidad;
- la EPA tiene error muestral alto en provincias pequeñas.

## 5. Respuesta de la oferta
Pregunta: si el parque y la construcción responden donde llega población.

**Hay:**
- **Catastro INSPIRE, por sección y barrio (2026):** edificios, inmuebles, viviendas y superficie por uso y periodo de construcción. Cubre València, 49 municipios del área metropolitana (≤ 20 km), Alicante y Castellón.
- **MIVAU, provincia, 1991-2026:** iniciadas y terminadas, protegida, suelo.
- **Catastro, estadística municipal (URBANA 2012-2026):** unidades urbanas por municipio.
- **Censo 2021:** viviendas principales, no principales y vacías por municipio y año de construcción.
- **Afiliación en construcción por municipio:** mensual desde 2022.

**Hueco:**
- visados y licencias municipales (no publicados);
- licencias de cambio de uso en València (solicitud 6).

## 6. Instrumento migratorio mejorado
Pregunta: con qué datos se puede construir un instrumento de llegada de población más preciso que el shift-share provincial de V9 (D4).

**Hay:**
- **Cuotas municipales iniciales por nacionalidad:**
  - EVR 1988-2001, flujos por país (CNAC);
  - padrón 2003.
- **Flujos nacionales por país de origen** (EVR, EMCR y Eurostat).
- **Shocks de oferta de migrantes por evento normativo con fecha (BOE):**
  - regularización de 2005;
  - reglamentos de 2011 y 2024;
  - RDL 2/2025;
  - protección temporal 2022.
- **Protección temporal y asilo por nacionalidad (Eurostat, nacional):** permite un shock por país (p. ej., Ucrania 2022, Venezuela y Colombia en solicitudes de asilo) repartido con cuotas municipales previas.

**Hueco:**
- protección temporal y arraigo por provincia o municipio (Interior e Inclusión inaccesibles; solicitud 5);
- afiliación de extranjeros por municipio. El fichero municipal no distingue nacionalidad. Sí se ha añadido la afiliación de extranjeros por provincia (2022-01, 2023-12 a 2025-12 y 2026-09).

## Sustituto de la OPI y de Interior: población por nacionalidad (segunda pasada)
La OPI (residentes documentados) e Interior (protección internacional y temporal) siguen bloqueados por el servidor.
Como sustituto de STOCK se documentan estas series, todas por código INE.

**Ucrania (protección temporal desde marzo de 2022):**
- **Trimestral nacional** (ECP 56936, `data/raw/ine_ecp_56936.csv`, desde 2002T1). Ejemplos de valores de la serie:
  202.247 personas el 1-4-2023, 210.012 el 1-1-2024 y 202.105 el 1-1-2025. Las filas desde 2026T3 son posterior_prereg.
- **Anual por provincia, municipio y sección:**
  - censo anual 2021-2025 (`data/raw/v9/ine_censo_anual/censo_seccion_pais.csv.gz`, nacionalidad «Ucrania»);
  - padrón continuo municipal 2003-2022 (`data/raw/v9/ine_padron_nacionalidad/`).
- **Trimestral por provincia:** solo por grupos de nacionalidad (ECP 56947 y 82104; Ucrania está en «Europa no UE»).
  La ECP no publica el país a escala provincial.

**Otras nacionalidades:** las mismas tablas, más los flujos de entrada por país y municipio (EVR 1988-2021, EMCR 2021-2024).

**Limitaciones del sustituto:**
- mide población residente empadronada, no situaciones administrativas (protección concedida, arraigo, tipo de tarjeta);
- no distingue a quien está en protección temporal de quien llegó por otras vías.

**Flujo nacional de concesiones** (protección temporal, asilo): Eurostat `migr_asytpfm`, `migr_asyappctzm`.

**Réplica parcial de la OPI:** la Comunidad de Madrid republica los residentes documentados de la provincia 28:
- 2013-2025 por país, en la base como `opi_residentes_documentados`;
- desde 1995 por edad y tipo de documentación.

## Histórico añadido (continuación V11)
- **Respuesta de la oferta:**
  - obra nueva por municipio y año, por dos vías:
    - INSPIRE, por año exacto de construcción, 1900-2026, 94 municipios;
    - Δ de unidades urbanas residenciales del Catastro, 2013-2026, todos los municipios;
  - viviendas por año de construcción y de reforma, 2019.
- **Propiedad:** titulares por municipio, 2012-2023, y titularidad por tramos y tipo de persona, 2024-2026.
- **Renta y alquiler:**
  - IRPF municipal (rentas de inmuebles, renta bruta y disponible), 2013-2024, en la Comunitat Valenciana;
  - IPVA por municipio y distrito, 2011-2024.
- **Empleo local:** afiliación por municipio, con diciembres desde 2011 y mensual desde 2022.

## Padrón municipal de València por barrio y distrito (tercera pasada, 2026-10-16)
Fuente: PDF anuales de la Oficina d'Estadística (`data/raw/v11/vlc_padron/`; variantes en `docs/v11/vlc_padron_ficheros.md`).
| Tabla | Barrio (87) | Distrito (19) |
|---|---|---|
| Población por sexo (`vlc_padron_pob`) | 2001-2013, 2015-2026 | 2001-2013, 2015-2026 |
| Edad en 3 grupos × sexo (`vlc_padron_pob_edad`) | 2002-2012, 2016-2024 | 2002-2009, 2016-2026 |
| Extranjeros por continente × sexo (`vlc_padron_ext_continente`) | 2002-2003, 2005-2026 (2011 por sexo no cuadra: excluido de la base) | 2002-2026 |
| Nacionalidades principales: total de la ciudad y 4 distritos con más peso | — | 2005-2018 (`vlc_nacionalidades_principales.csv.gz`, fuera de la base) |
| Altas y bajas (nacimientos, defunciones, inmigración, emigración, cambios de domicilio) | — | 1998-2016 (`vlc_altas_bajas`) |

**Falta:** padrón 2014 (no publicado en PDF; sí la población extranjera 2014); altas y bajas desde 2017 (sin informe);
altas y bajas por nacionalidad y países por barrio (filas en `tablas_crudas.csv.gz`, sin normalizar); edad en 2001, 2013, 2015 y 2025-2026 a escala de barrio.

**Validación** (`validacion.csv`): suma de barrios = total de la ciudad del PDF en todos los años; Total = Hombres + Mujeres en todas las filas salvo las señaladas;
ciudad frente al padrón del INE: 0,09-1,32 % (máximo en 2021). Barrios frente al censo anual por sección 2021-2025 (37 barrios comparables): mediana 2,2-3,3 %;
máximo ≈ 400 % en barrios rurales (Pobles del Nord y del Sud), por la asignación sección → barrio por superficie de V12-B1, no por el padrón.

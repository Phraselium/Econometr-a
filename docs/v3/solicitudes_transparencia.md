# Solicitudes de acceso a información pública (v3, oleada 1)

Base jurídica: Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública y buen gobierno (art. 12 y ss.). Se presentan por el Portal de la Transparencia de la Administración General del Estado (sede electrónica). Plazo de resolución: un mes, ampliable a otro (art. 20). Cabe reclamación ante el Consejo de Transparencia y Buen Gobierno (art. 24).

**Estado: redactadas, no presentadas.** Presentarlas exige identificación electrónica del solicitante, que el proyecto no tiene. Las presenta la persona responsable del proyecto. La ingesta está preparada en `src/v3/ingesta_grandes_tenedores.py`. La cota de grandes tenedores (P-B) queda en espera hasta recibir los datos.

---

## Solicitud 1 — Dirección General del Catastro: titularidad de inmuebles residenciales por tipo y tamaño de titular

**Órgano:** Dirección General del Catastro (Ministerio de Hacienda).

**Información solicitada.** Tabla agregada, sin datos personales, de los inmuebles de uso residencial (bienes inmuebles urbanos de uso «V»). Desglose:
1. Territorio: municipio (código INE). En los municipios de más de 50.000 habitantes, también sección censal o distrito si la DGC dispone de la correspondencia.
2. Fechas de referencia: 1 de enero de cada año de 2015 a 2026, o las disponibles.
3. Tipo de titular catastral: persona física, persona jurídica, administración pública, entidad sin ánimo de lucro, otros.
4. Tramos de tamaño del titular según el número total de inmuebles residenciales que posee en todo el territorio de régimen común: 1, 2, 3-4, 5-9, 10-24, 25-99, 100-999 y 1.000 o más. Debe identificarse el tramo de «10 o más», definición de gran tenedor de la Ley 12/2023, art. 3.k. Si la DGC lo prefiere, sirve el de 5 o más en zonas de mercado residencial tensionado.
5. Variables: número de inmuebles y superficie construida total.

**Formato:** CSV o XLSX reutilizable (art. 22.1 de la Ley 19/2013).

**Protección de datos:**
- Las celdas con menos de 5 titulares pueden suprimirse o agregarse. La información es estadística y no identifica a personas (art. 15.4 de la Ley 19/2013).
- No se solicitan referencias catastrales ni nombres.

**Finalidad (informativa, no exigida):** investigación estadística reproducible sobre la concentración de la propiedad residencial y su relación con el precio del alquiler.

## Solicitud 2 — MIVAU: Sistema de Información Urbana (SIU), series 2016-2024

**Órgano:** Dirección General de Vivienda y Suelo / Dirección General de Agenda Urbana y Arquitectura (Ministerio de Vivienda y Agenda Urbana).

**Información solicitada.** Para cada municipio (código INE) y cada año de 2016 a 2024 (o el último disponible), las series del SIU:
1. Superficie de suelo urbano consolidado, urbano no consolidado y urbanizable (sectorizado y no sectorizado), en hectáreas.
2. Superficie de suelo urbanizable y urbano no consolidado con uso global residencial.
3. Capacidad residencial estimada, en número de viviendas, del suelo pendiente de desarrollo.
4. Fecha de aprobación del planeamiento general vigente y figura de planeamiento.
5. Si existe: suelo residencial con ordenación pormenorizada aprobada y sin edificar (solares).

**Formato:** CSV o XLSX. El visor web del SIU muestra la información vigente, pero no ofrece descarga de las series anuales ni su histórico.

**Finalidad:** medir la disponibilidad de suelo como moderador de la respuesta de la oferta (P-C4).

---

## Seguimiento
| Solicitud | Fecha de presentación | N.º de expediente | Resolución | Datos ingeridos |
|---|---|---|---|---|
| 1 Catastro | pendiente | — | — | — |
| 2 SIU | pendiente | — | — | — |

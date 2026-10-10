# Licencias y condiciones de uso de los datos (v5)

En cada fuente se distingue entre el **uso** (análisis) y la **redistribución** (copias en este repositorio). Si las condiciones no se han verificado, se dice. El inventario de ficheros está en data/raw/_manifest.csv.

| Organismo | Datos | Uso | Redistribución en el repositorio | Condiciones (verificación) |
|---|---|---|---|---|
| INE | IPV, IPC, EPA, ECP, ECV, Censos, ETDP, ADRH, VUT, proyecciones de hogares | Libre con cita | Sí, con cita | Aviso legal del INE: reutilización libre citando la fuente (Ley 37/2007). Verificado en v3 |
| Ministerio de Vivienda y Agenda Urbana | Valor tasado, terminadas e iniciadas, protegida, transacciones, SERPAVI, suelo | Libre con cita | Sí, con cita | Ley 37/2007 y aviso legal del Ministerio. Verificado en v3 |
| Dirección General del Catastro | Estadísticas catastrales municipales; MBC (BOE) | Libre con cita | Sí (estadísticas agregadas) | Aviso legal de la Sede Electrónica del Catastro. Verificado en v4 |
| Banco de España | Boletín Estadístico, EFF (cuadros publicados), crédito | Libre con cita | Sí, con cita | Aviso legal del BdE: reproducción permitida citando la fuente. No verificado para la EFF microdatos (no se usan) |
| Eurostat | HPI, HICP, SILC, población | Libre | Sí | CC BY 4.0 (Decisión 2011/833/UE) |
| BCE, BIS, OCDE | Tipos, precios, indicadores | Libre con cita | Sí, con cita | Condiciones de cada organismo; la OCDE es CC BY 4.0 desde 2024 |
| Consejo General del Notariado | Compraventas y precios publicados | Con cita | Agregados publicados | **Condiciones de reutilización no verificadas** |
| Colegio de Registradores | Estadística registral, datos abiertos | Con cita | Agregados publicados | **Condiciones de reutilización no verificadas** |
| Incasòl (Generalitat de Catalunya) | Fianzas | Libre | Sí | CC BY 4.0 (portal de transparencia) |
| Generalitat Valenciana | Fianzas, VUT, padrón | Libre con cita | Sí | Licencia del portal de datos abiertos de la GVA (CC BY 4.0). Verificado en v4 y v5 |
| Ajuntament de València | Distritos, padrón | Libre | Sí | CC BY 4.0 (portal de datos abiertos) |
| CGPJ, Ministerio del Interior | Lanzamientos, criminalidad | Con cita | Agregados publicados | Condiciones de reutilización de cada portal; no verificadas en detalle |
| AEAT | Estadística de declarantes del IRPF | Con cita | Agregados publicados | Ley 37/2007; no verificado en detalle |
| BOE | Normas (RD de planes, RD 1020/1993) | Libre | Sí | Dominio público (art. 13 TRLPI) |
| Congreso de los Diputados | Proposiciones de ley | Libre | Sí | Textos oficiales (art. 13 TRLPI) |
| Partidos políticos | Programas electorales (PDF de webs oficiales) | Cita breve con fines de investigación (art. 32 TRLPI) | Copias versionadas en data/raw/v5/programas, con URL y hash, porque `make all` las necesita para reproducir los recuentos | Derechos del titular; los entregables solo citan fragmentos ≤40 palabras. **El autor debe confirmar si la copia es admisible; si no, se sustituye por URL + hash y el texto extraído deja de versionarse** |
| Inside Airbnb | Agregados de anuncios (solo robustez) | Libre | Sí | CC BY 4.0 |

**Pendiente:** antes de publicar, el autor debe confirmar las condiciones del Notariado, Registradores, CGPJ y AEAT, y la de las copias de los programas (docs/v5/tareas_autor.md).

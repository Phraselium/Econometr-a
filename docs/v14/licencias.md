# V14.2 · Condiciones de uso de Registradores, Notariado y AEAT (informe, no decisión)

Consultado el 2026-10-16. Hay copias en texto de cada página, con su URL y la fecha de consulta, en [licencias/](licencias/). Son solo para uso interno: no entran en el árbol público ni en el paquete (src/v14/arbol_publico.py y src/v13/paquete_zenodo.py las excluyen).

Este documento informa; no decide. La decisión es del autor y se fija en proyecto.json, campo `terceros_1_0` (escenarios en [escenarios.md](escenarios.md)). Las citas son literales. Donde el texto no dice algo, se marca **NO CONSTA** y no se rellena con suposiciones.

**Clave de las respuestas:**
- **CLARO**: el texto lo dice expresamente.
- **AMBIGUO**: el texto toca el punto, pero admite más de una lectura o choca con otra cláusula.
- **NO CONSTA**: ninguna cláusula lo trata.

**Qué series usa el proyecto de cada fuente** (src/extract_*.py, src/v11/fetch_aeat_irpf_municipios.py):
- **Registradores:**
  - conjunto de datos abierto «Compraventas de inmuebles, uso residencial, por provincia» (opendata.registradores.org): precio por m², número e importe. Lo usan los paneles provinciales y nacionales y la mayoría de las 91 cifras que dependen de esta fuente;
  - Anuario de la Estadística Registral Inmobiliaria (ERI, PDF): cuotas de compradores extranjeros y compraventas por tipo. Lo usan 5 cifras: A23-P5 y CA-CT-ratio-triang-2022 a 2025.
- **Notariado:**
  - informes del Consejo General del Notariado (CGN) y de su Centro de Información Estadística (CIEN) en notariado.org;
  - informes del Colegio Notarial de Valencia sobre compras de extranjeros.
  - No se usa el Portal Estadístico del Notariado (penotariado.com); sus condiciones se recogen porque es el portal estadístico vigente del CGN.
- **AEAT:**
  - Estadística de los declarantes del IRPF por municipios;
  - Estadística de declarantes del IRPF y de viviendas declaradas (tablas nacionales y por CCAA).

## 1. Colegio de Registradores (CORPME)

**Fuentes consultadas:**
- Aviso legal: https://www.registradores.org/aviso-legal
- Portal estadístico registral: https://www.registradores.org/actualidad/portal-estadistico-registral
- Portal de datos abiertos:
  - aviso legal: https://opendata.registradores.org/aviso-legal
  - términos y condiciones: https://opendata.registradores.org/terminos-y-condiciones-de-uso-del-servicio
  - ficha del conjunto de datos: https://opendata.registradores.org/dataset/dataset/compraventas-de-inmuebles-uso-residencial-por-provincia
- Texto de la ODbL 1.0: https://opendatacommons.org/licenses/odbl/1-0/
- Página de créditos del Anuario ERI 2025: data/raw/pdf/originales/registradores_eri_anuario_2025.pdf. Los de 2023 y 2024 llevan la misma nota.

La primera petición a opendata.registradores.org fue rechazada por su cortafuegos. Con cabeceras de navegador, la página respondió.

### Cláusulas relevantes (literales)
**Aviso legal de registradores.org.** El de opendata.registradores.org dice lo mismo.
- **Reutilización y redistribución:**
  > «Quedan reservados todos los derechos de propiedad intelectual e industrial sobre los Contenidos del Sitio Web y, en particular, queda prohibido modificar, copiar, reproducir, comunicar públicamente, poner a disposición, transformar o distribuir, por cualquier medio y bajo cualquier forma, la totalidad o parte de los contenidos incluidos en el mismo, para propósitos públicos o comerciales, si no se cuenta con autorización previa, expresa y por escrito de CORPME o, en su caso, del titular de los derechos correspondientes.»
- **Alcance del uso:**
  > «Al acceder al Sitio Web, el usuario adquiere un derecho de uso de los contenidos y/o servicios del Sitio Web dentro de un ámbito doméstico y únicamente con la finalidad de disfrutar de las prestaciones del servicio de acuerdo con el presente Aviso Legal.»
- **Condiciones particulares** (solo en el aviso de opendata):
  > «No obstante, el acceso a determinados contenidos y la utilización de concretos servicios puede encontrarse sometido a condiciones particulares, que serán en todo caso claramente mostrados. Estas condiciones particulares podrán sustituir, completar o, en su caso, modificar los términos del presente Aviso Legal. En caso de contradicción, siempre y en todo caso, prevalecerán las condiciones particulares.»
- **Avisos de derechos:**
  > «Asimismo, queda prohibido suprimir o manipular las indicaciones de copyright u otros créditos que identifiquen a los titulares de derechos de los contenidos del Sitio Web […]»

**Ficha del conjunto de datos abierto** (licencia):
> «Licencia — Open Data Commons Open Database License 1.0»

**ODbL 1.0:**
- **Obras derivadas y atribución:**
  > «4.3 Notice for using output (Contents). Creating and Using a Produced Work does not require the notice in Section 4.2. However, if you Publicly Use a Produced Work, You must include a notice associated with the Produced Work reasonably calculated to make any Person that uses, views, accesses, interacts with, or is otherwise exposed to the Produced Work aware that Content was obtained from the Database, Derivative Database, or the Database as part of a Collective Database, and that it is available under this License.»
  > «a. Example notice. The following text will satisfy notice under Section 4.3: Contains information from DATABASE NAME, which is made available here under the Open Database License (ODbL).»
- **Redistribución:**
  > «4.2 Notices. If You Publicly Convey this Database, any Derivative Database, or the Database as part of a Collective Database, then You must: a. Do so only under the terms of this License or another license permitted under Section 4.4; b. Include a copy of this License […] or its Uniform Resource Identifier (URI) with the Database or Derivative Database […]; and c. Keep intact any copyright or Database Right notices and notices that refer to this License.»
- **Bases de datos derivadas:**
  > «4.4 Share alike. a. Any Derivative Database that You Publicly Use must be only under the terms of: i. This License; ii. A later version of this License similar in spirit to this License; or […]»
- **Uso comercial:** la ODbL no lo restringe.

**Anuario ERI** (página de créditos):
> «No está permitida la reproducción total o parcial de este libro, ni su tratamiento informático, ni la transmisión de ninguna forma o por cualquier otro medio, ya sea electrónico, mecánico, por fotocopia, por registro u otros métodos, sin el permiso previo y por escrito del Copyright.»

### Respuestas
| Pregunta | Datos abiertos (ODbL) | Anuario ERI |
|---|---|---|
| (a) ¿Agregados propios citando la fuente? | **CLARO** (sí): un resultado propio es una «Produced Work» (4.3); el aviso legal cede ante las condiciones particulares | **AMBIGUO**: se prohíben la reproducción y el «tratamiento informático» sin permiso escrito; no se dice nada de citar cifras agregadas propias |
| (b) ¿Redistribuir la serie descargada? | **CLARO** (sí), con condiciones: bajo la ODbL, con su URI y los avisos (4.2). Una base derivada que se publique debe ir bajo la ODbL (4.4) | **CLARO** (no), sin permiso previo y por escrito |
| (c) ¿Qué atribución exige? | **CLARO**: aviso del tipo «Contains information from [nombre del conjunto, con enlace], which is made available here under the Open Database License (ODbL)» (4.3) | **NO CONSTA** |

**Lo que choca:**
- El aviso legal general reserva todos los derechos y limita el uso al ámbito doméstico.
- La ficha del conjunto de datos lo publica bajo la ODbL.
- El propio aviso de opendata resuelve el choque a favor de las condiciones particulares («prevalecerán»). Aquí se lee así porque lo dice el texto; no hay respuesta escrita de CORPME que lo confirme.

## 2. Consejo General del Notariado (CGN)

**Fuentes consultadas:**
- Aviso legal de notariado.org: https://www.notariado.org/portal/aviso-legal
- Aviso legal del CIEN: https://www.notariado.org/liferay/web/cien/aviso-legal
- Portal Estadístico del Notariado:
  - aviso legal: https://penotariado.com/inmobiliario/aviso-legal
  - términos y condiciones: https://penotariado.com/inmobiliario/terminos-y-condiciones
- Aviso legal del Colegio Notarial de Valencia: https://valencia.notariado.org/portal/aviso-legal

La URL anotada en V14.1 para el portal estadístico (https://www.notariado.org/portal/estad%C3%ADsticas) devuelve 404. El portal vigente es penotariado.com.

### Cláusulas relevantes (literales)
**Aviso legal de notariado.org.** El del CIEN y el del Colegio Notarial de Valencia dicen lo mismo, cambiando el titular.
- **Propiedad:**
  > «Toda la información contenida en este Sitio Web así como el diseño gráfico, imágenes, códigos fuente, marcas, nombres comerciales, denominaciones, artículos, informes, etc…, están sujetos a los derechos de propiedad intelectual e industrial del CGN o de terceros.»
- **Reutilización, redistribución, obras derivadas y uso comercial:**
  > «Bajo ningún supuesto, el acceso al Sitio Web supone la renuncia, transmisión, cesión o licencia total o parcial de dichos derechos de propiedad intelectual o industrial, ni confiere ningún derecho de utilización, traducción, adaptación, alteración, explotación, reproducción, distribución o comunicación pública, con fines comerciales, de dichos contenidos sin la previa y expresa autorización del CGN o del tercero titular de los derechos afectados. Quedan a salvo los derechos del Usuario de visualizar y obtener una copia en la memoria caché del ordenador del Usuario, como reproducción transitoria y accesoria, sin que en ningún caso esté autorizado para comunicar la misma a terceros.»

**Portal Estadístico del Notariado** (términos y condiciones).
- **Uso de los datos:**
  > «4. Condiciones de utilización de los datos del Portal. El CONSEJO GENERAL DEL NOTARIADO permite a todo Usuario público o registrado el acceso y uso de los servicios de datos ofrecidos por el Portal para su uso exclusivo personal no permitiéndose el uso comercial de los mismos, sin que ello suponga, en ningún caso, ningún otro derecho, comprometiéndose el Usuario a no incorporar dichos datos a bases de datos o ficheros informatizados que puedan ser susceptibles de consulta individualizada con fines comerciales por otras personas físicas o jurídicas y, ello, aunque se exprese la procedencia de la información.»
- **Reproducción y transformación:**
  > «6. Propiedad intelectual e industrial. […] queda prohibida la reproducción, distribución, comunicación pública, transformación y/o puesta a disposición del público de todo o parte del Servicio y/o sus contenidos, sin la previa autorización expresa del CONSEJO GENERAL DEL NOTARIADO.»

**Informes del CIEN** (pie de las tablas; es una mención de procedencia, no una licencia):
> «Fuente: Centro de Información Estadística del Notariado (CIEN).»

### Respuestas
| Pregunta | Informes de notariado.org y del Colegio de Valencia (los que usa el proyecto) | Portal Estadístico (no usado) |
|---|---|---|
| (a) ¿Agregados propios citando la fuente? | **AMBIGUO**: la prohibición se refiere a fines comerciales; para el uso no comercial no se concede ni se prohíbe nada expresamente («no confiere ningún derecho […] con fines comerciales»; «bajo ningún supuesto […] licencia») | **CLARO** (no sin autorización): «uso exclusivo personal»; se prohíbe la «transformación» y la «puesta a disposición del público» sin autorización |
| (b) ¿Redistribuir la serie descargada? | **AMBIGUO**: no hay licencia; la prohibición expresa solo cubre los fines comerciales | **CLARO** (no) |
| (c) ¿Qué atribución exige? | **NO CONSTA** (los informes rotulan «Fuente: Centro de Información Estadística del Notariado (CIEN)», sin exigir una forma de cita) | **NO CONSTA** |

## 3. Agencia Estatal de Administración Tributaria (AEAT)

**Fuentes consultadas:**
- Aviso legal: https://sede.agenciatributaria.gob.es/Sede/condiciones-uso-sede-electronica/aviso-legal/aviso-legal.html
- Utilización de la información: https://sede.agenciatributaria.gob.es/Sede/condiciones-uso-sede-electronica/aviso-legal/utilizacion-informacion-contenida-web-aeat.html
- Propiedad intelectual: https://sede.agenciatributaria.gob.es/Sede/condiciones-uso-sede-electronica/aviso-legal/propiedad-intelectual.html
- Condiciones de reutilización: https://sede.agenciatributaria.gob.es/Sede/gobierno-abierto/reutilizacion-informacion/condiciones-reutilizacion.html
- Estadísticas: https://sede.agenciatributaria.gob.es/Sede/estadisticas.html
- Portada de la estadística de declarantes del IRPF por municipios 2023: https://sede.agenciatributaria.gob.es/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/Estadisticas/Publicaciones/sites/irpfmunicipios/2023/home.html

El catálogo de datos abiertos de la AEAT en datos.gob.es no se pudo consultar: devuelve 403 desde este entorno.

### Cláusulas relevantes (literales)
**Utilización de la información** (página actualizada el 03/02/2022):
> «La información disponible en el sitio web de la Agencia Tributaria, salvo indicación expresa en contrario, es susceptible de reutilización, quedando autorizada su reproducción total o parcial, modificación, distribución y comunicación, para usos comerciales y no comerciales, con sujeción a las siguientes condiciones: Queda prohibida en cualquier circunstancia la desnaturalización del contenido de la información. Es obligatorio citar la fuente de los documentos objeto de la reutilización. Es obligatorio mencionar la fecha de la última actualización, cuando esté disponible, de los documentos objeto de la reutilización.»

**Condiciones de reutilización** (página actualizada el 02/10/2023):
> «Está prohibido desnaturalizar el sentido de la información. Debe citarse la fuente de los documentos objeto de la reutilización, citando el órgano administrativo, organismo o entidad del sector público estatal de que se trate. Debe mencionarse la fecha de la última actualización de los documentos objeto de la reutilización, siempre cuando estuviera incluida en el documento original. No se podrá indicar, insinuar o sugerir que el titular de la información reutilizada participa, patrocina o apoya la reutilización que se lleve a cabo con ella. Deben conservarse, no alterarse ni suprimirse los metadatos sobre la fecha de actualización y las condiciones de reutilización aplicables incluidos, en su caso, en el documento puesto a disposición para su reutilización.»

**Propiedad intelectual** (página actualizada el 03/02/2022). Es la cláusula en la que se basó E4 en V14:
> «Los derechos de propiedad intelectual del sitio web de la Agencia Tributaria, su diseño gráfico y los códigos que contiene son titularidad de la Agencia Tributaria, a no ser que se indique una titularidad diferente. La reproducción, distribución, comercialización o transformación no autorizadas de estas obras constituye una infracción de los derechos de propiedad intelectual de la Agencia Tributaria o de quien sea titular de las mismas.»

**Portada de la estadística del IRPF por municipios 2023:** en el texto de la página no consta ninguna «indicación expresa en contrario».

### Respuestas
| Pregunta | Respuesta |
|---|---|
| (a) ¿Agregados propios citando la fuente? | **CLARO** (sí): «autorizada su reproducción total o parcial, modificación, distribución y comunicación, para usos comerciales y no comerciales», sin desnaturalizar el contenido |
| (b) ¿Redistribuir la serie descargada? | **CLARO** (sí), con las mismas condiciones, «salvo indicación expresa en contrario». En la portada consultada no consta ninguna |
| (c) ¿Qué atribución exige? | **CLARO**: citar la fuente nombrando el organismo, mencionar la fecha de la última actualización si el documento la incluye, no sugerir que la AEAT apoya la reutilización y conservar los metadatos de fecha y condiciones |

**Corrección de E4 (V14).** E4 leyó solo la cláusula de propiedad intelectual. Esa cláusula se refiere al «sitio web […], su diseño gráfico y los códigos que contiene» y prohíbe lo «no autorizado». La cláusula de utilización de la información sí autoriza la reutilización de la información. E4 queda superada en ese punto (decisiones.md, E4-bis).

## 4. Recomendación (PENDIENTE DE DECISIÓN DEL AUTOR)

Valor actual en proyecto.json, el que se fijó por defecto: registradores = agregados, notariado = agregados, aeat = excluir.

**Para la AEAT, «redistribuir»:**
- (a), (b) y (c) son CLARO: el sitio autoriza la reproducción, modificación y distribución con cita, fecha y sin desnaturalizar.
- Con «excluir» se retiran 5 cifras (CB-C6-01 a 05) que el texto permite publicar.
- Antes de activarlo:
  1. comprobar en la publicación de cada ejercicio que no hay indicación en contrario;
  2. añadir a docs/v5/licencias_datos.md y al LEEME del depósito la cita «Agencia Estatal de Administración Tributaria, Estadística de los declarantes del IRPF por municipios, ejercicio N, actualizada el [fecha]»;
  3. seguir el procedimiento de docs/v14/tareas_autor.md (D4).
- Alternativa prudente: «agregados». Publica las 5 cifras sin redistribuir la serie.

**Para Registradores, «agregados»** (el valor actual), añadiendo el aviso de la ODbL (4.3) junto a las cifras que salen del conjunto de datos abierto:
- «Redistribuir» sería posible para ese conjunto (CLARO). Pero obligaría a publicar bajo la ODbL las bases derivadas que lo contengan (4.4), es decir, los paneles que mezclan fuentes. Eso choca con la licencia CC BY 4.0 del resto del depósito.
- Para las 5 cifras del Anuario ERI (A23-P5 y CA-CT-ratio-triang-2022 a 2025), el permiso es AMBIGUO para agregados y CLARO en contra de la redistribución.
- Lo prudente es pedir a CORPME autorización escrita para esas 5 cifras. Si no llega, el autor puede decidir retirarlas. Hoy el campo es por fuente, no por producto: retirarlas exigiría una regla por id.

**Para el Notariado: pedir autorización escrita al CGN/CIEN antes de publicar.** Mientras tanto, dos opciones con su coste:
- «agregados» (el valor actual): se apoya en que la única prohibición expresa es el uso comercial. Es AMBIGUO.
- «excluir»: retira 6 cifras (A23-P2, A23-P7, A23-P10, K3-RATIO-2015, K3-RATIO-2023 y compradores_extranjeros). A23-P2 es una cifra C1 central del precio de compra; con «excluir» quedaría sin publicar en la 1.0.
- La redistribución de la serie no tiene apoyo en el texto (AMBIGUO en el mejor caso): no se recomienda «redistribuir».

Ninguna de estas recomendaciones se ha aplicado. El repositorio queda con los valores por defecto.

# Decisiones V7.1 (W = decisión de V7.1)

- **W0.** La v7.1 es la versión de referencia; la v6.2 pasa a histórica. La única fuente de cifras sigue siendo output/v5/cifras_clave.csv, que ahora también incorpora los hechos.json de output/v7 y output/v7_1. No se cambia ninguna cifra publicada de v6.2 o v6.3: solo se añaden filas.
- **W1.** Las tareas de texto, consolidación y estructura las hace el orquestador. Motivo: los subagentes de entregables, revisión e inventario superaron sus topes en V7 (regla de disciplina).
- **W2.** cifras_clave también lee output/v7/*/hechos.json (R4, R4b, R5, R6) y output/v7_1/*/hechos.json, nunca los `_smoke`. Solo se añaden 46 filas; ninguna cifra existente cambia (diff con solo inserciones). Las variaciones % de los escenarios R6 pueden ser negativas, así que el test test_k4a_cifras admite el prefijo V7-R6-.
- **W3.** S1 no publica un «umbral de equivalencia» frente a f2 (rebaja de impuestos y costes de construcción). Motivo: R6 traslada la rebaja al precio de todo el mercado, mientras que el coste fiscal solo cubre la obra nueva. La eficiencia por euro de f2 queda sobrestimada por construcción, y compararse con ella sesgaría la lectura. Se declara en el resumen, las fichas y el atlas.
- **W4.** Normalización de S1:
  - **Efecto por 10.000 viviendas:** solo en los instrumentos de cantidad (a-d), sobre la dosis acumulada a 10 años.
  - **Efecto por 100 M€:** sobre el coste fiscal ANUAL, porque una ayuda permanente es un flujo y el efecto en el precio es un nivel. Solo se calcula donde hay coste estimable (e, f1 y f2 en compra).
  - **Ayudas a la demanda y rebaja de ITP/IVA:** como el precio de mercado sube, el «coste por punto» se refiere al precio neto que paga el beneficiario.
  - **Dosis de f1:** todas las compraventas, igual que en R6. Es una cota superior, porque el escenario es de vivienda nueva.
- **W5.** Los costes de los instrumentos de cantidad (construcción, vacías, vivienda pública, turísticos) y el de las ayudas al alquiler quedan como «coste no estimable», con su motivo. Se da una regla de lectura: efecto por 100 M€ = efecto por 10.000 viviendas × 10.000 / u, para un coste por vivienda u. No se publica ningún u.
- **W6.** Literatura de la nota (S2): Scimago devolvió 403. Ninguna referencia queda «VERIFICADA» completa; todas figuran como «DOI verificado, cuartil no verificado» (docs/v7_1/literatura_nota.md). Las 3 revistas propuestas también quedan con «cuartil no verificado» y pasan a las tareas del autor.
- **W7.** El mensaje «domina el factor común» se apoya en una contabilidad DESCRIPTIVA, no en un modelo nuevo: el R² de la variación interanual de cada CCAA sobre la media de las 17, y la correlación media entre pares (src/v7_1/s3_hechos.py). Se declaran tres cosas:
  - la media incluye a la propia CCAA;
  - la medida no mide cargas estructurales;
  - es C4 por ser de fuente única (INE).
  
  Las demás cifras de V7 que se difunden (hipótesis confirmadas, I(2), predicción frente a la base más exigente, Monte Carlo, precio de mercado de R6 y CCAA robustas) entran en cifras_clave mediante output/v7_1/S3/hechos.json.
- **W8.** La nota metodológica es una plantilla de render (docs/v5/plantillas/nota_metodologica.md), así que cumple la regla «toda cifra sale de cifras_clave» que comprueba check_v5. Cambios asociados:
  - check_v5 admite fórmulas LaTeX en línea;
  - las líneas con parámetros del diseño, el tamaño del panel, constantes o referencias llevan «check:cifra-libre» con su motivo;
  - render escribe sin unidad las proporciones (unidad «proporción») y con dos decimales los estadísticos t.
- **W9.** En la nota se cambian «conservador» e «izquierda», en su sentido estadístico, por sinónimos neutros, para no disparar el control de neutralidad.
- **W10.** Sección única «Qué cambió» (docs/v5/plantillas/que_cambio.md, renderizada en output/v5/que_cambio.md):
  - absorbe el bloque v6.1, que estaba repetido en cinco entregables, y el detalle propio del §12 del informe técnico;
  - los entregables enlazan a ella;
  - el artículo del Colegio solo recibe una nota para el autor (comentario HTML) y dos enlaces, sin prosa nueva, como pide el encargo.
- **W11.** Las unidades de normalización («diez mil viviendas», «cien millones») se escriben en palabras en las plantillas, para que los controles de cifras huérfanas (k4c) no las confundan con resultados. Las réplicas y el número de remuestras de la nota también van en palabras.
- **W12.** Ensayo de evaluate_v7 (S4): se recorre el camino NO simulado del script, sustituyendo solo la descarga (ficheros simulados con el formato de data/raw), el registro de accesos y la carpeta de salida (temporales). No se escribe en data/raw ni en docs/v7/evaluate_v7_accesos.md, y el script comprueba que el registro real queda intacto.
- **W13.** Alquiler 2026T3: dos de sus tres meses se publicaron antes del pre-registro. Se declara antes de abrir una sensibilidad sin 2026T3 (docs/v7/desviaciones.md). La evaluación principal no cambia.
- **W14.** historico/ se construye con el criterio de la carpeta archive/ de v6.1: se mueven con `git mv`, sin modificarlos, solo los documentos de versiones cerradas que no lee ningún script, test, plantilla ni el Makefile.
  - Se movieron 60 documentos: planes, estados, bloqueos, revisiones, auditorías y arbitrajes de v1-v6.2.
  - Se movieron también los 5 de archive/.
  - **No se mueven las salidas de los modelos (output/v1-v7).** `make all` y `make v7` las regeneran en su ruta, y cifras_clave y los entregables vigentes leen de ellas. Moverlas obligaría a reescribir rutas en cientos de scripts cerrados y pondría en riesgo la reproducibilidad.
  - historico/INDICE.md indica dónde está cada versión.
  - Las rutas que citaban los ficheros movidos se actualizan solo textualmente en 22 documentos, entre ellos README, CHANGELOG, MAPA y los skills de .claude.
  - k4c_cifras (v6.1) lee historico/ en lugar de archive/, que es un cambio solo de ruta. Sus salidas de `make all` cambiarán por ello.
- **W15.** publicacion/, metodologia/ y reproducir/ se generan siempre con `make publicacion`, que escribe una cabecera «no editar» y un manifiesto sha256. tests/v7_1/test_publicacion.py los regenera en un directorio temporal y exige identidad byte a byte. Los enlaces relativos se reescriben hacia la copia publicada o, si no se publica, hacia la ruta del repositorio. Las LinkedIn y los artículos de difusión no se publican en publicacion/, porque el encargo no los lista; siguen en output/v5.
- **W16. Cierre: diferencias con lo versionado.**
  - **`make v7` ×2 en un clon limpio (76683a9):** 523 ficheros con md5 idénticos y ninguna diferencia con lo versionado (git status vacío). `make check` rc=0.
  - **`make all` en otro clon:** rc=0 y `make check` rc=0. Nueve ficheros difieren:
    1. docs/v2/fallidas/ine.md: solo la marca de tiempo de la descarga, sin red. No se copia (ocurría ya en cierres anteriores).
    2. output/v2/BM/tiempos.json: tiempos de reloj. No se copia.
    3. output/informe.md (v1): cita la ruta nueva de revision_f7.md en historico/. Se copia.
    4. output/v6_1/K4C/* y output/v6_1/K4D/*: cambian por el traslado a historico/ (k4c lee historico/, k4d cuenta más .md) y por los ficheros nuevos de V7.1. Se regeneran en el repositorio.
  - **Ajustes antes de regenerar K4C y K4D, porque K4D detectó 15 enlaces rotos y una versión sin leer:**
    - los enlaces relativos de la plantilla de release notes pasan a rutas, que es lo correcto en una release de GitHub;
    - los README de output/v3 y output/v4 apuntan a historico/;
    - README.md vuelve a declarar «**Versión:** v7.1».
  - **Resultado:** 0 enlaces rotos y 580 .md revisados, igual que en el clon limpio. Se borran las carpetas ignoradas output/v7/*_smoke del repositorio de trabajo, que contaban de más.
  - **Ninguna cifra publicada cambia.** ERRATA no tiene entradas nuevas.

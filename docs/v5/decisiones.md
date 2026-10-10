# Decisiones v5

## Setup
- Rama r5/main desde r4/main (9673a4c, v4 cerrada). Push a la rama remota designada.
- CLAUDE.md pasa a v5: rutas docs/v5, output/v5; reglas nuevas (cifras_clave, ficheros versionados, recuentos oficiales, suma provincial = nacional).
- Presupuesto: la suma de los límites por módulo (4,5 M) supera el total menos la reserva (3,78 M). Manda el corte global del 80 % (3,36 M). Los entregables E los redacta el orquestador para ahorrar.
- Pendiente técnico detectado al empezar: `data/raw/gva_vut_municipio.csv` (67 MB) está versionado (>50 MB) → R1.
- R1 técnico. `gva_vut_municipio.csv` (67 MB):
  - deja de versionarse y pasa a .gitignore con checksum;
  - la copia versionada es `gva_vut_municipio.csv.gz` (1,2 MB, idéntica al leerla);
  - la leen build_dataset.py y m4_run.py; fetch_gva.py trata el .gz como caché y lo regenera al descargar.
- R1 técnico. Se añaden checksums de los 7 JSON ADRH (>50 MB, ignorados). Los pares «por persona» y «por hogar» son el mismo fichero de origen: cada capa trae varios indicadores (dato1-dato9), así que no es un error.

## Diseño de cifras clave (A1) y entregables (E)
- `src/v5/cifras_clave.py` construye `output/v5/cifras_clave.csv` y `.md` a partir de los resultado.json y hechos.json de v4 y v5. No hay cifras tecleadas a mano.
  - Columnas: id, indicador, valor, min, max, unidad, periodo, cobertura, fuentes, capa, fecha_dato, ficha, origen (script:clave).
- Los entregables v5 se escriben como plantillas (`docs/v5/plantillas/*.md`) con marcadores `{{id}}` o `{{id:campo}}`. `src/v5/render.py` los rellena en output/v5/.
- `src/v5/check_v5.py` entra en `make check` y comprueba:
  1. ningún marcador queda sin resolver, y toda cifra con etiqueta de capa en un entregable procede de un marcador;
  2. suma provincial = nacional en las tablas declaradas;
  3. los recuentos de programas solo usan documentos oficiales;
  4. ningún script de `make all` lee ficheros de data/raw no versionados (comprobación estática de nombres literales, excluidos los fetch);
  5. el léxico valorativo o partidista en E4, E5 y E8 (reutiliza check_texto).

## R1 técnico (orquestador)
- BK-045. Orden cronológico de las ediciones del Notariado en extract_notariado.py; queda en ERRATA.md.
- BK-046. Nombres de los 19 distritos SERPAVI de València:
  - nombres tomados de la capa oficial de distritos del Ajuntament (geoportal, CC BY 4.0, descargada el 2026-10-10, en data/raw/v5);
  - supuesto declarado: el código 46250dd corresponde al distrito municipal dd (19 = 19);
  - salida en output/v5/R1T, sin tocar output/f6 (v1 cerrada).
- BK-044. Fe de erratas de las notas de v2 en ERRATA.md, sin reescribir output/v2.
- BK-047. El blob de 95 MB de serpavi_v2_municipios.csv sigue en el historial remoto (a011c2f). No se reescribe, porque el force push está denegado; queda documentado.
- Los subagentes trabajan en el árbol principal con rutas disjuntas (src/v5/<módulo>_*, output/v5/<MÓDULO>), sin commit. No hacen falta worktrees porque no hay ficheros compartidos; esto cumple el límite de 3.

## R1a, R1b y R1c (subagentes)
- **R1a.**
  - Una frase de la ficha R1A-V1 con lenguaje causal («se debe a») se reescribe sin él.
  - BK-014 (alquiler de temporada) queda NO ANALIZADA: el agente no probó endpoints de red, así que sigue en el backlog.
- **R1b.** r1b_donut leía `serpavi_v2_municipios.csv` (95 MB, sin versionar) y pasa a leer el `.csv.gz` versionado. Lo detectó check_v5.
- **R1c.** La tenencia en propiedad es C1 (EFF, ECV y Censo, 72-76 %). En v4 el Censo era C4 por ser fuente única; ahora hay tres fuentes independientes.

## A2-A3 (subagente) y A6 (orquestador)
- **A23-V2** («el alquiler de contratos nuevos se ha duplicado»).
  - El agente había puesto una capa mixta con CONTRADICHA.
  - Por la regla B5, la cuantía nacional es de fuente única (IPVA, C4): ANALIZADA, NO CONCLUYENTE a escala nacional.
  - La contradicción en Cataluña y C. Valenciana (C1) se dice en la regla.
- **A6.** Consolidación documental de v4 M0, sin nuevas estimaciones (output/v5/A6/nota.md). check_v5 impide etiquetar los topes como C3.

## A4 (subagente + orquestador)
- **Coste oficial en nivel.**
  - Solo se obtuvo el MBC de 1993 (RD 1020/1993), actualizado con el índice de costes de Eurostat: 422-932 €/m², derivado y único para toda España.
  - Fallaron los módulos de protegida de las CCAA y el presupuesto de ejecución material de visados (docs/v5/fuentes_fallidas.md).
- **Corrección del orquestador.**
  - El MBC es un módulo de valoración fiscal y puede quedar por debajo del coste de mercado. Por eso C2 exige que la clase se mantenga en la UNIÓN del rango oficial derivado y el rango supuesto de v4 (422-1.500 €/m²).
  - Provincias C2 en 2021-2025: 8 de clase 1 y 3 de clase 2 (el agente daba 27 y 4).
  - En 2012-2025 la estabilidad solo se mide con el rango oficial, porque no hay clasificación v4 comparable; se marca así.
- **Clase 4 («no falta»).** Ninguna provincia en 2021-2025; 247 municipios.
- **Concentración del déficit.**
  - 2021-2025: 6 provincias suman el 50 % y 18 el 80 %.
  - 2021-2024: 6 y 17.
  - La suma provincial es igual a la nacional (700.934 y 562.692).
  - Las cuatro provincias forales solo tienen altas del Ministerio.

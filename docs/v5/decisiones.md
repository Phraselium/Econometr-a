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

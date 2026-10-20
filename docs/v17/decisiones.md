# V17 · Decisiones

## K0. V17 se ejecuta dentro de V18 (2026-10-19, orden del autor)
- El plan de V17 (docs/v17/plan.md) no se llegó a ejecutar en su momento. El autor ordena ejecutarlo dentro de V18.
- Se ejecutan completas las fases 0, 1, 2 y 3 de V17, y la 5 (integración y check_v17).
- La fase 4 (documento estilo Documento Ocasional del Banco de España) NO se ejecuta. Su contenido se integra en el Documento de Trabajo de la fase 6 de V18. Ese documento debe incluir también las secciones de V17 sobre demografía, problema general o local, factibilidad de construir, discurso público y medidas auditadas.
- CLAUDE.md sigue apuntando a V18, con una línea añadida que remite a docs/v17/plan.md.
- Todo lo de V17 es a posteriori (plan V17, sección A).

## K1. Subagentes sin worktree (2026-10-19)
- El plan pide worktrees para los subagentes que escriben.
- Quedan unos 4 GB de disco, y cada worktree con data/ enlazada y salidas ocupa varios GB.
- Los subagentes de V17 escriben en ficheros disjuntos (un grupo por fichero, nombres distintos en src/v17/, output/v17/ y tests/v17/) y nunca en src/econ_utils.py ni en data/ de versiones anteriores. Por eso trabajan en el árbol principal.
- Siguen siendo como máximo 3 a la vez.
- El orquestador revisa el diff de cada uno antes del commit.

## K2. Ficheros de terceros fuera de git (2026-10-19)
- Los PDF de data/raw/v17 se dejan fuera de git (.gitignore), con su sha256 en el _manifest.csv de cada carpeta.
- InsideAirbnb también queda fuera: su licencia es CC BY 4.0, pero su política pide no republicar los datos.
- Solo se versionan agregados propios.
- Los Registradores se guardan en _terceros/, también ignorada.

## K3. B4 (mejor estimación por canal) después de la auditoría (2026-10-19)
- La mejor estimación razonada de B4 combina nuestros datos con la inferencia de B2, el Banco de España, el BCE y la literatura con diseño creíble. La literatura de cada canal la reúnen los auditores de la fase 3.
- Por eso B4 se escribe al terminar la primera ronda de la auditoría, en docs/v17/mejor_estimacion.csv. src/v17/f2_lectura_bde.py la une a la tabla comparativa.
- Es juicio experto y se rotula así.

## K4. IPV por CCAA en D3-2 con comunidades de bloques sellados en v6 (incidencia, 2026-10-19)
- D3-2 (src/v17/d3_cuantitativo.py) usó el IPV y el esfuerzo por CCAA de la base. Ahí entraban las 8 CCAA de los bloques sellados en la validación v6 (K8 de V16), entre ellas la Comunidad de Madrid, uniprovincial. El filtro `not muestra_sellada_v6` de la base no las excluye, porque no marca las filas de CCAA (src/v10/base.py). Corregido el 2026-10-20: antes se decía «de data/raw».
- No es un acceso al directorio de la muestra sellada ni a filas marcadas como muestra_sellada_v6, así que no es la parada E. Sí va contra el criterio del proyecto de no usar las unidades selladas en las estimaciones.
- La revisión de la auditoría recalcula la cuota común con las 9 CCAA restantes: 81 % (63 % hasta 2024), cifra V17-AUD-OT-D32-IPV-CCAA-SIN-SELLADAS. La conclusión no cambia.
- En V18 toda estimación excluye las unidades selladas (plan V18, sección A), también cuando el dato viene de data/raw.

## K5. Guarda de fuga v6 en make check (decisión del autor del 2026-10-20)
- **check_v17, control «fuga v6».** Todo script de src/v17/ o posterior que lea datos (data/raw, data/processed, la base o la tabla de territorios) debe hacer una de estas dos cosas:
  - excluir las unidades de los bloques sellados de v6 con `holdout.excluir_sellados_v6(df, columna, nivel)`, que filtra las ocho CCAA de K8 y sus provincias, municipios, distritos y secciones;
  - declarar `ALCANCE_TERRITORIAL`: «nacional», «sin lectura de datos» o «reproduce publicado». Esta última es para los scripts que solo leen a través de los cargadores de la versión publicada que reproducen, ya cubiertos por la guarda «lecturas v6» de check_v15.
- **Incidente de D3.** La guarda lo habría detectado: tests/v17/test_fuga_v6.py lo comprueba con la versión del script del commit 415eb90.
- **Límite.** Es un control estático. Comprueba que el script usa el filtro, no que lo aplique en cada lectura. La revisión de cada script (y el abogado del diablo) cubre el resto.
- **V18.** Todos los scripts de V18 quedan sometidos a esta guarda.

# V14 · Decisiones

## E1. Incidente D3 de V13: constatado, sin apertura del sellado
- No hay entradas nuevas en los registros de acceso desde a58b426.
- La partición versionada es idéntica.
- No se pudo comparar el sha256 de data/sealed: el entorno deniega leerlo y no había huellas previas.
- Se anota en ERRATA.md y en metodologia/desviaciones_v8.md, aunque no cambia ninguna cifra (docs/v13/decisiones.md, D3).
- Regla nueva en CLAUDE.md y control en `make check` (src/v14/check_v14.py) contra los heredocs sin comillas.

## E2. Repositorio público nuevo, sin historia (resuelve D2 de V13)
- El repositorio público vivienda-espana-evidencia se genera con `make arbol_publico`: un único commit «Versión 1.0».
- No versiona datos: solo manifiestos y checksums. `make datos` los trae del depósito de Zenodo y verifica su sha256.
- Econometr-a queda archivado como historia de desarrollo. Ahí no se reescribe la historia: las etiquetas `prereg-*` siguen
  apuntando a sus commits.
- Con esto D2 deja de hacer falta: no hay que sacar data/raw de un árbol con historia, porque el árbol público nace sin
  datos ni historia.

## E3. Tablas propias con series de Notariado, Registradores o AEAT: redactadas, no excluidas (D5)
- V13 excluía del paquete las tablas de output/ cuya cabecera contenía esos nombres. Dos problemas:
  - el filtro tenía falsos positivos: «p_hipotesis_preregistrada», «especificaciones_registradas» y las cuotas de R² de Shapley;
  - la exclusión rompía enlaces publicados del verificador, del anexo y de consulta/.
- Desde V14, src/v14/terceros.py:
  - busca el nombre de la fuente como palabra;
  - mantiene una lista de tablas revisadas a mano sin series (las 2 de Shapley);
  - copia las 15 tablas afectadas sin esas columnas, en el árbol público y en el paquete.
- Búsqueda por valores de muestra en el árbol nuevo: para cada serie de los 9 ficheros brutos de Notariado y Registradores,
  se mide la fracción de sus valores presente en cada fichero, frente a un control con los mismos valores desplazados.
  - Ningún fichero supera el control en 30 puntos salvo uno: los 10 valores de `error_max` de notariado_validacion.csv,
    frente a una tabla provincial con miles de números (80 % frente a 50 % del control). Es una coincidencia: no es la serie.
- En Econometr-a no se reescribe la historia: las versiones anteriores siguen allí (docs/v8_1/datos_retirados.md).

## E4. AEAT (D4): sigue excluida
- El aviso legal de la sede de la AEAT (propiedad intelectual) reserva los derechos y no concede una licencia abierta de
  reutilización. Comprobado el 2026-10-16 en
  https://sede.agenciatributaria.gob.es/Sede/condiciones-uso-sede-electronica/aviso-legal/propiedad-intelectual.html.
- Las 7 variables `aeat_irpf_*` siguen fuera del paquete y de la capa pública que se deposita.
- Procedimiento para reincorporarlas en una 1.0.1: docs/v14/tareas_autor.md.

## E5. Tests que necesitan datos de terceros en el árbol público
- En el árbol público, sin `make datos_terceros`, los tests que leen esos datos se marcan como omitidos, con su motivo:
  paneles con series de Notariado y Registradores, ficheros brutos de esas fuentes, doble implementación, modelos de V8 y
  sellado v2.
- Solo se omite un test si falla con FileNotFoundError sobre un fichero de la lista cerrada (src/v14/terceros.py,
  REQUIEREN_TERCEROS). Cualquier otro fallo sigue siendo un fallo.
- En el repositorio de desarrollo, con los datos presentes, no se omite ninguno.
- Limitación documentada en reproducir/instrucciones.md.

## E6. Revisión externa
- La muestra de `make muestra_revision` tiene 40 cifras, 10 por capa:
  - C2 solo tiene 9 fichas distintas, y la plaza que sobra pasa a C4;
  - como mucho entra una cifra por ficha (anexo, verificador o familia de id).
- Hoja en revision_externa/hoja_revision.xlsx:
  - azul: dato fijo con su fuente;
  - negro: cálculo (amplitud del rango);
  - verde: URL tomada de la pestaña «fuentes»;
  - sin paneles inmovilizados.

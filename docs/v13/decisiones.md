# V13 · Decisiones

## D1. Versión pública única y fuente única de metadatos
- La versión pública es la **1.0** (16-10-2026). v1-V12 pasan a versiones internas de desarrollo; la correspondencia está en CHANGELOG.md.
- La versión pública, la fecha, la URL del repositorio, la web y el DOI se configuran solo en `proyecto.json`. Lo leen src/v5/render.py
  (marcadores `{{proyecto.<campo>}}` en docs/v5/plantillas), src/consulta/generar.py, src/v10/web.py y src/v13/metadatos.py
  (genera CITATION.cff y .zenodo.json; `make metadatos`, también dentro de `make publicacion`).
- Se eligió un fichero JSON en lugar de una variable del Makefile porque lo leen scripts de Python y plantillas, no solo make.
- README.md, LEEME_PRIMERO.md, CLAUDE.md y README_REPLICACION.md se escriben a mano (son puertas de entrada legibles); check_v13
  comprueba que declaran la versión pública y la URL configuradas.
- En los entregables, «versión de referencia vX» pasa a «versión interna vX» cuando se refiere a un tema; la frase «versión de
  referencia / vigente / pública / de consulta N» queda reservada a la versión pública. check_v13 lo hace cumplir.

## D2. PENDIENTE DEL AUTOR · Sacar data/raw del árbol de trabajo tras el depósito (propuesta; no ejecutada)
Hoy git versiona 1.212 MB de data/, de los que 1.072 MB son data/raw. Propuesta para después de publicar el DOI de Zenodo:
1. **Qué queda versionado:**
   - los manifiestos (data/raw/_manifest.csv, data/raw/v9/_manifest.csv, data/raw/v11/_manifest.csv y los de cada fuente), con
     URL, edición, fecha, licencia y sha256 de cada fichero;
   - data/CHECKSUMS.sha256, docs/v13/datos_inventario.csv y los scripts de descarga (src/fetch_*, src/v9/fetch_*, src/v11/fetch_*);
   - un fichero nuevo, `data/DEPOSITO.json`, con el DOI del depósito, la URL de cada fichero en Zenodo
     (`https://zenodo.org/records/<id>/files/<ruta>`) y su sha256.
2. **Qué sale del índice:** los ficheros de clase (a) de data/raw, por ejemplo con `git rm -r --cached data/raw` más una línea
   en .gitignore que excluya los manifiestos.
   - Siguen en disco y en el historial: no se reescribe la historia.
   - Quien clone versiones anteriores las tiene completas.
3. **Recuperación:** un objetivo nuevo, `make datos_deposito` (src/v13/datos_deposito.py, por escribir), que:
   - descarga del DOI de Zenodo los ficheros que falten, sin otra red alternativa;
   - verifica cada sha256 contra el manifiesto y falla si alguno difiere;
   - no toca nada versionado (mismo patrón que `proteger_versionados`).
   `make all` lo llamaría al principio si falta algún fichero. Sin red y con los datos ya en disco, solo verificaría.
4. **Coste y riesgos:**
   - un clon limpio pasa a necesitar red una vez (Zenodo), como ya ocurre con `make datos_terceros`;
   - si Zenodo no responde, no hay alternativa: se acepta, porque es un archivo con DOI y preservación a largo plazo;
   - un depósito nuevo (1.1, …) exige actualizar DEPOSITO.json y regenerar el inventario.
5. **Decisión que toma el autor:**
   - si se hace;
   - si data/processed (34,5 MB) también sale del índice, ya que se regenera con `make clean`;
   - y cuándo, después del depósito.

## D3. Incidencia de proceso (2026-10-16, bloque B)
- Al escribir docs/v13/datos_deposito.md con un heredoc de shell sin comillas, bash ejecutó tres órdenes que aparecían entre
  comillas invertidas en el texto:
  1. `python3 src/v13/inventario_datos.py --todo RUTA`;
  2. `make clean`, que ejecuta build_dataset, build_dataset_v2 y holdout.py build;
  3. `make all`, que pasó por `make data` y entró en el primer módulo de modelos (src/f2_nacional.py).
- Se detuvo en f2_nacional, en menos de dos minutos.
- **Efectos comprobados:**
  - data/processed y output/f2 se reescribieron con contenido idéntico: git no muestra cambios;
  - `make data` solo cambió la marca de tiempo de docs/v2/fallidas/ine.md, que se restauró con git;
  - holdout.py build reconstruyó data/sealed por la vía permitida (src/holdout.py). Esa función no evalúa ni registra
    accesos: docs/v2/holdout_accesos.md no cambió y no se leyó ninguna muestra sellada;
  - no cambió ninguna cifra (check_v13).
- **Corrección:** a partir de ahora, todo texto se escribe con el editor o con heredoc entrecomillado (`<<'EOF'`).

## D4. PENDIENTE DEL AUTOR · Licencia de la AEAT (IRPF por municipios)
- El manifiesto V11 dice «redistribuible: sí» (Ley 37/2007); docs/v5/licencias_datos.md y V8.1 dicen «no verificada en detalle».
  Se reportan las dos.
- Hasta que el autor la confirme:
  - el paquete de Zenodo excluye el fichero y las 7 variables `aeat_irpf_*` de la capa pública;
  - la base y la web versionadas no cambian.
- Si el autor confirma una licencia abierta, basta con vaciar `EXCLUIR_PUBLICA` en src/v13/paquete_zenodo.py y quitar la regla
  AEAT de src/v13/inventario_datos.py.

## D5. PENDIENTE DEL AUTOR · Derivados versionados con series de Notariado y Registradores
- Afecta a 5 paneles de data/processed y a 20 tablas de output/. Contienen series publicadas por fuentes cuya reutilización no
  está verificada.
- V8.1 retiró los ficheros brutos, pero no estos derivados.
- El paquete los excluye. Retirarlos también del índice de git (como en V8.1) cambiaría lo que `make all` necesita: un clon
  limpio tendría que ejecutar `make datos_terceros` antes de `make all`, que es lo que ya documenta README_REPLICACION.
- Decide el autor.

## D6. Redondeo de la página para lectores no técnicos
- Los campos `breve` y `rango_breve` de src/v5/render.py escriben las cifras grandes en «mil» o «millones», por ejemplo
  «998 mil hogares (982-1.013 mil)».
- El primer intento redondeaba a 3 cifras significativas («998.000»). tests/test_k4c_cifras.py lo rechazó con razón: una cifra
  así no se puede trazar hasta cifras_clave.
- Con la escala, cada cifra coincide con su valor de cifras_clave dentro de la precisión con que se escribe, y el test lo
  comprueba. No cambia ninguna cifra; solo su presentación.

### D3 · Verificación posterior (V14, bloque 0, 2026-10-16)
- **Registros de acceso.** Entre a58b426 (último commit antes de V13) y e4a2a3f no cambian:
  - `git diff a58b426 e4a2a3f -- src/holdout.py docs/v2/holdout_accesos.md docs/v8/evaluate_v8_accesos.md` sale vacío;
  - el último cambio de esos registros es de V8 F6 (0cbe849, 2026-10-13).
  - **No hay entradas nuevas.**
- **Qué hizo `holdout.py build`.** Lee data/sealed/_full, que escribe build_dataset_v2. Vuelve a escribir data/processed/v2/train/<panel>.csv y data/sealed/<panel>.csv con la misma máscara y la misma semilla.
  - No llama a `evaluate`, `evaluate_v3`, `evaluate_v6` ni `load_full`.
  - No escribe en `_accesos.log` ni en holdout_accesos.md.
- **Salidas comparables.** La partición de entrenamiento versionada coincide en git con a58b426, incluido _sellado.json (sha256 71376693…, con las filas selladas por panel).
  - Como la parte sellada es el complemento exacto de la misma tabla con la misma máscara, su contenido es el mismo salvo que cambiara la tabla de partida.
  - Eso no es posible: la tabla sale de data/raw versionado por un script sin cambios (build_dataset_v2, último cambio en 9925f68).
- **Lo que no se pudo comprobar.** El sha256 de data/sealed:
  - data/CHECKSUMS.sha256 no tiene huellas de data/sealed;
  - no hay huellas anteriores a V13;
  - el entorno deniega listar o leer data/sealed.
  - Queda como limitación declarada (ERRATA.md y metodologia/desviaciones_v8.md, 2026-10-16).
- **Conclusión.** Hubo regeneración, pero ni apertura ni evaluación. Ninguna cifra cambia.
- **Propuesta para el autor (docs/v14/tareas_autor.md):** registrar en su máquina el sha256 de data/sealed en un fichero versionado, para poder compararlo en el futuro.

## Seguimiento en V14 (2026-10-16)
- **D2 · resuelta por el bloque 1 de V14.** El repositorio público vivienda-espana-evidencia nace sin datos y sin historia (`make arbol_publico`). Los datos vienen del depósito de Zenodo (`make datos`). No hace falta sacar data/raw de Econometr-a, que queda archivado. Detalle en docs/v14/arbol_1_0.md y docs/v14/decisiones.md, E2.
- **D4 · se mantiene la exclusión.** El aviso legal de la AEAT reserva los derechos. Procedimiento para una 1.0.1: docs/v14/tareas_autor.md.
- **D5 · resuelta.** Las 15 tablas propias con columnas de Notariado o Registradores van redactadas en el árbol nuevo y en el paquete. Los paneles derivados no entran. La búsqueda por cabeceras y por valores de muestra no encuentra ninguna serie de esas fuentes (docs/v14/decisiones.md, E3). En Econometr-a no se reescribe la historia.

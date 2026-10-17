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

## E3. [SUPERADA en parte por E3-bis, V14.2] Tablas propias con series de Notariado, Registradores o AEAT: redactadas, no excluidas (D5)

> Versión original de V14, que se conserva. Afirmaba que no quedaba ninguna serie en el árbol nuevo. Era incorrecto: la redacción solo miraba los .csv, y output/v6/M0/paneles/prov_compra_anual_train.csv.gz llevaba dos columnas de Registradores (ln_pm2_registradores, ln_cv_registradores). Ver E3-bis.
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

## E4. [SUPERADA por E4-bis, V14.2] AEAT (D4): sigue excluida
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

## E3-bis. D5 corregida (V14.1-V14.2): el .csv.gz que se escapaba y el escaneo de todos los formatos
- **Qué falló en E3.** src/v14/terceros.py solo revisaba ficheros .csv. La búsqueda por valores de muestra tampoco abría los .gz.
  - output/v6/M0/paneles/prov_compra_anual_train.csv.gz entró en el árbol de V14 (origen cb19106) y en el paquete de entonces con dos columnas de Registradores: ln_pm2_registradores y ln_cv_registradores.
  - Ese árbol no se publicó y el paquete no se subió a Zenodo.
- **Corrección V14.1.** terceros.py revisa también .csv.gz y reconoce «registr» como palabra. Pasan a ser 16 tablas redactadas.
- **Corrección V14.2.**
  - terceros.py escanea:
    - .csv y .gz: cabecera;
    - .parquet: columnas, y los valores de las columnas `variable`, `serie` e `indicador`;
    - .xlsx: todas las hojas;
    - .zip: ficheros internos;
    - .json: claves;
    - .duckdb: tablas y columnas.
  - src/v14/escaneo_terceros.py añade dos búsquedas: por nombre de fichero y por valores (contra los ficheros brutos de cada fuente, con control).
  - Se aplica al repositorio, al árbol público y al paquete. Resultado: docs/v14/escaneo_terceros.md.
- **Lo que apareció.** Once ficheros de output/ eran la serie o la reproducían aunque ninguna columna nombrara la fuente:
  - Notariado de València (f6, M4);
  - AEAT municipal y nacional (v12/f0, CB);
  - CGPJ (CB).

  Ahora se vacían. Quedan la cabecera o una nota, para que no se rompa ningún enlace.
  - Dos tablas llevaban columnas de Registradores con otro nombre (`pm2`, `reg_compraventas_viv`…). Ahora se redactan.
  - Los agregados propios de la AEAT (output/v12/b5/aeat_cv_*) se vacían solo con aeat = «excluir».
- **Resultado.** Árbol y paquete regenerados desde d1c2162: 0 pendientes, y 0 ficheros por encima del control en la búsqueda por valores.
- **Lo que no se escanea por contenido.**
  - Las figuras no se escanean por contenido. output/f6/fig_notariado_provincia.png dibuja la serie y queda anotada para el autor.
  - Los resultados de modelos con el precio de Registradores se revisaron a mano (escaneo_terceros.csv) y son resultados propios: métricas, SHAP, ALE, PDP y el modelo ajustado.


## E4-bis. AEAT: E4 leyó solo la cláusula de propiedad intelectual (V14.2)
- E4 se basó en la cláusula de propiedad intelectual del aviso legal. Esa cláusula se refiere al sitio web, su diseño gráfico y sus códigos.
- La cláusula «Utilización de la información contenida en la web» autoriza expresamente la reproducción, la modificación y la distribución de la información, «para usos comerciales y no comerciales», salvo indicación en contrario. Lo hace con condiciones: citar la fuente, mencionar la fecha de actualización y no desnaturalizar.
- Citas y clasificación: docs/v14/licencias.md.
- La exclusión de las 7 variables `aeat_irpf_*` sigue aplicándose, porque proyecto.json fija aeat = «excluir» por defecto (decisión del autor, V14.2). Lo que cambia es el motivo: ya no es «no hay licencia abierta», sino «decisión pendiente del autor».

## E7. Política terceros_1_0 y registro de cifras íntegro (V14.2)
- proyecto.json → `terceros_1_0` fija, por fuente, «agregados», «excluir» o «redistribuir» (src/v14/terceros_1_0.py). Lo respetan:
  - `make publicacion`, a través de los marcadores de render;
  - `make consulta` y `make web`;
  - `make arbol_publico` y `make paquete_zenodo`.
- Valores por defecto (los del autor): registradores = agregados, notariado = agregados, aeat = excluir.
- **«excluir» no borra la cifra de cifras_clave.**
  - output/v5/cifras_clave.csv y su copia exacta publicacion/cifras_clave.csv siguen íntegras en todos los escenarios. Esa identidad la comprueban tests/v7_1/test_cifras_difundibles.py y tests/v10/test_base.py, y la exige check_v13.
  - Lo que se retira es la cifra en los textos (publicacion/*.md, consulta/ y las páginas de la web). En su lugar queda «[cifra no publicada en la versión 1.0: usa la serie de …]».
  - La lista de cifras retiradas va en publicacion/cifras_no_publicadas_1_0.csv.
  - Consecuencia: el valor sigue legible en publicacion/cifras_clave.csv y en la descarga de cifras_clave de la web. Quitarlo de ahí sería cambiar el registro, que es la condición de parada (a). Lo decide el autor.
- **Solo se retiran las cifras que usan de verdad la serie:** dependencia «directa» o «indirecta (el modelo usa la serie)». No se retiran las «técnicas» ni las que solo usan una estadística oficial del INE o del MIVAU que se elabora con datos de esa fuente.
- **CGPJ no tiene escenario.** Sus series nunca se redistribuyen y sus agregados se publican citando la fuente.

## E8. Registradores dividido por producto; ODbL para lo derivado de los datos abiertos; Notariado excluido (V14.3, orden del autor)
- proyecto.json → `terceros_1_0` pasa a cuatro claves:
  - registradores_odbl = «agregados»;
  - registradores_eri = «excluir»;
  - notariado = «excluir»;
  - aeat = «excluir».
- El origen de cada cifra y tabla de Registradores sale de src/v14/registradores_origen.py (docs/v14/registradores_origen.md):
  - **Cifras.** Reglas por orden:
    1. tabla manual con motivo;
    2. lo que digan `fuentes` o el enunciado;
    3. lo que lean los scripts del módulo.

    Resultado: 237 ODbL, 1 ERI (A23-P5) y 4 «ambos» (CA-CT-ratio-triang-2022 a 2025: compraventas del CSV abierto e hipotecas tecleadas del Anuario).
  - **Las «técnicas»** heredan el origen del panel y nunca se retiran.
- **Retiradas con los valores por defecto:** 16 cifras.
  - AEAT: 5 (CB-C6-01 a 05).
  - Notariado: 6 (A23-P2, A23-P7, A23-P10, K3-RATIO-2015, K3-RATIO-2023 y compradores_extranjeros).
  - Anuario ERI: 5 (A23-P5 y las 4 CA-CT).
  - Siguen en cifras_clave sin cambios. Lista en publicacion/cifras_no_publicadas_1_0.csv.
- **ODbL 1.0 (4.2-4.4).** La parte de cada fichero del árbol o del paquete construida con los datos abiertos se publica bajo la ODbL 1.0: variables, columnas, resultados de modelos con ese precio y filas de cifras_clave con origen ODbL o «ambos». Son 65 ficheros (docs/v14/licencias_tablas.csv). Se declara en:
  - LICENSE (punto 4, con el aviso);
  - .zenodo.json (`notes`) y CITATION.cff (`ODbL-1.0`), generados por `make metadatos`;
  - el diccionario de la base (sección «Licencias por tabla», escrita por src/v14/registradores_origen.py y por src/v10/base.py al regenerarlo);
  - las notas de la versión y los metadatos de Zenodo.
- **Avisos en los textos.**
  - Los textos de publicacion/ y consulta/ que citan una cifra ODbL publicada llevan al final el aviso de atribución (4.3), escrito por render y generar.
  - La web lo lleva en el pie de todas las páginas.
  - Cada hallazgo ODbL de consulta/hallazgos.json lleva `licencia` = «ODbL 1.0».
- **Las series** (columnas de los datos abiertos y del Anuario) siguen sin redistribuirse: ninguno de los dos productos está en «redistribuir».
- **No hay conflicto con CC BY 4.0.** Lo derivado de los datos abiertos queda solo bajo la ODbL, que exige el «share alike» (4.4) a las bases derivadas. El resto de cada fichero sigue bajo CC BY 4.0. No se ha cambiado data/base/variables.parquet (datos de solo lectura). Su columna `licencia` para registr_* sigue diciendo «sin licencia abierta clara». Esa base completa no entra en el árbol ni en el paquete.
- **Notariado:** solicitud de autorización en docs/v14/publicacion_1_0/solicitud_notariado.md. Si se concede, se cambia a «agregados».

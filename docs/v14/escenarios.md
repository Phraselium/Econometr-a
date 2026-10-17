# V14.2 · Escenarios de terceros_1_0: qué cambia en cada uno

> V14.3: desde E8, Registradores tiene dos claves (registradores_odbl y registradores_eri) y los valores por defecto son agregados / excluir / excluir / excluir. Las cifras de esta página corresponden a las tres claves de V14.2. Las retiradas con los valores actuales están en publicacion/cifras_no_publicadas_1_0.csv.

proyecto.json → `terceros_1_0` fija, por fuente (registradores, notariado, aeat), uno de tres valores. Implementación en src/v14/terceros_1_0.py y src/v14/terceros.py; decisión E7.

| Valor | Cifras en publicacion/, web/ y consulta/ | Serie en el árbol y en el paquete |
|---|---|---|
| «agregados» | se publican citando la fuente | no se redistribuye: columnas redactadas y tablas que son la serie vaciadas |
| «excluir» | las que usan de verdad la serie se retiran y se marcan «[cifra no publicada en la versión 1.0: …]»; siguen en cifras_clave sin cambios | como «agregados»; además se vacían los agregados propios de la serie (output/v12/b5/aeat_cv_*) |
| «redistribuir» | se publican | va al paquete: ficheros brutos de la fuente (terceros_1_0.SERIES_BRUTAS) y tablas sin redactar |

**Valor por defecto, que es el del repositorio:** registradores = agregados, notariado = agregados, aeat = excluir.

**Cómo se probó.** `python3 src/v14/escenarios.py --paquete <dir temporal>` (2026-10-16, desde be7c5a5):
- Plantillas de publicacion/ (docs/v5, v8 y v9) renderizadas y consulta/ generada en memoria. Se comparan con el render sin retiradas.
- Acciones sobre output/ en el árbol público.
- `make paquete_zenodo` completo en un directorio temporal, que después se borra.
- Resultados: [escenarios_resultado.json](escenarios_resultado.json) y la lista de ids en [escenarios_cifras.csv](escenarios_cifras.csv).
- Tests: tests/v14/test_terceros_1_0.py, uno por valor más el valor por defecto.
- `make web` en local con el valor por defecto: 324 páginas. La descarga hechos.parquet de la web no tiene ninguna variable `aeat_*`.

## Resumen
Los tres valores se aplican a las tres fuentes a la vez. «Por defecto» es el valor del repositorio.

| Escenario | Cifras retiradas (Registradores / Notariado / AEAT) | Marcas en los textos | Ficheros de texto que cambian | Árbol: tablas redactadas / vaciadas | hechos.parquet sin | Paquete: tamaño · ficheros · series brutas |
|---|---|---|---|---|---|---|
| Por defecto | 0 / 0 / 5 | 11 | 3 | 17 / 13 | `aeat_*` (7 variables) | 1.322.884.416 bytes · 3.797 · 0 |
| Todas = agregados | 0 / 0 / 0 | 0 | 0 | 17 / 11 | `aeat_*` | 1.322.884.580 bytes · 3.797 · 0 |
| Todas = excluir | 91 / 6 / 5 (98 cifras distintas) | 239 | 16 | 17 / 13 | `aeat_*` | 1.322.885.019 bytes · 3.797 · 0 |
| Todas = redistribuir | 0 / 0 / 0 | 0 | 0 | 0 / 2 (CGPJ, que no tiene escenario) | nada | 1.357.352.692 bytes · 3.816 · 19 |

- Con «redistribuir», el paquete crece 34,5 MB: 19 ficheros brutos (data/raw/pdf/notariado_*.csv y registradores_*.csv, y data/raw/v11/aeat_irpf_municipios/irpf_municipios_cv.csv.gz) y las 7 variables de la AEAT en hechos.parquet.
- Entre los otros escenarios el tamaño varía en unos cientos de bytes: el texto de LEEME_DEPOSITO y las tablas vaciadas.

## Cifras afectadas, por id
Por defecto (aeat = excluir) se retiran 5 cifras: CB-C6-01, CB-C6-02, CB-C6-03, CB-C6-04 y CB-C6-05 (declarantes del IRPF y viviendas arrendadas).

Con todas = excluir se retiran 98:
- **AEAT (5):** CB-C6-01 a CB-C6-05.
- **Notariado (2):** A23-P7 y compradores_extranjeros.
- **Notariado y Registradores (4):**
  - A23-P2: precio de compra 2015-2025, núcleo MIVAU/Notariado/Registradores; C1, en una_pagina;
  - A23-P10, K3-RATIO-2015 y K3-RATIO-2023.
- **Registradores (87):**
  - A23-P4, P5, P6, P8 y P9;
  - CA-CT-ratio-triang-2022 a 2025;
  - las del módulo B3 y sus extensiones E-B3 y B4-b3: Shapley, multiverso y contrastes de H-B3-1, H-B3-2 y H-B3-6;
  - K1 y V6-M4: predicción con el precio de Registradores y RMSE de las tareas evaluadas con ese panel;
  - K2-CUOTA: cuotas de varianza;
  - V8-M8-cv-…-alt: medida alternativa de precio;
  - m2_pip_*: probabilidades de inclusión del BMA;
  - m3b_PROV_PRECIO_ANUAL_REGISTRADORES_*.

  La lista completa está en escenarios_cifras.csv.

**Nunca se retiran:**
- las cifras «técnicas»: 151 de Notariado y 151 de Registradores, que salen de un panel con esas series sin que el modelo las use;
- las que solo usan una estadística oficial del INE o del MIVAU elaborada con datos de la AEAT (IPVA, SERPAVI).

La clasificación está en docs/v14/cifras_terceros.csv.

## Páginas que cambian
**Por defecto:**
- publicacion/informe_tecnico.md: secciones 5.2 y 5.6, con 6 marcadores sustituidos;
- consulta/hallazgos.json y consulta/hallazgos.md: las 5 cifras pasan a «no publicada (1.0)», sin valor;
- la web no cambia: ninguna cifra retirada aparece en sus páginas. Cambian las descargas:
  - hechos.parquet sin las variables `aeat_*`;
  - cifras_no_publicadas_1_0.csv añadido.

**Todas = excluir:**
- publicacion/: una_pagina, lo_que_sabemos, policy_brief, informe_tecnico, working_paper, articulo_colegio, que_cambio, ponencia/diapositivas, ponencia/guion, por_que_ha_subido e informe_econometrico_v8;
- también cambian output/v5/linkedin/05.md y output/v5/articulos/c_territorio.md, que no se copian a publicacion/;
- consulta/: hallazgos.json, hallazgos.md y preguntas_frecuentes.md;
- web: igual que por defecto. Ninguna de las 98 aparece en las páginas: si una página pidiera una cifra retirada, `make web` fallaría (src/v10/web.py, `_ck`).

**Todas = agregados y todas = redistribuir:** ningún texto cambia respecto a publicar todas las cifras.

## Lo que no cambia en ningún escenario
- output/v5/cifras_clave.csv y su copia exacta publicacion/cifras_clave.csv, que también es la descarga cifras_clave de la web. Es el registro de todas las cifras. En «excluir», el valor de una cifra retirada sigue legible ahí (decisiones.md, E7). Quitarlo cambiaría el registro, que es la condición de parada (a): lo decide el autor.
- Los resultados JSON de output/ que citan valores de la fuente (escaneo_terceros.md, «revisados»). Por ejemplo, output/v12/b5/resultado.json, `aeat_cv_cuota_pct`.
- La figura output/f6/fig_notariado_provincia.png.

## Cómo activar un escenario
```bash
# 1. editar proyecto.json → terceros_1_0 (registradores, notariado, aeat)
make publicacion consulta web && make check
git commit -am "1.0: terceros_1_0 = …"
make paquete_zenodo && make arbol_publico DEST=../vivienda-espana-evidencia
```

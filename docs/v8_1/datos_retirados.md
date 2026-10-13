# Datos de terceros retirados del repositorio (V8.1, bloque C)

> **AVISO: el historial de git NO se ha reescrito.** Los 75 ficheros de esta tabla siguen presentes en el historial
> de las ramas anteriores (V1-V8 y los puntos de control de V8.1) y en cualquier clon o fork ya existente. Retirarlos del
> índice solo evita que entren en la release y en el archivo de Zenodo. Si el autor necesita que desaparezcan también
> del historial, hace falta `git filter-repo` y un `git push --force` a todas las ramas: **es una decisión del autor**
> (destructiva e irreversible para quienes ya hayan clonado); aquí no se ha hecho ni se ha preparado la orden.

Zenodo archiva para siempre lo que contiene la release. Se retiran del índice de git (`git rm --cached`; los ficheros
**siguen en disco**, ahora en `.gitignore` con ruta explícita) los ficheros de `data/raw` cuya redistribución no está
claramente permitida según `docs/v5/licencias_datos.md`. Clasificación completa de los 450 ficheros que se versionaban:
`docs/v8_1/inventario_licencias.csv` (375 permitidos se quedan; 75 retirados).

## Resumen por organismo

| Organismo | Ficheros retirados | Motivo |
|---|---|---|
| Consejo General del Notariado | 34 | Condiciones de reutilización no verificadas (tabla v5) |
| Colegio de Registradores | 17 | Condiciones de reutilización no verificadas (tabla v5) |
| AEAT | 9 | Reutilización no verificada en detalle |
| Partidos políticos (programas electorales) | 7 | Derechos del titular; la tabla v5 exige confirmación del autor |
| CGPJ | 2 | No verificadas en detalle |
| Ministerio del Interior | 2 | No verificadas en detalle |
| Comunidad de Madrid (datos abiertos) | 2 | Organismo ausente de la tabla de licencias; licencia no verificada |
| Generalitat de Catalunya (Registre de Turisme) | 1 | Organismo ausente de la tabla; licencia no verificada |
| Jarociński y Karadi (dataset académico, GitHub) | 1 | Fuente ausente de la tabla; sin licencia verificada |
| **Total** | **75** | |

Los tres últimos organismos (Madrid, Registre de Turisme, Jarociński-Karadi) no figuran en la tabla v5: se retiran por
precaución («no consta»). Si el autor verifica una licencia abierta (p. ej. CC BY 4.0) pueden reincorporarse.

## Decisión pendiente del autor

`data/raw/v4/medidas_programas.csv` (codificación propia con citas literales breves de programas, art. 32 TRLPI, sin script
de descarga) **se mantiene versionado**; no es copia de terceros pero contiene fragmentos. Confirmar que es admisible.

## Qué cambia para quien clone el repositorio

Sin red, `make all` desde un clon limpio necesita estos ficheros. Hay que ejecutar antes `make datos_terceros`
(ver abajo; `python3 src/v8_1/datos_terceros.py`): con red descarga lo que falta con los `fetch_*`/`extract_*` existentes y,
siempre, verifica el sha256 contra `data/CHECKSUMS.sha256`. Sin red solo verifica. `src/v5/check_v5.py`
(`lecturas_no_versionadas`) acepta la lectura de estos ficheros porque están en `data/CHECKSUMS.sha256` y tienen script de
descarga en el inventario (sin ese requisito, la regla sigue fallando; hay test en `tests/v8_1/test_datos_terceros.py`).

## Prueba de descarga (2026-10-13, con red, a directorio temporal; `data/raw` intacto)

Cada script se ejecutó con salida redirigida a un directorio temporal (`RAW_DIR` para los que usan `src/utils_fetch.py`;
los demás, con la ruta de destino sustituida en un envoltorio, sin editar los scripts) y se comparó el sha256 con el versionado.

- **Idéntico: 70** ficheros, incluidas las 9 páginas HTML de la AEAT y los 17 de Registradores (el CSV de validación cruzada
  `registradores_validacion.csv` solo coincide si se regenera después de los CSV de Notariado, que lee: `datos_terceros.py` respeta ese orden).
- **Idéntico en contenido, distinto en bytes: 2** (`madrid_alquiler_cp_v3.csv.gz`, `hut_registro_turismo_cat_v3.csv.gz`):
  el contenido descomprimido coincide; cambia la marca de tiempo de la cabecera gzip. `datos_terceros.py` los compara por contenido
  (`docs/v8_1/contenido_gz.sha256`).
- **Distinto con la fuente revisada: 0. Falla la descarga: 0.**
- **Sin script: 3** renders PNG de validación hechos a mano con `pdftoppm` sobre un PDF original
  (`notariado_cv_actos_2019-2020_p1.png`, `notariado_cv_val_extranjeros_4T2025_p10_zoomA.png`, `..._zoomB.png`). Procedimiento:
  descargar el PDF original con `src/extract_notariado.py` y renderizar la página con `pdftoppm -png -r <dpi> -f <p> -l <p>`;
  no se leen en ningún cálculo, solo evidencian la validación visual.

Consecuencia: la descarga desde cero reproduce hoy los mismos bytes (o el mismo contenido). **No hay garantía a futuro**: si el organismo revisa la
fuente, el sha256 diferirá y `make all` no reproduciría byte a byte; en ese caso `datos_terceros.py` informa `DISTINTO` y hay que
decidir si se actualiza el checksum (decisión registrada en `docs/v8_1/decisiones.md`).

Notas: `a5_fetch.py` reescribe `docs/v5/programas/inventario.csv` (en la prueba se redirigió); `fetch_aeat.py` no descarga nada
(sede dinámica) y las páginas AEAT salen de `src/v5/cb_fetch.py`. Varias URL de Notariado/Registradores se resuelven
rastreando sus webs, de modo que un cambio de maquetación puede romper la descarga sin que cambie el dato.

## Fichero por fichero

| Fichero (bajo data/raw) | Organismo | Motivo | Script de descarga | sha256 | Prueba de descarga |
|---|---|---|---|---|---|
| `v5/cb_aeat_irpf_2019_bienes_inmobiliarios.html` | AEAT | Ley 37/2007; reutilización no verificada en detalle (docs/v5/licencias_datos.md); página HTML de la Sede | `src/v5/cb_fetch.py` | `6406c3d4059dddbfd969d5dfcdd596edad3ff420294363a0aa6a772c0ec3175a` | idéntico |
| `v5/cb_aeat_irpf_2020_bienes_inmobiliarios.html` | AEAT | Ley 37/2007; reutilización no verificada en detalle (docs/v5/licencias_datos.md); página HTML de la Sede | `src/v5/cb_fetch.py` | `3f01f0657f04bc5a752e81c234447d55b51530637492323d0d35d9672b7a0ff8` | idéntico |
| `v5/cb_aeat_irpf_2021_bienes_inmobiliarios.html` | AEAT | Ley 37/2007; reutilización no verificada en detalle (docs/v5/licencias_datos.md); página HTML de la Sede | `src/v5/cb_fetch.py` | `17173c356d83a68b8fc0816312704909ae53fc8b505d048c94d51a4edfdecb9e` | idéntico |
| `v5/cb_aeat_irpf_2022_bienes_inmobiliarios.html` | AEAT | Ley 37/2007; reutilización no verificada en detalle (docs/v5/licencias_datos.md); página HTML de la Sede | `src/v5/cb_fetch.py` | `37c5d02b35081119f21a96929b64dcfbce8188c55668cd49982a75cc69a67702` | idéntico |
| `v5/cb_aeat_irpf_2023_bienes_inmobiliarios.html` | AEAT | Ley 37/2007; reutilización no verificada en detalle (docs/v5/licencias_datos.md); página HTML de la Sede | `src/v5/cb_fetch.py` | `a01774da94f4cc2473051240f96fce45189f42c832e7471be935d6efa709f373` | idéntico |
| `v5/cb_aeat_irpf_2024_bienes_inmobiliarios.html` | AEAT | Ley 37/2007; reutilización no verificada en detalle (docs/v5/licencias_datos.md); página HTML de la Sede | `src/v5/cb_fetch.py` | `a288ac2e0e6a0caee79ea86361a324ae8cebd54faf402c58187a622ddbbe45f4` | idéntico |
| `v5/cb_aeat_irpfviv_2024_arrendamiento_ccaa_declarante.html` | AEAT | Ley 37/2007; reutilización no verificada en detalle (docs/v5/licencias_datos.md); página HTML de la Sede | `src/v5/cb_fetch.py` | `2974ae451070fd7cddb69a3104933e7a51d01dd9eeee3e419d2c2e5c3228273b` | idéntico |
| `v5/cb_aeat_irpfviv_2024_clasificacion_uso.html` | AEAT | Ley 37/2007; reutilización no verificada en detalle (docs/v5/licencias_datos.md); página HTML de la Sede | `src/v5/cb_fetch.py` | `385d2e402c0a3ce1fa06358ecdd668a9a40622c12c2160c188fdb45f8e6ada75` | idéntico |
| `v5/cb_aeat_irpfviv_2024_cuenta_resultados_ccaa.html` | AEAT | Ley 37/2007; reutilización no verificada en detalle (docs/v5/licencias_datos.md); página HTML de la Sede | `src/v5/cb_fetch.py` | `23ac10544b0aaf05754ec518b7b1cf6e934e71b09dc4b2f8ac993f4901087ed6` | idéntico |
| `v5/cb_cgpj_lanzamientos_pj_2013_2025.xlsx` | CGPJ | Condiciones de reutilización del portal no verificadas en detalle | `src/v5/cb_fetch.py` | `6d6023a2b5c738ae0ff4360722209e50ac8ea7be971033d480869bca741c7218` | idéntico |
| `v5/cb_cgpj_series_tsj_1T2026.xlsx` | CGPJ | Condiciones de reutilización del portal no verificadas en detalle | `src/v5/cb_fetch.py` | `6c72240817fc88e2fdef7543c7c708aee57a23707700d175c419d5b4c65a8f05` | idéntico |
| `pdf/originales/registradores_eri_anuario_2023.pdf` | Colegio de Registradores | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones registrales | `src/extract_registradores.py` | `1f862a411a75e8e36e3b44c448b3afe1c3adefdce61fac2a3709e1be3f0ff152` | idéntico |
| `pdf/originales/registradores_eri_anuario_2024.pdf` | Colegio de Registradores | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones registrales | `src/extract_registradores.py` | `7e05a260ab20381508f4f1e65579c77bda94c528c760fb17fc0642ad41cb1abc` | idéntico |
| `pdf/originales/registradores_eri_anuario_2025.pdf` | Colegio de Registradores | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones registrales | `src/extract_registradores.py` | `c618eb8625acf4668f4ee344f056defa006d9dc167d3b22e916e91abb4ce84a7` | idéntico |
| `pdf/originales/registradores_opendata_compraventas_resid_2007-2T2026.csv` | Colegio de Registradores | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones registrales | `src/extract_registradores.py` | `3049f4057c4795c6821c49b16b2b07fa55490c7458bf39db72dd89495a26b7a0` | idéntico |
| `pdf/registradores_eri_anuario.csv` | Colegio de Registradores | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones registrales | `src/extract_registradores.py` | `9b010e22ae4ea41b5e29db754a854c8440c00623ff2b2114c973e151bd0f5bf4` | idéntico |
| `pdf/registradores_opendata_anual.csv` | Colegio de Registradores | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones registrales | `src/extract_registradores.py` | `36fc2598e2578c7aaae26ef2fb52a4fe2b6ca7bd4cb739f32e9efd89d90823a7` | idéntico |
| `pdf/registradores_opendata_compraventas.csv` | Colegio de Registradores | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones registrales | `src/extract_registradores.py` | `173d3af457afd2554bf475c761f7e4ca075e9d4d62fd67b80ce8d4e87a38979a` | idéntico |
| `pdf/registradores_validacion.csv` | Colegio de Registradores | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones registrales | `src/extract_registradores.py` | `0392486c6eecb1e4fed7a66f8d0182470ed1f7c7495d517edc10c3593c37ba88` | idéntico (con notariado regenerado previamente en el mismo directorio) |
| `pdf/validacion/registradores_eri_anuario_2023_p73.png` | Colegio de Registradores | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones registrales | `src/extract_registradores.py` | `150587a07671f1f6fbb5a967ff270a82dc43241cfec59cc34fd2676b63a927f7` | idéntico |
| `pdf/validacion/registradores_eri_anuario_2023_p78.png` | Colegio de Registradores | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones registrales | `src/extract_registradores.py` | `4f1f1a69ce00da699628ddf23751a6d738f92476024579d11d6e23dc26dc090c` | idéntico |
| `pdf/validacion/registradores_eri_anuario_2025_p35.png` | Colegio de Registradores | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones registrales | `src/extract_registradores.py` | `66e87ec8cc85aa6bf8c6f42c4befcd1b99d7daa3261de25a998203bcbd8aa669` | idéntico |
| `pdf/validacion/registradores_eri_anuario_2025_p40.png` | Colegio de Registradores | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones registrales | `src/extract_registradores.py` | `49e673ea16e11f80066fb3f01a8f40cfb6f9a54045804af40774102929eac91b` | idéntico |
| `pdf/validacion/registradores_eri_anuario_2025_p43.png` | Colegio de Registradores | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones registrales | `src/extract_registradores.py` | `9002f787c9476ac2a018156299e2ba611abe602b3dfbc04b3a31e51c0054b598` | idéntico |
| `pdf/validacion/registradores_eri_anuario_2025_p73.png` | Colegio de Registradores | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones registrales | `src/extract_registradores.py` | `45bbc0c22889f02ea838d6689c2032f3742eb170009e7cde14bb3dff1c81ffdb` | idéntico |
| `pdf/validacion/registradores_eri_anuario_2025_p76.png` | Colegio de Registradores | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones registrales | `src/extract_registradores.py` | `446f5270a79ccc15f9db19c9603b2a76cbbd34ec3b24529ccf1cd7dac35105e0` | idéntico |
| `pdf/validacion/registradores_eri_anuario_2025_p78.png` | Colegio de Registradores | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones registrales | `src/extract_registradores.py` | `61d3ebe5a6f12128654ecd1962d10ecfcb88faa93a6c52b246a787a61fbdc496` | idéntico |
| `pdf/validacion/registradores_eri_anuario_2025_p82.png` | Colegio de Registradores | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones registrales | `src/extract_registradores.py` | `f853481e86d4b7d3003528001577f5195dd47e2d6c0235dc2dd876587fdc37e9` | idéntico |
| `v3/madrid_alquiler_cp_v3.csv.gz` | Comunidad de Madrid (datos abiertos) | Organismo no incluido en la tabla de licencias; licencia no verificada | `src/v3/fetch_madrid_alquiler_cp_v3.py` | `9f767c895f431fc756bd2a8a9dafbde99378e75d8799a35c3b9415e8013e8a7b` | idéntico en contenido (zcat); sha del .gz distinto por marca de tiempo de la cabecera gzip |
| `v3_orig/madrid_alquiler_cp_1934258.csv` | Comunidad de Madrid (datos abiertos) | Organismo no incluido en la tabla de licencias; licencia no verificada | `src/v3/fetch_madrid_alquiler_cp_v3.py` | `15032e63a9fd25f94afe201081b4f645525f9d49b1ebf8895be85cef566536c4` | idéntico |
| `pdf/notariado_cgn_extranjeros_semestral.csv` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `e8ce62b23b1e02f4d315bca2184ac2a348c21b605e6a0e5bcbf750d3288f417b` | idéntico |
| `pdf/notariado_cv_actos_mensual.csv` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `847949a4aadcea05cbbb847cf5ec70f1e341331ba57c267be1002e918e84e71e` | idéntico |
| `pdf/notariado_cv_municipios_anual.csv` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `3b878e924f9e458180c417af71baaf0c467d6252e17982eecfed538daca362be` | idéntico |
| `pdf/notariado_cv_prov_trimestral.csv` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `af7c03eb6f59f2a3cb70239499489ac3abdb6fae66945558cb4483eeb7a34005` | idéntico |
| `pdf/notariado_validacion.csv` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `4805e1c60ef259c6bdd9e5d8e00bea37e19fd3675570a240a09a96c8a804cb38` | idéntico |
| `pdf/originales/notariado_cgn_extranjeros_2S25_anexo.xlsx` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `e0728e5c97262a67cf5a27a9cf39eaa7294782102a35c763d051969abe787319` | idéntico |
| `pdf/originales/notariado_cgn_extranjeros_2S25_informe.pdf` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `97c3c5c9203d04b11ddf9d992774b779a97984cd61c16836360c877603adf479` | idéntico |
| `pdf/originales/notariado_cv_actos_1T2026.pdf` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `ad5634777e2b14b55c0b76fc2ec35f01ee62f8b637d23e3f4549affb177b8e28` | idéntico |
| `pdf/originales/notariado_cv_actos_2019-2020.pdf` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `fedae56d46d50e06fc32662ca3f1c3db266251ae6d9841df4a22745f6cf51a39` | idéntico |
| `pdf/originales/notariado_cv_actos_2020-2021.pdf` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `ac141fbbc82c139265e1a2f00013987b92033e1f325d868f2b8c783827f8dc0a` | idéntico |
| `pdf/originales/notariado_cv_actos_2021-2022.pdf` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `e08dfa9b707a8941abd4b42c960ced593b28c544affa910d5e09683ceff4c88d` | idéntico |
| `pdf/originales/notariado_cv_actos_2022-2023.pdf` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `246c9c629d68cc008e6201762ea53b01d75322c577e419cd1e81e40bb0468d52` | idéntico |
| `pdf/originales/notariado_cv_actos_2023-2024.pdf` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `b7c83b91433c10d0cdea263d1bd7153d737242812ea16485e0db175e69c3f23e` | idéntico |
| `pdf/originales/notariado_cv_actos_2024-2025.pdf` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `2d2ff369b31d73f9e98b9e733a0161e669ca405f3a0f8fac0fd667028e4ad2dd` | idéntico |
| `pdf/originales/notariado_cv_ali_extranjeros_4T2025.pdf` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `d96af15acdfc94ccc21fd1527bc4b8484841e2295275ff82a816b4fa96338d3a` | idéntico |
| `pdf/originales/notariado_cv_cas_extranjeros_4T2025.pdf` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `15f149fd9a04f8470d8ea42858ec36cd6ef3be7f9ae572bb56038a6f4a5fa6e9` | idéntico |
| `pdf/originales/notariado_cv_val_extranjeros_4T2025.pdf` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `51c6a398ef1e69e9953ef29de7b2c6f566a912252be9a7d39883ab296d5d728f` | idéntico |
| `pdf/originales/notariado_cv_val_municipios_extranjeros_4T2021.pdf` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `5396e3c11e29e0a6d677d9813472043896d9968c73ac1c5d646b87797fd08369` | idéntico |
| `pdf/originales/notariado_cv_val_municipios_extranjeros_4T2022.pdf` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `8ec9a63524d7fb984bdaa17ae6b8c2c199b689c0876dc3570055a087bd70f4e4` | idéntico |
| `pdf/originales/notariado_cv_val_municipios_extranjeros_4T2023.pdf` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `b39e07bbd1d72b696019b2e3ab2ba79e7dd9796d5c5b0a874a7a46bcd6ae4eee` | idéntico |
| `pdf/originales/notariado_cv_val_municipios_extranjeros_4T2024.pdf` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `68de2a4d0e0c11c6b46966ca67a831b1c6454a7f72d41d1d79f94dbebfbd315d` | idéntico |
| `pdf/originales/notariado_cv_val_municipios_extranjeros_4T2025.pdf` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `471aefe292d47a5da7e534bbf93b284a7fddfe345659dd63f96f8c38c11db9bd` | idéntico |
| `pdf/validacion/notariado_cv_actos_1T2026_p1.png` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `6172c42331ffd34958bdf2a5662ede05a8ebbcd30e207e77e35912e38e0df865` | idéntico |
| `pdf/validacion/notariado_cv_actos_2019-2020_p1.png` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `(manual) render con pdftoppm del PDF original` | `74fb0bc41810b61eb374d8794ea1d5f26d415924046c9ab70504af968dfc2588` | sin script: render manual (no reproducible por descarga) |
| `pdf/validacion/notariado_cv_actos_2024-2025_p3.png` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `fef66ce4252a105d6618cc164525e1f132a2a0039f436d0c4d74a2cbd347a56d` | idéntico |
| `pdf/validacion/notariado_cv_ali_extranjeros_4T2025_p10.png` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `126a63f175401fef89f220896386ae469a31d76bd1c96462ff1854905c42bdd8` | idéntico |
| `pdf/validacion/notariado_cv_cas_extranjeros_4T2025_p2.png` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `71776af484c54dcf37d6e33fa876cfe9829c89aa9979b6413309997cd9fd11cc` | idéntico |
| `pdf/validacion/notariado_cv_val_extranjeros_4T2025_p10.png` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `af83900aaf812c0ea4799808e8f6404345829243fd62060fd4f340ed14413c55` | idéntico |
| `pdf/validacion/notariado_cv_val_extranjeros_4T2025_p10_zoomA.png` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `(manual) render con pdftoppm del PDF original` | `0952389234ad0ba80488ec9e9c85a1f3527a359d9873e154b2767f9d7b416d78` | sin script: render manual (no reproducible por descarga) |
| `pdf/validacion/notariado_cv_val_extranjeros_4T2025_p10_zoomB.png` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `(manual) render con pdftoppm del PDF original` | `816fcda774842fc7841604dbb53dc40af947d37585ce55a5a20c34bcff68c1a0` | sin script: render manual (no reproducible por descarga) |
| `pdf/validacion/notariado_cv_val_extranjeros_4T2025_p2.png` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `e44b7a5b6679d8eef2b4fe23a05b8ebedb4cf6237fd153974651bb3b4c33491f` | idéntico |
| `pdf/validacion/notariado_cv_val_extranjeros_4T2025_p3.png` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `3375310a20662dd08cf68c8b1d9d178a4e44c0d6b438046e0cc0b31e5928ff9d` | idéntico |
| `pdf/validacion/notariado_cv_val_municipios_extranjeros_4T2022_p2.png` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `ba75ab674e8ac3ec574562a1a0e9e1d3267be91fb6ae1245c4e3ebe30a91dcbf` | idéntico |
| `pdf/validacion/notariado_cv_val_municipios_extranjeros_4T2025_p2.png` | Consejo General del Notariado | Condiciones de reutilización no verificadas (docs/v5/licencias_datos.md); copia de original o derivado de publicaciones del Notariado | `src/extract_notariado.py` | `c82400900b2695f4c5d4c044358b753c2f8f760aeca82d16643374915423c040` | idéntico |
| `v3/hut_registro_turismo_cat_v3.csv.gz` | Generalitat de Catalunya (Registre de Turisme) | Organismo no incluido en la tabla de licencias; licencia no verificada | `src/v3/fetch_d3_v3.py` | `2ad74deb03bb30fce11ac8106aa2c39009d4e9ec061acedf8a5db87db2dd49a3` | idéntico en contenido (zcat); sha del .gz distinto por marca de tiempo de la cabecera gzip |
| `v8/jk_shocks_ecb_mensual.csv` | Jarociński y Karadi (dataset académico, GitHub) | Fuente no incluida en la tabla de licencias; sin licencia verificada | `src/v8/fetch_v8.py` | `22e38524c34a776b751354c4f47952f8df518ab436c650de4eff4c5649323262` | idéntico |
| `v5/cb_interior_11001.px` | Ministerio del Interior | Condiciones de reutilización del portal no verificadas en detalle | `src/v5/cb_fetch.py` | `1952c90f3521eed83d6003d3c3fdac57ed899413d5c32da9ed787870e2abba8e` | idéntico |
| `v5/cb_interior_11002.px` | Ministerio del Interior | Condiciones de reutilización del portal no verificadas en detalle | `src/v5/cb_fetch.py` | `3913dbd50a1f5e678afface9dd6b976b109cad4a27d2b3375a9b8cebdc2faabc` | idéntico |
| `v5/programas/bng.pdf` | Partido político (BNG) | Programa electoral con derechos del titular; licencias_datos.md exige confirmación del autor | `src/v5/a5_fetch.py` | `b8994deec0bbc45cdcbef5d7c5395cabf30b0509706303c3d8e76058c48eebfd` | idéntico |
| `v5/programas/bildu.pdf` | Partido político (EH Bildu) | Programa electoral con derechos del titular; licencias_datos.md exige confirmación del autor | `src/v5/a5_fetch.py` | `6634c0786c1e771c61c1a65e549dfde0d4581d09e19949466e931c96a9642465` | idéntico |
| `v5/programas/erc.pdf` | Partido político (ERC) | Programa electoral con derechos del titular; licencias_datos.md exige confirmación del autor | `src/v5/a5_fetch.py` | `760db25e48422b74a9b0c3172cab16cf39d010345849e50b921ff8bf61be2854` | idéntico |
| `v5/programas/pnv.pdf` | Partido político (PNV) | Programa electoral con derechos del titular; licencias_datos.md exige confirmación del autor | `src/v5/a5_fetch.py` | `46fec3a017cdc5c4e506fa5e228b97690071d5a03dfd3d8128392aa20f57d132` | idéntico |
| `v5/programas/pp_resumen.pdf` | Partido político (PP) | Programa electoral con derechos del titular; licencias_datos.md exige confirmación del autor | `src/v5/a5_fetch.py` | `134cba662340ad555bfc0cc810e8c10bf0e62373185531c5b67f4ebdf79cdea7` | idéntico |
| `v5/programas/sumar.pdf` | Partido político (Sumar) | Programa electoral con derechos del titular; licencias_datos.md exige confirmación del autor | `src/v5/a5_fetch.py` | `d5ccdac0d20f1b93a5f703f180d086041bd988835072dd5cb5d1378bf0195820` | idéntico |
| `v5/programas/upn.pdf` | Partido político (UPN) | Programa electoral con derechos del titular; licencias_datos.md exige confirmación del autor | `src/v5/a5_fetch.py` | `6bbf12c4fe8acc17d8deb2ddc68a89cbee9e07ec70472ed7463655e8a59e15d6` | idéntico |

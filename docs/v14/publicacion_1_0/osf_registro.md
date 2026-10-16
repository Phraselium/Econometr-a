# Registro en OSF de los pre-registros (texto listo para copiar)

Sustituye al texto de docs/v13/tareas_autor.md, punto 5. Corrige una frase: allí se decía que «ningún resultado del proyecto alcanza la capa causal (C3/C3s)». Es inexacta: cifras_clave tiene cifras en C3s, válidas solo bajo restricciones de signo, y ninguna en C3.

**Pasos** (docs/v14/tareas_autor.md, punto 5):
1. En https://osf.io, cree el proyecto «Vivienda en España: base de evidencia reproducible».
2. Cree un registro de tipo «Open-Ended Registration» con el texto de abajo.
3. Adjunte cada documento tal como está en su commit, con su nombre de etiqueta. En un clon completo de Econometr-a con las etiquetas creadas:
   ```bash
   for p in prereg-v2:docs/v2/hipotesis.md prereg-v3:docs/v3/hipotesis.md prereg-v5:docs/v5/prereg_B3.md prereg-v6:docs/v6/hipotesis.md \
            prereg-v7:docs/v7/hipotesis.md prereg-v8:docs/v8/hipotesis.md prereg-v9:docs/v9/hipotesis.md \
            prereg-v9-a1:docs/v9/hipotesis_addendum_a1.md prereg-v9-a1b:docs/v9/hipotesis_addendum_a1.md; do
     git show "$p" > "${p%%:*}.md"; printf '%s  %s\n' "$(sha256sum < "${p%%:*}.md" | cut -c1-64)" "${p%%:*}.md"; done
   ```
   Los sha256 que imprime deben coincidir con los de la tabla.
4. Anote el DOI y la fecha del registro en docs/v14/tareas_autor.md (`osf_registro`).

---

**Título:** Pre-registros del proyecto «Vivienda en España: base de evidencia reproducible» (v2-V9)

**Autor:** Borja Romero, economista (firma individual, independiente).

**Descripción.** Este registro deja constancia externa de los pre-registros de análisis del proyecto.
- Cada pre-registro se fijó en un commit de git del repositorio de desarrollo (https://github.com/Phraselium/Econometr-a, archivado) antes de estimar los modelos a los que se refiere.
- El registro no añade hipótesis nuevas. Fija, con su huella criptográfica, documentos que ya existen.
- Los resultados se publican en el repositorio https://github.com/Phraselium/vivienda-espana-evidencia (versión pública 1.0) y en el depósito de Zenodo (DOI: {{DOI}}).

**Documentos registrados.**

| Etiqueta | Commit (SHA-1) | Fecha del commit (UTC) | Documento | sha256 del documento en ese commit |
|---|---|---|---|---|
| prereg-v2 | 910c42aef06348b884ea70e7b6cdc510d58e48c1 | 2026-10-10T07:13:42Z | docs/v2/hipotesis.md | 3fa640930bd0f645077808b8553a08e85be98196bd723d93c0fb3f40025040cb |
| prereg-v3 | 204c073e9e2c9e0edd6ac23dad7edf3049ba4428 | 2026-10-10T13:33:09Z | docs/v3/hipotesis.md | ee40f73e5e68482ecff3f4b194cd127dd0e6a35c691ac5a79a7b9a500d8e86b5 |
| prereg-v5 | 8803f049c0f46ae4db8a79221470594295931d86 | 2026-10-10T19:11:04Z | docs/v5/prereg_B3.md | 0b5d09d9f0ca778d47329b291884fdd1672d2ecc8046c6ea4369badc7d8030d1 |
| prereg-v6 | a33c167080fbd4b86a9239dcb3744d070e501429 | 2026-10-11T08:47:34Z | docs/v6/hipotesis.md | 9c5d9333e70fcbb9abc12252ad91a6218db92c84cccea020f64be7b53fb5a82d |
| prereg-v7 | 3fad305fc51bbcec67ec9ae298a31c58b8bd0fd0 | 2026-10-12T12:04:36Z | docs/v7/hipotesis.md | e82d61184dcb3d9ddfdda093bbc7e8f35d10d93c5b6a9b449b6d6b59bbde4c86 |
| prereg-v8 | 91e618be1a2d17879808982a1fe87729d7f5afaf | 2026-10-13T08:00:40Z | docs/v8/hipotesis.md | 9e7d28dcb2c2176358c6350547c1e150bcca53a1d2bac3c43362018cdc1cd0d2 |
| prereg-v9 | 2977349e3ed3092a51c8a3ad309140cf0b83dca8 | 2026-10-15T08:22:29Z | docs/v9/hipotesis.md | 845269079a46a6d84f08397fb02c4591aaf387e4a828f250f964f0e0df9872bb |
| prereg-v9-a1 | 9cb2200e7cb487fcd22d9da1e8b40ba68a3303d7 | 2026-10-15T08:32:35Z | docs/v9/hipotesis_addendum_a1.md | 22d9eadab98fe39ab4274cdaf79d3e9a1330b7fa8267a12dc9ed2b7e7e3c083e |
| prereg-v9-a1b | 4639772d1dbac4e01af0e24bc0a8501117fe1324 | 2026-10-15T08:35:36Z | docs/v9/hipotesis_addendum_a1.md | 58a2cb8fd4aabfba49be91c3b800bb892a6d8932f011bf99fcf8f4babb87c540 |

**Evaluaciones diferidas** (todavía no realizadas):
- V7 y V8 tienen predicciones congeladas que se evaluarán una sola vez con datos posteriores: `make evaluate_v7` y `make evaluate_v8`.
- La huella de las predicciones de V8 (sha256_predicciones_v8) está en docs/v8/notas_release.md.
- La muestra sellada de V6 no se publica. Su huella (sha256 del conjunto de ficheros) está en proyecto.json, `hash_sellado`.

**Declaración sobre la fecha del sello externo.**
- Este registro y el depósito de Zenodo son **posteriores** a los commits que fijan.
- Los commits se hicieron en un repositorio de trabajo antes de ser públicos, y la fecha de un commit la fija quien lo crea.
- La anterioridad de cada pre-registro respecto a sus resultados descansa en tres elementos: el commit (SHA-1), su fecha y el sha256 del documento.
- Este registro es la primera constancia independiente de esos documentos. No prueba por sí mismo que los commits sean anteriores a los resultados; prueba que los documentos existían, con esa huella, en la fecha del registro.

**Capas de evidencia.**
- Ningún resultado del proyecto está en C3 (efecto causal con un instrumento externo o un diseño que supera las pruebas).
- Los resultados en C3s valen solo bajo las restricciones de signo declaradas en el pre-registro de V8.

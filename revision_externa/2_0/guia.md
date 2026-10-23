# Guía para la revisión externa · publicación 2.0

**Proyecto:** *Vivienda en España: base de evidencia reproducible*, versión pública 2.0 (preparada, sin publicar). Autor: Borja Romero, economista (firma individual, independiente). Documento que se revisa: el **documento final** (`publicacion/documento_final/documento_final.md`), con su resumen ejecutivo de dos páginas (`resumen_ejecutivo.pdf`, en esta carpeta).

## Qué se le pide

Dos cosas, por este orden:

1. **Comprobar 40 cifras del documento final frente a sus fuentes.** ¿Es correcta la cifra (sale de la fuente citada con el método de su ficha)? ¿Está bien rotulada (periodo, unidad, capa del proyecto y, en las cifras V18, clase)?
2. **Leer el resumen ejecutivo** y decir, en el comentario general, si la «mejor estimación» de cada factor y su grado de confianza le parecen defendibles con la evidencia citada. Esa columna es juicio experto del autor, rotulado como tal; se le pide su opinión, no que la reproduzca.

No se pide valorar políticas ni a quien las propone.

**La muestra.** Cuarenta cifras citadas en el documento final, elegidas al azar con una semilla fija (SEED = 20261010), estratificadas por capa (C1, C2, C3s, C4) y, en las cifras de V18, por clase (SUGESTIVO, ASOCIACIÓN, NO CONCLUYENTE, NO ESTIMABLE y sin clase propia). Cada estrato tiene hasta cuatro cifras; las plazas que sobran van a los estratos con más cifras. Ninguna ficha aparece dos veces. `make revision_externa_2_0` reproduce la selección exacta; el reparto por estrato está en la columna «estrato» de `muestra.csv`.

**Tiempo estimado:** de 4 a 6 horas para las cifras y una hora para el resumen.

## Qué contiene el paquete

| Fichero | Para qué |
|---|---|
| `resumen_ejecutivo.pdf` | El resumen ejecutivo del documento final, tal como se publica |
| `hoja_revision.xlsx`, pestaña «revision» | Una fila por cifra: id, enunciado tal como se publica, valor, mínimo, máximo, unidad, periodo, capa y estrato, fuentes, URL del organismo, ficha y amplitud del rango; tres columnas para usted |
| `hoja_revision.xlsx`, pestaña «fuentes» | URL de cada organismo |
| `muestra.csv` | La misma muestra en texto plano, con el estrato |

Colores de la hoja: **azul**, dato fijo copiado de la tabla de cifras; **negro**, cálculo; **verde**, valor de otra pestaña. No modifique esas columnas.

## Cómo leer las etiquetas

- **Capa del proyecto.** C1 hecho (dos fuentes independientes coinciden); C2 cota con supuestos explícitos; C3s descomposición con restricciones de signo; C4 exploratorio (asociación, contabilidad, simulación o fuente única). Ningún resultado alcanza C3. Reglas: `metodologia/capas.md`.
- **Clase V18** (solo cifras V18, todas C4): qué permite el diseño de una estimación propia. Ninguna es IDENTIFICADO; la única SUGESTIVO es la de los topes al alquiler en Cataluña, que solo se difunde con su frase de limitación.
- **Confianza** (resumen ejecutivo): escala del Banco de España, «la evidencia indica / sugiere / es compatible con / no permite concluir».

## Cómo comprobar una cifra

1. **Lea la ficha.** La columna «ficha del anexo» da la ficha del anexo metodológico (`metodologia/anexo_metodologico.md`) o, si la cifra no tiene ficha propia, la salida del script que la produce (p. ej. `output/v18/f6/hechos.json`).
2. **Vaya a la fuente.** C1 y C2: descargue el dato del organismo y aplique la fórmula de la ficha. C3s y C4: compruebe que el valor coincide con la salida del script. Las cifras V18 de la literatura (ids `V18-AUX-LIT-*`) se comprueban con el artículo citado en su ficha (`docs/v18/bib/`). Las de la contabilidad con magnitudes de la literatura (`V18-AUX-JE-*`) salen de `output/v18/f5/contabilidad_ilustracion.csv`.
3. **Reproduzca la cifra, si quiere.** En una copia del repositorio: `python3 -m pip install -r requirements.lock`, `make datos` (datos redistribuibles del depósito, con verificación sha256) y `python3 <script>`. Todas las cifras están en `output/v5/cifras_clave.csv` con su id.
4. **Anote el resultado.** «Valor comprobado»; «¿coincide?» (S si coincide con la precisión publicada, N si no); «comentario» (fuente o edición usada y, si no coincide, la diferencia y su posible causa). Una diferencia por revisión posterior del dato oficial se anota como tal; un error de cálculo o de rótulo es una N; si no puede acceder a la fuente, deje la fila en blanco y dígalo.

## Cómo devolver la revisión

- Guarde la hoja como `hoja_revision_<apellido>.xlsx` y añada un comentario general sobre el resumen ejecutivo (una página como máximo). Envíelo al autor por el canal acordado.
- Si encuentra un error, el autor lo anotará en `ERRATA.md` con la fecha, la cifra y la corrección, que se publicará en una versión posterior (2.0.1 o siguiente). Si usted lo autoriza, se le citará por su nombre.

**Neutralidad.** Se evalúan cifras y afirmaciones, nunca a quien las formula. Si alguna redacción le parece valorativa o con lenguaje causal sin respaldo, anótelo.

# V17 · Fase 3 · Encargo común de la auditoría crítica (D1 y D3)

Análisis a posteriori (V17). Lo reciben los tres auditores de la fase 3; se versiona para poder auditarlo.

## Objetivo
Auditar con la máxima dureza cada conclusión de divulgación (docs/v17/plan.md, D1, texto literal) y responder a las preguntas
D3. No se busca confirmar nada: se busca dónde las afirmaciones son falsas, engañosas, incompletas o demasiado prudentes. Si una
afirmación incómoda para cualquiera es cierta, se dice; si una prudente es engañosa, también. Se evalúan afirmaciones e
instrumentos, nunca partidos ni personas.

## Material que hay que usar (leer antes)
- **Plan:** docs/v17/plan.md (D1, D2, D3 y la fase 3, punto 2, con las pruebas mínimas por fila).
- **Lo publicado:** publicacion/informe_integral/informe_integral.md (Partes III y VI) y publicacion/lo_que_sabemos.md. El
  verificador de la 1.0 está en publicacion/verificador/verificador.md.
- **Fase 0:**
  - docs/v17/referencias/: Banco de España (bde_informes.md y bde_bce_documentos.md) e INE (ine_demografia.md).
  - docs/v17/correcciones.md: comprobación D4. Ninguna cifra de prensa entra sin pasarla.
- **Fase 1:** docs/v17/fuentes/*.md y data/raw/v17/. Son terceros: solo agregados propios.
- **Fase 2:**
  - output/v17/lectura_bde/: inferencia convencional y su distorsión (inferencia.csv de cada grupo) y medidas de referencia del
    Banco de España.
  - output/v17/d3/: apoyo cuantitativo a D3.
- **Literatura ya verificada en el proyecto:** docs/v15/literatura.md, docs/v15/literatura/, docs/v16/literatura.md y
  docs/v16/literatura/.
- **Cifras del proyecto:** output/v5/cifras_clave.csv. Toda cifra propia se cita con su id.

## Por cada fila de D1
Una ficha output/v17/auditoria/filas/<id_fila>.md con:
1. **Texto auditado.** La frase literal de D1.
2. **Mejor argumento a favor y mejor argumento en contra, con datos.** Cifra, fuente, id o URL y periodo.
3. **Pruebas mínimas de la fila (plan, fase 3, punto 2).** Las que se puedan calcular con los datos del repositorio, con un script
   en src/v17/f3_<grupo>.py. Determinista; sin red en el script; SEED = 20261010; filtrando muestra_sellada_v6; sin leer
   data/sealed.
4. **Literatura.** Una referencia es VERIFICADA (DOI en Crossref, comprobado con src/v15/verificar_referencias.py o con
   api.crossref.org) o NO VERIFICADA. Se indica si se leyó completa o solo el resumen. Nada no leído al menos en su resumen. Prensa
   solo para localizar originales.
5. **Veredicto.** Uno de: «se sostiene», «se sostiene con matices», «engañosa», «incorrecta» o «no se puede saber».
6. **Texto corregido**, y la **confianza** en la escala del Banco de España: «la evidencia indica / sugiere / es compatible con /
   no permite concluir».
7. **Parada (plan, E).** Si la auditoría muestra que una conclusión de la 1.0 o del informe integral es FALSA, y no solo matizable,
   escríbelo en una sección «PARADA» de la ficha con la prueba. No lo corrijas en ningún fichero publicado: lo decide el autor.

## Por cada pregunta D3 asignada
Una ficha output/v17/auditoria/preguntas/<D3-n>.md con:
- la respuesta argumentada, con datos y literatura;
- la confianza;
- qué no se puede saber;
- una conclusión clara en dos o tres frases.

## Tabla del grupo
output/v17/auditoria/<grupo>.csv con las columnas:
`id_fila, texto_antes, veredicto, texto_despues, confianza, por_que, pruebas, referencias, parada`

## Reglas
- No se cambia ninguna cifra ni capa publicada.
- Las cifras nuevas van a output/v17/auditoria/<grupo>_hechos.json. Cada una lleva id V17-AUD-*, capa C4,
  lectura_v17 («OF», «hecho», «cota», «asociación» o «juicio experto»), fuentes y "nota": "a posteriori".
- Todos los .md empiezan por «Análisis a posteriori (V17).».
- Sin lenguaje causal salvo que se cite un diseño causal creíble de la literatura, atribuido a sus autores.
- Citas literales de 15 palabras como máximo.
- No se escribe fuera de: src/v17/f3_<grupo>.py, output/v17/auditoria/ (sus ficheros) y tests/v17/test_f3_<grupo>.py.

Devolver: rutas, resumen de 200 palabras como máximo con el veredicto de cada fila, las paradas si las hay, y los tokens.

# Guía para la revisión externa

**Proyecto:** *Vivienda en España: base de evidencia reproducible*, versión pública 1.0. Autor: Borja Romero, economista (firma individual, independiente).

## Qué se le pide

Comprobar **40 cifras publicadas** frente a sus fuentes. No se pide valorar conclusiones ni políticas, solo esto:
- **¿Es correcta la cifra?** Que el valor publicado salga de la fuente citada con el método de su ficha.
- **¿Está bien rotulada?** Que el periodo, la unidad y la capa de evidencia que la acompañan sean los correctos.

Las cifras se eligieron al azar con una semilla fija (SEED = 20261010). La muestra está estratificada por capa: 10 de C1, 9 de C2, 10 de C3s y 11 de C4. Ninguna ficha aparece dos veces. `make muestra_revision` reproduce la selección exacta.

**Tiempo estimado:** de 4 a 6 horas.
- Las cifras de C1 y C2 se comprueban con la fuente oficial en unos 5-10 minutos cada una.
- Las de C3s y C4 salen de modelos. Basta comprobar que la cifra coincide con la salida del script indicado (unos 5 minutos cada una). Si quiere, puede reproducir el modelo.

## Qué contiene el paquete

| Fichero | Para qué |
|---|---|
| `hoja_revision.xlsx`, pestaña «revision» | Una fila por cifra. Tiene: id, enunciado tal como se publica, valor, mínimo, máximo, unidad, periodo, capa, fuentes, URL del organismo, ficha del anexo y amplitud del rango. Le siguen tres columnas para usted |
| `hoja_revision.xlsx`, pestaña «fuentes» | URL de cada organismo; la columna «URL de la fuente» la toma de aquí |
| `muestra.csv` | La misma muestra en texto plano |

Colores de la hoja:
- **azul:** dato fijo copiado de la tabla de cifras, con su fuente en la columna «fuente(s)»;
- **negro:** cálculo (la amplitud del rango);
- **verde:** valor que viene de otra pestaña.

## Cómo comprobar una cifra

1. **Lea la ficha.** La columna «ficha del anexo» indica una de dos cosas:
   - la ficha del anexo metodológico (`metodologia/anexo_metodologico.md`, p. ej. «A1»), con definición, fuentes, fórmula paso a paso, supuestos, capa y script;
   - si la cifra no tiene ficha propia, el fichero de salida del script que la produce (p. ej. `output/v8/F6/hechos.json`).
2. **Vaya a la fuente.**
   - **C1 y C2:** descargue el dato del organismo (columna «URL de la fuente» y tabla o serie de la ficha) y aplique la fórmula de la ficha.
   - **C3s y C4:** compruebe que el valor coincide con la salida del script. Las reglas de cada capa están en `metodologia/capas.md`.
3. **Reproduzca la cifra, si quiere hacerlo con el código.** En una copia del repositorio:
   ```bash
   python3 -m pip install -r requirements.lock
   make datos            # datos redistribuibles desde el depósito de Zenodo (verifica sha256)
   make datos_terceros   # con red: Notariado, Registradores y otras fuentes que no se redistribuyen
   ```
   El script de la ficha se ejecuta con `python3 <script>`. Todas las cifras están en `output/v5/cifras_clave.csv`, con su id.
4. **Anote el resultado** en la pestaña «revision»:
   - «valor comprobado»: su valor;
   - «¿coincide?»: S si coincide dentro de la precisión con que se publica; N si no;
   - «comentario»: qué fuente o edición usó y, si no coincide, la diferencia y su posible causa.

Los criterios son estos:
- Una diferencia por **revisión posterior del dato oficial** se anota como tal: el periodo y la fecha del dato están en la fila.
- Un **error de cálculo o de rotulado** es una N.
- Si **no puede acceder a la fuente**, deje la fila en blanco y dígalo en el comentario.

## Cómo devolver la hoja

- Guarde la hoja con su nombre en el nombre del fichero (`hoja_revision_<apellido>.xlsx`) y envíela al autor por el canal acordado.
- No modifique las columnas en azul, verde o negro: así se pueden comparar las respuestas de varios revisores.
- Si encuentra un error:
  - el autor lo anotará en `ERRATA.md` con la fecha, la cifra y la corrección;
  - la corrección se publicará en una versión posterior (1.0.1 o siguiente);
  - si usted lo autoriza, se le citará por su nombre.

**Neutralidad.** Se evalúan cifras y afirmaciones, nunca a quien las formula. Si alguna redacción le parece valorativa o con lenguaje causal sin respaldo (capas C1, C2 o C4), anótelo en el comentario.

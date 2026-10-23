<!-- Generado por `make publicacion` desde docs/v7_1/evaluacion_2027.md. No editar a mano: se regenera y un test lo comprueba. -->

# Protocolo de la evaluación diferida de V7 (`make evaluate_v7`, 2027)

Este documento fija, antes de abrir nada, cómo se ejecutará y publicará la única validación limpia de V7. Es la hipótesis de predicción H7-P1: el mejor modelo regional congelado bate a la base fuerte en el agregado de las 17 CCAA. El ensayo con datos simulados está en [output/v7_1/S4/ensayo.md](ensayo_evaluate_v7.md) y fue superado.

## 1. Qué se evalúa y con qué

- **Modelos.** Los congelados en output/v7/R5/modelos_congelados.json, con sha256 `93795a9480eccf03f382bc20253561dd37e240287921453fd0d1add40a9a0646` (anotado en docs/v7/notas_release.md). Las predicciones están en output/v7/R5/predicciones_congeladas.csv.
- **Muestra limpia.** Trimestres de 2026T3 a 2027T2 del IPV (compra) y del IPC de alquiler por CCAA, publicados después de la fecha verificable del pre-registro (release o DOI de `prereg-v7`).
- **Métricas.** RMSE a 1-4 trimestres frente a la base fuerte (AR con factor común) y al AR(4); DM-HLN y permutación por CCAA; Holm por mercado, horizonte y comparador.

## 2. Fechas de publicación previstas (calendario oficial del INE)

Fuente: calendario de disponibilidad de estadísticas del INE (https://www.ine.es/dynt3/Calendario/calenHTML.htm), consultado el 12-10-2026. El calendario de 2027 aún no está publicado: las fechas de 2027 son **estimadas** con el patrón de 2026 y hay que confirmarlas cuando el INE lo publique (normalmente en el último trimestre del año anterior).

| Serie (uso) | Periodo | Fecha | Estado |
|---|---|---|---|
| IPV por CCAA (compra) | 2026T3 | 4 de diciembre de 2026 | oficial |
| IPV | 2026T4 | primera semana de marzo de 2027 | estimada (2026: 6 de marzo) |
| IPV | 2027T1 | primera quincena de junio de 2027 | estimada (2026: 8 de junio) |
| IPV | 2027T2 | primera quincena de septiembre de 2027 | estimada (2026: 7 de septiembre) |
| IPC, alquiler de vivienda por CCAA (alquiler) | septiembre de 2026 (cierra 2026T3) | 14 de octubre de 2026 | oficial |
| IPC | diciembre de 2026 (cierra 2026T4) | mediados de enero de 2027 | estimada (2026: 15 de enero) |
| IPC | marzo de 2027 (cierra 2027T1) | mediados de abril de 2027 | estimada (2026: 14 de abril) |
| IPC | junio de 2027 (cierra 2027T2) | mediados de julio de 2027 | estimada (2026: 15 de julio) |
| EPA (regresores) | 2026T3 / 2026T4 / 2027T1 / 2027T2 | 27 de octubre de 2026 / finales de enero, abril y julio de 2027 | oficial / estimadas |
| Hipotecas mensual | septiembre de 2026 / … / junio de 2027 | 25 de noviembre de 2026 / … / finales de agosto de 2027 | oficial / estimadas |
| Transmisiones (ETDP) | septiembre de 2026 / … / junio de 2027 | 17 de noviembre de 2026 / … / agosto de 2027 | oficial / estimadas |

**Fecha más temprana para evaluar:** después de la publicación del IPV de 2027T2, prevista hacia la primera quincena de septiembre de 2027. Se recomienda ejecutar en la segunda quincena de septiembre de 2027.

### Aviso sobre 2026T3 del alquiler (declarado antes de abrir)

Julio y agosto de 2026 del IPC de alquiler ya estaban publicados, y en data/raw, antes de la fecha del pre-registro. Ningún modelo los usó: R5 se estimó hasta 2026T2. Pero el trimestre 2026T3 del alquiler no es íntegramente posterior al pre-registro. Por eso:
- **la evaluación principal** es la pre-registrada (2026T3-2027T2);
- **se publica además, como sensibilidad declarada ahora,** la del alquiler con 2026T4-2027T2.

Si discrepan, se reportan las dos. Esta nota se añade a docs/v7/desviaciones.md como desviación declarada antes de la apertura.

## Integridad de la muestra sellada

- **Huella de data/sealed:** `PENDIENTE` (fecha: 2026-10-16; fuente: proyecto.json, campo `hash_sellado`).
- **Comando con el que se calcula** (desde la raíz del repositorio de desarrollo):
  ```bash
  find data/sealed -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum
  ```
- **Antes de evaluar**, recalcule la huella y compruebe que coincide con la de proyecto.json. Si no coincide, no evalúe: anótelo en ERRATA.md.
- La integridad anterior al 16/10/2026 se apoya en el registro de accesos de src/holdout.py, no en checksums (ver ERRATA y la decisión D3 de V13).

## 3. Orden exacto de las órdenes

Desde una copia limpia del repositorio en la versión pública 2.0 (contenido de V7: versión interna v7.1), con red y con permisos para publicar:

```bash
git checkout r7.1/main             # o la etiqueta v7.1 publicada
git log -1 --format=%H             # anotar el commit en el informe del resultado
sha256sum output/v7/R5/modelos_congelados.json   # debe ser 93795a94…0a9a0646
grep fecha_verificable docs/v7/notas_release.md  # debe tener la fecha del DOI, no PENDIENTE
python3 src/v7_1/s4_ensayo.py      # ensayo sin red: debe decir SUPERADO
make evaluate_v7                   # UNA sola vez: descarga a data/raw/v7_eval/<fecha>/, registra la apertura y evalúa
cat docs/v7/evaluate_v7_accesos.md # APERTURA y EVALUACIÓN registradas
git add docs/v7/evaluate_v7_accesos.md output/v7/evaluate/ data/raw/v7_eval/
git commit -m "Evaluación diferida de V7 (H7-P1): resultado"
```

`make evaluate_v7` sale sin registrar nada en tres casos, y entonces se puede repetir más tarde:
- no hay periodos posteriores a 2026T2;
- el sha256 no coincide;
- falta la congelación.

Si ya hay una apertura registrada, se niega a evaluar otra vez.

## 4. Qué hacer si cambia un formato o una base

1. **Antes de abrir.** Ejecutar el ensayo (`python3 src/v7_1/s4_ensayo.py`) y, si la descarga real lo permite, solo la descarga a un directorio aparte (variable de entorno `RAW_DIR`, que respetan los scripts fetch_*). Comprobar que `R5.nuevos_periodos()` detecta los trimestres sin evaluar. Esto no registra apertura.
2. **Cambio de formato** (columnas, nombres de territorio, códigos). Se adapta solo el lector (`observados()` en src/v7/r5_prediccion.py) en un commit aparte y anterior a la apertura, con un test que lea el fichero nuevo. Nunca se tocan los modelos ni las predicciones congeladas: su sha256 lo impediría.
3. **Cambio de base** del índice (p. ej. el IPV o el IPC con otro año base). Los modelos predicen logaritmos de niveles. Se enlaza la serie nueva con la antigua por el cociente en el trimestre de solape más reciente, como en v1. El enlace se documenta en docs/v7/desviaciones.md antes de abrir. Si no hay solape, se evalúan las tasas de variación y se declara.
4. **Revisión de datos ya publicados** (por ejemplo, 2026T2). Se usan los datos tal como estén publicados el día de la apertura, y se anota la revisión.
5. **Serie suprimida o retrasada.** Si falta un trimestre, se evalúa con los disponibles (mínimo, 2026T3-2027T1) y se declara. Si falta un mercado entero, se evalúa el otro y se declara.

## 5. Cómo publicar el resultado, sea cual sea

- **Se publica siempre, y una sola vez.** Esto incluye un resultado desfavorable («el mejor modelo regional no bate a la base fuerte») y un resultado nulo.
- **Contenido mínimo:**
  - commit evaluado;
  - sha256 de la congelación;
  - fecha de apertura;
  - periodos y CCAA con dato;
  - tabla de RMSE por mercado, modelo y horizonte;
  - DM-HLN, permutación y p de Holm frente a la base fuerte y al AR(4);
  - la sensibilidad del alquiler sin 2026T3;
  - las desviaciones declaradas.
- **Lectura.** Solo «predice mejor» si supera a la base más exigente (regla K1). La predicción no identifica causas: el resultado no cambia la capa C4 de ningún coeficiente de V7.
- **Dónde.**
  - output/v7/evaluate/resultado.json;
  - una entrada en CHANGELOG.md (versión v7.2);
  - una actualización de que_cambio.md mediante una plantilla nueva;
  - una release en GitHub y Zenodo con el DOI de la evaluación.
  
  Si el resultado contradice lo que dicen los entregables sobre la predicción regional, se corrige el texto y se anota en ERRATA.md.

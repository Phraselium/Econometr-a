# Decisiones v3

Formato: fecha · decisión · motivo. Las desviaciones del pre-registro (`prereg-v3`) se anotan aquí con motivo.

## Setup (2026-10-10)
- Rama r3/main desde r2/main (841c695). CLAUDE.md adaptado a v3 (19 líneas); los agentes apuntan a src/v3, output/v3, docs/v3. El reviewer v3 no reproduce el pipeline (lo hace el orquestador con `make check` y `make all` ×2). Revisa solo identificación, capas, neutralidad y conclusiones.
- `make check` no existía en v2: se crea (ruff + pytest + `src/v3/check_texto.py`). `check_texto.py` busca tres cosas:
  1. léxico valorativo o partidista y alusiones a partidos o personas en los textos v3;
  2. promoción de capa (lenguaje causal en fichas o párrafos C1, C2 o C4);
  3. fichas del verificador incompletas.
- Ventanas: se reutiliza el sellado v2 (2024Q3-2026Q2 y provincias 11, 16, 45) para lo provincial ya analizado. El sellado v3 propio es por sección censal: 20 % de los bloques espaciales de distritos más la última oleada. Se aplica solo a P-C.
- Bloques espaciales sin cartografía:
  - En municipios con ≥2 distritos, cada bloque es un par de distritos con numeración consecutiva. En las ciudades españolas la numeración de distritos suele ser contigua; esto es un supuesto, documentado.
  - En municipios de un solo distrito, el bloque es el municipio.
  - Si se obtiene la cartografía de secciones (INE), se sustituye por bloques de contigüidad antes del pre-registro.
- Magnitudes en €/mes, % y viviendas. Holm en confirmatorias v3; BH en exploratorias.
- Para P-A (C1) y P-B (C2) se usan los paneles COMPLETOS. Se leen con `holdout.load_full(nombre, uso)`, que solo funciona si ya existen las 4 evaluaciones selladas de v2 (H1, H2, H6 y H7) y registra cada lectura con el evento «v3_completo». El sellado v2 ya no protege ninguna hipótesis pendiente.
- La especificación de P-A y P-B (docs/v3/especificacion_PA_PB.md) se fija ANTES de calcular. También fija el efecto económicamente relevante de cada diseño P-C, que decide el go/no-go por potencia.
- Las solicitudes de transparencia están redactadas pero no presentadas: exigen la identificación electrónica de una persona física. La cota de grandes tenedores queda en espera, con la ingesta preparada.

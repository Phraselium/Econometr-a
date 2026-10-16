"""V14.2-B3 · Política de la versión 1.0 para las series de terceros: campo `terceros_1_0` de proyecto.json.

Un valor por fuente (registradores, notariado, aeat):
- «agregados»: las cifras propias se publican citando la fuente; la serie descargada no se redistribuye (ni en el árbol público
  ni en el paquete: columnas redactadas y tablas que son la serie vaciadas, src/v14/terceros.py).
- «excluir»: además, las cifras que usan de verdad la serie (dependencia «directa» o «indirecta (el modelo usa la serie)» en
  docs/v14/cifras_terceros.csv; nunca las «técnicas» ni las que solo usan una estadística oficial del INE o del MIVAU) se
  retiran de publicacion/, web/ y consulta/ y se marcan como no publicadas en la 1.0. No se borran de cifras_clave: el
  registro (output/v5/cifras_clave.csv y su copia exacta publicacion/cifras_clave.csv) no cambia en ningún escenario.
- «redistribuir»: la serie va al paquete del depósito y las tablas de output/ se publican sin redactar.
Lo leen src/v5/render.py (marcadores), src/consulta/generar.py, src/v10/web.py, src/v7_1/publicacion.py, src/v14/terceros.py
(árbol público y paquete) y src/v13/paquete_zenodo.py. Para probar escenarios sin tocar proyecto.json, la variable de entorno
VIVIENDA_TERCEROS_1_0 (JSON, p. ej. '{"aeat": "redistribuir"}') sustituye los valores que nombra. Determinista y sin red.
"""
from __future__ import annotations

import csv
import json
import os
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
FUENTES = ("registradores", "notariado", "aeat")
VALORES = ("agregados", "excluir", "redistribuir")
POR_DEFECTO = {"registradores": "agregados", "notariado": "agregados", "aeat": "excluir"}
NOMBRE = {"registradores": "Registradores", "notariado": "Notariado", "aeat": "AEAT"}   # como en docs/v14/cifras_terceros.csv
RETIRAN = ("directa", "indirecta (el modelo usa la serie)")
ENV = "VIVIENDA_TERCEROS_1_0"
NO_PUBLICADAS = "publicacion/cifras_no_publicadas_1_0.csv"


def politica() -> dict[str, str]:
    p = json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8")).get("terceros_1_0")
    if not isinstance(p, dict):
        raise SystemExit("proyecto.json: falta el campo terceros_1_0 (V14.2)")
    p = {k: v for k, v in p.items() if not k.startswith("_")}
    if os.environ.get(ENV):
        p.update(json.loads(os.environ[ENV]))
    if set(p) != set(FUENTES) or any(v not in VALORES for v in p.values()):
        raise SystemExit(f"terceros_1_0: hacen falta {FUENTES} con un valor de {VALORES}; hay {p}")
    return p


def redistribuye(fuente: str, pol: dict | None = None) -> bool:
    """CGPJ y las demás fuentes no redistribuibles no tienen escenario: nunca se redistribuyen."""
    return (pol or politica()).get(fuente) == "redistribuir"


@lru_cache(maxsize=None)
def _retiradas(clave: tuple) -> dict[str, tuple[str, ...]]:
    excl = {NOMBRE[f] for f, v in clave if v == "excluir"}
    out: dict[str, set] = {}
    if not excl:
        return {}
    with (RAIZ / "docs" / "v14" / "cifras_terceros.csv").open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["fuente"] in excl and r["dependencia"] in RETIRAN:
                out.setdefault(r["id"], set()).add(r["fuente"])
    return {i: tuple(sorted(f)) for i, f in sorted(out.items())}


def retiradas(pol: dict | None = None) -> dict[str, tuple[str, ...]]:
    """{id: fuentes} de las cifras que no se publican en la 1.0 con esta política."""
    return _retiradas(tuple(sorted((pol or politica()).items())))


def marca(fuentes) -> str:
    return f"[cifra no publicada en la versión 1.0: usa la serie de {' y '.join(fuentes)}]"


def filas_no_publicadas(pol: dict | None = None) -> list[dict]:
    pol = pol or politica()
    dep = {}
    with (RAIZ / "docs" / "v14" / "cifras_terceros.csv").open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            dep.setdefault(r["id"], []).append(f"{r['fuente']}: {r['dependencia']}")
    return [{"id": i, "fuentes": " y ".join(f), "dependencia": "; ".join(dep.get(i, [])),
             "estado_1_0": "no publicada (terceros_1_0 = excluir)", "en_cifras_clave": "sí, sin cambios"}
            for i, f in retiradas(pol).items()]


# ---------------------------------------------------------------- capa pública de la base: variables de la AEAT
VARIABLES_FUENTE = {"aeat": r"^aeat_"}   # variables de data/base/publica/hechos.parquet que son la serie de una fuente


def variables_excluidas(pol: dict | None = None) -> str | None:
    """Patrón de las variables de hechos.parquet que no se redistribuyen con esta política (None si ninguna)."""
    pol = pol or politica()
    pats = [p for f, p in VARIABLES_FUENTE.items() if not redistribuye(f, pol)]
    return "|".join(pats) or None


def filtrar_hechos(origen: Path, destino: Path, pol: dict | None = None) -> int:
    """Copia hechos.parquet sin las variables de `variables_excluidas`, por lotes (sin cargar la tabla entera). Devuelve cuántas quita."""
    import re
    import shutil

    import pyarrow.compute as pc
    import pyarrow.dataset as ds
    import pyarrow.parquet as pq

    pat = variables_excluidas(pol)
    variables = [] if pat is None else [v for v in pq.read_table(origen, columns=["variable"]).column("variable").unique().to_pylist()
                                        if re.match(pat, str(v))]
    if not variables:
        shutil.copyfile(origen, destino)
        return 0
    escritor = None
    for lote in ds.dataset(origen, format="parquet").to_batches(filter=~pc.field("variable").isin(variables), batch_size=500_000):
        if escritor is None:
            escritor = pq.ParquetWriter(destino, lote.schema, compression="zstd")
        escritor.write_batch(lote)
    if escritor is not None:
        escritor.close()
    return len(variables)


# ---------------------------------------------------------------- «redistribuir»: series brutas que van al paquete
SERIES_BRUTAS = {
    "notariado": ("data/raw/pdf/notariado_*.csv",),
    "registradores": ("data/raw/pdf/registradores_*.csv",),
    "aeat": ("data/raw/v11/aeat_irpf_municipios/irpf_municipios_cv.csv.gz", "data/raw/v5/cb_aeat_*.html"),
}


def series_brutas(pol: dict | None = None) -> list[str]:
    """Ficheros de data/raw con la serie de las fuentes con «redistribuir» (los que hay en disco: versionados o de `make datos_terceros`)."""
    pol = pol or politica()
    out = []
    for f, pats in SERIES_BRUTAS.items():
        if redistribuye(f, pol):
            for pat in pats:
                out += [p.relative_to(RAIZ).as_posix() for p in sorted(RAIZ.glob(pat)) if p.is_file()]
    return sorted(set(out))

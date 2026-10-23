"""V14.2-B3 · Política de la versión 1.0 para las series de terceros: campo `terceros_1_0` de proyecto.json.

Un valor por fuente (registradores_odbl, registradores_eri, notariado, aeat). V14.3: Registradores se divide por producto
(docs/v14/registradores_origen.csv): datos abiertos bajo ODbL 1.0 y Anuario ERI (derechos reservados). Las cifras con origen
«ambos» dependen de los dos valores; las ODbL que se publican llevan el aviso de atribución de la ODbL (`AVISO_ODBL`).
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
FUENTES = ("registradores_odbl", "registradores_eri", "notariado", "aeat")
VALORES = ("agregados", "excluir", "redistribuir")
POR_DEFECTO = {"registradores_odbl": "agregados", "registradores_eri": "agregados", "notariado": "agregados", "aeat": "agregados"}   # V14.4
NOMBRE = {"registradores_odbl": "Registradores (datos abiertos)", "registradores_eri": "Registradores (Anuario ERI)",
          "notariado": "Notariado", "aeat": "AEAT"}
CT_FUENTE = {"registradores_odbl": "Registradores", "registradores_eri": "Registradores", "notariado": "Notariado", "aeat": "AEAT"}
ORIGEN_REG = {"ODbL": ("registradores_odbl",), "ERI": ("registradores_eri",), "ambos": ("registradores_odbl", "registradores_eri")}
AVISO_ODBL = ("Contiene información de «Compraventas de inmuebles, uso residencial, por provincia» (Colegio de Registradores, "
              "https://opendata.registradores.org/dataset/dataset/compraventas-de-inmuebles-uso-residencial-por-provincia), disponible bajo la "
              "Open Database License (ODbL) 1.0, https://opendatacommons.org/licenses/odbl/1-0/.")
# K16 (2026-10-23): la AEAT autoriza la reutilización y redistribución citando la fuente y la fecha (docs/v18/decisiones.md)
AVISO_AEAT = ("Fuente: Agencia Estatal de Administración Tributaria (AEAT), Estadística de los declarantes del IRPF por municipios, "
              "ejercicios 2013-2024, consultado el 15 de octubre de 2026; y Estadística de los declarantes del IRPF (bienes inmobiliarios, "
              "ejercicios 2019-2024; vivienda, ejercicio 2024), consultado el 13 de octubre de 2026. Reutilización autorizada citando la "
              "fuente (https://sede.agenciatributaria.gob.es/Sede/condiciones-uso-sede-electronica/aviso-legal/"
              "utilizacion-informacion-contenida-web-aeat.html); la AEAT no participa ni patrocina este trabajo.")
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
def origen_registradores() -> dict[str, str]:
    """{id: ODbL | ERI | ambos} de las cifras que dependen de Registradores (docs/v14/registradores_origen.csv)."""
    with (RAIZ / "docs" / "v14" / "registradores_origen.csv").open(encoding="utf-8", newline="") as fh:
        return {r["id_o_fichero"]: r["origen"] for r in csv.DictReader(fh) if r["tipo"] == "cifra"}


@lru_cache(maxsize=None)
def _dependencias() -> dict[str, list[tuple[str, str]]]:
    """{id: [(fuente de terceros_1_0, dependencia)]}, con Registradores dividido por producto."""
    inv = {"Notariado": ("notariado",), "AEAT": ("aeat",)}
    out: dict[str, list] = {}
    with (RAIZ / "docs" / "v14" / "cifras_terceros.csv").open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            fs = ORIGEN_REG.get(origen_registradores().get(r["id"], "ambos"), ()) if r["fuente"] == "Registradores" else inv.get(r["fuente"], ())
            out.setdefault(r["id"], []).extend((f, r["dependencia"]) for f in fs)
    return out


@lru_cache(maxsize=None)
def _retiradas(clave: tuple) -> dict[str, tuple[str, ...]]:
    excl = {f for f, v in clave if v == "excluir"}
    out = {i: tuple(sorted({NOMBRE[f] for f, d in deps if f in excl and d in RETIRAN})) for i, deps in _dependencias().items()}
    return {i: f for i, f in sorted(out.items()) if f}


def nota_odbl() -> str:
    """Aviso de atribución (ODbL 4.3) para los textos que citan cifras construidas con los datos abiertos de Registradores."""
    return f"*Atribución (Open Database License).* {AVISO_ODBL} Las cifras construidas con esos datos se publican bajo la misma licencia."


def nota_aeat() -> str:
    """Atribución de la AEAT (K16) para la web, el depósito y los metadatos."""
    return f"*Atribución (AEAT).* {AVISO_AEAT}"


def odbl(pol: dict | None = None) -> set[str]:
    """Cifras publicadas (no retiradas) que usan la serie de los datos abiertos de Registradores: llevan el aviso de la ODbL."""
    ret = retiradas(pol)
    return {i for i, deps in _dependencias().items() if i not in ret and any(f == "registradores_odbl" and d in RETIRAN for f, d in deps)}


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
    orig = origen_registradores()
    return [{"id": i, "fuentes": " y ".join(f), "dependencia": "; ".join(d + (f" ({orig[i]})" if d.startswith("Registradores") and i in orig else "")
                                                                    for d in dep.get(i, [])),
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
    "registradores_odbl": ("data/raw/pdf/registradores_opendata_*.csv",),
    "registradores_eri": ("data/raw/pdf/registradores_eri_anuario.csv",),
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

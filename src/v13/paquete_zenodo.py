"""V13-B2 · `make paquete_zenodo`: genera el paquete del depósito en _deposito/ (ignorado por git). No borra ni reescribe nada
del repositorio ni de su historia.

Contenido (solo ficheros versionados, salvo la capa pública de la base, que se filtra):
- código y documentación: todo lo versionado fuera de data/ y output/ (src, tests, Makefile, docs, publicacion, metodologia,
  reproducir, consulta, figuras, web, paper, historico, metadatos);
- output/: salidas versionadas (las evaluaciones selladas ya hechas se leen de ahí; `make all` no reabre el sellado), salvo las
  tablas cuya cabecera contiene series de Notariado, Registradores o AEAT;
- data/: la clase (a) de docs/v13/datos_inventario.csv (redistribuible y versionado), con data/base/publica y data/base/geo;
  data/base/publica/hechos.parquet sin las variables de EXCLUIR_PUBLICA (licencia pendiente del autor; docs/v13/decisiones.md).
Excluido: clase (b) (no redistribuible: `make datos_terceros` o descarga manual), clase (c) (regenerable: `make datos_v9`,
`make datos_v11`, `src/v10/fetch_geo.py`, `make data`) y data/sealed (no se lee: solo vía src/holdout.py).
Escribe CHECKSUMS.sha256 y LEEME_DEPOSITO.md en la raíz del paquete. Uso: python3 src/v13/paquete_zenodo.py [--destino DIR] [--zip]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
P = json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8"))
NOMBRE = f"vivienda-espana-evidencia-{P['version_publica']}"
INVENTARIO = RAIZ / "docs" / "v13" / "datos_inventario.csv"
NO_REDIS_COL = re.compile(r"notar|registrad|cgn_|cgpj|aeat", re.I)
# variables de la capa pública con licencia en discrepancia (AEAT: manifiesto V11 «sí» frente a v5/V8.1 «no verificada»).
# Si el autor confirma la licencia, se vacía esta lista (docs/v13/decisiones.md, D4).
EXCLUIR_PUBLICA = re.compile(r"^aeat_")


def _git_ls() -> list[str]:
    r = subprocess.run(["git", "ls-files", "-z"], cwd=RAIZ, capture_output=True, text=True, check=True)
    return sorted(f for f in r.stdout.split("\0") if f and (RAIZ / f).is_file())


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _cabecera_no_redis(p: Path) -> bool:
    if p.suffix != ".csv":
        return False
    with p.open(encoding="utf-8", errors="ignore") as fh:
        return bool(NO_REDIS_COL.search(fh.readline()))


def seleccionar() -> tuple[list[str], list[tuple[str, str]]]:
    """Devuelve (incluidos, excluidos con motivo) entre los ficheros versionados."""
    clase = {}
    with INVENTARIO.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            clase[r["fichero"]] = (r["clase"], r["motivo"])
    inc, exc = [], []
    for f in _git_ls():
        if f.startswith(("data/sealed", ".claude/")):   # muestra sellada (no se lee) y configuración de los agentes de trabajo
            continue
        if f.startswith("data/"):
            c, m = clase.get(f, ("?", "sin clasificar en docs/v13/datos_inventario.csv"))
            (inc.append(f) if c == "a" else exc.append((f, f"clase ({c}): {m}")))
        elif f.startswith("output/") and _cabecera_no_redis(RAIZ / f):
            exc.append((f, "tabla con series de Notariado, Registradores o AEAT (licencia no verificada)"))
        else:
            inc.append(f)
    return inc, exc


def _filtrar_hechos(origen: Path, destino: Path) -> int:
    """Copia hechos.parquet sin las variables de EXCLUIR_PUBLICA, por lotes (sin cargar la tabla entera)."""
    import pyarrow.compute as pc
    import pyarrow.dataset as ds
    import pyarrow.parquet as pq

    dset = ds.dataset(origen, format="parquet")
    variables = [v for v in pq.read_table(origen, columns=["variable"]).column("variable").unique().to_pylist() if EXCLUIR_PUBLICA.match(str(v))]
    if not variables:
        shutil.copyfile(origen, destino)
        return 0
    filtro = ~pc.field("variable").isin(variables)
    escritor, n = None, 0
    for lote in dset.to_batches(filter=filtro, batch_size=500_000):
        if escritor is None:
            escritor = pq.ParquetWriter(destino, lote.schema, compression="zstd")
        escritor.write_batch(lote)
        n += lote.num_rows
    if escritor is not None:
        escritor.close()
    return len(variables)


def leeme(n_inc: int, excluidos: list[tuple[str, str]], quitadas: int) -> str:
    grupos: dict[str, int] = {}
    for _, m in excluidos:
        k = m.split(":")[0] if m.startswith("clase") else m
        grupos[k] = grupos.get(k, 0) + 1
    filas = "\n".join(f"| {k} | {v} |" for k, v in sorted(grupos.items()))
    return f"""# {P['titulo']} · versión {P['version_publica']} ({P['fecha_version']})

Depósito en Zenodo. Autor: {P['autor']}. Repositorio: {P['repositorio']}. DOI: {P['doi']}.

## Qué contiene
- Código (src/, tests/, Makefile, requirements.lock), documentación (docs/, metodologia/, reproducir/, historico/) y entregables (publicacion/, consulta/, figuras/, web/, paper/).
- Salidas versionadas (output/), incluidas las evaluaciones selladas ya hechas (`make all` no reabre la muestra sellada).
- Datos redistribuibles: data/raw de clase (a), la capa pública de la base (data/base/publica) y las geometrías (data/base/geo); clasificación en docs/v13/datos_inventario.csv y docs/v13/datos_deposito.md.
- {n_inc} ficheros, con su sha256 en CHECKSUMS.sha256 (`sha256sum -c CHECKSUMS.sha256`).

## Qué no contiene y cómo obtenerlo
| Motivo de la exclusión | Ficheros |
|---|---|
{filas}

- **No redistribuibles (clase b):** `make datos_terceros` descarga y verifica los de Notariado, Registradores, CGPJ, Interior, Incasòl, Registre de Turisme, Comunidad de Madrid y Jarociński-Karadi (sha256 en data/CHECKSUMS.sha256). Las descargas manuales del autor (Barcelona HUT, BDO de la GVA) se describen en docs/v11/descargas_manuales.md. Las tablas de output/ con series de esas fuentes y los paneles de data/processed se regeneran con `make all` después de `make datos_terceros`.
- **Regenerables (clase c):** originales y microdatos grandes; `make datos_v9`, `make datos_v11`, `python3 src/v10/fetch_geo.py` y `make data` (con red) los descargan y verifican contra sus manifiestos.
- **Muestra sellada (data/sealed):** no se incluye ni se lee; `make clean` la reconstruye (`src/holdout.py build`).
- **Capa pública:** se han quitado {quitadas} variables de AEAT de data/base/publica/hechos.parquet porque su licencia está pendiente de confirmar por el autor (docs/v13/decisiones.md, D4).

## Licencias
Código: MIT. Textos, tablas y figuras propios: CC BY 4.0 (LICENSE). Datos de terceros: la licencia de su fuente (docs/v5/licencias_datos.md, docs/v13/datos_deposito.md).

## Cómo reproducir
```bash
python3 -m pip install -r requirements.lock
make datos_terceros   # con red, una vez: datos de terceros no redistribuibles
make all              # sin red
make check
```
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--destino", default=str(RAIZ / "_deposito"))
    ap.add_argument("--zip", action="store_true")
    a = ap.parse_args()
    if not INVENTARIO.exists():
        raise SystemExit("falta docs/v13/datos_inventario.csv: ejecutar `python3 src/v13/inventario_datos.py`")
    base = Path(a.destino) / NOMBRE
    if base.exists():
        shutil.rmtree(base)
    inc, exc = seleccionar()
    quitadas = 0
    for f in inc:
        d = base / f
        d.parent.mkdir(parents=True, exist_ok=True)
        if f == "data/base/publica/hechos.parquet":
            quitadas = _filtrar_hechos(RAIZ / f, d)
        else:
            shutil.copyfile(RAIZ / f, d)
    (base / "LEEME_DEPOSITO.md").write_text(leeme(len(inc), exc, quitadas), encoding="utf-8")
    with (base / "EXCLUIDOS.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["fichero", "motivo"])
        w.writerows(exc)
    todos = sorted(p for p in base.rglob("*") if p.is_file() and p.name != "CHECKSUMS.sha256")
    (base / "CHECKSUMS.sha256").write_text("".join(f"{_sha(p)}  {p.relative_to(base).as_posix()}\n" for p in todos), encoding="utf-8")
    tam = sum(p.stat().st_size for p in base.rglob("*") if p.is_file())
    print(f"paquete_zenodo: {base} · {len(inc)} ficheros incluidos, {len(exc)} versionados excluidos, {quitadas} variables AEAT quitadas, {tam / 1e6:.0f} MB")
    if a.zip:
        z = base.with_suffix(".zip")
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in sorted(base.rglob("*")):
                if p.is_file():
                    zf.write(p, p.relative_to(base.parent).as_posix())
        print(f"paquete_zenodo: {z} ({z.stat().st_size / 1e6:.0f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""V13-B2 · `make paquete_zenodo`: genera el paquete del depósito en _deposito/ (ignorado por git). No borra ni reescribe nada
del repositorio ni de su historia.

Contenido (solo ficheros versionados, salvo la capa pública de la base, que se filtra):
- código y documentación: todo lo versionado fuera de data/ y output/ (src, tests, Makefile, docs, publicacion, metodologia,
  reproducir, consulta, figuras, web, paper, historico, metadatos);
- output/: salidas versionadas (las evaluaciones selladas ya hechas se leen de ahí; `make all` no reabre el sellado); las
  tablas con columnas de Notariado, Registradores o AEAT van redactadas, sin esas columnas, y las que son la serie van vacías
  (V14-V14.2; src/v14/terceros.py, según proyecto.json → terceros_1_0);
- data/: la clase (a) de docs/v13/datos_inventario.csv (redistribuible y versionado), con data/base/publica y data/base/geo;
  data/base/publica/hechos.parquet sin las variables de fuentes que no se redistribuyen (V14.2: las de la AEAT salvo
  terceros_1_0.aeat = «redistribuir»; src/v14/terceros_1_0.py);
- V14.2: con «redistribuir», las series brutas de esa fuente (terceros_1_0.SERIES_BRUTAS, también las que solo están en disco
  tras `make datos_terceros`).
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
sys.path.insert(0, str(RAIZ))
from src.v14 import terceros as T  # noqa: E402
from src.v14 import terceros_1_0 as T10  # noqa: E402

P = json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8"))
NOMBRE = f"vivienda-espana-evidencia-{P['version_publica']}"
INVENTARIO = RAIZ / "docs" / "v13" / "datos_inventario.csv"
NO_REDIS_COL = re.compile(r"notar|registrad|cgn_|cgpj|aeat", re.I)


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
    pol = T10.politica()
    brutas = T10.series_brutas(pol)   # V14.2: series de las fuentes con «redistribuir»
    for f in _git_ls():
        if f.startswith(("data/sealed", ".claude/", "docs/v14/licencias/")):   # muestra sellada (no se lee), agentes de trabajo y copias internas de avisos legales
            continue
        if f.startswith("data/"):
            c, m = clase.get(f, ("?", "sin clasificar en docs/v13/datos_inventario.csv"))
            (inc.append(f) if c == "a" or f in brutas else exc.append((f, f"clase ({c}): {m}")))
        else:
            inc.append(f)
    inc += sorted(set(brutas) - set(inc))   # las que solo están en disco (no versionadas)
    return inc, exc


def leeme(n_inc: int, excluidos: list[tuple[str, str]], quitadas: int) -> str:
    politica = ", ".join(f"{k} = {v}" for k, v in T10.politica().items())
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
- **Capa pública:** se han quitado {quitadas} variables de fuentes que no se redistribuyen de data/base/publica/hechos.parquet (proyecto.json → terceros_1_0: {politica}; docs/v14/licencias.md y docs/v14/escenarios.md).

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
            quitadas = T10.filtrar_hechos(RAIZ / f, d)
        elif motivo := T.aplicar(f, RAIZ / f, d):   # V14-V14.2: tabla de output/ redactada o vaciada según terceros_1_0
            exc.append((f, motivo))
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

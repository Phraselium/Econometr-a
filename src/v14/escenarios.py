"""V14.2-B3 · Prueba de los escenarios de terceros_1_0 → docs/v14/escenarios.md y docs/v14/escenarios_cifras.csv.

Cuatro escenarios: el valor por defecto de proyecto.json y los tres valores aplicados a las tres fuentes a la vez. Para cada uno:
- cifras retiradas por fuente (ids);
- páginas que cambian: plantillas de publicacion/ renderizadas en memoria (docs/v5, v8 y v9) frente al render sin retiradas,
  ficheros de consulta/ generados en memoria y descargas de la web;
- árbol público: tablas redactadas y vaciadas (src/v14/terceros.py, `accion`);
- paquete: `make paquete_zenodo` en un directorio temporal (opción --paquete), con su tamaño, que después se borra.
No escribe nada en el repositorio salvo los dos ficheros de salida. Usa la variable VIVIENDA_TERCEROS_1_0; no toca proyecto.json.
Uso: python3 src/v14/escenarios.py [--paquete DIR_TEMPORAL]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src" / "v5"))
from src.v14 import terceros as T  # noqa: E402
from src.v14 import terceros_1_0 as T10  # noqa: E402

PLANTILLAS = [RAIZ / "docs" / v / "plantillas" for v in ("v5", "v8", "v9")]
NINGUNA = {f: "agregados" for f in T10.FUENTES}   # referencia: sin retiradas


def escenarios() -> dict[str, dict]:
    base = json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8"))["terceros_1_0"]
    por_defecto = {f: base[f] for f in T10.FUENTES}
    return {"por defecto": por_defecto, **{f"todas = {v}": {f: v for f in T10.FUENTES} for v in T10.VALORES}}


def _con(pol: dict):
    os.environ[T10.ENV] = json.dumps(pol)


def textos(pol: dict) -> dict[str, str]:
    """Plantillas renderizadas y consulta/ generada en memoria con la política pol."""
    import pandas as pd
    import render as R
    from src.consulta import generar as G
    _con(pol)
    ck = pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv").set_index("id")
    out = {}
    for d in PLANTILLAS:
        for p in sorted(d.glob("**/*.md")):
            if p.name == "README.md" and d.parent.name == "v8":
                continue
            out[p.relative_to(RAIZ).as_posix()] = R.render(p, ck)[0]
    out.update(G.generar())
    return out


def arbol(pol: dict) -> dict[str, int]:
    r = subprocess.run(["git", "ls-files", "-z", "output"], cwd=RAIZ, capture_output=True, text=True, check=True)
    n = {"redactar": 0, "vaciar": 0}
    for f in r.stdout.split("\0"):
        if f and (RAIZ / f).is_file():
            a, _ = T.accion(f, RAIZ / f, pol)
            if a in n:
                n[a] += 1
    return n


def paquete(pol: dict, tmp: Path) -> dict:
    env = {**os.environ, T10.ENV: json.dumps(pol)}
    r = subprocess.run([sys.executable, str(RAIZ / "src" / "v13" / "paquete_zenodo.py"), "--destino", str(tmp)], cwd=RAIZ, env=env,
                       capture_output=True, text=True, check=True)
    base = next(tmp.iterdir())
    tam = sum(p.stat().st_size for p in base.rglob("*") if p.is_file())
    nf = sum(1 for p in base.rglob("*") if p.is_file())
    brutas = len(T10.series_brutas(pol))
    shutil.rmtree(tmp)
    assert r.returncode == 0
    return {"bytes": tam, "ficheros": nf, "series_brutas": brutas}   # sin la salida: lleva la ruta local del directorio temporal


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paquete", help="directorio temporal para generar el paquete de cada escenario (se borra)")
    a = ap.parse_args()
    previo = os.environ.get(T10.ENV)
    esc = escenarios()
    ref = textos(NINGUNA)
    filas, res = [], {}
    for nombre, pol in esc.items():
        ret = T10.retiradas(pol)
        for i, f in ret.items():
            filas.append({"escenario": nombre, "id": i, "fuentes": " y ".join(f)})
        tx = textos(pol)
        cambian = sorted(k for k in tx if tx[k] != ref.get(k))
        marcas = sum(tx[k].count("[cifra no publicada") for k in tx)
        res[nombre] = {"politica": pol, "retiradas": {f: sum(f in v for v in ret.values()) for f in ("Registradores", "Notariado", "AEAT")},
                       "n_ids": len(ret), "cambian": cambian, "marcas": marcas, "arbol": arbol(pol),
                       "hechos_sin": T10.variables_excluidas(pol) or "—"}
        if a.paquete:
            res[nombre]["paquete"] = paquete(pol, Path(a.paquete) / nombre.replace(" ", "_").replace("=", ""))
        print(nombre, {k: v for k, v in res[nombre].items() if k != "cambian"}, len(cambian), "ficheros cambian")
    if previo is None:
        os.environ.pop(T10.ENV, None)
    with (RAIZ / "docs" / "v14" / "escenarios_cifras.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, ["escenario", "id", "fuentes"], lineterminator="\n")
        w.writeheader()
        w.writerows(filas)
    (RAIZ / "docs" / "v14" / "escenarios_resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

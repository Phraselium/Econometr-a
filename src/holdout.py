"""Muestra sellada (holdout) de la v2.

Único punto de acceso a data/sealed. Reglas (docs/v2/decisiones.md, CLAUDE.md):
- Sellado temporal: los últimos 8 trimestres, 2024Q3-2026Q2 (en datos anuales: años >= 2025
  sellados y 2024 como EMBARGO, excluido de entrenamiento y de evaluación, porque mezcla
  trimestres de entrenamiento y sellados).
- Sellado transversal: 3 provincias elegidas con semilla fija (SEED=20261010) se excluyen de
  entrenamiento en TODOS los periodos (y sus municipios en los paneles municipales).
- Las ramas solo leen `load_train(nombre)`. `evaluate(hipotesis, fn)` abre la muestra sellada
  UNA vez por hipótesis confirmatoria, registra el acceso y se niega a repetirlo.
- data/sealed se resuelve en el repositorio PRINCIPAL (git common dir), no en el worktree.

Uso:
    python3 src/holdout.py build        # (re)genera train/ y sealed/ desde data/processed/v2
    from holdout import load_train, evaluate
"""
from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261010
Q_SELLO_INI, Q_SELLO_FIN = "2024Q3", "2026Q2"
ANIO_EMBARGO, ANIO_SELLO_INI = 2024, 2025
N_PROV_SELLADAS = 3

HERE = Path(__file__).resolve().parents[1]          # raíz del worktree o del repo
TRAIN = HERE / "data" / "processed" / "v2" / "train"  # paneles de entrenamiento (versionados)


def _repo_principal() -> Path:
    """Raíz del repositorio principal aunque se ejecute desde un worktree."""
    try:
        common = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                                cwd=HERE, capture_output=True, text=True, check=True).stdout.strip()
        return Path(common).parent
    except Exception:  # noqa: BLE001
        return HERE


SEALED = _repo_principal() / "data" / "sealed"
LOG = SEALED / "_accesos.log"
SRC_V2 = SEALED / "_full"                             # paneles completos (NO versionados)
LOG_MD = _repo_principal() / "docs" / "v2" / "holdout_accesos.md"

# Catálogo de paneles: nombre -> (frecuencia, columna de periodo, columna de provincia o None)
CATALOGO = {
    "panel_prov_q": ("Q", "trimestre", "cod_prov"),
    "panel_prov_a": ("A", "anio", "cod_prov"),
    "panel_muni_a": ("A", "anio", "cod_prov"),
    "panel_ue_a": ("A", "anio", None),
    "panel_ue_q": ("Q", "trimestre", None),
    "nacional_q_v2": ("Q", "trimestre", None),
    "eventos_q": ("Q", "trimestre", None),
}

# 52 provincias (códigos INE 01-52)
PROVINCIAS = [f"{i:02d}" for i in range(1, 53)]


def provincias_selladas() -> list[str]:
    rng = np.random.default_rng(SEED)
    return sorted(rng.choice(PROVINCIAS, size=N_PROV_SELLADAS, replace=False).tolist())


def _mascara_sellada(df: pd.DataFrame, freq: str, col_t: str, col_geo: str | None):
    """Devuelve (sellado, embargo) como máscaras booleanas."""
    if freq == "Q":
        t = df[col_t].astype(str)
        temporal = t >= Q_SELLO_INI   # todo lo posterior al inicio del sellado (incluye filas > 2026Q2 si existen)
        embargo = pd.Series(False, index=df.index)
    else:
        a = pd.to_numeric(df[col_t], errors="coerce")
        temporal = a >= ANIO_SELLO_INI
        embargo = a == ANIO_EMBARGO
    geo = pd.Series(False, index=df.index)
    if col_geo is not None and col_geo in df.columns:
        geo = df[col_geo].astype(str).str.zfill(2).isin(provincias_selladas())
    return temporal | geo, embargo & ~(temporal | geo)


def build() -> dict:
    """Genera data/processed/v2/train/<p>.csv y data/sealed/<p>.csv para cada panel existente."""
    TRAIN.mkdir(parents=True, exist_ok=True)
    SEALED.mkdir(parents=True, exist_ok=True)
    resumen = {"provincias_selladas": provincias_selladas(), "paneles": {}}
    for nombre, (freq, col_t, col_geo) in CATALOGO.items():
        src = SRC_V2 / f"{nombre}.csv"
        if not src.exists():
            src = SRC_V2 / f"{nombre}.csv.gz"
        if not src.exists():
            continue
        df = pd.read_csv(src, dtype={col_geo: str} if col_geo else None)
        sell, emb = _mascara_sellada(df, freq, col_t, col_geo)
        df[~sell & ~emb].to_csv(TRAIN / f"{nombre}.csv", index=False)
        df[sell].to_csv(SEALED / f"{nombre}.csv", index=False)
        resumen["paneles"][nombre] = {"filas": len(df), "train": int((~sell & ~emb).sum()),
                                      "sellado": int(sell.sum()), "embargo": int(emb.sum())}
    (TRAIN / "_sellado.json").write_text(json.dumps(resumen, indent=2, ensure_ascii=False))
    return resumen


def load_train(nombre: str) -> pd.DataFrame:
    """Lectura permitida para las ramas: solo la parte de entrenamiento."""
    _freq, _col_t, col_geo = CATALOGO[nombre]
    return pd.read_csv(TRAIN / f"{nombre}.csv", dtype={col_geo: str} if col_geo else None)


def _accesos() -> list[dict]:
    if not LOG.exists():
        return []
    return [json.loads(x) for x in LOG.read_text().splitlines() if x.strip()]


def evaluate(hipotesis: str, fn, rama: str, paneles: list[str]):
    """Evalúa UNA vez una hipótesis confirmatoria (id de docs/v2/hipotesis.md) en la muestra sellada.

    fn(dict nombre->DataFrame sellado, dict nombre->DataFrame train) -> dict serializable.
    """
    if any(a["hipotesis"] == hipotesis and a["evento"] == "evaluacion" for a in _accesos()):
        raise PermissionError(f"La hipótesis {hipotesis} ya se evaluó en la muestra sellada (una sola vez).")
    sellado = {}
    for p in paneles:
        _freq, _col_t, col_geo = CATALOGO[p]
        sellado[p] = pd.read_csv(SEALED / f"{p}.csv", dtype={col_geo: str} if col_geo else None)
    train = {p: load_train(p) for p in paneles}
    res = fn(sellado, train)
    reg = {"utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": "evaluacion",
           "hipotesis": hipotesis, "rama": rama, "paneles": paneles, "resultado": res}
    with open(LOG, "a") as f:
        f.write(json.dumps(reg, ensure_ascii=False, default=str) + "\n")
    LOG_MD.parent.mkdir(parents=True, exist_ok=True)
    nuevo = not LOG_MD.exists()
    with open(LOG_MD, "a") as f:
        if nuevo:
            f.write("# Accesos a la muestra sellada (copia versionada de data/sealed/_accesos.log)\n\n"
                    "| UTC | hipótesis | rama | paneles | resultado |\n|---|---|---|---|---|\n")
        f.write(f"| {reg['utc']} | {hipotesis} | {rama} | {', '.join(paneles)} | "
                f"{json.dumps(res, ensure_ascii=False, default=str)[:300]} |\n")
    return res


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        print(json.dumps(build(), indent=2, ensure_ascii=False))
    elif len(sys.argv) > 1 and sys.argv[1] == "provincias":
        print(provincias_selladas())
    else:
        print(__doc__)

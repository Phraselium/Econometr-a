"""BS · utilidades: rutas, lectura de ficheros versionados de las ramas y formato numérico en español.
Nada se estima aquí. Toda cifra del informe sale de un fichero y se cita (ver Fuentes)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

R = Path(__file__).resolve().parents[2]
O = R / "output" / "v2"
SEED = 20261010
RAMAS = ("BA", "BV", "BI", "BO", "BP", "BM", "BD")


def j(rel: str):
    return json.loads((O / rel).read_text())


def c(rel: str, **kw) -> pd.DataFrame:
    return pd.read_csv(O / rel, **kw)


def num(x, d: int = 3, signo: bool = False) -> str:
    """Número con coma decimal. NaN -> 'n/d'."""
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "n/d"
    s = f"{x:+.{d}f}" if signo else f"{x:.{d}f}"
    s = s.replace("-", "−") if s.startswith("-") else s
    return s.replace(".", ",")


def pv(p) -> str:
    """p-valor: 3 decimales; <0,001 como cota."""
    if p is None or (isinstance(p, float) and np.isnan(p)):
        return "n/d"
    if p < 0.001:
        return "<0,001"
    return num(p, 3)


def ic(lo, hi, d: int = 3) -> str:
    return f"[{num(lo, d)}; {num(hi, d)}]"


def entero(x) -> str:
    return f"{int(round(x)):,}".replace(",", ".")


def bh(p: pd.Series) -> pd.Series:
    """Benjamini-Hochberg (FDR); NaN se ignoran."""
    p = pd.Series(p, dtype=float)
    ok = p.notna()
    out = pd.Series(np.nan, index=p.index)
    if ok.sum() == 0:
        return out
    v = p[ok].to_numpy()
    m = len(v)
    o = np.argsort(v, kind="stable")
    adj = np.empty(m)
    prev = 1.0
    for rank in range(m, 0, -1):
        i = o[rank - 1]
        prev = min(prev, v[i] * m / rank)
        adj[i] = prev
    out[ok] = np.minimum(adj, 1.0)
    return out


def tabla_md(df: pd.DataFrame, fmt: dict | None = None) -> str:
    """DataFrame -> tabla markdown. fmt: columna -> función de formato."""
    fmt = fmt or {}
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in df.iterrows():
        cel = []
        for k in cols:
            v = r[k]
            if k in fmt:
                cel.append(fmt[k](v))
            elif isinstance(v, (float, np.floating)):
                cel.append(num(v, 3))
            else:
                cel.append(str(v).replace("|", "/"))
        out.append("| " + " | ".join(cel) + " |")
    return "\n".join(out)


def parse_hipotesis_md() -> pd.DataFrame:
    """Tabla de confirmatorias de docs/v2/hipotesis.md (Id, Rama, Hipótesis, Signo esperado, Especificación, Muestra sellada)."""
    filas = []
    for ln in (R / "docs" / "v2" / "hipotesis.md").read_text().splitlines():
        if re.match(r"^\| H\d \|", ln):
            p = [x.strip() for x in ln.strip().strip("|").split("|")]
            filas.append(dict(hipotesis=p[0], rama=p[1], enunciado=p[2], signo_esperado=p[3], especificacion=p[4], muestra_sellada=p[5]))
    return pd.DataFrame(filas)

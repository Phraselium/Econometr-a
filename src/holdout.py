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


def _sin_interpolacion_hacia_sellado(tr: pd.DataFrame, col_t: str, col_geo: str | None) -> pd.DataFrame:
    """Anula en entrenamiento los valores interpolados POSTERIORES a la última observación de entrenamiento.

    Una interpolación entre la última observación de entrenamiento y la primera sellada (p. ej. población
    de 2024Q2 entre el 1-ene-2024 y el 1-ene-2025) usa información sellada: fuga. Esos valores (y sus
    transformaciones ln_/d_ln_/d4_ln_) pasan a NaN.
    """
    met = [c for c in tr.columns if c.endswith("_metodo")]
    grupos = tr.groupby(col_geo) if col_geo and col_geo in tr.columns else [(None, tr)]
    for _, g in grupos:
        for mc in met:
            var = mc[: -len("_metodo")]
            obs = g.loc[g[mc] == "observado", col_t]
            if obs.empty:
                continue
            ult = obs.astype(str).max()
            idx = g.index[(g[mc] == "interpolado_loglineal") & (g[col_t].astype(str) > ult)]
            if len(idx):
                cols = [c for c in (var, f"ln_{var}", f"d_ln_{var}", f"d4_ln_{var}") if c in tr.columns]
                tr.loc[idx, cols] = np.nan
                tr.loc[idx, mc] = "anulado_fuga_sellado"
    return tr


# Índices publicados en base 2025=100 (INE IPV e IPC): su nivel incorpora información de 2025 (sellada).
# En entrenamiento se rebasan a media de 2015 = 100 por unidad; las diferencias logarítmicas no cambian.
INDICES_BASE_2025 = ["ipc_alquiler", "ipv", "ipv_nueva", "ipv_usada"]


def _rebase_indices_2015(tr: pd.DataFrame, nombre: str, col_t: str, col_geo: str | None) -> pd.DataFrame:
    anio = tr[col_t].astype(str).str[:4]
    unidad = tr[col_geo].astype(str) if col_geo and col_geo in tr.columns else pd.Series("_", index=tr.index)
    lnf = {}
    for v in INDICES_BASE_2025:
        if v not in tr.columns:
            continue
        base = tr[v].where(anio == "2015").groupby(unidad).transform("mean")
        f = 100.0 / base
        tr[v] = tr[v] * f
        lnf[v] = np.log(f)
        if f"ln_{v}" in tr.columns:
            tr[f"ln_{v}"] = tr[f"ln_{v}"] + lnf[v]
    if "ratio_precio_alquiler_idx" in tr.columns and "ipc_alquiler" in lnf:
        ajuste = -lnf["ipc_alquiler"]
        if nombre == "nacional_q_v2" and "ipv" in lnf:   # nacional: ln ipv − ln ipc_alquiler
            ajuste = ajuste + lnf["ipv"]
        tr["ratio_precio_alquiler_idx"] = tr["ratio_precio_alquiler_idx"] + ajuste
    return tr


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
        # Rebase ANTES de separar: entrenamiento y sellado quedan en la MISMA base (2015=100 por unidad).
        # El factor usa solo valores de 2015 (anteriores al sellado). Rebasar solo el entrenamiento
        # anulaba por construcción efectos medidos concatenando niveles (revisión BP).
        df = _rebase_indices_2015(df, nombre, col_t, col_geo)
        sell, emb = _mascara_sellada(df, freq, col_t, col_geo)
        tr = _sin_interpolacion_hacia_sellado(df[~sell & ~emb].copy(), col_t, col_geo)
        tr.to_csv(TRAIN / f"{nombre}.csv", index=False)
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
    # Cualquier acceso previo (apertura o evaluación) cuenta: una sola apertura por hipótesis, aunque falle.
    if any(a["hipotesis"] == hipotesis for a in _accesos()):
        raise PermissionError(f"La hipótesis {hipotesis} ya abrió la muestra sellada (una sola vez).")
    SEALED.mkdir(parents=True, exist_ok=True)
    apertura = {"utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": "apertura",
                "hipotesis": hipotesis, "rama": rama, "paneles": paneles}
    with open(LOG, "a") as f:   # se registra ANTES de leer nada sellado
        f.write(json.dumps(apertura, ensure_ascii=False) + "\n")
    _log_md(apertura["utc"], hipotesis, rama, paneles, "APERTURA (antes de leer)")
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
    _log_md(reg["utc"], hipotesis, rama, paneles, json.dumps(res, ensure_ascii=False, default=str)[:300])
    return res


HIPOTESIS_V2_SELLADAS = ("H1", "H2", "H6", "H7")   # las cuatro con evaluación sellada en v2


def load_full(nombre: str, uso: str) -> pd.DataFrame:
    """v3: panel COMPLETO (entrenamiento + sellado v2) para hechos (C1) y cotas (C2).

    Solo se permite cuando todas las evaluaciones selladas de v2 ya se hicieron: el sellado v2 ya no
    protege ninguna hipótesis pendiente. Cada lectura se registra (evento «v3_completo»).
    El sellado v3 propio (secciones censales) es otro y no pasa por aquí.
    """
    hechas = {a["hipotesis"] for a in _accesos() if a.get("evento") == "evaluacion"}
    faltan = [h for h in HIPOTESIS_V2_SELLADAS if h not in hechas]
    if faltan:
        raise PermissionError(f"Evaluaciones selladas v2 pendientes: {faltan}")
    _freq, _col_t, col_geo = CATALOGO[nombre]
    src = SRC_V2 / f"{nombre}.csv"
    df = pd.read_csv(src, dtype={col_geo: str} if col_geo else None)
    df = _rebase_indices_2015(df, nombre, _col_t, col_geo)
    reg = {"utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": "v3_completo",
           "hipotesis": "-", "rama": uso, "paneles": [nombre]}
    with open(LOG, "a") as f:
        f.write(json.dumps(reg, ensure_ascii=False) + "\n")
    return df


# ---------------------------------------------------------------- sellado v3 (secciones censales, P-C)
ULTIMA_OLEADA_V3 = "2026M05"          # última oleada de VUT del INE: sellada para todas las unidades
FRACCION_DISTRITOS_V3 = 0.20
VUT_SECCION = HERE / "data" / "raw" / "v3" / "ine_v3_vut_seccion.csv.gz"


def bloques_distritos_v3(distritos: list[str]) -> dict[str, str]:
    """distrito (7 dígitos: municipio 5 + distrito 2) -> bloque espacial.

    Sin cartografía: en municipios con ≥2 distritos, pares de distritos de numeración consecutiva (01-02, 03-04…);
    en municipios con un solo distrito, el propio municipio. Supuesto documentado en docs/v3/decisiones.md.
    """
    dist = sorted(set(distritos))
    por_mun: dict[str, list[str]] = {}
    for d in dist:
        por_mun.setdefault(d[:5], []).append(d)
    out = {}
    for mun, ds in por_mun.items():
        for d in ds:
            out[d] = mun if len(ds) == 1 else f"{mun}-{(int(d[5:]) - 1) // 2:02d}"
    return out


def distritos_sellados_v3() -> list[str]:
    """20 % de los distritos por bloques espaciales completos, ESTRATIFICADO: en municipios con ≥4 bloques el
    estrato es el municipio (cada gran ciudad conserva ~80 % de sus distritos para estimar); el resto de bloques
    se estratifica por provincia. En cada estrato, bloques en orden aleatorio (SEED) hasta alcanzar el 20 % de sus
    distritos. Lista de distritos de la oleada 2024M02 (estable)."""
    v = pd.read_csv(VUT_SECCION, usecols=["periodo", "nivel", "codigo"], dtype={"codigo": str})
    dist = v.loc[(v["nivel"] == "distrito") & (v["periodo"] == "2024M02"), "codigo"].str.zfill(7).unique().tolist()
    bl = bloques_distritos_v3(dist)
    miembros: dict[str, list[str]] = {}
    for d, b in bl.items():
        miembros.setdefault(b, []).append(d)
    n_bloques_mun: dict[str, int] = {}
    for b in miembros:
        n_bloques_mun[b[:5]] = n_bloques_mun.get(b[:5], 0) + 1
    estratos: dict[str, list[str]] = {}
    for b in sorted(miembros):
        e = b[:5] if n_bloques_mun[b[:5]] >= 4 else b[:2]
        estratos.setdefault(e, []).append(b)
    rng = np.random.default_rng(SEED)
    sel = set()
    for e in sorted(estratos):
        bs = estratos[e]
        objetivo = FRACCION_DISTRITOS_V3 * sum(len(miembros[b]) for b in bs)
        n = 0
        for i in rng.permutation(len(bs)):
            if n >= objetivo - 1e-9 or n + len(miembros[bs[i]]) > objetivo + 1:   # no pasarse más de 1 distrito
                continue
            sel.add(bs[i])
            n += len(miembros[bs[i]])
    return sorted(d for d, b in bl.items() if b in sel)


def es_sellado_v3(codigo_seccion_o_distrito: pd.Series, periodo: pd.Series | None = None,
                  sellados: list[str] | None = None) -> pd.Series:
    """True si la unidad pertenece a un distrito sellado o la observación es de la última oleada."""
    sellados = set(sellados if sellados is not None else distritos_sellados_v3())
    m = codigo_seccion_o_distrito.astype(str).str.zfill(7).str[:7].isin(sellados)
    if periodo is not None:
        m = m | (periodo.astype(str) >= ULTIMA_OLEADA_V3)
    return m


def _log_md(utc, hipotesis, rama, paneles, texto):
    LOG_MD.parent.mkdir(parents=True, exist_ok=True)
    nuevo = not LOG_MD.exists()
    with open(LOG_MD, "a") as f:
        if nuevo:
            f.write("# Accesos a la muestra sellada (copia versionada de data/sealed/_accesos.log)\n\n"
                    "| UTC | hipótesis | rama | paneles | evento / resultado |\n|---|---|---|---|---|\n")
        f.write(f"| {utc} | {hipotesis} | {rama} | {', '.join(paneles)} | {texto} |\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        print(json.dumps(build(), indent=2, ensure_ascii=False))
    elif len(sys.argv) > 1 and sys.argv[1] == "provincias":
        print(provincias_selladas())
    else:
        print(__doc__)

"""M7 · Precio de compra y alquiler triangulados (C1) y exuberancia GSADF (C4). Determinista, sin red.

Uso: python3 src/v4/m7_run.py [--smoke]   (smoke: 49 réplicas bootstrap, salida en output/v4/M7/smoke)

Supuestos declarados:
  - Independencia de fuentes de precio: el IPV del INE se construye con datos notariales, así que
    INE y Notariado forman UN grupo («notarial»); MIVAU (tasaciones) y Registradores (inscripciones)
    son otros dos. La serie BdE de precio tasado es la misma que la del MIVAU (no independiente).
  - C1 si al menos dos fuentes de grupos distintos difieren <= 5 pp anuales en la variación anualizada.
  - Alquiler: IPC de alquiler (encuesta/administrativo, índice), SERPAVI (STOCK: mediana de contratos
    vigentes declarados en el IRPF, responde con retraso) e Incasòl (FLUJO: fianzas de contratos
    nuevos; solo Cataluña; el umbral de la banda superior pasa de >650 a >600 euros en 2021).
  - GSADF: ADF con un rezago de Δy fijo; r0 = 0,01 + 1,8/sqrt(T); valores críticos por bootstrap
    wild recursivo (Phillips y Shi 2020): Δy*_t = e_t·Δy_t, e_t ~ N(0,1). Capa C4.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import econ_utils  # noqa: E402
import holdout  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
SMOKE = "--smoke" in sys.argv
NBOOT = 49 if SMOKE else 499
RAW = RAIZ / "data" / "raw"
OUT = RAIZ / "output" / "v4" / "M7" / ("smoke" if SMOKE else "")
TAB = OUT / "tablas"
TAB.mkdir(parents=True, exist_ok=True)
REG = econ_utils.Registry(OUT / "registro.csv")
TOL = 0.05
GRUPO = {"INE_IPV": "notarial", "Notariado": "notarial", "MIVAU_tasado": "tasacion",
         "Registradores": "registral", "IPC_alquiler": "ine", "SERPAVI": "irpf", "Incasol": "fianzas"}


def reg(fase, mid, formula, n, notas, ini="", fin="", coef=np.nan, p=np.nan):
    REG.log(fase, mid, formula, ini, fin, n, np.nan, np.nan, np.nan, coef_interes=coef, p_interes=p, notas=notas)


def rebase(s: pd.Series, base: int = 2015) -> pd.Series:
    return 100 * s / s.loc[base]


def anual_trim(df: pd.DataFrame, col: str) -> pd.Series:
    """Media anual de una serie trimestral; solo años con 4 trimestres observados."""
    d = df[["trimestre", col]].dropna().copy()
    d["y"] = d.trimestre.str[:4].astype(int)
    g = d.groupby("y")[col].agg(["mean", "count"])
    return g[g["count"] == 4]["mean"]


# ------------------------------------------------------------------ 1. triangulación
def variaciones(idx: dict[str, pd.Series], a0: int, a1: int) -> dict:
    """Variación acumulada y anualizada por fuente entre a0 y a1; regla C1 con independencia."""
    cum, ann = {}, {}
    for k, s in idx.items():
        if a0 in s.index and a1 in s.index and s.loc[a0] > 0:
            cum[k] = float(s.loc[a1] / s.loc[a0] - 1)
            ann[k] = float((s.loc[a1] / s.loc[a0]) ** (1 / (a1 - a0)) - 1)
    pares = [(a, b, abs(ann[a] - ann[b])) for a in ann for b in ann
             if a < b and GRUPO[a] != GRUPO[b]]
    ok = [(a, b, d) for a, b, d in pares if d <= TOL]
    mejor = min(pares, key=lambda x: x[2]) if pares else None
    return {"cum": cum, "ann": ann, "n_fuentes": len(cum),
            "rango_cum": [min(cum.values()), max(cum.values())] if cum else [np.nan, np.nan],
            "c1": bool(ok), "pares_ok": [f"{a}/{b}" for a, b, _ in ok],
            "mejor_par": f"{mejor[0]}/{mejor[1]} ({mejor[2] * 100:.1f} pp)" if mejor else ""}


def fila_var(terr, tipo, a0, a1, v):
    return {"territorio": terr, "tipo": tipo, "desde": a0, "hasta": a1, "n_fuentes": v["n_fuentes"],
            "min_pct": 100 * v["rango_cum"][0], "max_pct": 100 * v["rango_cum"][1],
            "mediana_pct": 100 * float(np.median(list(v["cum"].values()))) if v["cum"] else np.nan,
            "capa": "C1" if v["c1"] else "C4",
            "pares_dentro_5pp": ";".join(v["pares_ok"]), "par_mas_cercano": v["mejor_par"],
            **{f"var_{k}_pct": 100 * x for k, x in v["cum"].items()}}


def dispersion(idx: dict[str, pd.Series], nombre: str) -> pd.DataFrame:
    df = pd.DataFrame(idx)
    dl = np.log(df).diff()
    out = pd.DataFrame({"mediana_idx": df.median(axis=1), "min_idx": df.min(axis=1),
                        "max_idx": df.max(axis=1), "rango_idx": df.max(axis=1) - df.min(axis=1),
                        "sd_dln": dl.std(axis=1, ddof=1), "n": df.notna().sum(axis=1)})
    out.index.name = "anio"
    out.to_csv(TAB / f"dispersion_{nombre}.csv")
    return out


def triangulacion(nac: pd.DataFrame, pan: pd.DataFrame) -> dict:
    res: dict = {}
    # ---- precio nacional
    cgn = pd.read_csv(RAW / "pdf/notariado_cgn_extranjeros_semestral.csv")
    cgn = cgn[(cgn.serie == "precio_m2") & (cgn.categoria == "Total general")].copy()
    cgn["y"] = cgn.periodo.str[:4].astype(int)
    notar = cgn.groupby("y").valor.agg(["mean", "count"])
    notar = notar[notar["count"] == 2]["mean"]
    rg = pd.read_csv(RAW / "pdf/registradores_opendata_anual.csv")
    rgn = rg[(rg.serie == "compraventas_viv_pm2") & (rg.nivel == "nacional")]
    rgn = pd.Series(rgn.valor.to_numpy(), index=rgn.periodo.astype(int).to_numpy())
    precio = {"INE_IPV": anual_trim(nac, "ipv"), "MIVAU_tasado": anual_trim(nac, "p_tasado"),
              "Registradores": rgn, "Notariado": notar}
    precio = {k: rebase(s) for k, s in precio.items() if 2015 in s.index}
    pd.DataFrame(precio).to_csv(TAB / "precio_nacional_idx2015.csv", index_label="anio")
    dsp = dispersion(precio, "precio_nacional")
    filas = []
    for a0, a1 in [(2015, 2025), (2021, 2025)]:
        v = variaciones(precio, a0, a1)
        filas.append(fila_var("España", "precio", a0, a1, v))
        res[f"precio_{a0}_{a1}"] = v
        reg("triang", f"precio_nac_{a0}_{a1}", "var acumulada de índices 2015=100", v["n_fuentes"],
            f"rango [{100 * v['rango_cum'][0]:.1f}; {100 * v['rango_cum'][1]:.1f}] %; C1={v['c1']}",
            a0, a1, coef=float(np.median(list(v["cum"].values()))))
    # ---- precio por CCAA
    mp = {"Principado de Asturias": "Asturias", "C. Foral de Navarra": "Comunidad Foral de Navarra"}
    rc = rg[(rg.serie == "compraventas_viv_pm2") & (rg.nivel == "ccaa")].copy()
    rc["ccaa"] = rc.territorio.replace(mp)
    rc["anio"] = rc.periodo.astype(int)
    c1_ccaa = {}
    for c in sorted(pan.ccaa.unique()):
        p = pan[pan.ccaa == c]
        idx = {"INE_IPV": anual_trim(p, "ipv"), "MIVAU_tasado": anual_trim(p, "p_tasado"),
               "Registradores": rc[rc.ccaa == c].set_index("anio").valor}
        idx = {k: rebase(s) for k, s in idx.items() if 2015 in s.index}
        for a0, a1 in [(2015, 2025), (2021, 2025)]:
            v = variaciones(idx, a0, a1)
            filas.append(fila_var(c, "precio", a0, a1, v))
            c1_ccaa[(c, a0)] = v["c1"]
    pd.DataFrame(filas).to_csv(TAB / "variacion_precio.csv", index=False)
    res["n_ccaa_c1"] = {a0: sum(1 for (c, a), ok in c1_ccaa.items() if a == a0 and ok) for a0 in (2015, 2021)}
    reg("triang", "precio_ccaa_c1", "n CCAA con >=2 fuentes independientes a <=5 pp anuales",
        len(pan.ccaa.unique()), str(res["n_ccaa_c1"]))
    res["disp_precio"] = dsp

    # ---- alquiler
    srp = pd.read_csv(RAW / "pdf/serpavi_esp_agregado.csv")
    sp = {t: srp[srp.serie.str.endswith(f"pond_{t}")].set_index("periodo").valor
          for t in ("composicion_constante", "composicion_variable")}
    alq = {"IPC_alquiler": anual_trim(nac, "ipc_alquiler"), "SERPAVI": sp["composicion_constante"]}
    alq = {k: rebase(s) for k, s in alq.items()}
    alt = rebase(sp["composicion_variable"])
    pd.DataFrame({**alq, "SERPAVI_composicion_variable": alt}).to_csv(TAB / "alquiler_nacional_idx2015.csv",
                                                                       index_label="anio")
    # Cataluña: IPC, SERPAVI CCAA, Incasòl (media ponderada por contratos de las bandas)
    sc = pd.read_csv(RAW / "pdf/serpavi_ccaa.csv")
    sc = sc[(sc.variable == "alquiler_m2") & (sc.estadistico == "mediana") & (sc.tipologia == "VC")]
    inc = pd.read_csv(RAW / "v3/incasol_fianzas_municipio_v3.csv.gz")
    inc = inc[inc.periodo.str.contains("gener-desembre")].copy()
    inc["y"] = inc.periodo.str[:4].astype(int)
    inc["tipo"] = np.where(inc.unidad == "EUR/mes", "renta", "n")
    inc["banda_k"] = inc.serie.str.replace(r"_(renta_media|n_contratos)_", "|", regex=True).str.split("|").str[1]
    w = inc[inc.tipo == "n"].pivot_table(index=["codigo", "y", "banda_k"], values="valor", aggfunc="sum")
    r = inc[inc.tipo == "renta"].pivot_table(index=["codigo", "y", "banda_k"], values="valor", aggfunc="mean")
    j = w.join(r, lsuffix="_n", rsuffix="_r", how="inner").dropna()
    j["nr"] = j.valor_n * j.valor_r
    g = j.groupby("y")[["valor_n", "nr"]].sum()
    incasol = g.nr / g.valor_n
    cat = {"IPC_alquiler": anual_trim(pan[pan.ccaa == "Cataluña"], "ipc_alquiler"),
           "SERPAVI": sc[sc.nombre == "Cataluña"].set_index("periodo").valor,
           "Incasol": incasol}
    cat = {k: rebase(s) for k, s in cat.items() if 2015 in s.index}
    pd.DataFrame(cat).to_csv(TAB / "alquiler_cataluna_idx2015.csv", index_label="anio")
    dispersion(alq, "alquiler_nacional")
    dispersion(cat, "alquiler_cataluna")
    fa = []
    for terr, idx in (("España", alq), ("Cataluña", cat)):
        for a0, a1 in [(2015, 2025), (2021, 2025), (2015, 2024), (2021, 2024)]:
            v = variaciones(idx, a0, a1)
            if v["n_fuentes"] >= 2:
                fa.append(fila_var(terr, "alquiler", a0, a1, v))
                res[f"alq_{terr}_{a0}_{a1}"] = v
                reg("triang", f"alq_{terr}_{a0}_{a1}", "var acumulada de índices 2015=100", v["n_fuentes"],
                    f"rango [{100 * v['rango_cum'][0]:.1f}; {100 * v['rango_cum'][1]:.1f}] %; C1={v['c1']}",
                    a0, a1, coef=float(np.median(list(v["cum"].values()))))
    # CCAA: IPC frente a SERPAVI (dos fuentes independientes)
    mps = {"Asturias": "Principado de Asturias", "Comunidad Foral de Navarra": "Comunidad Foral de Navarra"}
    n_ok = 0
    for c in sorted(pan.ccaa.unique()):
        idx = {"IPC_alquiler": anual_trim(pan[pan.ccaa == c], "ipc_alquiler"),
               "SERPAVI": sc[sc.nombre == mps.get(c, c)].set_index("periodo").valor}
        idx = {k: rebase(s) for k, s in idx.items() if 2015 in s.index}
        v = variaciones(idx, 2015, 2024)
        fa.append(fila_var(c, "alquiler", 2015, 2024, v))
        n_ok += int(v["c1"])
    res["n_ccaa_alq_c1"] = n_ok
    pd.DataFrame(fa).to_csv(TAB / "variacion_alquiler.csv", index=False)
    reg("triang", "alq_ccaa_c1", "IPC frente a SERPAVI 2015-2024 <=5 pp anuales", 17, f"{n_ok} de 17 CCAA")
    res["alq"] = alq
    res["cat"] = cat
    res["precio"] = precio
    return res


# ------------------------------------------------------------------ 2. GSADF
def _prefijos(y: np.ndarray) -> tuple[np.ndarray, int]:
    """Sumas acumuladas de productos cruzados de [1, y_{t-1}, Δy_{t-1}, Δy_t] para t = 2..T-1."""
    dy = np.diff(y)
    x = y[1:-1]
    z = dy[:-1]
    w = dy[1:]
    m = np.column_stack([np.ones_like(x), x, z, w])
    prod = m[:, :, None] * m[:, None, :]
    p = np.zeros((len(m) + 1, 4, 4))
    p[1:] = np.cumsum(prod, axis=0)
    return p, len(m)


def _ventanas(n: int, w0: int) -> tuple[np.ndarray, np.ndarray]:
    a, b = np.triu_indices(n, k=w0 - 1)
    return a, b


def bsadf_path(y: np.ndarray, w0: int, ab: tuple[np.ndarray, np.ndarray] | None = None) -> np.ndarray:
    """Secuencia BSADF_b (b = fin de ventana) con ventana inicial libre y longitud >= w0."""
    p, n = _prefijos(y)
    a, b = ab if ab is not None else _ventanas(n, w0)
    s = p[b + 1] - p[a]
    xtx = s[:, :3, :3]
    xty = s[:, :3, 3]
    inv = np.linalg.inv(xtx + 1e-12 * np.eye(3))
    beta = np.einsum("nij,nj->ni", inv, xty)
    ssr = s[:, 3, 3] - np.einsum("ni,ni->n", beta, xty)
    k = (b - a + 1) - 3
    s2 = np.maximum(ssr, 1e-300) / k
    t = beta[:, 1] / np.sqrt(s2 * inv[:, 1, 1])
    m = np.full((n, n), -np.inf)
    m[b, a] = t
    return m.max(axis=1)


def gsadf(y: np.ndarray, nboot: int, seed: int) -> dict:
    t_len = len(y)
    r0 = 0.01 + 1.8 / math.sqrt(t_len)
    w0 = max(int(math.floor(r0 * t_len)), 8)
    n = t_len - 2
    ab = _ventanas(n, w0)
    bs = bsadf_path(y, w0, ab)
    gs = float(np.max(bs[w0 - 1:]))
    dy = np.diff(y)
    L = max(2, math.ceil(math.log(t_len)))

    def nulo(tipo: str, sem: int) -> dict:
        rng = np.random.default_rng(sem)
        bpaths = np.empty((nboot, n))
        for i in range(nboot):
            e = rng.standard_normal(len(dy))
            ys = np.concatenate([[y[0]], y[0] + np.cumsum(e * dy if tipo == "wild" else e)])
            bpaths[i] = bsadf_path(ys, w0, ab)
        bmax = bpaths[:, w0 - 1:].max(axis=1)
        cv = np.quantile(bpaths, 0.95, axis=0)
        sobre = np.zeros(n, bool)
        sobre[w0 - 1:] = bs[w0 - 1:] > cv[w0 - 1:]
        eps, i = [], 0
        while i < n:   # fechado: BSADF > vc 95 % al menos L = ceil(ln T) periodos seguidos
            if sobre[i]:
                j = i
                while j + 1 < n and sobre[j + 1]:
                    j += 1
                if j - i + 1 >= L:
                    eps.append((i + 2, j + 2))   # índices de y
                i = j + 1
            else:
                i += 1
        return {"cv_g": float(np.quantile(bmax, 0.95)), "p": float((1 + np.sum(bmax >= gs)) / (nboot + 1)),
                "cv_path": cv, "eps": eps}

    mc = nulo("mc", seed)
    wd = nulo("wild", seed + 7)
    return {"T": t_len, "r0": r0, "w0": w0, "gsadf": gs, "cv95": mc["cv_g"], "p": mc["p"], "bsadf": bs,
            "cv_path": mc["cv_path"], "episodios_idx": mc["eps"], "L": L, "cv95_wild": wd["cv_g"],
            "p_wild": wd["p"], "episodios_wild": wd["eps"], "cv_path_wild": wd["cv_path"]}


def verificar_implementacion() -> dict:
    """Serie simulada con burbuja (episodio explosivo 1,05 entre 45 y 65, colapso) y otra sin ella."""
    rng = np.random.default_rng(SEED)
    t_len = 120
    e = rng.standard_normal(t_len)
    nul = 100 + np.cumsum(e)
    b = np.empty(t_len)
    b[0] = 100.0
    for t in range(1, t_len):
        if 45 <= t < 65:
            b[t] = 1.05 * b[t - 1] + e[t]
        elif t == 65:
            b[t] = b[t - 1] * 0.55 + e[t]
        else:
            b[t] = b[t - 1] + e[t]
    r_nul = gsadf(nul, NBOOT, SEED + 1)
    r_bur = gsadf(b, NBOOT, SEED + 2)
    out = {"nula": {k: r_nul[k] for k in ("gsadf", "cv95", "p", "cv95_wild", "p_wild")},
           "burbuja": {k: r_bur[k] for k in ("gsadf", "cv95", "p", "cv95_wild", "p_wild")},
           "episodios_burbuja": r_bur["episodios_idx"], "episodios_nula": r_nul["episodios_idx"],
           "verdadero": [45, 65]}
    out["ok"] = bool(r_bur["p"] <= 0.05 < r_nul["p"] and r_bur["episodios_idx"])
    reg("verif", "gsadf_sim_nula", "GSADF sobre paseo aleatorio simulado T=120", 120,
        f"GSADF {r_nul['gsadf']:.2f}, cv95 {r_nul['cv95']:.2f}, p {r_nul['p']:.3f}", p=r_nul["p"])
    reg("verif", "gsadf_sim_burbuja", "GSADF sobre serie con episodio explosivo 45-65", 120,
        f"GSADF {r_bur['gsadf']:.2f}, cv95 {r_bur['cv95']:.2f}, p {r_bur['p']:.3f}; episodios {out['episodios_burbuja']}",
        p=r_bur["p"])
    return out


def trim_idx(fechas: list[str], i: int) -> str:
    return fechas[i]


def bh(p: np.ndarray) -> np.ndarray:
    """p ajustados de Benjamini-Hochberg."""
    m = len(p)
    o = np.argsort(p)
    adj = np.minimum.accumulate((p[o] * m / np.arange(1, m + 1))[::-1])[::-1]
    out = np.empty(m)
    out[o] = np.minimum(adj, 1.0)
    return out


def distorsion_tamano(r: int = 300) -> dict:
    """Tamaño del GSADF con valores críticos iid cuando Δy es AR(1) (phi = 0,5): evalúa el sobre-rechazo."""
    t_len = 78
    rng = np.random.default_rng(SEED + 5)
    w0 = max(int(math.floor((0.01 + 1.8 / math.sqrt(t_len)) * t_len)), 8)
    ab = _ventanas(t_len - 2, w0)
    stat = lambda y: float(np.max(bsadf_path(y, w0, ab)[w0 - 1:]))  # noqa: E731
    nul = np.array([stat(np.cumsum(rng.standard_normal(t_len))) for _ in range(r)])
    cv = float(np.quantile(nul, 0.95))
    out = {"cv95_iid": cv, "rechazo_iid": float(np.mean(nul > cv))}
    for phi in (0.3, 0.5):
        rej = 0
        for _ in range(r):
            e = rng.standard_normal(t_len)
            d = np.zeros(t_len)
            for t in range(1, t_len):
                d[t] = phi * d[t - 1] + e[t]
            rej += stat(np.cumsum(d)) > cv
        out[f"rechazo_phi{phi}"] = rej / r
    reg("verif", "tamano_gsadf", "tamaño con Δy AR(1), T=78, vc iid", r, str(out))
    return out


def tramo_continuo(p: pd.DataFrame) -> pd.DataFrame:
    """Tramo trimestral contiguo más largo sin huecos (el test exige una serie sin interrupciones)."""
    per = pd.PeriodIndex([f"{t[:4]}Q{t[-1]}" for t in p.index], freq="Q")
    pos = np.array([q.ordinal for q in per])
    corte = np.where(np.diff(pos) != 1)[0] + 1
    tramos = np.split(np.arange(len(p)), corte)
    return p.iloc[max(tramos, key=len)]


def series_gsadf(nac: pd.DataFrame, pan: pd.DataFrame) -> dict:
    """Ratios precio/alquiler (dos medidas) por CCAA y nacional; precio/renta solo nacional."""
    series = []
    n = nac.set_index("trimestre")
    n = n[["ipv", "p_tasado", "ipc_alquiler", "renta_hog"]].dropna()
    rb = n.loc["2015Q1":"2015Q4"].mean()
    nb = n / rb * 100
    series.append(("Nacional", "precio/alquiler: IPV / IPC alquiler", np.log(nb.ipv / nb.ipc_alquiler)))
    series.append(("Nacional", "precio/alquiler: valor tasado / IPC alquiler", np.log(nb.p_tasado / nb.ipc_alquiler)))
    series.append(("Nacional", "precio/renta: IPV / renta del hogar", np.log(nb.ipv / nb.renta_hog)))
    series.append(("Nacional", "precio/renta: valor tasado / renta del hogar", np.log(nb.p_tasado / nb.renta_hog)))
    series.append(("Nacional", "nivel: IPV", np.log(nb.ipv)))
    series.append(("Nacional", "nivel: valor tasado", np.log(nb.p_tasado)))
    for c in sorted(pan.ccaa.unique()):
        p = pan[pan.ccaa == c].set_index("trimestre")[["ipv", "p_tasado", "ipc_alquiler"]].dropna()
        p = tramo_continuo(p)
        pb = p / p.mean() * 100   # la base solo desplaza la constante de log(ratio)
        series.append((c, "precio/alquiler: IPV / IPC alquiler", np.log(pb.ipv / pb.ipc_alquiler)))
        series.append((c, "precio/alquiler: valor tasado / IPC alquiler", np.log(pb.p_tasado / pb.ipc_alquiler)))
    filas, curvas = [], {}
    for k, (terr, med, s) in enumerate(series):
        r = gsadf(s.to_numpy(), NBOOT, SEED + 100 + k)
        fe = list(s.index)
        eps = [f"{fe[a]}-{fe[b]}" for a, b in r["episodios_idx"]]
        filas.append({"territorio": terr, "medida": med, "T": r["T"], "ini": fe[0], "fin": fe[-1],
                      "r0": r["r0"], "gsadf": r["gsadf"], "cv95_mc": r["cv95"], "p_mc": r["p"],
                      "cv95_wild": r["cv95_wild"], "p_wild": r["p_wild"],
                      "episodios_wild": ";".join(f"{fe[a]}-{fe[b]}" for a, b in r["episodios_wild"]),
                      "episodios_bsadf": ";".join(eps), "capa": "C4"})
        curvas[(terr, med)] = (fe, r)
    df = pd.DataFrame(filas)
    h = econ_utils.holm(dict(zip(df.index.astype(str), df.p_mc)))
    df["p_holm"] = [h[str(i)] for i in df.index]
    hw = econ_utils.holm(dict(zip(df.index.astype(str), df.p_wild)))
    df["p_holm_wild"] = [hw[str(i)] for i in df.index]
    fam = np.where(df.territorio == "Nacional", "nacional", "ccaa")
    for col in ("p_mc", "p_wild"):
        df["bh_" + col] = np.nan
        for f in ("nacional", "ccaa"):
            m = fam == f
            df.loc[m, "bh_" + col] = bh(df.loc[m, col].to_numpy())
    df["exuberancia_holm05"] = (df.bh_p_mc < 0.05) & (df.bh_p_wild < 0.05)   # BH por familia, ambos métodos
    df.to_csv(TAB / "gsadf_resultados.csv", index=False)
    for _, f in df.iterrows():
        reg("gsadf", f"gsadf_{f.territorio}_{f.medida}", "GSADF ADF(1) con intercepto, wild bootstrap", int(f["T"]),
            f"cv95 {f.cv95_mc:.2f}; episodios: {f.episodios_bsadf or 'ninguno'}; Holm {f.p_holm:.3f}; BH {f.bh_p_mc:.3f}",
            f.ini, f.fin, coef=f.gsadf, p=f.p_mc)
    ac = [float(np.corrcoef(np.diff(s.to_numpy())[1:], np.diff(s.to_numpy())[:-1])[0, 1]) for _, _, s in series]
    return {"df": df, "curvas": curvas, "ac_dy_media": float(np.mean(ac))}


# ------------------------------------------------------------------ figuras
def figuras(tri: dict, gs: dict) -> None:
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    pd.DataFrame(tri["precio"]).loc[2007:].plot(ax=ax[0], marker="o", ms=3)
    ax[0].set_title("Precio de compra, España (2015 = 100)")
    ax[0].axhline(100, color="grey", lw=0.5)
    pd.DataFrame(tri["alq"]).plot(ax=ax[1], marker="o", ms=3)
    pd.DataFrame(tri["cat"]).plot(ax=ax[1], marker="x", ms=3, ls="--")
    ax[1].set_title("Alquiler (2015 = 100); trazo discontinuo: Cataluña")
    fig.tight_layout()
    fig.savefig(OUT / "fig1_triangulacion.png", dpi=110)
    plt.close(fig)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for a, med in zip(ax, ["precio/alquiler: IPV / IPC alquiler", "precio/alquiler: valor tasado / IPC alquiler"]):
        fe, r = gs["curvas"][("Nacional", med)]
        x = np.arange(len(fe))[2:]
        a.plot(x, r["bsadf"], label="BSADF")
        a.plot(x, r["cv_path"], "--", label="vc 95 % (bootstrap)")
        a.set_xticks(x[::12])
        a.set_xticklabels([fe[i] for i in x[::12]], rotation=45, fontsize=7)
        a.set_title(med, fontsize=9)
        a.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "fig2_bsadf_nacional.png", dpi=110)
    plt.close(fig)


# ------------------------------------------------------------------ ficha
def ficha(tri: dict, gs: dict, ver: dict) -> dict:
    df = gs["df"]
    nac = df[df.territorio == "Nacional"]
    pa = nac[nac.medida.str.startswith("precio/alquiler")]
    n_pa_ok = int(pa.exuberancia_holm05.sum())
    ccaa = df[(df.territorio != "Nacional") & df.medida.str.startswith("precio/alquiler")]
    cnt = ccaa[ccaa.exuberancia_holm05].groupby("territorio").size()
    ambas = sorted(cnt[cnt == 2].index)
    v15, v21 = tri["precio_2015_2025"], tri["precio_2021_2025"]
    mag = (f"Precio de compra 2015-2025: +{100 * v15['rango_cum'][0]:.0f} % a +{100 * v15['rango_cum'][1]:.0f} % "
           f"según la fuente ({v15['n_fuentes']} fuentes); 2021-2025: +{100 * v21['rango_cum'][0]:.0f} % a "
           f"+{100 * v21['rango_cum'][1]:.0f} %. GSADF nacional precio/alquiler: exuberancia (BH 5 %, ambos métodos) en "
           f"{n_pa_ok} de {len(pa)} medidas; CCAA con exuberancia en ambas medidas: {len(ambas)} de 17; "
           f"episodios nacionales: {'; '.join(pa.episodios_bsadf)}.")
    ver_txt = "ANALIZADA, NO CONCLUYENTE"
    if n_pa_ok == 0 and not ambas:
        regla = ("El test no detecta exuberancia en las series nacionales de precio/alquiler; no identifica una burbuja y "
                 "la ausencia de rechazo tampoco la descarta. C4.")
    else:
        regla = ("Hay exuberancia estadística en el ratio precio/alquiler (episodios fechados con BSADF), pero un test de "
                 "exuberancia no separa una burbuja de cambios en los fundamentos (renta, tipos de interés, oferta) ni mide "
                 "la sobrevaloración. Con capa C4 el veredicto no puede ser RESPALDADA ni CONTRADICHA.")
    return {
        "id": "M7-V1", "tema": "Burbuja de precios",
        "enunciado": "Hay una burbuja en el precio de la vivienda en España.",
        "capa": "C4", "magnitud": mag,
        "intervalo": f"[{100 * v15['rango_cum'][0]:.0f}; {100 * v15['rango_cum'][1]:.0f}] % de variación 2015-2025",
        "cota": "—",
        "literatura": "Phillips, Shi y Yu (2015), GSADF: NO VERIFICADA (DOI y cuartil no comprobados sin red).",
        "veredicto": ver_txt, "regla": regla,
        "limites": ("Sobre-rechazo moderado con Δy autocorrelacionada (tamaño 12,7 % con phi=0,5, vc al 5 %). El test detecta comportamiento explosivo de la serie, no una burbuja: no identifica si el precio se "
                    "separa de los fundamentos. Ratios con índices rebasados (nivel de la ratio arbitrario); ADF con un rezago; "
                    "valores críticos por simulación de paseo aleatorio (principal) y wild bootstrap (499 réplicas; conservador si la muestra ya contiene tramos explosivos); muestra 2007-2026 corta para el ciclo. Precio/renta solo nacional; sin renta "
                    "trimestral por CCAA. Verificación con series simuladas: " + ("superada." if ver["ok"] else "NO superada.")),
        "evidencia": ["output/v4/M7/tablas/gsadf_resultados.csv", "output/v4/M7/tablas/variacion_precio.csv",
                      "data/processed (nacional_q_v2 vía holdout.load_full)"]}


def main() -> None:
    nq = holdout.load_full("nacional_q_v2", "M7")
    pan = pd.read_csv(RAIZ / "data/processed/panel_ccaa_q.csv")
    tri = triangulacion(nq, pan)
    ver = verificar_implementacion()
    gs = series_gsadf(nq, pan)
    figuras(tri, gs)
    tam = distorsion_tamano()
    fch = ficha(tri, gs, ver)
    (OUT / "fichas_verificador.json").write_text(json.dumps([fch], ensure_ascii=False, indent=1), encoding="utf-8")
    df = gs["df"]
    hechos = {"precio_2015_2025": {k: v for k, v in tri["precio_2015_2025"].items() if k != "disp"},
              "precio_2021_2025": tri["precio_2021_2025"], "n_ccaa_precio_c1": tri["n_ccaa_c1"],
              "n_ccaa_alquiler_c1_2015_2024": tri["n_ccaa_alq_c1"],
              "alquiler": {k: v for k, v in tri.items() if k.startswith("alq_")},
              "verificacion_gsadf": ver, "tamano_gsadf": tam, "autocorr_dy_media": gs["ac_dy_media"]}
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    nac_r = df[df.territorio == "Nacional"]
    res = {"rama": "M7", "pregunta": "¿Hay exuberancia de precios? Triangulación de precio de compra y alquiler y GSADF.",
           "capa": "C1 (triangulación) / C4 (GSADF)",
           "datos": "INE IPV, MIVAU valor tasado, Registradores, Notariado, IPC alquiler, SERPAVI, Incasòl; panel_ccaa_q; nacional_q_v2",
           "N": int(df["T"].max()), "metodo": f"GSADF (Phillips, Shi y Yu 2015), ADF(1), r0=0,01+1,8/sqrt(T), valores críticos por simulación (paseo aleatorio) y wild bootstrap, {NBOOT} réplicas cada uno, SEED {SEED}",
           "estimacion": {r.medida + " | " + r.territorio: round(float(r.gsadf), 3) for r in nac_r.itertuples()},
           "ic95": {r.medida + " | " + r.territorio: round(float(r.cv95_mc), 3) for r in nac_r.itertuples()},
           "p_ajustado": {r.medida + " | " + r.territorio: round(float(r.bh_p_mc), 4) for r in nac_r.itertuples()},
           "nivel_evidencia": "EXPLORATORIO (GSADF); DESCRIPTIVO/C1 (triangulación)",
           "diagnosticos": {"verificacion_simulada": ver, "tamano_ar1": tam, "autocorr_dy_media": gs["ac_dy_media"], "fdr": "BH por familia (nacional 6; CCAA 34), exuberancia si BH<0,05 con ambos métodos; Holm en p_holm (con 499 réplicas y 40 pruebas el mínimo Holm es 0,08)"},
           "fuera_muestra": {"modelo": "no aplica (test de exuberancia, sin predicción)", "rmse": None, "dm_vs_ar4": None},
           "notas": "Un test de exuberancia no identifica burbujas. INE e IPV de Notariado comparten fuente; BdE=MIVAU. SERPAVI es un stock y acaba en 2024."}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    REG.flush()
    print(df[["territorio", "medida", "gsadf", "cv95_mc", "p_mc", "p_wild", "p_holm", "episodios_bsadf"]].to_string())
    print(json.dumps(ver, default=float))


if __name__ == "__main__":
    main()

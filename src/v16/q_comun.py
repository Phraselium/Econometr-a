"""V16 fase 6 · utilidades comunes de Q1, Q2, Q7 y Q8 (grupo A). Solo entrenamiento; sin efectos al importar.

Lee SOLO data/processed/v16/entrenamiento (y data/raw para ECV y MIVAU, nacionales y sin muestra sellada de v6 por provincia).
Todo lo que sale de aquí es C4 y 'pendiente_sellada'. Sin lenguaje causal.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
ENTR = ROOT / "data" / "processed" / "v16" / "entrenamiento"
SEED = 20261010
CORTE = "2026-10-17"

# grandes ciudades (adenda V16, punto 14): provincias y municipios. Las islas no selladas: ninguna (Baleares y Canarias son v6).
GRANDES_PROV = {"08": "Barcelona", "46": "València", "41": "Sevilla", "29": "Málaga"}
GRANDES_MUN = {"08019": "Barcelona", "46250": "València", "41091": "Sevilla", "29067": "Málaga"}


def cargar(nombre: str, nivel: str | None = None, variables=None, cols=None) -> pd.DataFrame:
    d = pd.read_parquet(ENTR / f"{nombre}.parquet", columns=cols)
    if nivel is not None:
        d = d[d.nivel == nivel]
    if variables is not None:
        v = [variables] if isinstance(variables, str) else list(variables)
        d = d[d.variable.isin(v)]
    d = d.copy()
    d["territorio_codigo"] = d.territorio_codigo.astype(str)
    return d


def trimestral(d: pd.DataFrame) -> pd.DataFrame:
    """Filas trimestrales ('2019T3') con columna q (Period)."""
    x = d[d.periodo.astype(str).str.contains("T")].copy()
    x["q"] = pd.PeriodIndex([f"{v[:4]}Q{v[-1]}" for v in x.periodo.astype(str)], freq="Q")
    return x


def centroides_provincia():
    sys_path_fix()
    from src.v16.montecarlo import _comun_panel as C
    return dict(C.CENTROIDES), dict(C.PROV_CCAA)


def sys_path_fix():
    import sys
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------- regresión con efectos fijos (FWL, sin errores típicos)
def _demean(M: np.ndarray, u: np.ndarray, t: np.ndarray, it: int = 200) -> np.ndarray:
    M = M.astype(float).copy()
    ku, iu = np.unique(u, return_inverse=True)
    kt, it_ = np.unique(t, return_inverse=True)
    for _ in range(it):
        ant = M.copy()
        for g, n in ((iu, len(ku)), (it_, len(kt))):
            s = np.zeros((n, M.shape[1]))
            np.add.at(s, g, M)
            c = np.bincount(g, minlength=n)[:, None]
            M = M - (s / c)[g]
        if np.max(np.abs(M - ant)) < 1e-12:
            break
    return M


def twfe(df: pd.DataFrame, y: str, x: str, unidad: str, tiempo: str, controles=(), efectos="ut"):
    """OLS con efectos fijos de unidad y tiempo por demedición alternada.

    Devuelve dict con beta, r2 (dentro), r2_parcial de x, n. NO calcula errores típicos (herramienta NO APTA).
    efectos: 'ut' (unidad y tiempo) o 'u' (solo unidad).
    """
    cols = [y, x, *controles]
    d = df[[unidad, tiempo, *cols]].dropna()
    u = d[unidad].to_numpy()
    t = d[tiempo].to_numpy()
    M = d[cols].to_numpy(float)
    if efectos == "ut":
        M = _demean(M, u, t)
    else:
        ku, iu = np.unique(u, return_inverse=True)
        s = np.zeros((len(ku), M.shape[1]))
        np.add.at(s, iu, M)
        M = M - (s / np.bincount(iu)[:, None])[iu]
    Y = M[:, 0]
    X = M[:, 1:]
    b, *_ = np.linalg.lstsq(X, Y, rcond=None)
    res = Y - X @ b
    r2 = 1 - (res @ res) / (Y @ Y)
    # R² parcial de x dado los demás
    if X.shape[1] > 1:
        Z = X[:, 1:]
        bz, *_ = np.linalg.lstsq(Z, Y, rcond=None)
        ry = Y - Z @ bz
        bx, *_ = np.linalg.lstsq(Z, X[:, 0], rcond=None)
        rx = X[:, 0] - Z @ bx
    else:
        ry, rx = Y, X[:, 0]
    rp = float((rx @ ry) ** 2 / ((rx @ rx) * (ry @ ry))) if (rx @ rx) > 0 and (ry @ ry) > 0 else float("nan")
    return {"beta": float(b[0]), "r2": float(r2), "r2_parcial": rp, "n": int(len(d)),
            "sd_resid": float(np.sqrt(res @ res / max(len(d) - X.shape[1], 1))), "residuos": res, "indice": d.index}


# ---------------------------------------------------------------- sensibilidad (punto 14 de la adenda)
def oster_delta(b_corto, r2_corto, b_largo, r2_largo, mult=1.3):
    """δ tal que β=0 (Oster 2019) con Rmax = mult*R²_largo (acotado a 1). δ<1 → frágil."""
    rmax = min(1.0, mult * r2_largo)
    den = (b_corto - b_largo) * (r2_largo - r2_corto)
    if den == 0 or not np.isfinite(den):
        return {"delta": None, "rmax": rmax, "nota": "denominador cero: el control no mueve la estimación"}
    return {"delta": float(b_largo * (rmax - r2_largo) / den), "rmax": float(rmax)}


def cinelli_hazlett_rv(r2_parcial):
    """Valor de robustez RV_{q=1} a partir del R² parcial (f = sqrt(R²p/(1-R²p)))."""
    if not np.isfinite(r2_parcial) or r2_parcial >= 1:
        return None
    f = np.sqrt(r2_parcial / (1 - r2_parcial))
    return float(0.5 * (np.sqrt(f ** 4 + 4 * f ** 2) - f ** 2))


def e_value_d(beta_sd, sd_resid):
    """E-value (VanderWeele-Ding) con d = β/σ_resid y RR ≈ exp(0,91 d). Puntual; sin IC."""
    d = abs(beta_sd) / sd_resid if sd_resid > 0 else np.nan
    rr = np.exp(0.91 * d)
    return float(rr + np.sqrt(rr * (rr - 1))) if np.isfinite(rr) and rr >= 1 else None


def moran(v: np.ndarray, coords: np.ndarray, B: int = 999, seed: int = SEED):
    """I de Moran con pesos 1/distancia (km, normalizados por fila) y permutación (diagnóstico, no contraste de diseño)."""
    la, lo = np.deg2rad(coords[:, 0]), np.deg2rad(coords[:, 1])
    dla = la[:, None] - la[None, :]
    dlo = lo[:, None] - lo[None, :]
    a = np.sin(dla / 2) ** 2 + np.cos(la)[:, None] * np.cos(la)[None, :] * np.sin(dlo / 2) ** 2
    dist = 2 * 6371 * np.arcsin(np.sqrt(a))
    with np.errstate(divide="ignore"):
        W = np.where(dist > 0, 1.0 / dist, 0.0)
    W = W / W.sum(1, keepdims=True)
    z = v - v.mean()

    def I(zz):
        return float(len(zz) / W.sum() * (zz @ W @ zz) / (zz @ zz))
    i0 = I(z)
    rng = np.random.default_rng(seed)
    perm = np.array([I(rng.permutation(z)) for _ in range(B)])
    return {"I": i0, "E_I": -1 / (len(v) - 1), "p_permutacion_diagnostico": float((1 + (perm >= i0).sum()) / (B + 1)), "n": len(v)}


def breusch_pagan(res, X):
    from statsmodels.stats.diagnostic import het_breuschpagan
    Xc = np.column_stack([np.ones(len(res)), X])
    lm, p, f, pf = het_breuschpagan(res, Xc)
    return {"LM": float(lm), "p_diagnostico": float(p)}


# ---------------------------------------------------------------- BLP / GATES descriptivo
def blp_gates(y: np.ndarray, d: np.ndarray, X: np.ndarray, nombres, reps: int = 50, seed: int = SEED):
    """BLP lineal y GATES descriptivos (NO APTO: solo puntuales, sin p-valor ni IC).

    y: cambio del resultado post−pre; d: exposición estandarizada; X: moderadores estandarizados.
    CATE proxy: bosque aleatorio de y sobre (X, d, d*X) entrenado en la mitad auxiliar, con pendiente por derivada finita en d.
    BLP: y = a + b1*d + b2*d*(s−mean s) con s = proxy en la mitad principal. GATES: pendiente de y sobre d por cuartil de s.
    Se repite `reps` veces y se reporta la mediana.
    """
    from sklearn.ensemble import RandomForestRegressor
    rng = np.random.default_rng(seed)
    n = len(y)
    out_b, out_g, out_lin = [], [], []
    for r in range(reps):
        idx = rng.permutation(n)
        aux, main = idx[: n // 2], idx[n // 2:]
        feat = lambda D, XX: np.column_stack([XX, D, XX * D[:, None]])
        rf = RandomForestRegressor(n_estimators=100, min_samples_leaf=3, random_state=int(rng.integers(1e9)))
        rf.fit(feat(d[aux], X[aux]), y[aux])
        h = 0.5
        s = (rf.predict(feat(d[main] + h, X[main])) - rf.predict(feat(d[main] - h, X[main]))) / (2 * h)
        dm, ym, sm = d[main], y[main], s
        Z = np.column_stack([np.ones(len(main)), dm, dm * (sm - sm.mean())])
        b, *_ = np.linalg.lstsq(Z, ym, rcond=None)
        out_b.append(b[1:])
        q = np.searchsorted(np.quantile(sm, [0.25, 0.5, 0.75]), sm)
        g = []
        for k in range(4):
            m = q == k
            if m.sum() > 3 and np.var(dm[m]) > 0:
                zz = np.column_stack([np.ones(m.sum()), dm[m]])
                bk, *_ = np.linalg.lstsq(zz, ym[m], rcond=None)
                g.append(bk[1])
            else:
                g.append(np.nan)
        out_g.append(g)
        # BLP lineal directo con moderadores
        ZZ = np.column_stack([np.ones(n), d, X * d[:, None], X])
        bl, *_ = np.linalg.lstsq(ZZ, y, rcond=None)
        out_lin.append(bl[2:2 + X.shape[1]])
    ob, og, ol = np.array(out_b), np.array(out_g), np.array(out_lin)
    return {"ATE_beta1_mediana": float(np.median(ob[:, 0])), "heterogeneidad_beta2_mediana": float(np.median(ob[:, 1])),
            "GATES_pendiente_por_cuartil_mediana": [None if np.all(np.isnan(og[:, k])) else float(np.nanmedian(og[:, k])) for k in range(4)],
            "GATES_cuartil4_menos_cuartil1": float(np.nanmedian(og[:, 3] - og[:, 0])),
            "interaccion_lineal_exposicion_x_moderador": {nm: float(np.median(ol[:, j])) for j, nm in enumerate(nombres)},
            "reps": reps, "n": n, "nota": "descriptivo; herramienta NO APTA (veredictos.csv): sin p-valor ni IC; subgrupos descriptivos C4"}


# ---------------------------------------------------------------- salida
def jdump(o, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

    def conv(x):
        if isinstance(x, (np.floating, np.integer)):
            return x.item()
        if isinstance(x, np.ndarray):
            return x.tolist()
        if isinstance(x, (pd.Timestamp, pd.Period)):
            return str(x)
        raise TypeError(type(x))
    path.write_text(json.dumps(o, ensure_ascii=False, indent=1, default=conv), encoding="utf-8")


def registro(filas: list[dict], path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    cols = ["id", "pregunta", "rol", "especificacion", "muestra", "n", "estimacion", "unidad", "inferencia", "nota"]
    pd.DataFrame(filas).reindex(columns=cols).to_csv(path, index=False)


def covariables_provincia(prov: list[str]) -> pd.DataFrame:
    """Moderadores/controles provinciales fijos en 2019 (antes de cualquier tratamiento): renta ADRH, población, cuota de extranjeros, obra nueva per cápita."""
    rp = cargar("renta_parque", "provincia", "ine_adrh_renta_neta_media_hogar_eur")
    renta = rp[rp.periodo.astype(str) == "2019"].set_index("territorio_codigo").valor
    bp = cargar("base_poblacion", "provincia", ["pob_total", "pob_extranj"])
    pob = bp[bp.periodo.astype(str) == "2019"].pivot_table(index="territorio_codigo", columns="variable", values="valor")
    bpr = cargar("base_precio", "provincia", "terminadas_anual_tabla")
    ter = bpr[bpr.periodo.astype(str) == "2019"].set_index("territorio_codigo").valor
    out = pd.DataFrame({"renta": renta, "pob": pob["pob_total"], "cuota_extranj": pob["pob_extranj"] / pob["pob_total"],
                        "obra_pc": ter / pob["pob_total"] * 1000})
    out["ln_pob"] = np.log(out.pob)
    out["ln_renta"] = np.log(out.renta)
    return out.reindex(prov)


def vut_provincia(prov: list[str], periodo: str = "2020-08") -> pd.Series:
    t = cargar("alquiler_turismo", "provincia")
    t = t[t.variable.str.startswith("ine_vte_porcentaje") & (t.periodo.astype(str) == periodo)]
    return t.set_index("territorio_codigo").valor.reindex(prov)


def ols_corte(y: np.ndarray, x: np.ndarray, Z: np.ndarray | None = None):
    """MCO de corte transversal: beta de x, R², R² parcial de x, σ_resid y residuos (sin errores típicos)."""
    n = len(y)
    A = np.column_stack([np.ones(n), x] + ([Z] if Z is not None else []))
    b, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ b
    r2 = 1 - (res @ res) / (((y - y.mean()) ** 2).sum())
    B = np.column_stack([np.ones(n)] + ([Z] if Z is not None else []))
    ry = y - B @ np.linalg.lstsq(B, y, rcond=None)[0]
    rx = x - B @ np.linalg.lstsq(B, x, rcond=None)[0]
    rp = float((rx @ ry) ** 2 / ((rx @ rx) * (ry @ ry))) if (rx @ rx) > 0 else float("nan")
    return {"beta": float(b[1]), "r2": float(r2), "r2_parcial": rp, "sd_resid": float(np.sqrt(res @ res / max(n - A.shape[1], 1))),
            "residuos": res, "n": n}


def sensibilidad(corto: dict, largo: dict, beta_sd: float | None = None) -> dict:
    """Oster (δ, β=0, Rmax=1,3 R²), Cinelli-Hazlett (RV_q=1) y E-value, todo puntual."""
    return {"oster": oster_delta(corto["beta"], corto["r2"], largo["beta"], largo["r2"]),
            "cinelli_hazlett_RV_q1": cinelli_hazlett_rv(largo["r2_parcial"]),
            "cinelli_hazlett_frágil_si_RV_menor_0_05": (cinelli_hazlett_rv(largo["r2_parcial"]) or 0) < 0.05,
            "e_value_puntual": e_value_d(largo["beta"] if beta_sd is None else beta_sd, largo["sd_resid"])}

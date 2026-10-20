"""V18 · fase 4 · piezas comunes de E2 (topes al alquiler) y E8 (ITP): lectura con sellado, regresión de diferencias en diferencias con
efectos fijos, inferencia (CR1, bootstrap de Webb con el nulo impuesto, aleatorización, Conley), pruebas de estudio de eventos
(pretendencias, potencia de Roth, TOST), efecto mínimo detectable por Monte Carlo, clasificación I1-I8 revisados y escritura de salidas.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18 (docs/v18/plan_replicacion.md + plan_replicacion_adenda.md).
SEED = 20261010; sin red. Cada lectura de datos pasa por sellado.filtrar (src/v18/sellado.py) y, además, por
holdout.excluir_sellados_v6(): nunca se abre data/sealed ni se ejecuta evaluate_*.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v18"))
import holdout  # noqa: E402
import sellado  # noqa: E402
from econ_utils import Registry, holm  # noqa: E402
from herramientas import aleatorizacion as ALE  # noqa: E402
from herramientas import honest_did as HON  # noqa: E402
from herramientas.conley import nucleo_bartlett  # noqa: E402

ALCANCE_TERRITORIAL = "lectura con sellado.filtrar y holdout.excluir_sellados_v6"
SEMILLA = 20261010
HECHOS = RAIZ / "data" / "base" / "hechos.parquet"
GEO = RAIZ / "data" / "base" / "geo" / "municipios.parquet"
MC = RAIZ / "output" / "v18" / "montecarlo"
WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])
ROTULO = "análisis V18; capa C4; pre-registro interno plan-replicacion-v18"
PROHIBIDAS = ("causa", "provoca", "debido a", "se debe a", "gracias a", "efecto causal", "impacto causal", "causal")


# ------------------------------------------------------------------------------------------------ lectura
def leer_hechos(variable: str, nivel: str, frecuencia: str, extra_cols: tuple = ()) -> pd.DataFrame:
    """Serie de la base con el filtro de sellado de V18 (tope temporal, unidades v6/V15/V16) y el filtro v6 de holdout."""
    cols = ["territorio_codigo", "periodo", "valor", "desagregacion", "edicion", "muestra_sellada_v6", *extra_cols]
    df = pd.read_parquet(HECHOS, columns=cols, filters=[("variable", "==", variable), ("nivel", "==", nivel), ("frecuencia", "==", frecuencia)])
    return filtrar(df, "territorio_codigo", nivel, "periodo", variable, frecuencia)


def filtrar(df: pd.DataFrame, col_cod: str, nivel: str, col_per: str, variable: str, frecuencia: str) -> pd.DataFrame:
    """sellado.filtrar + holdout.excluir_sellados_v6 (idempotente) sobre cualquier tabla con código INE."""
    df = df.copy()
    df[col_cod] = df[col_cod].astype(str)
    df[col_per] = df[col_per].astype(str)
    out = sellado.filtrar(df, col_cod, nivel, col_per, variable, frecuencia)
    if nivel in ("ccaa", "provincia", "municipio", "distrito", "seccion"):
        out = holdout.excluir_sellados_v6(out, col_cod, nivel)
    return out


def ancho(df: pd.DataFrame, periodos: list[str], col_cod: str = "territorio_codigo", col_val: str = "valor") -> pd.DataFrame:
    w = df[df["periodo"].isin(periodos)].pivot_table(index=col_cod, columns="periodo", values=col_val, aggfunc="first")
    return w.reindex(columns=periodos)


def trimestres(ini: str, fin: str) -> list[str]:
    a, b = int(ini[:4]) * 4 + int(ini[-1]) - 1, int(fin[:4]) * 4 + int(fin[-1]) - 1
    return [f"{i // 4}T{i % 4 + 1}" for i in range(a, b + 1)]


def indice_t(p: str) -> int:
    return int(p[:4]) * 4 + int(p[-1]) - 1


# ------------------------------------------------------------------------------------------------ regresión
class Modelo:
    """y = beta·d + extra·gamma + efectos fijos de unidad y de periodo (+ pesos de unidad). Residualiza por SVD (panel no necesariamente
    equilibrado); clusters contiguos para sumar puntuaciones. Un solo coeficiente de interés (d); el resto va como molestia."""

    def __init__(self, y, d, unit, time, extra=None, w=None, cluster=None):
        y, d = np.asarray(y, float), np.asarray(d, float)
        n = len(y)
        cl = np.asarray(unit if cluster is None else cluster)
        orden = np.argsort(cl, kind="stable")
        self.orden = orden
        self.n = n
        sw = np.ones(n) if w is None else np.sqrt(np.asarray(w, float))
        sw = sw[orden]
        u = np.asarray(unit)[orden]
        t = np.asarray(time)[orden]
        self.cl_ord = cl[orden]
        _, self.inicio, self.tam = np.unique(self.cl_ord, return_index=True, return_counts=True)
        self.G = len(self.tam)
        nu, nt = int(u.max()) + 1, int(t.max()) + 1
        cols = [(u[:, None] == np.arange(nu)[None, :]).astype(float), (t[:, None] == np.arange(1, nt)[None, :]).astype(float)]
        if extra is not None:
            ex = np.asarray(extra, float)
            ex = ex.reshape(n, -1)[orden]
            cols.append(ex)
        W = np.hstack(cols) * sw[:, None]
        U, s, _ = np.linalg.svd(W, full_matrices=False)
        self.Q = U[:, s > s[0] * 1e-9]
        self.k = self.Q.shape[1] + 1
        self.sw = sw
        self.unit_ord = u
        self.ytil = self._m(sw * y[orden])
        self.dtil = self._m(sw * d[orden])
        self.dd = float(self.dtil @ self.dtil)
        self.beta = float(self.dtil @ self.ytil / self.dd) if self.dd > 1e-12 else float("nan")
        self.e = self.ytil - self.beta * self.dtil
        self.c = self.G / (self.G - 1) * (n - 1) / max(n - self.k, 1)
        s_g = np.add.reduceat(self.dtil * self.e, self.inicio)
        self.se = float(np.sqrt(self.c * (s_g ** 2).sum()) / self.dd) if self.dd > 1e-12 else float("nan")
        self.t = self.beta / self.se if self.se > 0 else float("nan")
        self.p_t = float(2 * stats.t.sf(abs(self.t), self.G - 1)) if np.isfinite(self.t) else float("nan")
        q = stats.t.ppf(0.975, self.G - 1)
        self.ic_t = (self.beta - q * self.se, self.beta + q * self.se)

    def _m(self, z):
        return z - self.Q @ (self.Q.T @ z)

    def webb_p(self, beta0: float, B: int, rng: np.random.Generator, lote: int = 1000, V: np.ndarray | None = None) -> float:
        """Wild cluster bootstrap-t de Webb con el nulo beta = beta0 impuesto (WCR); EE de agrupación recalculado en cada réplica."""
        yr = self.ytil - beta0 * self.dtil
        cuenta, hechas = 0, 0
        t_obs = abs((self.beta - beta0) / self.se)
        while hechas < B:
            b = min(lote, B - hechas)
            v = WEBB[rng.integers(0, 6, size=(self.G, b))] if V is None else V[:, hechas:hechas + b]
            z = np.repeat(v, self.tam, axis=0) * yr[:, None]
            bs = (self.dtil @ z) / self.dd
            e = self._m(z) - bs[None, :] * self.dtil[:, None]
            s = np.add.reduceat(self.dtil[:, None] * e, self.inicio, axis=0)
            se_b = np.sqrt(self.c * (s ** 2).sum(0)) / self.dd
            cuenta += int(np.sum(np.abs(bs / np.maximum(se_b, 1e-300)) >= t_obs - 1e-12))
            hechas += b
        return (1 + cuenta) / (B + 1)

    def webb_ic(self, B: int = 1999, rng: np.random.Generator | None = None, nivel: float = 0.05) -> tuple[float, float]:
        """IC por inversión del contraste de Webb (mismos pesos en todas las evaluaciones)."""
        rng = rng or np.random.default_rng(SEMILLA)
        V = WEBB[rng.integers(0, 6, size=(self.G, B))]
        return ic_por_p(lambda b0: self.webb_p(b0, B, rng, V=V), self.beta, self.se, nivel)

    def puntuaciones_unidad(self) -> tuple[np.ndarray, np.ndarray]:
        """Puntuaciones d̃·e sumadas por unidad (identificador de unidad ordenado) para Conley."""
        u = self.unit_ord
        s = np.bincount(u, weights=self.dtil * self.e, minlength=int(u.max()) + 1)
        return s, np.arange(len(s))

    def conley(self, coords_km: np.ndarray, corte_km: float) -> float:
        s, _ = self.puntuaciones_unidad()
        K = nucleo_bartlett(coords_km, corte_km)
        v = float(s @ (K @ s))
        return float(np.sqrt(max(v, 0.0) * self.c) / self.dd)


def ic_por_p(pfun, centro: float, escala: float, nivel: float = 0.05, it: int = 18) -> tuple[float, float]:
    """Extremos del conjunto {theta0: p(theta0) >= nivel} por bisección a cada lado del centro."""
    out = []
    for signo in (-1.0, 1.0):
        dentro, fuera = centro, centro + signo * 6 * escala
        k = 0
        while pfun(fuera) >= nivel and k < 6:
            dentro, fuera = fuera, fuera + signo * 6 * escala
            k += 1
        for _ in range(it):
            m = (dentro + fuera) / 2
            dentro, fuera = (m, fuera) if pfun(m) >= nivel else (dentro, m)
        out.append((dentro + fuera) / 2)
    return float(out[0]), float(out[1])


def evento_multi(y, D, unit, time, extra=None, w=None, cluster=None) -> dict:
    """Regresión con varias columnas de interés (estudio de eventos): devuelve b, V (CR1 por cluster), G, k. `extra` va como molestia."""
    D = np.asarray(D, float)
    K = D.shape[1]
    M = Modelo(y, D[:, 0], unit, time, extra=extra, w=w, cluster=cluster)
    Dm = np.column_stack([M._m(M.sw * D[M.orden, j]) for j in range(K)])
    A = Dm.T @ Dm
    Ainv = np.linalg.pinv(A)
    coef = Ainv @ (Dm.T @ M.ytil)
    e = M.ytil - Dm @ coef
    sc = np.add.reduceat(Dm * e[:, None], M.inicio, axis=0)
    c = M.G / (M.G - 1) * (M.n - 1) / max(M.n - (M.Q.shape[1] + K), 1)
    V = c * Ainv @ (sc.T @ sc) @ Ainv
    return {"b": coef, "V": V, "G": M.G, "k": M.Q.shape[1] + K}


# ------------------------------------------------------------------------------------------------ diagnósticos
def wald_conjunto(b: np.ndarray, V: np.ndarray, G: int) -> tuple[float, float]:
    """Contraste conjunto b = 0 con la covarianza agrupada; p con la distribución F(k, G−1) (aproximación de Hotelling)."""
    k = len(b)
    W = float(b @ np.linalg.pinv(V) @ b)
    return W, float(stats.f.sf(W / k, k, max(G - 1, 1)))


def roth_pendiente(V: np.ndarray, ell: np.ndarray, potencia: float = 0.8, alfa: float = 0.05) -> float:
    """Pendiente lineal previa detectable (Roth, 2022) con la potencia dada por el contraste conjunto de los adelantos: δ tal que
    P(χ²_k(δ² ℓ'V⁻¹ℓ) > crítico) = potencia."""
    k = len(ell)
    crit = stats.chi2.ppf(1 - alfa, k)
    lo, hi = 0.0, 100.0
    for _ in range(80):
        m = (lo + hi) / 2
        if stats.ncx2.sf(crit, k, m) < potencia:
            lo = m
        else:
            hi = m
    lam = (lo + hi) / 2
    q = float(ell @ np.linalg.pinv(V) @ ell)
    return float(np.sqrt(lam / q))


def tost(beta: float, se: float, delta: float, gl: float) -> dict:
    """Equivalencia por TOST al 5 %: el IC al 90 % está dentro de ±δ."""
    q = stats.t.ppf(0.95, gl)
    lo, hi = beta - q * se, beta + q * se
    return {"ic90": (float(lo), float(hi)), "delta": delta, "equivalente": bool(lo > -delta and hi < delta)}


def p_corr(p: float, tamano_mc: float | None) -> float:
    """p con el valor crítico corregido por el tamaño del Monte Carlo (adenda 1.12): p × tamaño/0,05 si el tamaño cae fuera de [0,04; 0,06]."""
    if tamano_mc is None or 0.04 <= tamano_mc <= 0.06:
        return float(p)
    return float(min(1.0, p * tamano_mc / 0.05))


def banda_mc(tamano: float) -> str:
    if 0.04 <= tamano <= 0.06:
        return "apta"
    if tamano > 0.15 or tamano < 0.02:
        return "no fiable"
    return "con valor crítico corregido"


def honest_ic(Y: np.ndarray, tratado: np.ndarray, cluster: np.ndarray, ref: int, pre: list[int], post: list[int], Mbar: float,
              hotelling: bool = True) -> dict:
    """IC de Honest DiD (magnitudes relativas) con la covarianza agrupada al nivel del tratamiento (+ factor de Hotelling)."""
    b, V, info = HON.evento_agrupado(Y, tratado, cluster, ref, pre, post)
    G, k = info["G"], info["k"]
    if hotelling and G > k + 1:
        V = V * (G - 1) / (G - k)
    lo, hi = HON.ic(b, V, len(pre), len(post), Mbar)
    return {"Mbar": Mbar, "ic95": (lo, hi), "excluye_cero": bool(np.isfinite(lo) and (lo > 0 or hi < 0)), "G": G, "k": k, "rango_V": info["rango_V"]}


def moran_i(valores, coords_km: np.ndarray, k: int = 5, B: int = 999, semilla: int = SEMILLA) -> dict:
    """I de Moran de los residuos medios por unidad con pesos de los k vecinos más próximos (estandarizados por filas); p por permutación (unilateral, autocorrelación
    positiva) y bilateral. Diagnóstico espacial del pre-registro (no es una inferencia)."""
    from scipy.spatial import cKDTree
    v = np.asarray(valores, float)
    n = len(v)
    z = v - v.mean()
    kk = min(k, n - 1)
    idx = cKDTree(coords_km).query(coords_km, k=kk + 1)[1][:, 1:]
    W = np.zeros((n, n))
    W[np.repeat(np.arange(n), kk), idx.ravel()] = 1.0 / kk
    den = float(z @ z)
    i0 = float(z @ W @ z / den)
    rng = np.random.default_rng(semilla)
    ip = np.array([(lambda zz: zz @ W @ zz / den)(rng.permutation(z)) for _ in range(B)])
    return {"I": i0, "E_I": -1.0 / (n - 1), "p_unilateral": float((1 + np.sum(ip >= i0)) / (B + 1)),
            "p_bilateral": float((1 + np.sum(np.abs(ip - ip.mean()) >= abs(i0 - ip.mean()))) / (B + 1)), "n": n, "k": kk}


def residuo_medio_por_unidad(m: "Modelo") -> np.ndarray:
    """Residuo medio por unidad del modelo (orden de unidad 0..N−1)."""
    u = m.unit_ord
    return np.bincount(u, weights=m.e / np.where(m.sw == 0, 1.0, m.sw)) / np.bincount(u)


# ------------------------------------------------------------------------------------------------ efecto mínimo detectable
def mde_desde_placebos(placebos: np.ndarray, rng_semilla: int = SEMILLA, potencia: float = 0.8) -> dict:
    """MDE al 80 % de potencia, bilateral al 5 %: valor crítico = cuantil 95 % de |β̂| entre las reasignaciones placebo del tratamiento
    (con la variación real de la asignación); potencia(τ) = P(|β̂_placebo + τ| > crítico)."""
    p = np.asarray(placebos, float)
    p = p[np.isfinite(p)]
    crit = float(np.quantile(np.abs(p), 0.95))
    sd = float(p.std(ddof=1))
    grid = np.linspace(0, 8 * max(sd, 1e-9) + crit, 4001)
    pot = np.array([np.mean(np.abs(p + t) > crit) for t in grid])
    i = int(np.argmax(pot >= potencia)) if (pot >= potencia).any() else len(grid) - 1
    return {"mde80": float(grid[i]), "sd_placebo": sd, "critico_95": crit, "R": int(len(p)), "tamano_nominal": float(np.mean(np.abs(p) > crit))}


# ------------------------------------------------------------------------------------------------ Monte Carlo de V18 (bandas)
def tamano_mc(herramienta: str, escenario: str, variante: str) -> float | None:
    f = MC / herramienta / "tabla.csv"
    if not f.exists():
        return None
    t = pd.read_csv(f)
    s = t[(t["escenario"] == escenario) & (t["variante"] == variante)]
    return float(s["tamano_5pct"].iloc[0]) if len(s) else None


# ------------------------------------------------------------------------------------------------ clasificación
ORDEN = {"ASOCIACIÓN": 0, "SUGESTIVO": 1, "IDENTIFICADO": 2}


def clasificar(i: dict) -> dict:
    """Clasificación V18 con I1-I8 revisados (adenda 1.1 y 1.2). I8 (réplica ciega) queda pendiente: se rotula.
    Claves: estimable, coprincipal, p_holm, coef, ic90, delta, pretend_p, roth_ok, placebo_fecha, placebo_resultado, robustez,
    inferencia_banda, topes (lista), debiles_extra (lista), nulo_sin_sugestivo (K7: un no significativo sin I1-I5 es ASOCIACIÓN, no SUGESTIVO)."""
    if not i.get("estimable", True):
        return {"clase": "NO ESTIMABLE", "razones": [i.get("motivo_no_estimable", "")], "debiles": [], "decisivos": [], "topes": []}
    if i.get("coprincipal"):
        return {"clase": "no se clasifica", "razones": ["coprincipal P (adenda 1.6)"], "debiles": [], "decisivos": [], "topes": []}
    dec, deb = [], list(i.get("debiles_extra", []))
    pp = i.get("pretend_p")
    if pp is not None and np.isfinite(pp):
        if pp < 0.01:
            dec.append(f"pretendencias p = {pp:.3f} < 0,01")
        elif pp <= 0.10:
            deb.append(f"pretendencias p = {pp:.3f}")
    if i.get("roth_ok") is False:
        deb.append("potencia de Roth: el sesgo implicado por la pendiente detectable supera la mitad de |referencia|")
    pf = i.get("placebo_fecha")
    if pf is not None and np.isfinite(pf.get("p", np.nan)):
        if pf["p"] < 0.05 and pf.get("mismo_signo") and abs(pf["coef"]) >= 0.5 * abs(i["coef"]):
            dec.append("placebo de fecha significativo, del mismo signo y de al menos la mitad del efecto")
        elif pf["p"] <= 0.10:
            deb.append(f"placebo de fecha p = {pf['p']:.3f}")
    elif pf is None:
        deb.append("placebo de fecha no realizable")
    po = i.get("placebo_resultado")
    if po in (None, "no disponible"):
        deb.append("placebo de resultado sin dato en el repositorio")
    elif po == "falla":
        deb.append("placebo de resultado con p <= 0,10")
    rb = i.get("robustez") or {}
    if rb.get("cambio_signo"):
        dec.append(i.get("texto_cambio_signo", "cambio de signo en una prueba de robustez"))
    if rb.get("frac_mismo_signo") is not None and rb["frac_mismo_signo"] < 0.8:
        deb.append(f"mismo signo en {rb['frac_mismo_signo']:.0%} de las variantes enumeradas (< 80 %)")
    if rb.get("solape_ic") is False:
        deb.append("IC95 de alguna robustez no solapa con el principal")
    if i.get("inferencia_banda") == "no fiable":
        dec.append("inferencia principal «no fiable» (Monte Carlo) sin alternativa apta")
    ph = i.get("p_holm")
    topes = list(i.get("topes", []))
    if dec:
        return {"clase": "ASOCIACIÓN", "razones": dec, "debiles": deb, "decisivos": dec, "topes": topes}
    valido = not deb
    sig = ph is not None and ph < 0.05
    t = i.get("tost") or {}
    if sig:
        clase = "IDENTIFICADO" if (valido and not topes) else "SUGESTIVO"
    elif ph is not None and ph < 0.10:
        deb.append(f"p tras Holm = {ph:.3f} entre 0,05 y 0,10")
        clase = "SUGESTIVO"
    else:
        if t.get("equivalente"):
            clase = "IDENTIFICADO (efecto nulo acotado)" if (valido and not topes) else "SUGESTIVO (efecto nulo acotado)"
        elif valido:
            clase = "NO CONCLUYENTE (sin potencia)"
        elif i.get("nulo_sin_sugestivo"):
            # K7 (B6, ronda 1): no existe «SUGESTIVO sin significación»; un resultado no significativo que no supera I1-I5 es ASOCIACIÓN
            clase = "ASOCIACIÓN"
        else:
            clase = "SUGESTIVO"
    return {"clase": clase, "razones": deb + topes, "debiles": deb, "decisivos": [], "topes": topes}


def clase_corta(clase: str) -> str:
    """Valor admitido por check_v18 (CLASES): las etiquetas con paréntesis conservan su raíz."""
    for raiz in ("IDENTIFICADO", "SUGESTIVO", "NO CONCLUYENTE", "ASOCIACIÓN", "NO ESTIMABLE"):
        if clase.startswith(raiz):
            return raiz
    return clase


# ------------------------------------------------------------------------------------------------ salidas
def sin_palabras_prohibidas(txt: str) -> str:
    low = txt.lower()
    for w in PROHIBIDAS:
        if w in low:
            raise ValueError(f"lenguaje no admitido en una cifra V18: {w!r} en {txt[:80]!r}")
    return txt


def hecho(id_, indicador, valor, minimo, maximo, unidad, periodo, cobertura, fuentes, clase, nota) -> dict:
    sin_palabras_prohibidas(f"{indicador} {nota}")
    f = lambda x: None if x is None or (isinstance(x, float) and not np.isfinite(x)) else round(float(x), 6)  # noqa: E731
    return {"id": id_, "indicador": indicador, "valor": f(valor), "min": f(minimo), "max": f(maximo), "unidad": unidad, "periodo": periodo,
            "cobertura": cobertura, "fuentes": fuentes, "capa": "C4", "clasificacion_v18": clase_corta(clase), "nota": nota}


def volcar_json(ruta: Path, obj) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=_json), encoding="utf-8")


def _json(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (set, tuple)):
        return list(o)
    return str(o)


def holm_familia(pvals: dict) -> dict:
    """Holm (econ_utils.holm) sobre la familia; vacía devuelve {}."""
    return holm(pvals) if pvals else {}


__all__ = ["Registry", "holm", "math"]

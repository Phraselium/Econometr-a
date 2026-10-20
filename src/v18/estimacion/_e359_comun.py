"""V18 · fase 4 · piezas comunes de E3 (inmigración), E5 (oferta y suelo) y E9 (no residentes).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18 (docs/v18/plan_replicacion.md + plan_replicacion_adenda.md). SEED = 20261010.
Sin red: las fuentes nuevas se bajan antes con e359_adquisicion.py. Cada lectura con detalle territorial o temporal pasa por sellado.filtrar
(src/v18/sellado.py) y, además, por holdout.excluir_sellados_v6(); nunca se abre data/sealed ni se ejecuta evaluate_*.

Contenido:
- lectura con sellado (manifiesto de V18 más las tres series de Eurostat bajadas después de la etiqueta, regla 1.4 e);
- DisenoIV: IV con un regresor endógeno e instrumento único sobre panel de primeras diferencias con efectos absorbidos y pesos; inferencia
  por provincia: 2SLS con t(G-1), F efectivo de Montiel Olea-Pflueger, Anderson-Rubin exacto agrupado (iv_debil, APTO), Webb-AR (bootstrap
  de Webb con el nulo impuesto sobre la forma reducida, 9.999 réplicas) y su inversión;
- efecto mínimo detectable por Monte Carlo (adenda 1.3), BHJ y pesos de Rotemberg, Benjamini-Yekutieli, clasificación I1-I8 revisados;
- salidas: hecho(), volcar_json().
"""
from __future__ import annotations

import copy
import json
import math
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[3]
for _p in (RAIZ / "src", RAIZ / "src" / "v18", RAIZ / "src" / "v18" / "reproduccion"):
    sys.path.insert(0, str(_p))
import holdout  # noqa: E402
import sellado  # noqa: E402
from econ_utils import Registry, holm  # noqa: E402,F401
from herr18 import iv_debil as IVD  # noqa: E402
import bhj_lib  # noqa: E402

warnings.filterwarnings("ignore", message="Could not infer format")
ALCANCE_TERRITORIAL = "lectura con sellado.filtrar y holdout.excluir_sellados_v6"
SEMILLA = 20261010
HECHOS = RAIZ / "data" / "base" / "hechos.parquet"
RAW = RAIZ / "data" / "raw"
EURO = RAW / "v18" / "eurostat_e359"
OUT = RAIZ / "output" / "v18" / "estimacion"
MC = RAIZ / "output" / "v18" / "montecarlo"
ROTULO = "análisis V18; capa C4; pre-registro interno plan-replicacion-v18"
WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])
PROHIBIDAS = ("causa", "provoca", "debido a", "se debe a", "gracias a", "efecto causal", "impacto causal", "causal")

# ------------------------------------------------------------------------------------------------ geografía fija (antes de estimar)
SELLADAS_V6 = {"07", "22", "26", "28", "30", "31", "33", "35", "38", "44", "50"}
NUTS3_A_PROV = {
    "ES111": "15", "ES112": "27", "ES113": "32", "ES114": "36", "ES120": "33", "ES130": "39", "ES211": "01", "ES212": "20", "ES213": "48",
    "ES220": "31", "ES230": "26", "ES241": "22", "ES242": "44", "ES243": "50", "ES300": "28", "ES411": "05", "ES412": "09", "ES413": "24",
    "ES414": "34", "ES415": "37", "ES416": "40", "ES417": "42", "ES418": "47", "ES419": "49", "ES421": "02", "ES422": "13", "ES423": "16",
    "ES424": "19", "ES425": "45", "ES431": "06", "ES432": "10", "ES511": "08", "ES512": "17", "ES513": "25", "ES514": "43", "ES521": "03",
    "ES522": "12", "ES523": "46", "ES530": "07", "ES611": "04", "ES612": "11", "ES613": "14", "ES614": "18", "ES615": "21", "ES616": "23",
    "ES617": "29", "ES618": "41", "ES620": "30", "ES630": "51", "ES640": "52", "ES701": "35", "ES702": "38",
}
PROVINCIAS_ENTRENAMIENTO = sorted(p for p in NUTS3_A_PROV.values() if p not in SELLADAS_V6 and p not in ("51", "52"))   # 39
# Macrorregiones: las siete NUTS 1 de España, tras quitar las provincias selladas (Madrid y Canarias quedan vacías).
MACRO = {}
for _p in ("15", "27", "32", "36", "39"):
    MACRO[_p] = "NO"
for _p in ("01", "20", "48"):
    MACRO[_p] = "NE"
for _p in ("05", "09", "24", "34", "37", "40", "42", "47", "49", "02", "13", "16", "19", "45", "06", "10"):
    MACRO[_p] = "CE"
for _p in ("08", "17", "25", "43", "03", "12", "46"):
    MACRO[_p] = "ES"
for _p in ("04", "11", "14", "18", "21", "23", "29", "41"):
    MACRO[_p] = "SU"
COSTA = {"03", "04", "08", "11", "12", "15", "17", "18", "20", "21", "27", "29", "36", "39", "43", "46", "48"}   # adenda, AD-E3 (exclusión)
NOMBRE_A_PROV = {
    "Albacete": "02", "Alicante/Alacant": "03", "Almería": "04", "Araba/Alava": "01", "Badajoz": "06", "Barcelona": "08", "Bizkaia": "48",
    "Burgos": "09", "Castellón/Castelló": "12", "Ciudad Real": "13", "Coruña (A)": "15", "Cuenca": "16", "Cáceres": "10", "Cádiz": "11",
    "Córdoba": "14", "Gipuzkoa": "20", "Girona": "17", "Granada": "18", "Guadalajara": "19", "Huelva": "21", "Huesca": "22", "Jaén": "23",
    "León": "24", "Lleida": "25", "Lugo": "27", "Málaga": "29", "Ourense": "32", "Palencia": "34", "Palmas (Las)": "35", "Pontevedra": "36",
    "Salamanca": "37", "Santa Cruz de Tenerife": "38", "Segovia": "40", "Sevilla": "41", "Soria": "42", "Tarragona": "43", "Teruel": "44",
    "Toledo": "45", "Valencia/València": "46", "Valladolid": "47", "Zamora": "49", "Zaragoza": "50", "Ávila": "05", "Cantabria": "39",
}

# ------------------------------------------------------------------------------------------------ sellado
_FUENTES_NUEVAS = {
    "eurostat_censo2001_nacionalidad|provincia|A": ("2001", "Eurostat cens_01rsctz (Censo de 2001, datos del INE)"),
    "eurostat_empleo_nuts3_a10|provincia|A": ("2024", "Eurostat nama_10r_3empers (empleo por NUTS 3 y rama A*10, datos del INE)"),
    "eurostat_poblacion_nuts3|provincia|A": ("2024", "Eurostat demo_r_pjanaggr3 (población a 1 de enero por NUTS 3 y edad, datos del INE)"),
    "eurostat_empleo_nuts3_a10|nacional|A": ("2024", "Eurostat nama_10r_3empers, fila nacional (empleo por rama, datos del INE)"),
}
_MAN = None


def manifiesto() -> dict:
    """docs/v18/sellado_v18.json más tres series `posterior_prereg` bajadas después de la etiqueta (regla 1.4 e: no figuran en ningún conjunto
    de V15 o V16; tope = último periodo descargado, recortado a 2024 por la regla 1.4 b de las series anuales). No se modifica el fichero del
    repositorio: la ampliación vive en memoria y se declara en cada resultado.json (propuesta: añadirlas a src/v18/f3_sellado.py)."""
    global _MAN
    if _MAN is None:
        m = copy.deepcopy(sellado.cargar())
        for k, (tope, nota) in _FUENTES_NUEVAS.items():
            v, n, f = k.split("|")
            m["topes"][k] = {"variable": v, "nivel": n, "frecuencia": f, "tope": tope, "sellada_entera": False, "regla": "(e) + (g)",
                             "fuente_clave": "posterior_prereg: descargada después de la etiqueta; no figura en V15 ni V16", "origen": [nota],
                             "media_desde": None, "edicion_maxima": None, "conjuntos_v15_v16": [], "nota": nota}
        _MAN = m
    return _MAN


def filtrar(df: pd.DataFrame, col_cod: str, nivel: str, col_per: str, variable: str, frecuencia: str) -> pd.DataFrame:
    """sellado.filtrar (con el manifiesto ampliado) + holdout.excluir_sellados_v6 (idempotente) sobre una tabla con código INE."""
    df = df.copy()
    df[col_cod] = df[col_cod].astype(str)
    df[col_per] = df[col_per].astype(str)
    out = sellado.filtrar(df, col_cod, nivel, col_per, variable, frecuencia, manifiesto=manifiesto())
    if nivel in ("ccaa", "provincia", "municipio", "distrito", "seccion"):
        out = holdout.excluir_sellados_v6(out, col_cod, nivel)
    return out


def leer_hechos(variable: str, nivel: str, frecuencia: str, desag: str | None = None) -> pd.DataFrame:
    cols = ["territorio_codigo", "periodo", "valor", "desagregacion", "edicion", "muestra_sellada_v6"]
    f = [("variable", "==", variable), ("nivel", "==", nivel), ("frecuencia", "==", frecuencia)]
    df = pd.read_parquet(HECHOS, columns=cols, filters=f)
    if desag is not None:
        df = df[df["desagregacion"] == desag]
    return filtrar(df, "territorio_codigo", nivel, "periodo", variable, frecuencia)


def ancho(df: pd.DataFrame, col_cod="territorio_codigo", col_per="periodo", col_val="valor", cast=int) -> pd.DataFrame:
    w = df.pivot_table(index=col_cod, columns=col_per, values=col_val, aggfunc="first")
    w.columns = [cast(c) for c in w.columns]
    return w


# ------------------------------------------------------------------------------------------------ inferencia
def _ar_ic_1(a: np.ndarray, c: np.ndarray, cfac: float, alfa: float = 0.05):
    """IC AR exacto (p = 1, un instrumento) con varianza agrupada: {b: (sum a - b sum c)^2 <= chi2·cfac·sum (a_g - b c_g)^2}. Misma lógica que
    iv_debil.ar_ic_1 con un factor de varianza general. Devuelve ('intervalo'|'complemento'|'recta'|'vacio', a, b)."""
    q = stats.chi2.ppf(1 - alfa, 1) * cfac
    c2 = c.sum() ** 2 - q * np.sum(c ** 2)
    c1 = -2 * (a.sum() * c.sum() - q * np.sum(a * c))
    c0 = a.sum() ** 2 - q * np.sum(a ** 2)
    if abs(c2) < 1e-14:
        if abs(c1) < 1e-14:
            return ("recta", -np.inf, np.inf) if c0 <= 0 else ("vacio", np.nan, np.nan)
        r = -c0 / c1
        return ("complemento", r, r)
    disc = c1 ** 2 - 4 * c2 * c0
    if disc < 0:
        return ("recta", -np.inf, np.inf) if c2 < 0 else ("vacio", np.nan, np.nan)
    r1, r2 = sorted(((-c1 - np.sqrt(disc)) / (2 * c2), (-c1 + np.sqrt(disc)) / (2 * c2)))
    return ("intervalo", r1, r2) if c2 > 0 else ("complemento", r1, r2)


def _cl(cluster) -> np.ndarray:
    return pd.factorize(np.asarray(cluster))[0]


class DisenoIV:
    """y = beta·x + controles + e, con x instrumentada por z (un instrumento), pesos y efectos absorbidos por proyección (Frisch-Waugh).

    y, x, z: vectores (n,); C: matriz de controles (n, m) (debe llevar constante o efectos que la generen); w: pesos de regresión;
    cluster: etiqueta de provincia. Todo se multiplica por sqrt(w) y se proyecta fuera de C. Varianza agrupada con el factor G/(G-1) de iv_debil
    (el validado por el Monte Carlo de V18); contrastes: 2SLS con t(G-1), AR exacto agrupado, Webb-AR (nulo impuesto, 9.999 réplicas).
    """

    def __init__(self, y, x, z, cluster, C=None, w=None, tiempo=None, B: int = 9999, semilla: int = SEMILLA, grupos=None):
        """grupos: etiquetas de un único conjunto de efectos fijos disjuntos (p. ej. provincia × año) absorbidos por desmedia ponderada por grupo, para paneles
        grandes (municipios) donde la proyección densa sobre C no cabe; con grupos, C debe ser None. Los grupos deben estar contenidos en un cluster."""
        y, x, z = (np.asarray(a, float) for a in (y, x, z))
        n = len(y)
        cl = _cl(cluster)
        if grupos is not None:
            gr = _cl(grupos)
            orden = np.lexsort((gr, cl))
        else:
            orden = np.argsort(cl, kind="stable")
        self.orden = orden
        self.n, self.G = n, int(cl.max()) + 1
        self.cl = cl[orden]
        _, self.inicio = np.unique(self.cl, return_index=True)
        sw = np.ones(n) if w is None else np.sqrt(np.asarray(w, float))[orden]
        self.sw = sw
        self.grupos = None
        if grupos is not None:
            g = pd.factorize(gr[orden])[0]        # etiquetas por orden de aparición (== orden de posición: los grupos son contiguos)
            _, self._ginicio, self._gtam = np.unique(g, return_index=True, return_counts=True)
            self.grupos = g
            self._gden = np.add.reduceat(sw * sw, self._ginicio)
            self.Q = None
            self.k = len(self._ginicio)
        else:
            Cm = np.ones((n, 1)) if C is None else np.asarray(C, float).reshape(n, -1)[orden]
            U, s, _ = np.linalg.svd(Cm * sw[:, None], full_matrices=False)
            self.Q = U[:, s > s[0] * 1e-9]
            self.k = self.Q.shape[1]
        self.tiempo = None if tiempo is None else np.asarray(tiempo)[orden]
        self.yt, self.xt, self.zt = (self._m(sw * a[orden]) for a in (y, x, z))
        self.zx = float(self.zt @ self.xt)
        self.zz = float(self.zt @ self.zt)
        self.xx = float(self.xt @ self.xt)
        self.B = B
        self.semilla = semilla
        self._W = None
        self._cache = {}
        # factor de varianza agrupada: G/(G-1) de iv_debil (validado) por (n-1)/(n-k) de los efectos absorbidos (como `small` de Stata)
        self.c = self.G / (self.G - 1) * (n - 1) / max(n - self.k, 1)

    def _m(self, v):
        if self.grupos is not None:
            b = np.add.reduceat(self.sw * v, self._ginicio) / self._gden
            return v - self.sw * np.repeat(b, self._gtam)
        return v - self.Q @ (self.Q.T @ v)

    def _proy(self, ys):
        """Proyección fuera de los controles de cada réplica (filas): la muestra bootstrap w_g·u0 ya no es ortogonal a ellos."""
        if self.grupos is not None:
            b = np.add.reduceat(ys * self.sw[None, :], self._ginicio, axis=1) / self._gden[None, :]
            return ys - self.sw[None, :] * np.repeat(b, self._gtam, axis=1)
        return ys - (ys @ self.Q) @ self.Q.T

    # -- estimadores
    def _scores(self, e, z=None):
        z = self.zt if z is None else z
        return np.add.reduceat(z * e, self.inicio, axis=-1)

    def mco(self) -> dict:
        b = float(self.xt @ self.yt / self.xx)
        e = self.yt - b * self.xt
        s = np.add.reduceat(self.xt * e, self.inicio)
        se = float(np.sqrt(self.c * (s ** 2).sum()) / self.xx)
        return {"beta": b, "se": se}

    def iv(self) -> dict:
        b = self.zt @ self.yt / self.zx
        e = self.yt - b * self.xt
        s = self._scores(e)
        se = float(np.sqrt(self.c * (s ** 2).sum()) / abs(self.zx))
        t = float(b / se)
        q = stats.t.ppf(0.975, self.G - 1)
        pi = self.zx / self.zz
        ex = self.xt - pi * self.zt
        se_pi = float(np.sqrt(self.c * (self._scores(ex) ** 2).sum()) / self.zz)
        rf = float(self.zt @ self.yt / self.zz)
        return {"beta": float(b), "se": se, "t": t, "p_t": float(2 * stats.t.sf(abs(t), self.G - 1)), "ic95_t": (float(b - q * se), float(b + q * se)),
                "pi": float(pi), "se_pi": se_pi, "rf": rf, "n": self.n, "G": self.G, "k_absorbidos": self.k}

    def f_efectivo(self) -> float:
        return float(IVD.f_efectivo(self.xt[:, None], self.zt[:, None], self.cl, self.G)[0])

    def ar_exacto(self, alfa: float = 0.05) -> dict:
        """IC de Anderson-Rubin exacto con varianza agrupada (iv_debil.ar_ic_1, APTO en el Monte Carlo de V18)."""
        a = np.add.reduceat(self.zt * self.yt, self.inicio)
        cc = np.add.reduceat(self.zt * self.xt, self.inicio)
        ic = _ar_ic_1(a, cc, self.c, alfa)
        s0 = a.sum() ** 2 / (self.c * np.sum(a ** 2))
        return {"tipo": ic[0], "lo": float(ic[1]), "hi": float(ic[2]), "acotado": ic[0] == "intervalo", "p_beta0": float(stats.chi2.sf(s0, 1)),
                "nota": "iv_debil.ar_ic_1 (APTO) con el factor c = G/(G-1)·(n-1)/(n-k)"}

    # -- Webb-AR
    def _pesos(self):
        if self._W is None:
            rng = np.random.default_rng(self.semilla)
            self._W = WEBB[rng.integers(0, 6, size=(self.B, self.G))]
        return self._W

    def webb_ar_p(self, beta0: float, lote: int = 2000) -> float:
        """p de H0: beta = beta0 por bootstrap de Webb con el nulo impuesto (WCR) sobre la forma reducida de y - beta0·x sobre z (estadístico t
        con varianza agrupada por provincia, recalculada en cada réplica). Mismas réplicas para todo beta0 (inversión suave)."""
        u0 = self.yt - beta0 * self.xt
        c = self.c
        zz = self.zz
        pi = float(self.zt @ u0 / zz)
        s_obs = self._scores(u0 - pi * self.zt)
        t_obs = abs(pi) / (np.sqrt(c * (s_obs ** 2).sum()) / zz)
        W = self._pesos()
        cuenta = 0
        for i in range(0, self.B, lote):
            ys = W[i:i + lote][:, self.cl] * u0[None, :]
            pis = (ys @ self.zt) / zz
            es = self._proy(ys) - pis[:, None] * self.zt[None, :]
            ss = np.add.reduceat(es * self.zt[None, :], self.inicio, axis=1)
            ts = np.abs(pis) / (np.sqrt(c * (ss ** 2).sum(axis=1)) / zz)
            cuenta += int(np.sum(ts >= t_obs - 1e-12))
        return float(cuenta / self.B)

    def ic_webb_ar(self, alfa: float = 0.05, centro: float | None = None, escala: float | None = None, it: int = 16, tope: int = 8) -> dict:
        """Conjunto {beta0: p_WebbAR(beta0) >= alfa} por bisección a cada lado del 2SLS. Si el conjunto no se cierra en 6·tope errores típicos,
        el lado se declara no acotado."""
        r = self.iv()
        c0 = r["beta"] if centro is None else centro
        sc = max(r["se"], 1e-9) if escala is None else escala
        if self.webb_ar_p(c0) < alfa:   # el 2SLS no está en su propio conjunto (instrumento muy débil): rejilla gruesa
            malla = c0 + np.linspace(-6, 6, 25) * sc
            ps = np.array([self.webb_ar_p(b) for b in malla])
            if not (ps >= alfa).any():
                return {"lo": float("nan"), "hi": float("nan"), "acotado": False, "vacio": True}
            c0 = float(malla[int(np.argmax(ps))])
        out, acot = [], []
        for signo in (-1.0, 1.0):
            dentro, fuera, k = c0, c0 + signo * 4 * sc, 0
            while self.webb_ar_p(fuera) >= alfa and k < tope:
                dentro, fuera, k = fuera, fuera + signo * 6 * sc, k + 1
            if self.webb_ar_p(fuera) >= alfa:
                out.append(signo * float("inf"))
                acot.append(False)
                continue
            for _ in range(it):
                m = (dentro + fuera) / 2
                dentro, fuera = (m, fuera) if self.webb_ar_p(m) >= alfa else (dentro, m)
            out.append((dentro + fuera) / 2)
            acot.append(True)
        return {"lo": float(out[0]), "hi": float(out[1]), "acotado": bool(all(acot)), "vacio": False}

    def resumen(self, con_ic: bool = True, con_ic90: bool = False) -> dict:
        r = self.iv()
        r["F_eff"] = self.f_efectivo()
        r["mco"] = self.mco()
        r["ar"] = self.ar_exacto()
        r["p_webb_ar"] = self.webb_ar_p(0.0)
        if con_ic:
            r["ic_webb_ar"] = self.ic_webb_ar(0.05, centro=r["beta"], escala=r["se"])
        if con_ic90:
            r["ic90_webb_ar"] = self.ic_webb_ar(0.10, centro=r["beta"], escala=r["se"])
        return r


# ------------------------------------------------------------------------------------------------ efecto mínimo detectable (adenda 1.3)
def sigma_rho_pre(resid_panel: pd.DataFrame) -> tuple[float, float]:
    """σ y ρ (AR(1) dentro de la unidad) de los residuos del preperiodo. resid_panel: filas = unidad, columnas = años."""
    r = resid_panel.to_numpy(float)
    sig = float(np.nanstd(r, ddof=1))
    num = np.nansum(r[:, 1:] * r[:, :-1])
    den = np.nansum(r[:, :-1] ** 2)
    rho = float(np.clip(num / den if den > 0 else 0.0, -0.9, 0.9))
    return sig, rho


def sigma_rho_equicorr(resid: np.ndarray, unidad) -> tuple[float, float]:
    """σ y correlación intraclase de los residuos de un preperiodo de pocas observaciones por unidad (municipios, 2 años): ρ = Σ_{i≠j mismo i} r_i r_j / Σ r²
    (por pares), acotada a [0, 0,9]."""
    r = np.asarray(resid, float)
    u = pd.factorize(np.asarray(unidad))[0]
    sig = float(np.std(r, ddof=1))
    s1 = np.bincount(u, weights=r)
    s2 = np.bincount(u, weights=r ** 2)
    m = np.bincount(u)
    pares = (s1 ** 2 - s2).sum()
    npares = (m * (m - 1)).sum()
    rho = float(np.clip((pares / max(npares, 1)) / (r @ r / len(r)), 0.0, 0.9))
    return sig, rho


def mde_iv(dis: DisenoIV, unidad_t: np.ndarray, sigma: float, rho: float, R: int = 2000, semilla: int = SEMILLA, grid=None, unidad=None, lote: int = 500) -> dict:
    """MDE al 80 % (bilateral al 5 %) con el contraste AR agrupado por provincia (el mismo estadístico y varianza del Webb-AR, que no puede
    repetirse 9.999 veces dentro de 2.000 réplicas de potencia) y la variación real del instrumento y del regresor del diseño (dis.zt, dis.xt).
    Ruido: AR(1) dentro de la unidad (paneles provinciales) o equicorrelado dentro de la unidad (si se pasa `unidad`, municipios) con σ y ρ del
    preperiodo; se proyecta fuera de los controles. Devuelve mde80, curva de potencia y tamaño bajo el nulo. R réplicas en lotes (memoria)."""
    rng = np.random.default_rng(semilla)
    n, G = dis.n, dis.G
    c = dis.c
    crit = stats.chi2.ppf(0.95, 1)
    lotes = []
    left = R
    while left > 0:
        r_ = min(lote, left)
        left -= r_
        e = rng.standard_normal((r_, n))
        if unidad is not None:      # ruido equicorrelado dentro de la unidad (municipio): u = √ρ a_i + √(1-ρ) e
            ui = pd.factorize(np.asarray(unidad))[0]
            a = rng.standard_normal((r_, int(ui.max()) + 1))
            u = np.sqrt(rho) * a[:, ui] + np.sqrt(1 - rho) * e
        else:
            u = np.empty_like(e)
            u[:, 0] = e[:, 0]
            inicio = np.r_[True, dis.cl[1:] != dis.cl[:-1]]
            for j in range(1, n):
                u[:, j] = e[:, j] if inicio[j] else rho * u[:, j - 1] + np.sqrt(1 - rho ** 2) * e[:, j]
        u = sigma * u * dis.sw[None, :]
        lotes.append(dis._proy(u))
    u = np.vstack(lotes)
    se_ref = float(np.sqrt(c * (np.add.reduceat(dis.zt[None, :] * u, dis.inicio, axis=1) ** 2).sum(axis=1).mean()) / abs(dis.zx))
    grid = np.arange(0.25, 6.01, 0.25) * se_ref if grid is None else np.asarray(grid)
    pot = []
    for b in np.r_[0.0, grid]:
        yb = u + b * dis.xt[None, :]
        s = np.add.reduceat(dis.zt[None, :] * yb, dis.inicio, axis=1)
        ar = (s.sum(axis=1)) ** 2 / (c * (s ** 2).sum(axis=1))
        pot.append(float(np.mean(ar > crit)))
    tam, pot = pot[0], np.array(pot[1:])
    if (pot >= 0.80).any():
        i = int(np.argmax(pot >= 0.80))
        mde = float(grid[0]) if i == 0 else float(np.interp(0.80, [pot[i - 1], pot[i]], [grid[i - 1], grid[i]]))
    else:
        mde = float("inf")
    return {"mde80": mde, "tamano_nulo": tam, "se_ref": se_ref, "R": R, "sigma": sigma, "rho": rho,
            "curva": [(float(b), float(p)) for b, p in zip(grid, pot)]}


# ------------------------------------------------------------------------------------------------ shift-share: 1/HHI y Rotemberg
def inv_hhi(pesos) -> float:
    p = np.asarray(pesos, float)
    p = p[np.isfinite(p) & (p > 0)]
    p = p / p.sum()
    return float(1.0 / np.sum(p ** 2))


def rotemberg(zt_comp: np.ndarray, xt: np.ndarray, yt: np.ndarray) -> dict:
    """Pesos de Rotemberg por componente del instrumento. zt_comp: (n, K) componentes ya ponderados y proyectados (z = suma de columnas);
    xt, yt ya proyectados. alpha_k = (z_k'x)/(z'x) y beta_k = (z_k'y)/(z_k'x)."""
    zx = zt_comp.T @ xt
    alpha = zx / zx.sum()
    beta = np.where(np.abs(zx) > 1e-12, (zt_comp.T @ yt) / np.where(np.abs(zx) > 1e-12, zx, 1), np.nan)
    return {"alpha": alpha, "beta_k": beta}


def by_qvalores(p: dict) -> dict:
    """Benjamini-Yekutieli: q-valores de la familia de p (dict). Vacía devuelve {}."""
    ks = list(p)
    if not ks:
        return {}
    pv = np.array([p[k] for k in ks], float)
    m = len(pv)
    c = np.sum(1.0 / np.arange(1, m + 1))
    orden = np.argsort(pv)
    q = np.empty(m)
    prev = 1.0
    for rank in range(m, 0, -1):
        i = orden[rank - 1]
        prev = min(prev, pv[i] * m * c / rank)
        q[i] = min(prev, 1.0)
    return dict(zip(ks, q.tolist()))


# ------------------------------------------------------------------------------------------------ clasificación
def banda_mc(tamano: float) -> str:
    if 0.04 <= tamano <= 0.06:
        return "apta"
    if tamano > 0.15 or tamano < 0.02:
        return "no fiable"
    return "con valor crítico corregido"


def tamano_mc(herramienta: str, escenario_contiene: str, inferencia_contiene: str) -> float | None:
    f = MC / herramienta / "tabla.csv"
    if not f.exists():
        return None
    t = pd.read_csv(f)
    esc = [c for c in t.columns if c in ("escenario", "caso")]
    inf = [c for c in t.columns if c in ("inferencia", "variante")]
    if not esc or not inf:
        return None
    s = t[t[esc[0]].astype(str).str.contains(escenario_contiene, regex=False) & t[inf[0]].astype(str).str.contains(inferencia_contiene, regex=False)]
    return float(s["tamano_5pct"].iloc[0]) if len(s) else None


def clasificar(i: dict) -> dict:
    """Clasificación V18 con I1-I8 revisados (adenda 1.1 y 1.2). I8 (réplica ciega) queda pendiente: se rotula.
    Claves: estimable, motivo_no_estimable, coprincipal, p_holm, tost{equivalente}, F_eff, ar_acotado, pretend_p, roth_ok, placebo_fecha_p,
    placebo_resultado_p, robustez{cambio_signo, frac_mismo_signo, solape_ic}, inferencia_banda, topes, debiles_extra, tope_max."""
    if not i.get("estimable", True):
        return {"clase": "NO ESTIMABLE", "razones": [i.get("motivo_no_estimable", "")], "debiles": [], "decisivos": [], "topes": []}
    if i.get("coprincipal"):
        return {"clase": "no se clasifica", "razones": ["coprincipal P (adenda 1.6)"], "debiles": [], "decisivos": [], "topes": []}
    dec, deb, topes = [], list(i.get("debiles_extra", [])), list(i.get("topes", []))
    F, ar_ok = i.get("F_eff"), i.get("ar_acotado")
    if F is not None and np.isfinite(F):
        if F < 5 and not ar_ok:
            dec.append(f"F efectivo {F:.1f} < 5 y Anderson-Rubin no acotado")
        elif F < 10:
            deb.append(f"F efectivo {F:.1f} < 10")
            topes.append("tope SUGESTIVO por F efectivo < 10 (adenda 1.2, I2)")
    pp = i.get("pretend_p")
    if pp is not None and np.isfinite(pp):
        if pp < 0.01:
            dec.append(f"pretendencias del instrumento p = {pp:.3f} < 0,01")
        elif pp <= 0.10:
            deb.append(f"pretendencias del instrumento p = {pp:.3f}")
    elif pp is None:
        deb.append("pretendencias del instrumento no realizables")
    if i.get("roth_ok") is False:
        deb.append("potencia de las pretendencias (Roth): el sesgo implicado supera la mitad de |referencia|")
    pf = i.get("placebo_fecha_p")
    if pf is not None and np.isfinite(pf):
        if pf < 0.05 and i.get("placebo_fecha_mismo_signo_mitad"):
            dec.append("placebo de fecha significativo, del mismo signo y de al menos la mitad del efecto")
        elif pf <= 0.10:
            deb.append(f"placebo de fecha p = {pf:.3f}")
    else:
        deb.append("placebo de fecha no realizable")
    po = i.get("placebo_resultado_p")
    if po is None or not np.isfinite(po):
        deb.append("placebo de resultado sin dato")
    elif po <= 0.10:
        deb.append(f"placebo de resultado p = {po:.3f}")
    rb = i.get("robustez") or {}
    if rb.get("cambio_signo"):
        dec.append("cambio de signo en una prueba B4 o variante")
    if rb.get("frac_mismo_signo") is not None and rb["frac_mismo_signo"] < 0.8:
        deb.append(f"mismo signo en {rb['frac_mismo_signo']:.0%} de las variantes enumeradas (< 80 %)")
    if rb.get("solape_ic") is False:
        deb.append("IC95 de alguna robustez no solapa con el principal")
    for clave, txt in (("rotemberg_ok", "Rotemberg: sin los orígenes de más peso el signo no se mantiene o sale del IC95"),
                       ("jrs_ok", "Jaeger-Ruist-Stuhler: con el instrumento retardado la estimación sale del IC95"),
                       ("balance_ok", "balance del instrumento frente a las características de 2001 con p <= 0,10")):
        if i.get(clave) is False:
            deb.append(txt)
    if i.get("inferencia_banda") == "no fiable":
        dec.append("inferencia principal «no fiable» (Monte Carlo) sin alternativa apta")
    if dec:
        return {"clase": "ASOCIACIÓN", "razones": dec + deb, "debiles": deb, "decisivos": dec, "topes": topes}
    valido = not deb
    ph = i.get("p_holm")
    sig = ph is not None and ph < 0.05
    t = i.get("tost") or {}
    if sig:
        clase = "IDENTIFICADO" if (valido and not topes) else "SUGESTIVO"
    elif ph is not None and ph < 0.10:
        deb.append(f"p tras Holm = {ph:.3f} entre 0,05 y 0,10")
        clase = "SUGESTIVO"
    elif t.get("equivalente"):
        clase = "IDENTIFICADO (efecto nulo acotado)" if (valido and not topes) else "SUGESTIVO (efecto nulo acotado)"
    elif valido:
        clase = "NO CONCLUYENTE (sin potencia)"
    else:
        clase = "SUGESTIVO"
    tm = i.get("tope_max")
    orden = {"ASOCIACIÓN": 0, "SUGESTIVO": 1, "IDENTIFICADO": 2}
    if tm and clase.split(" (")[0] in orden and orden[clase.split(" (")[0]] > orden[tm]:
        topes.append(f"tope {tm} de la especificación (tabla consolidada)")
        clase = tm + (" (efecto nulo acotado)" if "nulo acotado" in clase else "")
    return {"clase": clase, "razones": deb + topes, "debiles": deb, "decisivos": [], "topes": topes}


def clase_corta(clase: str) -> str:
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


def _json(o):
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (set, tuple)):
        return list(o)
    return str(o)


def _limpio(o):
    """Sustituye los reales no finitos por None (JSON estándar) y convierte los tipos de numpy; recursivo."""
    if isinstance(o, dict):
        return {str(k): _limpio(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, set)):
        return [_limpio(v) for v in o]
    if isinstance(o, np.ndarray):
        return _limpio(o.tolist())
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


def volcar_json(ruta: Path, obj) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(_limpio(obj), ensure_ascii=False, indent=1, default=_json), encoding="utf-8")


def f4(x, d=4):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return f"{x:.{d}f}"


# ------------------------------------------------------------------------------------------------ diagnósticos B4 comunes (E3, E5, E9)
def residuos_wls(y: np.ndarray, C: np.ndarray, w: np.ndarray | None) -> np.ndarray:
    """Residuo en unidades de y de la regresión (ponderada) de y sobre C."""
    sw = np.ones(len(y)) if w is None else np.sqrt(np.asarray(w, float))
    b, *_ = np.linalg.lstsq(C * sw[:, None], y * sw, rcond=None)
    return y - C @ b


def sigma_rho_de_panel(y: np.ndarray, prov, año, C: np.ndarray, w) -> tuple[float, float]:
    """σ y ρ (AR(1)) del residuo de un panel de preperiodo tras proyectar y sobre C (la misma estructura de efectos de la estimación)."""
    r = residuos_wls(np.asarray(y, float), C, w)
    df = pd.DataFrame({"p": prov, "t": año, "r": r}).pivot_table(index="p", columns="t", values="r")
    return sigma_rho_pre(df)


def pendiente_previa(ypre: np.ndarray, zbar: np.ndarray, xbar: np.ndarray, region: np.ndarray, w: np.ndarray | None, B: int = 9999) -> dict:
    """Pretendencia del instrumento (corte transversal): ypre (resultado medio del preperiodo por provincia) sobre zbar (instrumento medio de la ventana) con efectos de
    macrorregión; p por Webb (nulo impuesto) con cada provincia como conglomerado. Potencia (Roth): pendiente detectable al 80 % = (1,96 + 0,84)·EE; el sesgo
    implicado en beta = pendiente / (primera etapa de corte transversal)."""
    n = len(ypre)
    C = pd.get_dummies(pd.Series(region), dtype=float).to_numpy()
    d = DisenoIV(ypre, zbar, zbar, np.arange(n), C=C, w=w, B=B)
    r = d.iv()
    pw = d.webb_ar_p(0.0)
    d1 = DisenoIV(xbar, zbar, zbar, np.arange(n), C=C, w=w, B=1)
    pi_cs = d1.iv()["beta"]
    det = (1.96 + 0.8416) * r["se"]
    return {"pendiente": r["beta"], "se": r["se"], "p_t": r["p_t"], "p_webb": pw, "pendiente_detectable80": det, "primera_etapa_cs": pi_cs,
            "sesgo_detectable_beta": det / abs(pi_cs) if pi_cs else float("inf"), "n": n}


def placebo_fecha(ypre: np.ndarray, zfalso: np.ndarray, prov, C: np.ndarray, w, rf_principal: float, B: int = 9999) -> dict:
    """Placebo de fecha: forma reducida del resultado del preperiodo sobre el instrumento de t + desfase (instrumento falso), con efectos región-año; p por Webb.
    mismo_signo_mitad: el coeficiente placebo tiene el signo de la forma reducida principal y al menos la mitad de su tamaño."""
    d = DisenoIV(ypre, zfalso, zfalso, prov, C=C, w=w, B=B)
    r = d.iv()
    pw = d.webb_ar_p(0.0)
    return {"coef": r["beta"], "se": r["se"], "p_webb": pw, "p_t": r["p_t"], "n": r["n"],
            "mismo_signo_mitad": bool(np.sign(r["beta"]) == np.sign(rf_principal) and abs(r["beta"]) >= 0.5 * abs(rf_principal))}


def ic_contiene(ic: tuple[float, float], v: float) -> bool:
    return bool(ic[0] <= v <= ic[1])


def wald_f(b: np.ndarray, V: np.ndarray, G: int) -> tuple[float, float]:
    k = len(b)
    W = float(b @ np.linalg.pinv(V) @ b)
    return W, float(stats.f.sf(W / k, k, max(G - 1, 1)))


def balance_provincial(zbar: np.ndarray, X: np.ndarray, region: np.ndarray) -> dict:
    """Balance: zbar sobre características iniciales (X: n×m, estandarizadas) con efectos de macrorregión; contraste conjunto con covarianza HC1 y F(m, n-k)."""
    n, m = X.shape
    Xs = (X - X.mean(0)) / X.std(0)
    Rg = pd.get_dummies(pd.Series(region), dtype=float).to_numpy()
    A = np.hstack([Rg, Xs])
    b, *_ = np.linalg.lstsq(A, zbar, rcond=None)
    e = zbar - A @ b
    AtAi = np.linalg.pinv(A.T @ A)
    meat = (A * e[:, None]).T @ (A * e[:, None]) * n / max(n - A.shape[1], 1)
    V = AtAi @ meat @ AtAi
    sel = slice(Rg.shape[1], A.shape[1])
    W = float(b[sel] @ np.linalg.pinv(V[sel, sel]) @ b[sel])
    return {"F": W / m, "p": float(stats.f.sf(W / m, m, max(n - A.shape[1], 1))), "coef_std": [float(v) for v in b[sel]], "n": n, "m": m}


def bhj_alternativa(y, x, E, g, w, año, C, origenes) -> dict:
    """BHJ a nivel de choque con bhj_lib (ssaggregate + iv_cluster, cluster por origen; ar_ic_nulo_impuesto). E: exposiciones e_pc,t (n, K); g: choques (n, K).
    Reescala por κ_t = max_p Σ_c e_pc,t (cuotas ≤ 1 para el sector «faltante»); la estimación es invariante a esa escala. Etiquetado «no fiable»: el Monte Carlo de
    V18 deja NO APTO el BHJ con 10-30 choques."""
    n, Kc = E.shape
    años = np.asarray(año)
    kap = pd.Series(E.sum(axis=1)).groupby(años).transform("max").to_numpy()
    s = E / kap[:, None]
    gg = g * kap[:, None]
    loc = np.arange(n)
    filas = pd.DataFrame({"loc": np.repeat(loc, Kc), "sector": np.tile(np.arange(1, Kc + 1), n), "s": s.ravel()})
    # el choque depende del año: se codifica el periodo en el sector agregando (sector, periodo); ssaggregate ya agrupa por (sector, periodo)
    V = pd.DataFrame({"y": y, "x": x})
    w_ = np.ones(n) if w is None else np.asarray(w, float)
    out = bhj_lib.ssaggregate(V, w_, loc, años, filas, controles={"": C[:, 1:] if False else C}, addmissing=True, sector_faltante=0)
    out = out.dropna()
    # choque g_{c,t}: media de los choques de las localizaciones (idéntico para todas las de un año)
    gt = {(c + 1, int(t)): float(np.mean(gg[años == t, c])) for t in np.unique(años) for c in range(Kc)}
    gn = np.array([0.0 if sec == 0 else gt.get((int(sec), int(per)), 0.0) for sec, per in zip(out["sector"], out["periodo"])])
    keep = out["sector"].to_numpy() != 0
    o = out[keep]
    r = bhj_lib.iv_cluster(o["y"].to_numpy(), o["x"].to_numpy(), gn[keep], o["s_n"].to_numpy(), o["sector"].to_numpy(), controles=None, ajuste="G")
    return {"beta": r["beta"], "se": r["se"], "F1": r["F1"], "n_choques": int(len(o)), "G": r["G"], "etiqueta": "no fiable (Monte Carlo de V18: BHJ con 10-30 choques NO APTO)"}


__all__ = ["Registry", "holm", "math"]

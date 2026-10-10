"""Infraestructura común de la v2 (SOLO LECTURA para las ramas; no modificar desde una rama).

Contenido
---------
1. load(nombre)            -> holdout.load_train(nombre). Único acceso a datos (nunca data/sealed,
                              data/raw ni data/processed por otra vía).
2. block_splits            -> ventana EXPANSIVA con bloques de test y embargo (>= max(embargo, h)).
3. dm_hln, dm_panel        -> Diebold-Mariano con corrección Harvey-Leybourne-Newbold (1997).
4. Líneas base de predicción DIRECTA a h pasos, objetivo y_{t+h} = ln X_{t+h} - ln X_t:
   ar4_nacional, ecm_v1_nacional, panel_ar4, panel_ecm_v1.
5. evaluar                 -> RMSE, MAE y DM-HLN vs AR(4) y vs ECM v1 en la MISMA muestra.
6. registrar, Presupuesto  -> cada configuración/hiperparámetro cuenta como especificación (Registry).
7. resultado_json          -> valida el esquema de CLAUDE.md y escribe resultado.json.

Convenciones
------------
* SEED = 20261010. Sin red. Sin aleatoriedad en las líneas base (mínimos cuadrados).
* Los índices de test de block_splits son ORÍGENES de predicción t (el objetivo es t+h). El
  entrenamiento usa solo orígenes s con s+h <= L (L = último periodo de entrenamiento), de modo que
  NADA posterior a L entra en la estimación (ni objetivos, ni adelantos del DOLS). Los regresores en
  los orígenes de test son retardos (información disponible en t).
* Los datos de entrenamiento de holdout pueden traer periodos > 2024Q2 (p. ej. una fila 2026Q3 con
  solo dummies en nacional_q_v2); las líneas base los recortan con Q_TRAIN_FIN = "2024Q2".
* Cada predictor devuelve un DataFrame con columnas
  (periodo [origen t], periodo_obj [t+h], unidad, y_real, y_pred, modelo, split, h) y guarda en
  `.attrs["coef"]` los coeficientes por split (para auditar fugas) y en `.attrs["omitidos"]` los
  splits sin muestra suficiente.
* ECM v1: el DOLS usa k=2 (adelantos/retardos de Δx); si la ventana de entrenamiento es demasiado
  corta (n < nº parámetros + 5) se reduce a k=1 y luego k=0 (atributo attrs["k_dols"]). Desviación
  documentada: con la ventana expansiva desde 2012Q1 el DOLS ±2 no es estimable en nacional.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import holdout  # noqa: E402

SEED = 20261010
Q_TRAIN_FIN = "2024Q2"
NIVELES_EVIDENCIA = ("CAUSAL", "ASOCIACIÓN ROBUSTA", "EXPLORATORIO", "DESCRIPTIVO")
BASE = "AR4"
ECM = "ECM_v1"


# ------------------------------------------------------------------ 1. datos
def load(nombre: str) -> pd.DataFrame:
    """Carga la parte de entrenamiento de un panel (único acceso permitido a los datos)."""
    return holdout.load_train(nombre)


# ------------------------------------------------------------------ 2. splits
def block_splits(periodos_ordenados, h: int, block_len: int = 4, embargo: int = 4,
                 min_train: int = 40, first_test=None):
    """Splits en bloques con ventana expansiva y embargo.

    Devuelve lista de (idx_train, idx_test): posiciones (np.ndarray) en `periodos_ordenados`.
    Entre el último periodo de entrenamiento y el primero de test hay exactamente
    emb_efectivo = max(embargo, h) periodos intermedios, de modo que el objetivo a h pasos de
    cualquier observación de entrenamiento (s+h <= L+h <= L+emb) cae antes del bloque de test.
    El entrenamiento es expansivo (0..L); el test son `block_len` orígenes consecutivos; el
    siguiente split avanza un bloque. `first_test` (etiqueta o posición) fija el inicio del primer
    bloque; si es None se usa min_train + emb_efectivo. Exige len(idx_train) >= min_train.
    Para paneles pasar los periodos únicos de la columna de tiempo (se aplican a todas las unidades).
    """
    per = list(periodos_ordenados)
    if per != sorted(per) or len(set(per)) != len(per):
        raise ValueError("periodos_ordenados debe estar ordenado y sin duplicados")
    emb = max(int(embargo), int(h))
    if first_test is None:
        start = min_train + emb
    elif isinstance(first_test, (int, np.integer)):
        start = int(first_test)
    else:
        start = per.index(first_test)
    if start - emb < min_train:
        raise ValueError(f"entrenamiento inicial {start - emb} < min_train={min_train}")
    out = []
    while start + block_len <= len(per):
        out.append((np.arange(0, start - emb), np.arange(start, start + block_len)))
        start += block_len
    return out


# ------------------------------------------------------------------ 3. Diebold-Mariano
def _loss(e, loss: str):
    e = np.asarray(e, float)
    if loss == "mse":
        return e ** 2
    if loss == "mae":
        return np.abs(e)
    raise ValueError("loss debe ser 'mse' o 'mae'")


def _dm_from_d(d, h: int) -> dict:
    d = np.asarray(d, float)
    n = len(d)
    if n < 3:
        return {"DM": np.nan, "p": np.nan, "mean_d": float(np.mean(d)) if n else np.nan, "n": n}
    dbar = d.mean()
    dc = d - dbar
    g = [dc @ dc / n] + [dc[k:] @ dc[:-k] / n for k in range(1, h)]
    lrv = g[0] + 2 * sum(g[1:])           # h-1 autocovarianzas (DM/HLN originales)
    if lrv <= 0:                          # estimador no definido positivo en muestras pequeñas
        lrv = g[0] + 2 * sum((1 - k / h) * g[k] for k in range(1, h))   # Bartlett
    if lrv <= 0:
        return {"DM": np.nan, "p": np.nan, "mean_d": float(dbar), "n": n}
    dm = dbar / np.sqrt(lrv / n)
    st = dm * np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
    return {"DM": float(st), "p": float(2 * stats.t.sf(abs(st), n - 1)), "mean_d": float(dbar), "n": n}


def dm_hln(e1, e2, h: int, loss: str = "mse") -> dict:
    """DM con corrección HLN y p con t(n-1). d = L(e1) - L(e2): positivo => el modelo 2 es mejor."""
    return _dm_from_d(_loss(e1, loss) - _loss(e2, loss), h)


def dm_panel(e1, e2, periodos, h: int, loss: str = "mse") -> dict:
    """DM en paneles: promedia la diferencia de pérdidas por periodo (media transversal) y aplica DM."""
    d = pd.Series(_loss(e1, loss) - _loss(e2, loss)).groupby(np.asarray(periodos)).mean().sort_index()
    return _dm_from_d(d.values, h)


# ------------------------------------------------------------------ 4. líneas base
def _ln(df, var):
    if var.startswith("ln_"):
        return df[var].astype(float)
    return np.log(df[var].astype(float))


def _prep(df, col_u, tmax=Q_TRAIN_FIN):
    d = df.copy()
    d["trimestre"] = d["trimestre"].astype(str)
    d = d[d["trimestre"] <= tmax].copy()
    d["unidad"] = "ES" if col_u is None else d[col_u].astype(str)
    return d


def _grid(d, lvl_fn):
    """Rejilla completa unidad x periodo (para que los retardos sean temporales), nivel 'lvl' y 'pos'."""
    d = d.copy()
    d["lvl"] = lvl_fn(d)
    first = d.loc[d["lvl"].notna(), "trimestre"].min()
    d = d[d["trimestre"] >= first]
    per = sorted(d["trimestre"].unique())
    units = sorted(d["unidad"].unique())
    idx = pd.MultiIndex.from_product([units, per], names=["unidad", "trimestre"])
    long = d.drop_duplicates(["unidad", "trimestre"]).set_index(["unidad", "trimestre"]).reindex(idx).reset_index()
    long["pos"] = long["trimestre"].map({p: i for i, p in enumerate(per)})
    return long, per, units


def _g(long, s, n):
    return s.groupby(long["unidad"]).shift(n)


def _qdum(labels, h=0):
    q = ((np.array([int(x[-1]) for x in labels]) - 1 + h) % 4) + 1
    return pd.DataFrame({f"q{k}": (q == k).astype(float) for k in (2, 3, 4)})


def _design(long, rows, fcols, units, h):
    """[features, dummies trimestre objetivo, dummies de unidad] para las filas `rows` (máscara)."""
    sub = long.loc[rows]
    qd = _qdum(sub["trimestre"].values, h)
    qd.index = sub.index
    ud = pd.DataFrame({f"u_{u}": (sub["unidad"] == u).astype(float) for u in units}, index=sub.index)
    return pd.concat([sub[fcols].astype(float), qd, ud], axis=1)


def _fit_predict(long, posL, test_pos, fcols, units, h, min_extra=4):
    tr = (long["pos"] + h <= posL) & long["yh"].notna() & long[fcols].notna().all(axis=1)
    te = long["pos"].isin(test_pos) & long[fcols].notna().all(axis=1)
    Xtr = _design(long, tr, fcols, units, h)
    if len(Xtr) < Xtr.shape[1] + min_extra or not te.any():
        return None
    Xte = _design(long, te, fcols, units, h)
    beta = np.linalg.lstsq(Xtr.values, long.loc[tr, "yh"].values, rcond=None)[0]
    return pd.Series(Xte.values @ beta, index=Xte.index), dict(zip(Xtr.columns, beta.tolist()))


def _dols(long, posL, ycol, xcols, units, k_max=2):
    """DOLS (Stock-Watson) agrupado con FE de unidad y dummies trimestrales, SOLO con pos <= posL.
    Devuelve función ect(long) -> Series y metadatos (k, n, coef). None si no es estimable."""
    fit = long[long["pos"] <= posL].copy()
    for k in range(k_max, -1, -1):
        cols = {}
        for x in xcols:
            dx = _g(fit, fit[x], 0) - _g(fit, fit[x], 1)
            for j in range(-k, k + 1):
                cols[f"D_{x}_{j}"] = _g(fit, dx, -j)
        Z = pd.concat([fit[[ycol] + xcols], pd.DataFrame(cols, index=fit.index)], axis=1)
        qd = _qdum(fit["trimestre"].values)
        qd.index = fit.index
        ud = pd.DataFrame({f"u_{u}": (fit["unidad"] == u).astype(float) for u in units}, index=fit.index)
        X = pd.concat([fit[xcols], qd, Z.drop(columns=[ycol] + xcols), ud], axis=1)
        ok = Z[ycol].notna() & X.notna().all(axis=1)
        if ok.sum() >= X.shape[1] + 5:
            b = np.linalg.lstsq(X[ok].values, Z.loc[ok, ycol].values, rcond=None)[0]
            par = pd.Series(b, index=X.columns)

            def ect(lg, par=par):
                q = _qdum(lg["trimestre"].values)
                q.index = lg.index
                alpha = lg["unidad"].map(lambda u: par.get(f"u_{u}", np.nan))
                return (lg[ycol] - alpha - (lg[xcols] * par[xcols].values).sum(axis=1)
                        - (q * par[["q2", "q3", "q4"]].values).sum(axis=1))
            return ect, dict(k=k, n=int(ok.sum()), coef=par[xcols + ["q2", "q3", "q4"]].to_dict())
    return None


def _run(df, col_u, h, splits, desde, min_train, block_len, embargo, lvl_fn, feat_fn, modelo, ecm_x=None,
         ecm_prep=None):
    d = _prep(df, col_u)
    if ecm_prep is not None:
        d = ecm_prep(d)
    long, per, units = _grid(d, lvl_fn)
    lvl = long["lvl"]
    long["dY"] = lvl - _g(long, lvl, 1)
    long["yh"] = _g(long, lvl, -h) - lvl
    fcols0 = feat_fn(long)
    if splits is None:
        splits = block_splits(per, h, block_len, embargo, min_train, first_test=desde)
    rows, coefs, omit, kd = [], {}, [], {}
    for sid, (itr, ite) in enumerate(splits):
        posL = int(itr[-1])
        lg, fcols = long, list(fcols0)
        if ecm_x is not None:
            r = _dols(long, posL, "lvl", ecm_x, units)
            if r is None:
                omit.append(sid)
                continue
            ect, meta = r
            lg = long.copy()
            lg["ect"] = ect(lg)
            fcols = ["ect"] + fcols
            kd[sid] = meta["k"]
        res = _fit_predict(lg, posL, set(ite.tolist()), fcols, units, h)
        if res is None:
            omit.append(sid)
            continue
        pred, cf = res
        coefs[sid] = cf
        sub = lg.loc[pred.index]
        obj = [per[p + h] if p + h < len(per) else None for p in sub["pos"]]
        rows.append(pd.DataFrame({"periodo": sub["trimestre"].values, "periodo_obj": obj,
                                  "unidad": sub["unidad"].values, "y_real": sub["yh"].values,
                                  "y_pred": pred.values, "modelo": modelo, "split": sid, "h": h}))
    out = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(
        columns=["periodo", "periodo_obj", "unidad", "y_real", "y_pred", "modelo", "split", "h"])
    out.attrs.update(coef=coefs, omitidos=omit, k_dols=kd, splits=[(a.tolist(), b.tolist()) for a, b in splits])
    return out


def _lvl_fn(var, real, nac=None):
    """Nivel ln(var) [- ln deflactor nacional si real]. Nacional: deflactor en el propio df."""
    def f(d):
        y = _ln(d, var)
        if real:
            defl = d["ln_deflactor"] if nac is None else d["trimestre"].map(
                _nac_series(nac, "ln_deflactor"))
            y = y - defl
        return y
    return f


def _nac_series(nac, col):
    n = nac.copy()
    n["trimestre"] = n["trimestre"].astype(str)
    n = n[n["trimestre"] <= Q_TRAIN_FIN]
    return n.set_index("trimestre")[col].astype(float)


def _feat_ar4(long):
    for k in range(4):
        long[f"dY_l{k}"] = _g(long, long["dY"], k) if k else long["dY"]
    return [f"dY_l{k}" for k in range(4)]


_ARGS = dict(splits=None, desde=None, min_train=40, block_len=4, embargo=4)


def ar4_nacional(df, var, h, real=False, splits=None, desde=None, min_train=40, block_len=4, embargo=4):
    """AR(4) directo: y_{t+h} sobre Δln X_t..Δln X_{t-3} + dummies del trimestre objetivo.
    `var`: columna (en niveles o 'ln_*'); real=True resta ln_deflactor. Reestimado por split con pos <= L."""
    return _run(df, None, h, splits, desde, min_train, block_len, embargo, _lvl_fn(var, real), _feat_ar4, BASE)


def _nac_x(d):
    d = d.sort_values("trimestre").copy()
    d["ln_permisos_l4"] = d["ln_permisos"].shift(4)
    d["ln_costes_real"] = d["ln_costes"] - d["ln_deflactor"]
    return d


def ecm_v1_nacional(df, h, var="ln_ipv", real=True, splits=None, desde=None, min_train=40, block_len=4,
                    embargo=4):
    """Versión directa del ECM real de v1 (output/f2/ecuacion_real.csv, sección 8 de resumen_f2.md).

    ect_t: DOLS ±2 (ver k en attrs) de ln precio real sobre ln_ocupados, tipo_hip_real, ln_permisos_l4,
    ln_costes_real (= ln_costes - ln_deflactor) con dummies trimestrales, estimado SOLO con la ventana de
    entrenamiento. Corto plazo (preferido real v1, solo con información en t): ect_t, Δln_ocupados_t,
    Δtipo_hip_t, Δln_renta_hog_real_t, Δy_{t-3}, Δln_credito_nuevo_t + dummies del trimestre objetivo.
    (En v1 los términos d_*_l1 y d_ln_ipv_real_l4 de Δy_t son retardos del trimestre t; aquí se
    desplazan para que todo esté disponible en el origen t; los contemporáneos de v1 pasan a t.)
    Nombres de columna idénticos a v1 en nacional_q_v2 (no hace falta mapeo)."""
    def feat(long):
        long["dOcup"] = long["ln_ocupados"] - _g(long, long["ln_ocupados"], 1)
        long["dTipo"] = long["tipo_hip"] - _g(long, long["tipo_hip"], 1)
        long["dRenta"] = long["ln_renta_hog_real"] - _g(long, long["ln_renta_hog_real"], 1)
        long["dCred"] = long["ln_credito_nuevo"] - _g(long, long["ln_credito_nuevo"], 1)
        long["dY_l3"] = _g(long, long["dY"], 3)
        return ["dOcup", "dTipo", "dRenta", "dY_l3", "dCred"]
    return _run(df, None, h, splits, desde, min_train, block_len, embargo, _lvl_fn(var, real), feat, ECM,
                ecm_x=["ln_ocupados", "tipo_hip_real", "ln_permisos_l4", "ln_costes_real"], ecm_prep=_nac_x)


def panel_ar4(df, var, unidad, h, real=False, nac=None, splits=None, desde=None, min_train=40,
              block_len=4, embargo=4):
    """AR(4) directo agrupado con FE de unidad y dummies de trimestre del año (no de periodo)."""
    nac = nac if nac is not None else (load("nacional_q_v2") if real else None)
    return _run(df, unidad, h, splits, desde, min_train, block_len, embargo, _lvl_fn(var, real, nac),
                _feat_ar4, BASE)


def panel_ecm_v1(df, var_precio, unidad, h, real=True, nac=None, splits=None, desde=None, min_train=40,
                 block_len=4, embargo=4):
    """Análogo provincial del ECM v1: ect_{i,t} de un DOLS agrupado con FE de provincia (ln precio real
    provincial sobre ln_ocupados provincial, tipo_hip_real, ln_costes_real nacional [de nacional_q_v2]),
    + 4 retardos de Δln precio y de Δln ocupados (t..t-3) + FE de unidad y trimestre; directo a h."""
    nac = nac if nac is not None else load("nacional_q_v2")
    costes = _nac_series(nac, "ln_costes") - _nac_series(nac, "ln_deflactor")

    def prep(d):
        d = d.copy()
        d["ln_costes_real"] = d["trimestre"].map(costes)
        return d

    def feat(long):
        dO = long["ln_ocupados"] - _g(long, long["ln_ocupados"], 1)
        cols = []
        for k in range(4):
            long[f"dY_l{k}"] = _g(long, long["dY"], k) if k else long["dY"]
            long[f"dO_l{k}"] = _g(long, dO, k) if k else dO
            cols += [f"dY_l{k}", f"dO_l{k}"]
        return cols
    return _run(df, unidad, h, splits, desde, min_train, block_len, embargo, _lvl_fn(var_precio, real, nac),
                feat, ECM, ecm_x=["ln_ocupados", "tipo_hip_real", "ln_costes_real"], ecm_prep=prep)


# ------------------------------------------------------------------ 5. evaluación
def _rm(e):
    return float(np.sqrt(np.mean(np.square(e)))), float(np.mean(np.abs(e)))


def evaluar(preds_modelo, preds_base, h: int | None = None, loss: str = "mse") -> pd.DataFrame:
    """RMSE, MAE y DM-HLN vs AR(4) y vs ECM v1 en la MISMA muestra.

    preds_base: dict {"AR4": df, "ECM_v1": df} (salidas de las líneas base). La muestra es la
    intersección exacta de (unidad, periodo) con y_real e y_pred no nulos en el modelo y en las bases.
    DM positivo => el modelo es mejor que la base. Con varias unidades usa dm_panel."""
    base = {k: v for k, v in preds_base.items()}
    h = int(h if h is not None else preds_modelo["h"].iloc[0])
    key = ["unidad", "periodo"]

    def ok(df):
        x = df.dropna(subset=["y_real", "y_pred"]).drop_duplicates(key)
        return x.set_index(key)
    mod = {m: ok(g) for m, g in preds_modelo.groupby("modelo")}
    bs = {k: ok(v) for k, v in base.items()}
    filas = []
    for nombre, M in mod.items():
        idx = M.index
        for B in bs.values():
            idx = idx.intersection(B.index)
        if len(idx) == 0:
            raise ValueError("intersección vacía entre el modelo y las líneas base")
        M2, rows = M.loc[idx], {}
        rows.update(modelo=nombre, n=len(idx), n_periodos=idx.get_level_values("periodo").nunique())
        rows["rmse"], rows["mae"] = _rm(M2["y_real"] - M2["y_pred"])
        e_m = (M2["y_real"] - M2["y_pred"]).values
        per = idx.get_level_values("periodo").values
        for etq, B in bs.items():
            B2 = B.loc[idx]
            e_b = (B2["y_real"] - B2["y_pred"]).values
            rows[f"rmse_{etq}"] = _rm(e_b)[0]
            dm = dm_panel(e_b, e_m, per, h, loss) if idx.get_level_values("unidad").nunique() > 1 else \
                dm_hln(e_b[np.argsort(per)], e_m[np.argsort(per)], h, loss)
            rows[f"dm_vs_{etq}"], rows[f"p_vs_{etq}"] = dm["DM"], dm["p"]
        filas.append(rows)
    return pd.DataFrame(filas)


# ------------------------------------------------------------------ 6. registro
def registrar(registry, fase, modelo_id, formula, muestra_ini, muestra_fin, n, rmse_oos=np.nan,
              config=None, notas="", **kw):
    """Anota UNA configuración en el Registry de econ_utils (cada hiperparámetro/configuración cuenta
    como especificación). `config` (dict) se serializa en `notas`."""
    extra = f" | config={json.dumps(config, ensure_ascii=False, default=str, sort_keys=True)}" if config else ""
    registry.log(fase, modelo_id, formula, muestra_ini, muestra_fin, n, np.nan, np.nan, np.nan,
                 rmse_oos=rmse_oos, notas=(notas + extra).strip(" |"), **kw)


class Presupuesto:
    """Presupuesto de configuraciones declarado ANTES de buscar. `usar()` registra y cuenta; al
    superar n_max lanza RuntimeError (no se puede probar una configuración fuera del presupuesto)."""

    def __init__(self, registry, fase: str, n_max: int, descripcion: str = ""):
        self.registry, self.fase, self.n_max, self.usadas = registry, fase, int(n_max), 0
        registry.log(fase, f"{fase}_PRESUPUESTO", "presupuesto declarado", "", "", 0, np.nan, np.nan, np.nan,
                     notas=f"n_max={n_max} configuraciones. {descripcion}".strip())

    def usar(self, modelo_id, config, formula="", muestra_ini="", muestra_fin="", n=0, rmse_oos=np.nan,
             notas=""):
        if self.usadas >= self.n_max:
            raise RuntimeError(f"presupuesto de {self.n_max} configuraciones agotado en {self.fase}")
        self.usadas += 1
        registrar(self.registry, self.fase, modelo_id, formula, muestra_ini, muestra_fin, n, rmse_oos,
                  config=config, notas=notas)


# ------------------------------------------------------------------ 7. resultado.json
_CAMPOS = ("rama", "pregunta", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado",
           "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas")


def resultado_json(ruta, **campos) -> dict:
    """Valida el esquema de CLAUDE.md y escribe `ruta`. Campos: rama, pregunta, datos, N, metodo,
    estimacion, ic95, p_ajustado, nivel_evidencia (CAUSAL | ASOCIACIÓN ROBUSTA | EXPLORATORIO |
    DESCRIPTIVO), diagnosticos, fuera_muestra {modelo, rmse, dm_vs_ar4}, notas."""
    falta = [c for c in _CAMPOS if c not in campos]
    sobra = [c for c in campos if c not in _CAMPOS]
    if falta or sobra:
        raise ValueError(f"resultado.json: faltan {falta}, sobran {sobra}")
    if campos["nivel_evidencia"] not in NIVELES_EVIDENCIA:
        raise ValueError(f"nivel_evidencia inválido: {campos['nivel_evidencia']!r}; use {NIVELES_EVIDENCIA}")
    fm = campos["fuera_muestra"]
    if not isinstance(fm, dict) or not {"modelo", "rmse", "dm_vs_ar4"} <= set(fm):
        raise ValueError("fuera_muestra debe ser dict con modelo, rmse y dm_vs_ar4")
    if not isinstance(campos["N"], (int, np.integer, dict)):
        raise ValueError("N debe ser entero (o dict de enteros)")
    ic = campos["ic95"]
    if ic is not None and not isinstance(ic, dict) and not (isinstance(ic, (list, tuple)) and len(ic) == 2):
        raise ValueError("ic95 debe ser [inf, sup], dict por coeficiente o None")
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(campos, indent=2, ensure_ascii=False, default=float))
    return campos


# ------------------------------------------------------------------ smoke test
def smoke(desde="2012Q1", h=4, min_train=8, salida="output/v2/common/smoke_lineas_base.csv"):
    """AR(4) vs ECM v1 en ventana expansiva (solo entrenamiento). Imprime y guarda la tabla."""
    nac, pan = load("nacional_q_v2"), load("panel_prov_q")
    kw = dict(desde=desde, min_train=min_train)
    casos = [("nacional", "ln_ipc_alquiler", False), ("nacional", "p_tasado", True),
             ("panel", "ipc_alquiler", False), ("panel", "p_tasado", True)]
    out = []
    for esc, var, real in casos:
        if esc == "nacional":
            a = ar4_nacional(nac, var, h, real=real, **kw)
            e = ecm_v1_nacional(nac, h, var=var, real=real, **kw)
        else:
            a = panel_ar4(pan, var, "cod_prov", h, real=real, nac=nac, **kw)
            e = panel_ecm_v1(pan, var, "cod_prov", h, real=real, nac=nac, **kw)
        r = evaluar(e, {BASE: a}, h)   # muestra común = intersección ECM v1 ∩ AR(4)
        out.append(dict(escenario=esc, objetivo=("real " if real else "") + var, h=h,
                        n=int(r["n"][0]), n_periodos=int(r["n_periodos"][0]),
                        rmse_AR4=r["rmse_AR4"][0], rmse_ECM_v1=r["rmse"][0],
                        dm_ECM_vs_AR4=r["dm_vs_AR4"][0], p=r["p_vs_AR4"][0],
                        k_dols=sorted(set(e.attrs["k_dols"].values())), omitidos_ecm=len(e.attrs["omitidos"])))
    t = pd.DataFrame(out)
    p = Path(__file__).resolve().parents[1] / salida
    p.parent.mkdir(parents=True, exist_ok=True)
    t.to_csv(p, index=False)
    return t


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "smoke":
        pd.set_option("display.width", 200)
        print(smoke(*(sys.argv[2:3] or ["2012Q1"])))
    else:
        print(__doc__)

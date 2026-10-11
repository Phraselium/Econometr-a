"""M4 v6: evaluacion SELLADA, una vez por modelo (holdout.evaluate_v6). NO entra en make.

Uso:
  python3 src/v6/m4_sellado.py --dry     ensayo con un sellado FALSO construido desde el entrenamiento (no abre data/sealed)
  python3 src/v6/m4_sellado.py --real    abre el sellado, un modelo por llamada; escribe output/v6/M4/sellado_<id>.json

Cada modelo (M3A, M3B), cada linea base (persistencia, AR por unidad, ECM v1 aproximado) y el econometrico M1
(M1A TWFE con tendencia en alquiler; M1B ADL con EF en compra) se evaluan sobre las MISMAS filas de cada tarea.
Regresores en t-1 (misma transformacion que el entrenamiento). Sin prediccion posible (rasgo ausente) -> persistencia
(declarado y contado en `n_fallback_persistencia`). Predice con modelos ya ajustados: nunca reajusta con el sellado.
Grupos: espacial (provincia sellada, periodo < corte), temporal (provincia de entrenamiento, periodo >= corte),
conjunta (provincia sellada, periodo >= corte), total. Los errores se agregan por (provincia, periodo, grupo).
Validacion espacial nueva; temporal ya vista en v2 (otras provincias) y de forma descriptiva en v4-v5.
"""
from __future__ import annotations

import json
import os
import sys
import traceback
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src/v6"))
import econ_utils  # noqa: E402


class _RegNulo:  # evita que importar m3b_run reescriba output/v6/M3B/registro.csv al salir
    def __init__(self, *a, **k):
        pass

    def log(self, *a, **k):
        pass

    def flush(self):
        pass


econ_utils.Registry = _RegNulo
import holdout  # noqa: E402
import m3a_dl as DLM  # noqa: E402
import m3a_lib as A  # noqa: E402
import m3b_lib as BL  # noqa: E402
import m3b_run as B  # noqa: E402

SEED = 20261010
OUT = RAIZ / "output/v6/M4"
CORTE_ALQ, CORTE_CP = 2024, 2025
GRUPOS = ("espacial", "temporal", "conjunta", "total")
MODO = {"dry": False, "sel": None, "corte_alq": CORTE_ALQ, "corte_cp": CORTE_CP}

TAREAS = {
    "alq_provincia": dict(kind="alq", nivel="provincia", mercado="alquiler de stock (SERPAVI)", medida="ln_alq_m2_serpavi_vc",
                          medida_precio=None, paneles=A.NOMBRES["provincia"]),
    "alq_municipio": dict(kind="alq", nivel="municipio", mercado="alquiler de stock (SERPAVI)", medida="ln_alq_m2_serpavi_mun",
                          medida_precio=None, paneles=A.NOMBRES["municipio"]),
    "alq_distrito": dict(kind="alq", nivel="distrito", mercado="alquiler de stock (SERPAVI)", medida="ln_alq_m2_serpavi_dis",
                         medida_precio=None, paneles=A.NOMBRES["distrito"]),
    "PROV_PRECIO_TRIM": dict(kind="cp", mercado="compra (precio)", nivel="provincia (trimestral)", medida="ln_pm2_tasado",
                             medida_precio="valor tasado MIVAU", paneles=["prov_trim_compra"]),
    "PROV_VOL_TRIM": dict(kind="cp", mercado="compra (volumen)", nivel="provincia (trimestral)", medida="ln_cv_etdp",
                          medida_precio=None, paneles=["prov_trim_compra"]),
    "PROV_PRECIO_ANUAL": dict(kind="cp", mercado="compra (precio)", nivel="provincia (anual)", medida="ln_pm2_tasado",
                              medida_precio="valor tasado MIVAU", paneles=["prov_compra_anual"]),
    "PROV_VOL_ANUAL": dict(kind="cp", mercado="compra (volumen)", nivel="provincia (anual)", medida="ln_cv_etdp",
                           medida_precio=None, paneles=["prov_compra_anual"]),
    "PROV_PRECIO_ANUAL_REGISTRADORES": dict(kind="cp", mercado="compra (precio)", nivel="provincia (anual)",
                                            medida="ln_pm2_registradores", medida_precio="Registradores (robustez)",
                                            paneles=["prov_compra_anual"]),
    "MUN_PRECIO_ANUAL": dict(kind="cp", mercado="compra (precio)", nivel="municipio (anual)", medida="ln_pm2_tasado_mun",
                             medida_precio="valor tasado MIVAU municipal", paneles=["mun_compra_anual", "prov_compra_anual"]),
}
BASES = {"persistencia": "persistencia", "ar_unidad": "AR por unidad (p<=4 por AIC)",
         "ecm_v1": "ECM v1 aproximado (agrupado, regresores t-1)",
         "m1_econ": "econometrico M1 (alquiler: M1A TWFE+tendencia; compra: M1B ADL con EF)"}


def prov_selladas():
    return ["99"] if MODO["dry"] else holdout.provincias_selladas_v6()


# ---------------------------------------------------------------- normalizacion de paneles sellados (mismo esquema que el entrenamiento)
def norm_sellado(s):
    out = {}
    for n, d in s.items():
        d = d.copy()
        if "cod" in d:
            d["cod"] = pd.to_numeric(d["cod"]).astype(int).astype(str).str.zfill(2)
        for c, w in (("cod_prov", 2), ("cod_mun", 5), ("distrito", 7)):
            if c in d:
                d[c] = d[c].astype(str).str.zfill(w)
        out[n] = d
    return out


def a_enteros(d):
    d = d.copy()
    for c in ("cod", "cod_prov"):
        if c in d:
            d[c] = pd.to_numeric(d[c]).astype(int)
    if "cod_mun" in d:
        d["cod_mun"] = pd.to_numeric(d["cod_mun"]).astype(int)
    return d


# ---------------------------------------------------------------- construccion de tareas
_CACHE = {}


def construir_alq(t, sell):
    nivel = t["nivel"]
    ex = norm_sellado(sell)
    if "tr" not in _CACHE.setdefault(nivel, {}):
        _CACHE[nivel]["tr"] = A.cargar(nivel)
    Ptr = _CACHE[nivel]["tr"]
    P = A.cargar(nivel, ex)
    claves = ex[A.NOMBRES[nivel][0]]
    kcol = {"provincia": "cod", "municipio": "cod_mun", "distrito": "distrito"}[nivel]
    ks = set(zip(claves[kcol].astype(str), claves.anio.astype(int)))
    va = P[[k in ks for k in zip(P.unit, P.anio)]].dropna(subset=["y", "y_lag1"]).copy()
    va["cod_prov"] = va.unit.str[:2]
    va["per"] = va.anio
    tr = Ptr.dropna(subset=["y"]).copy()
    return dict(P=P, ex=ex, tr=tr, va=va, corte=MODO["corte_alq"])


def construir_cp(t, sell):
    pc, cm, ca, tr, nac, mu, est, mest = B.cargar()
    s = {n: a_enteros(d) for n, d in sell.items()}
    keys = None
    if "prov_compra_anual" in s:
        sc = s["prov_compra_anual"]
        ca = pd.concat([ca, sc[[c for c in sc.columns if c in ca.columns]]], ignore_index=True).drop_duplicates(["cod", "anio"])
    if "prov_trim_compra" in s:
        st = s["prov_trim_compra"]
        tr = pd.concat([tr, st[[c for c in st.columns if c in tr.columns]]], ignore_index=True).drop_duplicates(["cod", "t"])
    if "mun_compra_anual" in s:
        sm = s["mun_compra_anual"]
        mu = pd.concat([mu, sm[[c for c in sm.columns if c in mu.columns]]], ignore_index=True).drop_duplicates(["cod_mun", "anio"])
    nid = t["_id"]
    if nid == "PROV_PRECIO_TRIM":
        S = B.S_trim("ln_pm2_tasado", "ln_cv_etdp", tr, nac, pc, nid, "compra (precio)", B.FUENTE_P, B.FUENTE_P)
    elif nid == "PROV_VOL_TRIM":
        S = B.S_trim("ln_cv_etdp", "ln_pm2_tasado", tr, nac, pc, nid, "compra (volumen)", "compraventas INE ETDP", None)
    elif nid == "PROV_PRECIO_ANUAL":
        S = B.S_anual("ln_pm2_tasado", "ln_cv_etdp", ca, pc, nid, "compra (precio)", B.FUENTE_P, B.FUENTE_P)
    elif nid == "PROV_VOL_ANUAL":
        S = B.S_anual("ln_cv_etdp", "ln_pm2_tasado", ca, pc, nid, "compra (volumen)", None, "compraventas INE ETDP")
    elif nid == "PROV_PRECIO_ANUAL_REGISTRADORES":
        S = B.S_anual("ln_pm2_registradores", "ln_cv_etdp", ca, pc, nid, "compra (precio)", "Registradores (robustez)", "Registradores pm2")
    else:
        S = B.S_mun(mu, ca, pc, cm, mest)
    D = S["D"].copy()
    if S["freq"] == "trimestral":
        k_s = {(int(r.cod), int(r.anio) * 4 + int(str(r.t)[-1]) - 1) for r in s["prov_trim_compra"].itertuples()}
        D["per"] = D.time.astype(int)
        D["cod_prov"] = D.unit.astype(int).astype(str).str.zfill(2)
        D["k"] = list(zip(D.unit.astype(int), D.per))
    elif nid == "MUN_PRECIO_ANUAL":
        k_s = {(int(r.cod_mun), int(r.anio)) for r in s["mun_compra_anual"].itertuples()}
        D["per"] = D.time.astype(int)
        D["cod_prov"] = D.unit.astype(str).str[:2]
        D["k"] = list(zip(D.unit.astype(int), D.per))
    else:
        k_s = {(int(r.cod), int(r.anio)) for r in s["prov_compra_anual"].itertuples()}
        D["per"] = D.time.astype(int)
        D["cod_prov"] = D.unit.astype(int).astype(str).str.zfill(2)
        D["k"] = list(zip(D.unit.astype(int), D.per))
    D["anio"] = D.per // 4 if S["freq"] == "trimestral" else D.per
    esv = D.k.isin(k_s)
    trn, va = D[~esv].copy(), D[esv].copy()
    return dict(S=S, tr=trn, va=va, corte=MODO["corte_cp"])


def grupo(va, corte):
    sel = va.cod_prov.isin(set(prov_selladas()))
    ult = va.anio >= corte
    g = np.where(sel & ~ult, "espacial", np.where(~sel & ult, "temporal", np.where(sel & ult, "conjunta", "otro")))
    return g


# ---------------------------------------------------------------- predictores
def pred_dl_m4(ruta, ficha, P, obj):
    """Como m3a_dl.predecir_dl, pero con el mapa de provincias del ENTRENAMIENTO (las no vistas usan la media de los
    embeddings entrenados). m3a_dl.predecir_dl reasigna pmap despues de construir pidx y falla con provincias nuevas."""
    import torch
    ck = torch.load(ruta, weights_only=False)
    T = DLM.tensores(P, ficha["variables"], ck["norm"])
    units = sorted(T["uid"], key=T["uid"].get)
    Pf = P[P.unit.isin(set(units))].drop_duplicates("unit").set_index("unit").loc[units]
    T["pidx"] = torch.tensor(Pf.cod_prov.map(lambda p: ck["pmap"].get(p, 0)).to_numpy(), dtype=torch.long)
    red = DLM.Red(T["X"].shape[2], ck["nprov"], ck["cfg"]["hidden"], 0.0, ck["grafo"])
    red.load_state_dict(ck["state"])
    with torch.no_grad():
        red.emb.weight[0] = red.emb.weight[1:].mean(0)
    return obj.y_lag1.to_numpy(float) + DLM.predecir_filas(red, T, obj, ck["dy_sd"])


def fe_base(trn, val, xs, tgt):
    """EF de unidad con pendientes comunes (como m3b_lib.fe_baseline); unidades nuevas -> NaN (el EF no esta identificado)."""
    A_ = trn[xs + [tgt]].to_numpy(float)
    u = pd.factorize(trn.unit)[0]
    Mt = A_ - pd.DataFrame(A_).groupby(u).transform("mean").to_numpy()
    b = np.linalg.lstsq(Mt[:, :-1], Mt[:, -1], rcond=None)[0]
    mu = trn.groupby("unit")[xs + [tgt]].mean()
    a_i = mu[tgt] - mu[xs].to_numpy() @ b
    ai = val.unit.map(a_i).to_numpy(float)  # unidad nueva -> NaN -> persistencia en `resumir` (declarado)
    pr = ai + val[xs].to_numpy(float) @ b
    return pr + val["y1"].to_numpy(float) if tgt == "dy" else pr


def pred_alq(rol, mid, t, T, ficha):
    nivel = t["nivel"]
    va, tr = T["va"], T["tr"]
    if rol == "modelo":
        if ficha["familia"] in ("dl_mlp", "dl_gnn"):
            p = pred_dl_m4(A.OUT / ficha["ruta_modelo"], ficha, T["P"], va)
            return va.assign(pred=p)
        r = A.predecir_modelo(mid, T["ex"])
        return va.merge(r[["unit", "anio", "pred"]], on=["unit", "anio"], how="left")
    reg = A.REGS_ECO[nivel]
    if mid == "persistencia":
        p = A.pred_persistencia(tr, va)
    elif mid == "ar_unidad":
        p = A.pred_ar(tr, va)
    elif mid == "ecm_v1":
        p = A.pred_ecm(tr, va, reg)
    else:
        p = A.pred_twfe(tr, va, reg)
    return va.assign(pred=p)


def pred_cp(rol, mid, t, T, ficha):
    S, va, tr = T["S"], T["va"], T["tr"]
    va = va.copy()
    sd = None
    if rol == "modelo":
        import joblib
        o = joblib.load(RAIZ / ficha["ruta"])
        X = va[o["spec"]["features"]].to_numpy(float)
        if hasattr(o["model"], "trees_"):
            d, sd = o["model"].predict(X, return_std=True)
        else:
            d = o["model"].predict(X)
        p = va.y1.to_numpy(float) + d
    elif mid == "persistencia":
        p = va.y1.to_numpy(float)
    elif mid == "ar_unidad":
        a_ = tr.rename(columns={"per": "anio_"}).assign(anio=tr.per)[["unit", "anio", "y"]]
        v_ = va.assign(anio=va.per, y_lag1=va.y1)[["unit", "anio", "y", "y_lag1"]]
        p = A.pred_ar(a_, v_)
    elif mid == "ecm_v1":
        if S["freq"] == "trimestral":
            xs, tg = S["base"]["ECMv1"]
            p = fe_base(tr, va, xs, tg)
        else:
            reg = [a + "_l1" for a in B.ADL_ANUAL]
            t2 = tr.assign(y_lag1=tr.y1, dy=tr.y - tr.y1)
            v2 = va.assign(y_lag1=va.y1)
            p = A.pred_ecm(t2, v2, reg)
    else:
        xs, tg = S["base"]["M1b_ADL"]
        p = fe_base(tr, va, xs, tg)
    va["pred"] = p
    if sd is not None:
        va["sd_bbf"] = sd
    return va


# ---------------------------------------------------------------- resumen
def resumir(df, corte, s_ref):
    df = df.copy()
    df["y1"] = df["y_lag1"] if "y_lag1" in df else df["y1"]
    nfb = int(df.pred.isna().sum())
    df["pred"] = df.pred.fillna(df.y1)  # fallback declarado: persistencia
    df["err"] = df.pred - df.y
    df["g"] = grupo(df, corte)
    df["cov"] = (df.err.abs() <= 1.96 * s_ref).astype(float)
    if "sd_bbf" in df:
        df["cov_bbf"] = (df.err.abs() <= 1.96 * df.sd_bbf).astype(float)
    met = {}
    for g in GRUPOS:
        d = df if g == "total" else df[df.g == g]
        if len(d) == 0:
            met[g] = {"n": 0, "rmse": None, "mae": None, "cobertura95": None}
            continue
        met[g] = {"n": int(len(d)), "rmse": float(np.sqrt(np.mean(d.err ** 2))), "mae": float(np.mean(d.err.abs())),
                  "cobertura95": float(d["cov"].mean()), "n_provincias": int(d.cod_prov.nunique()),
                  "sesgo": float(d.err.mean())}
        if "cov_bbf" in d:
            met[g]["cobertura95_banda_bosque"] = float(d.cov_bbf.mean())
    df["e2"], df["ae"] = df.err ** 2, df.err.abs()
    ce = df[df.g != "otro"].groupby(["cod_prov", "per", "g"]).agg(n=("err", "size"), sse=("e2", "sum"), sae=("ae", "sum"),
                                                                 cov=("cov", "sum"), anio=("anio", "first")).reset_index()
    cells = [dict(cod_prov=r.cod_prov, per=int(r.per), anio=int(r.anio), grupo=r.g, n=int(r.n), sse=float(r.sse), sae=float(r.sae),
                  cov=float(r["cov"])) for _, r in ce.iterrows()]
    return met, cells, nfb, int(len(df)), int((df.g == "otro").sum())


def evaluar(tid, rol, mid, ficha, s_ref, dry_sell=None):
    """Una llamada a evaluate_v6 (o ensayo) para (tarea, modelo)."""
    t = dict(TAREAS[tid], _id=tid)
    key = f"{tid}__{mid}" if rol == "base" else mid
    ruta = OUT / f"sellado_{key}.json"

    def fn(sell):
        try:
            T = construir_alq(t, sell) if t["kind"] == "alq" else construir_cp(t, sell)
            d = (pred_alq if t["kind"] == "alq" else pred_cp)(rol, mid, t, T, ficha)
            met, cells, nfb, n, nout = resumir(d, T["corte"], s_ref)
            res = dict(modelo_id=key, tarea=tid, rol=rol, modelo=mid, familia=(ficha or {}).get("familia", mid),
                       mercado=t["mercado"], nivel=t["nivel"], medida=t["medida"], medida_precio=t["medida_precio"],
                       corte_temporal=T["corte"], provincias_selladas=prov_selladas(), s_ref_intervalo=s_ref,
                       intervalo="pred +- 1,96 x RMSE de validacion en bloques del entrenamiento (cobertura empirica en el sellado)",
                       metricas=met, n_filas=n, n_fuera_de_grupo=nout, n_fallback_persistencia=nfb, celdas=cells,
                       validacion=("espacial nueva; temporal ya vista en v2 (otras provincias) y de forma descriptiva en v4-v5"),
                       capa="C4", estado="evaluado")
        except Exception as e:  # el sellado ya esta abierto: se registra el fallo en lugar de perderlo
            res = dict(modelo_id=key, tarea=tid, estado="fallo_tras_apertura", error=repr(e), traza=traceback.format_exc()[-1500:])
        if not MODO["dry"]:
            ruta.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float))
        return {"modelo_id": key, "estado": res["estado"], "metricas": res.get("metricas"), "fichero": str(ruta.relative_to(RAIZ)),
                "error": res.get("error"), "traza": res.get("traza")}

    if MODO["dry"]:
        r = fn(dry_sell)
        return r
    if ruta.exists():
        return {"modelo_id": key, "estado": "ya_evaluado"}
    return holdout.evaluate_v6(key, fn, "M4", t["paneles"])


# ---------------------------------------------------------------- lista de trabajo
def s_ref_de(tid, rol, mid):
    """RMSE de validacion en bloques (solo entrenamiento) para el intervalo."""
    if TAREAS[tid]["kind"] == "alq":
        m = pd.read_csv(RAIZ / "output/v6/M3A/metricas_validacion_interna.csv")
        m = m[(m.nivel == TAREAS[tid]["nivel"]) & (m.muestra == ("con_DL" if TAREAS[tid]["nivel"] == "distrito" else "sin_DL"))]
        nombre = {"persistencia": "persistencia", "ar_unidad": "AR_unidad", "ecm_v1": "ECM_v1_aprox", "m1_econ": "M1A_TWFE_tendencia"}.get(mid)
        if rol == "modelo":
            fam = mid.split("_", 2)[2]
            return float(m[m.modelo == {"mixto": "mixto_jerarquico"}.get(fam, fam)].rmse.iloc[0])
        return float(m[m.modelo == nombre].rmse.iloc[0])
    m = pd.read_csv(RAIZ / "output/v6/M3B/tablas/modelos_metricas.csv")
    m = m[m.setting == tid]
    if rol == "modelo":
        f = [x for x in json.loads((RAIZ / "output/v6/M3B/modelos_finales.json").read_text()) if x["id"] == mid][0]
        return float(f["rmse_ln_cv_bloques"])
    nombre = {"persistencia": "persistencia", "ar_unidad": "AR", "ecm_v1": "ECMv1" if tid.endswith("TRIM") else "M1b_ADL",
              "m1_econ": "M1b_ADL"}[mid]
    return float(m[m.modelo == nombre].rmse_ln.iloc[0])


def lista_trabajo():
    trab = []
    for f in json.loads((RAIZ / "output/v6/M3A/modelos_finales.json").read_text()):
        fi = json.loads((RAIZ / f["ruta"]).read_text())
        trab.append((f"alq_{f['nivel']}", "modelo", f["id"], fi))
    for f in json.loads((RAIZ / "output/v6/M3B/modelos_finales.json").read_text()):
        trab.append((f["especificacion"]["setting"], "modelo", f["id"], f))
    for tid in TAREAS:
        for b in BASES:
            trab.append((tid, "base", b, None))
    return trab


def fake_sellado(nombres):
    """Sellado FALSO para el ensayo: ultimo anio de entrenamiento + una provincia ficticia (99) copia de la 08."""
    out = {}
    for n in nombres:
        d = pd.read_csv(A.PAN / f"{n}_train.csv.gz", dtype={"cod": str, "cod_prov": str, "cod_mun": str, "distrito": str})
        ult = d[d.anio == d.anio.max()]
        if "cod" in d:
            base = d[d.cod == "08"].copy()
            base["cod"] = "99"
        elif "cod_prov" in d:
            base = d[d.cod_prov == "08"].copy()
            base["cod_prov"] = "99"
            for c in ("cod_mun", "distrito"):
                if c in base:
                    base[c] = "99" + base[c].str[2:]
        f = pd.concat([ult, base], ignore_index=True)
        if "cod" in f:
            f["cod"] = pd.to_numeric(f.cod).astype(int)
        out[n] = f
    return out


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else ""
    if modo not in ("--dry", "--real"):
        print(__doc__)
        return 2
    OUT.mkdir(parents=True, exist_ok=True)
    trab = lista_trabajo()
    if modo == "--dry":
        MODO.update(dry=True, corte_alq=int(pd.read_csv(A.PAN / "prov_alquiler_anual_train.csv.gz").dropna(subset=["ln_alq_m2_serpavi_vc"]).anio.max()),
                    corte_cp=int(pd.read_csv(A.PAN / "prov_compra_anual_train.csv.gz").anio.max()))
        sel = sys.argv[2:] or None
        for tid, rol, mid, fi in trab:
            key = f"{tid}__{mid}" if rol == "base" else mid
            if sel and not any(s in key for s in sel):
                continue
            r = evaluar(tid, rol, mid, fi, s_ref_de(tid, rol, mid), fake_sellado(TAREAS[tid]["paneles"]))
            m = r.get("metricas") or {}
            print(key, r["estado"], {g: (v["n"], round(v["rmse"], 4) if v["rmse"] is not None else None) for g, v in m.items()},
                  r.get("error") or "", flush=True)
            if r.get("traza"):
                print(r["traza"])
        return 0
    for tid, rol, mid, fi in trab:
        r = evaluar(tid, rol, mid, fi, s_ref_de(tid, rol, mid))
        print(r["modelo_id"], r["estado"], flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

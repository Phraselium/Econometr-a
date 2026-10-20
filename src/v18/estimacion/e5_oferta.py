"""V18 · E5 (oferta y suelo: Saiz 2010; Baum-Snow y Han 2024; Taltavull 2006) · elasticidad de la oferta con un Bartik de empleo, auge y caída.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18 (docs/v18/plan_replicacion.md, 1.5, + adenda R-17 y 1.13). SEED = 20261010; sin red.
Orden por especificación: (1) MDE (adenda 1.3) con la variación real del Bartik y del precio, SIN la variable resultado; (2) registro en el Registry; (3) estimación con inferencia por provincia
(Webb-AR + AR exacto; D-E359-7); (4) pruebas B4; (5) Holm por familia; (6) clasificación I1-I8 revisados (I8 pendiente).
Especificación: Δ ln Q_pt = ε·Δ ln P_pt + α_p + γ_t + u, con Δ ln P (valor tasado real) instrumentada por el Bartik de empleo B_pt = Σ_k s_pk,2001·g_kt(-p) de cuatro ramas
(A, B-E, G-J, O-U: sin construcción, finanzas, inmobiliarias ni servicios profesionales; D-E359-2 y D-E5-1); Q = viviendas libres iniciadas; 2002-2023; sin pesos.
Lecturas: todas pasan por _e359_comun.filtrar (sellado.filtrar + holdout.excluir_sellados_v6()).
Salidas: output/v18/estimacion/e5/{resultado.json, tabla.csv, informe.md, hechos.json, registro.csv, mde.csv}.
Uso: python3 src/v18/estimacion/e5_oferta.py [--rapido]
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e359_comun as K  # noqa: E402
import _e359_datos as D  # noqa: E402

SALIDA = K.OUT / "e5"
RAPIDO = "--rapido" in sys.argv
B_WEBB = 999 if RAPIDO else 9999
R_MDE = 500 if RAPIDO else 2000
SECTORES = ["A", "B-E", "G-J", "O-U"]
REF = dict(v=0.87, se=0.125, nombre="Taltavull (2006), panel de CCAA 1990-2004, elasticidad de los inicios", estado="NO VERIFICADA", delta=0.435, unidad="elasticidad")
PRE = list(range(1996, 2002))
TOPE_Q4 = "tope SUGESTIVO: Bartik en lugar de la Red Natura tras Q4 (adenda 1.6)"


class DatosE5:
    def __init__(self):
        self.P = list(K.PROVINCIAS_ENTRENAMIENTO)
        self.vt = D.valor_tasado_anual(self.P)
        self.ini = D.iniciadas_anual(self.P)
        self.ter = D.terminadas_anual(self.P)
        self.defl = D.deflactor_anual()
        self.emp = D.empleo_entrenamiento(self.P)           # (cod, rama) × año, solo provincias de entrenamiento
        self.emp_nac = D.empleo_nacional()
        pop = D.poblacion_edad(self.P)
        self.tot = pop.xs("TOTAL", level="age")
        self.p65 = pop.xs("Y_GE65", level="age")
        tot01 = self.emp.xs("TOTAL", level="nace_r2")[2001]
        self.s = pd.DataFrame({k: self.emp.xs(k, level="nace_r2")[2001] / tot01 for k in SECTORES}).reindex(self.P)
        self.s10 = None
        self.macro = pd.Series({p: K.MACRO[p] for p in self.P})

    def g(self, p: str, k: str, t: int) -> float:
        """Crecimiento (ln) del empleo nacional de la rama k entre t-1 y t sin la provincia p."""
        a1 = self.emp_nac.at[k, t] - self.emp.at[(p, k), t]
        a0 = self.emp_nac.at[k, t - 1] - self.emp.at[(p, k), t - 1]
        return float(np.log(a1 / a0))

    def _y(self, cfg: dict, p: str, t: int):
        ty = cfg["y"]
        try:
            if ty in ("dlnq", "dlnter"):
                s = self.ini if ty == "dlnq" else self.ter
                a, b = float(s.at[p, t]), float(s.at[p, t - 1])
                return float(np.log(a / b)) if a > 0 and b > 0 else None
            if ty == "dln65":
                return float(np.log(self.p65.at[p, t] / self.p65.at[p, t - 1]))
        except (KeyError, ValueError, ZeroDivisionError):
            return None
        raise ValueError(ty)

    def _x(self, p: str, t: int):
        try:
            return float(np.log(self.vt.at[p, t] / self.defl[t]) - np.log(self.vt.at[p, t - 1] / self.defl[t - 1]))
        except (KeyError, ValueError):
            return None

    def bartik(self, p: str, t: int, lag: int = 0):
        tt = t - lag
        comp = np.array([self.s.at[p, k] * self.g(p, k, tt) for k in SECTORES])
        return comp

    def panel(self, cfg: dict) -> dict:
        t0, t1 = cfg["ventana"]
        excl = set(cfg.get("excl_prov", []))
        filas = []
        for p in self.P:
            if p in excl:
                continue
            for t in range(t0, t1 + 1):
                y = self._y(cfg, p, t)
                x = self._x(p, t)
                if y is None or x is None or not np.isfinite(y) or not np.isfinite(x):
                    continue
                try:
                    comp = self.bartik(p, t, cfg.get("lag_instr", 0))
                except KeyError:
                    continue
                if not np.all(np.isfinite(comp)):
                    continue
                filas.append((p, t, y, x, comp))
        prov = np.array([f[0] for f in filas])
        año = np.array([f[1] for f in filas])
        y = np.array([f[2] for f in filas])
        x = np.array([f[3] for f in filas])
        zc = np.vstack([f[4] for f in filas])
        w = None
        if cfg.get("peso") == "pob2001":
            w = self.tot[2001].reindex(prov).to_numpy(float)
        C, cols = self._C(prov, año)
        return {"y": y, "x": x, "z": zc.sum(axis=1), "zc": zc, "prov": prov, "año": año, "w": w, "C": C, "cols": cols}

    def _C(self, prov, año):
        a = pd.get_dummies(pd.Series(prov), dtype=float)
        b = pd.get_dummies(pd.Series(año), dtype=float)
        return np.hstack([a.to_numpy(), b.to_numpy()]), [f"prov:{c}" for c in a.columns] + [f"año:{c}" for c in b.columns]

    def pre(self, cfg: dict, años: list[int]) -> dict:
        prov, año, y = [], [], []
        for p in self.P:
            if p in set(cfg.get("excl_prov", [])):
                continue
            for t in años:
                yy = self._y(cfg, p, t)
                if yy is None or not np.isfinite(yy):
                    continue
                prov.append(p)
                año.append(t)
                y.append(yy)
        prov, año, y = np.array(prov), np.array(año), np.array(y)
        w = None if cfg.get("peso") != "pob2001" else self.tot[2001].reindex(prov).to_numpy(float)
        C, _ = self._C(prov, año)
        return {"y": y, "prov": prov, "año": año, "w": w, "C": C}

    def z_en(self, prov, año, desfase: int) -> np.ndarray:
        out = np.full(len(prov), np.nan)
        for i, (p, t) in enumerate(zip(prov, año)):
            try:
                out[i] = float(self.bartik(p, int(t) + desfase).sum())
            except KeyError:
                pass
        return out


def construir_specs() -> list[dict]:
    S = []

    def add(id_, rol, cfg, padre=None, tope=None, nota="", ne=None, holgura=False):
        S.append(dict(id=id_, rol=rol, cfg=dict(cfg, id=id_), padre=padre, tope=tope, nota=nota, ne=ne, holgura=holgura))

    base = dict(ventana=(2002, 2023), y="dlnq", peso=None)
    add("E5-R1", "principal", base, tope=TOPE_Q4, nota="repite_visto (elección del instrumento tras Q4); Bartik de 4 ramas; 2002-2023; sin pesos")
    add("E5-R1-v1", "variante", dict(base, ventana=(2002, 2007)), padre="E5-R1", nota="auge 2002-2007")
    add("E5-R1-v2", "variante", dict(base, ventana=(2008, 2013)), padre="E5-R1", nota="caída 2008-2013")
    add("E5-R1-v3", "variante", dict(base, ventana=(2014, 2023)), padre="E5-R1", nota="2014-2023")
    add("E5-R1-v4", "variante", base, padre="E5-R1", ne="los diez sectores A*10: a escala NUTS 3 Eurostat solo da seis ramas")
    add("E5-R1-v5", "variante", dict(base, lag_instr=1), padre="E5-R1", nota="Bartik retardado un año (B_{p,t-1})")
    add("E5-R1-v6", "variante", dict(base, y="dlnter"), padre="E5-R1", nota="terminadas en lugar de iniciadas")
    add("E5-R1-v7", "variante", dict(base, excl_prov=["08"]), padre="E5-R1", nota="sin Barcelona")
    add("E5-R1-v8", "variante", dict(base, excl_prov=["03", "29", "17"]), padre="E5-R1", nota="sin Alicante, Málaga y Girona")
    add("E5-R1-v9", "variante", dict(base, peso="pob2001"), padre="E5-R1", nota="ponderada por la población de 2001")
    add("E5-R1-v10", "variante", base, padre="E5-R1", ne="exposición a cajas de 2007 × año: no está en el repositorio")
    add("E5-R1-v11", "variante", dict(base, ventana=(2009, 2023)), padre="E5-R1", nota="2009-2023 (la variante de secciones CNAE-2009 con afiliación no existe: se ejecuta como ventana)")
    return S


def precomprobar(dat: DatosE5, spec: dict) -> dict:
    pan = dat.panel(spec["cfg"])
    dis = K.DisenoIV(pan["y"], pan["x"], pan["z"], pan["prov"], C=pan["C"], w=pan["w"], B=1)
    pre = dat.pre(spec["cfg"], PRE)
    sig, rho = K.sigma_rho_de_panel(pre["y"], pre["prov"], pre["año"], pre["C"], pre["w"])
    m = K.mde_iv(dis, pan["año"][dis.orden], sig, rho, R=R_MDE)
    sc = (np.abs(pan["zc"])).sum(axis=0)
    m.update({"ref": REF["v"], "estimable": bool(m["mde80"] <= REF["v"]), "n": dis.n, "G": dis.G, "k": dis.k, "n_pre": len(pre["y"]), "F_eff": dis.f_efectivo(),
              "inv_hhi_sector": K.inv_hhi(sc), "pesos_sector": {k: float(v) for k, v in zip(SECTORES, sc / sc.sum())}, "n_sectores": len(SECTORES)})
    return m


def estimar(dat: DatosE5, spec: dict, completo: bool, B: int = B_WEBB) -> dict:
    pan = dat.panel(spec["cfg"])
    dis = K.DisenoIV(pan["y"], pan["x"], pan["z"], pan["prov"], C=pan["C"], w=pan["w"], B=B)
    r = dis.resumen(con_ic=True, con_ic90=completo)
    r["pan"], r["dis"] = pan, dis
    return r


def diag_principal(dat: DatosE5, spec: dict, r: dict, B: int) -> dict:
    cfg = spec["cfg"]
    pan, dis = r["pan"], r["dis"]
    ic = (r["ic_webb_ar"]["lo"], r["ic_webb_ar"]["hi"])
    out = {}
    pre = dat.pre(cfg, PRE)
    dfp = pd.DataFrame({"p": pre["prov"], "y": pre["y"]}).groupby("p")["y"].mean()
    # pretendencia: B medio de 2002-2007 sobre Δ ln Q medio de 1996-2001, con efectos de macrorregión
    zb = {}
    for p in dat.P:
        v = [dat.bartik(p, t).sum() for t in range(2002, 2008)]
        zb[p] = float(np.mean(v))
    zbar = pd.DataFrame({"p": pan["prov"], "x": pan["x"]}).groupby("p")["x"].mean()
    com = [p for p in dfp.index if p in zbar.index and p in zb]
    reg = np.array([K.MACRO[p] for p in com])
    zz = np.array([zb[p] for p in com])
    out["pretendencia"] = K.pendiente_previa(dfp.loc[com].to_numpy(), zz, zbar.loc[com].to_numpy(), reg, None, B=B)
    out["pretendencia"]["roth_ok"] = bool(out["pretendencia"]["sesgo_detectable_beta"] < 0.5 * REF["v"])
    # placebo de fecha: B de t + 6 sobre Δ ln Q del preperiodo (efectos provincia y año)
    zf = dat.z_en(pre["prov"], pre["año"], 6)
    ok = np.isfinite(zf)
    Cp, _ = dat._C(pre["prov"][ok], pre["año"][ok])
    out["placebo_fecha"] = K.placebo_fecha(pre["y"][ok], zf[ok], pre["prov"][ok], Cp, None, r["rf"], B=B)
    # placebo de resultado: población de 65 años o más
    c65 = dict(cfg, y="dln65")
    p65 = dat.panel(c65)
    d65 = K.DisenoIV(p65["y"], p65["x"], p65["z"], p65["prov"], C=p65["C"], w=p65["w"], B=B)
    r65 = d65.iv()
    out["placebo_resultado"] = {"coef": r65["beta"], "se": r65["se"], "p_webb_ar": d65.webb_ar_p(0.0), "p_ar_exacto": d65.ar_exacto()["p_beta0"], "n": r65["n"]}
    # Rotemberg y exclusión del sector de más peso (D-E5-2)
    ZC = np.column_stack([dis._m(dis.sw * pan["zc"][dis.orden, j]) for j in range(pan["zc"].shape[1])])
    rot = K.rotemberg(ZC, dis.xt, dis.yt)
    alpha = rot["alpha"]
    top = [int(np.argmax(np.abs(alpha)))]
    keep = [j for j in range(len(alpha)) if j not in top]
    z2 = pan["zc"][:, keep].sum(axis=1)
    d2 = K.DisenoIV(pan["y"], pan["x"], z2, pan["prov"], C=pan["C"], w=pan["w"], B=B)
    r2 = d2.iv()
    ic2 = d2.ic_webb_ar(0.05, centro=r2["beta"], escala=r2["se"])
    out["rotemberg"] = {"alpha": {k: float(a) for k, a in zip(SECTORES, alpha)}, "excluidos": [SECTORES[j] for j in top], "beta_sin_top": r2["beta"], "se": r2["se"], "F_eff": d2.f_efectivo(),
                        "ic_webb_ar": ic2, "mismo_signo": bool(np.sign(r2["beta"]) == np.sign(r["beta"])), "dentro_ic": bool(ic[0] <= r2["beta"] <= ic[1])}
    # sin atípicos
    d = pd.DataFrame({"p": pan["prov"], "z": pan["z"], "y": pan["y"]}).groupby("p").mean()
    at = sorted({d["z"].idxmax(), (d["y"] - d["y"].median()).abs().idxmax()})
    pa = dat.panel(dict(cfg, excl_prov=list(set(cfg.get("excl_prov", [])) | set(at))))
    da = K.DisenoIV(pa["y"], pa["x"], pa["z"], pa["prov"], C=pa["C"], w=pa["w"], B=B)
    ra = da.iv()
    out["sin_atipicos"] = {"excluidas": at, "beta": ra["beta"], "se": ra["se"], "mismo_signo": bool(np.sign(ra["beta"]) == np.sign(r["beta"])), "n": ra["n"]}
    out["bhj"] = {"nota": "BHJ a nivel de sector: 4 ramas (< 10 choques): el Monte Carlo de V18 deja NO APTO el BHJ con 10-30 choques; no se calcula"}
    return out


def a1_preparar(dat: DatosE5) -> dict:
    """E5-A1: Δ ln P_pt = φ·Z_pt + ψ·Z_pt·S_p + efectos de provincia y año, 2014-2022, con Z = el instrumento de inmigración de E3-A1 y S_p = solares por vivienda en 2012 (Catastro, municipios
    de entrenamiento), estandarizada. Forma reducida de MCO: ASOCIACIÓN como máximo; fuera de la familia de Holm (adenda 1.7). Devuelve el diseño y su MDE; no estima ψ."""
    import e3_inmigracion as E3
    import e3_panel as EP
    d3 = EP.DatosE3()
    pan = d3.panel(E3.cfg_a1())
    c = pd.read_csv(K.RAW / "v4" / "catastro_solares_municipios.csv.gz", dtype=str)
    c["periodo"] = c["anio"].astype(str)
    c["cod"] = c["cod_mun"].astype(str).str.zfill(5)
    for col in ("uu_solar", "uu_res"):
        c[col] = pd.to_numeric(c[col], errors="coerce")
    c = K.filtrar(c[["cod", "periodo", "uu_solar", "uu_res"]], "cod", "municipio", "periodo", "catastro_solares", "A")
    c12 = c[c["periodo"] == "2012"].copy()
    c12["prov"] = c12["cod"].str[:2]
    S = c12.groupby("prov")[["uu_solar", "uu_res"]].sum()
    Sp = (S["uu_solar"] / S["uu_res"]).reindex(d3.P)
    Sz = (Sp - Sp.mean()) / Sp.std()
    y = np.array([_ylnp(dat, p, t) for p, t in zip(pan.prov, pan.año)])
    S_i = Sz.reindex(pan.prov).to_numpy(float)
    ok = np.isfinite(y) & np.isfinite(S_i)
    Z = pan.z[ok]
    zs = Z * S_i[ok]
    prov, año = pan.prov[ok], pan.año[ok]
    Cc, _ = dat._C(prov, año)
    Cc = np.column_stack([Cc, Z])
    dis = K.DisenoIV(y[ok], zs, zs, prov, C=Cc, B=B_WEBB)
    # σ y ρ del preperiodo 2009-2013 (Δ ln P real) con efectos de provincia y año
    pr, aa, yy = [], [], []
    for p_ in dat.P:
        for t_ in range(2009, 2014):
            v = _ylnp(dat, p_, t_)
            if np.isfinite(v):
                pr.append(p_)
                aa.append(t_)
                yy.append(v)
    Cpre, _ = dat._C(np.array(pr), np.array(aa))
    sig, rho = K.sigma_rho_de_panel(np.array(yy), np.array(pr), np.array(aa), Cpre, None)
    m = K.mde_iv(dis, año[dis.orden], sig, rho, R=R_MDE)
    m.update({"ref": 0.10, "estimable": bool(m["mde80"] <= 0.10), "n": dis.n, "G": dis.G, "k": dis.k, "F_eff": float("nan"),
              "nota_unidad": "ψ en Δ ln P real por punto de Z y por desviación típica de S; sin referencia: umbral 2δ = 0,10 (δ = 0,05 en log, Anexo B)",
              "S_media": float(Sp.mean()), "S_sd": float(Sp.std())})
    return {"dis": dis, "mde": m}


def _ylnp(dat: DatosE5, p: str, t: int) -> float:
    try:
        return float(np.log(dat.vt.at[p, t] / dat.defl[t]) - np.log(dat.vt.at[p, t - 1] / dat.defl[t - 1]))
    except (KeyError, ValueError):
        return float("nan")


def a1_estimar(dis: K.DisenoIV) -> dict:
    r = dis.iv()
    p = dis.webb_ar_p(0.0)
    ic = dis.ic_webb_ar(0.05, centro=r["beta"], escala=r["se"])
    return {"psi": r["beta"], "se": r["se"], "p_webb": p, "p_t": r["p_t"], "ic_webb": (ic["lo"], ic["hi"]), "n": r["n"], "G": r["G"]}


def f_por_ventana(dat: DatosE5, spec: dict) -> dict:
    """F efectivo del Bartik (solo primera etapa: no usa el resultado) por ventana de auge y caída, como información de la NO ESTIMABLE."""
    out = {}
    for nombre, v in (("2002-2007", (2002, 2007)), ("2008-2013", (2008, 2013)), ("2014-2023", (2014, 2023)), ("2002-2023", (2002, 2023))):
        pan = dat.panel(dict(spec["cfg"], ventana=v))
        d = K.DisenoIV(pan["y"], pan["x"], pan["z"], pan["prov"], C=pan["C"], w=pan["w"], B=1)
        out[nombre] = {"F_eff": d.f_efectivo(), "n": d.n}
    return out


def main() -> int:
    t0 = time.time()
    dat = DatosE5()
    specs = construir_specs()
    reg = K.Registry(SALIDA / "registro.csv")
    mde_tab, res, ne = {}, {}, {}
    for s in specs:
        reg.log("v18-E5", f"{s['id']}|registrada", f"Δln Q ~ Δln P real | Bartik 4 ramas ({s['cfg']['y']}, {s['cfg']['ventana']})", s["cfg"]["ventana"][0], s["cfg"]["ventana"][1], 0, np.nan,
                np.nan, np.nan, notas=s["rol"])
        if s["ne"]:
            ne[s["id"]] = s["ne"]
            continue
        if s["rol"] == "principal":
            m = precomprobar(dat, s)
            mde_tab[s["id"]] = m
            if not m["estimable"]:
                ne[s["id"]] = ("NO ESTIMABLE por variación: " + (f"MDE {m['mde80']:.3g}" if np.isfinite(m["mde80"]) else "MDE superior a seis errores típicos de referencia (no se alcanza el 80 % de potencia)")
                               + f" frente a |referencia| {m['ref']:.3g}")
            print(f"[{time.time() - t0:5.0f}s] MDE {s['id']}: {m['mde80']:.4g} (ref {m['ref']}); F {m['F_eff']:.1f}; 1/HHI sectores {m['inv_hhi_sector']:.2f}", flush=True)
    for sid, motivo in (("E5-R2", "restricciones físicas (MDT05, agua, costa) y de planeamiento (SIU) no están en el repositorio"),
                        ("E5-A2", "Atlas de áreas urbanas del MIVAU (`posterior_prereg`) no descargado; la unidad exige el valor tasado y la obra nueva por área"),
                        ("E5-A3", "afiliación municipal por sección de la CNAE anterior a 2011-12 no agregada en el repositorio (solo tres ramas); el Bartik municipal no se puede construir"),
                        ("E5-P-Q4a", "la Red Natura municipal de V16 solo existe como panel de entrenamiento de V16 (data/processed/v16) y su variable no figura en docs/v18/sellado_v18.json: no se puede leer con sellado.filtrar")):
        ne[sid] = motivo
        reg.log("v18-E5", f"{sid}|registrada", "NO ESTIMABLE", 0, 0, 0, np.nan, np.nan, np.nan, notas=motivo)
    for s in specs:
        if s["id"] in ne:
            continue
        if s["padre"] and s["padre"] in ne:
            ne[s["id"]] = f"su principal {s['padre']} es NO ESTIMABLE"
            continue
        res[s["id"]] = estimar(dat, s, completo=(s["rol"] == "principal"))
        r = res[s["id"]]
        reg.log("v18-E5", f"{s['id']}|estimada", f"2SLS por provincia; Webb-AR ({B_WEBB}) + AR", s["cfg"]["ventana"][0], s["cfg"]["ventana"][1], r["n"], np.nan, np.nan, np.nan,
                coef_interes=r["beta"], p_interes=max(r["p_webb_ar"], r["ar"]["p_beta0"]), notas=s["nota"])
        print(f"[{time.time() - t0:5.0f}s] {s['id']}: n={r['n']} G={r['G']} F={r['F_eff']:.1f}", flush=True)
    a1p = a1_preparar(dat)
    mde_tab["E5-A1"] = a1p["mde"]
    reg.log("v18-E5", "E5-A1|registrada", "reducida Δln P ~ Z + Z·S (2014-2022)", 2014, 2022, a1p["mde"]["n"], np.nan, np.nan, np.nan, notas="principal; ASOCIACIÓN como máximo; fuera de Holm")
    print(f"[{time.time() - t0:5.0f}s] MDE E5-A1: {a1p['mde']['mde80']:.4g} (umbral {a1p['mde']['ref']})", flush=True)
    a1 = None
    if a1p["mde"]["estimable"]:
        a1 = a1_estimar(a1p["dis"])
        reg.log("v18-E5", "E5-A1|estimada", "reducida Δln P ~ Z + Z·S", 2014, 2022, a1["n"], np.nan, np.nan, np.nan, coef_interes=a1["psi"], p_interes=a1["p_webb"], notas="ASOCIACIÓN como máximo; fuera de Holm")
    else:
        ne["E5-A1"] = f"NO ESTIMABLE por variación: MDE {a1p['mde']['mde80']:.3g} > umbral 2δ = 0,10 (sin referencia, Anexo B)"
    fven = f_por_ventana(dat, specs[0])
    print(f"[{time.time() - t0:5.0f}s] F por ventana: " + ", ".join(f"{k} {v['F_eff']:.2f}" for k, v in fven.items()), flush=True)
    import e5_salidas as SAL
    SAL.escribir(sys.modules[__name__], dat, specs, mde_tab, res, ne, a1, fven, reg, B_WEBB, t0)
    return 0


if __name__ == "__main__":
    sys.exit(main())

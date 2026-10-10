"""Potencia (EMD vs EER) de los diseños P-C1..P-C4. Determinista, sin red. Uso: python src/v3/pot_run.py [--smoke]
Sellado v3 excluido ANTES de calcular (gl_data.carga). Nunca se lee la oleada 2026M05."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gl_data as g  # noqa: E402

import holdout  # noqa: E402
from econ_utils import Registry  # noqa: E402

OUT = g.RAIZ / "output/v3/POT"
OUT.mkdir(parents=True, exist_ok=True)
SMOKE = "--smoke" in sys.argv
REPS = 100 if SMOKE else 500
Z = stats.norm.ppf(0.975) + stats.norm.ppf(0.80)   # 2,8016
reg = Registry(OUT / "registro.csv")
rows = []
EER = {"P-C1": 0.01, "P-C2": 0.01 / 0.1, "P-C3_alquiler": 0.03, "P-C3_contratos": 0.10, "P-C4": 0.1}


def sums(zt, xt, et, cl):
    """Sumas por clúster para FWL con un regresor (instrumento zt, regresor xt, residuo et)."""
    f, G = pd.factorize(cl)[0], len(set(cl))
    return (np.bincount(f, zt * et, G), np.bincount(f, zt * xt, G), G)


def estima(zt, xt, yt, cl):
    Sze, Szx, G = sums(zt, xt, yt, cl)
    Szx = np.bincount(pd.factorize(cl)[0], zt * xt, G)
    b = Sze.sum() / Szx.sum()
    Szy_b = Sze - b * Szx
    V = (Szy_b ** 2).sum() / Szx.sum() ** 2 * G / (G - 1)
    return b, float(np.sqrt(V)), G


def potencia_sim(zt, xt, yt, cl, delta, reps=REPS):
    """Bootstrap de clústeres (bloques) con residuos reales; añade delta*x; devuelve frecuencia de rechazo al 5 %."""
    b0, _, _ = estima(zt, xt, yt, cl)
    e = yt - b0 * xt
    Sze, Szx, G = sums(zt, xt, e, cl)
    rng = np.random.default_rng(g.SEED)
    tc = stats.t.ppf(0.975, G - 1)
    rej = 0
    for _ in range(reps):
        c = np.bincount(rng.integers(0, G, G), minlength=G)
        Sy = Sze + delta * Szx
        den = (c * Szx).sum()
        if abs(den) < 1e-12:
            continue
        b = (c * Sy).sum() / den
        V = (c * (Sy - b * Szx) ** 2).sum() / den ** 2 * G / (G - 1)
        rej += abs(b / np.sqrt(V)) > tc
    return rej / reps


def fila(diseno, spec, n, G, se, eer, unidad, nota="", emd_sim=None, pot=None, F=np.nan, coef=np.nan):
    emd = Z * se if np.isfinite(se) else np.inf
    ver = "estimable" if emd <= eer else "no detectable con los datos disponibles"
    rows.append(dict(diseno=diseno, especificacion=spec, N=n, clusters=G, ee=se, emd=emd, eer=eer, unidad=unidad,
                     potencia_sim_en_emd=pot, F_1a_etapa=F, veredicto=ver, nota=nota))
    reg.log("POT", f"{diseno}:{spec}", "EMD=2,8016*EE_cluster", 2021, 2024, n, np.nan, np.nan, np.nan,
            coef_interes=emd, p_interes=np.nan, notas=f"{ver}; EER={eer}; {unidad}; {nota}")


# --------------------------------------------------------------------------- P-C1
def pc1():
    prov = ["08"] if SMOKE else None
    sec, perd = g.carga("seccion", prov)
    ciu = {"08019": "Barcelona", "28079": "Madrid", "46250": "València", "41091": "Sevilla", "29067": "Málaga",
           "07040": "Palma"}
    def ols(p, nombre, nota=""):
        if p.distrito.nunique() < 3:
            return
        r = g.fe_cluster(p, "lnalq", ["vut100"])
        zt = g.demean2(p, ["vut100"])["vut100"].values
        yt = g.demean2(p, ["lnalq"])["lnalq"].values
        pot = potencia_sim(zt, zt, yt, p.distrito.values, Z * r["se"][0])
        fila("P-C1", nombre, r["n"], r["G"], float(r["se"][0]), EER["P-C1"], "log-puntos de alquiler por 1 pp VUT/viviendas",
             nota + f"; sd residual VUT tras FE={zt.std():.3f}; coef={r['b'][0]:.4f}", pot=pot)
    ols(sec, "OLS FE sección+año, nacional" if not SMOKE else "OLS FE, prov. 08 (smoke)")
    gr = sec[sec.muni.isin(ciu)]
    ols(gr, "OLS FE, 6 ciudades grandes (pool)", "cluster distrito")
    for m, n in ciu.items():
        ols(sec[sec.muni == m], f"OLS FE, {n}")
    # shift-share leave-one-out
    s = sec.sort_values(["codigo", "anio"]).copy()
    share = s[s.anio == 2021].set_index("codigo").eval("100*vut/viv").rename("share0")
    s = s.join(share, on="codigo")
    for nivel, col in (("municipio", "muni"), ("provincia", "prov")):
        t = s.groupby([col, "anio"]).agg(V=("vut", "sum"), H=("viv", "sum")).reset_index()
        s2 = s.merge(t, on=[col, "anio"])
        s2["Vr"] = s2.V - s2.vut
        s2["Hr"] = s2.H - s2.viv
        s2["rest"] = 100 * s2.Vr / s2.Hr
        base = s2[s2.anio == 2021].set_index("codigo").rest.rename("rest0")
        s2 = s2.join(base, on="codigo")
        s2["z"] = s2.share0 * (s2.rest - s2.rest0)     # cuota inicial x variación (por 100 viv.) del resto
        s2 = s2.replace([np.inf, -np.inf], np.nan).dropna(subset=["z"])
        for nm, sub in ((f"shift-share LOO {nivel}, nacional", s2), (f"shift-share LOO {nivel}, 6 ciudades", s2[s2.muni.isin(ciu)])):
            ok = sub.groupby("codigo").anio.nunique()
            sub = sub[sub.codigo.isin(ok[ok == 4].index)]
            if sub.distrito.nunique() < 3:
                continue
            d = g.demean2(sub, ["lnalq", "vut100", "z"])
            zt, xt, yt = d.z.values, d.vut100.values, d.lnalq.values
            b, se, G = estima(zt, xt, yt, sub.distrito.values)
            b1, se1, _ = estima(zt, zt, xt, sub.distrito.values)
            pot = potencia_sim(zt, xt, yt, sub.distrito.values, Z * se)
            fila("P-C1", nm, len(sub), G, se, EER["P-C1"], "log-puntos por 1 pp VUT (2SLS)",
                 f"coef 2SLS={b:.4f}; sd z tras FE={zt.std():.3f}", pot=pot, F=(b1 / se1) ** 2)
    return perd


# --------------------------------------------------------------------------- P-C2
def pc2():
    d = g.D
    mx = {}
    s = pd.read_csv(d / "serpavi_distritos_nacional_v3.csv.gz", usecols=["periodo"])
    mx["serpavi_distrito_max_anio"] = int(s.periodo.max())
    i = pd.read_csv(d / "incasol_fianzas_municipio_v3.csv.gz", usecols=["periodo"])
    mx["incasol_max_anio_nivel_municipal"] = int(i.periodo.str[:4].max())
    m = pd.read_csv(d / "madrid_alquiler_cp_v3.csv.gz", usecols=["periodo"])
    mx["madrid_cp_periodos"] = sorted(map(str, m.periodo.unique()))
    a = pd.read_csv(d / "airbnb_insideairbnb_agregados_v3.csv.gz", usecols=["fecha"])
    mx["insideairbnb_rango"] = [a.fecha.min(), a.fecha.max()]
    fino_post_2025 = False   # SERPAVI acaba en 2024; Incasòl es municipal; Madrid CP 2023-2024
    nota = (f"Resultado de alquiler a escala fina posterior a 2025: {'sí' if fino_post_2025 else 'NO'}. {json.dumps(mx)}. "
            "Incasòl llega a 2026 pero solo a escala municipal y las capturas Inside Airbnb empiezan en 2025-12 (sin periodo previo).")
    fila("P-C2", "caída de anuncios 2025-2026 -> alquiler fino", 0, 0, np.inf, EER["P-C2"],
         "log-puntos de alquiler por 1 de caída log de anuncios", nota)
    return mx


# --------------------------------------------------------------------------- P-C3
def fwl(df, y, x, fe=("mun", "anio")):
    """Residualiza y,x sobre FE de municipio y año (desbalanceado: dummies + lstsq)."""
    D = pd.get_dummies(df[list(fe)].astype(str), drop_first=False).astype(float).values
    out = []
    for c in (y, x):
        v = df[c].values.astype(float)
        out.append(v - D @ np.linalg.lstsq(D, v, rcond=None)[0])
    return out[0], out[1]


def incasol():
    f = pd.read_csv(g.D / "incasol_fianzas_municipio_v3.csv.gz",
                    usecols=["periodo", "serie", "valor", "codigo", "banda"], dtype={"codigo": str})
    f = f[f.periodo.str.endswith("gener-desembre")].copy()
    f["anio"] = f.periodo.str[:4].astype(int)
    f["tipo"] = f.serie.str.split("_").str[3]
    n = f[(f.tipo == "n") & (f.banda == "TOTAL_bandas")].groupby(["codigo", "anio"]).valor.sum().rename("n")
    nb = f[(f.tipo == "n") & (f.banda != "TOTAL_bandas")].set_index(["codigo", "anio", "banda"]).valor.rename("nb")
    r = f[f.tipo == "renta"].set_index(["codigo", "anio", "banda"]).valor.rename("renta")
    j = pd.concat([nb, r], axis=1).dropna()
    j["w"] = j.nb * j.renta
    rent = (j.groupby(level=[0, 1]).w.sum() / j.groupby(level=[0, 1]).nb.sum()).rename("alq")
    p = pd.concat([n, rent], axis=1).reset_index().rename(columns={"codigo": "mun"})
    p = p[(p.n > 0) & (p.alq > 0)]
    p["lnalq"], p["lnn"] = np.log(p.alq), np.log(p.n)
    return p[p.mun != "08019"]       # como Jofre-Monseny et al. (2023): sin Barcelona


def pc3():
    p = incasol()
    z = pd.read_csv(g.D / "zonas_tensionadas_v3.csv", dtype={"cod_ine_municipio": str})
    z = z[z.ccaa == "Cataluña"].copy()
    z["mun"] = z.cod_ine_municipio.str.zfill(5)
    z["f"] = pd.to_datetime(z.fecha_efecto)
    z = z.groupby("mun").f.min()
    res = {}
    # (a) topes 2020-2022: lista 2020 NO disponible en data/ -> proxy: 58 municipios zonificados con más contratos en 2019
    pre = p[(p.anio.between(2016, 2019))]
    bal = pre.groupby("mun").anio.nunique()
    bal = bal[bal == 4].index
    n19 = p[p.anio == 2019].set_index("mun").n
    prox = [m for m in n19.sort_values(ascending=False).index if m in z.index and m in bal][:58]
    q = p[p.anio.between(2016, 2022) & p.mun.isin(bal)].copy()
    q["post"] = q.anio.map({2020: 0.27, 2021: 1.0, 2022: 0.2}).fillna(0.0)
    q["D"] = q.mun.isin(prox) * q.post
    q = q[q.groupby("mun").anio.transform("nunique") == 7]
    # (b) zonas tensionadas 2024-2025 (tratamiento observado en eventos/zonas)
    w = p[p.anio.between(2016, 2025) & p.mun.isin(bal)].copy()
    w = w[w.groupby("mun").anio.transform("nunique") == 10]
    def frac(row):
        if row.mun not in z.index:
            return 0.0
        ini = z[row.mun]
        a0 = pd.Timestamp(row.anio, 1, 1)
        a1 = pd.Timestamp(row.anio, 12, 31)
        return float(np.clip((a1 - ini).days / 365.0, 0, 1)) if ini <= a1 else 0.0
    w["D"] = w.apply(frac, axis=1)
    for dis, d, nombre, nota in (("a", q, "topes Ley 11/2020 (2016-2022)", "PROXY de tratados (58 mayores zonificados); la lista 2020 no está en data/"),
                                 ("b", w, "zonas tensionadas (2016-2025)", "tratamiento = fracción del año con zona declarada")):
        ntr = int(d.loc[d.D > 0, "mun"].nunique())
        for var, eer, lab in (("lnalq", EER["P-C3_alquiler"], "alquiler"), ("lnn", EER["P-C3_contratos"], "contratos")):
            if ntr < 3:
                continue
            yt, xt = fwl(d, var, "D")
            b, se, G = estima(xt, xt, yt, d.mun.values)
            pot = potencia_sim(xt, xt, yt, d.mun.values, Z * se)
            fila("P-C3", f"{nombre} -> {lab}", len(d), G, se, eer, "log-puntos (efecto = coef de D)",
                 f"{nota}; tratados={ntr}, controles={d.mun.nunique() - ntr}; coef={b:.4f}; "
                 "renta = media ponderada de medias de banda (bandas cambian entre años)", pot=pot)
    return {"tratados_proxy_topes": len(prox)}


# --------------------------------------------------------------------------- P-C4
def pc4():
    p = holdout.load_full("panel_prov_a", "POT")
    p = p[p.anio.between(2003, 2025)].copy()
    sz = p.groupby("cod_prov").p_suelo.mean().rename("zsuelo")
    p = p.join(sz, on="cod_prov")
    p["zl"] = np.log(p.zsuelo)
    for shock in ("d_ln_ocupados", "d_ln_pob_total"):
        d = p.dropna(subset=["d_ln_p_tasado", shock, "zl"]).copy()
        d = d[d.groupby("cod_prov").anio.transform("count") >= 10]
        d["int"] = d[shock] * (d.zl - d.zl.mean())
        iqr = float(d.drop_duplicates("cod_prov").zl.quantile(.75) - d.drop_duplicates("cod_prov").zl.quantile(.25))
        d["cod_prov"] = d.cod_prov.astype(str)
        # FWL: partir "int" y y de FE prov+año y del shock
        D = pd.get_dummies(d[["cod_prov", "anio"]].astype(str)).astype(float)
        D = np.column_stack([D.values, d[shock].values])
        out = []
        for c in ("d_ln_p_tasado", "int"):
            v = d[c].values.astype(float)
            out.append(v - D @ np.linalg.lstsq(D, v, rcond=None)[0])
        yt, xt = out
        b, se, G = estima(xt, xt, yt, d.cod_prov.values)
        pot = potencia_sim(xt, xt, yt, d.cod_prov.values, Z * se)
        # EMD en unidades del EER: diferencia de elasticidad entre p75 y p25 de ln p_suelo = coef * IQR
        fila("P-C4", f"{shock} x ln p_suelo", len(d), G, se * iqr, EER["P-C4"],
             "diferencia de elasticidad p75-p25 de ln(p_suelo)",
             f"coef interacción={b:.4f}; IQR ln p_suelo={iqr:.2f}; p_suelo = media provincial (invariante)", pot=pot)


def main():
    perd = pc1()
    mx = pc2()
    extra = pc3()
    pc4()
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "potencia.csv", index=False)
    md = ["# Potencia de P-C (EMD vs EER)", "",
          "EMD = (z_0,975 + z_0,80) x EE clúster = 2,8016 x EE; EE de datos reales tras efectos fijos; potencia verificada por "
          f"bootstrap de clústeres con residuos reales ({REPS} réplicas, SEED=20261010) añadiendo un efecto igual al EMD "
          "(columna potencia_sim_en_emd, objetivo ≈ 0,80). Sellado v3 (distritos y 2026M05) excluido antes de calcular. "
          "Capa: C4 (potencia, no estimación de efectos).", "",
          df[["diseno", "especificacion", "N", "clusters", "emd", "eer", "potencia_sim_en_emd", "F_1a_etapa", "veredicto"]]
          .round(4).to_markdown(index=False), "", "## Notas por fila", ""]
    md += [f"- {r.diseno} / {r.especificacion}: {r.unidad}. {r.nota}" for r in df.itertuples()]
    md += ["", f"Pérdidas de armonización P-C1 (secciones): {json.dumps(perd)}", "",
           "Advertencia P-C1: SERPAVI es stock IRPF y amortigua el alquiler; si el efecto sobre el stock es una fracción k del "
           "efecto sobre contratos nuevos, el EMD relevante es EMD/k (peor). VUT INE cubre ~89-90 % (error de medida, sesgo a 0)."]
    (OUT / "potencia.md").write_text("\n".join(md))
    ver = {d_: sorted(set(df[df.diseno == d_].veredicto)) for d_ in df.diseno.unique()}
    res = dict(rama="POT", capa="C4", pregunta="¿Tienen los diseños P-C potencia para detectar el EER?",
               datos="SERPAVI sec/distrito, INE VUT, Censo 2021, Incasòl, zonas tensionadas, panel_prov_a (load_full)",
               N=int(df.N.max()), metodo="EMD analítico con EE clúster + bootstrap de clústeres (500 réplicas)",
               estimacion=None, ic95=None, p_ajustado=None, nivel_evidencia="DESCRIPTIVO",
               diagnosticos=dict(veredictos=ver, filas=df.drop(columns=["nota"]).to_dict("records"), p2=mx, p3=extra),
               fuera_muestra=dict(modelo=None, rmse=None, dm_vs_ar4=None, nota="no aplica: cálculo de potencia"),
               notas=f"Smoke={SMOKE}. P-C3a con tratados PROXY. Pérdidas: {perd}")
    (OUT / "resultado.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    reg.flush()
    print(df[["diseno", "especificacion", "N", "clusters", "emd", "eer", "potencia_sim_en_emd", "F_1a_etapa", "veredicto"]].round(4).to_string())


if __name__ == "__main__":
    main()

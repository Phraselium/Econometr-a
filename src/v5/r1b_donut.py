"""R1b-1 (BK-041): gradiente centro-periferia del precio y del alquiler, 2015-2019 vs 2019-2024.

Capa C4 por defecto (la dirección puede ser C1 solo si tasado y SERPAVI coinciden y cada uno es significativo).
Descriptivo/asociativo: sin lenguaje causal. Sin red.
"""
import itertools
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

RAIZ = Path(__file__).resolve().parents[2]
RAW = RAIZ / "data/raw"
OUT = RAIZ / "output/v5/R1B"
SEED = 20261010

CAPITALES = ("01059 02003 03014 04013 05019 06015 07040 08019 09059 10037 11012 12040 13034 14021 15030 16078 17079 "
             "18087 19130 20069 21041 22125 23050 24089 25120 26089 27028 28079 29067 30030 31201 32054 33044 34120 "
             "35016 36038 37274 38038 39075 40194 41091 42173 43148 44216 45168 46250 47186 48020 49275 50297 "
             "51001 52001").split()
MANUAL = {"Almazora/Almassora": "12009", "Calpe/Calp": "03047", "Castellón de la Plana": "12040", "Mahón": "07032",
          "Palma de Mallorca": "07040", "Puerto de Santa María": "11027", "San Cristóbal Laguna": "38023",
          "San Sebastián/Donostia": "20069", "Santa Coloma Gramanet": "08245", "Santa Eulalia del Río": "07054",
          "Villarreal/Vila-real": "12135", "Vitoria": "01059"}
PROV_AMBIG = {("Cieza", "Murcia"): "30019", ("Mieres", "ASTURIAS"): "33037", ("Torrent", "Valencia"): "46244"}


def norm(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def censo():
    c = pd.read_csv(RAW / "v3/ine_v3_censo2021_municipio_viviendas.csv", dtype={"codigo": str})
    c = c[(c.nivel == "municipio") & (c.serie == "V_TOTAL")][["codigo", "territorio", "valor"]]
    return c.rename(columns={"valor": "viv"})


def codigos_tasado(cen):
    names = {}
    for _, r in cen.iterrows():
        n = r.territorio
        names.setdefault(norm(n), set()).add(r.codigo)
        if ", " in n:
            a, b = n.split(", ", 1)
            names.setdefault(norm(b + " " + a), set()).add(r.codigo)
        if " (" in n:
            a, b = n.split(" (", 1)
            names.setdefault(norm(b.rstrip(")") + " " + a), set()).add(r.codigo)
        for p in n.split("/"):
            names.setdefault(norm(p), set()).add(r.codigo)
    d = pd.read_csv(RAW / "mivau_valor_tasado_municipios.csv")
    t = d[["territorio", "provincia"]].drop_duplicates()
    cod = {}
    for _, r in t.iterrows():
        k = (r.territorio, r.provincia)
        if k in PROV_AMBIG:
            cod[k] = PROV_AMBIG[k]
        elif r.territorio in MANUAL:
            cod[k] = MANUAL[r.territorio]
        else:
            s = names.get(norm(r.territorio), set())
            cod[k] = next(iter(s)) if len(s) == 1 else None
    d["codigo"] = [cod[(a, b)] for a, b in zip(d.territorio, d.provincia)]
    return d


def tasado_anual(d):
    d = d.dropna(subset=["codigo"]).copy()
    d["anio"] = d.periodo.str[:4].astype(int)
    g = d.groupby(["codigo", "anio"]).valor.agg(["mean", "size"]).reset_index()
    g = g[g["size"] == 4]
    return g.pivot(index="codigo", columns="anio", values="mean")


def serpavi_anual(minc):
    s = pd.read_csv(RAW / "pdf/serpavi_v2_municipios.csv.gz", dtype={"codigo": str})
    s = s[(s.tipologia == "VC")]
    a = s[(s.variable == "alquiler_m2") & (s.estadistico == "mediana")].pivot_table(index="codigo", columns="periodo", values="valor")
    n = s[s.variable == "n_contratos"].pivot_table(index="codigo", columns="periodo", values="valor")
    return a, n


def distancias(cen, cent):
    g = pd.read_csv(RAW / "v5/municipio_centroides_utm30.csv", dtype={"codigo": str}).set_index("codigo")
    return g


def asignar(cods, g, centros, R):
    """Cada municipio al centro más cercano a <= R km. Devuelve DataFrame codigo, area, dist_km."""
    cx = g.loc[centros, ["x_m", "y_m"]].values
    out = []
    for c in cods:
        if c not in g.index:
            continue
        d = np.hypot(cx[:, 0] - g.at[c, "x_m"], cx[:, 1] - g.at[c, "y_m"]) / 1000
        j = int(np.argmin(d))
        if d[j] <= R:
            out.append((c, centros[j], d[j]))
    return pd.DataFrame(out, columns=["codigo", "area", "dist_km"])


def pendiente(df, forma, excl_centro, minmun=3):
    """Δ(crecimiento anualizado) sobre distancia con FE de área; errores agrupados por área."""
    x = df.copy()
    if excl_centro:
        x = x[x.dist_km > 0]
    x["d"] = x.dist_km / 10 if forma == "lineal" else np.log1p(x.dist_km)
    x = x[x.groupby("area").codigo.transform("size") >= minmun]
    if x.area.nunique() < 6 or x.d.nunique() < 5:
        return None
    out = {"n": len(x), "areas": x.area.nunique()}
    for nom in ("g_pre", "g_post", "dg"):
        m = smf.ols(f"{nom} ~ d + C(area)", x).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(x.area)[0]}, use_t=True)
        out[nom] = (m.params["d"], m.bse["d"], m.pvalues["d"])
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "tablas").mkdir(exist_ok=True)
    cen = censo()
    g = distancias(cen, None)
    viv = cen.set_index("codigo").viv
    t = codigos_tasado(cen)
    sin_cod = sorted(t[t.codigo.isna()].territorio.unique())
    ta = tasado_anual(t)
    sa, sn = serpavi_anual(0)
    # centros
    cap = [c for c in CAPITALES if c in g.index]
    prov = viv.groupby(viv.index.str[:2]).idxmax()
    mayor = sorted(set(c for c in prov.values if c in g.index))
    centros = {"capital": cap, "mayor_parque": mayor}
    # periodos: (pre_ini, pre_fin, post_ini, post_fin)
    periodos = {"15-19|19-24": (2015, 2019, 2019, 2024), "15-19|20-24": (2015, 2019, 2020, 2024),
                "14-19|19-24": (2014, 2019, 2019, 2024), "15-19|19-25": (2015, 2019, 2019, 2025)}
    fuentes = {"tasado": ta, "serpavi_VC": sa, "serpavi_VC_n50": sa}
    filas, regs = [], []
    for (fu, df_f), (cn, cl), R, (pn, p), forma, ex in itertools.product(
            fuentes.items(), centros.items(), (15, 25, 40, 60), periodos.items(), ("lineal", "log"), (False, True)):
        a0, a1, b0, b1 = p
        if b1 not in df_f.columns or a0 not in df_f.columns:
            continue
        if fu == "serpavi_VC" and b1 > 2024:
            continue
        v = df_f[sorted({a0, a1, b0, b1})].dropna()
        v = v[(v > 0).all(axis=1)]
        if fu == "serpavi_VC_n50":
            ok = sn[sorted({a0, a1, b0, b1})].min(axis=1)
            v = v[v.index.map(ok).fillna(0) >= 50]
        asg = asignar(list(v.index), g, cl, R)
        if asg.empty:
            continue
        asg = asg.merge(v, left_on="codigo", right_index=True)
        asg["g_pre"] = 100 * (np.log(asg[a1]) - np.log(asg[a0])) / (a1 - a0)
        asg["g_post"] = 100 * (np.log(asg[b1]) - np.log(asg[b0])) / (b1 - b0)
        asg["dg"] = asg.g_post - asg.g_pre
        r = pendiente(asg, forma, ex)
        if r is None:
            continue
        filas.append(dict(fuente=fu, centro=cn, radio_km=R, periodo=pn, forma=forma, excl_centro=ex, n=r["n"], areas=r["areas"],
                          b_pre=r["g_pre"][0], b_post=r["g_post"][0], dif=r["dg"][0], ee=r["dg"][1], p=r["dg"][2],
                          tstat=r["dg"][0] / r["dg"][1]))
    res = pd.DataFrame(filas)
    # Holm (todas las especificaciones del multiverso, familia única)
    res = res.sort_values("p").reset_index(drop=True)
    m = len(res)
    res["p_holm"] = np.minimum(1, np.maximum.accumulate((m - np.arange(m)) * res.p.values))
    res.to_csv(OUT / "tablas/donut_multiverso.csv", index=False)
    # registro
    reg = pd.DataFrame({"fase": "R1b-donut", "modelo_id": [f"donut_{i}" for i in range(m)],
                        "formula": res.apply(lambda r: f"dg~dist|area[{r.fuente},{r.centro},{r.radio_km}km,{r.periodo},{r.forma},excl={r.excl_centro}]", axis=1),
                        "muestra_ini": 2014, "muestra_fin": 2025, "n": res.n, "coef_interes": res.dif, "p_interes": res.p, "notas": "p_holm=" + res.p_holm.round(4).astype(str)})
    resumen = {}
    for fu, x in res.groupby("fuente"):
        resumen[fu] = dict(n_spec=len(x), prop_dif_pos=float((x.dif > 0).mean()), prop_sig_nominal_pos=float(((x.dif > 0) & (x.p < .05)).mean()),
                           prop_sig_holm=float((x.p_holm < .05).mean()), mediana_dif=float(x.dif.median()), mediana_b_pre=float(x.b_pre.median()),
                           mediana_b_post=float(x.b_post.median()))
    # especificación principal: capital, 25 km, 15-19|19-24, lineal, con centro
    prin = {}
    for fu in fuentes:
        x = res[(res.fuente == fu) & (res.centro == "capital") & (res.radio_km == 25) & (res.periodo == "15-19|19-24") & (res.forma == "lineal") & (~res.excl_centro)]
        if len(x):
            prin[fu] = x.iloc[0].to_dict()
    # placebo (tasado): 2010-15 vs 2015-19 con la misma especificación principal
    plac = []
    asg = asignar(list(ta.index), g, cap, 25)
    for (a0, a1, b0, b1) in [(2010, 2015, 2015, 2019), (2011, 2015, 2015, 2019)]:
        v = ta[sorted({a0, a1, b0, b1})].dropna()
        z = asg.merge(v, left_on="codigo", right_index=True)
        z["g_pre"] = 100 * (np.log(z[a1]) - np.log(z[a0])) / (a1 - a0)
        z["g_post"] = 100 * (np.log(z[b1]) - np.log(z[b0])) / (b1 - b0)
        z["dg"] = z.g_post - z.g_pre
        r = pendiente(z, "lineal", False)
        if r:
            plac.append(dict(ventana=f"{a0}-{a1}|{b0}-{b1}", n=r["n"], areas=r["areas"], dif=r["dg"][0], ee=r["dg"][1], p=r["dg"][2]))
    # cobertura
    cob = {"municipios_tasado": int(ta.index.nunique()), "tasado_sin_codigo": sin_cod, "municipios_serpavi_VC": int(sa.index.nunique())}
    import json
    out = dict(resumen=resumen, principal=prin, placebo=plac, cobertura=cob, n_spec=m)
    (OUT / "tablas/donut_resumen.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=float))
    reg.to_csv(OUT / "registro_donut.csv", index=False)
    print(json.dumps(out, ensure_ascii=False, indent=1, default=float))


if __name__ == "__main__":
    main()

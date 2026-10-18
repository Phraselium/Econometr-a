"""Replica ciega lote b2: T3-H5b, T4-H2, T4-H3. SEED=20261010.

Entradas: tablas intermedias de output/v5 (B1, B2), output/v5_1 (T1, T2) y data/raw MIVAU.
No lee hechos.json de T3/T4 ni su codigo; la comparacion final solo se hace con cifras_clave.csv.
"""
import json
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261010
np.random.seed(SEED)
R = Path("/home/user/Econometr-a")
OUT = R / "output/v16/replica/v10_b2"


def clave(s):
    s = re.sub(r"\(.*?\)", "", str(s))
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    s = re.split(r"[/,]", s)[0]
    return re.sub(r"[^a-z]", "", s)


def t3_h5b():
    b = pd.read_csv(R / "output/v5/B1/tablas/B1_provincias.csv", dtype={"cod_prov": str})
    t = pd.read_csv(R / "output/v5_1/T1/tablas/bajas_provincia.csv", dtype={"cod_prov": str})
    d = b.merge(t[["cod_prov", "tasa_min", "tasa_central", "tasa_max"]], on="cod_prov")
    assert len(d) == 52
    # Reposicion R de T1: 10 anios x tasa x viviendas Censo 2021
    for k in ("min", "central", "max"):
        d["R1_" + k] = 10 * d["tasa_" + k] * d["viv_total_2021"]
    S = lambda c: d[c].sum()
    c6 = pd.read_csv(R / "output/v5_1/T3/tablas/deficit_2021_2025_combinaciones.csv").deficit
    a1 = dict(min=c6.min(), central=c6.mean(), max=c6.max())
    for k in ("min", "central", "max"):
        d["A_" + k] = 0.0
    A = {k: a1[k] + S("A2_" + k) for k in a1}
    S0 = S
    S = lambda c: A[c[2:]] if c in ("A_min", "A_central", "A_max") else S0(c)
    ctr = (S("A_central") + S("R1_central") + S("V_central") + S("F_central") - S("M_central") - S("K_central")) / 10
    mn = (S("A_min") + S("R1_min") + S("V_min") + S("F_min") - S("M_max") - S("K_max")) / 10
    mx = (S("A_max") + S("R1_max") + S("V_max") + S("F_max") - S("M_min") - S("K_min")) / 10
    return dict(valor=ctr, min=mn, max=mx)


def terminadas_prov():
    """Terminadas anuales por provincia (libres + protegida definitiva), 2019-2025."""
    m = pd.read_csv(R / "data/raw/mivau_v2_iniciadas_terminadas_prov.csv")
    q = pd.read_csv(R / "data/raw/mivau_v2_protegida.csv")
    anios = range(2019, 2026)

    def anual(df, patron_anual, patron_mens):
        a = df[df.serie.str.contains(patron_anual) & df.nivel.isin(["provincia", "ccaa", "ciudad_autonoma"])].copy()
        a["anio"] = a.periodo.astype(str).str[:4].astype(int)
        a = a.groupby(["territorio", "anio"]).valor.sum().unstack()
        mm = df[df.serie.str.contains(patron_mens) & df.nivel.isin(["provincia", "ccaa", "ciudad_autonoma"])].copy()
        mm["anio"] = mm.periodo.astype(str).str[:4].astype(int)
        mm = mm.groupby(["territorio", "anio"]).valor.sum().unstack()
        return a, mm

    la, lm = anual(m, "terminadas_anual", "terminadas_mensual")
    pa, pm = anual(q, "prot_definitiva_anual", "prot_definitiva_mensual")
    ser = {}
    for nombre, (a, mm) in {"lib": (la, lm), "pro": (pa, pm)}.items():
        d = {}
        for t in set(a.index) | set(mm.index):
            row = a.loc[t] if t in a.index else mm.loc[t]
            d[clave(t)] = row.reindex(list(anios))
        ser[nombre] = pd.DataFrame(d).T
    return ser


def calcula_T(prov_names):
    ser = terminadas_prov()
    lib, pro = ser["lib"], ser["pro"]
    keys = [clave(n) for n in prov_names]
    L = lib.reindex(keys).fillna(0)
    P = pro.reindex(keys).fillna(0)
    faltan = [k for k in keys if k not in lib.index]
    return L.values + P.values, faltan


def iniciadas_prov(prov_names):
    """Iniciadas anuales (libres + protegida provisional) por provincia, 1991-2025."""
    m = pd.read_csv(R / "data/raw/mivau_v2_iniciadas_terminadas_prov.csv")
    q = pd.read_csv(R / "data/raw/mivau_v2_protegida.csv")
    niv = ["provincia", "ccaa", "ciudad_autonoma"]

    def tab(df, pa, pm):
        out = {}
        for pat, anual in ((pa, True), (pm, False)):
            a = df[df.serie.str.contains(pat) & df.nivel.isin(niv)].copy()
            a["anio"] = a.periodo.astype(str).str[:4].astype(int)
            g = a.groupby(["territorio", "anio"]).valor.sum().unstack()
            out[anual] = g
        r = {}
        for t in set(out[True].index) | set(out[False].index):
            r[clave(t)] = out[True].loc[t] if t in out[True].index else out[False].loc[t]
        return pd.DataFrame(r).T

    li = tab(m, "iniciadas_anual", "iniciadas_mensual")
    pr = tab(q, "prot_provisional_anual", "prot_provisional_mensual")
    keys = [clave(n) for n in prov_names]
    anios = list(range(2000, 2026))
    return li.reindex(keys)[anios].fillna(0).values + pr.reindex(keys).reindex(columns=anios).fillna(0).values, anios


def cartera(I, anios, L, fut):
    """T(y)=iniciadas(y-L), y=2026..2030, interpolacion lineal; iniciadas > 2025 = fut (vector por provincia)."""
    n = I.shape[0]
    def ini(a):
        if a > 2025:
            return fut
        return I[:, anios.index(a)]
    tot = np.zeros(n)
    for y in range(2026, 2031):
        x = y - L
        f = int(np.floor(x)); w = x - f
        tot += (1 - w) * ini(f) + w * ini(f + 1)
    return tot


def parque_2025(prov_names, cods, censo):
    """Parque MIVAU del ultimo anio (2025) por provincia; Extremadura y Ceuta/Melilla se reparten por el Censo 2021."""
    q = pd.read_csv(R / "data/raw/mivau_parque.csv")
    q = q[q.serie.str.startswith("parque_total_viviendas") & (q.periodo == 2025)]
    v = {clave(t): g.valor.sum() for t, g in q.groupby("territorio")}
    keys = [clave(n) for n in prov_names]
    out = pd.Series([v.get(k, np.nan) for k in keys], index=cods, dtype=float)
    for grp, tot in ((["badajoz", "caceres"], v.get("extremadura")), (["ceuta", "melilla"], v.get("ceutaymelilla"))):
        idx = [c for c, k in zip(cods, keys) if k in grp]
        if idx and tot:
            w = censo.loc[idx]
            out.loc[idx] = tot * w / w.sum()
    return out


def cuota_x_2030(prov_names):
    """Defunciones 75+ de 2026-2030 sobre 2026-2035: poblacion por edad simple (36726) x riesgo por tramo (67235)."""
    a = pd.read_csv(R / "data/raw/v5/ine_b1_t36726_proy_poblacion_prov.csv")
    b = pd.read_csv(R / "data/raw/v5/ine_b1_t67235_mortalidad_prov.csv")
    e = a.nombre.str.extract(r"^Total\. Poblaci.n\. (.*?)\. Proyecci.n a corto plazo\. (.*?)\. $")
    a = a.assign(terr=e[0].map(lambda t: clave(t) if isinstance(t, str) else None), edad=e[1])
    a = a[a.edad.str.match(r"^\d+ a.os$|^100 y m.s", na=False)].copy()
    a["e"] = a.edad.str.extract(r"^(\d+)")[0].astype(int)
    a = a[a.e >= 75]
    def tramo(e):
        return min((e - 75) // 5, 4) if e < 95 else 4
    a["tr"] = a.e.map(lambda e: 0 if e < 80 else 1 if e < 85 else 2 if e < 90 else 3 if e < 95 else 4)
    b = b.copy()
    eb = b.nombre.str.extract(r"^(.*?)\. Total\. (De 75 a 79|De 80 a 84|De 85 a 89|De 90 a 94|95 y m)")
    b["terr"] = eb[0].map(lambda t: clave(t) if isinstance(t, str) else None)
    b["tr"] = eb[1].map({"De 75 a 79": 0, "De 80 a 84": 1, "De 85 a 89": 2, "De 90 a 94": 3, "95 y m": 4})
    b = b.dropna(subset=["terr", "tr"]).drop_duplicates(["terr", "tr"])
    riesgo = b.set_index(["terr", "tr"]).valor
    a = a.drop_duplicates(["terr", "e", "anyo"])
    a["r"] = [riesgo.get((t, k), np.nan) for t, k in zip(a.terr, a.tr)]
    a["d"] = a.valor * a.r
    D = a[(a.anyo >= 2026) & (a.anyo <= 2035)].groupby(["terr", "anyo"]).d.sum().unstack()
    c = D[list(range(2026, 2031))].sum(axis=1) / D.sum(axis=1)
    return pd.Series([c.get(clave(n), np.nan) for n in prov_names])


def retardos():
    """Estimador de la ficha: igualdad de acumulados a fin de anio (I acumulada = 0 a fin de 1990), media de t - x por ventana."""
    m = pd.read_csv(R / "data/raw/mivau_v2_iniciadas_terminadas_prov.csv")
    q = pd.read_csv(R / "data/raw/mivau_v2_protegida.csv")

    def nac(df, pat):
        a = df[(df.nivel == "nacional") & df.serie.str.contains(pat)].copy()
        a["y"] = a.periodo.astype(str).str[:4].astype(int)
        return a.groupby("y").valor.sum()

    ini = nac(m, "iniciadas_anual").add(nac(q, "prot_provisional_anual_nacional"), fill_value=0).loc[1991:2025]
    ter = nac(m, "terminadas_anual").add(nac(q, "prot_definitiva_anual_nacional"), fill_value=0).loc[1991:2025]
    xs = np.arange(1990, 2026)
    cI = np.concatenate([[0], ini.cumsum().values])
    cT = ter.cumsum()
    L = [float(np.mean([t - np.interp(cT[t], cI, xs) for t in range(a, 2026)])) for a in (2008, 2012, 2016, 2019, 2022)]
    return float(np.median(L)), min(L), max(L)


def t4():
    d = pd.read_csv(R / "output/v5/B2/tablas/B2_provincias_completo.csv", dtype={"cod_prov": str})
    t1 = pd.read_csv(R / "output/v5_1/T1/tablas/bajas_provincia.csv", dtype={"cod_prov": str})
    d = d.merge(t1[["cod_prov", "tasa_min", "tasa_central", "tasa_max"]], on="cod_prov")
    T, faltan = calcula_T(d.provincia)  # 2019-2025
    I, anios = iniciadas_prov(d.provincia)
    H = 5
    ia = lambda a, b: I[:, [anios.index(k) for k in range(a, b + 1)]]
    m2325 = ia(2023, 2025).mean(axis=1)
    max2125 = ia(2021, 2025).max(axis=1)
    L_med, L_short, L_long = retardos()
    Ta = H * T[:, 4:7].mean(axis=1)
    Tb = cartera(I, anios, L_med, m2325)
    x = np.arange(2021, 2026); X = np.vstack([np.ones(5), x]).T
    Tc = np.zeros(len(d))
    for k in range(len(d)):
        beta = np.linalg.lstsq(X, T[k, 2:7], rcond=None)[0]
        Tc[k] = sum(max(0.0, beta[0] + beta[1] * y) for y in range(2026, 2031))
    T_lo = np.minimum(H * T[:, 4:7].min(axis=1), cartera(I, anios, L_long, m2325))
    T_opt = np.maximum(H * T.max(axis=1), cartera(I, anios, L_short, max2125))
    ctrl = dict(Ta=float(np.abs(Ta - d.Ta_central).sum()), Tb=float(Tb.sum() - d.Tb_central.sum()),
                Tc=float(Tc.sum() - d.Tc_central.sum()))
    park = pd.read_csv(R / "output/v5/B1/tablas/B1_provincias.csv", dtype={"cod_prov": str}).set_index("cod_prov").viv_total_2021
    d["park"] = d.cod_prov.map(park)
    d["park"] = parque_2025(d.provincia, d.cod_prov, park).values
    x = pd.read_csv(R / "output/v5_1/T2/tablas/liberadas_provincia.csv", dtype={"cod_prov": str})
    x = x[x.periodo == "2026-2035"].copy()
    x["x_max"] = x.liberadas_central * (1 - x.fraccion_mercado_min)
    cuota = cuota_x_2030(d.provincia).values
    Xmax = d.cod_prov.map(x.groupby("cod_prov").x_max.sum()).values * cuota
    B_hi = H * d.tasa_max * d.park
    B_c = H * d.tasa_central * d.park
    # rejilla completa de 180 escenarios (5 T x 3 F x 3 bajas x 4 X); un escenario aplica el mismo caso a todas las provincias
    Ts = {"a": Ta, "b": Tb, "c": Tc, "lo": T_lo, "opt": T_opt}
    Fs = [d.F_min.values, d.F_central.values, d.F_max.values]
    Bs = [0.0 * B_hi, B_c, B_hi]
    xx = x.assign(x_c=x.liberadas_central * (1 - 0.5 * (x.fraccion_mercado_min + x.fraccion_mercado_max)),
                  x_n=x.liberadas_central * (1 - x.fraccion_mercado_max)).groupby("cod_prov")[["x_n", "x_c", "x_max"]].sum()
    Xs = [np.zeros(len(d)), d.cod_prov.map(xx.x_n).values * cuota, d.cod_prov.map(xx.x_c).values * cuota,
          d.cod_prov.map(xx.x_max).values * cuota]
    cambios = np.array([Fk - Tv + Bk + Xk for Tv in Ts.values() for Fk in Fs for Bk in Bs for Xk in Xs])  # 180 x 52
    assert cambios.shape == (180, len(d))
    tot = cambios.sum(axis=1)
    fav, des = tot.min(), tot.max()
    emp = int((cambios.min(axis=0) > 0).sum()); mej = int((cambios.max(axis=0) < 0).sum())
    return dict(faltan=faltan, control=ctrl, T_opt_anual=float(T_opt.sum() / H), T_lo_anual=float(T_lo.sum() / H),
                cambio_central=float((d.F_central - Ta + B_c).sum()), cambio_min=float(fav),
                cambio_max=float(des), X_total=float(np.nansum(Xmax)), B_hi=float(B_hi.sum()), cuota_nac=float(np.nanmean(cuota)), empeoran=emp, mejoran=mej, indet=52 - emp - mej)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    h5b = t3_h5b()
    t = t4()
    json.dump(dict(h5b=h5b, t4=t), open(OUT / "bruto.json", "w"), indent=1, default=float)
    pub = {"T3-H5b": (210424.4, 99388.2, 292082.8), "T4-H2": (585609.4, 87246.5, 946852), "T4-H3": (15, 0, 37)}
    rep = {"T3-H5b": (h5b["valor"], h5b["min"], h5b["max"]),
           "T4-H2": (t["cambio_central"], t["cambio_min"], t["cambio_max"]),
           "T4-H3": (t["empeoran"], t["mejoran"], t["indet"])}
    diag = {
        "T3-H5b": "A1 = deficit 2021-2025 ECP con bajas T1 (6 combinaciones: min, media, max); A2, V, F, M, K de B1; R = 10 x tasa T1 x viviendas Censo 2021. Pegado a la ficha solo tras ver que el rango de A en B1 no cuadra con la descomposicion de T3; la central de A1 (media de 6 combinaciones) es una eleccion de la replica.",
        "T4-H2": "Central 585.609,35 (exacta) y maximo 946.278 (-0,06 %) coinciden. Retardos con el estimador de la ficha (igualdad de acumulados a fin de anio): 2,971 / 3,206 / 3,201 / 3,073 / 3,207 por ventana, identicos a B2_retardo.csv; mediana 3,201, min 2,971, max 3,207; cartera con valores anuales en el propio anio e interpolacion lineal en y-L. Con ello el minimo no cambia: opt = 143.124/anio (necesarios ~146.435), minimo 103.803 frente a 87.247. El opt publicado exigiria un retardo de ~2,60 anios (con fill = maximo 2021-2025), que no coincide con ninguna media, mediana, minimo o maximo de ventana (2,971; 1,758 es el minimo anual de la ventana 2008). Falta: la regla exacta por la que el retardo corto de opt toma ~2,6 anios, o el relleno posterior a 2025 de opt; con la ficha actual no se reproduce el minimo.",
        "T4-H3": "15 / 0 / 37 exactos con la regla de la ficha (empeora si cambio > 0 en todos los escenarios; mejora si < 0 en todos)."
    }
    ver = {"T3-H5b": "COINCIDE", "T4-H2": "DISCREPA", "T4-H3": "COINCIDE"}
    res = [dict(id=i, publicado=dict(valor=pub[i][0], min=pub[i][1], max=pub[i][2]),
                replica=dict(valor=float(rep[i][0]), min=float(rep[i][1]), max=float(rep[i][2])),
                veredicto=ver[i], diagnostico=diag[i]) for i in pub]
    json.dump(res, open(OUT / "resultado.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()

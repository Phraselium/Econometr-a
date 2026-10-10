"""M2 (C1): descomposición de la creación de hogares y demanda latente juvenil (C2). Sin red, determinista.

H(t) = Σ_{nac,edad} N_nac(t) · s_{nac,edad}(t) · h_edad(t); h = personas de referencia / población (EPA 65944).
Shapley exacto sobre 4 factores (N_esp, N_ext, estructura por edad s, tasa h): la suma iguala ΔH.
"""
from __future__ import annotations

import itertools
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import holdout  # noqa: E402
from econ_utils import Registry  # noqa: E402

SEED = 20261010
RAW = RAIZ / "data" / "raw"
OUT = RAIZ / "output" / "v4" / "M2"
G4 = ["0-19", "20-34", "35-64", "65+"]
EPA2G = {"De 0 a 4 años": "0-19", "De 5 a 9 años": "0-19", "De 10 a 15 años": "0-19", "De 16 a 19 años": "0-19",
         "De 20 a 24 años": "20-34", "De 25 a 29 años": "20-34", "De 30 a 34 años": "20-34",
         **{f"De {a} a {a + 4} años": "35-64" for a in range(35, 65, 5)},
         "De 65 a 69 años": "65+", "70 y más años": "65+"}
FINO = {"16-34": ["De 16 a 19 años", "De 20 a 24 años", "De 25 a 29 años", "De 30 a 34 años"],
        "35-44": ["De 35 a 39 años", "De 40 a 44 años"]}
PERIODOS = [("2006-2007", 2006, 2007), ("2008-2013", 2008, 2013), ("2014-2019", 2014, 2019),
            ("2020-2025", 2020, 2025), ("2021-2025", 2021, 2025)]
FACT = ["N_esp", "N_ext", "estructura", "tasa"]


def epa_cells() -> pd.DataFrame:
    """EPA 65944 (miles, media anual): población y personas de referencia por tramo quinquenal."""
    filas = []
    for x in json.loads((RAW / "v3" / "pa_aux" / "ine_t65944.json").read_text()):
        m = re.match(r"Total Nacional\. Ambos sexos\. (.+?)\. (Total|Persona de referencia)\. Personas", x["Nombre"])
        if m and m.group(1) in EPA2G:
            for d in x["Data"]:
                filas.append((int(d["Anyo"]), m.group(1), m.group(2), (d["Valor"] or 0.0) * 1000))
    t = pd.DataFrame(filas, columns=["anio", "tramo", "rel", "v"])
    return t.pivot_table(index=["anio", "tramo"], columns="rel", values="v", aggfunc="first").rename(
        columns={"Total": "pob", "Persona de referencia": "ref"}).reset_index()


def tasas4(cel: pd.DataFrame) -> pd.DataFrame:
    c = cel.assign(g=cel.tramo.map(EPA2G)).groupby(["anio", "g"])[["pob", "ref"]].sum()
    c["h"] = c.ref / c.pob
    return c.h.unstack()[G4]


def padron() -> pd.DataFrame:
    d = pd.read_csv(RAW / "ine_v2_padron_prov_edad_nac.csv", usecols=["periodo", "valor", "codigo", "nivel", "desglose"])
    d = d[d.periodo.str.endswith("T1")].copy()
    m = d.desglose.str.extract(r"nacionalidad=(\w+); edad=(.+)")
    d["nac"], d["g"] = m[0], m[1]
    d = d[d.nac.isin(["Española", "Extranjera"]) & d.g.isin(G4)]
    d["anio"] = d.periodo.str[:4].astype(int)
    d["cod"] = d.codigo.astype(int).astype(str).str.zfill(2)
    d.loc[d.nivel == "nacional", "cod"] = "00"
    return d.pivot_table(index=["cod", "anio"], columns=["nac", "g"], values="valor", aggfunc="first")


def shapley(P0, P1, h0, h1):
    """P*: dict {'N':[N_esp,N_ext], 's': (2,4) cuotas por edad}; h*: (4,). Devuelve ΔH y efectos por factor."""
    def H(sel):
        n = [P0, P1]
        N = np.array([n[sel[0]]["N"][0], n[sel[1]]["N"][1]])
        s = n[sel[2]]["s"]
        h = [h0, h1][sel[3]]
        return float((N[:, None] * s * h[None, :]).sum())
    ef = dict.fromkeys(FACT, 0.0)
    perms = list(itertools.permutations(range(4)))
    for pr in perms:
        sel = [0, 0, 0, 0]
        prev = H(sel)
        for f in pr:
            sel[f] = 1
            cur = H(sel)
            ef[FACT[f]] += (cur - prev) / len(perms)
            prev = cur
    return H([1, 1, 1, 1]) - H([0, 0, 0, 0]), ef


def celda(row: pd.Series) -> dict:
    v = np.array([[row[("Española", g)] for g in G4], [row[("Extranjera", g)] for g in G4]], float)
    N = v.sum(axis=1)
    return {"N": N, "s": v / N[:, None]}


def decompone(pad, h4, cod, a, b):
    r0, r1 = pad.loc[(cod, a)], pad.loc[(cod, b)]
    dH, ef = shapley(celda(r0), celda(r1), h4.loc[a].values, h4.loc[b].values)
    H0 = float((celda(r0)["N"][:, None] * celda(r0)["s"] * h4.loc[a].values).sum())
    return {"H0": H0, "dH": dH, **ef}


def flujos(pad_nac, pad):
    """Inmigración bruta desde el extranjero (INE 24421, 2008-2022S1; Eurostat migr_imm1ctz, 2002-2024) frente a ΔN_ext."""
    d = pd.read_csv(RAW / "ine_v2_migraciones_prov.csv", usecols=["periodo", "valor", "codigo", "nivel", "desglose"])
    d = d[d.desglose == "nacionalidad=Extranjero; sexo=Ambos; edad=Total"].copy()
    d["anio"], d["sem"] = d.periodo.str[:4].astype(int), d.periodo.str[-2:]
    ine = d[d.nivel == "nacional"].groupby("anio").agg(v=("valor", "sum"), n=("sem", "nunique"))
    ine = ine[ine.n == 2].v
    e = pd.read_csv(RAW / "eurostat_inmigracion_anual.csv")
    eu = e[(e.citizen == "TOTAL") & (e.age == "TOTAL") & (e.sex == "T")].set_index("periodo").valor
    eu.index = eu.index.astype(int)
    filas = []
    for nombre, a, b in PERIODOS:
        # población a 1-ene: la inmigración entre a y b son los años a..b-1
        ys = range(a, b)
        dN = pad.loc[("00", b), "Extranjera"].sum() - pad.loc[("00", a), "Extranjera"].sum()
        i_ine = float(ine.reindex(ys).sum()) if all(y in ine.index for y in ys) else np.nan
        i_eu = float(eu.reindex(ys).sum()) if all(y in eu.index for y in ys) else np.nan
        filas.append({"periodo": nombre, "delta_poblacion_extranjera": dN, "inmigracion_bruta_INE": i_ine,
                      "inmigracion_bruta_Eurostat": i_eu})
    return pd.DataFrame(filas)


def latente(cel, h4, pad, ecp25):
    c25 = cel[cel.anio == 2025].set_index("tramo")
    refs = {"2008": lambda t: cel[(cel.anio == 2008)].set_index("tramo"),
            "media 2006-2007": lambda t: cel[cel.anio.isin([2006, 2007])].groupby("tramo")[["pob", "ref"]].sum()}
    filas = []
    for nref, f in refs.items():
        r = f(None)
        hr = r.ref / r.pob
        h25 = c25.ref / c25.pob
        ex = c25.pob * (hr - h25)  # hogares adicionales por tramo con la tasa de referencia
        for nombre, tr in [("16-34", FINO["16-34"]), ("35-44", FINO["35-44"]), ("total", list(c25.index))]:
            filas.append({"fuente": "EPA 65944 (población EPA 2025)", "referencia": nref, "grupo": nombre,
                          "hogares_adicionales": float(ex[tr].sum())})
        # segunda vía: población del padrón 1-ene-2025 por 4 grupos, nivel calibrado a hogares ECP
        rr = (r.assign(g=r.index.map(EPA2G)).groupby("g")[["pob", "ref"]].sum())
        hr4 = (rr.ref / rr.pob).reindex(G4)
        h25g = h4.loc[2025]
        Pg = pad.loc[("00", 2025)].groupby(level=1).sum().reindex(G4)
        H25m = float((Pg * h25g).sum())
        k = ecp25 / H25m
        ex4 = Pg * (hr4 - h25g) * k
        for nombre, tr in [("20-34", ["20-34"]), ("35-64", ["35-64"]), ("total", G4)]:
            filas.append({"fuente": "Padrón 2025 x tasas EPA, calibrado a hogares ECP", "referencia": nref,
                          "grupo": nombre, "hogares_adicionales": float(ex4[tr].sum())})
    return pd.DataFrame(filas)


def main(smoke: bool = False) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "tablas").mkdir(exist_ok=True)
    reg = Registry(OUT / "registro.csv")
    cel = epa_cells()
    h4 = tasas4(cel)
    pad = padron()
    provs = sorted({c for c, _ in pad.index if c != "00"})
    if smoke:
        provs = ["28"]
    # comprobación cruzada padrón CSV frente a panel_prov_a (sellado: solo lectura vía holdout)
    pa = holdout.load_full("panel_prov_a", "M2")
    cols = [f"pob_{n}_{g}" for n in ("espanola", "extranjera") for g in ("0_19", "20_34", "35_64", "65_mas")]
    pa = pa[pa.anio == 2022].assign(cod=lambda x: x.cod_prov.astype(str).str.zfill(2)).set_index("cod")[cols]
    p22 = pad.xs(2022, level=1).drop(index="00")
    p22.columns = cols
    comun = pa.index.intersection(p22.index)
    dif_panel = float(((pa.loc[comun] - p22.loc[comun]).abs().sum().sum()) / p22.loc[comun].sum().sum())
    # hogares observados para calibración
    ecp = pd.read_csv(RAW / "ine_hogares_60131.csv")
    ecp = ecp[ecp.nombre.str.startswith("Total Nacional. Total.")].set_index("periodo").valor
    epa_h = pd.read_csv(RAW / "ine_epa_hogares.csv")
    epa_h = epa_h[epa_h.nombre == "Hogares. Total Nacional. Ambos sexos. Total. Total."]
    epa_h["anio"] = epa_h.periodo.str[:4].astype(int)
    epa_anual = epa_h.groupby("anio").valor.mean()  # valor en miles
    calib = []
    for y in range(2006, 2026):
        Hm = float((pad.loc[("00", y)].values.reshape(2, 4) * h4.loc[y].values).sum())
        calib.append({"anio": y, "H_modelo_padron_x_h_EPA": Hm, "H_EPA_hogares": float(epa_anual.get(y, np.nan)) * 1000,
                      "H_ECP_1T": float(ecp.get(f"{y}T1", np.nan))})
    calib = pd.DataFrame(calib)
    nac, prv, ret = [], [], []
    for nombre, a, b in PERIODOS:
        r = decompone(pad, h4, "00", a, b)
        reg.log("M2", f"nac_{nombre}", "ΔH=Shapley(N_esp,N_ext,estructura,tasa)", a, b, 8, np.nan, np.nan, np.nan,
                coef_interes=r["dH"], notas="C1; sin contraste de hipótesis: no aplica FDR")
        nac.append({"periodo": nombre, **r})
        for c in provs:
            q = decompone(pad, h4, c, a, b)
            reg.log("M2", f"prov{c}_{nombre}", "ΔH=Shapley con h nacional", a, b, 8, np.nan, np.nan, np.nan,
                    coef_interes=q["dH"], notas="tasa h nacional aplicada a la provincia")
            prv.append({"cod_prov": c, "periodo": nombre, **q})
    nac = pd.DataFrame(nac)
    prv = pd.DataFrame(prv)
    for d in (nac, prv):
        d["tamano_nativos"], d["tamano_extranjeros"] = d.N_esp, d.N_ext
        d["tamano_total"] = d.N_esp + d.N_ext
        for k in ("tamano_nativos", "tamano_extranjeros", "estructura", "tasa", "dH"):
            d[f"pct_{k}"] = 100 * d[k] / d.dH
        d.drop(columns=["N_esp", "N_ext"], inplace=True)
    # validación 2021-2025: ΔH provincial observado (ECP) frente a modelo
    hp = pd.read_csv(RAW / "ine_v2_hogares_prov.csv", usecols=["periodo", "valor", "codigo", "nivel", "desglose"])
    hp = hp[(hp.desglose == "tamaño=Total") & hp.periodo.isin(["2021T1", "2025T1"])] if (hp.desglose == "tamaño=Total").any() else hp.iloc[0:0]
    if len(hp):
        hp["cod"] = hp.codigo.astype(int).astype(str).str.zfill(2)
        o = hp.pivot_table(index="cod", columns="periodo", values="valor")
        o["dH_obs"] = o["2025T1"] - o["2021T1"]
        q = prv[prv.periodo == "2021-2025"].set_index("cod_prov").dH.rename("dH_modelo")
        v = pd.concat([o.dH_obs, q], axis=1).dropna()
        v["residuo_obs_menos_modelo"] = v.dH_obs - v.dH_modelo
        v.to_csv(OUT / "tablas" / "validacion_prov_2021_2025.csv", index_label="cod_prov")
        corr = float(v.dH_obs.corr(v.dH_modelo)) if len(v) > 2 else np.nan
    else:
        corr = np.nan
    fl = flujos(None, pad)
    lat = latente(cel, h4, pad, float(ecp["2025T1"]))
    nac.to_csv(OUT / "tablas" / "descomposicion_nacional.csv", index=False)
    prv.to_csv(OUT / "tablas" / ("descomposicion_provincial_smoke.csv" if smoke else "descomposicion_provincial.csv"), index=False)
    fl.to_csv(OUT / "tablas" / "flujos_inmigracion.csv", index=False)
    lat.to_csv(OUT / "tablas" / "demanda_latente.csv", index=False)
    calib.to_csv(OUT / "tablas" / "calibracion_hogares.csv", index=False)
    h4.to_csv(OUT / "tablas" / "tasas_jefatura_4grupos.csv")
    if smoke:
        print(nac.round(1).to_string())
        print(prv.round(1).to_string())
        print(lat.round(0).to_string())
        print(fl.round(0).to_string())
        print(calib.tail(3).round(0), dif_panel, corr)
        return
    # top 3 provincias por efecto (periodo 2021-2025 y 2008-2013 y 2014-2019 y 2020-2025)
    nombres = pd.read_csv(RAW / "ine_v2_padron_prov_edad_nac.csv", usecols=["codigo", "territorio", "nivel"]).drop_duplicates()
    nombres = nombres[nombres.nivel == "provincia"]
    nm = dict(zip(nombres.codigo.astype(int).astype(str).str.zfill(2), nombres.territorio, strict=False))
    tops = {}
    for nombre, _, _ in PERIODOS:
        s = prv[prv.periodo == nombre].set_index("cod_prov")
        tops[nombre] = {k: [(nm[i], round(float(s.loc[i, k]))) for i in s[k].abs().sort_values(ascending=False).index[:3]]
                        for k in ("tamano_nativos", "tamano_extranjeros", "estructura", "tasa")}
    json.dump(tops, open(OUT / "tablas" / "top3_provincias.json", "w"), ensure_ascii=False, indent=1)
    figuras(nac, prv, lat, nm)
    escribe_json(nac, lat, fl, calib, dif_panel, corr, tops)
    reg.flush()


def figuras(nac, prv, lat, nm):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 4.5))
    cols = ["tamano_nativos", "tamano_extranjeros", "estructura", "tasa"]
    base = np.zeros(len(nac))
    for c, col in zip(cols, ["#4c78a8", "#f58518", "#54a24b", "#b279a2"], strict=True):
        ax.bar(nac.periodo, nac[c] / 1e3, bottom=np.where(nac[c] >= 0, base, 0), label=c, color=col)
        base = base + np.where(nac[c] >= 0, nac[c] / 1e3, 0)
    ax.plot(nac.periodo, nac.dH / 1e3, "ko", label="ΔH total")
    ax.set_ylabel("miles de hogares"); ax.set_title("Descomposición de ΔH (Shapley), España"); ax.legend(fontsize=7)
    fig.tight_layout(); fig.savefig(OUT / "figuras" / "descomposicion_nacional.png", dpi=130); plt.close(fig)
    s = prv[prv.periodo == "2014-2019"].set_index("cod_prov")
    s = s.reindex(s.dH.abs().sort_values(ascending=False).index[:15])
    fig, ax = plt.subplots(figsize=(8, 5))
    left = np.zeros(len(s))
    for col in cols:
        ax.barh([nm[i] for i in s.index], s[col] / 1e3, left=left, label=col)
        left = left + s[col].values / 1e3
    ax.invert_yaxis(); ax.set_xlabel("miles de hogares"); ax.set_title("15 provincias con mayor ΔH, 2014-2019"); ax.legend(fontsize=7)
    fig.tight_layout(); fig.savefig(OUT / "figuras" / "provincias_2014_2019.png", dpi=130); plt.close(fig)


def escribe_json(nac, lat, fl, calib, dif_panel, corr, tops):
    n = nac.set_index("periodo")
    desc = {p: {k: round(float(n.loc[p, k])) for k in ("dH", "tamano_nativos", "tamano_extranjeros", "estructura", "tasa")}
            | {"pct_" + k: round(float(n.loc[p, "pct_" + k]), 1) for k in ("tamano_nativos", "tamano_extranjeros", "estructura", "tasa")}
            for p in n.index}
    L = lat.set_index(["fuente", "referencia", "grupo"]).hogares_adicionales
    tot = lat[lat.grupo == "total"].hogares_adicionales
    j = lat[lat.grupo.isin(["16-34", "20-34"])].hogares_adicionales
    f35 = lat[lat.grupo.isin(["35-44", "35-64"])].hogares_adicionales
    comun_s = ("EPA con ruptura de serie hacia 2021 (marco censal); la tasa 65+ cae en 2025. Jefatura por edad solo de EPA (una fuente) y sin desglose por nacionalidad; "
               "tasa h común a nativos y extranjeros.")
    hechos = [
        {"id": "M2-H1", "enunciado_neutro": "Descomposición shapley de la variación de hogares (personas de referencia) en España por periodo.",
         "capa": "C1", "magnitud": desc, "unidad": "hogares y % de ΔH", "intervalo": "ver notas: población padrón x tasa EPA frente a hogares EPA/ECP en calibracion_hogares.csv",
         "fuentes": ["INE padrón (ine_v2_padron_prov_edad_nac.csv; contraste con panel_prov_a)", "INE EPA 65944 (jefatura por edad)",
                     "EPA hogares y ECP 60131 (calibración de nivel)"],
         "supuestos": ["Cuatro grupos de edad; 'nativos' = nacionalidad española (incluye nacionalizados)", "h por edad común a ambas nacionalidades",
                       "Shapley con 4 factores (N_esp, N_ext, estructura, tasa)"],
         "limites": [comun_s, "Periodo 2002-2007 no disponible: EPA 65944 empieza en 2006; se informa 2006-2007.",
                     f"Diferencia relativa padrón CSV frente a panel_prov_a (2022): {dif_panel:.4%}"]},
        {"id": "M2-H2", "enunciado_neutro": "Inmigración bruta desde el extranjero frente a la variación de población extranjera (dos fuentes).",
         "capa": "C1", "magnitud": fl.round(0).to_dict("records"), "unidad": "personas", "intervalo": "INE frente a Eurostat",
         "fuentes": ["INE EM 24421 (semestral, 2008-2022S1)", "Eurostat migr_imm1ctz"],
         "supuestos": ["Flujo bruto, no neto"],
         "limites": ["No hay emigración ni migración interior en data/raw: no se separa migración interior ni neta; no es un término de la descomposición.",
                     "INE y Eurostat difieren desde 2021"]},
        {"id": "M2-L1", "enunciado_neutro": "Hogares adicionales en 2025 si rigieran las tasas de jefatura por edad de 2008 (y media 2006-2007).",
         "capa": "C2", "magnitud": {f"{a}|{b}|{c}": round(float(v)) for (a, b, c), v in L.items()}, "unidad": "hogares",
         "intervalo": [round(float(j.min())), round(float(j.max()))], "fuentes": ["EPA 65944", "Padrón INE", "ECP 60131"],
         "supuestos": ["Contrafactual: la tasa de jefatura por edad de la referencia aplica en 2025 a la población de 2025",
                       "Referencia 2004-2007 sustituida por 2006-2007 (EPA 65944 desde 2006)"],
         "limites": [comun_s, "Los tramos 16-34 y 35-44 solo salen de la vía EPA; la vía padrón usa 20-34 y 35-64.",
                     "Una cota con supuesto contrafactual; no es déficit ni demanda a cualquier precio."]},
    ]
    json.dump(hechos, open(OUT / "hechos.json", "w"), ensure_ascii=False, indent=1)
    res = {"rama": "M2", "pregunta": "¿Por qué se crean tantos hogares?", "capa": "C1 (descomposición) y C2 (demanda latente)",
           "datos": ["ine_v2_padron_prov_edad_nac.csv", "panel_prov_a (contraste)", "pa_aux/ine_t65944.json", "ine_hogares_60131.csv",
                     "ine_epa_hogares.csv", "ine_v2_migraciones_prov.csv", "eurostat_inmigracion_anual.csv"],
           "N": int(len(n)), "metodo": "Shapley sobre 4 factores (tamaño nativos, tamaño extranjeros, estructura por edad, tasa de jefatura)",
           "estimacion": desc, "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO (C1 hechos); latente: cota C2",
           "diagnosticos": {"dif_rel_padron_vs_panel_2022": dif_panel, "corr_dH_obs_modelo_prov_2021_2025": corr,
                            "top3_provincias": tops, "latente_total_rango": [round(float(tot.min())), round(float(tot.max()))]},
           "fuera_muestra": {"modelo": "no aplica (identidad contable)", "rmse": None, "dm_vs_ar4": None},
           "notas": "Sin jefatura por nacionalidad ni migración interior; provincias con h nacional; 2002-2007 sustituido por 2006-2007."}
    json.dump(res, open(OUT / "resultado.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)

"""A1 · Déficit contable acumulado: D(t0,t1) = suma de variacion de hogares - suma de (terminadas - bajas)."""
from __future__ import annotations

import numpy as np
import pandas as pd

import pa_data as pdat

BAJAS = [0.0, 0.001, 0.002]
PERIODOS = [(2002, 2007), (2008, 2013), (2014, 2019), (2020, 2025), (2014, 2025),
            (2012, 2021), (2022, 2025), (2012, 2025), (2021, 2025)]  # los 4 últimos: ventanas con dos fuentes de hogares
BDE = {"cifra": 750000, "ief": 700000, "periodo": "2021-2025",
       "fuente": "BdE, Informe Anual 2025, cap. 2 (≈750.000; IEF otoño 2025: 700.000). El DO 2432 trata del alquiler y no del déficit"}


def _stock_q(serie: pd.Series, y: int, base_alt: str | None = None) -> tuple[float | None, str]:
    """Stock al final del año y (cuarto trimestre). Si falta, devuelve None."""
    k = f"{y}Q4"
    if k in serie.index and pd.notna(serie[k]):
        return float(serie[k]), ""
    if base_alt and base_alt in serie.index and pd.notna(serie[base_alt]):
        return float(serie[base_alt]), f"base {base_alt} (no hay {k})"
    return None, ""


def hogares_nacional() -> dict[str, dict]:
    """Devuelve, por fuente, función (t0,t1) -> (delta, nota)."""
    q = pdat.nacional_q()
    epa = q.hogares_epa * 1000.0
    ecp = q.hogares_ecp
    c11 = pdat.censo2011_nacional()["principal"]
    c21 = pdat.censo2021_hogares_nacional()

    def f_epa(t0, t1):
        a, na = _stock_q(epa, t0 - 1, "2002Q1")
        b, _ = _stock_q(epa, t1)
        nota = "EPA, 4.º trimestre; " + na + ("; quiebre EPA 2021 dentro del periodo" if t0 <= 2021 <= t1 else "")
        return (None if a is None or b is None else b - a), nota

    def f_ecp(t0, t1):
        # ECP solo desde 2021T1 y anclada al Censo 2021: no es independiente del Censo.
        if t0 - 1 < 2021:
            if (t0, t1) == (2021, 2025):
                a, b = float(ecp["2021Q1"]), float(ecp["2025Q4"])
                return b - a, "ECP desde 2021T1 (base 1T-2021 en vez de 4T-2020)"
            return None, ""
        return float(ecp[f"{t1}Q4"]) - float(ecp[f"{t0 - 1}Q4"]), "ECP, 4.º trimestre"

    def f_censo(t0, t1):
        # Censos 2011 y 2021 (1 nov.) + ECP (anclada al Censo 2021) para 2022-2025
        if (t0, t1) == (2012, 2021):
            return c21 - c11, "Censo 2011 (viviendas principales) y Censo 2021 (hogares), 1 de noviembre"
        if (t0, t1) == (2022, 2025):
            return float(ecp["2025Q4"]) - float(ecp["2021Q4"]), "ECP 4T-2021 a 4T-2025 (cadena Censo 2021 + ECP)"
        if (t0, t1) == (2012, 2025):
            return (c21 - c11) + float(ecp["2025Q4"]) - float(ecp["2021Q4"]), "Censo 2011-2021 + ECP 2021-2025"
        return None, ""

    return {"EPA": f_epa, "Censo+ECP": lambda a, b: f_censo(a, b) if (a, b) in [(2012, 2021), (2022, 2025), (2012, 2025)]
            else f_ecp(a, b)}


def netas_nacional(t0: int, t1: int, m: pd.DataFrame) -> list[dict]:
    """Altas netas por fuente. Fin de obra (bruto, admite bajas), Δ parque MIVAU y Δ stock del Censo (netos)."""
    yrs = range(t0, t1 + 1)
    out = []
    lib = m.libres.reindex(yrs)
    prot = m.protegida.reindex(yrs)
    park0 = m.parque.reindex([y - 1 for y in yrs]).values
    for prot_flag, serie in (("con", lib + prot.fillna(0)), ("sin", lib)):
        if serie.isna().any():
            continue
        for b in BAJAS:
            bajas = float(np.nansum(b * park0))
            out.append({"neta_fuente": "MIVAU fin de obra (bruto)", "protegida": prot_flag, "bajas_pct": 100 * b,
                        "neta": float(serie.sum()) - bajas, "bruto": float(serie.sum()), "bajas": bajas})
    if t0 - 1 in m.parque.index and t1 in m.parque.index and m.parque[[t0 - 1, t1]].notna().all():
        out.append({"neta_fuente": "MIVAU parque (Δ, neto)", "protegida": "incluida", "bajas_pct": np.nan,
                    "neta": float(m.parque[t1] - m.parque[t0 - 1]), "bruto": np.nan, "bajas": np.nan})
    c = pdat.censo2011_nacional()
    if (t0, t1) == (2012, 2021):
        out.append({"neta_fuente": "Censo (Δ stock total, neto)", "protegida": "incluida", "bajas_pct": np.nan,
                    "neta": 26623708.0 - 25208623.0, "bruto": np.nan, "bajas": np.nan})
    if (t0, t1) == (2012, 2025):
        out.append({"neta_fuente": "Censo (Δ stock 2011-21) + Δ parque MIVAU 2021-25", "protegida": "incluida",
                    "bajas_pct": np.nan, "neta": 26623708.0 - 25208623.0 + float(m.parque[2025] - m.parque[2021]),
                    "bruto": np.nan, "bajas": np.nan})
    del c
    return out


def a1_nacional(reg) -> tuple[pd.DataFrame, pd.DataFrame]:
    m = pdat.mivau_nacional_anual()
    H = hogares_nacional()
    filas = []
    for (t0, t1) in PERIODOS:
        for hn, hf in H.items():
            dh, nota_h = hf(t0, t1)
            if dh is None:
                continue
            for n in netas_nacional(t0, t1, m):
                d = dh - n["neta"]
                filas.append({"periodo": f"{t0}-{t1}", "t0": t0, "t1": t1, "hogares_fuente": hn, "delta_hogares": dh,
                              **n, "deficit": d, "nota_hogares": nota_h})
                reg.log("A1_nacional", f"A1_{t0}_{t1}_{hn}_{n['neta_fuente'][:12]}_{n['protegida']}_{n['bajas_pct']}",
                        "D = Σ Δhogares − Σ(terminadas − bajas)", t0, t1, t1 - t0 + 1, np.nan, np.nan, np.nan,
                        np.nan, d, np.nan, f"{hn}; {n['neta_fuente']}; protegida {n['protegida']}; bajas {n['bajas_pct']}")
    t = pd.DataFrame(filas)
    res = []
    for per, g in t.groupby("periodo", sort=False):
        con = g[g.protegida.isin(["con", "incluida"])]
        cen = con[(con.bajas_pct.isna()) | (con.bajas_pct == 0.1)]
        bj = con[(con.neta_fuente == "MIVAU fin de obra (bruto)")]
        res.append({
            "periodo": per, "n_fuentes_hogares": con.hogares_fuente.nunique(), "n_fuentes_altas": con.neta_fuente.nunique(),
            "min_total": con.deficit.min(), "max_total": con.deficit.max(),
            "min_entre_fuentes_bajas01": cen.deficit.min(), "max_entre_fuentes_bajas01": cen.deficit.max(),
            "efecto_bajas_01_viviendas": float(bj[bj.bajas_pct == 0.1].bajas.iloc[0]) if (bj.bajas_pct == 0.1).any() else np.nan,
            "efecto_bajas_02_viviendas": float(bj[bj.bajas_pct == 0.2].bajas.iloc[0]) if (bj.bajas_pct == 0.2).any() else np.nan,
            "sin_protegida_min": g[g.protegida == "sin"].deficit.min() if (g.protegida == "sin").any() else np.nan,
            "sin_protegida_max": g[g.protegida == "sin"].deficit.max() if (g.protegida == "sin").any() else np.nan,
            "capa": "C1" if con.hogares_fuente.nunique() >= 2 and con.neta_fuente.nunique() >= 2 else "C4",
        })
    return t, pd.DataFrame(res)


def a1_provincial(reg) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Provincias: hogares con una sola fuente por periodo (Censo o ECP) -> C4; altas con dos fuentes (fin de obra y Catastro)."""
    pp = pdat.panel("panel_prov_a")
    mp = pdat.mapa_prov(pp)
    c11 = pdat.censo2011_provincias()
    cat = pdat.catastro()
    cm = pdat.censo2021_municipios()
    cm["cod_prov"] = cm.index.str[:2]
    c21 = cm.groupby("cod_prov")[["V_PRINCIPAL", "V_TOTAL"]].sum()
    h = pd.read_csv(pdat.RAW / "ine_v2_hogares_prov.csv", dtype={"codigo": str})
    h = h[(h.nivel == "provincia") & (h.desglose == "tamaño=Total")].pivot(index="codigo", columns="periodo", values="valor")
    cat_s = cat.groupby(["cod_prov", "periodo"]).uu_res.sum().unstack()
    panel_idx = pp.set_index(["cod_prov", "anio"])
    filas = []
    for cod in sorted(pp.cod_prov.unique()):
        cod = str(cod).zfill(2)
        k = next((kk for kk, vv in mp.items() if vv == cod), None)
        if k not in c11.index:
            continue
        for (t0, t1) in [(2012, 2021), (2022, 2025), (2012, 2025)]:
            if (t0, t1) == (2012, 2021):
                dh, hn = c21.loc[cod, "V_PRINCIPAL"] - c11.loc[k, "Vivienda principal"], "Censo"
            elif (t0, t1) == (2022, 2025):
                dh, hn = h.loc[cod, "2025T4"] - h.loc[cod, "2021T4"], "ECP"
            else:
                dh, hn = (c21.loc[cod, "V_PRINCIPAL"] - c11.loc[k, "Vivienda principal"]
                          + h.loc[cod, "2025T4"] - h.loc[cod, "2021T4"]), "Censo+ECP"
            yrs = range(t0, t1 + 1)
            lib = [panel_idx["terminadas_libres_anual"].get((cod, y), np.nan) for y in yrs]
            pr = [panel_idx["protegida"].get((cod, y), np.nan) for y in yrs]
            stock0 = c11.loc[k, "Total viviendas"] if t0 == 2012 else c21.loc[cod, "V_TOTAL"]
            for prot_flag, tot in (("con", np.nansum(lib) + np.nansum(pr)), ("sin", np.nansum(lib))):
                for b in BAJAS:
                    n = tot - b * stock0 * (t1 - t0 + 1)
                    filas.append({"cod_prov": cod, "periodo": f"{t0}-{t1}", "hogares_fuente": hn, "delta_hogares": dh,
                                  "neta_fuente": "MIVAU fin de obra (bruto)", "protegida": prot_flag, "bajas_pct": 100 * b,
                                  "neta": n, "deficit": dh - n})
            if cod in cat_s.index and pd.notna(cat_s.loc[cod, t0]) and cod not in ("01", "20", "31", "48"):
                a = cat_s.loc[cod]
                if (t0, t1) == (2012, 2021):
                    ncat = a[2022] - a[2012]
                elif (t0, t1) == (2022, 2025):
                    ncat = a[2026] - a[2022]
                else:
                    ncat = a[2026] - a[2012]
                filas.append({"cod_prov": cod, "periodo": f"{t0}-{t1}", "hogares_fuente": hn, "delta_hogares": dh,
                              "neta_fuente": "Catastro (Δ unidades urbanas residenciales, neto)", "protegida": "incluida",
                              "bajas_pct": np.nan, "neta": ncat, "deficit": dh - ncat})
    t = pd.DataFrame(filas)
    t["provincia"] = t.cod_prov.map(pp.drop_duplicates("cod_prov").set_index("cod_prov").provincia)
    for r in t.drop_duplicates(["cod_prov", "periodo"]).itertuples():
        reg.log("A1_provincial", f"A1prov_{r.cod_prov}_{r.periodo}", "D provincial, hogares fuente única", r.periodo[:4],
                r.periodo[5:], 1, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, "capa C4: hogares de una sola fuente")
    res = []
    for (cod, per), g in t[t.protegida.isin(["con", "incluida"])].groupby(["cod_prov", "periodo"]):
        res.append({"cod_prov": cod, "provincia": g.provincia.iloc[0], "periodo": per, "min": g.deficit.min(),
                    "max": g.deficit.max(), "n_fuentes_altas": g.neta_fuente.nunique(),
                    "hogares_fuente": g.hogares_fuente.iloc[0], "capa": "C4"})
    return t, pd.DataFrame(res)

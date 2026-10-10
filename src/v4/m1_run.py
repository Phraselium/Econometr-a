"""M1 · Geografía del déficit (C1/C2). Determinista, sin red. Uso: python src/v4/m1_run.py [--smoke]

Déficit D = Δ hogares − altas netas (viviendas nuevas), por provincia y por municipio de más de 10.000 habitantes.
Hogares provinciales (2021-2025): ECP y Censo anual (personas / tamaño medio de hogar del Censo 2021: supuesto).
Altas provinciales: fin de obra MIVAU (bajas 0 / 0,1 / 0,2 %) y Δ unidades urbanas residenciales del Catastro.
Municipios: Catastro (única fuente municipal; no hay terminadas MIVAU por municipio en data/raw) -> C4.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v3"))
import econ_utils  # noqa: E402
import pa_data as pdat  # noqa: E402

SEED = 20261010
TOL = 0.15
np.random.seed(SEED)
RAW = RAIZ / "data" / "raw"
OUT = RAIZ / "output" / "v4" / "M1"
BAJAS = [0.0, 0.001, 0.002]
UMBRAL = 10000
FORALES = ["01", "20", "31", "48"]
UNIPROV = {"07": "Balears (Illes)", "28": "Madrid (Comunidad de)", "30": "Murcia (Región de)",
           "31": "Navarra (Comunidad Foral de)", "33": "Asturias (Principado de )", "39": "Cantabria",
           "26": "Rioja (La)", "51": "Ceuta", "52": "Melilla"}
UNIPROV_PROT = {"07": "Balears (Illes)", "28": "Madrid (Comunidad de)", "30": "Murcia (Región de)",
                "31": "Navarra (Comunidad Foral de)", "33": "Asturias (Principado de)", "39": "Cantabria",
                "26": "Rioja (La)", "51": "Ceuta", "52": "Melilla"}
SMOKE = "--smoke" in sys.argv


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"^(.*?)\s*\((a|el|la|las|los|l|o|as|os)\)$", r"\2 \1", s.strip())
    s = re.sub(r"\(.*?\)", lambda m: " " + m.group(0)[1:-1], s)
    m = re.match(r"^(.*), (a|el|la|las|los|l|o|as|os)$", s.strip())
    if m:
        s = m.group(2) + " " + m.group(1)
    return re.sub(r"[^a-z0-9]", "", s)


def claves(nombre: str) -> list[str]:
    ks = [norm(nombre)]
    if "/" in nombre:
        ks += [norm(p) for p in nombre.split("/")]
    return list(dict.fromkeys(ks))


# ------------------------------------------------------------------ lecturas
def leer_censo_anual() -> pd.DataFrame:
    """Personas por sección (Censo anual, 1 de enero de cada año). Devuelve municipio x año y provincia x año."""
    g = pd.read_csv(RAW / "v3" / "ine_v3_gis_seccion.csv.gz", dtype={"codigo": str},
                    usecols=["codigo", "campo", "valor", "servicio", "anio"])
    g = g[(g.campo == "n_personas") & g.servicio.str.match(r"^Censo_20\d\d___Número_de_personas$")]
    g = g.assign(mun=g.codigo.str[:5], anio=g.anio.astype(int))
    return g.groupby(["mun", "anio"]).valor.sum().unstack()


def provincias_ecp() -> tuple[pd.DataFrame, dict[str, str]]:
    h = pd.read_csv(RAW / "ine_v2_hogares_prov.csv", dtype={"codigo": str})
    nombres = h[h.nivel == "provincia"].drop_duplicates("codigo").set_index("codigo").territorio.to_dict()
    h = h[(h.nivel == "provincia") & (h.desglose == "tamaño=Total")].pivot(index="codigo", columns="periodo", values="valor")
    return h, nombres


def terminadas_mivau() -> tuple[pd.DataFrame, pd.DataFrame]:
    a = pd.read_csv(RAW / "mivau_v2_iniciadas_terminadas_prov.csv")
    a = a[a.serie.str.contains("viv_libres_terminadas_anual") & a.nivel.isin(["provincia", "ccaa", "ciudad_autonoma"])]
    lib = a.pivot_table(index="territorio", columns="periodo", values="valor", aggfunc="first")
    q = pd.read_csv(RAW / "mivau_v2_protegida.csv")
    q = q[q.serie.str.startswith("prot_definitiva_anual")]
    pro = q.pivot_table(index="territorio", columns="periodo", values="valor", aggfunc="first")
    lib.columns = lib.columns.astype(int)
    pro.columns = pro.columns.astype(int)
    return lib, pro


def catastro_stock() -> pd.DataFrame:
    c = pdat.catastro()
    c = c[c.codigo.str.len() == 5]
    return c.pivot_table(index="codigo", columns="periodo", values="uu_res", aggfunc="sum")


def censo2011_mun() -> pd.Series:
    c = pdat.censo2011_municipios()
    return c["Vivienda principal"].dropna()


def mapa_2011(cm: pd.DataFrame) -> pd.Series:
    """Viviendas principales 2011 por código de municipio (cruce por nombre; descarta homónimos)."""
    c11 = censo2011_mun()
    idx: dict[str, set[str]] = {}
    for cod, nom in cm.nombre.items():
        for k in claves(nom):
            idx.setdefault(k, set()).add(cod)
    asign: dict[str, list[float]] = {}
    for nom, v in c11.items():
        hit = None
        for k in claves(nom):
            s = idx.get(k, set())
            if len(s) == 1:
                hit = next(iter(s))
                break
        if hit:
            asign.setdefault(hit, []).append(v)
    return pd.Series({k: v[0] for k, v in asign.items() if len(v) == 1}, name="principal_2011")


# ------------------------------------------------------------------ déficit provincial
def deficit_provincial(reg, H_ecp, nombres, ca, cm, cat, lib, pro, filtro) -> pd.DataFrame:
    c11 = pdat.censo2011_provincias()
    cm = cm.copy()
    cm["cod_prov"] = cm.index.str[:2]
    c21 = cm.groupby("cod_prov")[["V_PRINCIPAL", "V_TOTAL"]].sum()
    pers21 = ca[2021].groupby(ca.index.str[:2]).sum()
    tam21 = pers21 / c21.V_PRINCIPAL
    pers = {y: ca[y].groupby(ca.index.str[:2]).sum() for y in range(2021, 2026)}
    cat_p = cat.groupby(cat.index.str[:2]).sum(min_count=1)
    claves_mivau = {norm(t): t for t in lib.index}
    filas = []
    for cod in sorted(nombres):
        if filtro and cod not in filtro:
            continue
        k = pdat.clave(nombres[cod])
        if k not in c11.index or cod not in c21.index:
            continue
        terr = UNIPROV.get(cod) or claves_mivau.get(norm(nombres[cod])) or claves_mivau.get(norm(nombres[cod].split("/")[0]))
        terr_p = UNIPROV_PROT.get(cod) or next((t for t in pro.index if norm(t) == norm(terr or "")), None)
        if terr not in lib.index:
            continue
        for per, (t0, t1) in {"2012-2025": (2012, 2025), "2021-2025": (2021, 2025)}.items():
            rutas = {}
            if per == "2021-2025":
                rutas["ECP"] = (H_ecp.loc[cod, "2025T4"] - H_ecp.loc[cod, "2021T1"], 2025, 2026, "ECP 2021T1-2025T4")
                rutas["Censo anual"] = (pers[2025][cod] / tam21[cod] - pers[2021][cod] / tam21[cod], 2024, 2025,
                                        "Censo anual 1-ene-2021 a 1-ene-2025; hogares = personas/tamaño medio Censo 2021 (supuesto)")
            else:
                d1 = c21.loc[cod, "V_PRINCIPAL"] - c11.loc[k, "Vivienda principal"]
                rutas["Censo+ECP"] = (d1 + H_ecp.loc[cod, "2025T4"] - H_ecp.loc[cod, "2021T4"], 2025, 2026,
                                      "Censos 2011-2021 + ECP 2021T4-2025T4")
                rutas["Censo+Censo anual"] = (pers[2025][cod] / tam21[cod] - c11.loc[k, "Vivienda principal"], 2024, 2025,
                                              "Censo 2011 (viv. principales) y Censo anual 1-ene-2025 / tamaño medio 2021 (supuesto)")
            stock0 = c11.loc[k, "Total viviendas"] if t0 == 2012 else c21.loc[cod, "V_TOTAL"]
            for rn, (dh, ylast, ccat1, nota) in rutas.items():
                yrs = range(t0, ylast + 1)
                li = np.nansum([lib.loc[terr].get(y, np.nan) for y in yrs])
                pr = np.nansum([pro.loc[terr_p].get(y, np.nan) for y in yrs]) if terr_p in pro.index else 0.0
                assert li > 0, f"terminadas MIVAU nulas: {cod} {t0}-{ylast}"
                for pf, tot in (("con", li + pr), ("sin", li)):
                    for b in BAJAS:
                        n = tot - b * stock0 * len(yrs)
                        filas.append({"cod_prov": cod, "provincia": nombres[cod], "periodo": per, "ruta_hogares": rn,
                                      "ambito": "robustez" if "Censo anual" in rn else "principal",
                                      "delta_hogares": dh, "fuente_altas": "MIVAU fin de obra (bruto)", "protegida": pf,
                                      "bajas_pct": 100 * b, "altas": n, "deficit": dh - n, "nota": nota})
                a0 = {2012: 2012, 2021: 2021}[t0]
                if cod not in FORALES and cod in cat_p.index and pd.notna(cat_p.loc[cod].get(a0)) and pd.notna(cat_p.loc[cod].get(ccat1)):
                    n = cat_p.loc[cod, ccat1] - cat_p.loc[cod, a0]
                    filas.append({"cod_prov": cod, "provincia": nombres[cod], "periodo": per, "ruta_hogares": rn,
                                  "ambito": "robustez" if "Censo anual" in rn else "principal",
                                  "delta_hogares": dh, "fuente_altas": "Catastro (Δ unidades urbanas residenciales, neto)",
                                  "protegida": "incluida", "bajas_pct": np.nan, "altas": n, "deficit": dh - n, "nota": nota})
    t = pd.DataFrame(filas)
    for y in range(2012, 2026):
        v = float(lib[y].sum())
        assert np.isfinite(v) and v > 0, f"terminadas MIVAU nacionales nulas o NaN en {y}"
    for r in t.itertuples():
        reg.log("M1_prov", f"M1prov_{r.cod_prov}_{r.periodo}_{r.ruta_hogares}_{r.fuente_altas[:6]}_{r.protegida}_{r.bajas_pct}",
                "D = Δhogares − altas", r.periodo[:4], r.periodo[5:], 1, np.nan, np.nan, np.nan, np.nan, r.deficit, np.nan,
                r.nota)
    return t


def resumen_prov(t: pd.DataFrame) -> pd.DataFrame:
    """Cifra principal: ruta ECP (2021-2025) o Censos+ECP (2012-2025). Capa por triangulación de las altas (±15 %)."""
    base = t[(t.ambito == "principal") & t.protegida.isin(["con", "incluida"])]
    res = []
    for (cod, per), g in base.groupby(["cod_prov", "periodo"]):
        mi = g[(g.fuente_altas.str.startswith("MIVAU")) & (g.bajas_pct == 0)]
        ca = g[g.fuente_altas.str.startswith("Catastro")]
        dif = np.nan
        if len(mi) and len(ca):
            dif = (ca.altas.iloc[0] - mi.altas.iloc[0]) / mi.altas.iloc[0]
        tri = bool(np.isfinite(dif) and abs(dif) <= TOL)
        res.append({"cod_prov": cod, "provincia": g.provincia.iloc[0], "periodo": per, "min": g.deficit.min(),
                    "mediana": g.deficit.median(), "max": g.deficit.max(), "n_rutas_hogares": g.ruta_hogares.nunique(),
                    "n_fuentes_altas": g.fuente_altas.nunique(), "dif_rel_altas_catastro_vs_mivau": dif,
                    "altas_triangulan_15pct": tri, "capa": "C2" if tri else "C4",
                    "motivo_capa": ("altas MIVAU y Catastro coinciden en ±15 %; hogares de una fuente (ECP) y bajas supuestas: C2"
                                    if tri else "altas sin triangular en ±15 % (o sin Catastro: foral) -> C4")})
    return pd.DataFrame(res)


def robustez_censo_anual(t: pd.DataFrame, pr: pd.DataFrame) -> pd.DataFrame:
    """Vía Censo anual (personas / tamaño medio 2021): robustez, fuera de la cifra principal; cuantifica el sesgo en ΔH."""
    r = t[t.ambito == "robustez"].drop_duplicates(["cod_prov", "periodo"])[["cod_prov", "periodo", "delta_hogares"]]
    p = t[t.ambito == "principal"].drop_duplicates(["cod_prov", "periodo"])[["cod_prov", "periodo", "delta_hogares"]]
    m = r.merge(p, on=["cod_prov", "periodo"], suffixes=("_censo_anual", "_principal"))
    m["cociente"] = m.delta_hogares_censo_anual / m.delta_hogares_principal
    d = t[t.ambito == "robustez"]
    d = d[d.protegida.isin(["con", "incluida"])].groupby(["cod_prov", "periodo"]).deficit.agg(["min", "median", "max"]).reset_index()
    return m.merge(d, on=["cod_prov", "periodo"]).rename(columns={"min": "deficit_min", "median": "deficit_mediana", "max": "deficit_max"})


# ------------------------------------------------------------------ déficit municipal
def deficit_municipal(reg, ca, cm, cat, filtro) -> pd.DataFrame:
    c11 = mapa_2011(cm)
    tam21 = ca[2021] / cm.V_PRINCIPAL
    grandes = ca.index[ca[2021] > UMBRAL]
    filas = []
    for m in grandes:
        if filtro and m[:2] not in filtro:
            continue
        if m not in cm.index or m not in tam21.index or not np.isfinite(tam21.get(m, np.nan)):
            continue
        h21, h25 = ca.loc[m, 2021] / tam21[m], ca.loc[m, 2025] / tam21[m]
        cs = cat.loc[m] if m in cat.index else pd.Series(dtype=float)
        for per, h0, a0, a1 in (("2021-2025", h21, 2021, 2025), ("2012-2025", c11.get(m, np.nan), 2012, 2025)):
            nc = cs.get(a1, np.nan) - cs.get(a0, np.nan)
            filas.append({"cod_mun": m, "municipio": cm.nombre.get(m, ""), "cod_prov": m[:2], "periodo": per,
                          "pob_2021": ca.loc[m, 2021], "personas_por_hogar_2021": tam21[m], "hogares_ini": h0, "hogares_fin": h25,
                          "delta_hogares": h25 - h0, "altas_catastro": nc, "deficit": h25 - h0 - nc,
                          "fuentes_hogares": 1, "fuentes_altas": 1, "capa": "C4"})
    t = pd.DataFrame(filas)
    t["deficit_valido"] = t.deficit.notna()
    for per, g in t.groupby("periodo"):
        reg.log("M1_mun", f"M1mun_{per}", "D municipal (Catastro; hogares Censo anual / tamaño 2021)", per[:4], per[5:],
                int(g.deficit.notna().sum()), np.nan, np.nan, np.nan, np.nan, g.deficit.sum(), np.nan,
                f"C4 fuente única; suma de municipios >{UMBRAL} hab")
    return t


# ------------------------------------------------------------------ concentración
def concentracion(serie: pd.Series, niveles=(0.5, 0.8)) -> dict:
    pos = serie[serie > 0].sort_values(ascending=False)
    if pos.empty:
        return {f"n_{int(100 * q)}": 0 for q in niveles} | {"total_positivo": 0.0, "n_positivos": 0}
    cum = pos.cumsum() / pos.sum()
    out = {f"n_{int(100 * q)}": int((cum < q).sum() + 1) for q in niveles}
    out |= {"total_positivo": float(pos.sum()), "n_positivos": int(len(pos))}
    return out


def tablas_concentracion(prov_res: pd.DataFrame, t_prov: pd.DataFrame, mun: pd.DataFrame):
    filas, exc = [], []
    for per in ["2012-2025", "2021-2025"]:
        r = prov_res[prov_res.periodo == per].set_index("cod_prov")
        c = concentracion(r.mediana)
        filas.append({"nivel": "provincia", "periodo": per, "escenario": "mediana", "n_unidades": len(r), **c})
        base = t_prov[(t_prov.periodo == per) & t_prov.protegida.isin(["con", "incluida"])]
        ns = {50: [], 80: []}
        for _, g in base.groupby(["ruta_hogares", "fuente_altas", "bajas_pct"], dropna=False):
            cc = concentracion(g.set_index("cod_prov").deficit)
            ns[50].append(cc["n_50"])
            ns[80].append(cc["n_80"])
        filas.append({"nivel": "provincia", "periodo": per, "escenario": "rango entre combinaciones", "n_unidades": len(r),
                      "n_50": f"{min(ns[50])}-{max(ns[50])}", "n_80": f"{min(ns[80])}-{max(ns[80])}",
                      "total_positivo": np.nan, "n_positivos": np.nan})
        neg = r.mediana[r.mediana < 0]
        exc.append({"nivel": "provincia", "periodo": per, "n_excedente": int(len(neg)), "viviendas_excedente_mediana": abs(float(neg.sum())),
                    "viviendas_excedente_min": abs(float(r[r["max"] < 0]["max"].sum())),
                    "viviendas_excedente_max": abs(float(r[r["min"] < 0]["min"].sum())),
                    "nota": "min/max: solo provincias con exceso en todas las combinaciones, suma de la cota correspondiente"})
        m = mun[(mun.periodo == per) & mun.deficit_valido].set_index("cod_mun").deficit
        c = concentracion(m)
        filas.append({"nivel": "municipio", "periodo": per, "escenario": "Catastro, fuente única", "n_unidades": len(m), **c})
        neg = m[m < 0]
        exc.append({"nivel": "municipio", "periodo": per, "n_excedente": int(len(neg)), "viviendas_excedente_mediana": abs(float(neg.sum())),
                    "viviendas_excedente_min": np.nan, "viviendas_excedente_max": np.nan, "nota": "Catastro, fuente única (C4)"})
    return pd.DataFrame(filas), pd.DataFrame(exc)


# ------------------------------------------------------------------ latente
def latente(nombres) -> tuple[pd.DataFrame, dict]:
    s = pd.read_csv(RAIZ / "output" / "v3" / "PA" / "tablas" / "A2_series_tasa.csv").set_index("anio")
    p = pd.read_csv(RAW / "ine_v2_padron_prov_edad_nac.csv", dtype={"codigo": str})
    p = p[(p.desglose == "nacionalidad=Total; edad=20-34") & (p.periodo == "2025T1")]
    pp = p[p.nivel == "provincia"].set_index("codigo").valor
    nac = float(p[p.nivel == "nacional"].valor.iloc[0])
    pob_n = float(s.loc[2025, "pob_25_34_epa"])
    pob25 = float(s.loc[2025, "pob_25_34_epa"])
    del pob_n
    esc = []
    for fuente, col in (("Eurostat/ECV", "tasa_eurostat_ecv_ES"), ("EPA hijo/a de persona de referencia", "tasa_epa_hijo_persona_ref_ES")):
        t25, t08 = float(s.loc[2025, col]), float(s.loc[2008, col])
        for ppl in (1.5, 2.0):
            esc.append({"fuente_tasa": fuente, "tasa_2008": t08, "tasa_2025": t25, "personas_hogar_joven": ppl,
                        "nacional": (t25 - t08) / 100 * pob25 / ppl})
    e = pd.DataFrame(esc)
    filas = []
    for cod, v in pp.items():
        if cod not in nombres:
            continue
        sh = v / nac
        filas.append({"cod_prov": cod, "provincia": nombres[cod], "pob_20_34_2025": v, "cuota_nacional": sh,
                      "latente_min": e.nacional.min() * sh, "latente_max": e.nacional.max() * sh,
                      "latente_mediana": e.nacional.median() * sh, "capa": "C2"})
    return pd.DataFrame(filas), {"escenarios": e, "pob_20_34_nacional": nac, "pob_25_34": pob25}


# ------------------------------------------------------------------ figuras
def figuras(prov_res: pd.DataFrame, mun: pd.DataFrame, lat: pd.DataFrame) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rutas = []
    (OUT / "figuras").mkdir(parents=True, exist_ok=True)
    for per in ["2021-2025", "2012-2025"]:
        r = prov_res[prov_res.periodo == per].sort_values("mediana", ascending=False)
        fig, ax = plt.subplots(figsize=(8, 12))
        y = np.arange(len(r))
        ax.barh(y, r.mediana, color=np.where(r.mediana >= 0, "#b04a3a", "#3a7ab0"),
                xerr=[r.mediana - r["min"], r["max"] - r.mediana], ecolor="gray", capsize=1.5)
        ax.set_yticks(y)
        ax.set_yticklabels(r.provincia, fontsize=6)
        ax.invert_yaxis()
        ax.set_xlabel("viviendas (mediana y rango entre combinaciones)")
        ax.set_title(f"Déficit contable por provincia {per} (hogares − altas)\nCapa por provincia en tabla; coropleta no disponible (sin geopandas)", fontsize=9)
        fig.tight_layout()
        f = OUT / "figuras" / f"M1_deficit_provincias_{per}.png"
        fig.savefig(f, dpi=110)
        plt.close(fig)
        rutas.append(str(f.relative_to(RAIZ)))
    for per in ["2021-2025", "2012-2025"]:
        r = mun[(mun.periodo == per) & mun.deficit_valido].nlargest(20, "deficit")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(r.municipio.str[:28], r.deficit, color="#b04a3a")
        ax.invert_yaxis()
        ax.set_xlabel("viviendas (Catastro; capa C4)")
        ax.set_title(f"20 municipios con mayor déficit contable {per}", fontsize=9)
        fig.tight_layout()
        f = OUT / "figuras" / f"M1_top20_municipios_{per}.png"
        fig.savefig(f, dpi=110)
        plt.close(fig)
        rutas.append(str(f.relative_to(RAIZ)))
    r = lat.sort_values("latente_mediana", ascending=False).head(30)
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.barh(r.provincia, r.latente_mediana, xerr=[r.latente_mediana - r.latente_min, r.latente_max - r.latente_mediana],
            color="#6a8f3a", ecolor="gray")
    ax.invert_yaxis()
    ax.set_xlabel("hogares implícitos (C2, referencia España 2008)")
    ax.set_title("Demanda latente por emancipación retrasada, 30 primeras provincias", fontsize=9)
    fig.tight_layout()
    f = OUT / "figuras" / "M1_latente_provincias.png"
    fig.savefig(f, dpi=110)
    plt.close(fig)
    rutas.append(str(f.relative_to(RAIZ)))
    return rutas


# ------------------------------------------------------------------ main
def main() -> None:
    (OUT / "tablas").mkdir(parents=True, exist_ok=True)
    reg = econ_utils.Registry(OUT / "registro.csv")
    filtro = ["46"] if SMOKE else None
    H, nombres = provincias_ecp()
    ca = leer_censo_anual()
    cm = pdat.censo2021_municipios()
    cat = catastro_stock()
    lib, pro = terminadas_mivau()
    t = deficit_provincial(reg, H, nombres, ca, cm, cat, lib, pro, filtro)
    pr = resumen_prov(t)
    mun = deficit_municipal(reg, ca, cm, cat, filtro)
    if SMOKE:
        print(pr.to_string())
        print(mun.groupby("periodo").deficit.describe())
        print("match 2011:", mun[mun.periodo == "2012-2025"].deficit.notna().mean())
        return
    conc, exc = tablas_concentracion(pr, t, mun)
    lat, lat_info = latente(nombres)
    rob = robustez_censo_anual(t, pr)
    rob.to_csv(OUT / "tablas" / "M1_robustez_censo_anual.csv", index=False, float_format="%.4f")
    pr2 = pr.merge(lat[["cod_prov", "latente_min", "latente_mediana", "latente_max"]], on="cod_prov", how="left")
    t.to_csv(OUT / "tablas" / "M1_provincias_combinaciones.csv", index=False, float_format="%.4f")
    pr2.to_csv(OUT / "tablas" / "M1_provincias.csv", index=False, float_format="%.4f")
    mun.to_csv(OUT / "tablas" / "M1_municipios.csv", index=False, float_format="%.4f")
    conc.to_csv(OUT / "tablas" / "M1_concentracion.csv", index=False, float_format="%.4f")
    exc.to_csv(OUT / "tablas" / "M1_excedentes.csv", index=False, float_format="%.4f")
    lat.to_csv(OUT / "tablas" / "M1_latente_provincias.csv", index=False, float_format="%.4f")
    lat_info["escenarios"].to_csv(OUT / "tablas" / "M1_latente_escenarios_nacional.csv", index=False, float_format="%.4f")
    # lista de los 20 primeros
    top = []
    for per in ["2012-2025", "2021-2025"]:
        r = pr[pr.periodo == per].nlargest(20, "mediana").assign(nivel="provincia", ranking=lambda d: range(1, len(d) + 1))
        top.append(r.rename(columns={"provincia": "unidad", "cod_prov": "codigo"})[["nivel", "periodo", "ranking", "codigo", "unidad", "min", "mediana", "max", "capa"]])
        m = mun[(mun.periodo == per) & mun.deficit_valido].nlargest(20, "deficit").assign(nivel="municipio", ranking=lambda d: range(1, len(d) + 1))
        top.append(m.rename(columns={"cod_mun": "codigo", "municipio": "unidad", "deficit": "mediana"})
                   .assign(min=np.nan, max=np.nan)[["nivel", "periodo", "ranking", "codigo", "unidad", "min", "mediana", "max", "capa"]])
    pd.concat(top).to_csv(OUT / "tablas" / "M1_top20.csv", index=False, float_format="%.1f")
    figs = figuras(pr, mun, lat)
    reg.flush()
    escribir_json(t, pr, mun, conc, exc, lat, lat_info, figs)


def nacional_comun(t: pd.DataFrame, per: str) -> dict:
    """Suma de provincias por combinación; muestra común = provincias con todas las combinaciones (sin forales)."""
    b = t[(t.periodo == per) & (t.ambito == "principal") & t.protegida.isin(["con", "incluida"])]
    comun = sorted(set(b.cod_prov) - set(FORALES))
    s = b[b.cod_prov.isin(comun)].groupby(["ruta_hogares", "fuente_altas", "bajas_pct"], dropna=False).deficit.sum()
    s_fo = b[b.fuente_altas.str.startswith("MIVAU")].groupby(["ruta_hogares", "bajas_pct"]).deficit.sum()
    return {"n_prov_comun": len(comun), "min": float(s.min()), "max": float(s.max()), "mediana": float(s.median()),
            "n_combinaciones": int(len(s)), "signo_unico": bool((s > 0).all() or (s < 0).all()),
            "n_prov_fin_obra": int(b.cod_prov.nunique()), "min_fin_obra_todas": float(s_fo.min()), "max_fin_obra_todas": float(s_fo.max())}


def escribir_json(t, pr, mun, conc, exc, lat, lat_info, figs) -> None:
    nac = {p: nacional_comun(t, p) for p in ["2012-2025", "2021-2025"]}
    hechos = []

    def top(per, n=10):
        r = pr[pr.periodo == per].nlargest(n, "mediana")
        return [f"{a} ({b:,.0f})".replace(",", ".") for a, b in zip(r.provincia, r.mediana)]

    for per in nac:
        n = nac[per]
        capa = "C2" if per == "2021-2025" and n["signo_unico"] else "C4"
        hechos.append({
            "id": f"M1-H-nacional-{per}",
            "enunciado_neutro": f"Suma provincial del déficit contable (Δ hogares − altas) {per}, muestra común de {n['n_prov_comun']} provincias",
            "capa": capa, "magnitud": n["mediana"], "unidad": "viviendas", "intervalo": [n["min"], n["max"]],
            "fuentes": ["ECP INE" if per == "2021-2025" else "Censos 2011/2021 + ECP", "MIVAU fin de obra", "Catastro"],
            "supuestos": ["bajas del parque 0/0,1/0,2 % anual (supuesto: la cifra con bajas es C2)"],
            "limites": ["Hogares de una sola fuente (ECP, 2021T1-2025T4 = 4,75 años) frente a 5 años de altas: ventana ≈5 % más corta en hogares", "Catastro no cubre territorios forales (Álava, Bizkaia, Gipuzkoa, Navarra): el rango usa 48 provincias",
                        "Déficit contable no equivale a demanda insatisfecha a cualquier precio"] +
                       ([] if capa == "C1" else ["Tramo de hogares 2011-2021 de fuente única"])})
        hechos.append({
            "id": f"M1-H-top10-prov-{per}",
            "enunciado_neutro": f"Provincias con mayor déficit contable {per} (mediana entre combinaciones): " + "; ".join(top(per)),
            "capa": "C4", "magnitud": float(pr[pr.periodo == per].nlargest(10, "mediana").mediana.sum()),
            "unidad": "viviendas (suma de 10 provincias)", "intervalo": [float(pr[pr.periodo == per].nlargest(10, "mediana")["min"].sum()),
                                                                          float(pr[pr.periodo == per].nlargest(10, "mediana")["max"].sum())],
            "fuentes": ["ECP", "Censo anual", "MIVAU", "Catastro"], "supuestos": ["como arriba"],
            "limites": ["Capa por provincia en M1_provincias.csv (C2 si las altas MIVAU y Catastro coinciden en ±15 %, si no C4)"]})
    for r in conc.itertuples():
        hechos.append({
            "id": f"M1-H-concentracion-{r.nivel}-{r.periodo}",
            "enunciado_neutro": f"Unidades ({r.nivel}) que acumulan el 50 % y el 80 % del déficit positivo {r.periodo}: {r.n_50} y {r.n_80} ({r.escenario})",
            "capa": "C4", "magnitud": r.n_80, "unidad": "unidades (80 %)",
            "intervalo": [None, None], "fuentes": ["M1_provincias.csv" if r.nivel == "provincia" else "Catastro + Censo anual"],
            "supuestos": ["déficit = mediana entre combinaciones (provincias) o única estimación (municipios)"] + ([] if r.nivel == "provincia" else ["hogares municipales = personas del Censo anual / tamaño medio de hogar del Censo 2021 constante (sesga ΔH a la baja si el tamaño cae; ver M1_robustez_censo_anual.csv)"]),
            "limites": ["Depende del universo con datos"]})
    for r in exc.itertuples():
        hechos.append({
            "id": f"M1-H-excedente-{r.nivel}-{r.periodo}",
            "enunciado_neutro": f"{r.n_excedente} {r.nivel}s con déficit negativo (altas > Δ hogares) {r.periodo}, suma {r.viviendas_excedente_mediana:,.0f} viviendas".replace(",", "."),
            "capa": "C4", "magnitud": r.viviendas_excedente_mediana,
            "unidad": "viviendas", "intervalo": [None if pd.isna(r.viviendas_excedente_min) else r.viviendas_excedente_min,
                                                 None if pd.isna(r.viviendas_excedente_max) else r.viviendas_excedente_max],
            "fuentes": ["como arriba"], "supuestos": ["excedente contable; no implica vivienda vacía ni utilizable"] + ([] if r.nivel == "provincia" else ["hogares municipales = personas Censo anual / tamaño medio 2021 constante (sesgo a la baja de ΔH)"]),
            "limites": ["Puede reflejar segunda residencia, vacía o hogares no captados"]})
    e = lat_info["escenarios"]
    hechos.append({
        "id": "M1-H-latente-provincias", "enunciado_neutro": "Demanda latente por emancipación retrasada repartida por provincias según población de 20-34 años (referencia: tasa de convivencia con los padres de España 2008)",
        "capa": "C2", "magnitud": float(e.nacional.median()), "unidad": "hogares implícitos (nacional)",
        "intervalo": [float(e.nacional.min()), float(e.nacional.max())],
        "fuentes": ["Eurostat ilc_lvps08 / ECV", "EPA 65944", "Padrón INE 20-34 años por provincia"],
        "supuestos": ["Tasa de convivencia 2008 como referencia contrafactual", "personas por hogar joven 1,5-2,0",
                      "misma brecha de tasa en todas las provincias (no hay tasa provincial)"],
        "limites": ["Solo cambia la población joven entre provincias", "M2 (output/v4/M2) no estaba disponible al calcular",
                    "No se suma al déficit: puede solaparse con Δ hogares observado"]})
    rob = pd.read_csv(OUT / "tablas" / "M1_robustez_censo_anual.csv", dtype={"cod_prov": str})
    r21 = rob[rob.periodo == "2021-2025"]
    n21c = nac["2021-2025"]
    hechos.append({
        "id": "M1-H-conciliacion-M0", "enunciado_neutro": "Conciliación del déficit nacional 2021-2025 con M0/v3 (701 mil; 560-969 mil)",
        "capa": "C2", "magnitud": n21c["min_fin_obra_todas"], "unidad": "viviendas (52 provincias, MIVAU, bajas 0 %)",
        "intervalo": [n21c["min_fin_obra_todas"], n21c["max_fin_obra_todas"]],
        "fuentes": ["ECP", "MIVAU fin de obra", "Catastro"],
        "supuestos": ["mismos Δ hogares ECP 2021T1-2025T4 y terminadas 2021-2025 que M0"],
        "limites": ["Con bajas 0 % y 52 provincias la cifra coincide con M0 (≈701 mil); con bajas 0,2 % llega a ≈967 mil (techo 969 mil de v3)",
                    "Con Catastro (48 provincias, sin Álava, Bizkaia, Gipuzkoa ni Navarra) el déficit es menor (≈657 mil) porque el Catastro suma más altas que el fin de obra",
                    "El suelo 560 mil de v3 no se reproduce en M1: incluye otra fuente de hogares o altas (Δ parque); la diferencia es de fuente"]})
    hechos.append({
        "id": "M1-H-robustez-censo-anual", "enunciado_neutro": "Vía Censo anual (personas / tamaño medio 2021) fuera de la cifra principal: ΔH 2021-2025 frente a ECP",
        "capa": "C4", "magnitud": float(r21.delta_hogares_censo_anual.sum()), "unidad": "hogares (52 provincias)",
        "intervalo": [float(r21.delta_hogares_principal.sum()), float(r21.delta_hogares_principal.sum())],
        "fuentes": ["Censo anual INE", "ECP INE (comparación)"],
        "supuestos": ["tamaño medio de hogar constante en 2021 (sesgo a la baja de ΔH cuando el tamaño cae)"],
        "limites": ["Ventana 1-ene-2021 a 1-ene-2025 (4 años)", "No independiente de ECP (ambos derivan del padrón)", "Solo robustez"]})
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=2))
    n21, n25 = nac["2021-2025"], nac["2012-2025"]
    cm = conc.set_index(["nivel", "periodo", "escenario"])
    res = {
        "rama": "M1", "pregunta": "¿Dónde se concentra el déficit contable de vivienda (hogares frente a viviendas nuevas)?",
        "capa": "C2 (déficit nacional 2021-2025 y provincias con altas triangulables en ±15 %) / C4 (resto, municipios, 2012-2025) / C2 (latente)",
        "datos": ["ine_v2_hogares_prov", "ine_v3_gis_seccion (Censo anual)", "censo 2011/2021", "mivau_v2_iniciadas_terminadas_prov",
                  "mivau_v2_protegida", "catastro_urbana_municipios", "ine_v2_padron_prov_edad_nac"],
        "N": {"provincias": int(pr.cod_prov.nunique()), "municipios_2021_2025": int(mun[(mun.periodo == "2021-2025") & mun.deficit_valido].shape[0]),
              "municipios_2012_2025": int(mun[(mun.periodo == "2012-2025") & mun.deficit_valido].shape[0])},
        "metodo": "Déficit contable D = Δhogares − altas netas; rutas de hogares y fuentes de altas cruzadas; bajas 0/0,1/0,2 %",
        "estimacion": {"nacional_2021_2025": n21, "nacional_2012_2025": n25},
        "ic95": None, "p_ajustado": None,
        "nivel_evidencia": "ASOCIACIÓN/DESCRIPTIVO (sin identificación causal)",
        "diagnosticos": {"concentracion": conc.replace({np.nan: None}).to_dict("records"), "excedentes": exc.replace({np.nan: None}).to_dict("records"),
                         "capas_provincia_2021_2025": pr[pr.periodo == "2021-2025"].capa.value_counts().to_dict(),
                         "mapa": "sin geopandas: gráficos de barras ordenados (no coropleta)"},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": ["No hay contrastes de hipótesis: FDR no aplicable; todas las combinaciones están en registro.csv",
                  "Municipal: sin terminadas MIVAU por municipio en data/raw/mivau_*; solo Catastro (C4); no se descargó nada",
                  "EPA provincial solo ocupados/parados: no hay hogares por provincia en EPA",
                  "Censo anual n_personas = 1 de enero; vía Censo anual solo en robustez (M1_robustez_censo_anual.csv)",
                  "Cifra principal: ECP (única fuente de hogares) y altas MIVAU/Catastro; C1 exigiría dos fuentes independientes dentro de ±15 %: no se cumple en hogares",
                  "Ventanas: ECP 2021T1-2025T4 (4,75 años) frente a 5 años de altas",
                  "Cruce censo 2011 municipal por nombre; homónimos descartados"],
        "figuras": figs}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=2, default=float))
    print(json.dumps({"nac": nac, "conc": conc.replace({np.nan: None}).to_dict("records"), "exc": exc.replace({np.nan: None}).to_dict("records")},
                     ensure_ascii=False, default=float))


if __name__ == "__main__":
    main()

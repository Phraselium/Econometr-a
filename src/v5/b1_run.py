"""B1 · Necesidad de vivienda por provincia 2026-2035 (stock-flujo por componentes). Determinista, sin red.

Necesidad = A + R + V + F - M - K - L (D y S aparte). Detalle y supuestos en output/v5/B1/metodo.md
y en docs/v5/decisiones.md. Uso: python3 src/v5/b1_run.py [--smoke]
Todo se calcula en viviendas; el horizonte es 1-ene-2026 a 1-ene-2036 (10 años).
"""
from __future__ import annotations

import gzip
import json
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
for p in ("src", "src/v3", "src/v4"):
    sys.path.insert(0, str(RAIZ / p))
import econ_utils  # noqa: E402
import m1_run as m1  # noqa: E402
import pa_data as pdat  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
RAW = RAIZ / "data" / "raw"
V5 = RAW / "v5"
OUT = RAIZ / "output" / "v5" / "B1"
SMOKE = "--smoke" in sys.argv
Y0, Y1 = 2026, 2036  # stock a 1-ene de cada año; flujo 2026-2035
FRAC_M = (0.10, 0.20, 0.30)       # P-D v3: fracción movilizable de vacías (supuesto del encargo)
FRIC = (0.00, 0.02, 0.04)         # vacancia friccional: 0 si ya hay >= objetivo; 2 % y 4 % del encargo
H_FACT = (0.85, 1.00, 1.15)       # factor sobre la tasa de jefatura 65+ de M2 para 75+ (supuesto, sin dato propio)
DISOL = (0.5, 0.75, 1.0)          # fracción de muertes de jefes que disuelve el hogar (parejas 0,5 / solos 1,0)
FECHA = {
    "proy_hogares": "INE Proyección de Hogares (tabla 54562, mod. 2026-06-17), base 1-ene-2026",
    "proy_pob": "INE Proyecciones de Población 2024-2074 (tabla 36726, corto plazo)",
    "mort": "INE Tablas de mortalidad por provincia 2024 (tabla 67235, mod. 2025-11)",
    "censo": "INE Censo 2021 (1-nov-2021)",
    "mivau": "MIVAU Boletín Online (hasta 2025)",
    "cat": "Catastro estadísticas urbanas (ejercicios 2012-2025)",
}


def kn(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    s = s.split("/")[0].split(",")[0]
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^a-z]", "", s)


def triple(lo, c, hi):
    return {"min": lo, "central": c, "max": hi}


# ---------------------------------------------------------------- lecturas
def lee_proy_hogares() -> pd.DataFrame:
    h = pd.read_csv(V5 / "ine_b1_t54562_proy_hogares.csv")
    h = h[h.nombre.str.endswith(". Total. ")].copy()
    h["k"] = h.nombre.str.replace(". Total. ", "", regex=False).map(kn)
    nac = h[h.k == "totalnacional"].set_index("anyo").valor
    h = h[h.k != "totalnacional"].drop_duplicates(["k", "anyo"])
    return h.pivot(index="k", columns="anyo", values="valor"), nac


def lee_proy_pob() -> tuple[pd.DataFrame, pd.Series]:
    p = pd.read_csv(V5 / "ine_b1_t36726_proy_poblacion_prov.csv")
    m = p.nombre.str.extract(r"^Total\. Población\. (.+?)\. Proyección a corto plazo\. (.+?)\. $")
    p["terr"], p["edad"] = m[0], m[1]
    p["k"] = p.terr.map(kn)

    def edad(e):
        if e == "Todas las edades":
            return -1
        return int(re.match(r"(\d+)", e).group(1))
    p["e"] = p.edad.map(edad)
    nac = p[p.k == "totalnacional"]
    p = p[p.k != "totalnacional"]
    return p[["k", "e", "anyo", "valor"]], nac[nac.e == -1].set_index("anyo").valor


def lee_mortalidad() -> pd.DataFrame:
    q = pd.read_csv(V5 / "ine_b1_t67235_mortalidad_prov.csv")
    m = q.nombre.str.extract(r"^(.+?)\. Total\. (.+?)\. Riesgo de muerte")
    q["k"] = m[0].map(kn)
    q["e0"] = m[1].map(lambda e: int(re.search(r"(\d+)", e).group(1)))
    return q[["k", "e0", "valor"]].drop_duplicates(["k", "e0"])  # por mil


def lee_saldos() -> pd.DataFrame:
    s = pd.read_csv(V5 / "ine_b1_t69764_saldos_prov.csv")
    s = s[s.nombre.str.contains("Saldo interior")].copy()
    s["k"] = s.nombre.str.extract(r"^(.+?)\. Todas las edades")[0].map(kn)
    s = s[s.k != "totalnacional"].drop_duplicates(["k", "anyo"])
    return s.pivot(index="k", columns="anyo", values="valor")


def lee_censo_secciones(serie: str) -> pd.Series:
    d = pd.read_csv(RAW / "v3" / "ine_v3_censo2021_seccion_indicadores.csv.gz", dtype={"codigo": str},
                    usecols=["serie", "codigo", "valor"])
    d = d[d.serie == serie]
    return d.groupby(d.codigo.str.zfill(10).str[:2]).valor.sum()


def serie_prov(df: pd.DataFrame, patron: str, nombres: dict[str, str], extra: dict | None = None) -> pd.DataFrame:
    """Serie anual por provincia (cod x año) a partir de tablas MIVAU con territorio (misma lógica que M1)."""
    a = df[df.serie.str.contains(patron) & df.nivel.isin(["provincia", "ccaa", "ciudad_autonoma"])]
    t = a.pivot_table(index="territorio", columns="periodo", values="valor", aggfunc="first")
    t.columns = t.columns.astype(int)
    claves = {m1.norm(x): x for x in t.index}
    filas = {}
    for cod, nom in nombres.items():
        terr = (extra or {}).get(cod) or claves.get(m1.norm(nom)) or claves.get(m1.norm(nom.split("/")[0]))
        if terr in t.index:
            filas[cod] = t.loc[terr]
    return pd.DataFrame(filas).T


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "tablas").mkdir(exist_ok=True)
    (OUT / "figuras").mkdir(exist_ok=True)
    reg = econ_utils.Registry(OUT / "registro.csv")
    Hecp, nombres = m1.provincias_ecp()
    cods = sorted(nombres)
    if SMOKE:
        cods = ["46", "28", "52"]
    kcod = {c: kn(nombres[c]) for c in cods}
    assert len(set(kcod.values())) == len(kcod)
    base = pd.DataFrame({"cod_prov": cods, "provincia": [nombres[c] for c in cods]}).set_index("cod_prov")

    # ---------------- F · flujo futuro (INE) y método alternativo
    hp, hnac = lee_proy_hogares()
    pp, pnac = lee_proy_pob()
    pob = pp[pp.e == -1].pivot(index="k", columns="anyo", values="valor")
    for c in cods:
        k = kcod[c]
        assert k in hp.index and k in pob.index, f"sin proyección: {c} {k}"
    base["hogares_2026"] = [hp.loc[kcod[c], Y0] for c in cods]
    base["hogares_2036"] = [hp.loc[kcod[c], Y1] for c in cods]
    f_ine = base.hogares_2036 - base.hogares_2026
    pr = pd.Series({c: pob.loc[kcod[c], Y1] / pob.loc[kcod[c], Y0] - 1 for c in cods})
    f_alt = base.hogares_2026 * pr          # jefatura constante de 2026 con población proyectada
    base["F_ine"] = f_ine
    base["F_alt"] = f_alt
    base["F_min"], base["F_max"] = np.minimum(f_ine, f_alt), np.maximum(f_ine, f_alt)
    base["F_central"] = f_ine
    base["tam_hogar_2026"] = [pob.loc[kcod[c], Y0] / hp.loc[kcod[c], Y0] for c in cods]

    # ---------------- A · atraso
    a4 = pd.read_csv(RAIZ / "output/v5/A4/clasificacion_provincias.csv", dtype={"cod_prov": str}).set_index("cod_prov")
    lat = pd.read_csv(RAIZ / "output/v4/M1/tablas/M1_provincias.csv", dtype={"cod_prov": str})
    lat = lat[lat.periodo == "2021-2025"].set_index("cod_prov")
    base["A1_min"] = a4.deficit_2021_2025_min.clip(lower=0).reindex(base.index)
    base["A1_central"] = a4.deficit_2021_2025_mediana.clip(lower=0).reindex(base.index)
    base["A1_max"] = a4.deficit_2021_2025_max.clip(lower=0).reindex(base.index)
    base["A2_min"] = lat.latente_min.reindex(base.index)
    base["A2_central"] = lat.latente_mediana.reindex(base.index)
    base["A2_max"] = lat.latente_max.reindex(base.index)
    for s in ("min", "central", "max"):
        base[f"A_{s}"] = base[f"A1_{s}"] + base[f"A2_{s}"]
    base["clase_A4"] = a4.clase_2021_2025.reindex(base.index)
    base["presion"] = base.clase_A4.isin([1, 2])

    # ---------------- R · reposición (dos métodos)
    c11 = pdat.censo2011_provincias()
    cm = pdat.censo2021_municipios().copy()
    cm["cod_prov"] = cm.index.str[:2]
    c21 = cm.groupby("cod_prov").V_TOTAL.sum()
    base["viv_total_2021"] = c21.reindex(base.index)
    mi = pd.read_csv(RAW / "mivau_v2_iniciadas_terminadas_prov.csv")
    mp = pd.read_csv(RAW / "mivau_v2_protegida.csv")
    ex_l = {c: m1.UNIPROV.get(c) for c in cods}
    ex_p = {c: m1.UNIPROV_PROT.get(c) for c in cods}
    lib_t = serie_prov(mi, "viv_libres_terminadas_anual", nombres, ex_l)
    pro_t = serie_prov(mp, "prot_definitiva_anual", nombres, ex_p)
    lib_i = serie_prov(mi, "viv_libres_iniciadas_anual", nombres, ex_l)
    pro_i = serie_prov(mp, "prot_provisional_anual", nombres, ex_p)
    cat = m1.catastro_stock()
    cat_p = cat.groupby(cat.index.str[:2]).sum(min_count=1)
    cat_p.columns = cat_p.columns.astype(int)

    def acum(t, c, a, b):
        if c not in t.index:
            return np.nan
        v = t.loc[c, [y for y in range(a, b + 1) if y in t.columns]]
        return float(v.sum()) if len(v) == (b - a + 1) else np.nan

    rate_c, rate_k, b_c, b_k = {}, {}, {}, {}
    for c in cods:
        k = pdat.clave(nombres[c])
        term_c = acum(lib_t, c, 2012, 2021) + (acum(pro_t, c, 2012, 2021) if c in pro_t.index else 0.0)
        if k in c11.index and np.isfinite(term_c):
            v11 = c11.loc[k, "Total viviendas"]
            b_c[c] = v11 + term_c - base.loc[c, "viv_total_2021"]
            rate_c[c] = b_c[c] / (10 * v11)
        term_k = acum(lib_t, c, 2012, 2024) + (acum(pro_t, c, 2012, 2024) if c in pro_t.index else 0.0)
        if c not in m1.FORALES and c in cat_p.index and np.isfinite(term_k) and 2012 in cat_p.columns and 2025 in cat_p.columns:
            u0, u1 = cat_p.loc[c, 2012], cat_p.loc[c, 2025]
            if np.isfinite(u0) and np.isfinite(u1):
                b_k[c] = term_k - (u1 - u0)
                rate_k[c] = b_k[c] / (13 * u0)
    base["R_bajas_censo_1121"] = pd.Series(b_c)
    base["R_bajas_catastro_1224"] = pd.Series(b_k)
    base["R_tasa_censo"] = pd.Series(rate_c)
    base["R_tasa_catastro"] = pd.Series(rate_k)
    tm = base[["R_tasa_censo", "R_tasa_catastro"]].clip(lower=0)
    base["R_n_metodos"] = tm.notna().sum(axis=1)
    base["R_tasa_min"], base["R_tasa_max"], base["R_tasa_central"] = tm.min(axis=1), tm.max(axis=1), tm.mean(axis=1)
    for s in ("min", "central", "max"):
        base[f"R_{s}"] = 10 * base[f"R_tasa_{s}"] * base.viv_total_2021  # 10 años

    # ---------------- V · vacancia friccional (solo con presión)
    alq = lee_censo_secciones("t20_2")
    base["alquiler_2021"] = alq.reindex(base.index)
    for s, f in zip(("min", "central", "max"), FRIC):
        base[f"V_{s}"] = np.where(base.presion, f * base.alquiler_2021, 0.0)

    # ---------------- M · vacías movilizables (solo con presión)
    vac = pd.read_csv(RAIZ / "output/v5/R1C/vacias_esporadicas_municipio_censo2021.csv")
    vac["cod_prov"] = vac.terr.str[:2]
    vp = vac.groupby("cod_prov")[["vacias", "esporadicas", "totales"]].sum()
    base["vacias_2021"] = vp.vacias.reindex(base.index)
    base["esporadicas_2021"] = vp.esporadicas.reindex(base.index)
    for s, f in zip(("min", "central", "max"), FRAC_M):
        base[f"M_{s}"] = np.where(base.presion, f * base.vacias_2021, 0.0)

    # ---------------- K · cartera en construcción (iniciadas - terminadas, últimas N campañas)
    def kwin(n):
        out = {}
        for c in cods:
            ini = acum(lib_i, c, 2025 - n + 1, 2025) + (acum(pro_i, c, 2025 - n + 1, 2025) if c in pro_i.index else 0.0)
            ter = acum(lib_t, c, 2025 - n + 1, 2025) + (acum(pro_t, c, 2025 - n + 1, 2025) if c in pro_t.index else 0.0)
            out[c] = max(0.0, ini - ter) if np.isfinite(ini) and np.isfinite(ter) else np.nan
        return pd.Series(out)
    k2, k3 = kwin(2), kwin(3)
    base["K_N2"], base["K_N3"] = k2, k3
    base["K_min"], base["K_max"] = np.minimum(k2, k3), np.maximum(k2, k3)
    base["K_central"] = (k2 + k3) / 2

    # ---------------- L · vivienda liberada por envejecimiento
    mort = lee_mortalidad()
    qk5 = mort.pivot(index="k", columns="e0", values="valor") / 1000.0   # riesgo de muerte en el tramo quinquenal
    qk = 1.0 - (1.0 - qk5.clip(upper=0.999)) ** 0.2                          # tasa anual equivalente
    qk[95] = qk[90]  # 95+ : riesgo del tramo = 1 (cierre de tabla); se usa la tasa anual de 90-94 (cota baja)
    jef = pd.read_csv(RAIZ / "output/v4/M2/tablas/tasas_jefatura_4grupos.csv")
    h65 = float(jef["65+"].iloc[-1])
    anio_h65 = int(jef.anio.iloc[-1])
    l_ann = {s: {} for s in ("min", "central", "max")}
    p75_26, det = {}, {}
    for c in cods:
        k = kcod[c]
        sub = pp[(pp.k == k) & (pp.e >= 75)]
        pv = sub.pivot(index="e", columns="anyo", values="valor")
        band = pv.index.map(lambda e: min(95, 75 + 5 * ((e - 75) // 5)))
        qb = np.array([qk.loc[k, b] for b in band])
        muertes = (pv.loc[:, Y0:Y1 - 1].mul(qb, axis=0)).sum()      # defunciones 75+ por año 2026..2035
        p75_26[c] = pv[Y0].sum()
        det[c] = muertes.mean()
        for s, hf, dd in zip(("min", "central", "max"), H_FACT, DISOL):
            l_ann[s][c] = h65 * hf * dd * muertes.mean()
    base["pob75_2026"] = pd.Series(p75_26)
    base["defunciones75_anual"] = pd.Series(det)
    for s in ("min", "central", "max"):
        base[f"L_anual_{s}"] = pd.Series(l_ann[s])
        base[f"L_{s}"] = 10 * base[f"L_anual_{s}"]

    # ---------------- D · desplazada, S · segunda residencia (aparte)
    sd = lee_saldos()
    base["D_saldo_interprov_personas_anual"] = [sd.loc[kcod[c], [2021, 2022, 2023, 2024]].mean() for c in cods]
    base["D_hogares_anual"] = base.D_saldo_interprov_personas_anual / base.tam_hogar_2026
    base["S_esporadicas_2021_stock"] = base.esporadicas_2021

    # ---------------- necesidad
    f = base
    for s_out, s_c, inv in (("min", "min", "max"), ("central", "central", "central"), ("max", "max", "min")):
        pass
    comp = lambda col, s: f[f"{col}_{s}"]  # noqa: E731
    f["N10_min"] = comp("A", "min") + comp("R", "min") + comp("V", "min") + comp("F", "min") - comp("M", "max") - comp("K", "max")
    f["N10_central"] = comp("A", "central") + comp("R", "central") + comp("V", "central") + comp("F", "central") - comp("M", "central") - comp("K", "central")
    f["N10_max"] = comp("A", "max") + comp("R", "max") + comp("V", "max") + comp("F", "max") - comp("M", "min") - comp("K", "min")
    for s in ("min", "central", "max"):
        f[f"N_anual_{s}"] = f[f"N10_{s}"] / 10
        f[f"atraso_anual_{s}"] = f[f"A_{s}"] / 10                         # atraso absorbido en 10 años
        f[f"crec_rep_anual_{s}"] = (f[f"F_{s}"] + f[f"R_{s}"]) / 10     # crecimiento + reposición
    f["N10_central_formula_literal_menos_L"] = f.N10_central - f.L_central
    f["capa_A"], f["capa_R"], f["capa_V"], f["capa_F"] = "C4", "C4", "C4", "C2"
    f["capa_M"], f["capa_K"], f["capa_L"] = "C4", "C4", "C4"
    f["capa_total"] = "C4"  # menor de los componentes (A, R, V, M, K, L en C4)

    # ---------------- registro
    for c in f.index:
        r = f.loc[c]
        for comp_, col in (("A", "A_central"), ("R", "R_central"), ("V", "V_central"), ("F", "F_central"),
                           ("M", "M_central"), ("K", "K_central"), ("L", "L_central"), ("N", "N10_central")):
            reg.log("B1", f"B1_{comp_}_{c}", f"componente {comp_} 2026-2035 (central; rango en tabla)", Y0, Y1 - 1, 1,
                    np.nan, np.nan, np.nan, np.nan, float(r[col]) if pd.notna(r[col]) else np.nan, np.nan,
                    f"{r.provincia}; capa {r.get('capa_' + comp_, 'C4')}; p ajustado no aplica (estimación, sin contraste)")
    for nombre, valor in (("F_alt_jefatura_constante", f.F_alt.sum()), ("R_censo", f.R_bajas_censo_1121.sum()),
                          ("R_catastro", f.R_bajas_catastro_1224.sum())):
        reg.log("B1", f"B1_nac_{nombre}", "suma provincial", Y0, Y1 - 1, len(f), np.nan, np.nan, np.nan, np.nan,
                float(valor), np.nan, "método alternativo")

    f.to_csv(OUT / "tablas" / "B1_provincias.csv", float_format="%.4f")
    if SMOKE:
        print(f[["provincia", "A_central", "R_central", "V_central", "F_central", "M_central", "K_central", "L_central",
                 "N10_central", "N_anual_central"]].round(0).to_string())
        return

    # ---------------- nacional, controles, tablas
    nac = {}
    for col in ("A1", "A2", "A", "R", "V", "F", "M", "K", "L", "N10"):
        nac[col] = {s: float(f[f"{col}_{s}"].sum()) for s in ("min", "central", "max")}
    nac["D_hogares_anual"] = float(f.D_hogares_anual.sum())
    nac["S_esporadicas_2021"] = float(f.esporadicas_2021.sum())
    nac["N10_formula_literal_menos_L"] = float(f.N10_central_formula_literal_menos_L.sum())
    nac["N10_solo_presion_central"] = float(f.loc[f.presion, "N10_central"].sum())
    nac["N10_solo_positivas_central"] = float(f.N10_central.clip(lower=0).sum())
    nac["L_en_presion_central"] = float(f.loc[f.presion, "L_central"].sum())
    nac["n_prov_presion"] = int(f.presion.sum())
    nac["n_prov_R_un_metodo"] = int((f.R_n_metodos < 2).sum())
    nac["n_prov_K_sin_dato"] = int(f.K_central.isna().sum())

    ccaa_ok = float(hnac[Y1] - hnac[Y0])
    control = [
        {"tabla": "hogares_proyectados_2026", "suma_provincial": float(f.hogares_2026.sum()), "nacional": float(hnac[Y0]),
         "tolerancia_rel": 0.001},
        {"tabla": "hogares_proyectados_2036", "suma_provincial": float(f.hogares_2036.sum()), "nacional": float(hnac[Y1]),
         "tolerancia_rel": 0.001},
        {"tabla": "F_variacion_hogares_2026_2036", "suma_provincial": float(f.F_ine.sum()), "nacional": ccaa_ok,
         "tolerancia_rel": 0.01},
        {"tabla": "poblacion_proyectada_2026", "suma_provincial": float(sum(pob.loc[kcod[c], Y0] for c in cods)),
         "nacional": float(pnac[Y0]), "tolerancia_rel": 0.001},
        {"tabla": "viviendas_totales_censo2021", "suma_provincial": float(f.viv_total_2021.sum()), "nacional": 26623708.0,
         "tolerancia_rel": 0.001},
        {"tabla": "vacias_censo2021_INE59531", "suma_provincial": float(f.vacias_2021.sum()), "nacional": 3828307.0,
         "tolerancia_rel": 0.001},
        {"tabla": "esporadicas_censo2021_INE59531", "suma_provincial": float(f.esporadicas_2021.sum()),
         "nacional": 2517628.0, "tolerancia_rel": 0.001},
        {"tabla": "latente_A2_central", "suma_provincial": float(f.A2_central.sum()), "nacional": nac["A2"]["central"],
         "tolerancia_rel": 0.001},
        {"tabla": "necesidad_10a_central", "suma_provincial": float(f.N10_central.sum()), "nacional": nac["N10"]["central"],
         "tolerancia_rel": 1e-9},
        {"tabla": "D_saldo_interprovincial_personas", "suma_provincial": float(f.D_saldo_interprov_personas_anual.sum()),
         "nacional": 0.0, "tolerancia_rel": 0.0, "nota": "suma interprovincial = 0 por construcción (tolerancia absoluta 1 persona)"},
    ]
    # tolerancias: fallo si no se cumple (salvo D, absoluta)
    for t in control:
        if t["tabla"].startswith("D_"):
            t["ok"] = abs(t["suma_provincial"]) < 1.0
        else:
            t["ok"] = abs(t["suma_provincial"] - t["nacional"]) <= t["tolerancia_rel"] * abs(t["nacional"]) + 1e-9
    (OUT / "control_sumas.json").write_text(json.dumps(control, ensure_ascii=False, indent=1))
    fallos = [t["tabla"] for t in control if not t["ok"]]
    print("control_sumas fallos:", fallos)

    # tablas derivadas
    cols = ["provincia", "presion", "clase_A4"] + [f"{x}_{s}" for x in ("A", "R", "V", "F", "M", "K", "L", "N10")
                                                   for s in ("min", "central", "max")] + \
           [f"N_anual_{s}" for s in ("min", "central", "max")] + \
           [f"atraso_anual_{s}" for s in ("min", "central", "max")] + [f"crec_rep_anual_{s}" for s in ("min", "central", "max")]
    f[cols].round(0).to_csv(OUT / "tablas" / "B1_tabla_provincial.csv")
    pd.DataFrame([{"componente": k, **(v if isinstance(v, dict) else {"central": v})} for k, v in nac.items()]).to_csv(
        OUT / "tablas" / "B1_nacional.csv", index=False, float_format="%.1f")
    f[["provincia", "viv_total_2021", "R_bajas_censo_1121", "R_bajas_catastro_1224", "R_tasa_censo", "R_tasa_catastro",
       "R_n_metodos", "R_tasa_min", "R_tasa_central", "R_tasa_max"]].to_csv(OUT / "tablas" / "B1_reposicion_metodos.csv",
                                                                           float_format="%.5f")
    f[["provincia", "pob75_2026", "defunciones75_anual", "L_anual_min", "L_anual_central", "L_anual_max", "presion"]].to_csv(
        OUT / "tablas" / "B1_envejecimiento.csv", float_format="%.1f")
    sol = pd.DataFrame([
        {"componente": "A1 déficit 2021-2025 (A4/M1)", "estado": "dato", "solapamiento": "base; hogares formados sin vivienda"},
        {"componente": "A2 emancipación retrasada (M1 latente, Eurostat/ECV o EPA)", "estado": "dato",
         "solapamiento": "no solapa con A1 (hogares NO formados); sí con A3 si hubiera datos"},
        {"componente": "A3 hogares compartidos/varios núcleos", "estado": "sin dato",
         "solapamiento": "Censo 2021 provincial por núcleos no accesible por Tempus; solaparía con A2"},
        {"componente": "A4 hacinamiento e infravivienda", "estado": "sin dato", "solapamiento": "solaparía con A3"},
        {"componente": "A5 pisos y habitaciones compartidas", "estado": "sin dato", "solapamiento": "solaparía con A2/A3"},
    ])
    sol.to_csv(OUT / "tablas" / "B1_atraso_solapamientos.csv", index=False)
    figura(f)
    escribe_json(f, nac, control, h65, anio_h65, fallos)


def figura(f: pd.DataFrame) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    cen = pd.read_csv(V5 / "municipio_centroides_utm30.csv", dtype={"codigo": str})
    cen["cod_prov"] = cen.codigo.str[:2]
    cen = cen[~cen.cod_prov.isin(["35", "38", "51", "52"])]  # Canarias y plazas africanas: fuera del mapa peninsular+Baleares
    xy = cen.groupby("cod_prov")[["x_m", "y_m"]].median()
    g = f.join(xy, how="inner")
    fig, ax = plt.subplots(1, 2, figsize=(13, 7), gridspec_kw={"width_ratios": [1.1, 1]})
    sizes = g.N_anual_central.clip(lower=0) / g.N_anual_central.max() * 1800
    col = np.where(g.presion, "#b2182b", "#4575b4")
    ax[0].scatter(g.x_m / 1e3, g.y_m / 1e3, s=sizes, c=col, alpha=0.6, edgecolor="k", linewidth=0.4)
    for c, r in g.iterrows():
        ax[0].annotate(c, (r.x_m / 1e3, r.y_m / 1e3), fontsize=6, ha="center", va="center")
    ax[0].set_aspect("equal")
    ax[0].set_title("Necesidad anual central 2026-2035 (viviendas/año)\nTamaño ∝ valor; rojo = presión (A4 clase 1-2); capa C4", fontsize=9)
    ax[0].set_xlabel("UTM30 x (km), mediana de centroides municipales")
    top = f.sort_values("N_anual_central", ascending=False).head(20)
    yy = range(len(top))[::-1]
    ax[1].barh(list(yy), top.N_anual_central, color="#4575b4")
    ax[1].errorbar(top.N_anual_central, list(yy), xerr=[top.N_anual_central - top.N_anual_min, top.N_anual_max - top.N_anual_central],
                   fmt="none", ecolor="k", lw=0.7)
    ax[1].set_yticks(list(yy))
    ax[1].set_yticklabels(top.provincia, fontsize=7)
    ax[1].set_title("20 mayores: central con rango mín-máx (viviendas/año)", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "figuras" / "B1_mapa_necesidad.png", dpi=110, metadata={"Software": None})
    plt.close(fig)


def escribe_json(f, nac, control, h65, anio_h65, fallos) -> None:
    N = nac["N10"]
    anual = {s: N[s] / 10 for s in N}
    fd = "2026-10-10 (descarga); INE proyecciones 2026-06; Censo 2021-11; MIVAU/Catastro hasta 2025"
    ficha_mayores = {
        "L_anual": {s: nac["L"][s] / 10 for s in nac["L"]},
        "frac_presion": nac["L_en_presion_central"] / nac["L"]["central"],
    }

    def H(i, ind, vals, ud, per, cob, fu, capa, fecha=fd):
        v = vals
        return {"id": i, "indicador": ind, "valor": round(v["central"], 1), "min": round(v["min"], 1),
                "max": round(v["max"], 1), "unidad": ud, "periodo": per, "cobertura": cob, "fuentes": fu, "capa": capa,
                "fecha_dato": fecha}
    per = "2026-2035"
    hechos = [
        H("B1-H1", "Necesidad total de vivienda por año (A+R+V+F-M-K), suma de 52 provincias", anual, "viviendas/año", per,
          "España (52 provincias)", ["A4/M1", "INE 54562", "Censo 2021", "MIVAU", "Catastro"], "C4"),
        H("B1-H2", "Atraso a absorber en 10 años (déficit 2021-2025 + emancipación retrasada)", nac["A"], "viviendas (stock)",
          "2021-2025 absorbido en 2026-2035", "España", ["A4", "M1", "M2"], "C4"),
        H("B1-H3", "Reposición del parque (10 años)", nac["R"], "viviendas", per, "España",
          ["Censo 2011/2021 + MIVAU", "Catastro + MIVAU"], "C4"),
        H("B1-H4", "Crecimiento de hogares proyectado (INE, 10 años)", nac["F"], "hogares", per, "España",
          ["INE Proyección de Hogares 54562", "INE Proyecciones de Población 36726"], "C2"),
        H("B1-H5", "Ajuste de vacancia friccional en zonas con presión", nac["V"], "viviendas", per, "España", ["Censo 2021"], "C4"),
        H("B1-H6", "Vacías movilizables en zonas con presión (10-30 %)", nac["M"], "viviendas", per, "España",
          ["INE 59531", "A4"], "C4"),
        H("B1-H7", "Cartera en construcción (iniciadas menos terminadas, 2-3 años)", nac["K"], "viviendas", "2023-2025", "España",
          ["MIVAU"], "C4"),
        H("B1-H8", "Viviendas liberadas por envejecimiento (tasa de disolución de hogares de 75+)", nac["L"], "viviendas (10 años)",
          per, "España", ["INE 36726", "INE 67235", "M2 jefatura"], "C4"),
    ]
    resultado = {
        "rama": "B1",
        "pregunta": "¿Cuántas viviendas al año, por provincia, hacen falta en 2026-2035 (stock-flujo por componentes)?",
        "capa": "C4",
        "datos": ["INE Proyección de Hogares 54562 (2026)", "INE Proyecciones de Población 36726", "INE tablas de mortalidad 67235",
                  "INE EM saldos 69764", "Censo 2021", "MIVAU terminadas/iniciadas", "Catastro", "A4/M1/M2/R1C"],
        "N": int(len(f)),
        "metodo": "Necesidad = A+R+V+F-M-K (L aparte, ya neta en F); rango min-central-max por componente; "
                  "capa del total = menor de sus componentes",
        "estimacion": {"necesidad_anual_viviendas": anual, "necesidad_10a": N,
                       "atraso_anual": {s: nac['A'][s] / 10 for s in nac['A']},
                       "crecimiento_mas_reposicion_anual": {s: (nac['F'][s] + nac['R'][s]) / 10 for s in nac['F']},
                       "componentes_10a": {k: nac[k] for k in ("A1", "A2", "A", "R", "V", "F", "M", "K", "L")}},
        "ic95": None,
        "p_ajustado": None,
        "nivel_evidencia": "EXPLORATORIO (C4: componentes de fuente única o con supuestos no contrastados)",
        "diagnosticos": {"control_sumas_fallos": fallos, "n_prov_presion": nac["n_prov_presion"],
                         "n_prov_R_un_metodo": nac["n_prov_R_un_metodo"],
                         "n_prov_K_sin_dato": nac["n_prov_K_sin_dato"],
                         "R_prov_con_ambas_tasas_no_positivas": int(((f.R_tasa_censo.fillna(-1) <= 0) & (f.R_tasa_catastro.fillna(-1) <= 0)).sum()),
                         "R_tasa_censo_mediana": float(f.R_tasa_censo.median()),
                         "R_tasa_catastro_mediana": float(f.R_tasa_catastro.median()),
                         "necesidad_formula_literal_menos_L_10a": nac["N10_formula_literal_menos_L"],
                         "necesidad_solo_provincias_con_presion_10a": nac["N10_solo_presion_central"],
                         "necesidad_solo_provincias_positivas_10a": nac["N10_solo_positivas_central"]},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": [
            "No es un modelo predictivo: es una contabilidad con rangos; AR(4) y ECM v1 no aplican (fuera_muestra null).",
            "Holm/BH no aplica: no hay contrastes de hipótesis; todas las especificaciones están en registro.csv.",
            "F (INE) ya es neta de disoluciones de hogares; restar L además duplicaría. Se da la fórmula literal como variante.",
            "A3-A5 (hogares compartidos, hacinamiento, habitaciones compartidas) SIN DATO provincial accesible; rango sin ellos.",
            "R: 2 métodos (Censo 2011-2021 + MIVAU; Catastro + MIVAU); tasas negativas se acotan a 0; forales sin Catastro (1 método).",
            "R (resultado negativo): en la mayoría de provincias el stock crece más que las terminadas (tasas brutas de baja negativas); "
            "los métodos no detectan bajas netas y el rango inferior se acota a 0; R es un límite inferior no informativo, no una medición.",
            "V: base = viviendas en alquiler Censo 2021 (venta sin dato); disponible sin dato: mínimo 0, central 2 %, máximo 4 %.",
            "L: tasa de jefatura 75+ no disponible; se usa la de 65+ de M2 (%.3f, %d) con factor 0,85-1,15; traslados a residencias SIN DATO." % (h65, anio_h65),
            "Min y máx combinan los extremos de todos los componentes a la vez: son cotas, no intervalos de confianza.",
            "D y S van aparte: D = saldo interprovincial EM 2021-2024 (suma 0); S = esporádicas Censo 2021 (stock).",
        ],
    }
    (OUT / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1, default=float))
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1, default=float))
    fichas = [
        {
            "id": "B1-V1", "tema": "Necesidad de vivienda",
            "enunciado": "Hacen falta X viviendas al año en España.",
            "capa": "C4",
            "magnitud": ("Contabilidad stock-flujo 2026-2035 (suma de 52 provincias): %.0f viviendas/año central, rango %.0f a %.0f "
                         "(cotas con todos los componentes en su extremo). De ellas, atraso a absorber en 10 años: %.0f/año; "
                         "crecimiento de hogares más reposición: %.0f/año. D y S aparte." %
                         (anual["central"], anual["min"], anual["max"], nac["A"]["central"] / 10,
                          (nac["F"]["central"] + nac["R"]["central"]) / 10)),
            "intervalo": "%.0f a %.0f viviendas/año (C4)" % (anual["min"], anual["max"]),
            "cota": "—", "literatura": "Gabriel y Nothaft (2001), J. Urban Econ., DOI 10.1006/juec.2000.2187: VERIFICADA (DOI en Crossref; JUE, Q1 según docs/literatura.md); sustenta la existencia de una vacancia friccional, no el rango 2-4 % (supuesto del encargo).",
            "veredicto": "ANALIZADA, NO CONCLUYENTE",
            "regla": "Capa del total = menor de sus componentes: A, R, V, M, K y L en C4 (hogares provinciales de fuente única, supuestos no contrastados); solo F (INE, dos métodos) en C2. Con C4 el máximo es ANALIZADA, NO CONCLUYENTE. El valor depende del atraso y de las vacías movilizables, que son los componentes más inciertos.",
            "limites": "Sin dato de hogares compartidos, hacinamiento ni residencias; vacancia disponible sin dato; K aproxima la cartera con iniciadas menos terminadas; los rangos no son IC.",
            "evidencia": ["output/v5/B1/tablas/B1_tabla_provincial.csv", "output/v5/B1/resultado.json"],
        },
        {
            "id": "B1-V2", "tema": "Envejecimiento",
            "enunciado": "La vivienda que dejan los mayores resolverá el problema de la vivienda.",
            "capa": "C4",
            "magnitud": ("Viviendas liberadas por disolución de hogares de 75+ en 2026-2035: %.0f/año central (rango %.0f-%.0f); "
                         "equivalen al %.0f%% de la necesidad anual central; %.0f%% de ellas en provincias con presión (A4 clase 1-2). "
                         "Ya están descontadas en el crecimiento neto de hogares del INE, así que no suman a la oferta adicional." %
                         (ficha_mayores["L_anual"]["central"], ficha_mayores["L_anual"]["min"], ficha_mayores["L_anual"]["max"],
                          100 * ficha_mayores["L_anual"]["central"] / anual["central"], 100 * ficha_mayores["frac_presion"])),
            "intervalo": "%.0f a %.0f viviendas/año (C4)" % (ficha_mayores["L_anual"]["min"], ficha_mayores["L_anual"]["max"]),
            "cota": "—", "literatura": "—",
            "veredicto": "ANALIZADA, NO CONCLUYENTE",
            "regla": "L es C4 (tasa de jefatura 75+ sin dato propio, traslados a residencias sin dato, destino de la vivienda liberada -venta, alquiler, herencia, uso esporádico- sin dato). Los hechos acotan el orden de magnitud, no el veredicto.",
            "limites": "Sin Censo 2021 por edad del jefe; mortalidad de 2024 constante (sesgo al alza de la liberación).",
            "evidencia": ["output/v5/B1/tablas/B1_envejecimiento.csv"],
        },
    ]
    (OUT / "fichas_verificador.json").write_text(json.dumps(fichas, ensure_ascii=False, indent=1, default=float))
    (OUT / "metodo.md").write_text(
        "# B1 · método\n\nNecesidad = A + R + V + F − M − K (− L solo en la variante literal), 2026-2035, en viviendas.\n"
        "Rango: mínimo = componentes que suman en su mínimo y los que restan en su máximo; máximo al revés.\n"
        "Capa: menor de los componentes. Fechas de datos: " + "; ".join(FECHA.values()) + ".\n")


if __name__ == "__main__":
    main()

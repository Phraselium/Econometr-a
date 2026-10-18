"""Replica ciega lote b (V16): deficit 2021-2024 (SENS, SINBAJAS) y E-B1-F. SEED=20261010."""
import gzip
import json
import re
import unicodedata
import numpy as np
import pandas as pd

SEED = 20261010
RAW = "/home/user/Econometr-a/data/raw/"


def _clave(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    s = re.split(r"[/,]", s)[0]
    return re.sub(r"[^a-z]", "", s)


def hogares_series():
    ecp = pd.read_csv(RAW + "ine_hogares_60131.csv")
    ecp = ecp[ecp.nombre == "Total Nacional. Total. Hogares en viviendas familiares. Número."].set_index("periodo").valor
    epa = pd.read_csv(RAW + "ine_epa_hogares.csv")
    epa = epa[epa.nombre == "Hogares. Total Nacional. Ambos sexos. Total. Total."].set_index("periodo").valor * 1000
    return ecp, epa


def _prev(p, k=1):
    y, q = int(p[:4]), int(p[5])
    n = y * 4 + (q - 1) - k
    return f"{n // 4}T{n % 4 + 1}"


def variantes_hogares():
    ecp, epa = hogares_series()
    d = lambda t: epa[t] - epa[_prev(t)]
    base = epa["2024T4"] - epa["2020T4"]
    salto = epa["2021T1"] - epa["2020T4"]
    v = {}
    v["v1"] = base + 242400
    v["a"] = base
    v["b"] = base - salto + np.mean([d("2020T4"), d("2021T2")])
    v["b4"] = base - salto + np.mean([d("2020T3"), d("2020T4"), d("2021T2"), d("2021T3")])
    v["c"] = base - salto
    v["d1"] = ecp["2025T1"] - epa["2020T4"] * (ecp["2021T1"] / epa["2021T1"])
    v["d2"] = ecp["2025T1"] - (ecp["2021T1"] - np.mean([d(f"2020T{i}") for i in (1, 2, 3, 4)]))
    v["e"] = ecp["2025T1"] - ecp["2021T1"]
    return v


def _suma(df, serie, anios):
    s = df[df.serie == serie]
    return float(s[s.periodo.astype(str).str[:4].astype(int).isin(anios)].valor.sum())


def terminadas():
    lib = pd.read_csv(RAW + "mivau_v2_iniciadas_terminadas_prov.csv")
    pro = pd.read_csv(RAW + "mivau_v2_protegida.csv")
    A = range(2021, 2025)
    l_nac = _suma(lib, "viv_libres_terminadas_anual_nacional", A)
    p_nac = _suma(pro, "prot_definitiva_anual_nacional", A)
    sl = [s for s in lib.serie.unique() if s.startswith("viv_libres_terminadas_anual_ccaa_") and ("pais_vasco" in s or "navarra" in s)]
    sp = [s for s in pro.serie.unique() if s.startswith("prot_definitiva_anual_ccaa_") and ("pais_vasco" in s or "navarra" in s)]
    pvna = sum(_suma(lib, s, A) for s in sl) + sum(_suma(pro, s, A) for s in sp)
    cat = pd.read_csv(RAW + "catastro_urbana_municipios.csv.gz")
    cat = cat[cat.unidad == "unidades_urbanas_residenciales"]
    uu = cat.groupby("periodo").valor.sum()
    altas = float(uu[2025] - uu[2021])
    return {"mivau_con_prot": l_nac + p_nac, "mivau_sin_prot": l_nac, "catastro": altas + pvna,
            "_pvna": pvna, "_altas": altas}


def deficit_tabla():
    h = variantes_hogares()
    t = terminadas()
    filas = []
    for kh, vh in h.items():
        if kh == "v1":
            continue  # las 8 variantes del anexo son a,b,b4,c,d1,d2,e + v1: ver nota
        for kt in ("mivau_con_prot", "mivau_sin_prot", "catastro"):
            filas.append((kh, kt, vh - t[kt]))
    return h, t, pd.DataFrame(filas, columns=["h", "t", "def"])


def _h8():
    h = variantes_hogares()
    return h


def _resumen(excluir=()):
    h = variantes_hogares()
    t = terminadas()
    vals = [(kh, kt, vh - t[kt]) for kh, vh in h.items() if kh not in excluir
            for kt in ("mivau_con_prot", "mivau_sin_prot", "catastro")]
    d = np.array([x[2] for x in vals])
    return {"valor": float((d.min() + d.max()) / 2), "min": float(d.min()), "max": float(d.max()), "n": len(d)}


def l3_def_sinbajas():
    return _resumen()


def l3_def_sens():
    r = _resumen(excluir=("a", "d1"))
    r["valor"] = float((r["min"] + r["max"]) / 2)
    return r


def e_b1_f():
    h = pd.read_csv(RAW + "v5/ine_b1_t54562_proy_hogares.csv")
    h = h[h.nombre.str.endswith(". Total. ") & (h.nombre != "Total Nacional. Total. ")].copy()
    h["k"] = h.nombre.str.replace(". Total. ", "", regex=False).map(_clave)
    H = h.drop_duplicates(["k", "anyo"]).set_index(["k", "anyo"]).valor
    p = pd.read_csv(RAW + "v5/ine_b1_t36726_proy_poblacion_prov.csv")
    p = p[p.nombre.str.endswith("Proyección a corto plazo. Todas las edades. ")].copy()
    p["t"] = p.nombre.str.extract(r"^Total\. Población\. (.*)\. Proyección")[0]
    terr = [x for x in p.t.unique() if x != "Total Nacional"]
    p["k"] = p.t.map(_clave)
    P = p.drop_duplicates(["k", "anyo"]).set_index(["k", "anyo"]).valor
    # provincias = territorios de la tabla 36726 que no son CCAA pluriprovinciales con nombre propio
    ks = sorted({_clave(x) for x in terr})  # las 52 provincias de la tabla 36726 (sin Total Nacional)
    rows = []
    for k in ks:
        if (k, 2026) not in H.index:
            continue
        fi = H[(k, 2036)] - H[(k, 2026)]
        fa = H[(k, 2026)] * (P[(k, 2036)] / P[(k, 2026)] - 1)
        rows.append((k, fi, fa))
    df = pd.DataFrame(rows, columns=["k", "fi", "fa"])
    return {"valor": float(df.fi.sum()), "min": float(np.minimum(df.fi, df.fa).sum()),
            "max": float(np.maximum(df.fi, df.fa).sum()), "n_prov": len(df)}


def v10_atl_a1():
    """Sobrecarga >40 % (coste de vivienda neto de ayudas / renta neta de ayudas), personas en alquiler de mercado, ECV 2025."""
    import io
    import zipfile
    z = zipfile.ZipFile(RAW + "v9/ine_microdatos/ecv/datos_2025.zip")

    def lee(interno, csv, **kw):
        zi = zipfile.ZipFile(io.BytesIO(z.read(interno)))
        return pd.read_csv(zi.open(csv), **kw)

    h = lee("ECV_Th_2025.zip", "CSV/esudb25h.csv", usecols=["HB030", "HY020", "HY070N", "HH021", "HH070"])
    r = lee("ECV_Tr_2025.zip", "CSV/esudb25r.csv", usecols=["RB030", "RB050"])
    h["HH070"] = pd.to_numeric(h.HH070, errors="coerce")
    r["hid"] = r.RB030 // 100
    x = r.merge(h, left_on="hid", right_on="HB030")
    x = x[(x.HH021 == 3) & x.HH070.notna()].copy()
    x["y"] = (((x.HH070 * 12 - x.HY070N) / (x.HY020 - x.HY070N)) > 0.4).astype(float)
    W = x.RB050.sum()
    p = (x.RB050 * x.y).sum() / W
    # linealizacion con el hogar como conglomerado
    x["u"] = x.RB050 * (x.y - p)
    tot = x.groupby("hid").u.sum()
    n = len(tot)
    var = n / (n - 1) * (tot ** 2).sum() / W ** 2
    se = var ** 0.5
    return {"valor": float(100 * p), "min": float(100 * (p - 1.96 * se)), "max": float(100 * (p + 1.96 * se)),
            "n_personas": int(len(x)), "n_hogares": int(n)}


NO_REPRODUCIBLE = {
    "T3-H5b": "La ficha da la formula (A+R+V+F-M-K)/10 y la tabla de componentes de v5, pero A (deficit A4 por provincia y latente M1), "
              "R con las bajas estimadas de T1, V y M (clases A4 1-2) y K no se definen con datos de data/raw: remiten a tablas intermedias "
              "(B1_provincias.csv, A4/clasificacion_provincias.csv, T1/tablas). Solo F se reconstruye (ver E-B1-F).",
    "T4-H2": "Rejilla B2 x T1 x T2 (180 escenarios) sin especificacion en la ficha: faltan escenarios de terminadas por provincia, "
             "hogares bajos, bajas, liberadas y la definicion del deficit provincial de partida 2025.",
    "T4-H3": "Misma rejilla; ademas falta la regla de clasificacion empeora/mejora/indeterminada por provincia.",
}


def main():
    pub = {
        "L3-DEF-2124-SENS": (l3_def_sens, "valor"),
    }
    out = []
    ids = [("L3-DEF-2124-SENS", l3_def_sens), ("L3-DEF-2124-SINBAJAS", l3_def_sinbajas), ("E-B1-F", e_b1_f), ("V10-ATL-A1", v10_atl_a1)]
    for i, fn in ids:
        r = fn()
        out.append({"id": i, "replica": {k: r[k] for k in ("valor", "min", "max")}, "extra": r})
    for i, msg in NO_REPRODUCIBLE.items():
        out.append({"id": i, "replica": None, "veredicto": "NO REPRODUCIBLE DESDE LA FICHA", "diagnostico": msg})
    return out


if __name__ == "__main__":
    res = main()
    print(json.dumps(res, indent=1, default=float))
    json.dump(res, open("/home/user/Econometr-a/output/v16/replica/v10_b/_replica_sin_comparar.json", "w"), indent=1, default=float)

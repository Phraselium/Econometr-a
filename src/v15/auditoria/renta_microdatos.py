"""V15 fase 1.2 · Auditoría de datos, grupo RENTA Y MICRODATOS (capa C4, descriptivo, sin efectos estimados).

Fuentes: AEAT IRPF por municipios (crudo data/raw/v11/aeat_irpf_municipios y variables aeat_irpf_* de la base, Comunitat
Valenciana), INE ADRH por sección (base, 2019-2023; crudo data/raw/v3 para 2021), microdatos ECV 2018-2025 (leídos como en
src/v12/b6_condiciones.py), EPA (solo inventario), ECEPOV 2021 y muestra del 10 % del Censo 2021 (c21md_*, clase b: solo
estadísticos agregados con n >= 10; nunca celdas pequeñas ni microdatos).
Base con duckdb filtrando NOT coalesce(muestra_sellada_v6,false). No se accede a la muestra reservada. Sin red, solo lectura.
Cruces territoriales por código INE (sección -> municipio = 5 primeros dígitos del código de sección).
Determinista (SEED=20261010). Salida: output/v15/auditoria/renta_microdatos/.
Uso: python3 src/v15/auditoria/renta_microdatos.py   (la lectura de la ECV tarda unos minutos; V15_ECV_CACHE=ruta.pkl
permite reutilizar el DataFrame ya preparado durante el desarrollo, sin cambiar el resultado).
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import re
import zipfile
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

SEED = 20261010
np.random.seed(SEED)
RAIZ = Path(__file__).resolve().parents[3]
RAW = RAIZ / "data" / "raw"
HECHOS = RAIZ / "data" / "base" / "hechos.parquet"
OUT = RAIZ / "output" / "v15" / "auditoria" / "renta_microdatos"
UMBRAL_Z = 5.0
MIN_N_CELDA = 10      # clase b del Censo y supresión general
N_P8 = 200            # umbral de la pregunta P8
PROV_CV = ("03", "12", "46")
FILTRO = "NOT coalesce(muestra_sellada_v6,false)"

# ---------------------------------------------------------------- utilidades


def con_base() -> duckdb.DuckDBPyConnection:
    return duckdb.connect()


def base(con, variable: str, nivel: str | None = None) -> pd.DataFrame:
    q_ = f"select territorio_codigo c, periodo p, valor v from '{HECHOS}' where variable='{variable}' and {FILTRO}"
    if nivel:
        q_ += f" and nivel='{nivel}'"
    return con.sql(q_).df()


def zrob(x: pd.Series, min_n: int = 30) -> pd.Series | None:
    x = x.dropna().astype(float)
    if len(x) < min_n:
        return None
    med = float(np.median(x))
    mad = float(np.median(np.abs(x - med)))
    if mad == 0:
        return None
    return (x - med) / (1.4826 * mad)


def q(x, p) -> float:
    x = pd.Series(x).dropna()
    return round(float(np.quantile(x, p)), 4) if len(x) else np.nan


def spearman(a: pd.Series, b: pd.Series) -> float:
    j = pd.concat([a, b], axis=1).dropna()
    if len(j) < 10:
        return np.nan
    return float(j.rank().iloc[:, 0].corr(j.rank().iloc[:, 1]))


def pearson(a: pd.Series, b: pd.Series) -> float:
    j = pd.concat([a, b], axis=1).dropna()
    if len(j) < 10 or j.iloc[:, 0].std() == 0 or j.iloc[:, 1].std() == 0:
        return np.nan
    return float(j.iloc[:, 0].corr(j.iloc[:, 1]))


def sup(n: float) -> float:
    """Supresión de recuentos < MIN_N_CELDA."""
    return float(n) if n >= MIN_N_CELDA else np.nan


# ---------------------------------------------------------------- 1. AEAT 2013-2015 (unidades)

PARES_CONCEPTO = {
    "trabajo": ("RENDIMIENTOS DEL TRABAJO (neto reducido)", "RENTAS DEL TRABAJO"),
    "capital_mobiliario": ("RENDIMIENTOS DEL CAPITAL MOBILIARIO", "RENTAS DEL CAPITAL MOBILIARIO"),
    "inmuebles_no_afectos": ("RENDIMIENTOS DERIVADOS DE BIENES INMUEBLES NO AFECTOS A ACTIV. ECONÓMICAS",
                             "RENTAS DE BIENES INMUEBLES NO AFECTOS A ACTIV. ECONÓMICAS"),
    "actividades_economicas": ("RENDIMIENTOS DE ACTIVIDADES ECONÓMICAS", "RENTAS DE ACTIVIDADES ECONÓMICAS"),
    "ganancias_patrimoniales": ("GANANCIAS Y PÉRDIDAS PATRIMONIALES", "GANANCIAS PATRIMONIALES NETAS"),
    "cuota_autoliquidacion": ("CUOTA RESULTANTE DE LA AUTOLIQUIDACIÓN", "CUOTA RESULTANTE DE LA AUTOLIQUIDACIÓN"),
}


def cargar_aeat() -> pd.DataFrame:
    d = pd.read_csv(RAW / "v11" / "aeat_irpf_municipios" / "irpf_municipios_cv.csv.gz", dtype={"cod_municipio": str})
    d["cod_municipio"] = d.cod_municipio.str.zfill(5)
    # nombres repetidos dentro de un municipio y año (p. ej. «Ingresos íntegros»): se numeran por orden
    d["orden"] = d.groupby(["ejercicio", "cod_municipio", "variable"]).cumcount()
    return d


def tarea1_aeat(d: pd.DataFrame):
    cl = ["NÚMERO DE DECLARACIONES", "RENTA BRUTA MEDIA", "RENTA DISPONIBLE MEDIA"]
    est = []
    for a, g in d.groupby("ejercicio"):
        por_mun = g.groupby("cod_municipio").size()
        est.append({"ejercicio": int(a), "municipios": int(g.cod_municipio.nunique()), "filas": int(len(g)),
                    "conceptos_distintos": int(g.variable.nunique()), "filas_por_municipio_mediana": float(por_mun.median()),
                    "tiene_NUM_DECLARACIONES": bool(cl[0] in set(g.variable)), "tiene_RENTA_BRUTA_MEDIA": bool(cl[1] in set(g.variable)),
                    "tiene_RENTA_DISPONIBLE_MEDIA": bool(cl[2] in set(g.variable)),
                    "valencia_46250_presente": bool((g.cod_municipio == "46250").any()),
                    "pct_valores_nulos": round(float(g.valor.isna().mean() * 100), 1),
                    "valor_mediano_global": round(float(g.valor.median()), 1)})
    EST = pd.DataFrame(est)

    def val(a: int, nombre: str) -> pd.Series:
        g = d[(d.ejercicio == a) & (d.variable == nombre) & (d.orden == 0)]
        return g.set_index("cod_municipio").valor

    filas = []
    for k, (n15, n16) in PARES_CONCEPTO.items():
        for a0, a1 in ((2013, 2014), (2014, 2015), (2015, 2016), (2016, 2017), (2017, 2018)):
            x = val(a0, n15 if a0 <= 2015 else n16)
            y = val(a1, n15 if a1 <= 2015 else n16)
            r = (x / y).replace([np.inf, -np.inf], np.nan).dropna()
            r = r[r > 0]
            filas.append({"concepto": k, "par": f"{a0}/{a1}", "n_municipios": int(len(r)), "razon_p10": q(r, .1), "razon_mediana": q(r, .5),
                          "razon_p90": q(r, .9), "log10_mediana": round(float(np.log10(r.median())), 3) if len(r) else np.nan,
                          "pct_razon_entre_0.5_y_2": round(float(((r >= .5) & (r <= 2)).mean() * 100), 1) if len(r) else np.nan})
    RZ = pd.DataFrame(filas)
    ndecl16 = val(2016, "NÚMERO DE DECLARACIONES")
    hip = []
    for k, (n15, n16) in PARES_CONCEPTO.items():
        v15 = val(2015, n15)
        imp16 = val(2016, n16)
        cuenta_ = (v15 / ndecl16).replace([np.inf, -np.inf], np.nan).dropna()
        hip.append({"concepto": k, "razon_2015_sobre_importe_2016_mediana": float(f"{(v15 / imp16).replace([np.inf, -np.inf], np.nan).median():.3e}"),
                    "razon_2015_sobre_n_declaraciones_2016_mediana": q(cuenta_, .5), "razon_2015_sobre_n_declaraciones_2016_p10": q(cuenta_, .1),
                    "razon_2015_sobre_n_declaraciones_2016_p90": q(cuenta_, .9),
                    "pct_municipios_2015_menor_igual_1.2_n_declaraciones_2016": round(float((cuenta_ <= 1.2).mean() * 100), 1),
                    "n_municipios": int(len(cuenta_))})
    HIP = pd.DataFrame(hip)
    chk = []
    for a in range(2016, 2025):
        rb, nd, med = val(a, "RENTA BRUTA"), val(a, "NÚMERO DE DECLARACIONES"), val(a, "RENTA BRUTA MEDIA")
        rr = (rb / nd / med).replace([np.inf, -np.inf], np.nan).dropna()
        chk.append({"ejercicio": a, "n": int(len(rr)), "razon_importe_sobre_n_sobre_media_p05": q(rr, .05), "mediana": q(rr, .5),
                    "p95": q(rr, .95), "renta_bruta_media_mediana_eur": q(med, .5)})
    CHK = pd.DataFrame(chk)
    v15n = set(d[(d.ejercicio == 2015) & (d.orden == 0)].variable)
    v16n = set(d[(d.ejercicio == 2016) & (d.orden == 0)].variable)
    m15, m16 = set(d[d.ejercicio == 2015].cod_municipio), set(d[d.ejercicio == 2016].cod_municipio)
    ex = {"conceptos_2015": len(v15n), "conceptos_2016": len(v16n), "conceptos_nombre_identico": sorted(v15n & v16n),
          "municipios_solo_2015": sorted(m15 - m16), "municipios_solo_2016": sorted(m16 - m15)}
    return EST, RZ, HIP, {"chk": CHK, "ex": ex}


# ---------------------------------------------------------------- 2. atípicos (MAD)


def atipicos_aeat(con):
    filas, top, rangos = [], [], {}
    for var in ("aeat_irpf_renta_bruta_media", "aeat_irpf_renta_disponible_media", "aeat_irpf_declaraciones", "aeat_irpf_rentas_inmuebles_media"):
        b = base(con, var, "municipio")
        b["p"] = b.p.astype(int)
        rangos[var] = {"min": round(float(b.v.min()), 1), "max": round(float(b.v.max()), 1), "n": int(len(b)),
                       "pct_nulos_o_cero": round(float((b.v.fillna(0) <= 0).mean() * 100), 2)}
        W = b.pivot_table(index="c", columns="p", values="v")
        L = np.log(W.where(W > 0))
        for a in L.columns:
            z = zrob(L[a])
            if z is None:
                continue
            g = z[z.abs() > UMBRAL_Z]
            filas.append({"variable": var, "tipo": "nivel_log_corte_transversal", "periodo": str(a), "n": int(len(z)), "n_atip": int(len(g))})
            for c, zz in g.items():
                top.append({"variable": var, "tipo": "nivel", "cod_ine": c, "periodo": str(a), "z_robusto": round(float(zz), 2)})
        D = L.diff(axis=1)
        for a in D.columns[1:]:
            z = zrob(D[a])
            if z is None:
                continue
            g = z[z.abs() > UMBRAL_Z]
            filas.append({"variable": var, "tipo": "variacion_interanual_log", "periodo": str(a), "n": int(len(z)), "n_atip": int(len(g))})
            for c, zz in g.items():
                top.append({"variable": var, "tipo": "variacion", "cod_ine": c, "periodo": str(a), "z_robusto": round(float(zz), 2)})
        nser = natip = 0
        for c, s in D.iterrows():
            z = zrob(s, min_n=6)
            if z is None:
                continue
            nser += 1
            natip += int((z.abs() > UMBRAL_Z).sum())
        filas.append({"variable": var, "tipo": "serie_municipal_variaciones", "periodo": "2016-2024", "n": nser, "n_atip": natip})
    bm = base(con, "aeat_irpf_renta_bruta_media", "municipio").merge(base(con, "aeat_irpf_renta_disponible_media", "municipio"), on=["c", "p"])
    rr = bm.v_y / bm.v_x
    rangos["disponible_sobre_bruta"] = {"min": q(rr, 0), "p01": q(rr, .01), "mediana": q(rr, .5), "p99": q(rr, .99), "max": q(rr, 1),
                                        "n_disponible_mayor_bruta": int((rr > 1).sum())}
    return pd.DataFrame(filas), pd.DataFrame(top), rangos


def cargar_adrh(con) -> dict:
    out = {}
    for v in ("adrh_renta_neta_persona", "adrh_renta_neta_hogar", "adrh_gini"):
        b = base(con, v, "seccion")
        out[v] = b.pivot_table(index="c", columns="p", values="v")
        out[v].columns = [int(c) for c in out[v].columns]
    return out


def atipicos_adrh(A: dict):
    filas, top, rangos = [], [], {}
    for var, W in A.items():
        v = W.stack()
        rangos[var] = {"min": round(float(v.min()), 2), "max": round(float(v.max()), 2), "n": int(len(v))}
        L = np.log(W.where(W > 0))
        for a in L.columns:
            z = zrob(L[a])
            g = z[z.abs() > UMBRAL_Z] if z is not None else pd.Series(dtype=float)
            filas.append({"variable": var, "tipo": "nivel_log_corte_transversal", "periodo": str(a), "n": int(L[a].notna().sum()), "n_atip": int(len(g))})
            for c, zz in g.items():
                top.append({"variable": var, "tipo": "nivel", "cod_ine": c, "periodo": str(a), "z_robusto": round(float(zz), 2)})
        cols = list(L.columns)
        for a0, a1 in zip(cols[:-1], cols[1:], strict=True):
            dl = L[a1] - L[a0]
            z = zrob(dl)
            g = z[z.abs() > UMBRAL_Z] if z is not None else pd.Series(dtype=float)
            filas.append({"variable": var, "tipo": "variacion_log_corte_transversal", "periodo": f"{a0}->{a1}", "n": int(dl.notna().sum()), "n_atip": int(len(g))})
            for c, zz in g.items():
                top.append({"variable": var, "tipo": "variacion", "cod_ine": c, "periodo": f"{a0}->{a1}", "z_robusto": round(float(zz), 2)})
    tam = (A["adrh_renta_neta_hogar"] / A["adrh_renta_neta_persona"]).stack()
    rangos["hogar_sobre_persona"] = {"min": q(tam, 0), "p01": q(tam, .01), "mediana": q(tam, .5), "p99": q(tam, .99), "max": q(tam, 1),
                                     "n_fuera_1_a_6": int(((tam < 1) | (tam > 6)).sum())}
    g_ = A["adrh_gini"].stack()
    rangos["gini_fuera_0_100"] = int(((g_ < 0) | (g_ > 100)).sum())
    return pd.DataFrame(filas), pd.DataFrame(top), rangos


# ---------------------------------------------------------------- 3. coherencia AEAT-ADRH


def a_municipio(W: pd.DataFrame) -> pd.DataFrame:
    """Sección -> municipio por código INE (5 primeros dígitos); media simple de secciones (sin pesos de población)."""
    m = W.copy()
    m["mun"] = [c[:5] for c in m.index]
    return m[m.mun.str[:2].isin(PROV_CV)].groupby("mun").mean()


def adrh_2021_crudo():
    raw = pd.read_csv(RAW / "v3" / "ine_v3_gis_seccion.csv.gz", dtype=str)
    r = raw[(raw.servicio == "Renta_media_por_hogar") & (raw.campo.isin(["dato1", "dato2"]))].copy()
    r["valor"] = pd.to_numeric(r.valor, errors="coerce")
    return (r[r.campo == "dato1"].set_index("codigo").valor, r[r.campo == "dato2"].set_index("codigo").valor)


def tarea3_coherencia(con, A: dict):
    def piv(v):
        return base(con, v, "municipio").assign(p=lambda x: x.p.astype(int)).pivot_table(index="c", columns="p", values="v")

    bruta, disp = piv("aeat_irpf_renta_bruta_media"), piv("aeat_irpf_renta_disponible_media")
    pers = a_municipio(A["adrh_renta_neta_persona"])
    hog = a_municipio(A["adrh_renta_neta_hogar"])
    p21, h21 = adrh_2021_crudo()
    pers[2021] = a_municipio(p21.rename(2021).to_frame())[2021]
    hog[2021] = a_municipio(h21.rename(2021).to_frame())[2021]
    niveles = []
    for a in (2019, 2020, 2021, 2022, 2023):
        for nombre, adrh in (("persona", pers), ("hogar", hog)):
            for nb, aeat in (("bruta", bruta), ("disponible", disp)):
                if a not in adrh.columns or a not in aeat.columns:
                    continue
                x, y = np.log(aeat[a]), np.log(adrh[a])
                j = pd.concat([x, y], axis=1).dropna()
                ratio = (aeat[a] / adrh[a]).dropna()
                niveles.append({"anio": a, "AEAT": f"renta_{nb}_media", "ADRH": f"neta_{nombre}", "n_municipios": int(len(j)),
                                "pearson_log": round(pearson(x, y), 3), "spearman": round(spearman(x, y), 3),
                                "razon_AEAT_sobre_ADRH_mediana": q(ratio, .5), "razon_p10": q(ratio, .1), "razon_p90": q(ratio, .9),
                                "nota": "2021 ADRH solo en crudo (campo etiquetado por orden, supuesto)" if a == 2021 else ""})
    NV = pd.DataFrame(niveles)
    tasas = []
    for a0, a1 in [(2019, 2020), (2020, 2021), (2021, 2022), (2022, 2023), (2020, 2022)]:
        for nombre, adrh in (("persona", pers), ("hogar", hog)):
            for nb, aeat in (("bruta", bruta), ("disponible", disp)):
                dx = np.log(aeat[a1]) - np.log(aeat[a0])
                dy = np.log(adrh[a1]) - np.log(adrh[a0])
                j = pd.concat([dx, dy], axis=1).dropna()
                fila = {"periodo": f"{a0}->{a1}", "AEAT": f"renta_{nb}_media", "ADRH": f"neta_{nombre}", "n_municipios": int(len(j)),
                        "pearson_tasas": round(pearson(dx, dy), 3), "spearman_tasas": round(spearman(dx, dy), 3),
                        "dif_media_pp_AEAT_menos_ADRH": round(float((j.iloc[:, 0] - j.iloc[:, 1]).mean() * 100), 2),
                        "tasa_media_AEAT_pp": round(float(dx.mean() * 100), 2), "tasa_media_ADRH_pp": round(float(dy.mean() * 100), 2)}
                if (a1 - a0) == 1 and (a0 - 1) in aeat.columns:
                    dxl = np.log(aeat[a1 - 1]) - np.log(aeat[a0 - 1])
                    fila["pearson_tasas_AEAT_desfase_-1"] = round(pearson(dxl, dy), 3)
                tasas.append(fila)
    TS = pd.DataFrame(tasas)
    cobertura = {"municipios_AEAT": int(bruta.index.nunique()), "municipios_ADRH_cv": int(pers.index.nunique()),
                 "municipios_en_ambas": int(len(set(bruta.index) & set(pers.index))),
                 "municipios_ADRH_sin_AEAT": int(len(set(pers.index) - set(bruta.index))),
                 "periodos_ADRH_base": sorted(int(c) for c in A["adrh_renta_neta_persona"].columns),
                 "agregacion": "media simple de secciones por municipio (sin pesos de población)"}
    return NV, TS, cobertura


# ---------------------------------------------------------------- 4. rupturas ADRH y ECV


def seccionado_adrh(A: dict) -> pd.DataFrame:
    P = A["adrh_renta_neta_persona"].copy()
    p21, _ = adrh_2021_crudo()
    P[2021] = p21
    P = P[[2019, 2020, 2021, 2022, 2023]]
    raw = pd.read_csv(RAW / "v3" / "ine_v3_gis_seccion.csv.gz", dtype=str, usecols=["codigo", "servicio"])
    rent = {2019: "Renta_neta_media_por_hogar__2019_", 2020: "1_Renta_neta_media_por_persona__2020_", 2021: "Renta_media_por_hogar",
            2022: "ADRH_2022_Renta_media_por_persona", 2023: "ADRH_2023_Renta_media_por_persona"}
    cod = {a: set(raw[raw.servicio == s].codigo) for a, s in rent.items()}
    anios = [2019, 2020, 2021, 2022, 2023]
    filas = []
    for a0, a1 in zip(anios[:-1], anios[1:], strict=True):
        c0, c1 = cod[a0], cod[a1]
        persist = c0 & c1
        mun0 = pd.Series([c[:5] for c in sorted(c0)]).value_counts()
        mun1 = pd.Series([c[:5] for c in sorted(c1)]).value_counts()
        cambia = {m for m in set(mun0.index) | set(mun1.index) if mun0.get(m, 0) != mun1.get(m, 0)}
        dl = (np.log(P[a1]) - np.log(P[a0])).dropna()
        dl = dl[dl.index.isin(persist)]
        marca = pd.Series([c[:5] in cambia for c in dl.index], index=dl.index)
        est, cam = dl[~marca], dl[marca]
        filas.append({"intervalo": f"{a0}->{a1}", "secciones_a0": len(c0), "secciones_a1": len(c1), "secciones_persisten": len(persist),
                      "secciones_salen": len(c0 - c1), "secciones_entran": len(c1 - c0),
                      "municipios_con_distinto_n_secciones": len(cambia), "n_var_estables": int(len(est)),
                      "mediana_var_log_estables": q(est, .5), "p05_estables": q(est, .05), "p95_estables": q(est, .95),
                      "pct_abs_gt_20_estables": round(float((est.abs() > .2).mean() * 100), 2) if len(est) else np.nan,
                      "n_var_cambiantes": int(len(cam)), "mediana_var_log_cambiantes": q(cam, .5),
                      "p05_cambiantes": q(cam, .05), "p95_cambiantes": q(cam, .95),
                      "pct_abs_gt_20_cambiantes": round(float((cam.abs() > .2).mean() * 100), 2) if len(cam) else np.nan})
    return pd.DataFrame(filas)


def cargar_ecv() -> pd.DataFrame:
    cache = os.environ.get("V15_ECV_CACHE")
    if cache and Path(cache).exists():
        return pd.read_pickle(cache)
    spec = importlib.util.spec_from_file_location("b6_condiciones", RAIZ / "src" / "v12" / "b6_condiciones.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    p = m.ecv()
    if cache:
        p.to_pickle(cache)
    return p


def ecv_diseno(p: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for a, g in p.groupby("anio"):
        alq = g.tenencia == "alquiler de mercado"
        filas.append({"anio": int(a), "personas_muestra": int(len(g)), "hogares_muestra": int(g.HB030.nunique()),
                      "suma_pesos_RB050_millones": round(float(g.RB050.sum() / 1e6), 2),
                      "pct_sin_nacionalidad": round(float(g.origen.isna().mean() * 100), 1),
                      "pct_sin_nacionalidad_adultos": round(float(g[g.edad_g != "0-17"].origen.isna().mean() * 100), 1),
                      "pct_sin_pais_nacimiento": round(float(g.nacimiento.isna().mean() * 100), 1),
                      "pct_sin_edad": round(float((g.edad_g == "nan").mean() * 100), 1),
                      "pct_sin_renta_HY020": round(float(g.HY020.isna().mean() * 100), 1),
                      "pct_sin_gasto_HH070": round(float(g.HH070.isna().mean() * 100), 1),
                      "pct_alquiler_mercado_sin_HH060_positivo": round(float((alq & ~(g.HH060 > 0)).sum() / max(alq.sum(), 1) * 100), 1),
                      "personas_con_esfuerzo_alquiler": int(g.esfuerzo_alquiler_30.notna().sum()),
                      "personas_con_sobrecarga": int(g.sobrecarga_30.notna().sum()),
                      "hogares_en_alquiler_mercado_con_esfuerzo": int(g.loc[g.esfuerzo_alquiler_30.notna(), "HB030"].nunique())})
    D = pd.DataFrame(filas)
    D["razon_hogares_vs_anio_previo"] = (D.hogares_muestra / D.hogares_muestra.shift(1)).round(3)
    D["razon_pesos_vs_anio_previo"] = (D.suma_pesos_RB050_millones / D.suma_pesos_RB050_millones.shift(1)).round(4)
    return D


# ---------------------------------------------------------------- 5. recuentos ECV y P8

INDIC = {"esfuerzo_alquiler_30": "esfuerzo_alquiler", "sobrecarga_30": "sobrecarga", "esfuerzo_hipoteca_30": "esfuerzo_hipoteca"}


def cuenta(g: pd.DataFrame, ind: str):
    x = g[g[ind].notna()]
    return int(len(x)), int(x.cl.nunique())


def ecv_celdas(p: pd.DataFrame):
    p = p.copy()
    p["cl"] = p.anio.astype(str) + "-" + p.HB030.astype(str)
    p["tenencia_g"] = p.tenencia.map({"propiedad sin hipoteca": "propiedad sin hipoteca", "propiedad con hipoteca": "propiedad con hipoteca",
                                       "alquiler de mercado": "alquiler de mercado", "alquiler inferior al de mercado": "alquiler reducido o cesion",
                                       "cesión gratuita": "alquiler reducido o cesion"})
    p["quintil"] = p.quintil_renta.map(lambda v: f"Q{int(v)}" if pd.notna(v) else None)
    a = p[p.edad_g != "0-17"].copy()
    a["periodo"] = a.anio.astype(str)
    base_ = pd.concat([a, a[a.anio >= 2023].assign(periodo="2023-2025"), a.assign(periodo="2018-2025")], ignore_index=True)
    filas = []
    for grupo in ("origen", "nacimiento", "edad_g", "tenencia_g"):
        for (an, cat), g in a.groupby(["anio", grupo]):
            for ind, nom in INDIC.items():
                n, h = cuenta(g, ind)
                filas.append({"anio": int(an), "grupo": grupo, "categoria": cat, "variable": nom, "n_personas": sup(n), "n_hogares": sup(h)})
    N = pd.DataFrame(filas)
    cruces = {
        "origen": ["origen"], "origen×edad": ["origen", "edad_g"], "origen×tenencia": ["origen", "tenencia_g"],
        "origen×quintil": ["origen", "quintil"], "origen×edad×tenencia": ["origen", "edad_g", "tenencia_g"],
        "origen×edad×quintil": ["origen", "edad_g", "quintil"], "origen×tenencia×quintil": ["origen", "tenencia_g", "quintil"],
        "origen×edad×tenencia×quintil": ["origen", "edad_g", "tenencia_g", "quintil"],
    }
    celdas, res = [], []
    for nom, ks in cruces.items():
        for per, g0 in base_.groupby("periodo"):
            if per not in ("2018", "2021", "2025", "2023-2025", "2018-2025"):
                continue
            for ind, ni in INDIC.items():
                x = g0[g0[ind].notna()].dropna(subset=ks)
                cel = x.groupby(ks).agg(n_personas=("RB030", "size"), n_hogares=("cl", "nunique")).reset_index()
                cel["cruce"], cel["periodo"], cel["variable"] = nom, per, ni
                cel["ok_n200_personas"] = cel.n_personas >= N_P8
                cel["ok_n200_hogares"] = cel.n_hogares >= N_P8
                res.append({"cruce": nom, "periodo": per, "variable": ni, "celdas": int(len(cel)), "celdas_n200_personas": int(cel.ok_n200_personas.sum()),
                            "celdas_n200_hogares": int(cel.ok_n200_hogares.sum()),
                            "pct_celdas_n200_hogares": round(float(cel.ok_n200_hogares.mean() * 100), 1) if len(cel) else np.nan,
                            "min_n_personas": int(cel.n_personas.min()) if len(cel) else 0,
                            "mediana_n_personas": float(cel.n_personas.median()) if len(cel) else 0,
                            "celdas_menores_10_suprimidas": int((cel.n_personas < MIN_N_CELDA).sum()),
                            "cruce_viable_todas_celdas_n200_hogares": bool(cel.ok_n200_hogares.all()) if len(cel) else False})
                celdas.append(cel[cel.n_personas >= MIN_N_CELDA])
    CE = pd.concat(celdas, ignore_index=True)
    for c in ("origen", "edad_g", "tenencia_g", "quintil"):
        CE[c] = CE[c].fillna("")
    CE = CE[["cruce", "periodo", "variable", "origen", "edad_g", "tenencia_g", "quintil", "n_personas", "n_hogares", "ok_n200_hogares"]]
    return N, pd.DataFrame(res), CE


# ---------------------------------------------------------------- Censo 2021, ECEPOV, EPA


def resumen_cruce(fuente: str, nom: str, c: pd.Series) -> dict:
    return {"fuente": fuente, "cruce": nom, "celdas": int(len(c)), "min_n": int(c.min()) if len(c) else 0,
            "celdas_n_menor_10": int((c < MIN_N_CELDA).sum()), "celdas_n200": int((c >= N_P8).sum()),
            "pct_celdas_n200": round(float((c >= N_P8).mean() * 100), 1) if len(c) else np.nan}


def censo_ecepov():
    filas, info = [], {}
    h = pd.read_csv(RAW / "v11" / "ine_censo2021" / "hogares_muestra_municipio_nacionalidad.csv.gz", dtype=str)
    h["n"] = pd.to_numeric(h.hogares_muestra)
    info["censo_hogares_muestra_total_crudo"] = int(h.n.sum())
    info["censo_municipios_crudo"] = int(h.cod_municipio.nunique())
    b = con_base().sql(f"select count(distinct territorio_codigo) m, sum(valor) s from '{HECHOS}' where variable='c21md_hogares_muestra' and {FILTRO}").df()
    info["censo_hogares_muestra_total_base"] = int(b.s[0])
    info["censo_municipios_base"] = int(b.m[0])
    info["censo_tenencia_codigos"] = sorted(h.tenencia.dropna().unique().tolist())
    info["censo_tiene_renta_o_gasto"] = False
    mun = h.groupby("cod_municipio").n.sum()
    info["censo_municipios_con_n200"] = int((mun >= N_P8).sum())
    info["censo_municipios_con_n_menor_10"] = int((mun < MIN_N_CELDA).sum())
    for ks, nom in ((["nac_primera_persona", "tenencia"], "nacionalidad×tenencia"),
                    (["nac_primera_persona", "edad_primera_persona", "tenencia"], "nacionalidad×edad×tenencia"),
                    (["nac_primera_persona", "llegada_espana", "tenencia"], "nacionalidad×llegada×tenencia"),
                    (["nac_primera_persona", "edad_primera_persona", "tenencia", "tipo_hogar"], "nacionalidad×edad×tenencia×tipo_hogar")):
        filas.append(resumen_cruce("Censo 2021 muestra 10 % (nacional, hogares de muestra)", nom, h.groupby(ks).n.sum()))
    z = zipfile.ZipFile(RAW / "v11" / "ine_ecepov" / "original" / "datos_2021.zip")
    zv = zipfile.ZipFile(io.BytesIO(z.read("ECEPOVvivienda.zip")))
    v = pd.read_csv(zv.open("CSV/ECEPOVvivienda_2021.csv"), sep="\t", usecols=["IDEN", "REGVI", "PAGOVI", "INGREHOG"], dtype=str)
    zh = zipfile.ZipFile(io.BytesIO(z.read("ECEPOVhogar.zip")))
    pe = pd.read_csv(zh.open("CSV/ECEPOVhogar_2021.csv"), sep="\t", usecols=["IDEN", "NPV", "NAC", "EDAD"], dtype=str)
    info["ecepov_personas_hogar"] = int(len(pe))
    pe = pe[pe.NPV == "01"].copy()
    pe["edad_g"] = pd.cut(pd.to_numeric(pe.EDAD, errors="coerce"), [-1, 34, 49, 64, 200], labels=["<=34", "35-49", "50-64", "65+"]).astype(str)
    e = v.merge(pe[["IDEN", "NAC", "edad_g"]], on="IDEN", how="left")
    e["tenencia"] = e.REGVI.map({"1": "propia herencia/donacion", "2": "propia pagada", "3": "propia con hipoteca", "4": "alquilada", "5": "cedida", "6": "otra"})
    e["ing"] = pd.to_numeric(e.INGREHOG, errors="coerce")
    e["ing_g"] = pd.cut(e.ing, [0, 2, 3, 4, 100], labels=["<1.000", "1.000-1.500", "1.500-2.000", ">=2.000"]).astype(str)
    e["pago"] = e.PAGOVI.str.strip().replace("", np.nan)
    e["nac"] = e.NAC.map({"1": "NAC=1", "2": "NAC=2"})
    info["ecepov_viviendas"] = int(len(v))
    info["ecepov_pct_pago_vivienda_informado"] = round(float(e.pago.notna().mean() * 100), 1)
    alq = e.tenencia == "alquilada"
    info["ecepov_viviendas_alquiladas"] = int(alq.sum())
    info["ecepov_pct_alquiladas_con_pago_e_ingreso"] = round(float((alq & e.pago.notna() & e.ing.notna()).sum() / max(alq.sum(), 1) * 100), 1)
    info["ecepov_renta_intervalizada"] = True
    for ks, nom, sub in ((["tenencia"], "tenencia", e), (["tenencia", "ing_g"], "tenencia×ingreso", e), (["tenencia", "nac"], "tenencia×nacionalidad", e),
                         (["tenencia", "nac", "ing_g"], "tenencia×nacionalidad×ingreso", e), (["tenencia", "nac", "edad_g"], "tenencia×nacionalidad×edad", e),
                         (["tenencia", "nac", "edad_g", "ing_g"], "tenencia×nacionalidad×edad×ingreso", e),
                         (["nac", "edad_g", "ing_g"], "alquiler: nacionalidad×edad×ingreso", e[alq]), (["nac", "ing_g"], "alquiler: nacionalidad×ingreso", e[alq])):
        filas.append(resumen_cruce("ECEPOV 2021 (viviendas muestrales; persona 01 del hogar)", nom, sub.dropna(subset=ks).groupby(ks).size()))
    ep = sorted(f.name for f in (RAW / "v9" / "ine_microdatos" / "epa").glob("datos_*t*.zip"))
    trims = sorted((2000 + int(re.search(r"_(\d)t(\d\d)", f).group(2)), int(re.search(r"_(\d)t(\d\d)", f).group(1))) for f in ep)
    info["epa_trimestres"] = len(trims)
    info["epa_primero"], info["epa_ultimo"] = f"{trims[0][0]}T{trims[0][1]}", f"{trims[-1][0]}T{trims[-1][1]}"
    info["epa_huecos"] = [f"{y}T{t}" for y in range(trims[0][0], trims[-1][0] + 1) for t in range(1, 5) if trims[0] <= (y, t) <= trims[-1] and (y, t) not in set(trims)]
    info["epa_diseno_registro_2021_presente"] = (RAW / "v9" / "ine_microdatos" / "epa" / "dr_EPA_2021.xlsx").exists()
    return pd.DataFrame(filas), info


# ---------------------------------------------------------------- principal


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    con = con_base()
    d = cargar_aeat()
    EST, RZ, HIP, extra = tarea1_aeat(d)
    EST.to_csv(OUT / "aeat_estructura_por_ejercicio.csv", index=False)
    RZ.to_csv(OUT / "aeat_razones_entre_ejercicios.csv", index=False)
    HIP.to_csv(OUT / "aeat_hipotesis_recuentos_2015.csv", index=False)
    extra["chk"].to_csv(OUT / "aeat_comprobacion_unidades_2016_2024.csv", index=False)
    ATa, TOPa, RGa = atipicos_aeat(con)
    A = cargar_adrh(con)
    ATd, TOPd, RGd = atipicos_adrh(A)
    AT = pd.concat([ATa.assign(fuente="AEAT"), ATd.assign(fuente="ADRH")], ignore_index=True)
    AT.to_csv(OUT / "atipicos_recuento.csv", index=False)
    TOP = pd.concat([TOPa.assign(fuente="AEAT"), TOPd.assign(fuente="ADRH")], ignore_index=True)
    TOP = TOP.reindex(TOP.z_robusto.abs().sort_values(ascending=False, kind="mergesort").index).head(40).reset_index(drop=True)
    TOP.to_csv(OUT / "atipicos_top40.csv", index=False)
    NV, TS, cob = tarea3_coherencia(con, A)
    NV.to_csv(OUT / "coherencia_aeat_adrh_niveles.csv", index=False)
    TS.to_csv(OUT / "coherencia_aeat_adrh_tasas.csv", index=False)
    SEC = seccionado_adrh(A)
    SEC.to_csv(OUT / "adrh_seccionado_rupturas.csv", index=False)
    p = cargar_ecv()
    DIS = ecv_diseno(p)
    DIS.to_csv(OUT / "ecv_diseno_por_anio.csv", index=False)
    N, RES, CE = ecv_celdas(p)
    N.to_csv(OUT / "ecv_n_por_anio_grupo.csv", index=False)
    RES.to_csv(OUT / "p8_cruces_resumen.csv", index=False)
    CE.to_csv(OUT / "p8_celdas_ecv_n.csv", index=False)
    CEN, info = censo_ecepov()
    CEN.to_csv(OUT / "p8_censo_ecepov_n.csv", index=False)

    def por_concepto(par):
        return {r.concepto: r.razon_mediana for r in RZ[RZ.par == par].itertuples()}

    dictamen = {
        "veredicto": "NO UTILIZABLE como serie de renta en euros; el reescalado no es aplicable",
        "motivo": ("La tabla de 2013-2015 no tiene las mismas magnitudes que la de 2016-2024: carece de NÚMERO DE DECLARACIONES, RENTA BRUTA MEDIA y RENTA "
                   "DISPONIBLE MEDIA y sus valores tienen el orden de un recuento de declarantes por concepto, no de un importe. Un factor de unidades "
                   "(euros frente a miles de euros) no la reconcilia (ver razones)."),
        "razon_mediana_2014_2015": por_concepto("2014/2015"), "razon_mediana_2015_2016": por_concepto("2015/2016"),
        "razon_mediana_2016_2017": por_concepto("2016/2017"),
    }
    resultado = {
        "rama": "v15/auditoria/renta_microdatos",
        "pregunta": ("¿Son utilizables la renta de la AEAT (2013-2015 y 2016-2024), el ADRH por sección y los microdatos (ECV, ECEPOV, Censo 2021) para P8 "
                     "(esfuerzo de acceso por renta, edad, nacionalidad y tenencia)? Unidades, atípicos, coherencia, rupturas y tamaños muestrales."),
        "capa": "C4",
        "datos": ["AEAT IRPF por municipios, Comunitat Valenciana (crudo 2013-2024; base 2016-2024)", "INE ADRH por sección (base 2019, 2020, 2022, 2023; crudo 2021)",
                  "INE ECV microdatos 2018-2025", "INE ECEPOV 2021 (microdatos)", "INE Censo 2021, muestra 10 % (c21md_*, solo agregados n>=10)",
                  "INE EPA 2018T1-2026T2 (solo inventario)"],
        "N": {"municipios_AEAT": int(d.cod_municipio.nunique()), "secciones_ADRH_base": int(A["adrh_renta_neta_persona"].shape[0]),
              "personas_ECV": int(len(p)), "viviendas_ECEPOV": info["ecepov_viviendas"]},
        "metodo": ("Auditoría descriptiva determinista (SEED=20261010): razones entre ejercicios por municipio y concepto, z robusto con mediana y MAD (|z|>5) "
                   "en cortes transversales y variaciones, correlación de niveles (log) y de variaciones entre AEAT y ADRH agregado a municipio por código INE, "
                   "recuentos muestrales por año × grupo y por cruce de P8 (umbral n>=200). Sin estimación de efectos."),
        "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO",
        "diagnosticos": {
            "aeat_dictamen_2013_2015": dictamen,
            "aeat_estructura_por_ejercicio": json.loads(EST.to_json(orient="records")),
            "aeat_razones": json.loads(RZ.to_json(orient="records")),
            "aeat_hipotesis_recuentos_2015": json.loads(HIP.to_json(orient="records")),
            "aeat_comprobacion_unidades_2016_2024": json.loads(extra["chk"].to_json(orient="records")),
            "aeat_conceptos_y_municipios": extra["ex"],
            "atipicos_recuento_resumen": json.loads(AT.groupby(["fuente", "variable", "tipo"]).agg(n_atip=("n_atip", "sum"), n=("n", "sum")).reset_index().to_json(orient="records")),
            "atipicos_top40": json.loads(TOP.to_json(orient="records")),
            "rangos_aeat": RGa, "rangos_adrh": RGd,
            "coherencia_niveles": json.loads(NV.to_json(orient="records")),
            "coherencia_tasas": json.loads(TS.to_json(orient="records")),
            "coherencia_cobertura": cob,
            "adrh_seccionado": json.loads(SEC.to_json(orient="records")),
            "ecv_diseno": json.loads(DIS.to_json(orient="records")),
            "p8_cruces_resumen": json.loads(RES[RES.periodo.isin(["2025", "2023-2025", "2018-2025"]) & (RES.variable != "esfuerzo_hipoteca")].to_json(orient="records")),
            "censo_ecepov_epa": info,
            "censo_ecepov_cruces": json.loads(CEN.to_json(orient="records")),
        },
        "fuera_muestra": None,
        "notas": ["Auditoría C4: sin efectos. Solo agregados propios de AEAT (razones, recuentos de atípicos, correlaciones); sin series municipales de AEAT.",
                  "Celdas del Censo 2021 (clase b) y recuentos ECV con n<10 suprimidos; no se escribe ningún microdato.",
                  "ADRH 2021 solo en el crudo (data/raw/v3), con campos etiquetados por orden (supuesto); la base no tiene 2021.",
                  "ECEPOV: persona 01 del hogar como proxy de la persona de referencia; códigos NAC no decodificados en el inventario.",
                  "ECV: la ruptura de 2021 (base del Censo) no consta en docs/: se reportan solo señales de los datos."],
    }

    def conv(o):
        if isinstance(o, np.floating):
            return None if np.isnan(o) else float(o)
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.bool_):
            return bool(o)
        return str(o)

    (OUT / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1, default=conv), encoding="utf-8")
    print("OK", OUT)


if __name__ == "__main__":
    main()

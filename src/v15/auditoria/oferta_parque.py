"""V15 · Fase 1.2 · Auditoría de datos del grupo OFERTA Y PARQUE (C4, descriptivo; sin efectos ni regresiones).

Fuentes: MIVAU (iniciadas y terminadas libres, calificaciones definitivas de protegida, parque estimado),
Catastro (unidades urbanas residenciales por municipio y ejercicio), Censos 2011 y 2021 (INE) y la geometría municipal.
Tareas: (1) atípicos robustos (mediana y MAD, |z| > 5); (2) coherencia flujo-stock por provincia (código INE);
(3) rupturas; (4) inventario de restricciones físicas para P1; (5) cobertura municipal por año.

Determinista (SEED = 20261010). Lee data/base y data/raw; escribe solo en output/v15/auditoria/oferta_parque/.
Uso: python3 src/v15/auditoria/oferta_parque.py
"""
from __future__ import annotations

import csv
import json
import os
import re
import unicodedata
import warnings
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

SEED = 20261010
RAIZ = Path(__file__).resolve().parents[3]
OUT = RAIZ / "output/v15/auditoria/oferta_parque"
HECHOS = RAIZ / "data/base/hechos.parquet"
UMBRAL_Z = 5.0
UMBRAL_REL = 0.15
UNIPROV = {"asturias": "33", "balears": "07", "cantabria": "39", "madrid": "28", "murcia": "30",
           "navarra": "31", "rioja": "26"}
warnings.simplefilter("ignore", RuntimeWarning)


# ----------------------------------------------------------------------------------------------- utilidades
def clave(nombre: str) -> str:
    n = re.sub(r"\(.*?\)", "", str(nombre)).split(",")[0]
    n = "".join(c for c in unicodedata.normalize("NFKD", n) if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", n.lower())


def z_filas(m: np.ndarray, min_n: int = 8) -> np.ndarray:
    """z robusto por fila: (x - mediana) / (1,4826 MAD); si MAD = 0, desviación media absoluta * 1,2533."""
    med = np.nanmedian(m, axis=1, keepdims=True)
    dev = np.abs(m - med)
    mad = 1.4826 * np.nanmedian(dev, axis=1, keepdims=True)
    alt = 1.2533 * np.nanmean(dev, axis=1, keepdims=True)
    esc = np.where(mad > 0, mad, alt)
    z = (m - med) / np.where(esc > 0, esc, np.nan)
    n = np.sum(~np.isnan(m), axis=1)
    z[n < min_n, :] = np.nan
    return z


def qidx(p: str) -> int:
    a, q = p.split("T")
    return int(a) * 4 + int(q) - 1


def spearman(a: pd.Series, b: pd.Series) -> float:
    d = pd.concat([a, b], axis=1).dropna()
    if len(d) < 5:
        return float("nan")
    return float(np.corrcoef(d.iloc[:, 0].rank(), d.iloc[:, 1].rank())[0, 1])


def num(x) -> float | None:
    return float(x) if x is not None and np.isfinite(x) else None


# ----------------------------------------------------------------------------------------------- carga
def territorios() -> tuple[pd.DataFrame, dict[str, str]]:
    t = pd.read_parquet(RAIZ / "data/base/territorios.parquet")
    p = t[t.nivel == "provincia"][["territorio_codigo", "nombre", "cod_ccaa"]].copy()
    p["clave"] = p.nombre.map(clave)
    assert p.clave.is_unique and len(p) == 52
    return p.sort_values("territorio_codigo").reset_index(drop=True), dict(zip(p.clave, p.territorio_codigo, strict=True))


def a_unidad(d: pd.DataFrame, mapa: dict[str, str]) -> pd.DataFrame:
    """Asigna código INE de provincia: provincias por nombre; CCAA uniprovinciales por su provincia; Ceuta y Melilla."""
    d = d.copy()
    cod = []
    for nivel, terr, serie in zip(d.nivel, d.territorio, d.serie, strict=True):
        c = None
        if nivel == "provincia":
            c = mapa.get(clave(terr))
        elif nivel == "ccaa":
            c = UNIPROV.get(clave(terr))
        elif nivel == "ciudad_autonoma":
            s = serie.lower()
            c = "CM" if "ceuta_y_melilla" in s else ("51" if s.endswith("ceuta") else "52" if s.endswith("melilla") else None)
        cod.append(c)
    d["u"] = cod
    return d


def leer_raw(nombre: str, prefijo: str, mapa: dict[str, str]) -> tuple[pd.DataFrame, dict]:
    d = pd.read_csv(RAIZ / "data/raw" / nombre, dtype={"periodo": str})
    d = d[d.serie.str.startswith(prefijo)].drop_duplicates(["serie", "periodo"])
    d = a_unidad(d[d.nivel != "nacional"], mapa)
    sin = sorted(d[d.u.isna()].territorio.unique().tolist())
    d = d.dropna(subset=["u"])
    assert d.groupby(["u", "periodo"]).size().max() == 1
    wide = d.pivot(index="u", columns="periodo", values="valor").sort_index(axis=1)
    return wide, {"sin_codigo": sin}


def anual_desde_mensual(w: pd.DataFrame, y0: int, y1: int) -> pd.DataFrame:
    out = {}
    for y in range(y0, y1 + 1):
        cols = [f"{y}-{m:02d}" for m in range(1, 13)]
        if all(c in w.columns for c in cols):
            out[y] = w[cols].sum(axis=1, min_count=12)
    return pd.DataFrame(out)


def ventana(w: pd.DataFrame, m0: str, m1: str) -> pd.Series:
    cols = [c for c in w.columns if m0 <= c <= m1]
    esperado = (int(m1[:4]) - int(m0[:4])) * 12 + int(m1[5:]) - int(m0[5:]) + 1
    assert len(cols) == esperado, (m0, m1, len(cols))
    return w[cols].sum(axis=1, min_count=esperado)


def meses_ausentes(w: pd.DataFrame) -> list[str]:
    todos = pd.period_range(w.columns.min(), w.columns.max(), freq="M").strftime("%Y-%m")
    return [m for m in todos if m not in w.columns]


def valor_es(s: str) -> float:
    return float(s.replace(".", "").replace(",", "."))


def censo2021(prov: pd.DataFrame) -> pd.DataFrame:
    """Viviendas Censo 2021 por provincia (tpx 59521: tipo x provincia x año de construcción; fila Total)."""
    f = RAIZ / "data/raw/v11/ine_censo2021/censo2021_tpx59521.csv"
    ok = {(c, k) for c, k in zip(prov.territorio_codigo, prov.clave, strict=True)}
    filas = {}
    with open(f, encoding="utf-8-sig") as fh:
        for r in csv.reader(fh, delimiter=";"):
            if len(r) < 4 or r[2] != "Total" or r[0] not in ("Total", "Vivienda principal", "Vivienda no principal"):
                continue
            m = re.match(r"(\d{2}) (.*)", r[1])
            if m and (m.group(1), clave(m.group(2))) in ok:
                filas[(m.group(1), r[0])] = valor_es(r[3])
    d = pd.DataFrame({"tot2021": {k[0]: v for k, v in filas.items() if k[1] == "Total"},
                      "ppal2021": {k[0]: v for k, v in filas.items() if k[1] == "Vivienda principal"},
                      "nopal2021": {k[0]: v for k, v in filas.items() if k[1] == "Vivienda no principal"}})
    f2 = RAIZ / "data/raw/v11/ine_censo2021/censo2021_tpx59520.csv"
    alt = {}
    with open(f2, encoding="utf-8-sig") as fh:
        for r in csv.reader(fh, delimiter=";"):
            if len(r) >= 4 and r[0] == "Total" and r[2].startswith("Total (tamaño"):
                m = re.match(r"(\d{2}) (.*)", r[1])
                if m and (m.group(1), clave(m.group(2))) in ok:
                    alt[m.group(1)] = valor_es(r[3])
    d["tot2021_t59520"] = pd.Series(alt)
    assert len(d) == 52, len(d)
    return d


# ----------------------------------------------------------------------------------------------- tarea 1
def atipicos_mivau(con, extra: dict[str, tuple[pd.DataFrame, str]]) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    q = """select variable, nivel, frecuencia f, territorio_codigo t, periodo p, valor, metodo_dato m
           from 'data/base/hechos.parquet'
           where variable in ('iniciadas','terminadas','visados','iniciadas_anual_tabla','terminadas_anual_tabla','permisos')
             and nivel in ('nacional','ccaa','provincia')"""
    h = con.execute(q).fetchdf()
    ndup = int(h.duplicated(["variable", "nivel", "f", "t", "p"]).sum())
    ndup_dist = int(h.drop_duplicates().duplicated(["variable", "nivel", "f", "t", "p"]).sum())
    h = h.drop_duplicates(["variable", "nivel", "f", "t", "p"])
    n_interp = int((h.m == "interpolado").sum())
    h = h[h.m != "interpolado"]
    grupos: dict[tuple, pd.DataFrame] = {}
    for (v, n, f), g in h.groupby(["variable", "nivel", "f"]):
        g = g.assign(i=g.p.map(qidx) if f == "T" else g.p.astype(int))
        grupos[(v, n, f)] = g.pivot(index="t", columns="i", values="valor")
    for nombre, (w, f) in extra.items():
        grupos[(nombre, "unidad_prov", f)] = w
    res, det = [], []
    huecos = {}
    for (v, n, f), w in sorted(grupos.items()):
        paso = 4 if f == "T" else 1
        cols = np.arange(w.columns.min(), w.columns.max() + 1)
        w = w.reindex(columns=cols)
        lw = np.log1p(w.to_numpy(float))
        zn = z_filas(lw)
        d = lw[:, paso:] - lw[:, :-paso]
        zy = np.full_like(lw, np.nan)
        zy[:, paso:] = z_filas(d)
        faltan = int(np.isnan(lw).sum())
        if faltan and f == "T":
            huecos[f"{v}|{n}"] = faltan
        fn, fy = np.abs(zn) > UMBRAL_Z, np.abs(zy) > UMBRAL_Z
        res.append({"variable": v, "nivel": n, "frecuencia": f, "n_series": w.shape[0],
                    "n_obs": int((~np.isnan(lw)).sum()), "n_huecos_internos": faltan,
                    "n_ceros": int((w.to_numpy(float) == 0).sum()),
                    "n_atipicos_nivel_log": int(fn.sum()), "n_atipicos_var_interanual": int(fy.sum()),
                    "n_series_con_atipico": int((fn | fy).any(axis=1).sum())})
        for r, c in zip(*np.where(fn | fy), strict=True):
            per = f"{cols[c] // 4}T{cols[c] % 4 + 1}" if f == "T" else str(cols[c])
            det.append({"variable": v, "nivel": n, "frecuencia": f, "territorio": w.index[r], "periodo": per,
                        "valor": w.iat[r, c], "z_nivel_log": num(zn[r, c]), "z_var_interanual": num(zy[r, c])})
    inf = {"duplicados_exactos_entre_origenes": ndup, "duplicados_con_valor_distinto": ndup_dist,
           "filas_interpoladas_excluidas": n_interp, "huecos_trimestrales_internos": huecos}
    return pd.DataFrame(res), pd.DataFrame(det), inf


def atipicos_catastro(con) -> tuple[pd.DataFrame, pd.DataFrame, dict, pd.DataFrame]:
    h = con.execute("""select territorio_codigo t, periodo p, variable v, valor from 'data/base/hechos.parquet'
                       where variable in ('obra_nueva_neta_catastro','catastro_unidades_urbanas_residenciales')""").fetchdf()
    neta = h[h.v == "obra_nueva_neta_catastro"].pivot(index="t", columns="p", values="valor")
    stock = h[h.v == "catastro_unidades_urbanas_residenciales"].pivot(index="t", columns="p", values="valor")
    val = neta.to_numpy(float)
    z = z_filas(val)
    flag = np.abs(z) > UMBRAL_Z
    mat = flag & (np.abs(val) >= 50)
    filas = [{"municipio": neta.index[r], "ejercicio_fichero": neta.columns[c], "obra_neta": val[r, c], "z": float(z[r, c])}
             for r, c in zip(*np.where(mat), strict=True)]
    det = pd.DataFrame(filas)
    if len(det):
        det = det.reindex(det.z.abs().sort_values(ascending=False, kind="stable").index).head(2000)
    por_anio = pd.DataFrame({"ejercicio_fichero": neta.columns, "n_municipios": neta.notna().sum().to_numpy(),
                             "n_atipicos_z5": flag.sum(axis=0), "n_atipicos_z5_material_ge50": mat.sum(axis=0),
                             "n_negativos": (val < 0).sum(axis=0), "neta_total_catastro_estatal": np.nansum(val, axis=0)})
    neta_p = neta.groupby(neta.index.str[:2]).sum(min_count=1)
    zp = z_filas(neta_p.to_numpy(float))
    prov_fl = [{"provincia": neta_p.index[r], "ejercicio_fichero": neta_p.columns[c], "obra_neta": float(neta_p.iat[r, c]),
                "z": float(zp[r, c])} for r, c in zip(*np.where(np.abs(zp) > UMBRAL_Z), strict=True)]
    evaluables = neta.notna().sum(axis=1).to_numpy() >= 8
    inf = {"municipios_con_serie_evaluable": int(evaluables.sum()),
           "atipicos_z5_total": int(flag.sum()), "atipicos_z5_material_ge50": int(mat.sum()),
           "series_sin_escala_(constantes)": int((evaluables & np.isnan(z).all(axis=1)).sum()),
           "provincias_atipico_z5": prov_fl, "negativos_total": int((val < 0).sum()),
           "atipicos_material_por_ejercicio": dict(zip(por_anio.ejercicio_fichero, por_anio.n_atipicos_z5_material_ge50.astype(int), strict=True))}
    return por_anio, det, inf, stock


# ----------------------------------------------------------------------------------------------- tarea 2
def flujo_stock(prov: pd.DataFrame, term_m, prot_m, stock_m: pd.DataFrame, cen11: pd.DataFrame, cen21: pd.DataFrame):
    sp = stock_m.groupby(stock_m.index.str[:2]).sum(min_count=1)  # provincia (código INE) x fichero
    unid = prov.territorio_codigo.tolist()
    d = pd.DataFrame(index=unid)
    d["nombre"] = prov.set_index("territorio_codigo").nombre
    d["delta_censo_familiar"] = cen21.tot2021.reindex(unid) - cen11.familiar.reindex(unid)
    d["delta_censo_total11"] = cen21.tot2021.reindex(unid) - cen11.total.reindex(unid)
    lib = ventana(term_m, "2011-11", "2021-10").reindex(unid)
    pro = ventana(prot_m, "2011-11", "2021-10").reindex(unid)
    d["flujo_libres_nov11_oct21"] = lib
    d["flujo_libres_mas_protegida_nov11_oct21"] = lib + pro
    d["dif_rel_libres_vs_censo"] = d.flujo_libres_nov11_oct21 / d.delta_censo_familiar - 1
    d["dif_rel_total_vs_censo"] = d.flujo_libres_mas_protegida_nov11_oct21 / d.delta_censo_familiar - 1
    # Catastro. A) convención del origen (fichero t = stock a 31-12-(t-1)): flujo 2012-2021 frente a fichero 2022 - 2012.
    # B) convención de hechos (periodo t = 31-12-t): flujo 2013-2021 frente a fichero 2021 - 2012.
    la = ventana(term_m, "2012-01", "2021-12").reindex(unid) + ventana(prot_m, "2012-01", "2021-12").reindex(unid)
    lb = ventana(term_m, "2013-01", "2021-12").reindex(unid) + ventana(prot_m, "2013-01", "2021-12").reindex(unid)
    d["delta_catastro_A_fichero2022_menos_2012"] = (sp["2022"] - sp["2012"]).reindex(unid)
    d["flujo_total_2012_2021"] = la
    d["dif_rel_total_vs_catastro_A"] = la / d.delta_catastro_A_fichero2022_menos_2012 - 1
    d["delta_catastro_B_fichero2021_menos_2012"] = (sp["2021"] - sp["2012"]).reindex(unid)
    d["flujo_total_2013_2021"] = lb
    d["dif_rel_total_vs_catastro_B"] = lb / d.delta_catastro_B_fichero2021_menos_2012 - 1
    d["catastro_A_sobre_censo"] = d.delta_catastro_A_fichero2022_menos_2012 / d.delta_censo_familiar - 1
    d["nivel_catastro2012_sobre_censo2011"] = sp["2012"].reindex(unid) / cen11.familiar.reindex(unid)
    d["nivel_catastro2022_sobre_censo2021"] = sp["2022"].reindex(unid) / cen21.tot2021.reindex(unid)
    d["viv_censo2011_familiar"] = cen11.familiar.reindex(unid)
    d["gap_total_vs_censo_por_mil_stock11"] = (d.flujo_libres_mas_protegida_nov11_oct21 - d.delta_censo_familiar) / d.viv_censo2011_familiar * 1000
    for c in COLS_REL:
        d["fuera15_" + c.replace("dif_rel_", "")] = np.where(d[c].notna(), d[c].abs() > UMBRAL_REL, np.nan)
    d.index.name = "provincia_ine"
    return d.reset_index(), sp


COLS_REL = ["dif_rel_libres_vs_censo", "dif_rel_total_vs_censo", "dif_rel_total_vs_catastro_A", "dif_rel_total_vs_catastro_B",
            "catastro_A_sobre_censo"]


def resumen_flujo_stock(d: pd.DataFrame) -> dict:
    out = {}
    for c in COLS_REL:
        s = d[c].dropna()
        out[c] = {"n": int(len(s)), "n_fuera_15": int((s.abs() > UMBRAL_REL).sum()), "mediana": num(s.median()),
                  "p10": num(s.quantile(0.1)), "p90": num(s.quantile(0.9)),
                  "fuera_15_provincias": d.loc[d[c].abs() > UMBRAL_REL, "provincia_ine"].tolist()}
    for c in ["nivel_catastro2012_sobre_censo2011", "nivel_catastro2022_sobre_censo2021"]:
        s = d[c].dropna()
        out[c] = {"n": int(len(s)), "min": num(s.min()), "mediana": num(s.median()), "max": num(s.max()),
                  "n_fuera_15": int(((s - 1).abs() > UMBRAL_REL).sum())}
    tot = d[["delta_censo_familiar", "flujo_libres_nov11_oct21", "flujo_libres_mas_protegida_nov11_oct21"]].sum()
    out["nacional_52_unidades"] = {k: num(v) for k, v in tot.items()}
    foral = ["01", "20", "48", "31"]
    fp = d[d.provincia_ine.isin(foral)]
    out["pais_vasco_navarra_dif_rel_total_vs_censo"] = {k: round(float(v), 3) for k, v in zip(fp.provincia_ine, fp.dif_rel_total_vs_censo, strict=True)}
    out["pais_vasco_navarra_dif_rel_libres_vs_censo"] = {k: round(float(v), 3) for k, v in zip(fp.provincia_ine, fp.dif_rel_libres_vs_censo, strict=True)}
    c48 = d.dropna(subset=["delta_catastro_A_fichero2022_menos_2012"])
    out["catastro_48_provincias"] = {k: num(c48[k].sum()) for k in [
        "delta_catastro_A_fichero2022_menos_2012", "flujo_total_2012_2021", "delta_catastro_B_fichero2021_menos_2012",
        "flujo_total_2013_2021", "delta_censo_familiar"]}
    out["resto_dif_rel_total_vs_censo_mediana"] = num(d[~d.provincia_ine.isin(foral)].dif_rel_total_vs_censo.median())
    out["resto_dif_rel_libres_vs_censo_mediana"] = num(d[~d.provincia_ine.isin(foral)].dif_rel_libres_vs_censo.median())
    return out


def coherencia_anual(sp: pd.DataFrame, term_a: pd.DataFrame, prot_a: pd.DataFrame, unid: list[str]) -> tuple[pd.DataFrame, dict]:
    """Catastro frente a MIVAU por año. Convención del origen: variación del año t = fichero(t+1) - fichero(t).
    Convención de hechos: variación etiquetada t = fichero(t) - fichero(t-1), comparada con las terminadas del año t."""
    tot = (term_a + prot_a.reindex(term_a.index)).reindex(unid)
    est = sp.reindex([u for u in unid if u in sp.index])
    filas, corr = [], []
    for y in range(2012, 2026):
        neta_b4 = est[str(y + 1)] - est[str(y)]
        f = tot[y].reindex(est.index)
        r = neta_b4 / f
        filas.append({"anio_terminadas": y, "convencion": "fichero(t+1)-fichero(t)", "n_prov": int(r.notna().sum()),
                      "ratio_agregado": num(neta_b4.sum() / f.sum()), "ratio_mediana_prov": num(r.median()),
                      "n_prov_dentro_15": int(((r - 1).abs() <= UMBRAL_REL).sum()), "n_prov_ratio_mayor_2": int((r > 2).sum())})
        if y >= 2013:
            neta_h = est[str(y)] - est[str(y - 1)]
            rh = neta_h / f
            filas.append({"anio_terminadas": y, "convencion": "fichero(t)-fichero(t-1) [etiqueta hechos]", "n_prov": int(rh.notna().sum()),
                          "ratio_agregado": num(neta_h.sum() / f.sum()), "ratio_mediana_prov": num(rh.median()),
                          "n_prov_dentro_15": int(((rh - 1).abs() <= UMBRAL_REL).sum()), "n_prov_ratio_mayor_2": int((rh > 2).sum())})
            corr.append({"anio": y, "rho_fichero": spearman(neta_b4, f), "rho_hechos": spearman(neta_h, f)})
    c = pd.DataFrame(corr)
    f = pd.DataFrame(filas)
    rec = f[f.anio_terminadas.between(2018, 2024)].assign(d=lambda x: (x.ratio_agregado - 1).abs())
    inf = {"desvio_medio_abs_ratio_agregado_1_2018_2024": {k: num(g.d.mean()) for k, g in rec.groupby("convencion")},
           "spearman_corte_transversal_media_fichero_t1_menos_t": num(c.rho_fichero.mean()),
           "spearman_corte_transversal_media_etiqueta_hechos": num(c.rho_hechos.mean()),
           "anios_donde_gana_fichero": int((c.rho_fichero > c.rho_hechos).sum()), "anios_comparados": int(len(c))}
    return pd.DataFrame(filas), inf


def parque_vs_censo(mapa, cen11, cen21) -> tuple[pd.DataFrame, dict]:
    p = pd.read_csv(RAIZ / "data/raw/mivau_parque.csv", dtype={"periodo": str})
    nac = p[p.nivel == "nacional"].set_index("periodo").valor
    q = a_unidad(p[p.nivel != "nacional"], mapa).dropna(subset=["u"])
    w = q.pivot(index="u", columns="periodo", values="valor")
    cm11 = cen11.familiar.reindex(["51", "52"]).sum()
    cm21 = cen21.tot2021.reindex(["51", "52"]).sum()
    filas = []
    for u in sorted(w.index):
        c11 = cm11 if u == "CM" else cen11.familiar.get(u)
        c21 = cm21 if u == "CM" else cen21.tot2021.get(u)
        filas.append({"unidad": u, "parque_2011": w.at[u, "2011"], "parque_2021": w.at[u, "2021"],
                      "delta_parque_2011_2021": w.at[u, "2021"] - w.at[u, "2011"],
                      "censo_2011_familiar": c11, "censo_2021": c21, "delta_censo": c21 - c11,
                      "nivel2011_parque_sobre_censo": w.at[u, "2011"] / c11, "nivel2021_parque_sobre_censo": w.at[u, "2021"] / c21})
    d = pd.DataFrame(filas)
    d["delta_parque_sobre_delta_censo"] = d.delta_parque_2011_2021 / d.delta_censo - 1
    d["fuera15_delta"] = d.delta_parque_sobre_delta_censo.abs() > UMBRAL_REL
    inf = {"unidades": int(len(d)), "fuera15_delta": int(d.fuera15_delta.sum()),
           "unidades_fuera15": d.loc[d.fuera15_delta, "unidad"].tolist(),
           "nivel2011_min_med_max": [num(d.nivel2011_parque_sobre_censo.min()), num(d.nivel2011_parque_sobre_censo.median()),
                                     num(d.nivel2011_parque_sobre_censo.max())],
           "nivel2021_min_med_max": [num(d.nivel2021_parque_sobre_censo.min()), num(d.nivel2021_parque_sobre_censo.median()),
                                     num(d.nivel2021_parque_sobre_censo.max())],
           "nacional_parque_2011_2021": [num(nac.get("2011")), num(nac.get("2021"))],
           "nacional_censo_2011_familiar_2021": [num(cen11.familiar.sum()), num(cen21.tot2021.sum())]}
    return d, inf


def coherencia_fuentes(con, prov, ini_m, term_m, ini_a, term_a) -> pd.DataFrame:
    filas = []

    def add(chequeo, detalle, n, nd, mx, mxr):
        filas.append({"chequeo": chequeo, "detalle": detalle, "n_comparaciones": n, "n_discrepancias": nd,
                      "max_abs_dif": mx, "max_rel_dif": mxr})

    h = con.execute("""select variable, nivel, territorio_codigo t, periodo p, valor from 'data/base/hechos.parquet'
        where frecuencia='T' and ((variable='visados' and nivel='ccaa') or (variable='iniciadas' and nivel='provincia'))""").fetchdf()
    h = h.drop_duplicates(["variable", "nivel", "t", "p"])
    vis = h[h.variable == "visados"].pivot(index="p", columns="t", values="valor")
    ini = h[h.variable == "iniciadas"].pivot(index="p", columns="t", values="valor")
    n = nd = 0
    mx = mr = 0.0
    completas = []
    for cc, g in prov.groupby("cod_ccaa"):
        ps = g.territorio_codigo.tolist()
        if len(ps) > 1 and all(x in ini.columns for x in ps) and cc in vis.columns:
            completas.append(cc)
            s = ini[ps].sum(axis=1, min_count=len(ps))
            dd = (vis[cc] - s).dropna()
            n += len(dd)
            nd += int((dd.abs() > 0.5).sum())
            mx = max(mx, float(dd.abs().max()))
            mr = max(mr, float((dd.abs() / s.reindex(dd.index)).max()))
    add("visados(CCAA) = suma de iniciadas libres provinciales",
        f"CCAA multiprovinciales con provincias completas: {','.join(completas)}", n, nd, mx, mr)
    iq = ini_m.copy()
    iq.columns = [f"{c[:4]}T{(int(c[5:]) - 1) // 3 + 1}" for c in iq.columns]
    iq = iq.T.groupby(level=0).sum(min_count=3).T
    n = nd = 0
    mx = 0.0
    for t_ in ini.columns:
        if t_ in iq.index:
            dd = (ini[t_] - iq.loc[t_]).dropna()
            n += len(dd)
            nd += int((dd.abs() > 0.5).sum())
            mx = max(mx, float(dd.abs().max()) if len(dd) else 0)
    add("iniciadas T provincial: hechos frente a suma de meses del raw", "43 provincias", n, nd, mx, None)
    for nom, wm, wa in (("iniciadas", ini_m, ini_a), ("terminadas", term_m, term_a)):
        am = anual_desde_mensual(wm, 2008, 2025)
        n = nd = 0
        mx = mr = 0.0
        for y in range(2008, 2026):
            if y in am.columns and y in wa.columns:
                dd = (am[y] - wa[y].reindex(am.index)).dropna()
                n += len(dd)
                nd += int((dd.abs() > 0.5).sum())
                mx = max(mx, float(dd.abs().max()))
                mr = max(mr, float((dd.abs() / wa[y].reindex(dd.index).replace(0, np.nan)).max()))
        add(f"{nom} libres: suma mensual frente a tabla anual", "provincias, CCAA uniprovinciales, Ceuta y Melilla, 2008-2025", n, nd, mx, mr)
    d = pd.read_csv(RAIZ / "data/raw/mivau_v2_iniciadas_terminadas_prov.csv", dtype={"periodo": str})
    for nom, wa, pref in (("iniciadas", ini_a, "viv_libres_iniciadas_anual_nacional"), ("terminadas", term_a, "viv_libres_terminadas_anual_nacional")):
        nac = d[d.serie == pref].set_index("periodo").valor
        nac.index = nac.index.astype(int)
        s = wa.sum(axis=0, min_count=int(len(wa) * 0.9))
        dd = (s - nac.reindex(s.index)).dropna()
        add(f"{nom} libres: suma de unidades frente a total nacional (tabla anual)", f"unidades con dato: {len(wa)}",
            len(dd), int((dd.abs() > 0.5).sum()), float(dd.abs().max()), float((dd.abs() / nac.reindex(dd.index)).max()))
    pe = con.execute("""select periodo p, valor, variable from 'data/base/hechos.parquet'
                        where variable in ('permisos','visados') and nivel='nacional' and metodo_dato!='interpolado'""").fetchdf()
    a = pe[pe.variable == "permisos"].drop_duplicates("p").set_index("p").valor
    b = pe[pe.variable == "visados"].drop_duplicates("p").set_index("p").valor
    j = pd.concat([a, b], axis=1, keys=["permisos", "visados"]).dropna()
    rat = j.permisos / j.visados
    lg = np.log(j.assign(i=[qidx(k) for k in j.index]).set_index("i").sort_index())
    d4 = (lg - lg.shift(4)).dropna()
    r4 = float(np.corrcoef(d4.permisos, d4.visados)[0, 1]) if len(d4) > 5 else float("nan")
    add("permisos (nacional T) frente a visados (nacional T): unidades",
        f"permisos es un índice (2021=100, Eurostat sts_cobp_q según src/build_dataset.py) con unidad declarada «viviendas (visados)» y fuente declarada MIVAU; "
        f"ratio mediano a visados {rat.median():.4f}; correlación de variaciones interanuales log {r4:.2f} (n={len(d4)})",
        len(j), len(j), float((j.permisos - j.visados).abs().max()), float((rat - 1).abs().max()))
    gz = RAIZ / "data/raw/catastro_urbana_municipios.csv.gz"   # versionado
    sin_gz = gz.with_suffix("")   # copia local sin comprimir (no versionada): solo se compara si existe
    y = pd.read_csv(gz, dtype=str)
    x = pd.read_csv(sin_gz, dtype=str) if sin_gz.exists() else y.iloc[0:0]
    comunes = [c for c in x.columns if c in y.columns]
    if sin_gz.exists() and len(x) == len(y):
        xs = x[comunes].fillna("").sort_values(["serie", "periodo"]).reset_index(drop=True)
        ys = y[comunes].fillna("").sort_values(["serie", "periodo"]).reset_index(drop=True)
        nd = int(xs.ne(ys).any(axis=1).sum())
    else:
        nd = -1
    add("Catastro URBANA: .csv frente a .csv.gz (dos copias en data/raw)",
        f"filas {len(x)} / {len(y)}; columnas comunes {len(comunes)} de {x.shape[1]} / {y.shape[1]}", len(x), nd, None, None)
    return pd.DataFrame(filas)


# ----------------------------------------------------------------------------------------------- tarea 3
def sup_t(y: np.ndarray, kmin: int = 3) -> tuple[np.ndarray, np.ndarray]:
    """Estadístico sup-t de cambio de media (ruptura única, fecha desconocida) sobre el último eje; devuelve (stat, k)."""
    t = y.shape[-1]
    mejor = np.zeros(y.shape[:-1])
    kk = np.zeros(y.shape[:-1], int)
    for k in range(kmin, t - kmin + 1):
        a, b = y[..., :k], y[..., k:]
        ssr = ((a - a.mean(-1, keepdims=True)) ** 2).sum(-1) + ((b - b.mean(-1, keepdims=True)) ** 2).sum(-1)
        s = np.sqrt(ssr / (t - 2)) + 1e-12
        st = np.abs(a.mean(-1) - b.mean(-1)) / (s * np.sqrt(1 / k + 1 / (t - k)))
        m = st > mejor
        mejor = np.where(m, st, mejor)
        kk = np.where(m, k, kk)
    return mejor, kk


def rupturas_mivau(term_a, ini_a, prot_a, unid, perms: int = 999) -> tuple[pd.DataFrame, dict]:
    rng = np.random.default_rng(SEED)
    filas, inf = [], {}
    anios = list(range(2008, 2026))
    tt, ii, pp = term_a.reindex(unid)[anios], ini_a.reindex(unid)[anios], prot_a.reindex(unid)[anios]
    series = {"cuota_terminadas_libres": tt / tt.sum(axis=0), "cuota_iniciadas_libres": ii / ii.sum(axis=0),
              "peso_libres_en_libres_mas_protegida": tt / (tt + pp)}
    for nom, w in series.items():
        w = w.dropna(how="any")
        w = w[(w > 0).all(axis=1)] if nom.startswith("cuota") else w[((w > 0) & (w < 1)).all(axis=1)]
        a = w.to_numpy(float)
        y = np.log(a) if nom.startswith("cuota") else np.log(a / (1 - a))
        st, k = sup_t(y)
        idx = rng.permuted(np.tile(np.arange(len(anios)), (perms, y.shape[0], 1)), axis=2)
        yp = np.take_along_axis(np.broadcast_to(y, (perms,) + y.shape), idx, axis=2)
        sp, _ = sup_t(yp)
        crit_fw = float(np.quantile(sp.max(axis=1), 0.95))
        p_u = (sp >= st[None, :]).mean(axis=0)
        for i, u in enumerate(w.index):
            filas.append({"serie": nom, "unidad": u, "ruptura_primer_anio_tramo2": anios[k[i]], "sup_t": float(st[i]),
                          "p_permutacion_unidad": float(p_u[i]), "umbral_fw_95": crit_fw, "supera_umbral_fw": bool(st[i] > crit_fw)})
        inf[nom] = {"unidades": int(len(w)), "umbral_fw_95": crit_fw, "supera_umbral_fw": w.index[st > crit_fw].tolist(),
                    "sup_t_pv_navarra": {u: round(float(st[list(w.index).index(u)]), 2) for u in ("01", "20", "48", "31") if u in w.index}}
    return pd.DataFrame(filas), inf


def rupturas_catastro(con, stock_m: pd.DataFrame, sp: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    ine = pd.read_parquet(RAIZ / "data/base/geo/municipios.parquet", columns=["cod_municipio", "cod_provincia"])
    cat, ine_s = set(stock_m.index), set(ine.cod_municipio)
    cols = list(stock_m.columns)
    filas, prev = [], None
    for y in cols:
        cods = set(stock_m[y].dropna().index)
        filas.append({"ejercicio_fichero": y, "n_municipios": len(cods),
                      "altas_codigo_respecto_anterior": len(cods - prev) if prev else None,
                      "bajas_codigo_respecto_anterior": len(prev - cods) if prev else None,
                      "unidades_residenciales_total": float(stock_m[y].sum())})
        prev = cods
    d = pd.DataFrame(filas)
    saltos, caidas = [None], [None]
    for a, b in zip(cols[:-1], cols[1:], strict=True):
        base = stock_m[a]
        r = (stock_m[b] - base) / base
        saltos.append(int(((r.abs() > 0.10) & (base >= 100)).sum()))
        caidas.append(int(((r < -0.05) & (base >= 100)).sum()))
    d["saltos_municipales_mayor10pct_stock_ge100"] = saltos
    d["caidas_municipales_mayor5pct_stock_ge100"] = caidas
    pv = con.execute("""select periodo p, variable v, sum(valor) s from 'data/base/hechos.parquet'
        where variable in ('catastro_unidades_urbanas_residenciales','catastro_unidades_urbanas_total') group by all""").fetchdf()
    pv = pv.pivot(index="p", columns="v", values="s")
    d["cuota_residencial_sobre_total"] = (pv["catastro_unidades_urbanas_residenciales"] / pv["catastro_unidades_urbanas_total"]).reindex(d.ejercicio_fichero).to_numpy()
    zp = z_filas(np.diff(np.log(sp.to_numpy(float)), axis=1))
    prov_saltos = [{"provincia": sp.index[r], "ejercicio_fichero": cols[c + 1], "z": float(zp[r, c])}
                   for r, c in zip(*np.where(np.abs(zp) > UMBRAL_Z), strict=True)]
    inf = {"municipios_catastro": len(cat), "municipios_ine_2025": len(ine_s),
           "n_en_catastro_no_ine2025": len(cat - ine_s), "en_catastro_y_no_en_ine2025_muestra": sorted(cat - ine_s)[:20],
           "n_ine2025_sin_catastro": len(ine_s - cat),
           "ine2025_sin_catastro_por_provincia": {k: int(v) for k, v in ine[ine.cod_municipio.isin(ine_s - cat)].cod_provincia.value_counts().sort_index().items()},
           "provincias_con_salto_z5_en_crecimiento_stock": prov_saltos,
           "cuota_residencial_min_max": [num(d.cuota_residencial_sobre_total.min()), num(d.cuota_residencial_sobre_total.max())]}
    return d, inf


def censo_vacia(con, prov: pd.DataFrame, cen21: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    h = con.execute("""select territorio_codigo t, desagregacion d, valor from 'data/base/hechos.parquet'
                       where variable='censo2011_viviendas'""").fetchdf()
    h["tipo"] = h.d.str.replace("tipo=", "", regex=False)
    w = h.pivot(index="t", columns="tipo", values="valor")
    d = w.rename(columns={"Total viviendas": "total", "Vivienda familiar": "familiar", "Vivienda colectiva": "colectiva",
                          "Vivienda principal": "principal", "Vivienda no principal": "no_principal",
                          "Vivienda secundaria": "secundaria", "Vivienda vacía": "vacia"}).copy()
    d["resid_total_vs_familiar_mas_colectiva"] = d.total - d.familiar - d.colectiva
    d["resid_familiar_vs_principal_mas_no_principal"] = d.familiar - d.principal - d.no_principal
    d["resid_no_principal_vs_secundaria_mas_vacia"] = d.no_principal - d.secundaria - d.vacia
    d["cuota_vacia_sobre_familiar_2011"] = d.vacia / d.familiar
    d = d.join(cen21)
    d["cuota_no_principal_2011"] = d.no_principal / d.familiar
    d["cuota_no_principal_2021"] = d.nopal2021 / d.tot2021
    d["dif_rel_tot2021_tabla59520_vs_59521"] = d.tot2021_t59520 / d.tot2021 - 1
    d["resid_2021_total_vs_ppal_mas_nopal"] = d.tot2021 - d.ppal2021 - d.nopal2021
    d.index.name = "provincia_ine"
    d = d.loc[d.index.isin(prov.territorio_codigo)]
    v = pd.read_parquet(RAIZ / "data/base/variables.parquet")
    cand = v[v.variable.str.startswith("censo2021") & v.definicion.fillna("").str.contains("vac|secundar", case=False, regex=True)].variable.tolist()
    inf = {"vacia_2011_nacional": num(d.vacia.sum()), "secundaria_2011_nacional": num(d.secundaria.sum()),
           "no_principal_2011_nacional": num(d.no_principal.sum()), "no_principal_2021_nacional": num(d.nopal2021.sum()),
           "principal_2011_nacional": num(d.principal.sum()), "principal_2021_nacional": num(d.ppal2021.sum()),
           "max_abs_resid_no_principal_2011": num(d.resid_no_principal_vs_secundaria_mas_vacia.abs().max()),
           "max_abs_resid_familiar_2011": num(d.resid_familiar_vs_principal_mas_no_principal.abs().max()),
           "max_abs_resid_total_2011": num(d.resid_total_vs_familiar_mas_colectiva.abs().max()),
           "max_abs_dif_rel_tablas_ine_2021_59520_vs_59521": num(d.dif_rel_tot2021_tabla59520_vs_59521.abs().max()),
           "max_abs_resid_2021": num(d.resid_2021_total_vs_ppal_mas_nopal.abs().max()),
           "variables_censo2021_en_base_con_vacia_o_secundaria": cand,
           "vacia_comparable_2011_2021": False}
    return d.reset_index(), inf


# ----------------------------------------------------------------------------------------------- tarea 4
def inventario_fisico() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    v = pd.read_parquet(RAIZ / "data/base/variables.parquet")
    pat = re.compile(r"pendiente|slope|altitud|elevaci|\bmdt\b|natura 2000|protegid|hidro|litoral|corine|siose|r[uú]stic|no urbaniz|"
                     r"clasificaci[oó]n del suelo|superficie municipal|rugosidad", re.I)
    txt = (v.variable.fillna("") + " " + v.definicion.fillna("") + " " + v.fuente.fillna("")).tolist()
    hits = [v.variable.iloc[i] for i, t in enumerate(txt) if pat.search(t)]
    ext = {".tif", ".tiff", ".asc", ".shp", ".gpkg", ".geojson", ".nc", ".hgt", ".img", ".jp2"}
    encontrados = []
    for base in ("data", "src"):
        for dp, dn, fn in os.walk(RAIZ / base):
            dn[:] = sorted(x for x in dn if "sealed" not in x.lower() and x != ".git")
            for f in sorted(fn):
                if Path(f).suffix.lower() in ext or re.search(r"(^|[_\-.])(mdt\d*|slope|siose|corine|natura2000|pendiente)([_\-.]|$)", f, re.I):
                    encontrados.append(str((Path(dp) / f).relative_to(RAIZ)))
    try:
        import geopandas as gpd

        g = gpd.read_parquet(RAIZ / "data/base/geo/municipios.parquet")
        area = g.to_crs("EPSG:6933").area / 1e6
        area_inf = {"municipios": int(len(g)), "area_total_km2_epsg6933": num(area.sum()), "area_mediana_km2": num(area.median()),
                    "geometrias_validas_pct": num(float(g.geometry.is_valid.mean()) * 100)}
    except Exception as e:  # pragma: no cover
        area_inf = {"error": str(e)[:100]}
    filas = [
        ("Pendiente / altitud / MDT por municipio", "no", "-", "Ninguna variable ni fichero ráster (búsqueda en variables.parquet y árbol de ficheros)."),
        ("Superficie municipal (km2)", "derivable", "data/base/geo/municipios.parquet",
         "Polígonos INE 2025 (WGS84, 8.132 municipios): el área se calcula; son límites administrativos, no suelo clasificable."),
        ("Superficie no urbanizable / clasificación del suelo", "no", "-",
         "Solo precio del suelo urbano (MIVAU, tabla 4) y unidades urbanas del Catastro; sin superficie clasificada."),
        ("Suelo protegido (Red Natura 2000, ENP)", "no", "-", "Sin capa ni variable."),
        ("Agua / hidrografía / litoral", "no", "-", "Sin capa; la costa podría derivarse de los límites, no está calculada."),
        ("Usos del suelo (SIOSE, Corine)", "no", "-", "Sin datos."),
        ("Huella edificada", "parcial", "Catastro INSPIRE (hechos: catastro_inspire_*)",
         "Solo València (87 barrios, 1.659 secciones) y 108 municipios en obra_nueva_viviendas_inspire (cota inferior)."),
        ("Viviendas por año de construcción (stock)", "parcial", "catastro_viviendas_por_anio_construccion",
         "Un solo corte (2019), 7.608 municipios; sirve para antigüedad, no para flujo anual."),
        ("Licencias municipales de obra", "no", "-", "Solo iab_n_con_licencia (anuncios con licencia turística, no de obra)."),
        ("Visados de colegios de arquitectos / CSCAE", "no", "-",
         "La variable «visados» es la tabla 3.1 del MIVAU (viviendas libres INICIADAS), no visado de dirección de obra."),
    ]
    inv = pd.DataFrame(filas, columns=["concepto", "existe_en_repositorio", "donde", "observacion"])
    req = pd.DataFrame([
        ("Pendiente y altitud", "MDT05 / MDT25 / MDT200 (IGN-CNIG), Centro de Descargas del CNIG", "CC BY 4.0 (IGN)",
         "Parcial: hojas por formulario web; los servicios INSPIRE de descarga (ATOM/WCS) permiten el acceso en bloque",
         "Estadísticos zonales por municipio con los polígonos del repositorio; MDT25 pesa del orden de GB (no verificado)"),
        ("Usos y cubiertas del suelo", "SIOSE (CNIG/IGN, ediciones 2005-2020), descarga por CCAA", "CC BY 4.0 (IGN)",
         "Sí por ATOM o descarga directa por CCAA (Canarias aparte)", "Series SIOSE no homogéneas entre ediciones: solo sección transversal"),
        ("Usos del suelo europeos", "CORINE Land Cover 1990-2018 (Copernicus CLMS)", "Libre y abierta (Copernicus)",
         "Sí con la API de CLMS; requiere cuenta EU Login", "Resolución de 25 ha: gruesa para municipios pequeños"),
        ("Suelo protegido", "Red Natura 2000 y Espacios Naturales Protegidos (MITECO, EEA)", "Reutilización con cita (MITECO); CC BY 4.0 (EEA)",
         "Sí por descarga directa de capas", "Intersección con límites municipales; no equivale a suelo no urbanizable"),
        ("Clasificación urbanística del suelo", "SIU, Sistema de Información Urbana (MIVAU)", "no verificada",
         "No comprobada", "Es la medida más cercana a «suelo no urbanizable»; cobertura y vintage por comprobar"),
        ("Hidrografía / masas de agua", "BCN y red hidrográfica (CNIG), MITECO", "CC BY 4.0 (IGN); reutilización con cita (MITECO)",
         "Sí (capas por descarga)", "«Agua» como restricción de oferta exige definir el concepto (cuenca, no solo masa de agua)"),
    ], columns=["concepto", "fuente_publica", "licencia_segun_conocimiento_previo_no_verificada", "descarga_automatizable", "nota"])
    return inv, req, {"variables_con_coincidencia": hits, "ficheros_raster_o_vectoriales_encontrados": encontrados[:20],
                      "area_municipal": area_inf}


# ----------------------------------------------------------------------------------------------- tarea 5
def cobertura_municipal(con) -> tuple[pd.DataFrame, dict]:
    q = """select variable, periodo, count(distinct territorio_codigo) n, count(*) filas
           from 'data/base/hechos.parquet' where nivel='municipio' and variable in
           ('catastro_unidades_urbanas_residenciales','catastro_unidades_urbanas_total','obra_nueva_neta_catastro',
            'catastro_titulares_jaxi','catastro_tit_viviendas','catastro_viviendas_por_anio_construccion',
            'catastro_viviendas_por_anio_reforma','obra_nueva_viviendas_inspire','v12_obra_neta','v12_ratio_obra_hogares')
           group by all order by 1,2"""
    c = con.execute(q).fetchdf()
    nz = con.execute("""select periodo, count(distinct territorio_codigo) n from 'data/base/hechos.parquet'
        where variable='obra_nueva_neta_catastro' and valor!=0 group by 1 order by 1""").fetchdf()
    c["universo_ine_2025"] = 8132
    c["pct_universo"] = (c.n / 8132 * 100).round(1)
    c["observacion"] = ""
    c.loc[c.variable == "obra_nueva_neta_catastro", "observacion"] = "diferencia de dos ficheros; sin País Vasco ni Navarra"
    c.loc[c.variable.str.startswith("v12_"), "observacion"] = "v12_obra_neta: dos periodos (2011-2021 y 2021-2025); municipios con hogares estimables"
    extra = []
    f = RAIZ / "data/raw/v11/ine_censo2021/viviendas_muestra_municipio.csv.gz"
    m = pd.read_csv(f, dtype={"cod_municipio": str}, usecols=["cod_municipio"]).cod_municipio.nunique()
    extra.append({"variable": "censo2021_viviendas_muestra_municipio", "periodo": "2021", "n": m, "filas": None,
                  "universo_ine_2025": 8132, "pct_universo": round(m / 8132 * 100, 1), "observacion": "muestra (no es recuento)"})
    for nom, per in (("iniciadas", "2008-2026"), ("terminadas", "2008-2026"), ("visados", "2008-2026"), ("parque estimado", "2001-2025")):
        extra.append({"variable": f"MIVAU {nom}", "periodo": per, "n": 0, "filas": None, "universo_ine_2025": 8132, "pct_universo": 0.0,
                      "observacion": "solo nacional, CCAA y provincia (sin dato municipal)"})
    c = pd.concat([c, pd.DataFrame(extra)], ignore_index=True)
    return c, {"municipios_con_obra_neta_distinta_de_cero_por_anio": {k: int(v) for k, v in zip(nz.periodo, nz.n, strict=True)}}


# ----------------------------------------------------------------------------------------------- principal
def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    os.chdir(RAIZ)
    con = duckdb.connect()
    prov, mapa = territorios()
    unid = prov.territorio_codigo.tolist()
    ini_m, i_inf = leer_raw("mivau_visados.csv", "viv_libres_iniciadas_", mapa)
    term_m, t_inf = leer_raw("mivau_fin_obra.csv", "viv_libres_terminadas_", mapa)
    prot_m, p_inf = leer_raw("mivau_v2_protegida.csv", "prot_definitiva_mensual_", mapa)
    ini_a = anual_desde_mensual(ini_m, 2008, 2025)
    term_a = anual_desde_mensual(term_m, 2008, 2025)
    prot_a = anual_desde_mensual(prot_m, 2008, 2025)
    d2 = pd.read_csv(RAIZ / "data/raw/mivau_v2_iniciadas_terminadas_prov.csv", dtype={"periodo": str})
    anual_tab = {}
    for nom, pref in (("ini", "viv_libres_iniciadas_anual_"), ("term", "viv_libres_terminadas_anual_")):
        x = d2[d2.serie.str.startswith(pref) & (d2.nivel != "nacional")].drop_duplicates(["serie", "periodo"])
        x = a_unidad(x, mapa).dropna(subset=["u"])
        w = x.pivot(index="u", columns="periodo", values="valor")
        w.columns = w.columns.astype(int)
        anual_tab[nom] = w
    cen11 = pd.read_parquet(HECHOS, columns=["territorio_codigo", "variable", "desagregacion", "valor"],
                            filters=[("variable", "=", "censo2011_viviendas")])
    cen11["tipo"] = cen11.desagregacion.str.replace("tipo=", "", regex=False)
    cen11 = cen11.pivot(index="territorio_codigo", columns="tipo", values="valor").rename(
        columns={"Total viviendas": "total", "Vivienda familiar": "familiar"})
    cen21 = censo2021(prov)

    extra = {"prot_definitiva_anual(raw)": (prot_a.copy(), "A"), "terminadas_libres_anual(raw, unidad provincial)": (term_a.copy(), "A"),
             "iniciadas_libres_anual(raw, unidad provincial)": (ini_a.copy(), "A")}
    res_m, det_m, inf_m = atipicos_mivau(con, extra)
    res_m.to_csv(OUT / "atipicos_mivau_resumen.csv", index=False)
    det_m.sort_values(["variable", "nivel", "territorio", "periodo"], kind="stable").to_csv(OUT / "atipicos_mivau_detalle.csv", index=False)
    por_anio, det_c, inf_c, stock_m = atipicos_catastro(con)
    por_anio.to_csv(OUT / "atipicos_catastro_por_anio.csv", index=False)
    det_c.to_csv(OUT / "atipicos_catastro_detalle_top2000.csv", index=False)

    fs, sp = flujo_stock(prov, term_m, prot_m, stock_m, cen11, cen21)
    fs.to_csv(OUT / "coherencia_flujo_stock_provincia.csv", index=False)
    r_fs = resumen_flujo_stock(fs)
    ca, c_inf = coherencia_anual(sp, term_a, prot_a, unid)
    ca.to_csv(OUT / "coherencia_anual_catastro_mivau.csv", index=False)
    pq, q_inf = parque_vs_censo(mapa, cen11, cen21)
    pq.to_csv(OUT / "coherencia_parque_censo.csv", index=False)
    cf = coherencia_fuentes(con, prov, ini_m, term_m, anual_tab["ini"], anual_tab["term"])
    cf.to_csv(OUT / "coherencia_fuentes.csv", index=False)

    rm, rm_inf = rupturas_mivau(anual_tab["term"], anual_tab["ini"], prot_a, unid)
    rm.to_csv(OUT / "rupturas_mivau.csv", index=False)
    rc, rc_inf = rupturas_catastro(con, stock_m, sp)
    rc.to_csv(OUT / "rupturas_catastro.csv", index=False)
    cv, cv_inf = censo_vacia(con, prov, cen21)
    cv.to_csv(OUT / "rupturas_censo_vacia.csv", index=False)

    inv, req, f_inf = inventario_fisico()
    inv.to_csv(OUT / "inventario_restricciones_fisicas.csv", index=False)
    req.to_csv(OUT / "datos_publicos_necesarios_P1.csv", index=False)

    cob, cob_inf = cobertura_municipal(con)
    cob.to_csv(OUT / "cobertura_municipal_por_anio.csv", index=False)

    diag = {
        "convenciones": {"umbral_z_robusto": UMBRAL_Z, "umbral_dif_rel": UMBRAL_REL, "seed": SEED,
                         "dif_rel": "flujo / variación de stock - 1", "ventana_censo": "meses 2011-11 a 2021-10",
                         "catastro_convencion_A": "fichero t = stock a 31-12-(t-1) según el campo fecha del origen; flujo 2012-2021 frente a fichero 2022 - 2012",
                         "catastro_convencion_B": "etiqueta de hechos (periodo t = 31-12-t); flujo 2013-2021 frente a fichero 2021 - 2012"},
        "t1_atipicos": {"mivau_resumen": res_m.to_dict("records"), "mivau_aux": inf_m, "catastro": inf_c},
        "t2_flujo_stock": {"resumen": r_fs, "alineacion_temporal_catastro": c_inf, "parque_vs_censo": q_inf,
                           "coherencia_fuentes": cf.to_dict("records")},
        "t3_rupturas": {"mivau_permutacion": rm_inf, "catastro": rc_inf, "censo_vacia": cv_inf,
                        "mivau_nombres_sin_codigo_raw": {"iniciadas": i_inf["sin_codigo"], "terminadas": t_inf["sin_codigo"],
                                                         "protegida": p_inf["sin_codigo"]}},
        "meses_ausentes_en_raw": {"iniciadas": meses_ausentes(ini_m), "terminadas": meses_ausentes(term_m), "protegida": meses_ausentes(prot_m)},
        "t4_fisico": f_inf,
        "t5_cobertura": cob_inf,
    }
    resultado = {
        "rama": "V15-F1.2-oferta_parque",
        "pregunta": "¿Son coherentes, completas y estables las series de oferta y parque (MIVAU, Catastro, Censos 2011/2021) para P1 y P7?",
        "capa": "C4",
        "datos": "MIVAU iniciadas/terminadas libres y calificaciones definitivas (provincia, CCAA); MIVAU parque estimado; Catastro URBANA 2012-2026 (municipio); Censos 2011 y 2021 (provincia); geometría municipal INE 2025",
        "N": int(len(unid)),
        "metodo": "auditoría descriptiva: z robusto (mediana, MAD), coherencia flujo-stock, ruptura sup-t con permutación (999, SEED=20261010), inventario y cobertura",
        "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO",
        "diagnosticos": diag,
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": "Sin efectos ni regresiones. Cruces solo por código INE. Interpolados excluidos de los atípicos. La regularización catastral 2013-2017 y el origen del parque estimado del MIVAU se citan de la documentación del repositorio (docs/v12) y no se han verificado aquí.",
    }
    (OUT / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("OK", OUT)


if __name__ == "__main__":
    main()

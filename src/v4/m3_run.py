"""M3 ¿Se puede construir donde hace falta? Determinista y sin red (SEED=20261010).

Entradas: data/raw/v4/catastro_solares_municipios.csv.gz (de m3_fetch.py), mivau_valor_tasado_*, mivau_v2_suelo,
mivau_v2_iniciadas_terminadas_prov, eurostat_costes, eurostat_produccion_construccion y output/v4/M1/tablas.
Salidas: output/v4/M3/.   SMOKE=1 usa una submuestra (10 provincias, 60 municipios) y escribe en output/v4/M3/_smoke.

UMBRALES Y SUPUESTOS DECLARADOS ANTES DE CLASIFICAR (docs/v4/decisiones.md, M3):
  clases: 4 si déficit <= 0; 3 si brecha <= 0; 2 si precio > r*(coste + suelo repercutido); 1 si brecha > 0, no 2 y solares
  suficientes; 5 (clase añadida) si brecha moderada pero solares insuficientes; 9 si falta el dato de solares.
  multiverso: margen {15,20,25} %; edificabilidad {0,8; 1,2; 1,6} m2/m2; coste {900; 1.200; 1.500} EUR/m2 construido
  (supuesto externo NO verificado: ninguna fuente de coste en nivel accesible); suelo {todos los municipios; >50.000 hab.};
  r {1,25; 1,5}; viviendas por solar {5; 10; 20}; variante de déficit M1 (periodo y, en provincias, min/mediana/max).
  Central: margen 20 %, edif. 1,2, coste 1.200, suelo todos, r 1,25, 10 viviendas/solar, 2021-2025, mediana.
  C2 solo si la clase modal aparece en >= 80 % de las especificaciones válidas; si no, C4.
"""
from __future__ import annotations

import itertools
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from econ_utils import Registry  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
SMOKE = os.environ.get("SMOKE") == "1"
OUT = ROOT / "output" / "v4" / "M3" / ("_smoke" if SMOKE else "")
RAW = ROOT / "data" / "raw"
M1T = ROOT / "output" / "v4" / "M1" / "tablas"

MARGEN = [0.15, 0.20, 0.25]
EDIF = [0.8, 1.2, 1.6]
COSTE = [900.0, 1200.0, 1500.0]
SUELO_V = [0, 1]          # 0 = todos los municipios; 1 = municipios > 50.000 hab. (si hay dato)
RATIO = [1.25, 1.5]
VIV_SOLAR = [5, 10, 20]
CENTRAL = dict(m=0.20, e=1.2, c=1200.0, s=0, r=1.25, v=10)
UMBRAL_C2 = 0.80
# Sin fuente verificable de coste en nivel (PEM/m2, licencias, MBC; Catastro sin superficie construida): todo es C4.
COSTE_VERIFICADO = False
ETIQ = {1: "1 falta y hay suelo rentable", 2: "2 falta y brecha regulatoria", 3: "3 falta pero no rentable",
        4: "4 no falta", 5: "5 falta, brecha moderada, solares insuficientes (clase añadida)",
        9: "9 indeterminada (sin dato de solares)"}
CODIGOS = [1, 2, 3, 4, 5, 9]
UNI_PROV = {"07": "balears illes", "28": "madrid comunidad de", "30": "murcia region de",
            "31": "navarra comunidad foral de", "33": "asturias principado de", "39": "cantabria",
            "26": "rioja la"}
CIUDAD = {"51": "ceuta", "52": "melilla"}
ALIAS_PROV = {"guipuzcoa": "gipuzkoa", "vizcaya": "bizkaia", "alava": "araba/alava", "avila": "avila"}
ALIAS_MUN = {"Almazora/Almassora": "12009", "Burriana": "12032", "Calpe/Calp": "03047", "Castellón de la Plana": "12040",
             "Mahón": "07032", "Palma de Mallorca": "07040", "Puerto de Santa María": "11027",
             "San Cristóbal Laguna": "38023", "San Sebastián/Donostia": "20069", "San Vicente del Raspeig": "03122",
             "Santa Coloma Gramanet": "08245", "Santa Cruz deTenerife": "38038", "Villarreal/Vila-real": "12135",
             "Vitoria": "01059"}


def k(s) -> str:
    s = unicodedata.normalize("NFD", str(s))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    s = " ".join(re.sub(r"[^a-z0-9/ ]", " ", s).split())
    return ALIAS_PROV.get(s, s)


def media_ultimos(df: pd.DataFrame, periodos: list[str], minimo: int) -> pd.Series:
    d = df[df.periodo.isin(periodos)].groupby(["nivel", "kk"]).valor.agg(["mean", "count"])
    return d[d["count"] >= minimo]["mean"]


def buscar(s: pd.Series, cod: str, nombre: str, ciudad_nivel: str = "ciudad_autonoma") -> float:
    if ("provincia", k(nombre)) in s.index:
        return float(s[("provincia", k(nombre))])
    if cod in UNI_PROV and ("ccaa", UNI_PROV[cod]) in s.index:
        return float(s[("ccaa", UNI_PROV[cod])])
    if cod in UNI_PROV and ("ccaa", UNI_PROV[cod].replace("comunidad foral de", "com foral de")) in s.index:
        return float(s[("ccaa", UNI_PROV[cod].replace("comunidad foral de", "com foral de"))])
    if cod in CIUDAD and (ciudad_nivel, CIUDAD[cod]) in s.index:
        return float(s[(ciudad_nivel, CIUDAD[cod])])
    if cod in CIUDAD and (ciudad_nivel, "ceuta y melilla") in s.index:
        return float(s[(ciudad_nivel, "ceuta y melilla")])
    return float("nan")


# ------------------------------------------------------------------ datos
def cargar():
    prov = pd.read_csv(M1T / "M1_provincias.csv", dtype={"cod_prov": str})
    nombres = prov[["cod_prov", "provincia"]].drop_duplicates().set_index("cod_prov").provincia
    mun = pd.read_csv(M1T / "M1_municipios.csv", dtype={"cod_mun": str, "cod_prov": str})
    cat = pd.read_csv(RAW / "v4" / "catastro_solares_municipios.csv.gz", dtype={"cod_mun": str})
    c26 = cat[cat.anio == cat.anio.max()].set_index("cod_mun")
    # precio provincial (nivel provincia, ccaa, ciudad autónoma)
    vp = pd.read_csv(RAW / "mivau_valor_tasado_nacional_ccaa_prov.csv")
    vp = vp[vp.nivel.isin(["provincia", "ccaa", "ciudad_autonoma"])].copy()
    vp["kk"] = vp.territorio.map(k)
    p4 = ["2025T3", "2025T4", "2026T1", "2026T2"]
    precio_p = media_ultimos(vp, p4, 3)
    # suelo
    sv = pd.read_csv(RAW / "mivau_v2_suelo.csv")
    sv["kk"] = sv.territorio.map(k)
    q8 = ["2024T3", "2024T4", "2025T1", "2025T2", "2025T3", "2025T4", "2026T1", "2026T2"]
    suelo_t = media_ultimos(sv[sv.serie.str.startswith("suelo_pm2_m50k") == False], q8, 4)  # noqa: E712
    suelo_5 = media_ultimos(sv[sv.serie.str.startswith("suelo_pm2_m50k")], q8, 4)
    # precio municipal
    vm = pd.read_csv(RAW / "mivau_valor_tasado_municipios.csv")
    vm = vm[vm.periodo.isin(p4)].groupby("territorio").valor.agg(["mean", "count"])
    vm = vm[vm["count"] >= 3]["mean"]
    # terminadas libres anuales
    it = pd.read_csv(RAW / "mivau_v2_iniciadas_terminadas_prov.csv")
    it = it[it.serie.str.startswith("viv_libres_terminadas_anual")].copy()
    it["kk"] = it.territorio.map(k)
    return prov, nombres, mun, c26, precio_p, suelo_t, suelo_5, vm, it


def tabla_provincias(prov, nombres, c26, precio_p, suelo_t, suelo_5, it):
    filas = []
    for cod, nom in nombres.items():
        sub = c26[c26.index.str[:2] == cod]
        sol, res = sub.uu_solar.sum(), sub.uu_res.sum()
        fila = dict(cod_prov=cod, provincia=nom, precio=buscar(precio_p, cod, nom),
                    suelo_todos=buscar(suelo_t, cod, nom, "ccaa"), suelo_m50k=buscar(suelo_5, cod, nom, "ccaa"),
                    uu_solar=sol if len(sub) else np.nan, uu_res=res if len(sub) else np.nan)
        if cod in CIUDAD:
            fila["suelo_todos"] = buscar(suelo_t, cod, nom, "ciudad_autonoma")
            fila["suelo_m50k"] = buscar(suelo_5, cod, nom, "ciudad_autonoma")
        # terminadas libres: media 2021-2025 y máximo histórico
        s = float("nan")
        serie = None
        for nivel, kk in (("provincia", k(nom)), ("ccaa", UNI_PROV.get(cod, "")), ("ciudad_autonoma", CIUDAD.get(cod, ""))):
            x = it[(it.nivel == nivel) & (it.kk == kk)]
            if len(x):
                serie = x.set_index("periodo").valor
                break
        if serie is not None:
            serie.index = serie.index.astype(int)
            s = serie.loc[2021:2025].mean()
            fila.update(term_media_2021_25=s, term_max_hist=serie.max(), term_max_anio=int(serie.idxmax()))
        filas.append(fila)
    t = pd.DataFrame(filas)
    t["suelo_m50k"] = t.suelo_m50k.fillna(t.suelo_todos)
    for c in ("term_media_2021_25", "term_max_hist"):
        if c not in t:
            t[c] = np.nan
    return t


def deficit_prov(prov):
    out = {}
    for per in ("2012-2025", "2021-2025"):
        p = prov[prov.periodo == per].set_index("cod_prov")
        for stat, col in (("min", "min"), ("mediana", "mediana"), ("max", "max")):
            out[(per, stat)] = p[col]
    capa = prov[prov.periodo == "2021-2025"].set_index("cod_prov").capa
    return out, capa


# ------------------------------------------------------------------ multiverso
def rejilla():
    g = list(itertools.product(MARGEN, EDIF, COSTE, SUELO_V, RATIO, VIV_SOLAR))
    a = np.array(g)
    return a  # columnas m, e, c, s, r, v


def clasificar(P, S0, S1, SOL, DEF, grid):
    """P, S0, S1, SOL, DEF: vectores (U,). Devuelve (U,S) códigos de clase y brecha (U,S); 0 = sin dato."""
    m, e, c, s, r, v = (grid[:, i][None, :] for i in range(6))
    Pm = P[:, None]
    S = np.where(s == 1, S1[:, None], S0[:, None])
    rep = S / e
    brecha = Pm - c * (1 + m) - rep
    cob = SOL[:, None] * v / np.where(DEF[:, None] > 0, DEF[:, None], np.nan)
    cls = np.full(brecha.shape, 0)
    d = DEF[:, None]
    ok = ~np.isnan(brecha) & ~np.isnan(d)
    cls = np.where(ok & (d <= 0), 4, cls)
    falta = ok & (d > 0)
    cls = np.where(falta & (brecha <= 0), 3, cls)
    reg = falta & (brecha > 0) & (Pm > r * (c + rep))
    cls = np.where(reg, 2, cls)
    mod = falta & (brecha > 0) & ~reg
    sol_nd = np.isnan(cob)
    cls = np.where(mod & sol_nd, 9, cls)
    cls = np.where(mod & ~sol_nd & (cob >= 1), 1, cls)
    cls = np.where(mod & ~sol_nd & (cob < 1), 5, cls)
    return cls, brecha


def multiverso(P, S0, S1, SOL, defs: dict, grid):
    """defs: {variante: vector (U,)}. Devuelve cls (U, S*V), brechas (U,S) y orden de variantes."""
    cs, bs = [], []
    for _, dv in defs.items():
        c, b = clasificar(P, S0, S1, SOL, dv, grid)
        cs.append(c)
        bs.append(b)
    return np.concatenate(cs, axis=1), bs[0]


def resumen_clases(cls):
    valido = (cls > 0).sum(1)
    cuentas = np.stack([(cls == c).sum(1) for c in CODIGOS], axis=1)
    idx = cuentas.argmax(1)
    modal = np.array(CODIGOS)[idx]
    share = np.where(valido > 0, cuentas.max(1) / np.maximum(valido, 1), np.nan)
    modal = np.where(valido == 0, 0, modal)
    return modal, share, valido, cuentas


def central_idx(grid):
    for i, g in enumerate(grid):
        if np.allclose(g, [CENTRAL["m"], CENTRAL["e"], CENTRAL["c"], CENTRAL["s"], CENTRAL["r"], CENTRAL["v"]]):
            return i
    raise RuntimeError


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "tablas").mkdir(exist_ok=True)
    (OUT / "figuras").mkdir(exist_ok=True)
    reg = Registry(OUT / "registro.csv")
    prov, nombres, mun, c26, precio_p, suelo_t, suelo_5, vm, it = cargar()
    grid = rejilla()
    ci = central_idx(grid)

    # ============ provincias
    tp = tabla_provincias(prov, nombres, c26, precio_p, suelo_t, suelo_5, it)
    dprov, capa_def = deficit_prov(prov)
    tp = tp.set_index("cod_prov")
    if SMOKE:
        tp = tp.iloc[:10]
    defs_p = {kk: v.reindex(tp.index).to_numpy(float) for kk, v in dprov.items()}
    cls_p, _ = multiverso(tp.precio.to_numpy(float), tp.suelo_todos.to_numpy(float), tp.suelo_m50k.to_numpy(float),
                          tp.uu_solar.to_numpy(float), defs_p, grid)
    modal_p, share_p, valid_p, cnt_p = resumen_clases(cls_p)
    nS = len(grid)
    # brecha (sin déficit) rango en multiverso
    _, br_p = clasificar(tp.precio.to_numpy(float), tp.suelo_todos.to_numpy(float), tp.suelo_m50k.to_numpy(float),
                         tp.uu_solar.to_numpy(float), defs_p[("2021-2025", "mediana")], grid)
    # central
    c_central = np.array([clasificar(tp.precio.to_numpy(float), tp.suelo_todos.to_numpy(float),
                                     tp.suelo_m50k.to_numpy(float), tp.uu_solar.to_numpy(float),
                                     defs_p[("2021-2025", "mediana")], grid)[0][i, ci] for i in range(len(tp))])
    dm = defs_p[("2021-2025", "mediana")]
    # estabilidad de la brecha (sin déficit): clase de brecha {<=0, moderada, regulatoria}
    out_p = pd.DataFrame({
        "cod_prov": tp.index, "provincia": tp.provincia.values, "precio_eur_m2": tp.precio.values,
        "suelo_eur_m2": tp.suelo_todos.values, "deficit_2021_2025_mediana": dm,
        "uu_solar": tp.uu_solar.values, "cobertura_solares_10viv": tp.uu_solar.values * 10 / np.where(dm > 0, dm, np.nan),
        "brecha_central": br_p[:, ci] if br_p.shape[1] > ci else np.nan,
        "brecha_min": np.nanmin(br_p, 1), "brecha_max": np.nanmax(br_p, 1),
        "brecha_p10": np.nanpercentile(br_p, 10, axis=1), "brecha_p90": np.nanpercentile(br_p, 90, axis=1),
        "pct_brecha_positiva": np.nanmean(br_p > 0, axis=1) * 100,
        "clase_central": c_central, "clase_modal": modal_p, "estabilidad_pct": share_p * 100,
        "n_especificaciones": valid_p,
    })
    for j, c in enumerate(CODIGOS):
        out_p[f"pct_clase_{c}"] = cnt_p[:, j] / np.maximum(valid_p, 1) * 100
    out_p["capa_fuente_deficit"] = capa_def.reindex(out_p.cod_prov).values
    out_p["estable_80"] = out_p.estabilidad_pct >= UMBRAL_C2 * 100
    out_p["capa"] = np.where(out_p.estable_80 & COSTE_VERIFICADO, "C2", "C4")
    out_p["capa_efectiva"] = np.where((out_p.capa == "C2") & (out_p.capa_fuente_deficit.isin(["C1", "C2"])), "C2", "C4")
    out_p["clase_etiqueta"] = out_p.clase_modal.map(ETIQ)
    out_p.to_csv(OUT / "clasificacion_provincias.csv", index=False, float_format="%.3f")

    # ============ municipios
    m = mun[mun.deficit_valido].copy()
    dm_m = {per: m[m.periodo == per].set_index("cod_mun").deficit for per in ("2012-2025", "2021-2025")}
    base = mun[mun.periodo == "2021-2025"].drop_duplicates("cod_mun").set_index("cod_mun")
    # emparejar valor tasado municipal con cod_mun por nombre
    mk = base.assign(kk=base.municipio.map(k)).reset_index()
    vmd = vm.reset_index()
    vmd["kk"] = vmd.territorio.map(k)
    vmd["cod_mun"] = vmd.territorio.map(ALIAS_MUN)
    vmd = vmd.merge(mk[["kk", "cod_mun"]].rename(columns={"cod_mun": "cod_mun_n"}).drop_duplicates("kk", keep=False),
                    on="kk", how="left")
    vmd["cod_mun"] = vmd.cod_mun.fillna(vmd.cod_mun_n)
    vmd = vmd.dropna(subset=["cod_mun"]).drop_duplicates("cod_mun").set_index("cod_mun")
    cods = sorted(set(dm_m["2021-2025"].index) | set(dm_m["2012-2025"].index))
    um = pd.DataFrame(index=cods)
    um["municipio"] = base.municipio.reindex(cods).values
    um["cod_prov"] = [c[:2] for c in cods]
    um["pob_2021"] = base.pob_2021.reindex(cods).values
    pmun = vmd["mean"].reindex(cods)
    um["precio_fuente"] = np.where(pmun.notna(), "municipal", "provincial_proxy")
    um["precio"] = np.where(pmun.notna(), pmun, tp.precio.reindex(um.cod_prov).values if not SMOKE else np.nan)
    if SMOKE:
        um = um[um.precio.notna()].iloc[:60]
        cods = list(um.index)
    tpf = tabla_provincias(prov, nombres, c26, precio_p, suelo_t, suelo_5, it).set_index("cod_prov")
    um["precio"] = np.where(um.precio_fuente == "municipal", um.precio, tpf.precio.reindex(um.cod_prov).values)
    um["suelo_todos"] = tpf.suelo_todos.reindex(um.cod_prov).values
    um["suelo_m50k"] = np.where(um.pob_2021 >= 50000, tpf.suelo_m50k.reindex(um.cod_prov).values, um.suelo_todos)
    um["uu_solar"] = c26.uu_solar.reindex(um.index).values
    um["uu_res"] = c26.uu_res.reindex(um.index).values
    defs_m = {per: dm_m[per].reindex(um.index).to_numpy(float) for per in dm_m}
    cls_m, _ = multiverso(um.precio.to_numpy(float), um.suelo_todos.to_numpy(float), um.suelo_m50k.to_numpy(float),
                          um.uu_solar.to_numpy(float), defs_m, grid)
    modal_m, share_m, valid_m, cnt_m = resumen_clases(cls_m)
    d21 = defs_m["2021-2025"]
    _, br_m = clasificar(um.precio.to_numpy(float), um.suelo_todos.to_numpy(float), um.suelo_m50k.to_numpy(float),
                         um.uu_solar.to_numpy(float), d21, grid)
    cen_m = clasificar(um.precio.to_numpy(float), um.suelo_todos.to_numpy(float), um.suelo_m50k.to_numpy(float),
                       um.uu_solar.to_numpy(float), d21, grid)[0][:, ci]
    out_m = pd.DataFrame({
        "cod_mun": um.index, "municipio": um.municipio.values, "cod_prov": um.cod_prov.values,
        "pob_2021": um.pob_2021.values, "precio_fuente": um.precio_fuente.values, "precio_eur_m2": um.precio.values,
        "suelo_eur_m2": um.suelo_todos.values, "deficit_2021_2025": d21, "deficit_2012_2025": defs_m["2012-2025"],
        "uu_solar": um.uu_solar.values, "uu_res": um.uu_res.values,
        "brecha_central": br_m[:, ci], "brecha_min": np.nanmin(br_m, 1), "brecha_max": np.nanmax(br_m, 1),
        "pct_brecha_positiva": np.nanmean(br_m > 0, axis=1) * 100,
        "clase_central": cen_m, "clase_modal": modal_m, "estabilidad_pct": share_m * 100, "n_especificaciones": valid_m,
    })
    for j, c in enumerate(CODIGOS):
        out_m[f"pct_clase_{c}"] = cnt_m[:, j] / np.maximum(valid_m, 1) * 100
    out_m["capa_fuente_deficit"] = "C4"   # M1: todos los déficits municipales son C4
    est = out_m.estabilidad_pct >= UMBRAL_C2 * 100
    out_m["estable_80"] = est
    out_m["capa"] = np.where(est & (out_m.precio_fuente == "municipal") & COSTE_VERIFICADO, "C2", "C4")
    out_m["capa_efectiva"] = "C4"
    out_m["clase_etiqueta"] = out_m.clase_modal.map(ETIQ)
    out_m.to_csv(OUT / "clasificacion_municipios.csv", index=False, float_format="%.3f")

    # ============ registro (una fila por especificación)
    def log_spec(fase, cls, nombres_def, n_unid):
        for vi, dn in enumerate(nombres_def):
            for si, g in enumerate(grid):
                col = cls[:, vi * nS + si]
                cnt = {c: int((col == c).sum()) for c in CODIGOS}
                reg.log(fase, f"{fase}_{'-'.join(map(str, dn)) if isinstance(dn, tuple) else dn}_{si:03d}",
                        "brecha=P-c(1+m)-suelo/e; clases 1-5,9",
                        "2021", "2026", n_unid, np.nan, np.nan, np.nan,
                        notas=f"m={g[0]};e={g[1]};c={g[2]};suelo={int(g[3])};r={g[4]};viv/solar={int(g[5])};"
                              f"deficit={dn};clases={json.dumps(cnt)}")
    log_spec("M3_prov", cls_p, list(dprov.keys()), len(tp))
    log_spec("M3_mun", cls_m, list(defs_m.keys()), len(um))
    reg.flush()

    # ============ tablas de apoyo
    tp_out = tp.reset_index()
    tp_out["deficit_anual_2021_2025_mediana"] = dm / 5
    tp_out["deficit_anual_sobre_terminadas_2021_25"] = tp_out.deficit_anual_2021_2025_mediana / tp_out.term_media_2021_25
    tp_out["term_media_sobre_max_hist"] = tp_out.term_media_2021_25 / tp_out.term_max_hist
    tp_out["deficit_anual_sobre_max_hist"] = tp_out.deficit_anual_2021_2025_mediana / tp_out.term_max_hist
    tp_out.to_csv(OUT / "tablas" / "M3_capacidad_provincias.csv", index=False, float_format="%.3f")
    out_p[["cod_prov", "provincia", "precio_eur_m2", "suelo_eur_m2", "brecha_central", "brecha_min", "brecha_max",
           "brecha_p10", "brecha_p90", "pct_brecha_positiva"]].to_csv(OUT / "tablas" / "M3_brecha_provincias.csv",
                                                                     index=False, float_format="%.2f")
    out_m[["cod_mun", "municipio", "precio_fuente", "precio_eur_m2", "brecha_central", "brecha_min", "brecha_max",
           "pct_brecha_positiva"]].to_csv(OUT / "tablas" / "M3_brecha_municipios.csv", index=False, float_format="%.2f")
    sol = c26.copy()
    sol["cod_prov"] = sol.index.str[:2]
    nac = sol[["uu_solar", "uu_res", "v_cat_solar", "parcelas_urb", "superf_urb"]].sum()
    pd.DataFrame([nac]).to_csv(OUT / "tablas" / "M3_solares_nacional_catastro.csv", index=False)
    # coste: índices Eurostat (solo variación; no son niveles)
    ec = pd.read_csv(RAW / "eurostat_costes.csv")
    ep = pd.read_csv(RAW / "eurostat_produccion_construccion.csv")
    idx = pd.concat([ec[["periodo", "valor"]].assign(serie="coste_construccion_residencial_I21"),
                     ep[["periodo", "valor"]].assign(serie="produccion_construccion_I21")])
    idx.to_csv(OUT / "tablas" / "M3_indices_construccion_eurostat.csv", index=False)
    # estabilidad por clase
    est_tab = []
    for nom, df in (("provincias", out_p), ("municipios", out_m)):
        for c in CODIGOS:
            x = df[df.clase_modal == c]
            est_tab.append(dict(nivel=nom, clase=c, etiqueta=ETIQ[c], n=len(x),
                                n_estables_80=int((x.estabilidad_pct >= 80).sum()),
                                estabilidad_mediana_pct=float(x.estabilidad_pct.median()) if len(x) else np.nan))
    pd.DataFrame(est_tab).to_csv(OUT / "tablas" / "M3_estabilidad_por_clase.csv", index=False, float_format="%.1f")

    # ============ figuras
    fig, ax = plt.subplots(figsize=(8, 11))
    o = out_p.dropna(subset=["brecha_central"]).sort_values("brecha_central")
    col = {1: "tab:green", 2: "tab:red", 3: "tab:blue", 4: "tab:gray", 5: "tab:orange", 9: "tab:purple", 0: "black"}
    ax.barh(o.provincia, o.brecha_central, color=[col[c] for c in o.clase_modal])
    ax.errorbar(o.brecha_central, o.provincia, xerr=[o.brecha_central - o.brecha_p10, o.brecha_p90 - o.brecha_central],
                fmt="none", ecolor="k", lw=0.7)
    ax.axvline(0, color="k", lw=0.8)
    ax.set_xlabel("Brecha precio - coste (EUR/m2); barra: central; bigote: p10-p90 del multiverso")
    ax.set_title("M3: brecha por provincia (color = clase modal)")
    ax.tick_params(axis="y", labelsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "figuras" / "M3_brecha_provincias.png", dpi=110)
    plt.close(fig)
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.5))
    for a, (nom, df) in zip(axs, (("provincias", out_p), ("municipios", out_m)), strict=True):
        a.hist(df.estabilidad_pct.dropna(), bins=20, range=(0, 100), color="tab:gray")
        a.axvline(80, color="r", ls="--")
        a.set_title(f"Estabilidad de la clase modal: {nom} (n={len(df)})")
        a.set_xlabel("% de especificaciones en la clase modal")
    fig.tight_layout()
    fig.savefig(OUT / "figuras" / "M3_estabilidad_clase.png", dpi=110)
    plt.close(fig)

    # ============ hechos, resultado y ficha
    escribir_json(out_p, out_m, nac, tp_out, grid, capa_def)
    print("ok", OUT, "prov", len(out_p), "mun", len(out_m))


def conteo(df):
    return {ETIQ[c]: int((df.clase_modal == c).sum()) for c in CODIGOS}


def escribir_json(out_p, out_m, nac, tp_out, grid, capa_def) -> None:
    pe = out_p[out_p.estabilidad_pct >= 80]
    me = out_m[out_m.estabilidad_pct >= 80]
    pp = out_p.dropna(subset=["brecha_central"])
    ext_alto = pp.nlargest(3, "brecha_central")[["provincia", "brecha_central"]].values.tolist()
    ext_bajo = pp.nsmallest(3, "brecha_central")[["provincia", "brecha_central"]].values.tolist()
    rng = (float(pp.brecha_central.min()), float(pp.brecha_central.max()))
    # ficha M3-V1
    fal = out_p[out_p.deficit_2021_2025_mediana > 0]
    cob = {v: float((fal.uu_solar * v / fal.deficit_2021_2025_mediana >= 1).mean()) for v in VIV_SOLAR}
    rent = float((fal.pct_brecha_positiva >= 80).mean())
    if cob[5] >= 0.8:
        ver = "PARCIALMENTE"
    elif cob[20] < 0.5:
        ver = "NO RESPALDADA"
    else:
        ver = "ANALIZADA, NO CONCLUYENTE"
    ficha = {
        "id": "M3-V1", "tema": "Suelo disponible",
        "enunciado": "Hay suelo de sobra para construir.",
        "capa": "C4",
        "magnitud": (f"Solares catastrales (uso «solar») 2026: {int(nac.uu_solar):,} unidades urbanas; con 5/10/20 viviendas por "
                     f"solar cubren el déficit 2021-2025 (mediana M1) en {cob[5]*100:.0f} %/{cob[10]*100:.0f} %/{cob[20]*100:.0f} % de "
                     f"las {len(fal)} provincias con déficit positivo. La brecha precio-coste no se usa en esta "
                     f"ficha: el coste en nivel es un supuesto.").replace(",", "."),
        "intervalo": f"cobertura provincial [{cob[5]*100:.0f} %; {cob[20]*100:.0f} %] según viviendas por solar (5 a 20)",
        "cota": "—",
        "literatura": "Glaeser y Gyourko (2018, VERIFICADA): precio por encima del coste de construcción más suelo como indicio de restricción de oferta; sin cifra citable para España.",
        "veredicto": ver,
        "regla": ("PROVISIONAL: depende del déficit de M1, en corrección al generar este fichero; se recalcula al ejecutar m3_run. "
                  "Regla fijada antes de calcular: PARCIALMENTE si los solares cubren el déficit en >= 80 % de las provincias con 5 "
                  "viviendas por solar; NO RESPALDADA si en < 50 % con 20; en otro caso, ANALIZADA, NO CONCLUYENTE. "
                  "RESPALDADA no es posible: la única fuente de suelo (Catastro) no distingue suelo urbanizado, clasificado ni "
                  "disponible, y el SIU no es accesible."),
        "limites": ("El uso «solar» catastral es suelo urbano sin edificar, no suelo urbanizable ni edificabilidad; SIU inaccesible "
                    "(docs/v4/fuentes_fallidas.md). Catastro no cubre territorios forales. El coste de construcción en nivel "
                    "no tiene fuente verificable."),
        "evidencia": ["output/v4/M3/clasificacion_provincias.csv", "output/v4/M3/tablas/M3_solares_nacional_catastro.csv",
                      "data/raw/v4/catastro_solares_municipios.csv.gz"],
    }
    (OUT / "fichas_verificador.json").write_text(json.dumps([ficha], ensure_ascii=False, indent=1), encoding="utf-8")

    cc_p, cc_m = conteo(out_p), conteo(out_m)
    sup = ["coste de construcción 900/1.200/1.500 EUR/m2 (supuesto externo, NO verificado)",
           "margen del promotor 15/20/25 % (Glaeser y Gyourko)", "edificabilidad 0,8/1,2/1,6 m2/m2",
           "suelo MIVAU provincial (no existe dato municipal)", "viviendas por solar 5/10/20"]
    lim = ["PROVISIONAL: déficit de M1 en corrección", "Sin fuente verificable de PEM/m2 ni de MBC: el nivel del coste es un supuesto, no un dato",
           "Costes fuera: honorarios técnicos, tasas e ICIO, licencias, financiación y beneficio (cubiertos por el margen)",
           "Valor tasado = tasación de vivienda libre existente y nueva, no precio de obra nueva",
           "Solares catastrales ≠ suelo disponible (SIU inaccesible)"]
    hechos = [
        {"id": "M3-H-brecha-prov", "enunciado_neutro": (
            f"Brecha central precio - coste(1+margen) - suelo repercutido por provincia: rango [{rng[0]:.0f}; {rng[1]:.0f}] EUR/m2; "
            f"mayores {ext_alto}; menores {ext_bajo}"),
         "capa": "C4", "magnitud": float(pp.brecha_central.median()), "unidad": "EUR/m2 (mediana provincial)",
         "intervalo": [float(pp.brecha_min.min()), float(pp.brecha_max.max())],
         "fuentes": ["MIVAU valor tasado", "MIVAU suelo urbano", "supuesto de coste"], "supuestos": sup, "limites": lim},
        {"id": "M3-H-clases-prov", "enunciado_neutro": f"Clase modal por provincia: {cc_p}; estables (>=80 %): {len(pe)} de {len(out_p)}",
         "capa": "C4", "magnitud": len(pe), "unidad": "provincias estables", "intervalo": [0, len(out_p)],
         "fuentes": ["M1", "MIVAU", "Catastro"], "supuestos": sup, "limites": lim + ["La capa efectiva está limitada por la del déficit de M1"]},
        {"id": "M3-H-clases-mun", "enunciado_neutro": f"Clase modal por municipio: {cc_m}; estables (>=80 %): {len(me)} de {len(out_m)}",
         "capa": "C4", "magnitud": len(me), "unidad": "municipios estables", "intervalo": [0, len(out_m)],
         "fuentes": ["M1", "MIVAU", "Catastro"], "supuestos": sup,
         "limites": lim + ["Déficit municipal M1 es C4", "Municipios sin valor tasado propio usan el precio provincial (proxy)"]},
        {"id": "M3-H-solares", "enunciado_neutro": (f"Catastro 2026: {int(nac.uu_solar)} unidades urbanas con uso solar y "
                                                    f"{int(nac.uu_res)} residenciales"),
         "capa": "C4", "magnitud": float(nac.uu_solar), "unidad": "unidades urbanas", "intervalo": [float(nac.uu_solar)] * 2,
         "fuentes": ["Catastro (fuente única; SIU inaccesible)"], "supuestos": [], "limites": lim},
    ]
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1), encoding="utf-8")
    res = {
        "rama": "M3", "pregunta": "¿Se puede construir donde hace falta? (suelo, brecha precio-coste, capacidad, clasificación)",
        "capa": "C4 (coste en nivel supuesto, no verificado)",
        "datos": ["catastro_solares_municipios (v4)", "mivau_valor_tasado_*", "mivau_v2_suelo", "mivau_v2_iniciadas_terminadas_prov",
                  "eurostat_costes", "eurostat_produccion_construccion", "output/v4/M1"],
        "N": {"provincias": len(out_p), "municipios": len(out_m), "especificaciones_por_unidad": int(len(grid))},
        "metodo": "Brecha al estilo Glaeser-Gyourko con coste supuesto; multiverso de umbrales; estabilidad de la clase modal",
        "estimacion": {"brecha_provincial_rango_central": rng, "clases_provincias": cc_p, "clases_municipios": cc_m,
                       "estables_provincias": len(pe), "estables_municipios": len(me), "cobertura_solares": cob},
        "ic95": None, "p_ajustado": None,
        "nivel_evidencia": "EXPLORATORIO (C4): brecha con coste supuesto; sin lenguaje causal",
        "diagnosticos": {"umbral_estabilidad": UMBRAL_C2, "fdr": "no aplica: no hay contrastes de hipótesis", "semilla": SEED},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": ("PROVISIONAL: los recuentos dependen de las tablas de M1 (déficit con error de terminadas, en corrección); "
                  "m3_run las lee en tiempo de ejecución y se recalcula. Sin PEM/m2 ni MBC verificables: el coste en nivel es supuesto (900-1.500). Empleo sectorial y plazos de licencia: "
                  "no hay datos abiertos en la base (Eurostat empleo es total; EPA sin rama). SIU: fallo de red."),
    }
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")


if __name__ == "__main__":
    main()

"""A4 Coste de construccion oficial y reclasificacion territorial. Determinista y sin red (SEED=20261010, un hilo).

Entradas versionadas: data/raw/v5/a4_mbc_rd1020_1993.csv (a4_fetch.py), data/raw/eurostat_costes.csv,
output/v4/M1/tablas, output/v4/M3 (+tablas), data/raw/mivau_v2_*.csv, data/raw/ine_v2_hogares_prov.csv.
SMOKE=1 usa 10 provincias y escribe en output/v5/A4/_smoke.

COSTE OFICIAL (rango derivado, por area geografica = unico para toda Espana: sin MBC de ponencia por municipio accesible):
  minimo = MBC7 (1993, 28.800 pta/m2) y maximo = MBC1 x 1,36 (46.800 pta/m2 x coef. maximo de incremento, norma 16 del RD 1020/1993
  segun RD 1464/2007), convertidos a EUR (166,386 pta/EUR, tipo fijo legal) y actualizados con el indice Eurostat sts_copi_q
  (coste de construccion de edificios residenciales, ES, 2021=100) de 1993 (media anual) a la ventana de precios 2025T3-2026T2.
  Supuesto de la actualizacion: la relacion entre el MBC y el coste de ejecucion evoluciona como el indice. Fuentes (b) modulos de
  VPO autonomicos y (c) PEM de visados/licencias: SIN DATO (docs/v5/fuentes_fallidas.md).
CLASES (clase publicada = la del coste central del rango, m=20 %, r=1,25; por unidad, con precio P, suelo repercutido rep = S/e, coste c, margen m, holgura r):
  falta   = deficit del periodo > 0 (mediana de combinaciones de M1; min y max en las variantes);
  1  falta y es rentable: brecha = P - c(1+m) - rep > 0 y no se cumple la condicion de la clase 2;
  2  falta con freno regulatorio o de suelo: P > r (c + rep) (precio supera con holgura coste mas suelo; brecha elevada) Y la oferta
     no responde (terminadas libres medias 2021-25 / medias 2016-20 - 1 < umbral u);
  3  falta y no es rentable: brecha <= 0;
  4  no falta: deficit <= 0 (sin deficit positivo; no implica exceso de oferta);
  9  sin dato: falta precio, suelo, deficit u oferta (no se imputa).
CAPA: C2 solo si la clase es la misma en TODO el rango de coste oficial (5 puntos), los 3 margenes {15,20,25} %, las 2 holguras
  r {1,25; 1,5} y el signo del deficit coincide en min/mediana/max de M1 (resto de parametros en el valor central). Si no, C4. El
  nivel del deficit sigue siendo C4 (regla B5): `capa_estricta_B5` = C4 en todas; la clase C2 es condicional al SIGNO.
  Municipios: C4 siempre (deficit de fuente unica Catastro).
"""
from __future__ import annotations

import itertools
import json
import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "v3"), str(ROOT / "src" / "v4")]
from econ_utils import Registry  # noqa: E402
import m1_run as m1  # noqa: E402
import m3_run as m3  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
SMOKE = os.environ.get("SMOKE") == "1"
OUT = ROOT / "output" / "v5" / "A4" / ("_smoke" if SMOKE else "")
M1T = ROOT / "output" / "v4" / "M1" / "tablas"
M3T = ROOT / "output" / "v4" / "M3" / "tablas"
PTA_EUR = 166.386
MARGEN = [0.15, 0.20, 0.25]
RATIO = [1.25, 1.5]
EDIF = [0.8, 1.2, 1.6]
SUELO_V = [0, 1]
UMBRAL = [0.0, 0.10, 0.25]
CEN = dict(m=0.20, r=1.25, e=1.2, s=0, u=0.10)
C_SUP = [900.0, 1200.0, 1500.0]
ETIQ = {1: "1 falta y es rentable", 2: "2 falta con freno regulatorio o de suelo (precio > r(c+suelo) y oferta sin respuesta)",
        3: "3 falta y no es rentable", 4: "4 no falta (deficit <= 0)", 9: "9 sin dato"}
COD = [1, 2, 3, 4, 9]


# ------------------------------------------------------------------ coste oficial
def coste_oficial():
    mb = pd.read_csv(ROOT / "data" / "raw" / "v5" / "a4_mbc_rd1020_1993.csv")
    v = mb[mb.concepto == "valor_pesetas_m2_1993"].set_index("clave").valor
    cf = mb[mb.concepto == "coef_max_incremento"].set_index("clave").valor
    e = pd.read_csv(ROOT / "data" / "raw" / "eurostat_costes.csv").set_index("periodo").valor
    i93 = float(e[[f"1993-Q{i}" for i in range(1, 5)]].mean())
    v25 = float(e[["2025-Q3", "2025-Q4", "2026-Q1", "2026-Q2"]].mean())
    f = v25 / i93
    base = (v / PTA_EUR)
    tab = pd.DataFrame({"mbc_pta_1993": v, "mbc_eur_1993": base, "coef_max": cf, "mbc_max_eur_1993": base * cf,
                        "mbc_eur_2025_26": base * f, "mbc_max_eur_2025_26": base * cf * f})
    cmin, cmax = float(tab.mbc_eur_2025_26.min()), float(tab.mbc_max_eur_2025_26.max())
    meta = dict(indice_1993=i93, indice_2025T3_2026T2=v25, factor=f, cmin=cmin, cmax=cmax,
                url_mbc=str(mb.url.iloc[0]), fecha_consulta=str(mb.fecha_consulta.iloc[0]))
    return tab, meta


# ------------------------------------------------------------------ clasificacion
def clasificar(P, S0, S1, RESP, D, c, m, r, e, s, u):
    """Vectores por unidad (U,); parametros escalares. Devuelve codigos (U,) y brecha (U,)."""
    S = S1 if s == 1 else S0
    rep = S / e
    brecha = P - c * (1 + m) - rep
    ok = ~np.isnan(P) & ~np.isnan(S) & ~np.isnan(D)
    reg = P > r * (c + rep)
    nores = RESP < u
    cls = np.full(P.shape, 9)
    cls = np.where(ok & (D <= 0), 4, cls)
    falta = ok & (D > 0)
    cls = np.where(falta & (brecha <= 0), 3, cls)
    sinresp = np.isnan(RESP)
    cls = np.where(falta & (brecha > 0) & ~sinresp, 1, cls)
    cls = np.where(falta & (brecha > 0) & ~sinresp & reg & nores, 2, cls)
    cls = np.where(falta & (brecha > 0) & sinresp, 9, cls)
    return cls, brecha


def evaluar(U, defs, cgrid, reg_log, fase):
    """U: dict P,S0,S1,RESP. defs: {variante: vector}. Devuelve tabla de resultados por unidad."""
    n = len(U["P"])
    cen_c = float(np.median(cgrid))
    res = {}
    todas = []
    for vname, D in defs.items():
        for c, m, r, e, s, u in itertools.product(cgrid, MARGEN, RATIO, EDIF, SUELO_V, UMBRAL):
            cls, _ = clasificar(U["P"], U["S0"], U["S1"], U["RESP"], D, c, m, r, e, s, u)
            todas.append((vname, c, m, r, e, s, u, cls))
            cnt = {k: int((cls == k).sum()) for k in COD}
            reg_log(fase, f"{fase}_{vname}_c{c:.0f}_m{m}_r{r}_e{e}_s{s}_u{u}", n, f"clases={json.dumps(cnt)}")
    # estabilidad total
    M = np.stack([t[7] for t in todas], axis=1)
    cuentas = np.stack([(M == k).sum(1) for k in COD], axis=1)
    modal = np.array(COD)[cuentas.argmax(1)]
    res["estab_total_pct"] = cuentas.max(1) / M.shape[1] * 100
    res["clase_modal"] = modal
    # criterio C2: costes x margenes x r en valores centrales del resto + signo del deficit
    med = list(defs)[1] if len(defs) == 3 else list(defs)[0]
    sel = [t[7] for t in todas if t[0] == med and t[4] == CEN["e"] and t[5] == CEN["s"] and t[6] == CEN["u"]]
    Mc = np.stack(sel, axis=1)
    res["estable_costes_m_r"] = (Mc == Mc[:, [0]]).all(1)
    res["clase_costes_m_r"] = Mc[:, 0]
    # estabilidad solo respecto al coste (m, r centrales)
    sc = [t[7] for t in todas if t[0] == med and t[2] == CEN["m"] and t[3] == CEN["r"] and t[4] == CEN["e"]
          and t[5] == CEN["s"] and t[6] == CEN["u"]]
    Ms = np.stack(sc, axis=1)
    res["estable_solo_coste"] = (Ms == Ms[:, [0]]).all(1)
    if len(defs) == 3:
        sg = np.stack([np.sign(np.nan_to_num(D, nan=0)) > 0 for D in defs.values()], axis=1)
        res["signo_deficit_estable"] = (sg == sg[:, [0]]).all(1)
    else:
        res["signo_deficit_estable"] = np.full(n, False)
    res["clase_central"] = [t[7] for t in todas if t[0] == med and t[1] == cen_c and t[2] == CEN["m"] and t[3] == CEN["r"]
                            and t[4] == CEN["e"] and t[5] == CEN["s"] and t[6] == CEN["u"]][0]
    # misma clasificacion central con el rango SUPUESTO de M3 (C4) para contraste
    sup = []
    for c in C_SUP:
        cl, _ = clasificar(U["P"], U["S0"], U["S1"], U["RESP"], defs[med], c, CEN["m"], CEN["r"], CEN["e"], CEN["s"], CEN["u"])
        sup.append(cl)
    sup = np.stack(sup, axis=1)
    res["clase_rango_supuesto_M3"] = np.where((sup == sup[:, [0]]).all(1), sup[:, 0], -1)
    _, br = clasificar(U["P"], U["S0"], U["S1"], U["RESP"], defs[med], cgrid[0], CEN["m"], CEN["r"], CEN["e"], CEN["s"], CEN["u"])
    _, br2 = clasificar(U["P"], U["S0"], U["S1"], U["RESP"], defs[med], cgrid[-1], CEN["m"], CEN["r"], CEN["e"], CEN["s"], CEN["u"])
    res["brecha_cmin"], res["brecha_cmax"] = br, br2
    return res


# ------------------------------------------------------------------ datos
def respuesta_oferta(nombres):
    _, _, _, _, _, _, _, _, it = m3.cargar()
    out = {}
    for cod, nom in nombres.items():
        serie = None
        for nivel, kk in (("provincia", m3.k(nom)), ("ccaa", m3.UNI_PROV.get(cod, "")), ("ciudad_autonoma", m3.CIUDAD.get(cod, ""))):
            x = it[(it.nivel == nivel) & (it.kk == kk)]
            if len(x):
                serie = x.set_index("periodo").valor
                break
        if serie is None:
            out[cod] = np.nan
            continue
        serie.index = serie.index.astype(int)
        a, b = serie.loc[2016:2020].mean(), serie.loc[2021:2025].mean()
        out[cod] = b / a - 1 if a > 0 else np.nan
    return pd.Series(out, name="resp_terminadas_21_25_vs_16_20")


def main():
    (OUT / "tablas").mkdir(parents=True, exist_ok=True)
    (OUT / "figuras").mkdir(exist_ok=True)
    reg = Registry(OUT / "registro.csv")

    def reg_log(fase, mid, n, notas):
        reg.log(fase, mid, "brecha=P-c(1+m)-S/e; clases 1-4,9", "2021", "2026", n, np.nan, np.nan, np.nan, notas=notas)

    tab, meta = coste_oficial()
    tab.to_csv(OUT / "tablas" / "A4_coste_oficial_rango.csv", float_format="%.2f")
    cgrid = list(np.linspace(meta["cmin"], meta["cmax"], 5))

    # ---------- provincias
    p1 = pd.read_csv(M1T / "M1_provincias.csv", dtype={"cod_prov": str})
    cap = pd.read_csv(M3T / "M3_capacidad_provincias.csv", dtype={"cod_prov": str}).set_index("cod_prov")
    nombres = cap.provincia.to_dict()
    resp = respuesta_oferta(nombres)
    defs_per = {}
    for per in ("2021-2025", "2012-2025"):
        d = p1[p1.periodo == per].set_index("cod_prov")
        defs_per[per] = {v: d[v].reindex(cap.index).to_numpy(float) for v in ("min", "mediana", "max")}
    idx = cap.index[:10] if SMOKE else cap.index
    sel = cap.index.get_indexer(idx)
    U = dict(P=cap.precio.to_numpy(float)[sel], S0=cap.suelo_todos.to_numpy(float)[sel], S1=cap.suelo_m50k.to_numpy(float)[sel],
             RESP=resp.reindex(idx).to_numpy(float))
    tp = {}
    for per in ("2021-2025", "2012-2025"):
        defs = {k: v[sel] for k, v in defs_per[per].items()}
        r = evaluar(U, defs, cgrid, reg_log, f"A4_prov_{per}")
        tp[per] = (r, defs)
    r21, d21 = tp["2021-2025"]
    r12, d12 = tp["2012-2025"]
    v4p = pd.read_csv(ROOT / "output" / "v4" / "M3" / "clasificacion_provincias.csv", dtype={"cod_prov": str}).set_index("cod_prov")
    out_p = pd.DataFrame({
        "cod_prov": idx, "provincia": cap.provincia.reindex(idx).values, "precio_eur_m2": U["P"], "suelo_eur_m2": U["S0"],
        "resp_oferta": U["RESP"], "deficit_2021_2025_min": d21["min"], "deficit_2021_2025_mediana": d21["mediana"],
        "deficit_2021_2025_max": d21["max"], "clase_2021_2025": r21["clase_central"], "clase_modal_2021_2025": r21["clase_modal"],
        "estable_costes_m_r": r21["estable_costes_m_r"], "estable_solo_coste": r21["estable_solo_coste"],
        "signo_deficit_estable": r21["signo_deficit_estable"], "estab_total_pct": r21["estab_total_pct"],
        "brecha_cmin": r21["brecha_cmin"], "brecha_cmax": r21["brecha_cmax"],
        "clase_con_rango_supuesto_M3": r21["clase_rango_supuesto_M3"],
        "clase_2012_2025": r12["clase_central"], "clase_modal_2012_2025": r12["clase_modal"],
        "estable_2012_2025": r12["estable_costes_m_r"] & r12["signo_deficit_estable"],
        "estab_total_2012_2025_pct": r12["estab_total_pct"]})
    # v5 (orquestador): el rango oficial es derivado de una sola norma fiscal (MBC 1993 actualizado) y puede
    # quedar por debajo del coste de mercado; C2 exige además la misma clase con el rango supuesto de v4
    # (900-1.500 EUR/m2), es decir, estabilidad en la unión 422-1.500 EUR/m2.
    out_p["estable_union_rangos"] = out_p.estable_costes_m_r & (out_p.clase_con_rango_supuesto_M3 == out_p.clase_2021_2025)
    out_p["capa"] = np.where(out_p.estable_union_rangos & out_p.signo_deficit_estable, "C2", "C4")
    out_p["capa"] = np.where(out_p.clase_2021_2025 == 9, "sin dato", out_p.capa)
    out_p["capa_estricta_B5"] = "C4"
    out_p["clase_v4_modal"] = v4p.clase_modal.reindex(idx).values
    out_p["clase_etiqueta"] = out_p.clase_2021_2025.map(ETIQ)
    out_p.to_csv(OUT / "clasificacion_provincias.csv", index=False, float_format="%.3f")

    # ---------- municipios
    mu = pd.read_csv(ROOT / "output" / "v4" / "M3" / "clasificacion_municipios.csv", dtype={"cod_mun": str, "cod_prov": str})
    if SMOKE:
        mu = mu.iloc[:60]
    S1m = np.where(mu.pob_2021 >= 50000, cap.suelo_m50k.reindex(mu.cod_prov).to_numpy(float), mu.suelo_eur_m2.to_numpy(float))
    Um = dict(P=mu.precio_eur_m2.to_numpy(float), S0=mu.suelo_eur_m2.to_numpy(float), S1=S1m,
              RESP=resp.reindex(mu.cod_prov).to_numpy(float))
    tm = {}
    for per, col in (("2021-2025", "deficit_2021_2025"), ("2012-2025", "deficit_2012_2025")):
        D = mu[col].to_numpy(float)
        tm[per] = evaluar(Um, {"unico": D}, cgrid, reg_log, f"A4_mun_{per}")
    out_m = pd.DataFrame({
        "cod_mun": mu.cod_mun, "municipio": mu.municipio, "cod_prov": mu.cod_prov, "pob_2021": mu.pob_2021,
        "precio_fuente": mu.precio_fuente, "precio_eur_m2": mu.precio_eur_m2, "suelo_eur_m2": mu.suelo_eur_m2,
        "deficit_2021_2025": mu.deficit_2021_2025, "deficit_2012_2025": mu.deficit_2012_2025,
        "clase_2021_2025": tm["2021-2025"]["clase_central"], "clase_modal_2021_2025": tm["2021-2025"]["clase_modal"],
        "estable_costes_m_r": tm["2021-2025"]["estable_costes_m_r"], "estab_total_pct": tm["2021-2025"]["estab_total_pct"],
        "clase_con_rango_supuesto_M3": tm["2021-2025"]["clase_rango_supuesto_M3"],
        "clase_2012_2025": tm["2012-2025"]["clase_central"], "clase_modal_2012_2025": tm["2012-2025"]["clase_modal"],
        "capa": "C4", "clase_v4_modal": mu.clase_modal})
    out_m.to_csv(OUT / "clasificacion_municipios.csv", index=False, float_format="%.3f")
    reg.flush()

    # ---------- recuentos y transicion
    filas = []
    for nivel, df in (("provincia", out_p), ("municipio", out_m)):
        for per, col in (("2021-2025", "clase_2021_2025"), ("2012-2025", "clase_2012_2025")):
            for k in COD:
                sub = df[df[col] == k]
                if nivel == "provincia":
                    c2 = int(((sub.capa == "C2")).sum()) if per == "2021-2025" else int(sub.get("estable_2012_2025", pd.Series(dtype=bool)).sum())
                else:
                    c2 = 0
                filas.append(dict(nivel=nivel, periodo=per, clase=k, etiqueta=ETIQ[k], n=len(sub), n_C2=c2,
                                  n_C4=len(sub) - c2))
    rec = pd.DataFrame(filas)
    rec.to_csv(OUT / "tablas" / "A4_recuentos_por_clase.csv", index=False)
    trans = []
    for nivel, df in (("provincia", out_p), ("municipio", out_m)):
        for per, col in (("2021-2025", "clase_2021_2025"), ("2012-2025", "clase_2012_2025")):
            v4col = df.clase_v4_modal.fillna(0).astype(int) if per == "2021-2025" else (
                (v4p.clase_modal_2012_2025.reindex(df.cod_prov).fillna(0).astype(int).to_numpy()) if nivel == "provincia"
                else pd.read_csv(ROOT / "output" / "v4" / "M3" / "clasificacion_municipios.csv", dtype={"cod_mun": str})
                .set_index("cod_mun").clase_modal_2012_2025.reindex(df.cod_mun).fillna(0).astype(int).to_numpy())
            ct = pd.crosstab(pd.Series(np.asarray(v4col), name="clase_v4"), pd.Series(df[col].to_numpy(), name="clase_A4"))
            ct = ct.stack().rename("n").reset_index().assign(nivel=nivel, periodo=per)
            trans.append(ct)
    pd.concat(trans)[["nivel", "periodo", "clase_v4", "clase_A4", "n"]].to_csv(OUT / "tablas" / "A4_transicion_v4_a_v5.csv", index=False)

    conc = concentracion(nombres, SMOKE)
    figuras(out_p, rec, conc, tab, meta)
    escribir_json(out_p, out_m, rec, conc, tab, meta, cgrid)


# ------------------------------------------------------------------ concentracion y reconciliacion
def concentracion(nombres, smoke):
    H, nom = m1.provincias_ecp()
    lib, pro = m1.terminadas_mivau()
    claves = {m1.norm(t): t for t in lib.index}
    filas = []
    for cod in sorted(nom):
        terr = m1.UNIPROV.get(cod) or claves.get(m1.norm(nom[cod])) or claves.get(m1.norm(nom[cod].split("/")[0]))
        terr_p = m1.UNIPROV_PROT.get(cod) or next((t for t in pro.index if m1.norm(t) == m1.norm(terr or "")), None)
        if terr not in lib.index:
            continue
        for per, (h0, h1, y0, y1) in {"2021-2025": ("2021T1", "2025T4", 2021, 2025), "2021-2024": ("2021T1", "2024T4", 2021, 2024)}.items():
            dh = float(H.loc[cod, h1] - H.loc[cod, h0])
            li = float(np.nansum([lib.loc[terr].get(y, np.nan) for y in range(y0, y1 + 1)]))
            pr = float(np.nansum([pro.loc[terr_p].get(y, np.nan) for y in range(y0, y1 + 1)])) if terr_p in pro.index else 0.0
            filas.append(dict(cod_prov=cod, provincia=nom[cod], periodo=per, delta_hogares=dh, altas_libres=li, altas_protegidas=pr,
                              deficit_bajas0=dh - li - pr, forales=cod in m1.FORALES))
    t = pd.DataFrame(filas)
    t.to_csv(OUT / "tablas" / "A4_deficit_provincial_ECP_MIVAU.csv", index=False, float_format="%.1f")
    # nacional independiente
    nac = {}
    ecp = H.sum()
    n = pd.read_csv(ROOT / "data" / "raw" / "mivau_v2_iniciadas_terminadas_prov.csv")
    nl = n[(n.nivel == "nacional") & n.serie.str.contains("viv_libres_terminadas_anual")].set_index("periodo").valor
    nl.index = nl.index.astype(int)
    q = pd.read_csv(ROOT / "data" / "raw" / "mivau_v2_protegida.csv")
    np_ = q[(q.nivel == "nacional") & q.serie.str.startswith("prot_definitiva_anual")].set_index("periodo").valor if "nivel" in q else pd.Series(dtype=float)
    np_.index = np_.index.astype(int) if len(np_) else np_.index
    for per, (h0, h1, y0, y1) in {"2021-2025": ("2021T1", "2025T4", 2021, 2025), "2021-2024": ("2021T1", "2024T4", 2021, 2024)}.items():
        dh = float(ecp[h1] - ecp[h0])
        li = float(nl.loc[y0:y1].sum())
        pr = float(np_.loc[y0:y1].sum()) if len(np_) else np.nan
        s = t[t.periodo == per]
        nac[per] = dict(dh_prov=float(s.delta_hogares.sum()), dh_nac=dh, libres_prov=float(s.altas_libres.sum()), libres_nac=li,
                        prot_prov=float(s.altas_protegidas.sum()), prot_nac=pr, deficit_prov=float(s.deficit_bajas0.sum()),
                        deficit_nac=dh - li - (pr if pr == pr else 0.0), n_prov=int(len(s)))
    conc = {}
    for per in ("2021-2025", "2021-2024"):
        s = t[t.periodo == per].set_index("provincia").deficit_bajas0
        pos = s[s > 0].sort_values(ascending=False)
        cum = (pos.cumsum() / pos.sum()).to_numpy()
        conc[per] = dict(n_50=int((cum < 0.5).sum() + 1), n_80=int((cum < 0.8).sum() + 1), n_pos=int(len(pos)),
                         total_pos=float(pos.sum()), total_neto=float(s.sum()), n_prov=int(len(s)),
                         top=[[a, float(b)] for a, b in pos.head(20).items()],
                         prov_50=list(pos.index[:int((cum < 0.5).sum() + 1)]), prov_80=list(pos.index[:int((cum < 0.8).sum() + 1)]))
    # M1 (mediana de combinaciones) 2021-2025
    cm = pd.read_csv(M1T / "M1_concentracion.csv")
    conc["m1_2021_2025"] = cm[(cm.nivel == "provincia") & (cm.periodo == "2021-2025")].to_dict("records")
    conc["reconciliacion"] = nac
    pd.DataFrame([{"periodo": k, **v} for k, v in nac.items()]).to_csv(OUT / "tablas" / "A4_reconciliacion_prov_nacional.csv", index=False)
    pd.DataFrame([{"periodo": p, "n_50": conc[p]["n_50"], "n_80": conc[p]["n_80"], "n_positivos": conc[p]["n_pos"],
                   "total_positivo": conc[p]["total_pos"], "total_neto_52prov": conc[p]["total_neto"]}
                  for p in ("2021-2025", "2021-2024")]).to_csv(OUT / "tablas" / "A4_concentracion.csv", index=False)
    return conc


# ------------------------------------------------------------------ figuras
def figuras(out_p, rec, conc, tab, meta):
    # M1 usa barras ordenadas (sin geopandas): mismo criterio, sin cartografia.
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for a, per in zip(ax, ("2021-2025", "2012-2025")):
        r = rec[(rec.nivel == "provincia") & (rec.periodo == per)]
        a.bar([str(k) for k in r.clase], r.n_C2, label="C2")
        a.bar([str(k) for k in r.clase], r.n_C4, bottom=r.n_C2, label="C4")
        a.set_title(f"Provincias por clase, {per}")
        a.set_xlabel("clase")
        a.legend()
    fig.tight_layout()
    fig.savefig(OUT / "figuras" / "A4_provincias_por_clase.png", dpi=110)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(9, 5))
    top = conc["2021-2025"]["top"]
    ax.barh([a for a, _ in top][::-1], [b for _, b in top][::-1])
    ax.set_title("Deficit 2021-2025 (ECP, MIVAU, bajas 0): 20 primeras provincias")
    fig.tight_layout()
    fig.savefig(OUT / "figuras" / "A4_concentracion_2021_2025.png", dpi=110)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(tab.index, tab.mbc_eur_2025_26, label="MBC min (coef. 1,00)")
    ax.bar(tab.index, tab.mbc_max_eur_2025_26 - tab.mbc_eur_2025_26, bottom=tab.mbc_eur_2025_26, label="hasta coef. maximo")
    ax.set_ylabel("EUR/m2 (2025T3-2026T2, derivado)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "figuras" / "A4_rango_coste_oficial.png", dpi=110)
    plt.close(fig)


def escribir_json(out_p, out_m, rec, conc, tab, meta, cgrid):
    def rc(nivel, per):
        r = rec[(rec.nivel == nivel) & (rec.periodo == per)]
        return {int(k): [int(n), int(c2)] for k, n, c2 in zip(r.clase, r.n, r.n_C2)}
    rcn = conc["reconciliacion"]
    resultado = {
        "rama": "A4", "pregunta": "¿Dónde falta vivienda y es rentable construirla con el coste oficial? Rango oficial de coste y reclasificación",
        "capa": "C2 (clases estables en todo el rango de coste, margen y r, condicionadas al signo del déficit) / C4 (resto, municipios)",
        "datos": ["RD 1020/1993 (BOE-A-1993-19265): MBC1-MBC7 y coeficientes de la norma 16", "Eurostat sts_copi_q (ES)",
                  "MIVAU valor tasado y precios de suelo", "output/v4/M1 (déficit)", "output/v4/M3 (suelo, precio, municipios)"],
        "N": {"provincias": int(len(out_p)), "municipios": int(len(out_m))},
        "metodo": "Rango de coste = MBC 1993 (BOE) actualizado con índice Eurostat; clases por unidad en rejilla coste x margen x r x edificabilidad x suelo x umbral de oferta x variante de déficit",
        "estimacion": {"coste_eur_m2_rango": [round(meta["cmin"], 1), round(meta["cmax"], 1)], "factor_actualizacion_1993_a_2025_26": round(meta["factor"], 4),
                       "provincias_2021_2025_[n,n_C2]": rc("provincia", "2021-2025"), "provincias_2012_2025_[n,n_C2]": rc("provincia", "2012-2025"),
                       "municipios_2021_2025_[n,n_C2]": rc("municipio", "2021-2025"), "municipios_2012_2025_[n,n_C2]": rc("municipio", "2012-2025"),
                       "concentracion": {p: {k: conc[p][k] for k in ("n_50", "n_80", "n_pos", "total_pos", "total_neto", "n_prov")} for p in ("2021-2025", "2021-2024")}},
        "ic95": None, "p_ajustado": None,
        "nivel_evidencia": "COTA (C2) condicionada y EXPLORATORIO (C4); sin lenguaje causal",
        "diagnosticos": {"reconciliacion_prov_nacional": rcn, "cobertura": "52 provincias; Álava, Bizkaia, Gipuzkoa y Navarra solo con altas MIVAU (sin Catastro)",
                         "coste_fuentes": {"a_MBC": "dato 1993 + índice (derivado)", "b_VPO_CCAA": "sin dato", "c_PEM_visados_licencias": "sin dato"}},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": "Sin contraste de hipótesis: no hay p-valores que ajustar (Holm/BH no aplica). Registro de especificaciones en registro.csv. El rango de coste es derivado de una sola norma y un índice; no equivale a coste de mercado observado."}
    (OUT / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1, default=float))
    hoy = meta["fecha_consulta"]
    h = []

    def add(i, ind, val, mn, mx, uni, per, cob, fu, capa, fecha):
        h.append(dict(id=i, indicador=ind, valor=val, min=mn, max=mx, unidad=uni, periodo=per, cobertura=cob, fuentes=fu, capa=capa, fecha_dato=fecha))

    add("A4-001", "Rango oficial derivado de coste de construcción (MBC 1993 actualizado)", round((meta["cmin"] + meta["cmax"]) / 2, 0),
        round(meta["cmin"], 0), round(meta["cmax"], 0), "EUR/m2 construido", "2025T3-2026T2", "España (sin MBC por municipio)",
        "BOE-A-1993-19265; Eurostat sts_copi_q", "C4", hoy)
    for per in ("2021-2025", "2012-2025"):
        for k in COD:
            n, c2 = rc("provincia", per)[k]
            add(f"A4-prov-{per}-c{k}", f"Provincias en clase {k} ({ETIQ[k]})", n, c2, n, "provincias", per, "52 provincias", "output/v4/M1; M3; A4", "C2" if c2 == n and n > 0 else "C4", hoy)
    for p in ("2021-2025", "2021-2024"):
        add(f"A4-conc50-{p}", "Provincias que suman el 50 % del déficit positivo", conc[p]["n_50"], conc[p]["n_50"], conc[p]["n_50"], "provincias", p,
            "52 provincias", "ECP INE; MIVAU fin de obra (bajas 0)", "C1" if p == "2021-2024" else "C4", "2026-10")
        add(f"A4-conc80-{p}", "Provincias que suman el 80 % del déficit positivo", conc[p]["n_80"], conc[p]["n_80"], conc[p]["n_80"], "provincias", p,
            "52 provincias", "ECP INE; MIVAU fin de obra (bajas 0)", "C1" if p == "2021-2024" else "C4", "2026-10")
    (OUT / "hechos.json").write_text(json.dumps(h, ensure_ascii=False, indent=1, default=float))


if __name__ == "__main__":
    main()

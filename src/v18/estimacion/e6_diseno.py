"""V18 · fase 4 · E6-R1 y variantes · diseño: pilas por cohorte de terminación del edificio (diferencias en diferencias apiladas con controles aún no expuestos).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18 (plan 1.6 + adenda: «solo secciones contiguas», controles terminados en T+6 o después y en 2024 como máximo,
cohortes 2015-2018, k = 0 el primer año completo tras la terminación = T+1, SERPAVI desde 2011). Sin resultados: solo la construcción de la muestra.

Definiciones operativas (decididas antes de estimar; docs/v18/desviaciones_e1_e6.md, D-E6-1 a D-E6-4):
- Edificio cualificado: uso residencial, año de construcción (fin de obra del Catastro) en 2011-2024 y al menos `umbral` viviendas (20 en R1; 50 en A1; 10 en v6).
- Unidad: sección INE no sellada, sin vecina sellada (la exposición a edificios de secciones selladas no es observable), con SERPAVI de todos los años de la ventana.
- Expuesta por un edificio: contigua a la sección del edificio (modo «contigua») o con el centroide a menos de 250 m del edificio (modo «anillo», A1), sin ser la sección del edificio.
- Pila E (año del evento = terminación, o terminación − 2 en v2): tratadas = unidades cuyo primer edificio expuesto es de la cohorte E y sin otro edificio expuesto en E−4..E+4, y sin
  edificio propio cualificado en esa ventana; controles = unidades cuyo primer edificio expuesto es de E+6 a 2024 y sin edificio propio en la ventana.
- Evento k = año − (E + 1); ventana E−4..E+4 (k = −5..3); referencia k = −5; adelantos k = −4..−1; resumen = media de k = 0..3.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e1_datos as D  # noqa: E402
import e6_datos as DT  # noqa: E402

COHORTES = [2015, 2016, 2017, 2018]
ANIO_MIN, ANIO_MAX = 2011, 2024


def base() -> dict:
    """Tablas comunes: secciones no selladas, adyacencias, edificios, SERPAVI (VC, VU) por sección y geometrías de las secciones selladas (solo frontera)."""
    import geopandas as gpd
    secs = DT.secciones_provincia()
    ok = set(secs.cod_seccion)
    adj = DT.adyacencias(secs)
    e = DT.edificios_46()
    e = e[e.uso.str.contains("residential", na=False) & e.anio.notna() & e.cod_seccion.isin(ok)].copy()
    e["anio"] = e.anio.astype(int)
    e = e[e.anio.between(ANIO_MIN, ANIO_MAX)]
    sp = {t: D.serpavi(secs.cod_seccion, t).pivot_table(index="cod_seccion", columns="anio", values="valor") for t in ("VC", "VU")}
    g = gpd.read_parquet(D.GEO)
    g = g[g.cod_provincia == "46"][["cod_seccion", "geometry"]].reset_index(drop=True).to_crs(25830)
    selladas = g[~g.cod_seccion.isin(ok)].copy()
    # centroides de todas las secciones de la provincia (para el anillo de 250 m)
    cen = g.geometry.representative_point()
    allc = pd.DataFrame({"cod_seccion": g.cod_seccion.values, "x": cen.x.values, "y": cen.y.values})
    return {"secs": secs, "ok": ok, "adj": adj, "edif": e, "sp": sp, "selladas": selladas, "centroides": allc.set_index("cod_seccion"), "geom_all": g}


def construir(B: dict, umbral: int = 20, modo: str = "contigua", propia: bool = False, resta: int = 0, gap: int = 6, tip: str = "VC", segundo_orden: bool = False,
              cohortes=COHORTES, sin_valencia: bool = False) -> dict:
    """Pilas por cohorte. Devuelve {'datos': DataFrame largo, 'conteos': {...}}. resta = años que se restan a la terminación para el evento (v2: 2)."""
    e = B["edif"][B["edif"].viviendas >= umbral].copy()
    e["evento"] = e.anio - resta
    adj, ok = B["adj"], B["ok"]
    cen = B["centroides"]
    # unidades expuestas por cada edificio
    exp_por_edif: list[tuple[int, list[str]]] = []
    for r in e.itertuples():
        if modo == "contigua":
            u = [j for j in adj.get(r.cod_seccion, set()) if j in ok]
        else:
            d = np.sqrt((cen.x.values - r.x) ** 2 + (cen.y.values - r.y) ** 2)
            u = [j for j in cen.index[d <= 250.0] if j in ok and j != r.cod_seccion]
        exp_por_edif.append((r.Index, u))
    ev_por_unidad: dict[str, list[tuple[int, str]]] = {}
    for (idx, u), r in zip(exp_por_edif, e.itertuples()):
        for j in u:
            ev_por_unidad.setdefault(j, []).append((int(r.evento), r.cod_seccion))
    propios = e.groupby("cod_seccion").evento.apply(list).to_dict()
    # unidades con alguna sección sellada que podría exponerlas (no observable)
    if modo == "contigua":
        contaminada = {j for j in ok if any(n not in ok for n in adj.get(j, set()))}
    else:
        import geopandas as gpd
        pts = gpd.GeoDataFrame({"cod_seccion": list(ok)}, geometry=gpd.points_from_xy(cen.loc[list(ok)].x, cen.loc[list(ok)].y), crs=25830)
        pts["geometry"] = pts.geometry.buffer(250.0)
        s = gpd.sjoin(pts, B["selladas"][["geometry"]], how="inner", predicate="intersects")
        contaminada = set(s.cod_seccion)
    sp = B["sp"][tip]
    filas, conteos = [], {}
    segundo = _segundo_orden(B, e, ok) if segundo_orden else {}
    for E in cohortes:
        anios = list(range(E - 4, E + 5))
        if anios[0] < ANIO_MIN or anios[-1] > ANIO_MAX:
            conteos[E] = {"tratadas": 0, "controles": 0, "motivo": "ventana fuera de 2011-2024"}
            continue
        completo = set(sp.index[sp.reindex(columns=anios).notna().all(axis=1)]) if all(a in sp.columns for a in anios) else set()
        tr, co = {}, {}
        for j in ok:
            if j in contaminada or j not in completo:
                continue
            if sin_valencia and j.startswith("46250"):
                continue
            own = propios.get(j, [])
            ev = sorted(ev_por_unidad.get(j, []))
            if propia:
                ev = sorted(ev + [(y, j) for y in own])
            elif any(E - 4 <= y <= E + 4 for y in own):
                continue
            if not ev:
                continue
            y0 = ev[0][0]
            ys = [y for y, _ in ev]
            if y0 == E and all(y == E or y > E + 4 for y in ys):
                tr[j] = ev[0][1]
            elif not segundo_orden and E + gap <= y0 <= ANIO_MAX and y0 >= E + gap:
                co[j] = ev[0][1]
        if segundo_orden:        # controles: contiguas de segundo orden de los mismos edificios (sin ser expuestas por ningún edificio en la ventana)
            bs_tr = set(tr.values())
            for bs in bs_tr:
                for j in segundo.get(bs, set()):
                    if j in tr or j in co or j in contaminada or j not in completo or (sin_valencia and j.startswith("46250")):
                        continue
                    ev = ev_por_unidad.get(j, [])
                    own = propios.get(j, [])
                    if any(E - 4 <= y <= E + 4 for y, _ in ev) or any(E - 4 <= y <= E + 4 for y in own):
                        continue
                    co[j] = bs
        conteos[E] = {"tratadas": len(tr), "controles": len(co), "municipios_tratadas": len({j[:5] for j in tr}), "municipios_controles": len({j[:5] for j in co}),
                      "valencia_ciudad_tratadas": sum(j.startswith("46250") for j in tr)}
        for grupo, dic in ((1, tr), (0, co)):
            for j, bs in dic.items():
                w = sp.loc[j, anios]
                for a in anios:
                    filas.append({"pila": E, "cod_seccion": j, "anio": a, "y": float(np.log(w[a])), "tr": grupo, "k": a - (E + 1), "bsec": bs, "mun": j[:5]})
    d = pd.DataFrame(filas)
    if len(d):
        d["unit_pila"] = d.pila.astype(str) + "_" + d.cod_seccion
        d["anio_pila"] = d.pila.astype(str) + "_" + d.anio.astype(str)
        d["mun_anio_pila"] = d.pila.astype(str) + "_" + d.mun + "_" + d.anio.astype(str)
    return {"datos": d, "conteos": conteos, "contaminadas": len(contaminada)}


def _segundo_orden(B: dict, e: pd.DataFrame, ok: set) -> dict[str, set[str]]:
    adj = B["adj"]
    out = {}
    for bs in e.cod_seccion.unique():
        n1 = adj.get(bs, set())
        n2 = set()
        for n in n1:
            n2 |= adj.get(n, set())
        out[bs] = {j for j in n2 - n1 - {bs} if j in ok}
    return out


def totales(c: dict) -> dict:
    cs = c["conteos"]
    return {"tratadas": int(sum(v.get("tratadas", 0) for v in cs.values())), "controles_unicos_aprox": int(sum(v.get("controles", 0) for v in cs.values()))}

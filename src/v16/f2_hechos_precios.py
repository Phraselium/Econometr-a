"""V16-F2.1 · Hecho 1: precios de compra, nominales y reales (deflactor: IPC general), España y CCAA, 2007/2013/2019 → 2025.

Medidas: INE IPV (base notarial), MIVAU valor tasado (tasaciones), Registradores (compraventas inscritas, pm2 medio, agregado propio
de datos abiertos ODbL) y Notariado (precio medio por m2 semestral; mismo grupo que el IPV). Media anual de 4 trimestres (o 2 semestres).
Control: 2015-2025 reproduce A23-P1 (79,9) y los extremos de A23-P2 (44,2 a 56,1); si no, se anota en discrepancias.
Deflactor: ipc_general nacional (data/processed/v8/nacional_q_v8.csv); no hay IPC por CCAA en el repositorio, así que el real autonómico
usa el mismo deflactor nacional (supuesto declarado).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from f2_hechos_base import FECHA, GRUPO, RAIZ, SAL, TOL_PP, anotar, capa_por_vara, pct  # noqa: F401

ANIOS_BASE = (2007, 2013, 2019)
ULTIMO = 2025
MP = {"Principado de Asturias": "Asturias", "C. Foral de Navarra": "Comunidad Foral de Navarra"}


def media_anual(df: pd.DataFrame, col: str) -> pd.Series:
    d = df[["trimestre", col]].dropna().copy()
    d["y"] = d.trimestre.str[:4].astype(int)
    g = d.groupby("y")[col].agg(["mean", "count"])
    return g[g["count"] == 4]["mean"]


def cambio(s: pd.Series, a0: int, a1: int) -> float:
    return float(s.loc[a1] / s.loc[a0] - 1) if a0 in s.index and a1 in s.index else float("nan")


def series_nacionales() -> tuple[dict[str, pd.Series], pd.Series]:
    n = pd.read_csv(RAIZ / "data/processed/v8/nacional_q_v8.csv")
    raw = RAIZ / "data/raw/pdf"
    rg = pd.read_csv(raw / "registradores_opendata_anual.csv")
    x = rg[(rg.serie == "compraventas_viv_pm2") & (rg.nivel == "nacional")]
    cgn = pd.read_csv(raw / "notariado_cgn_extranjeros_semestral.csv")
    cgn = cgn[(cgn.serie == "precio_m2") & (cgn.categoria == "Total general")].copy()
    cgn["y"] = cgn.periodo.str[:4].astype(int)
    g = cgn.groupby("y").valor.agg(["mean", "count"])
    s = {"INE IPV": media_anual(n, "ipv"), "MIVAU valor tasado": media_anual(n, "p_tasado"),
         "Registradores": pd.Series(x.valor.to_numpy(), index=x.periodo.astype(int).to_numpy()),
         "Notariado": g[g["count"] == 2]["mean"]}
    return s, media_anual(n, "ipc_general")


def series_ccaa() -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    p = pd.read_csv(RAIZ / "data/processed/v8/panel_ccaa_q_v8.csv")
    p["y"] = p.trimestre.str[:4].astype(int)
    out = {}
    for nombre, col in (("INE IPV", "ipv"), ("MIVAU valor tasado", "p_tasado")):
        d = p.dropna(subset=[col]).groupby(["ccaa", "y"])[col].agg(["mean", "count"]).reset_index()
        d = d[d["count"] == 4]
        out[nombre] = d.pivot(index="y", columns="ccaa", values="mean")
    rg = pd.read_csv(RAIZ / "data/raw/pdf/registradores_opendata_anual.csv")
    x = rg[(rg.serie == "compraventas_viv_pm2") & (rg.nivel == "ccaa")].copy()
    x["ccaa"] = x.territorio.replace(MP)
    out["Registradores"] = x.pivot_table(index="periodo", columns="ccaa", values="valor")
    return out, p[["ccaa", "codigo_ine_ccaa"]].drop_duplicates().set_index("ccaa")


def real(nom: float, ipc: float) -> float:
    return (1 + nom) / (1 + ipc) - 1


def calcular() -> dict:
    s, ipc = series_nacionales()
    res: dict = {"control": {}, "nacional": {}, "ccaa": None}
    for k, v in s.items():
        res["control"][k] = cambio(v, 2015, ULTIMO)
    filas = []
    for b in ANIOS_BASE:
        nom = {k: cambio(v, b, ULTIMO) for k, v in s.items()}
        rea = {k: real(nom[k], cambio(ipc, b, ULTIMO)) for k in nom}
        res["nacional"][b] = {"ipc": cambio(ipc, b, ULTIMO), "nom": nom, "real": rea}
    ccaa, cod = series_ccaa()
    for cc in sorted(ccaa["INE IPV"].columns):
        for b in ANIOS_BASE:
            fila = {"codigo_ine_ccaa": int(cod.loc[cc, "codigo_ine_ccaa"]), "ccaa": cc, "base": b, "ultimo": ULTIMO}
            nom = {}
            for k in ("INE IPV", "MIVAU valor tasado", "Registradores"):
                d = ccaa[k]
                nom[k] = cambio(d[cc], b, ULTIMO) if cc in d.columns else float("nan")
            ipc_b = cambio(ipc, b, ULTIMO)
            rea = {k: real(v, ipc_b) for k, v in nom.items()}
            for k in nom:
                fila[f"nominal_{k}_pct"] = round(pct(nom[k]), 2)
                fila[f"real_{k}_pct"] = round(pct(rea[k]), 2)
            capa, nuc = capa_por_vara({k: 100 * v for k, v in rea.items()})
            fila["capa_real"] = capa
            fila["fuentes_que_coinciden"] = "; ".join(nuc)
            filas.append(fila)
    res["ccaa"] = pd.DataFrame(filas)
    return res


def _cifra_nacional(r: dict, b: int, tipo: str) -> None:
    vals = {k: 100 * v for k, v in r["nacional"][b][tipo].items()}
    capa, nuc = capa_por_vara(vals)
    etiqueta = "reales (deflactor IPC general)" if tipo == "real" else "nominales"
    cual = {k: round(v, 1) for k, v in vals.items()}
    if capa == "C1":
        v = float(np.mean([vals[k] for k in nuc]))
        lo, hi = min(vals[k] for k in nuc), max(vals[k] for k in nuc)
        motivo = (f"Coinciden {', '.join(nuc)} (grupos distintos) dentro de ±{TOL_PP} p.p.; valor = punto medio de esas fuentes, "
                  f"rango = entre fuentes. Todas las medidas: {cual}.")
    else:
        v = None
        lo, hi = min(vals.values()), max(vals.values())
        motivo = (f"Las medidas no coinciden dentro de ±{TOL_PP} p.p. entre al menos dos grupos independientes: {cual}. Se publican "
                  f"todas (rango) y no se escoge una; la discrepancia de método entre el IPV y las tasaciones ya era conocida (A23-P3).")
        nuc = list(vals)
    # v6: cada resultado de compra declara su medida de precio
    medida = (f"medida: precio medio por m² sin ajuste de calidad ({', '.join(nuc)}); el IPV del INE, ajustado por calidad, da "
              f"{cual.get('INE IPV', 'n. d.')} %") if capa == "C1" else "medidas: IPV del INE (ajustado por calidad) y precios medios por m²"
    anotar(f"V16-HEC-PRECIO-{tipo.upper()}-{b}-{ULTIMO}",
           f"Precio de compra, cambio acumulado {etiqueta} {b}-{ULTIMO} (media anual), España; {medida}",
           v, lo, hi, "%", f"{b}-{ULTIMO} (media anual)", "España", list(vals), capa, f"{ULTIMO} (anual)",
           f"f2_hechos_precios.py: media anual de 4 trimestres (IPV, tasado), anual (Registradores pm2) y de 2 semestres (Notariado); "
           f"cambio = X_{ULTIMO}/X_{b}-1; real = (1+nominal)/(1+IPC general)-1 con IPC {100 * r['nacional'][b]['ipc']:.1f} %.",
           tolerancia=f"±{TOL_PP} p.p. entre cambios acumulados", motivo_capa=motivo)


def hechos(r: dict) -> list[str]:
    avisos = []
    ck = pd.read_csv(RAIZ / "output/v5/cifras_clave.csv", dtype=str).set_index("id")
    pub = {"INE IPV": float(ck.at["A23-P1", "valor"]), "MIVAU valor tasado": 44.2, "Notariado": 47.2, "Registradores": 56.1}
    for k, v in pub.items():
        mio = round(100 * r["control"][k], 1)
        if abs(mio - v) > 0.1:
            avisos.append(f"Control 2015-2025 {k}: V16 {mio} frente a 1.0 {v} (A23-P1/P2)")
    for b in ANIOS_BASE:
        for tipo in ("nom", "real"):
            _cifra_nacional(r, b, tipo)
    t = r["ccaa"]
    for b in ANIOS_BASE:
        d = t[t.base == b]
        n = int((d.capa_real == "C1").sum())
        anotar(f"V16-HEC-PRECIO-CCAA-NCOINC-{b}-{ULTIMO}",
               f"CCAA (de {len(d)}) con al menos dos medidas de grupos distintos (IPV, tasado, Registradores) dentro de ±{TOL_PP} p.p. en el cambio real {b}-{ULTIMO}",
               n, None, None, "CCAA", f"{b}-{ULTIMO}", f"{len(d)} CCAA", ["INE IPV", "MIVAU valor tasado", "Registradores"], "C4", f"{ULTIMO} (anual)",
               "f2_hechos_precios.py: tabla precios_ccaa.csv (cambios por CCAA y medida; columna capa_real). Deflactor nacional para todas.",
               tolerancia=f"±{TOL_PP} p.p.", motivo_capa="Recuento interno del análisis (contabilidad del proyecto), no un hecho contrastado con dos fuentes "
               "(misma razón que VER-A23-V2-1 en bajadas_capa.csv). El cambio por CCAA de cada medida está en precios_ccaa.csv.")
    d = SAL / "precios_ccaa.csv"
    t.to_csv(d, index=False)
    return avisos

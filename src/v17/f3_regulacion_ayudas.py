"""V17 · Fase 3 · Auditoría del grupo «regulacion_ayudas» (topes, regulación turística, ayudas a la demanda).

ANÁLISIS A POSTERIORI (V17), capa C4.
- Ronda 0: aritmética sobre cifras publicadas por terceros (fichas versionadas de docs/v15/literatura y docs/v16/literatura)
  y del proyecto (output/v5/cifras_clave.csv, output/v17/lectura_bde/v15_v16_micro/inferencia.csv, output/v3/PB/tablas).
- Ronda 1 (abogado del diablo): descomposición de la discrepancia sobre contratos de la Ley 11/2020 con el fichero de
  fianzas del Incasòl que usó V9-D1b (data/raw/v9/incasol, solo lectura): grupo de control, vecinos, forma funcional y
  ponderación. Cada especificación va al Registry (src/econ_utils.py); BH dentro de la familia como sensibilidad.
Sin red. SEED = 20261010 (nada aleatorio). Las provincias de la muestra cerrada v6 se leen de data/base/hechos.parquet
(campo muestra_sellada_v6) y se excluyen; Cataluña no está entre ellas. No se toca la muestra cerrada ni se ejecuta
ninguna evaluación.

Uso: python3 src/v17/f3_regulacion_ayudas.py
Salidas: output/v17/auditoria/regulacion_ayudas_hechos.json y output/v17/auditoria/regulacion_ayudas_registro.csv
"""
from __future__ import annotations

import csv
import json
import math
import statistics
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.econ_utils import Registry  # noqa: E402

SEED = 20261010
OUT = ROOT / "output" / "v17" / "auditoria" / "regulacion_ayudas_hechos.json"
REGISTRO = ROOT / "output" / "v17" / "auditoria" / "regulacion_ayudas_registro.csv"
L1 = ROOT / "docs" / "v16" / "literatura" / "L1_control_alquileres_efectos.csv"
L5 = ROOT / "docs" / "v16" / "literatura" / "L5_ayudas_demanda_efectos.csv"
INF = ROOT / "output" / "v17" / "lectura_bde" / "v15_v16_micro" / "inferencia.csv"
CIFRAS = ROOT / "output" / "v5" / "cifras_clave.csv"
PB_NAC = ROOT / "output" / "v3" / "PB" / "tablas" / "b1_nacional_sensibilidad.csv"
RAW = ROOT / "data" / "raw"
INCASOL = RAW / "v9" / "incasol" / "incasol_qww9-bvhh_actual.csv.gz"
REGIMEN = RAW / "v3" / "cataluna_contencion_rentas_v3.csv"
CENTROIDES = RAW / "v5" / "municipio_centroides_utm30.csv"
PADRON = RAW / "v16" / "tension_social" / "padron_cifras_oficiales" / "ine_cifras_oficiales_padron_municipio_29005.csv.gz"
BASE = ROOT / "data" / "base" / "hechos.parquet"
FECHA = "2026-10-19"
FICHA = "output/v17/auditoria/filas/{}.md"
CAT = ("08", "17", "25", "43")
T_INI, T_TRAT, T_FIN = "2019T1", "2020T4", "2022T1"   # ventana de V9-D1b; primer trimestre tratado como en src/v9/paneles.py
RADIO_VECINOS_M = 5_000

DOC = {
    # Fack (2006), Labour Economics 13(6), DOI 10.1016/j.labeco.2006.01.001: 78 céntimos por euro (resumen).
    "fack2006_theta": 0.78,
    # Gibbons y Manning (2006), JPubE, DOI 10.1016/j.jpubeco.2005.01.002: 60 % a dos tercios sobre el arrendador (resumen).
    "gm2006_theta_min": 0.60, "gm2006_theta_max": 2 / 3,
    # Grislain-Letrémy y Trevien (2022), BdF WP 886 (docs/v17/referencias/no_beneficiarios.md): perceptores +0,052 log
    # (e.e. 0,018), alquiler medio 454 euros, diferencial de ayuda 15-40 euros/mes (ejemplo de la tabla 1: 22-27).
    "glt_b": 0.052, "glt_se": 0.018, "glt_renta": 454.0, "glt_ayuda_min": 15.0, "glt_ayuda_max": 40.0,
    "glt_ayuda_ej_min": 22.0, "glt_ayuda_ej_max": 27.0,
    # Bono Alquiler Joven, RD 42/2022 (BOE-A-2022-802): 250 euros/mes (art. 11), 24 meses como máximo (art. 12).
    "bono_eur_mes": 250.0, "bono_meses": 24,
    # Ley 29/1994 (LAU), art. 9: prórroga obligatoria hasta 5 años (7 si el arrendador es persona jurídica).
    "lau_meses_min": 60, "lau_meses_pj": 84,
    # García-López et al. (2020), JUE 119, 103278 (P5): 54 anuncios -> +1,9 %; 200 -> +7 %; 220 áreas.
    "gl_anuncios_medio": 54, "gl_alquiler_medio": 1.9, "gl_anuncios_d10": 200, "gl_alquiler_d10": 7.0, "gl_areas": 220,
    # Gyódi, Mazur y Cocola-Gant (2025), Cities, DOI 10.1016/j.cities.2025.105915 (resumen): 10.700 frente a 20.000.
    "gyodi_medidos": 10_700, "gyodi_contrafactual": 20_000,
    # Monràs y García-Montalvo, UPF WP 1836 (abril de 2022), tabla IV (L1, sección 4): PPML por tramo.
    "mm_ppml_arriba": -0.449, "mm_ppml_abajo": 0.342,
    # Banco de España, Informe Anual 2025, p. 150 (docs/v17/referencias/bde_informes.md): «cerca del 10 %» del alquiler.
    "bde_vut_cuota_alquiler": 10.0,
}

HECHOS: list[dict] = []
REG: Registry | None = None


def hecho(id_, indicador, valor, minimo, maximo, unidad, periodo, cobertura, fuentes, lectura, ficha, nota=""):
    assert lectura in ("OF", "hecho", "cota", "asociación", "juicio experto", "no fiable", "no se puede saber", "sin cambio")
    r = lambda x: None if x is None or (isinstance(x, float) and not math.isfinite(x)) else round(float(x), 4)
    HECHOS.append({"id": f"V17-AUD-RA-{id_}", "indicador": indicador, "valor": r(valor), "min": r(minimo), "max": r(maximo),
                   "unidad": unidad, "periodo": periodo, "cobertura": cobertura, "fuentes": fuentes, "capa": "C4",
                   "lectura_v17": lectura, "fecha_dato": FECHA, "ficha": FICHA.format(ficha),
                   "nota": "a posteriori" + (f"; {nota}" if nota else "")})


def leer(p: Path) -> list[dict]:
    with p.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def fila(filas, **cond) -> dict:
    out = [f for f in filas if all(f.get(k) == v for k, v in cond.items())]
    assert len(out) == 1, (cond, len(out))
    return out[0]


def pnorm2(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2))


def tindex(p: str) -> int:
    return int(p[:4]) * 4 + int(p[-1]) - 1


def bh(p: list[float]) -> list[float]:
    p = np.asarray(p, float)
    n = len(p)
    o = np.argsort(p)
    adj = np.empty(n)
    acc = 1.0
    for k in range(n - 1, -1, -1):
        acc = min(acc, p[o[k]] * n / (k + 1))
        adj[o[k]] = acc
    return adj.tolist()


# ------------------------------------------------------------------ topes: literatura
def topes_literatura() -> dict:
    l1 = leer(L1)

    def busca(autor, resultado, fuente):
        c = [f for f in l1 if autor in f["autores_anio"] and f["resultado"] == resultado and f["fuente_cifra"] == fuente]
        assert len(c) == 1, (autor, resultado, fuente)
        return c[0]
    jm = busca("Jofre", "oferta_contratos", "tabla 3, columna 2")
    mm = busca("Monràs y García-Montalvo (2022)", "oferta_contratos", "tabla IV, columna 1")
    b_jm, s_jm = float(jm["estimacion"]), float(jm["ee"])
    b_mm, s_mm = float(mm["estimacion"]), float(mm["ee"])
    solape = (max(b_jm - 1.96 * s_jm, b_mm - 1.96 * s_mm), min(b_jm + 1.96 * s_jm, b_mm + 1.96 * s_mm))
    z = (b_jm - b_mm) / math.hypot(s_jm, s_mm)
    hecho("TOP-CONTRATOS-DIF", "Diferencia entre las estimaciones de contratos nuevos de Jofre-Monseny et al. (0,001; RSUE "
          "2023, tabla 3) y Monràs y García-Montalvo (-0,102; UPF WP 1836, abril de 2022, tabla IV, PPML), Ley 11/2020 "
          "(valor: diferencia en log; min/max: IC 95 % de la diferencia suponiendo independencia)",
          b_jm - b_mm, b_jm - b_mm - 1.96 * math.hypot(s_jm, s_mm), b_jm - b_mm + 1.96 * math.hypot(s_jm, s_mm),
          "log contratos", "2016-2022", "Cataluña, municipios",
          "docs/v16/literatura/L1_control_alquileres_efectos.csv (tablas de los autores)", "juicio experto", "topes",
          f"z = {z:.2f}, p bilateral = {pnorm2(z):.4f} suponiendo independencia; los IC 95 % solo se solapan entre "
          f"{solape[0]:.3f} y {solape[1]:.3f}; mismo registro (Incasòl): orientativo. La versión FRBSF 2023-28 da en "
          "torno a -10 % en la introducción (cifra por versión en docs/v17/referencias/d2_versiones.md)")
    hecho("TOP-TRAMO-ARRIBA", "Contratos nuevos por encima de la referencia, Monràs y García-Montalvo (UPF WP 1836, abril de "
          "2022, tabla IV, PPML; exp(b)-1)", 100 * (math.exp(DOC["mm_ppml_arriba"]) - 1), None, None, "%", "2016-2021",
          "Cataluña", "Monràs y García-Montalvo, UPF WP 1836, tabla IV (L1)", "juicio experto", "topes",
          "cifra de la versión de abril de 2022; la de 2023 presenta el reparto por sextiles del precio en exceso")
    hecho("TOP-TRAMO-ABAJO", "Contratos nuevos por debajo de la referencia, Monràs y García-Montalvo (UPF WP 1836, abril de "
          "2022, tabla IV, PPML; exp(b)-1)", 100 * (math.exp(DOC["mm_ppml_abajo"]) - 1), None, None, "%", "2016-2021",
          "Cataluña", "Monràs y García-Montalvo, UPF WP 1836, tabla IV (L1)", "juicio experto", "topes",
          "cifra de la versión de abril de 2022")
    inf = leer(INF)
    res = {}
    for ide in ("H1-CS", "H1-SDID", "H2-CS", "H2-SDID", "H2-PPML", "Q1c-global", "Q1c-sin-grandes"):
        f = fila(inf, id_resultado=ide)
        res[ide] = (float(f["estimacion_publicada"]), f["p_conv"], f["tamano_real"], f["publicable"])
    f = fila(inf, id_resultado="H2-SDID")
    hecho("TOP-H2-SDID", "H2 (V15), contratos nuevos en zonas tensionadas de Cataluña 2024, SDID: lectura convencional "
          "(valor: estimación; min/max: IC 95 % Webb)", float(f["estimacion_publicada"]), float(f["ic95_lo"]),
          float(f["ic95_hi"]), "%", "2024T2-2026T1", "Cataluña, municipios",
          "output/v17/lectura_bde/v15_v16_micro/inferencia.csv (H2-SDID); id publicado V15-H2-sdid-att", "asociación",
          "topes", f"p = {f['p_conv']}, tamaño real {f['tamano_real']}; H2-CS y H2-PPML no fiables (tamaño > 15 %); "
          "pretendencias de contratos rechazadas en V9-D1a; no se cambia la lectura publicada")
    return {"z": z, "solape": solape, "inferencia": res}


# ------------------------------------------------------------------ topes: descomposición con el Incasòl del repositorio
def provincias_cerradas() -> set[str]:
    import duckdb
    d = duckdb.sql(f"select distinct territorio_codigo c from '{BASE}' where nivel='provincia' and muestra_sellada_v6").df()
    return set(d.c)


def panel_incasol() -> pd.DataFrame:
    i = pd.read_csv(INCASOL, dtype=str)
    i = i[i.ambit_territorial.str.lower().str.startswith("municipi") & (i.posterior_prereg.str.lower() != "true")]
    i = i[i.periodo_iso.str.fullmatch(r"\d{4}T[1-4]")]
    i["cod"] = i.codi_territorial.str.zfill(5)
    i["contratos"] = pd.to_numeric(i.habitatges, errors="coerce")
    i["renta"] = pd.to_numeric(i.renda.str.replace(",", "."), errors="coerce")
    i["t"] = i.periodo_iso.map(tindex)
    i = i[(i.t >= tindex(T_INI)) & (i.t <= tindex(T_FIN)) & i.cod.str[:2].isin(CAT)]
    cerr = provincias_cerradas()
    assert not (set(CAT) & cerr), "Cataluña en la muestra cerrada: no se usa"
    i = i[~i.cod.str[:2].isin(cerr)]
    g = i.groupby(["cod", "t"]).agg(contratos=("contratos", "sum"), renta=("renta", "mean")).reset_index()
    nt = tindex(T_FIN) - tindex(T_INI) + 1
    ok = g[g.contratos > 0].groupby("cod").t.nunique()
    g = g[g.cod.isin(ok[ok == nt].index)].copy()          # panel equilibrado con contratos > 0 en los 13 trimestres
    reg = pd.read_csv(REGIMEN, dtype=str)
    ley11 = set(reg[reg.regimen == "ley11_2020"].cod_ine.str.zfill(5))
    zt = set(reg[reg.regimen == "ley12_2023_zona_tensionada"].cod_ine.str.zfill(5))
    g["tratado"] = g.cod.isin(ley11)
    g["tenso"] = g.cod.isin(zt) & ~g.tratado            # aproximación al control de Jofre-Monseny et al.
    g["post"] = g.t >= tindex(T_TRAT)
    g["d"] = (g.tratado & g.post).astype(float)
    cen = pd.read_csv(CENTROIDES, dtype={"codigo": str}).assign(codigo=lambda x: x.codigo.str.zfill(5)).set_index("codigo")
    trat = cen.loc[cen.index.isin(ley11), ["x_m", "y_m"]].to_numpy()
    xy = cen.reindex(sorted(g.cod.unique()))[["x_m", "y_m"]]
    dist = np.sqrt(((xy.to_numpy()[:, None, :] - trat[None, :, :]) ** 2).sum(-1)).min(1)
    vecino = dict(zip(xy.index, dist < RADIO_VECINOS_M))
    g["vecino"] = g.cod.map(vecino).fillna(False) & ~g.tratado
    p = pd.read_csv(PADRON, sep=";", dtype=str, encoding="utf-8-sig")
    p = p[p.Sexo == "Total"]
    p["cod"] = p.Municipios.str[:5]
    p["anio"] = p.Periodo.astype(int)
    p["pob"] = pd.to_numeric(p.Total.str.replace(".", "", regex=False), errors="coerce")
    pob = p.set_index(["cod", "anio"]).pob
    g["anio"] = g.t // 4
    g["pob"] = [pob.get((c, a), np.nan) for c, a in zip(g.cod, g.anio)]
    pre = g[~g.post].groupby("cod").contratos.mean()
    g["w"] = g.cod.map(pre)
    return g.dropna(subset=["pob"]).reset_index(drop=True)


def _did(df: pd.DataFrame, forma: str, ponderar: bool) -> tuple[float, float, int]:
    import statsmodels.api as sm
    cods = pd.Categorical(df.cod)
    ts = pd.Categorical(df.t)
    X = pd.concat([df[["d"]].reset_index(drop=True),
                   pd.get_dummies(cods, prefix="m", drop_first=True, dtype=float),
                   pd.get_dummies(ts, prefix="t", drop_first=True, dtype=float)], axis=1)
    X = sm.add_constant(X)
    grupos = cods.codes
    w = df.w.to_numpy() if ponderar else None
    if forma == "ppml":
        y = df.contratos.to_numpy()
        m = sm.GLM(y, X, family=sm.families.Poisson(), var_weights=w)
        r = m.fit(cov_type="cluster", cov_kwds={"groups": grupos}, maxiter=200)
    else:
        if forma == "log":
            y = np.log(df.contratos.to_numpy())
        elif forma == "log_pc":
            y = np.log(df.contratos.to_numpy() / df.pob.to_numpy())
        elif forma == "log_renta":
            y = np.log(df.renta.to_numpy())
        m = sm.WLS(y, X, weights=w) if ponderar else sm.OLS(y, X)
        r = m.fit(cov_type="cluster", cov_kwds={"groups": grupos})
    return float(r.params["d"]), float(r.bse["d"]), int(len(df))


def topes_descomposicion() -> dict:
    g = panel_incasol()
    controles = {
        "todos": ~g.tratado,
        "todos_sin_vecinos": ~g.tratado & ~g.vecino,
        "tensos": g.tenso,
        "tensos_sin_vecinos": g.tenso & ~g.vecino,
    }
    ventanas = {   # V9-D1b completa; la de Monràs y García-Montalvo (hasta junio de 2021); sin los trimestres de la COVID
        "v9": lambda d: d,
        "hasta_2021T2": lambda d: d[d.t <= tindex("2021T2")],
        "sin_2020T2_T3": lambda d: d[~d.t.isin([tindex("2020T2"), tindex("2020T3")])],
    }
    # PPML ya pondera por niveles; su versión ponderada (var_weights) no tiene errores agrupados fiables en statsmodels
    formas = [("log", False), ("log", True), ("log_pc", False), ("log_pc", True), ("ppml", False),
              ("log_renta", False), ("log_renta", True)]
    filas = []
    for nv, fv in ventanas.items():
        for nc, mc in controles.items():
            df = fv(g[g.tratado | mc]).copy()
            for forma, pond in formas:
                dd = df.dropna(subset=["renta"]) if forma == "log_renta" else df
                b, se, n = _did(dd, forma, pond)
                p = pnorm2(b / se)
                filas.append(dict(ventana=nv, control=nc, forma=forma, ponderado=pond, b=b, se=se, p=p, n=n,
                                  n_trat=int(dd[dd.tratado].cod.nunique()), n_ctrl=int(dd[~dd.tratado].cod.nunique())))
                REG.log("V17-F3-RA", f"topes_ley11_{nv}_{nc}_{forma}_{'w' if pond else 'nw'}",
                        f"{forma} ~ d + EF municipio + EF trimestre; cluster municipio; control={nc}; ponderado={pond}; "
                        f"ventana={nv}", T_INI, T_FIN, n, np.nan, np.nan, np.nan, coef_interes=b, p_interes=p,
                        notas="a posteriori; Incasòl (fianzas nuevas, municipio-trimestre), panel equilibrado; "
                              f"tratado desde {T_TRAT}; vecinos < {RADIO_VECINOS_M} m de un tratado")
    t = pd.DataFrame(filas)
    cant = t.forma != "log_renta"
    t.loc[cant, "p_bh"] = bh(t.loc[cant, "p"].tolist())
    t.loc[~cant, "p_bh"] = bh(t.loc[~cant, "p"].tolist())
    t["efecto_pct"] = 100 * (np.exp(t.b) - 1)
    ref = t[(t.ventana == "v9") & (t.control == "todos") & (t.forma == "log") & ~t.ponderado].iloc[0]
    sub = t[cant]
    nsub, nr = len(sub), int((~cant).sum())
    hecho("TOP-INC-CONTRATOS-REF", "Ley 11/2020, contratos nuevos (Incasòl, municipio-trimestre): DiD en log, control = todos "
          "los municipios catalanes no tratados, sin ponderar (valor: exp(b)-1; min/max: IC 95 %)",
          ref.efecto_pct, 100 * (math.exp(ref.b - 1.96 * ref.se) - 1), 100 * (math.exp(ref.b + 1.96 * ref.se) - 1), "%",
          f"{T_INI}-{T_FIN}", f"Cataluña, {int(ref.n_trat)} tratados y {int(ref.n_ctrl)} controles (panel equilibrado)",
          "Incasòl (data/raw/v9/incasol; no redistribuible); BOE/DOGC; elaboración propia", "asociación", "topes",
          f"p = {ref.p:.3f}; registro en output/v17/auditoria/regulacion_ayudas_registro.csv")
    hecho("TOP-INC-CONTRATOS-RANGO", f"Ley 11/2020, contratos nuevos: rango de las {nsub} especificaciones de cantidad (3 "
          "ventanas × 4 controles × log y log per cápita con y sin ponderar, y PPML) (valor: mediana; min/max: extremos; "
          "no es IC)",
          float(sub.efecto_pct.median()), float(sub.efecto_pct.min()), float(sub.efecto_pct.max()), "%",
          f"{T_INI}-{T_FIN}", "Cataluña, municipios", "Incasòl; elaboración propia", "asociación", "topes",
          f"{int((sub.p < 0.05).sum())} de {nsub} con p < 0,05; {int((sub.p_bh < 0.05).sum())} tras BH en la familia; "
          f"negativas: {int((sub.b < 0).sum())} de {nsub}; con p < 0,05 negativas: {int(((sub.p < 0.05) & (sub.b < 0)).sum())}")
    rt = t[~cant]
    hecho("TOP-INC-RENTA-RANGO", f"Ley 11/2020, renta media de los contratos nuevos: rango de las {nr} especificaciones (3 "
          "ventanas × 4 controles × con y sin ponderar) (valor: mediana; min/max: extremos; no es IC)",
          float(rt.efecto_pct.median()), float(rt.efecto_pct.min()), float(rt.efecto_pct.max()), "%",
          f"{T_INI}-{T_FIN}", "Cataluña, municipios", "Incasòl; elaboración propia", "asociación", "topes",
          f"{int((rt.p_bh < 0.05).sum())} de {nr} con p BH < 0,05; la renta media mezcla precio y composición")
    return {"tabla": t, "n_mun": int(g.cod.nunique()), "n_trat": int(g[g.tratado].cod.nunique()),
            "n_tenso": int(g[g.tenso].cod.nunique()), "n_vecino": int(g[g.vecino].cod.nunique())}


# ------------------------------------------------------------------ turística
def turistica() -> dict:
    por_anuncio = DOC["gl_alquiler_medio"] / DOC["gl_anuncios_medio"]
    assert abs(por_anuncio - DOC["gl_alquiler_d10"] / DOC["gl_anuncios_d10"]) < 0.002   # casi lineal en anuncios
    evitados = DOC["gyodi_contrafactual"] - DOC["gyodi_medidos"]
    por_area = evitados / DOC["gl_areas"]
    efecto = por_area * por_anuncio
    hecho("TUR-BCN-TRASLACION", "Traslación orientativa a alquiler del freno a los anuncios en Barcelona: anuncios evitados "
          "según el contrafactual de Gyódi et al. (2025) repartidos por igual entre las 220 áreas de García-López et al. "
          "(2020) y multiplicados por su efecto por anuncio (valor: reparto uniforme; min: solo la mitad de los anuncios "
          "evitados vuelve al alquiler residencial; max: los anuncios evitados se concentran en la mitad de las áreas)",
          efecto, 0.5 * efecto, 2 * efecto, "% de alquiler (área media)", "2015-2023",
          "Barcelona", "Gyódi, Mazur y Cocola-Gant (2025, DOI 10.1016/j.cities.2025.105915, resumen); García-López et al. "
          "(2020, DOI 10.1016/j.jue.2020.103278, P5)", "juicio experto", "turistica_regulacion",
          "JUICIO EXPERTO SIN ESTIMACIÓN: combina un contrafactual descriptivo de anuncios con una elasticidad de 2007-2017; "
          "supone linealidad y que cada anuncio evitado es una vivienda residencial; no es una evaluación de la norma")
    inf = leer(INF)
    q2a = fila(inf, id_resultado="Q2a")
    hecho("TUR-Q2A", "Q2a (V16) con inferencia convencional: Δlog IPC de alquiler por DT del log de la exposición turística "
          "(valor: estimación; min/max: IC 95 %)", float(q2a["estimacion_publicada"]), float(q2a["ic95_lo"]),
          float(q2a["ic95_hi"]), "Δlog por DT", "2017-2019 frente a 2022-2025", "41 provincias de entrenamiento",
          "output/v17/lectura_bde/v15_v16_micro/inferencia.csv (Q2a); id publicado V16-Q2-1", "asociación",
          "turistica_regulacion", f"p = {q2a['p_conv']}; tamaño real {q2a['tamano_real']} (cerca del límite del 15 %); "
          "mide densidad, no regulación; depende de controles y fecha de exposición")
    # Denominador: mismo numerador que el Banco de España (stock de viviendas turísticas) sobre alquiler habitual + turísticas.
    pb = pd.read_csv(PB_NAC)
    pb = pb[pb.eps == pb.eps.min()]
    cuotas = {}
    for _, r in pb.iterrows():
        cuotas[(r.periodo, r.stock)] = dict(vut=r.VUT_fin, alq=r.stock_alquiler, cuota=100 * r.VUT_fin / (r.stock_alquiler + r.VUT_fin),
                                           flujo=r.cota_cantidad_pct)
    c24 = cuotas[("2020M08-2024M08", "censo2021")]
    otros = [v["cuota"] for k, v in cuotas.items() if k[0].endswith("2024M08") or k[0].endswith("2026M05")]
    hecho("TUR-CUOTA-STOCK", "Viviendas turísticas (stock, INE VUT) sobre alquiler habitual (Censo 2021) + turísticas: mismo "
          "numerador que el Banco de España (valor: agosto de 2024 con el Censo; min/max: otras fechas y stock ECV × ECP)",
          c24["cuota"], min(otros), max(otros), "% de (alquiler habitual + turísticas)", "2024M08 (y 2026M05)", "España",
          "output/v3/PB/tablas/b1_nacional_sensibilidad.csv (INE VUT experimental; Censo 2021; ECV 2021 × ECP)", "cota", "turistica_regulacion",
          f"la cota C2 publicada (B4-v3-vut-cantidad = {c24['flujo']:.3f} %) es el AUMENTO de viviendas turísticas "
          f"2020M08-2024M08 ({int(c24['vut'] - pb.iloc[0].VUT_ini)}) sobre el alquiler, no el stock; el Banco de España "
          "(IA2025, p. 150) da «cerca del 10 %» con su propio numerador (unas 355.000 en 2025)")
    return {"efecto_medio": efecto, "por_area": por_area, "cuotas": cuotas}


# ------------------------------------------------------------------ ayudas
def tabla_theta() -> pd.DataFrame:
    """Todas las filas de L5 con traslación al alquiler de perceptores (θ = euros de alquiler por euro de ayuda o fracción
    de incidencia), más Fack (2006) y Gibbons y Manning (2006) por su resumen publicado y la θ implícita de
    Grislain-Letrémy y Trevien (2022) en perceptores."""
    l5 = leer(L5)
    meta = {  # estimando: tipo de variación, horizonte, calidad, rigidez de oferta según los autores
        "Fack": ("aumento de la ayuda (extensión de los 90)", "medio (1988-1996) / largo (DDD 1984-2002)", "oferta poco elástica (autor)"),
        "GibbonsManning": ("recorte a nuevos solicitantes", "corto (1996-1997)", "oferta privada poco elástica (autor)"),
        "CollinsonGanong": ("techo de cupón", "medio (hasta 6 años)", "sin dato"),
        "Kangasharju": ("aumento (reforma de 2002)", "medio (1994-2003)", "sin dato"),
        "Viren": ("variación general de la ayuda", "largo (2000-2008)", "sin dato"),
        "HyslopRea": ("aumento zonal (frontera)", "corto (segundo año)", "sin dato"),
        "EerolaEtAl2026": ("aumento (reforma de 2015)", "medio (5 años)", "oferta con cambios modestos (autores)"),
        "GrislainTrevien": ("diferencial de cuantía por zona", "largo (2000-2016)", "inelástica en 3+ habitaciones (autores)"),
    }
    filas = []
    for f in l5:
        if f["ficha"] not in meta or f["medida"].startswith("precio"):
            continue
        txt = f["estimacion"].replace(" a ", "-")
        if f["ficha"] == "GibbonsManning":
            continue    # sus filas de L5 son % de variación del alquiler, no θ; se usa el resumen publicado (abajo)
        if "-" in txt.lstrip("-"):
            a, b = [float(x) for x in txt.split("-")]
            th, lo, hi = (a + b) / 2, a, b
        else:
            th, lo, hi = float(txt), np.nan, np.nan
        se = float(f["ee"]) if f["ee"] else np.nan
        if f["medida"] == "renta regulada":
            continue    # Kangasharju, sector municipal (renta regulada por costes): no es traslación de mercado
        cal = "a calidad constante" if "calidad constante" in f["medida"] or "confort" in f["diseno"] else (
            "incluye calidad (hedónica +0,05)" if f["ficha"] == "CollinsonGanong" else "no ajustada")
        filas.append(dict(estudio=f["autores_anio"], ficha=f["ficha"], theta=th, se=se, lo=lo, hi=hi,
                          detalle=f["unidad_efecto"], fuente=f["fuente_cifra"], calidad=cal, principal=False))
    # cifras publicadas por resumen (no en el CSV)
    filas.append(dict(estudio="Fack (2006)", ficha="Fack", theta=DOC["fack2006_theta"], se=np.nan, lo=np.nan, hi=np.nan,
                      detalle="céntimos de alquiler por euro de ayuda (nuevos perceptores)", fuente="resumen (Labour Economics)",
                      calidad="no ajustada", principal=True))
    filas.append(dict(estudio="Gibbons y Manning (2006)", ficha="GibbonsManning",
                      theta=(DOC["gm2006_theta_min"] + DOC["gm2006_theta_max"]) / 2, se=np.nan,
                      lo=DOC["gm2006_theta_min"], hi=DOC["gm2006_theta_max"],
                      detalle="fracción de la incidencia del recorte sobre el arrendador", fuente="resumen (JPubE); en la "
                      "versión de 2003 la caída en perceptores desaparece con tendencias por antigüedad", calidad="no ajustada",
                      principal=True))
    rr = DOC["glt_b"] * DOC["glt_renta"]
    filas.append(dict(estudio="Grislain-Letrémy y Trevien (2022)", ficha="GrislainTrevien",
                      theta=rr / ((DOC["glt_ayuda_ej_min"] + DOC["glt_ayuda_ej_max"]) / 2),
                      se=DOC["glt_se"] * DOC["glt_renta"] / ((DOC["glt_ayuda_ej_min"] + DOC["glt_ayuda_ej_max"]) / 2),
                      lo=rr / DOC["glt_ayuda_max"], hi=rr / DOC["glt_ayuda_min"],
                      detalle="θ implícita: 0,052 log × 454 euros / diferencial de ayuda (22-27 euros; rango 15-40)",
                      fuente="tablas 1 y 7 (docs/v17/referencias/no_beneficiarios.md); cálculo del auditor",
                      calidad="sin efecto en calidad (autores)", principal=True))
    t = pd.DataFrame(filas)
    # columna principal por estudio: la primera fila de L5 de cada ficha, salvo Fack (resumen de 2006)
    for fi in t.ficha.unique():
        if not t[(t.ficha == fi) & t.principal].shape[0]:
            t.loc[t[t.ficha == fi].index[0], "principal"] = True
    t["variacion"] = t.ficha.map(lambda k: meta[k][0])
    t["horizonte"] = t.ficha.map(lambda k: meta[k][1])
    t["rigidez"] = t.ficha.map(lambda k: meta[k][2])
    t["z_theta_lt_1"] = (1 - t.theta) / t.se
    t["p_unilateral_theta_lt_1"] = [0.5 * math.erfc(z / math.sqrt(2)) if math.isfinite(z) else np.nan for z in t.z_theta_lt_1]
    t["contrasta_theta_lt_1"] = np.where(t.se.isna(), "sin e.e.: no contrastable",
                                         np.where(t.p_unilateral_theta_lt_1 < 0.05, "sí (p < 0,05)", "no"))
    return t


def ayudas() -> dict:
    t = tabla_theta()
    pr = t[t.principal].set_index("ficha").theta
    siete = pr.drop("GrislainTrevien")
    med7 = statistics.median(siete)
    hecho("AYU-TRASLACION-MEDIANA", "Traslación al alquiler de las ayudas a perceptores (θ), mediana de siete estudios con "
          "diseño, un valor por estudio (valor: mediana; min/max: Eerola et al. 2026 y Fack 2006)",
          100 * med7, 100 * siete.min(), 100 * siete.max(), "% de la ayuda", "1984-2020",
          "Francia, Reino Unido, EE. UU., Finlandia, Nueva Zelanda",
          "docs/v16/literatura/L5_ayudas_demanda_efectos.csv; Fack (2006) y Gibbons y Manning (2006), resúmenes",
          "juicio experto", "ayudas_demanda",
          "id citado en ERRATA.md (P1); la tabla completa y las sensibilidades están en la ficha; θ < 1 contrastado "
          "solo donde hay e.e.")
    hecho("AYU-RETIENE-MEDIANA", "Parte de la ayuda al alquiler que retiene el perceptor (1 - θ), mediana de los mismos siete "
          "estudios (valor: mediana; min/max: Fack 2006 y Eerola et al. 2026)", 100 * (1 - med7), 100 * (1 - siete.max()),
          100 * (1 - siete.min()), "% de la ayuda", "1984-2020", "ídem", "ídem", "juicio experto", "ayudas_demanda",
          "identidad coste neto = renta - ayuda: vale a calidad constante y mientras dure la ayuda")
    sens = {
        "ocho_con_GLT": statistics.median(pr),
        "sin_CollinsonGanong": statistics.median(siete.drop("CollinsonGanong")),
        "sin_GibbonsManning": statistics.median(siete.drop("GibbonsManning")),
        "ocho_sin_CollinsonGanong": statistics.median(pr.drop("CollinsonGanong")),
        "aumentos": statistics.median(pr[["Fack", "Kangasharju", "HyslopRea", "EerolaEtAl2026", "GrislainTrevien"]]),
        "corto_plazo": statistics.median(pr[["GibbonsManning", "HyslopRea"]]),
        "medio_largo": statistics.median(pr.drop(["GibbonsManning", "HyslopRea"])),
    }
    hecho("AYU-TRASLACION-SENS", "Traslación mediana con otras composiciones (valor: ocho estudios con la θ implícita de "
          "Grislain-Letrémy y Trevien; min/max: extremos de las sensibilidades de la ficha)",
          100 * sens["ocho_con_GLT"], 100 * min(sens.values()), 100 * max(sens.values()), "% de la ayuda", "1984-2020",
          "ídem", "ídem; docs/v17/referencias/no_beneficiarios.md", "juicio experto", "ayudas_demanda",
          "; ".join(f"{k} = {100 * v:.1f} %" for k, v in sens.items()))
    # duración: el bono dura 24 meses; el contrato, 60 (LAU). Si el arrendador sube la renta θ·ayuda durante todo el contrato:
    def neto(theta, meses_contrato):
        return DOC["bono_eur_mes"] * (DOC["bono_meses"] - theta * meses_contrato)
    hecho("AYU-BONO-DURACION", "Ganancia neta del perceptor del Bono Alquiler Joven en todo el contrato si la subida θ·250 "
          "se mantiene los 60 meses de la LAU y la ayuda solo dura 24 (valor: θ = mediana de siete estudios; min/max: "
          "θ de Fack 2006 y de Eerola et al. 2026)", neto(med7, DOC["lau_meses_min"]), neto(siete.max(), DOC["lau_meses_min"]),
          neto(siete.min(), DOC["lau_meses_min"]), "euros por contrato", "escenario",
          "España (sin evaluación propia)", "RD 42/2022, arts. 11-12; Ley 29/1994, art. 9; θ de la literatura",
          "juicio experto", "ayudas_demanda",
          f"umbral: la ganancia es negativa si θ > {DOC['bono_meses'] / DOC['lau_meses_min']:.2f}; con traslación "
          "limitada al periodo de la ayuda la ganancia es 250·(1-θ)·24")
    inf = leer(INF)
    q7 = fila(inf, id_resultado="Q7")
    hecho("AYU-Q7", "Q7a (V16) con inferencia convencional: diferencia en discontinuidades del log del alquiler en el corte de "
          "35 años (valor: estimación; min/max: IC 95 %)", float(q7["estimacion_publicada"]), float(q7["ic95_lo"]),
          float(q7["ic95_hi"]), "Δlog", "2018-2021 / 2023-2025", "inquilinos de mercado de la ECV",
          "output/v17/lectura_bde/v15_v16_micro/inferencia.csv (Q7); id publicado V16-Q7-1", "no se puede saber",
          "ayudas_demanda", f"p = {q7['p_conv']}; distorsión sin medir; placebos de edad del mismo orden (V16-Q7-4)")
    return {"tabla": t, "mediana7": med7, "sens": sens}


def cifra_publicada(ide: str) -> str:
    return fila(leer(CIFRAS), id=ide)["valor"]


def main() -> dict:
    global REG
    HECHOS.clear()
    REG = Registry(REGISTRO)
    r = {"topes": topes_literatura(), "topes_inc": topes_descomposicion(), "turistica": turistica(), "ayudas": ayudas()}
    r["publicadas"] = {i: cifra_publicada(i) for i in ("V9-D1b-renta-att", "V9-D1b-contratos-att", "V9-D1a-contratos-att",
                                                         "B4-v3-vut-cantidad", "V16-Q7-1", "D1-H11")}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(HECHOS, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    REG.flush()
    return r


if __name__ == "__main__":
    res = main()
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 30)
    print(res["topes_inc"]["tabla"].round(4).to_string())
    print({k: v for k, v in res["topes_inc"].items() if k != "tabla"})
    print(res["ayudas"]["tabla"][["estudio", "theta", "se", "lo", "hi", "calidad", "variacion", "horizonte", "rigidez",
                                  "contrasta_theta_lt_1", "principal", "fuente"]].round(3).to_string())
    print(json.dumps({k: round(v, 4) for k, v in res["ayudas"]["sens"].items()}), res["ayudas"]["mediana7"])
    print({str(k): {kk: round(float(vv), 3) for kk, vv in v.items()} for k, v in res["turistica"]["cuotas"].items()})
    print(json.dumps(res["publicadas"], ensure_ascii=False))

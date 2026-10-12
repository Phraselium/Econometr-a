"""Segunda doble implementacion (L2, v6.2), a ciegas: sigue SOLO output/v6_2/anexo_metodologico.md.

Cada funcion devuelve (valor, min, max). Determinista, sin red, SEED=20261010.
Capa C4 (documentacion/verificacion). Lee solo data/raw y las tablas intermedias que el anexo cita.
"""
from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261010
RAIZ = Path(__file__).resolve().parents[2]
RAW = RAIZ / "data" / "raw"


@lru_cache(maxsize=None)
def _csv(rel: str, **kw) -> pd.DataFrame:
    return pd.read_csv(RAW / rel, **kw)


# ----------------------------------------------------------------- hogares
def _ecp() -> pd.Series:
    d = _csv("ine_hogares_60131.csv")
    d = d[d.nombre == "Total Nacional. Total. Hogares en viviendas familiares. Número."]
    return d.drop_duplicates("periodo").set_index("periodo")["valor"].astype(float)


def _epa() -> pd.Series:
    d = _csv("ine_epa_hogares.csv")
    d = d[d.nombre == "Hogares. Total Nacional. Ambos sexos. Total. Total."]
    return d.drop_duplicates("periodo").set_index("periodo")["valor"].astype(float) * 1000.0


def dh_2125():
    epa, ecp = _epa(), _ecp()
    m = lambda y: np.mean([epa[f"{y}T{q}"] for q in range(1, 5)])  # noqa: E731
    v_epa = m(2025) - m(2021)
    v_ecp = ecp["2025T1"] - ecp["2021T1"]
    lo, hi = min(v_epa, v_ecp), max(v_epa, v_ecp)
    return (lo + hi) / 2, lo, hi


# ------------------------------------------------------------- terminadas
def _miv_serie(fichero: str, serie: str) -> pd.Series:
    d = _csv(fichero)
    d = d[d.serie == serie].copy()
    d["a"] = d.periodo.astype(str).str[:4].astype(int)
    return d.groupby("a")["valor"].sum().astype(float)


def _term(territorio: str | None = None) -> pd.Series:
    """libres + protegidas definitivas anuales. territorio: None=nacional, o sufijo ccaa."""
    suf = "nacional" if territorio is None else f"ccaa_{territorio}"
    lib = _miv_serie("mivau_v2_iniciadas_terminadas_prov.csv", f"viv_libres_terminadas_anual_{suf}")
    pro = _miv_serie("mivau_v2_protegida.csv", f"prot_definitiva_anual_{suf}")
    return lib.add(pro, fill_value=0.0)


def _libres_nac() -> pd.Series:
    return _miv_serie("mivau_v2_iniciadas_terminadas_prov.csv", "viv_libres_terminadas_anual_nacional")


def _pv_na() -> pd.Series:
    return _term("pais_vasco").add(_term("navarra_comunidad_foral_de"), fill_value=0.0)


def terminadas_1924():
    comun = _term() - _pv_na()
    s = comun.loc[2019:2024]
    return float("nan"), float(s.min()), float(s.max())


def _parque_bajas():
    d = _csv("mivau_parque.csv")
    d = d[d.serie == "parque_total_viviendas_nacional"].copy()
    d["a"] = d.periodo.astype(int)
    suma = d.set_index("a").loc[2020:2023, "valor"].sum()
    return 0.001 * suma, 0.002 * suma


@lru_cache(maxsize=None)
def _catastro_altas() -> float:
    c = _csv("catastro_urbana_municipios.csv.gz")
    c = c[c.unidad == "unidades_urbanas_residenciales"]
    uu = c.groupby("periodo")["valor"].sum()
    return float(sum(uu[y + 1] - uu[y] for y in range(2021, 2025)))


def _hogares_variantes() -> dict[str, float]:
    epa, ecp = _epa(), _ecp()
    base = epa["2024T4"] - epa["2020T4"]
    salto = epa["2021T1"] - epa["2020T4"]
    d = epa.diff()
    b = base - salto + np.mean([d["2020T4"], d["2021T2"]])
    b4 = base - salto + np.mean([d["2020T3"], d["2020T4"], d["2021T2"], d["2021T3"]])
    d1 = ecp["2024T4"] - epa["2020T4"] * (ecp["2021T1"] / epa["2021T1"])
    m2020 = np.mean([d[f"2020T{q}"] for q in range(1, 5)])
    d2 = ecp["2024T4"] - (ecp["2021T1"] - m2020)
    return {
        "v1": base + 242400.0, "a": base, "b": b, "b4": b4, "c": base - salto,
        "d1": d1, "d2": d2, "e": ecp["2024T4"] - ecp["2021T1"],
    }


def _terminadas_fuentes() -> dict[str, float]:
    with_p = float((_term().loc[2021:2024]).sum())
    sin_p = float(_libres_nac().loc[2021:2024].sum())
    pvna = float(_pv_na().loc[2021:2024].sum())
    return {"con_prot": with_p, "sin_prot": sin_p, "catastro": _catastro_altas() + pvna}


def _def_sin_bajas() -> list[float]:
    h, t = _hogares_variantes(), _terminadas_fuentes()
    return [hv - tv for hv in h.values() for tv in t.values()]


def L3_DEF_2124_SINBAJAS():
    x = _def_sin_bajas()
    lo, hi = min(x), max(x)
    return (lo + hi) / 2, lo, hi


def L3_DEF_2124_CONBAJAS():
    x = _def_sin_bajas()
    b01, b02 = _parque_bajas()
    lo = min(x)
    hi = max(x) + b02
    return (lo + hi) / 2, lo, hi


# ------------------------------------------------------------- alquiler
def _nucleo(vals: dict[str, float], tol: float = 0.15) -> list[str]:
    """Mayor conjunto de fuentes con (1+max)/(1+min)-1 <= tol (variaciones en fraccion)."""
    ks = sorted(vals, key=vals.get)
    mejor: list[str] = []
    for i in range(len(ks)):
        for j in range(i, len(ks)):
            if (1 + vals[ks[j]]) / (1 + vals[ks[i]]) - 1 <= tol and j - i + 1 > len(mejor):
                mejor = ks[i:j + 1]
    return mejor


def A23_A2():
    ipc = _csv("ine_ipc_alquiler.csv")
    ipc = ipc[ipc.nombre == "Nacional. Alquiler de vivienda. Índice."].copy()
    ipc["a"] = ipc.periodo.str[:4].astype(int)
    m = ipc.groupby("a")["valor"].mean()
    v = _csv("ine_v2_ipva.csv")
    v = v[(v.nivel == "nacional") & (v.medida == "IPVA_indice")]
    tot = v[v.desglose == "Total"].set_index("periodo")["valor"]
    ex = v[v.desglose == "Contrato existente"].set_index("periodo")["valor"]
    s = _csv("pdf/serpavi_esp_agregado.csv")
    s = s[s.serie == "SERPAVI_ESP_VC_alquiler_m2_mediana_pond_composicion_constante"].set_index("periodo")["valor"]
    var = {
        "ipc": m[2024] / m[2015] - 1,
        "ipva_total": tot[2024] / tot[2015] - 1,
        "ipva_existente": ex[2024] / 100.0 - 1,
        "serpavi": s[2024] / s[2015] - 1,
    }
    nuc = _nucleo(var)
    x = [var[k] * 100 for k in nuc]
    return float("nan"), min(x), max(x)


def A23_P2():
    v = _csv("mivau_valor_tasado_nacional_ccaa_prov.csv")
    v = v[v.serie == "valor_tasado_libre_nacional"].copy()
    v["a"] = v.periodo.str[:4].astype(int)
    mv = v.groupby("a")["valor"].mean()
    n = _csv("pdf/notariado_cgn_extranjeros_semestral.csv")
    n = n[(n.serie == "precio_m2") & (n.categoria == "Total general")].copy()
    n["a"] = n.periodo.str[:4].astype(int)
    g = n.groupby("a")["valor"].agg(["mean", "count"])
    g = g[g["count"] == 2]["mean"]
    r = _csv("pdf/registradores_opendata_anual.csv")
    r = r[(r.serie == "compraventas_viv_pm2") & (r.nivel == "nacional")].set_index("periodo")["valor"]
    var = {
        "mivau": mv[2025] / mv[2015] - 1,
        "notariado": g[2025] / g[2015] - 1,
        "registradores": r[2025] / r[2015] - 1,
    }
    x = [var[k] * 100 for k in _nucleo(var)]
    return float(np.median(x)), min(x), max(x)


def _clave(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.split(r"[/,]", s)[0]
    return re.sub(r"[^a-z]", "", s)


def A23_A10():
    v = _csv("ine_v2_ipva.csv")
    v = v[(v.nivel == "provincia") & (v.tabla == 59005) & (v.medida == "IPVA_indice") & (v.desglose == "Nuevo contrato")]
    var, pes = {}, {}
    s = _csv("pdf/serpavi_provincias.csv")
    s = s[(s.variable == "n_contratos") & (s.tipologia == "VC") & (s.periodo == 2024)]
    peso = {_clave(n): w for n, w in zip(s.nombre, s.valor)}
    for terr in ["Alicante/Alacant", "Castellón/Castelló", "Valencia/València"]:
        x = v[v.territorio == terr].set_index("periodo")["valor"]
        var[terr] = x[2024] / x[2021] - 1
        pes[terr] = peso[_clave(terr)]
    ponder = sum(var[k] * pes[k] for k in var) / sum(pes.values())
    med = {}
    for a in (2021, 2024):
        g = pd.read_csv(RAW / "v5" / f"gva_fianzas_{a}.csv", sep=";")
        i = g[(g.importe_fianza >= 100) & (g.importe_fianza <= 5000)]["importe_fianza"]
        med[a] = float(i.median())
    fian = med[2024] / med[2021] - 1
    var2 = {"ipva": ponder, "fianzas": fian}
    x = [var2[k] * 100 for k in _nucleo(var2)]
    return float(np.mean(x)), min(x), max(x)


# ---------------------------------------------------------------- R1C
def R1C_001():
    e = _csv("v3/eff_tenencia_edad_v3.csv")
    eff = e[(e.serie == "eff_pct_hogares_vivienda_principal|edad=total|ed=DO 2413 (EFF2022)") & (e.periodo == 2022)]["valor"].iloc[0]
    c = _csv("v3/ine_ecv_tenencia_edad_v3.csv")
    ecv = c[(c.serie == "ecv_pct_hogares_tenencia|Propiedad|edad_persona_referencia=Total|sexo=Ambos sexos") & (c.periodo == 2022)]["valor"].iloc[0]
    t = _csv("v4/ine_v4_t59523.csv")
    num = t[t.serie_nombre == "Total Nacional, En propiedad, Total (tamaño de municipio)"]["valor"].iloc[0]
    den = t[t.serie_nombre == "Total Nacional, Total (régimen de tenencia), Total (tamaño de municipio)"]["valor"].iloc[0]
    x = [float(eff), float(ecv), 100.0 * num / den]
    return float(np.mean(x)), min(x), max(x)


# ------------------------------------------------------------------ B4
def B4_v3_vut_cantidad():
    v = _csv("ine_v2_vut.csv")
    v = v[(v.nivel == "nacional") & (v.medida == "viviendas_turisticas")].set_index("periodo")["valor"]
    dvut = v["2024M08"] - v["2020M08"]
    g = _csv("v3/ine_v3_censo2021_seccion_indicadores.csv.gz")
    stock1 = g[g.serie == "t20_2"]["valor"].sum()
    c = _csv("v3/ine_ecv_tenencia_edad_v3.csv")
    pct = 0.0
    for t in ("Alquiler a precio de mercado", "Alquiler inferior al precio de mercado"):
        pct += c[(c.serie == f"ecv_pct_hogares_tenencia|{t}|edad_persona_referencia=Total|sexo=Ambos sexos") & (c.periodo == 2021)]["valor"].iloc[0]
    stock2 = pct / 100.0 * _ecp()["2021T4"]
    a, b = 100 * dvut / stock1, 100 * dvut / stock2
    return float(a), float(min(a, b)), float(max(a, b))


# ----------------------------------------------------------- convivencia
def latente_convivencia():
    e = _csv("v3/eurostat_emancipacion_tenencia_v3.csv")
    e = e[e.fuente.str.contains("lvps08") & e.serie.str.contains("Y25-34_T_con_padres") & (e.codigo == "ES")].set_index("periodo")["valor"]
    d_eu = e[2025] - e[2008]
    ser = json.load(open(RAW / "v3" / "pa_aux" / "ine_t65944.json"))
    pat = re.compile(r"Total Nacional\. Ambos sexos\. De (25 a 29|30 a 34) años\. (Total|Hijo/a)\. Personas")
    acc: dict[tuple[int, str], float] = {}
    for s in ser:
        m = pat.search(s["Nombre"])
        if m:
            for r in s["Data"]:
                if r["Anyo"] in (2008, 2025):
                    acc[(r["Anyo"], m.group(2))] = acc.get((r["Anyo"], m.group(2)), 0.0) + r["Valor"]
    tasa = {a: acc[(a, "Hijo/a")] / acc[(a, "Total")] * 100 for a in (2008, 2025)}
    pob = acc[(2025, "Total")] * 1000
    d_epa = tasa[2025] - tasa[2008]
    esc = [d / 100 * pob / p for d in (d_eu, d_epa) for p in (1.5, 2.0)]
    return float("nan"), round(min(esc), -3), round(max(esc), -3)


# -------------------------------------------------------------- B1 / F
def _proy():
    h = _csv("v5/ine_b1_t54562_proy_hogares.csv")
    h = h[h.nombre.str.endswith(". Total. ")].copy()
    h["k"] = h.nombre.str[: -len(". Total. ")].map(_clave)
    p = _csv("v5/ine_b1_t36726_proy_poblacion_prov.csv")
    suf = ". Proyección a corto plazo. Todas las edades. "
    p = p[p.nombre.str.startswith("Total. Población. ") & p.nombre.str.endswith(suf)].copy()
    p["k"] = p.nombre.str[len("Total. Población. "): -len(suf)].map(_clave)
    h = h.drop_duplicates(["k", "anyo"])
    p = p.drop_duplicates(["k", "anyo"])
    provs = pd.read_csv(RAIZ / "output" / "v5" / "A4" / "clasificacion_provincias.csv")["provincia"].map(_clave).tolist()
    return h, p, provs


@lru_cache(maxsize=None)
def _F():
    h, p, provs = _proy()
    hh = h.set_index(["k", "anyo"])["valor"]
    pp = p.set_index(["k", "anyo"])["valor"]
    fi, fa = [], []
    for k in provs:
        fi.append(hh[(k, 2036)] - hh[(k, 2026)])
        fa.append(hh[(k, 2026)] * (pp[(k, 2036)] / pp[(k, 2026)] - 1))
    fi, fa = np.array(fi), np.array(fa)
    return float(fi.sum()), float(np.minimum(fi, fa).sum()), float(np.maximum(fi, fa).sum())


def B1_H4():
    c, lo, hi = _F()
    return c, lo, hi


def E_B1_F():
    return B1_H4()


def B1_H1():
    t = pd.read_csv(RAIZ / "output" / "v5" / "B1" / "tablas" / "B1_nacional.csv").set_index("componente")
    g = lambda c, k: float(t.loc[c, k])  # noqa: E731
    cen = g("A", "central") + g("R", "central") + g("V", "central") + g("F", "central") - g("M", "central") - g("K", "central")
    lo = g("A", "min") + g("R", "min") + g("V", "min") + g("F", "min") - g("M", "max") - g("K", "max")
    hi = g("A", "max") + g("R", "max") + g("V", "max") + g("F", "max") - g("M", "min") - g("K", "min")
    return cen / 10, lo / 10, hi / 10


# ------------------------------------------------------------------ D1
EPS_D = (0.3, 0.6, 1.0, 1.5)


def _d1(clase: int):
    a = pd.read_csv(RAIZ / "output" / "v5" / "A4" / "clasificacion_provincias.csv")
    es = np.clip(a[a.clase_2021_2025 == clase]["resp_oferta"].astype(float).to_numpy(), 0, None)
    lo, ce, hi = (float(np.percentile(es, q)) for q in (25, 50, 75))
    inc = lambda e, d: 100.0 * d / (e + d)  # noqa: E731
    todas = [inc(e, d) for e in (lo, ce, hi) for d in EPS_D]
    central = float(np.median([inc(ce, d) for d in EPS_D]))
    return central, min(todas), max(todas)


def D1_H11():
    return _d1(1)


def D1_H12():
    return _d1(2)

"""V16-F2.2a · Contabilidad de la variación del número de hogares (shift-share exacto; C4, sin lectura causal).

Amplía V12-B3 (descomposición 2011-2021 con censos, ya hecha: NO se repite) a 2021-2026 con ECP y EPA, y a 2002-2021 con EPA.

Identidad. Grupos g = nacionalidad (española, extranjera) x edad. H = k · Σ_g N · m_n · s_(a|n) · h_g, con N población total, m_n cuota de la
nacionalidad n, s_(a|n) estructura por edad dentro de la nacionalidad y h_g la tasa de jefatura por grupo del Censo 2021 (microdatos,
data/raw/v11) con un factor k que hace que el nivel inicial reproduzca los hogares observados. Se contabilizan:
  población (N), composición por nacionalidad (m: extranjera frente a española; incluye cambios de nacionalidad), estructura por edad (s),
  y jefatura (cambio de la tasa de jefatura agregada a población constante: residuo exacto H1 − k·V(1,1,1)).
Los tres factores demográficos se reparten por Shapley (media de los 6 órdenes; rango = mínimo y máximo de los órdenes). La suma de los cuatro
reproduce EXACTAMENTE el cambio observado. No hay tasas de jefatura por edad observadas después de 2021: la jefatura es un residuo agregado.
Muestra: nacional (publicado) y CCAA y provincias NO selladas de v6 (K8: las 8 CCAA con provincias selladas no se calculan).
Fuentes: ECP (INE, t60129, hogares t60133/60131), EPA hogares (data/base/hechos.parquet, muestra_sellada_v6 == False), padrón por edad y
nacionalidad (data/raw/ine_v2_padron_prov_edad_nac.csv, agregados nacionales), EMCR (data/processed/v16/tension_social.parquet).
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
SEED = 20261010
SELLADAS_V6 = ["07", "22", "26", "28", "30", "31", "33", "35", "38", "44", "50"]
EDADES = ["0-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69",
          "70-74", "75-79", "80-84", "85+"]
EDAD4 = {"0-14": "0-19", "15-19": "0-19", "20-24": "20-34", "25-29": "20-34", "30-34": "20-34", "65-69": "65+", "70-74": "65+",
         "75-79": "65+", "80-84": "65+", "85+": "65+"}
for _e in EDADES[5:11]:
    EDAD4[_e] = "35-64"
NACS = ["ES", "EXT"]
HECHOS = RAIZ / "data/base/hechos.parquet"


# ---------------------------------------------------------------- datos
def _ccaa_de_provincia() -> dict:
    t = pd.read_parquet(RAIZ / "data/base/territorios.parquet")
    return t[t.nivel == "provincia"].set_index("territorio_codigo").cod_ccaa.to_dict()


def _nombres_ccaa() -> dict:
    t = pd.read_parquet(RAIZ / "data/base/territorios.parquet")
    return t[t.nivel == "ccaa"].set_index("territorio_codigo").nombre.to_dict()


def provincias_libres() -> list[str]:
    """Provincias INE (01-52) menos las 11 selladas v6. Comprueba que la marca de la base coincide con K8."""
    marc = duckdb.sql(f"select distinct territorio_codigo c from '{HECHOS}' where nivel='provincia' and muestra_sellada_v6").df().c
    assert set(marc) <= set(SELLADAS_V6), "la base marca provincias distintas de K8"
    return [f"{i:02d}" for i in range(1, 53) if f"{i:02d}" not in SELLADAS_V6]


def ccaa_libres() -> dict:
    """CCAA cuyas provincias están TODAS fuera de la muestra sellada: {cod_ccaa: [provincias]}."""
    m = _ccaa_de_provincia()
    out: dict = {}
    for p, c in m.items():
        out.setdefault(c, []).append(p)
    return {c: sorted(ps) for c, ps in out.items() if not set(ps) & set(SELLADAS_V6)}


def pob_ecp() -> pd.DataFrame:
    """ECP t60129: territorio ('NAC' o cpro), fecha, nac, grupo_edad, poblacion (1 de enero, 16 grupos)."""
    e = pd.read_csv(RAIZ / "data/raw/v11/ine_ecp/ecp_t60129.csv.gz", dtype=str)
    e = e[(e.Nacionalidad != "Total") & e.Periodo.str.startswith("1 de enero")]
    e["terr"] = np.where(e.Provincias == "Total Nacional", "NAC", e.Provincias.str[:2])
    e = e[(e.terr == "NAC") | e.terr.str.fullmatch(r"\d{2}")]
    ini = e["Grupo quinquenal de edad"].str.extract(r"(\d+)")[0].astype(float)
    e = e[ini.notna()].copy()
    ini = ini[ini.notna()]
    e["grupo_edad"] = pd.cut(ini, [-1, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 84, 200], labels=EDADES).astype(str)
    e["nac"] = e.Nacionalidad.map({"Española": "ES", "Extranjera": "EXT"})
    e["poblacion"] = pd.to_numeric(e.Total.str.replace(".", "", regex=False), errors="coerce")
    e["anio"] = e.fecha.str[:4].astype(int)
    return e.groupby(["terr", "anio", "nac", "grupo_edad"], as_index=False).poblacion.sum()


def hogares_ecp() -> pd.DataFrame:
    h = pd.read_csv(RAIZ / "data/raw/ine_v2_hogares_prov.csv", dtype={"codigo": str})
    h = h[(h.desglose == "tamaño=Total") & h.periodo.str.endswith("T1")]
    h = h.assign(anio=h.periodo.str[:4].astype(int), terr=np.where(h.nivel == "nacional", "NAC", h.codigo.str.zfill(2)))
    return h[["terr", "anio", "valor"]].rename(columns={"valor": "hogares"})


def hogares_epa() -> pd.Series:
    """EPA, hogares totales (miles x 1000), primer trimestre de cada año, del hecho de la base (filas no selladas)."""
    d = duckdb.sql(f"select periodo, valor from '{HECHOS}' where variable='hogares_epa' and nivel='nacional' and not muestra_sellada_v6 "
                   "and periodo like '%T1'").df()
    return pd.Series(d.valor.values * 1000.0, index=d.periodo.str[:4].astype(int).values).sort_index()


def censo_jefatura(anio: int) -> pd.DataFrame:
    f = RAIZ / f"data/raw/v11/ine_censos_microdatos/jefatura_{anio}.csv.gz"
    j = pd.read_csv(f, dtype={"cpro": str, "cmun": str})
    j["cpro"] = j.cpro.str.zfill(2)
    return j


def tasas_jefatura(j: pd.DataFrame, provs: list[str] | None, minimo: int = 50, nacional: pd.DataFrame | None = None) -> pd.DataFrame:
    """Tasa de jefatura (referencias/personas) por nac x edad. Si la celda tiene < `minimo` personas en la muestra se usa la tasa nacional."""
    x = j if provs is None else j[j.cpro.isin(provs)]
    g = x.groupby(["nac", "grupo_edad"])[["personas", "referencias", "personas_muestra"]].sum()
    r = (g.referencias / g.personas.where(g.personas > 0)).rename("h")
    out = pd.concat([r, g.personas_muestra], axis=1).reindex(pd.MultiIndex.from_product([NACS, EDADES], names=["nac", "grupo_edad"]))
    if nacional is not None:
        pobre = out.personas_muestra.fillna(0) < minimo
        out.loc[pobre, "h"] = nacional.reindex(out.index[pobre]).h.values
    out["h"] = out.h.fillna(0.0)
    return out


def vec(df: pd.DataFrame, terr, anio: int, grupos: list[str] = EDADES) -> np.ndarray:
    """Población (2 x n_edades) de la(s) unidad(es) `terr` (lista) en el 1 de enero `anio`."""
    x = df[(df.terr.isin(terr)) & (df.anio == anio)].groupby(["nac", "grupo_edad"]).poblacion.sum()
    return x.reindex(pd.MultiIndex.from_product([NACS, grupos])).fillna(0.0).values.reshape(2, len(grupos))


# ---------------------------------------------------------------- núcleo contable
def _estado(P: np.ndarray):
    N = P.sum()
    pn = P.sum(axis=1)
    m = pn / N
    s = P / np.where(pn[:, None] > 0, pn[:, None], 1.0)
    return N, m, s


def descomponer(P0: np.ndarray, P1: np.ndarray, h: np.ndarray, H0: float, H1: float) -> dict:
    """Contabilidad exacta de H1 − H0. P0, P1, h: arrays (2 x n_edades). Devuelve componentes (Shapley + rango de órdenes)."""
    s0, s1 = _estado(P0), _estado(P1)

    def V(sel):  # sel = (tamaño, composición, estructura): 0 → estado inicial, 1 → final
        N = (s0, s1)[sel[0]][0]
        m = (s0, s1)[sel[1]][1]
        s = (s0, s1)[sel[2]][2]
        return float((N * m[:, None] * s * h).sum())

    k = H0 / V((0, 0, 0))
    v = {c: k * V(c) for c in itertools.product((0, 1), repeat=3)}
    nombres = ["poblacion", "composicion_nacionalidad", "estructura_edad"]
    ordenes = list(itertools.permutations(range(3)))
    contrib = {n: [] for n in nombres}
    for o in ordenes:
        est = [0, 0, 0]
        for f in o:
            antes = v[tuple(est)]
            est[f] = 1
            contrib[nombres[f]].append(v[tuple(est)] - antes)
    r = {n: float(np.mean(c)) for n, c in contrib.items()}
    r.update({f"{n}_min": float(np.min(c)) for n, c in contrib.items()})
    r.update({f"{n}_max": float(np.max(c)) for n, c in contrib.items()})
    r["jefatura_residuo"] = float(H1 - v[(1, 1, 1)])
    r["cambio_observado"] = float(H1 - H0)
    r["suma_componentes"] = float(sum(r[n] for n in nombres) + r["jefatura_residuo"])
    r["error_identidad"] = r["suma_componentes"] - r["cambio_observado"]
    r["H0"], r["H1"], r["k"] = float(H0), float(H1), float(k)
    r["jefatura_agregada_pct"] = float(100 * (H1 / v[(1, 1, 1)] - 1))
    # vista alternativa aditiva exacta: aportación de cada nacionalidad a tasas de jefatura iniciales constantes
    dP = (P1 - P0) * h * k
    r["nac_ES"], r["nac_EXT"] = float(dP[0].sum()), float(dP[1].sum())
    r["pobl_ES"], r["pobl_EXT"] = float(P1[0].sum() - P0[0].sum()), float(P1[1].sum() - P0[1].sum())
    r["pobl0"], r["pobl1"] = float(P0.sum()), float(P1.sum())
    r["pct_ext_0"], r["pct_ext_1"] = float(100 * P0[1].sum() / P0.sum()), float(100 * P1[1].sum() / P1.sum())
    return r


# ---------------------------------------------------------------- bloques
def bloque_ecp(desde: int, hasta: int, smoke: bool = False) -> pd.DataFrame:
    """2021→2025/2026 con ECP: España, CCAA libres y provincias libres."""
    pop, hog = pob_ecp(), hogares_ecp()
    j21 = censo_jefatura(2021)
    nac_t = tasas_jefatura(j21, None)
    hg = hog.set_index(["terr", "anio"]).hogares
    provs = provincias_libres()
    ccaa = ccaa_libres()
    nom = _nombres_ccaa()
    unidades = [("nacional", "NAC", "España", None, ["NAC"])]
    unidades += [("ccaa", c, nom.get(c, c), ps, ps) for c, ps in sorted(ccaa.items())]
    unidades += [("provincia", p, p, [p], [p]) for p in provs]
    if smoke:
        unidades = unidades[:4]
    filas = []
    for nivel, cod, nombre, pj, pp in unidades:
        h = tasas_jefatura(j21, pj, nacional=nac_t).h.values.reshape(2, -1)
        H0 = float(sum(hg[(t, desde)] for t in pp))
        H1 = float(sum(hg[(t, hasta)] for t in pp))
        r = descomponer(vec(pop, pp, desde), vec(pop, pp, hasta), h, H0, H1)
        r.update(nivel=nivel, codigo=cod, nombre=nombre, fuente_hogares="ECP", desde=desde, hasta=hasta)
        filas.append(r)
    return pd.DataFrame(filas)


def bloque_ecp_anual(smoke: bool = False) -> pd.DataFrame:
    """Pasos anuales 2021→2022 … 2025→2026 (nacional) con ECP."""
    pop, hog = pob_ecp(), hogares_ecp()
    hg = hog.set_index(["terr", "anio"]).hogares
    h = tasas_jefatura(censo_jefatura(2021), None).h.values.reshape(2, -1)
    filas = []
    for a in range(2021, 2026):
        r = descomponer(vec(pop, ["NAC"], a), vec(pop, ["NAC"], a + 1), h, float(hg[("NAC", a)]), float(hg[("NAC", a + 1)]))
        r.update(nivel="nacional", codigo="NAC", nombre="España", fuente_hogares="ECP", desde=a, hasta=a + 1)
        filas.append(r)
    return pd.DataFrame(filas)


def bloque_epa_reciente(desde: int, hasta: int) -> dict:
    """Mismos factores demográficos (ECP), hogares de la EPA."""
    pop = pob_ecp()
    he = hogares_epa()
    h = tasas_jefatura(censo_jefatura(2021), None).h.values.reshape(2, -1)
    r = descomponer(vec(pop, ["NAC"], desde), vec(pop, ["NAC"], hasta), h, float(he[desde]), float(he[hasta]))
    r.update(nivel="nacional", codigo="NAC", nombre="España", fuente_hogares="EPA", desde=desde, hasta=hasta)
    return r


def pob_padron4() -> pd.DataFrame:
    p = pd.read_csv(RAIZ / "data/raw/ine_v2_padron_prov_edad_nac.csv", dtype={"codigo": str})
    p = p[(p.nivel == "nacional") & (p.nombre_ine == "Suma de grupos quinquenales INE (agregado)")]
    d = p.desglose.str.extract(r"nacionalidad=(\w+); edad=(.+)")
    p = p.assign(nacn=d[0], edad=d[1], anio=p.periodo.str[:4].astype(int))
    p = p[p.nacn.isin(["Española", "Extranjera"]) & p.edad.isin(["0-19", "20-34", "35-64", "65+"])]
    p["nac"] = p.nacn.map({"Española": "ES", "Extranjera": "EXT"})
    return p.rename(columns={"edad": "grupo_edad", "valor": "poblacion"})[["anio", "nac", "grupo_edad", "poblacion"]].assign(terr="NAC")


def tasas4(anio_censo: int) -> np.ndarray:
    """Tasas de jefatura del censo agregadas a 4 grupos de edad (pesos: personas del propio censo, nacional)."""
    j = censo_jefatura(anio_censo)
    g = j.groupby(["nac", "grupo_edad"])[["personas", "referencias"]].sum().reindex(pd.MultiIndex.from_product([NACS, EDADES]))
    g["g4"] = [EDAD4[e] for e in g.index.get_level_values(1)]
    a = g.groupby([g.index.get_level_values(0), "g4"])[["personas", "referencias"]].sum()
    h = (a.referencias / a.personas).reindex(pd.MultiIndex.from_product([NACS, ["0-19", "20-34", "35-64", "65+"]]))
    return h.values.reshape(2, 4)


def bloque_epa_larga() -> pd.DataFrame:
    """2002→2021 (y subperíodos) con EPA y padrón en 4 grupos de edad; referencia Censo 2021 (principal) y Censo 2011 (sensibilidad)."""
    pop, he = pob_padron4(), hogares_epa()
    g4 = ["0-19", "20-34", "35-64", "65+"]
    filas = []
    for ref in (2021, 2011):
        h = tasas4(ref)
        for a, b in [(2002, 2021), (2002, 2008), (2008, 2014), (2014, 2021)]:
            r = descomponer(vec(pop, ["NAC"], a, g4), vec(pop, ["NAC"], b, g4), h, float(he[a]), float(he[b]))
            r.update(nivel="nacional", codigo="NAC", nombre="España", fuente_hogares="EPA", desde=a, hasta=b, referencia_censo=ref)
            filas.append(r)
    return pd.DataFrame(filas)


def emcr_saldo_exterior() -> dict:
    d = duckdb.sql("select periodo, valor from read_parquet('" + str(RAIZ / "data/processed/v16/tension_social.parquet") + "') "
                   "where nivel='nacional' and not muestra_sellada_v6 and variable='ine_emcr_saldo_migratorio_personas' "
                   "and desagregacion='sexo=ambos_sexos;tipo_saldo=saldo_exterior'").df()
    d["anio"] = d.periodo.astype(str).str[:4].astype(int)
    s = d.groupby("anio").valor.sum()
    return {int(k): float(v) for k, v in s.items()}


if __name__ == "__main__":
    t = bloque_ecp(2021, 2025, smoke=True)
    print(t[["nivel", "codigo", "cambio_observado", "poblacion", "composicion_nacionalidad", "estructura_edad", "jefatura_residuo", "error_identidad"]]
          if "poblacion" in t else t.columns)

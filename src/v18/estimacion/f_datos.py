"""V18 · fase 4 · datos de entrenamiento de los modelos de conjunto F1-F3 (y de E7), siempre a través de src/v18/sellado.filtrar.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Nunca abre data/sealed ni ejecuta sellar_*/evaluate_*: lee data/base/hechos.parquet
y los CSV de data/raw y aplica sellado.filtrar, que llama a holdout.excluir_sellados_v6() (unidades de v6) y excluye además las de V15 y V16, los periodos
posteriores al tope de V18 y las ediciones posteriores. Sin red.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v18"))
import sellado  # noqa: E402

HECHOS = RAIZ / "data" / "base" / "hechos.parquet"
RAW = RAIZ / "data" / "raw"
COLS = ["territorio_codigo", "nivel", "periodo", "frecuencia", "variable", "desagregacion", "valor", "edicion", "metodo_dato", "muestra_sellada_v6"]


VARIABLES = ["p_tasado", "deflactor", "renta_hog_real", "tipo_hip_real_bde", "tipo_hip_bde", "pob_total", "pib_vol_idx", "ipv", "valor_tasado",
             "ipc_alquiler_indice", "ipc_alquiler", "parados_epa", "ocupados_epa", "iniciadas_anual_tabla", "terminadas_anual_tabla",
             "serpavi_alquiler_m2_mediana", "credito_promotor", "costes_constr", "valor_tasado_ccaa", "compraventas", "hip_n", "inflacion_ipc_yoy",
             "euribor_1y", "credito_nuevo", "visados"]


@lru_cache(maxsize=1)
def _todo() -> pd.DataFrame:
    """Una sola lectura de la base para todas las variables de F y E7 (la lectura filtrada por variable es lenta)."""
    return pd.read_parquet(HECHOS, columns=COLS, filters=[("variable", "in", VARIABLES)])


@lru_cache(maxsize=None)
def _hechos(variable: str, nivel: str, frec: str) -> pd.DataFrame:
    d = _todo()
    return d[(d.variable == variable) & (d.nivel == nivel) & (d.frecuencia == frec)]


def base(variable: str, nivel: str, frec: str, clave: tuple[str, str, str] | None = None, desag: str | None = None) -> pd.DataFrame:
    """Serie de la base con el filtro de entrenamiento de V18. clave = (variable, nivel, frecuencia) de sellado_v18.json si difiere."""
    df = _hechos(variable, nivel, frec).copy()
    if desag is not None:
        df = df[df.desagregacion == desag]
    v, n, f = clave or (variable, nivel, frec)
    return sellado.filtrar(df, "territorio_codigo", n, "periodo", v, f)


def a_anual(df: pd.DataFrame, agg: str = "mean", sumar_completos: bool = True) -> pd.DataFrame:
    """Anualiza una serie trimestral (periodo 'YYYYTq'): solo años con los cuatro trimestres (regla 1.4 b). Devuelve periodo 'YYYY'."""
    d = df.copy()
    d["anio"] = d.periodo.str[:4]
    g = d.groupby(["territorio_codigo", "anio"]).valor
    out = g.agg(agg).to_frame("valor")
    out["n"] = g.size()
    out = out[out.n == 4].drop(columns="n").reset_index().rename(columns={"anio": "periodo"})
    return out


def anual_con_tope(df_a: pd.DataFrame, variable: str, nivel: str) -> pd.DataFrame:
    """Aplica el filtro de entrenamiento de V18 (clave anual) a una serie ya anualizada."""
    d = df_a.copy()
    d["nivel"] = nivel
    return sellado.filtrar(d, "territorio_codigo", nivel, "periodo", variable, "A")


def anual_de_t(variable: str, nivel: str, agg: str = "mean") -> pd.DataFrame:
    """Media anual (años completos) de una serie trimestral que solo tiene clave anual en sellado_v18.json (regla 1.4 b con e)."""
    return anual_con_tope(a_anual(_hechos(variable, nivel, "T"), agg), variable, nivel)


def trim_idx(df: pd.DataFrame) -> pd.Series:
    s = df.set_index(pd.PeriodIndex(df.periodo.str.replace("T", "Q"), freq="Q")).valor
    return s.sort_index()


# ---------------------------------------------------------------------------------------------- nombres de provincia -> código INE
def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower().strip()
    m = re.match(r"^(.*)\((.*)\)$", s)
    if m:
        s = f"{m.group(2).strip()} {m.group(1).strip()}"
    return s


@lru_cache(maxsize=1)
def _mapa_provincias() -> dict[str, str]:
    t = pd.read_parquet(RAIZ / "data" / "base" / "territorios.parquet")
    t = t[t.nivel == "provincia"]
    m: dict[str, str] = {}
    for _, r in t.iterrows():
        for parte in re.split(r"/", r["nombre"]):
            m[_norm(parte)] = r["territorio_codigo"]
        m[_norm(r["nombre"])] = r["territorio_codigo"]
    m.update({"balears illes": "07", "illes balears": "07", "palmas las": "35", "las palmas": "35", "coruna a": "15", "a coruna": "15",
              "araba alava": "01", "rioja la": "26", "la rioja": "26", "alicante alacant": "03", "valencia valencia": "46"})
    return m


def codigo_provincia(nombre: str) -> str | None:
    m = _mapa_provincias()
    n = _norm(nombre)
    if n in m:
        return m[n]
    for parte in n.split("/"):
        if parte.strip() in m:
            return m[parte.strip()]
    return None


@lru_cache(maxsize=1)
def _ccaa_de_provincia() -> dict[str, str]:
    t = pd.read_parquet(RAIZ / "data" / "base" / "territorios.parquet")
    t = t[t.nivel == "provincia"]
    return dict(zip(t.territorio_codigo, t.padre_codigo))


# ---------------------------------------------------------------------------------------------- series raw con tope
def _raw_prov_anual(fichero: str, filtro, variable: str) -> pd.DataFrame:
    d = pd.read_csv(RAW / fichero)
    d = d[filtro(d)].copy()
    d["territorio_codigo"] = d["territorio"].map(codigo_provincia)
    d = d.dropna(subset=["territorio_codigo"])
    d["periodo"] = d["periodo"].astype(str)
    d["nivel"] = "provincia"
    d["frecuencia"] = "A"
    return sellado.filtrar(d[["territorio_codigo", "nivel", "periodo", "valor"]], "territorio_codigo", "provincia", "periodo", variable, "A")


def pib_provincial() -> pd.DataFrame:
    d = pd.read_csv(RAW / "ine_v2_cre.csv")
    d = d[(d.nivel == "provincia") & (d.medida == "PIB_precios_corrientes")].copy()
    d["territorio_codigo"] = d["codigo"].astype(str).str.zfill(2)
    d["periodo"] = d["periodo"].astype(str)
    d["nivel"] = "provincia"
    return sellado.filtrar(d[["territorio_codigo", "nivel", "periodo", "valor"]], "territorio_codigo", "provincia", "periodo", "pib_provincial_cre", "A")


def parque_provincial() -> pd.DataFrame:
    return _raw_prov_anual("mivau_parque.csv", lambda d: d.nivel == "provincia", "mivau_parque")


def parque_nacional() -> pd.DataFrame:
    d = pd.read_csv(RAW / "mivau_parque.csv")
    d = d[d.nivel == "nacional"][["periodo", "valor"]].copy()
    d["territorio_codigo"] = "00"
    d["nivel"] = "nacional"
    d["periodo"] = d["periodo"].astype(str)
    return sellado.filtrar(d, "territorio_codigo", "nacional", "periodo", "mivau_parque", "A")


def suelo_provincial_anual() -> pd.DataFrame:
    d = pd.read_csv(RAW / "mivau_v2_suelo.csv")
    d = d[(d.nivel == "provincia") & (d.tabla_codigo.astype(str) == "36400500")].copy()
    d["territorio_codigo"] = d["territorio"].map(codigo_provincia)
    d = d.dropna(subset=["territorio_codigo"])
    d["periodo"] = d["periodo"].astype(str)
    q = d[["territorio_codigo", "periodo", "valor"]]
    a = a_anual(q)
    return anual_con_tope(a, "mivau_v2_suelo", "provincia")


def iniciadas_libres_provincial() -> pd.DataFrame:
    """Viviendas libres iniciadas por provincia (MIVAU, anual desde 1991), con la clave mivau_obra_libre_iniciadas|provincia|A."""
    d = pd.read_csv(RAW / "mivau_v2_iniciadas_terminadas_prov.csv")
    d = d[((d.nivel == "provincia") & d.serie.str.startswith("viv_libres_iniciadas_anual_provincia"))
          | ((d.nivel == "ccaa") & (d.territorio == "Cantabria") & d.serie.str.startswith("viv_libres_iniciadas_anual_ccaa"))].copy()
    # Cantabria es uniprovincial y el MIVAU solo la publica como comunidad: se trata como la provincia 39 (misma unidad)
    d["territorio_codigo"] = d["territorio"].map(codigo_provincia)
    d = d.dropna(subset=["territorio_codigo"])
    d["periodo"] = d["periodo"].astype(str)
    d["nivel"] = "provincia"
    return sellado.filtrar(d[["territorio_codigo", "nivel", "periodo", "valor"]], "territorio_codigo", "provincia", "periodo",
                           "mivau_obra_libre_iniciadas", "A")


# ---------------------------------------------------------------------------------------------- nacional trimestral
def nacional_t(con_ipv: bool = False) -> pd.DataFrame:
    """Series nacionales trimestrales de F1-R1 (1996T1-2026T2): ln precio real, ln renta real de los hogares, tipo hipotecario real y nominal, ln población."""
    p = trim_idx(base("p_tasado", "nacional", "T"))
    d = trim_idx(base("deflactor", "nacional", "T"))
    r = trim_idx(base("renta_hog_real", "nacional", "T"))
    tr = trim_idx(base("tipo_hip_real_bde", "nacional", "T"))
    tn = trim_idx(base("tipo_hip_bde", "nacional", "T"))
    pobd = base("pob_total", "nacional", "T")
    pob = trim_idx(pobd)
    interp = pobd.set_index(pd.PeriodIndex(pobd.periodo.str.replace("T", "Q"), freq="Q")).metodo_dato.str.contains("interpol")
    pv = trim_idx(base("pib_vol_idx", "nacional", "T"))
    out = pd.DataFrame({"y": np.log(p / d * 100), "renta": np.log(r), "tipo_real": tr, "tipo_nom": tn, "pob": np.log(pob),
                        "pob_interpolada": interp.reindex(pob.index).fillna(False).astype(bool), "pib": np.log(pv), "defl": d, "p_nom": p})
    if con_ipv:
        out["ipv_real"] = np.log(trim_idx(base("ipv", "nacional", "T")) / d * 100)
    return out.dropna(subset=["y", "renta", "tipo_real", "pob"], how="any")


def nacional_a() -> pd.DataFrame:
    """Medias anuales (años completos, regla 1.4 b) para F1-A2: ln precio real, ln renta real, tipo real, ln población, ln parque per cápita."""
    def anual(var, niv="nacional"):
        q = base(var, niv, "T")
        return anual_con_tope(a_anual(q), var, niv).set_index("periodo").valor
    p, d, r = anual("p_tasado"), anual("deflactor"), anual("renta_hog_real")
    tr = anual("tipo_hip_real_bde")
    pob = anual("pob_total")
    pq = parque_nacional().set_index("periodo").valor
    idx = sorted(set(p.index) & set(d.index) & set(r.index) & set(tr.index) & set(pob.index) & set(pq.index))
    out = pd.DataFrame({"y": np.log(p / d * 100), "renta": np.log(r), "tipo_real": tr, "pob": np.log(pob), "parque_pc": np.log(pq / pob)}).loc[idx]
    out.index = out.index.astype(int)
    return out


# ---------------------------------------------------------------------------------------------- panel provincial anual
def _wide(df: pd.DataFrame, nombre: str) -> pd.Series:
    s = df.assign(periodo=df.periodo.astype(int)).set_index(["territorio_codigo", "periodo"]).valor
    s.name = nombre
    return s[~s.index.duplicated()]


def panel_prov() -> pd.DataFrame:
    """Panel anual provincial (índice (provincia, año)) con todo lo que usan F1-F3, ya filtrado por el sellado de V18."""
    vt = _wide(base("valor_tasado", "provincia", "A"), "vt")
    defl = anual_con_tope(a_anual(base("deflactor", "nacional", "T")), "deflactor", "nacional").set_index("periodo").valor
    defl.index = defl.index.astype(int)
    ipcal = _wide(base("ipc_alquiler_indice", "provincia", "A"), "ipc_alq")
    pob = _wide(base("pob_total", "provincia", "A"), "pob")
    par = _wide(base("parados_epa", "provincia", "A"), "parados")
    ocu = _wide(base("ocupados_epa", "provincia", "A"), "ocupados")
    pib = _wide(pib_provincial(), "pib")
    parque = _wide(parque_provincial(), "parque")
    suelo = _wide(suelo_provincial_anual(), "suelo")
    ini = _wide(base("iniciadas_anual_tabla", "provincia", "A"), "iniciadas")
    ter = _wide(base("terminadas_anual_tabla", "provincia", "A"), "terminadas")
    ser = _wide(base("serpavi_alquiler_m2_mediana", "provincia", "A", desag="tipologia=VC"), "serpavi_vc")
    P = pd.concat([vt, ipcal, pob, par, ocu, pib, parque, suelo, ini, ter, ser], axis=1)
    P = P.reset_index().rename(columns={"level_0": "prov", "level_1": "anio"})
    P.columns = ["prov", "anio"] + list(P.columns[2:])
    P["defl"] = P.anio.map(defl)
    tn = anual_con_tope(a_anual(base("tipo_hip_bde", "nacional", "T")), "tipo_hip_bde", "nacional").set_index("periodo").valor
    tr = anual_con_tope(a_anual(base("tipo_hip_real_bde", "nacional", "T")), "tipo_hip_real_bde", "nacional").set_index("periodo").valor
    cp = anual_de_t("credito_promotor", "nacional").set_index("periodo").valor
    P["tipo_nom"] = P.anio.map({int(k): v for k, v in tn.items()})
    P["tipo_real"] = P.anio.map({int(k): v for k, v in tr.items()})
    P["credito_prom"] = P.anio.map({int(k): v for k, v in cp.items()})
    P["ln_p"] = np.log(P.vt / P.defl * 100)
    P["ln_alq"] = np.log(P.ipc_alq / P.defl * 100)
    P["ln_renta"] = np.log(P.pib * 1000 / (P["pob"]) / P.defl * 100)      # PIB corriente (miles de euros) por habitante, real; sustituto de la renta de los hogares
    P["paro"] = P.parados / (P.parados + P.ocupados) * 100
    P["ln_pob"] = np.log(P["pob"])
    P["ln_parque_pc"] = np.log(P.parque / P["pob"])
    P["ln_suelo"] = np.log(P.suelo / P.defl * 100)
    P["ln_ini"] = np.log(P.iniciadas.where(P.iniciadas > 0))
    P["ln_credprom"] = np.log(P.credito_prom / P.defl * 100)
    return P


def a_arrays(P: pd.DataFrame, y: str, xs: list[str], ini: int, fin: int, minimo: int | None = None):
    """Panel balanceado (provincias con todos los años de [ini, fin] en y y xs). Devuelve Y (N, T), X (N, T, k), códigos y años; N y T tras el recorte."""
    d = P[(P.anio >= ini) & (P.anio <= fin)][["prov", "anio", y] + xs].dropna()
    T = fin - ini + 1
    cnt = d.groupby("prov").size()
    ok = cnt[cnt == T].index
    d = d[d.prov.isin(ok)].sort_values(["prov", "anio"])
    codigos = sorted(d.prov.unique())
    N = len(codigos)
    Y = d[y].to_numpy().reshape(N, T)
    X = d[xs].to_numpy().reshape(N, T, len(xs))
    return Y, X, codigos, list(range(ini, fin + 1)), {"N": N, "T": T, "descartadas": int(len(cnt) - N)}


# ---------------------------------------------------------------------------------------------- F3-R1: CCAA no selladas
def panel_ccaa_oferta() -> pd.DataFrame:
    """9 CCAA no selladas, anual: viviendas libres iniciadas (suma de provincias), valor tasado real y coste de construcción real."""
    ini = iniciadas_libres_provincial()
    cc = _ccaa_de_provincia()
    ini["ccaa"] = ini.territorio_codigo.map(cc)
    ini = ini.dropna(subset=["ccaa"])
    s = ini.groupby(["ccaa", "periodo"]).valor.agg(["sum", "size"]).reset_index()
    nprov = {c: sum(1 for p, cc_ in cc.items() if cc_ == c and p in set(ini.territorio_codigo)) for c in s.ccaa.unique()}
    s = s[s.apply(lambda r: r["size"] == nprov[r["ccaa"]], axis=1)]
    iv = s.rename(columns={"sum": "iniciadas", "periodo": "anio"})[["ccaa", "anio", "iniciadas"]]
    iv["anio"] = iv.anio.astype(int)
    a = anual_de_t("valor_tasado_ccaa", "ccaa").rename(columns={"territorio_codigo": "ccaa"})
    a["anio"] = a.periodo.astype(int)
    vt = a[["ccaa", "anio", "valor"]].rename(columns={"valor": "vt"})
    defl = anual_con_tope(a_anual(base("deflactor", "nacional", "T")), "deflactor", "nacional").set_index("periodo").valor
    cost = anual_de_t("costes_constr", "nacional").set_index("periodo").valor
    D = iv.merge(vt, on=["ccaa", "anio"], how="inner")
    D["defl"] = D.anio.map({int(k): v for k, v in defl.items()})
    D["coste"] = D.anio.map({int(k): v for k, v in cost.items()})
    D["ln_ini"] = np.log(D.iniciadas.where(D.iniciadas > 0))
    D["ln_p"] = np.log(D.vt / D.defl * 100)
    D["ln_coste"] = np.log(D.coste / D.defl * 100)
    return D.sort_values(["ccaa", "anio"]).reset_index(drop=True)


# ---------------------------------------------------------------------------------------------- P-E1P2: precio y alquiler provinciales trimestrales
def panel_prov_trimestral_alquiler() -> pd.DataFrame:
    vt = base("valor_tasado", "provincia", "T")
    ia = base("ipc_alquiler_indice", "provincia", "T")
    d = trim_idx(base("deflactor", "nacional", "T"))
    a = vt.pivot(index="periodo", columns="territorio_codigo", values="valor")
    b = ia.pivot(index="periodo", columns="territorio_codigo", values="valor")
    cols = sorted(set(a.columns) & set(b.columns))
    idx = sorted(set(a.index) & set(b.index))
    a, b = a.loc[idx, cols], b.loc[idx, cols]
    pi = pd.PeriodIndex([s.replace("T", "Q") for s in idx], freq="Q")
    dd = d.reindex(pi).to_numpy()[:, None]
    return {"y": np.log(a.to_numpy() / dd * 100), "x": np.log(b.to_numpy() / dd * 100), "cols": cols, "idx": idx}

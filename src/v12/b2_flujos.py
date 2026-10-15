"""V12-B2 · A dónde va y quién se desplaza (descriptivo, C4; sin modelos ni lenguaje causal).

1. Flujos origen-destino entre municipios (microdatos EVR 2002-2020 y EMCR 2021-2024; INE) para cinco áreas:
   - València: ámbito oficial del PATEVAL (GVA, 90 municipios incluida la ciudad);
   - Madrid y Barcelona: municipios con centroide a ≤ 25 km del de la capital (definición operativa; no hay delimitación
     oficial en data/raw);
   - Alicante/Alacant y Castelló de la Plana: ≤ 20 km (misma definición operativa que V11).
   Los microdatos agregan los municipios < 10.000 hab. de cada provincia (PP999): la «corona» es el conjunto de
   municipios del área identificados en TODOS los años 2002-2024 (composición fija); el resto del área queda en
   «resto de España». Flujos capital → corona, corona → capital, capital ↔ resto, corona ↔ resto, por nacionalidad
   (ES/EXT) y edad (0-15, 16-34, 35-64, 65+).
2. Saldos interiores (por edad × nacionalidad) y exteriores (por nacionalidad; los microdatos exteriores municipales no
   traen edad) por municipio ≥ 10.000 hab., provincia y periodo.
3. Relación descriptiva con alquileres y precios (C4, asociación de rangos, sin causalidad):
   - alquiler: SERPAVI, mediana €/m² de vivienda colectiva (código INE);
   - compra: valor tasado medio de vivienda libre (MIVAU, municipios > 25.000 hab.) con concordancia nombre → código INE
     explícita y versionada (solo coincidencias únicas dentro de la provincia; las demás se descartan y se listan);
   - por pares: alquiler medio en destino frente a origen de quienes salen de cada capital, ponderado por el flujo.
   Las correlaciones van al Registry y se ajustan por Holm.
Caché: los OD completos (data/raw/v11/*/od_municipios_*.parquet, no versionados por tamaño) se leen solo si falta
data/cache/v12/od_seleccion.csv.gz (versionada, uso interno y NO difundible: contiene celdas pequeñas); las salidas de
output/v12/b2 solo publican agregados por área y periodo.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.econ_utils import Registry  # noqa: E402
from src.v9.comun import GZ_PANDAS  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
RAW, RAW11 = RAIZ / "data/raw", RAIZ / "data/raw/v11"
OUT = RAIZ / "output/v12/b2"
SEED = 20261010
CAPITALES = {"valencia": "46250", "madrid": "28079", "barcelona": "08019", "alicante": "03014", "castellon": "12040"}
RADIO_KM = {"madrid": 25, "barcelona": 25, "alicante": 20, "castellon": 20}
PERIODOS = {"2003-2007": (2003, 2007), "2008-2013": (2008, 2013), "2014-2019": (2014, 2019), "2020-2021": (2020, 2021),
            "2022-2024": (2022, 2024)}
CACHE = RAIZ / "data/cache/v12/od_seleccion.csv.gz"   # caché interna, no difundible (celdas pequeñas): data/cache/v12/LEEME.md


def areas() -> dict[str, set[str]]:
    import geopandas as gpd
    m = gpd.read_parquet(RAIZ / "data/base/geo/municipios.parquet").to_crs(25830)
    c = m.geometry.centroid
    m["x"], m["y"] = c.x, c.y
    out = {"valencia": set(pd.read_csv(RAW11 / "gva_pateval/pateval_municipios.csv", dtype=str).cod_municipio)}
    for a, r in RADIO_KM.items():
        cap = m[m.cod_municipio == CAPITALES[a]].iloc[0]
        d = np.hypot(m.x - cap.x, m.y - cap.y) / 1000
        out[a] = set(m.loc[d <= r, "cod_municipio"])
    return out


def od(ar: dict[str, set[str]]) -> pd.DataFrame:
    if CACHE.exists():
        return pd.read_csv(CACHE, dtype={"origen": str, "destino": str})
    todos = set().union(*ar.values())
    partes = []
    for a in range(2002, 2025):
        fuente = "ine_evr" if a <= 2020 else "ine_emcr"
        d = pd.read_parquet(RAW11 / fuente / f"od_municipios_{a}.parquet")
        d = d[d.origen.isin(todos) | d.destino.isin(todos)]
        g = d.groupby(["origen", "destino", "nac", "edad_g"], as_index=False).n.sum()
        g.insert(0, "anio", a)
        g["fuente"] = "EVR" if a <= 2020 else "EMCR"
        partes.append(g)
    x = pd.concat(partes, ignore_index=True)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    x.to_csv(CACHE, index=False, compression=GZ_PANDAS)
    return x


def coronas(x: pd.DataFrame, ar: dict[str, set[str]]) -> dict[str, set[str]]:
    """Municipios del área (sin la capital) identificados en todos los años (composición fija)."""
    pres = pd.concat([x[["anio", "origen"]].rename(columns={"origen": "m"}), x[["anio", "destino"]].rename(columns={"destino": "m"})])
    anios = pres.groupby("m").anio.nunique()
    fijos = set(anios[anios == x.anio.nunique()].index)
    return {a: (s & fijos) - {CAPITALES[a]} for a, s in ar.items()}


def flujos_area(x: pd.DataFrame, cor: dict[str, set[str]]) -> pd.DataFrame:
    filas = []
    for a, cap in CAPITALES.items():
        c = cor[a]
        zona = lambda s: np.where(s == cap, "capital", np.where(s.isin(c), "corona", "resto"))  # noqa: E731
        y = x[(x.origen == cap) | (x.destino == cap) | x.origen.isin(c) | x.destino.isin(c)].copy()
        y["zo"], y["zd"] = zona(y.origen), zona(y.destino)
        y = y[y.zo != y.zd]   # los movimientos dentro de la corona (entre municipios de la corona) no cambian el reparto capital/corona
        g = y.groupby(["anio", "nac", "edad_g", "zo", "zd"], as_index=False).n.sum()
        g.insert(0, "area", a)
        filas.append(g)
    return pd.concat(filas, ignore_index=True)


def resumen_area(f: pd.DataFrame) -> pd.DataFrame:
    w = f.assign(flujo=f.zo + "_a_" + f.zd).pivot_table(index=["area", "anio", "nac", "edad_g"], columns="flujo", values="n",
                                                        aggfunc="sum", fill_value=0).reset_index()
    for c in ("capital_a_corona", "corona_a_capital", "capital_a_resto", "resto_a_capital", "corona_a_resto", "resto_a_corona"):
        if c not in w:
            w[c] = 0
    w["saldo_capital_con_corona"] = w.corona_a_capital - w.capital_a_corona
    w["saldo_capital_con_resto"] = w.resto_a_capital - w.capital_a_resto
    w["saldo_corona_con_resto"] = w.resto_a_corona - w.corona_a_resto
    return w


def por_periodo(w: pd.DataFrame, claves: list[str]) -> pd.DataFrame:
    num = [c for c in w.columns if c not in claves + ["anio"] and pd.api.types.is_numeric_dtype(w[c])]
    filas = []
    for p, (i, j) in PERIODOS.items():
        g = w[w.anio.between(i, j)].groupby(claves, as_index=False)[num].sum()
        g.insert(0, "periodo", p)
        filas.append(g)
    return pd.concat(filas, ignore_index=True)


def destinos(x: pd.DataFrame, i: int = 2022, j: int = 2024, top: int = 15) -> pd.DataFrame:
    nombres = pd.read_parquet(RAIZ / "data/base/geo/municipios.parquet", columns=["cod_municipio", "nombre_municipio"]).set_index("cod_municipio").nombre_municipio
    filas = []
    for a, cap in CAPITALES.items():
        for sentido, col, otro in (("salidas", "origen", "destino"), ("entradas", "destino", "origen")):
            y = x[(x[col] == cap) & x.anio.between(i, j)]
            g = y.groupby(otro).n.sum().sort_values(ascending=False)
            tot = g.sum()
            g = g.head(top).rename("n").reset_index().rename(columns={otro: "cod_municipio"})
            g["cuota_pct"] = (100 * g.n / tot).round(1)
            g["nombre"] = g.cod_municipio.map(nombres).fillna(g.cod_municipio.str[2:].map({"999": "municipios < 10.000 hab. (provincia)"}))
            g.insert(0, "sentido", sentido)
            g.insert(0, "area", a)
            g["periodo"] = f"{i}-{j}"
            filas.append(g)
    return pd.concat(filas, ignore_index=True)


def saldos_edad_nac() -> pd.DataFrame:
    """Saldos interiores (edad × nac) y exteriores (nac) por municipio ≥ 10.000 hab. y periodo."""
    partes = []
    for fuente, ini, fin in (("ine_evr", 2003, 2020), ("ine_emcr", 2021, 2024)):
        s = pd.read_csv(RAW11 / f"{fuente}/saldos_internos_municipio.csv.gz", dtype={"cod_municipio": str})
        partes.append(s[s.anio.between(ini, fin)])
    s = pd.concat(partes)
    s = s[s.cod_municipio.str[2:] != "999"]
    filas = []
    for p, (i, j) in PERIODOS.items():
        g = s[s.anio.between(i, j)].groupby(["cod_municipio", "nac", "edad_g"], as_index=False)[["altas", "bajas", "saldo"]].sum()
        g.insert(0, "periodo", p)
        filas.append(g)
    t = pd.concat(filas, ignore_index=True).rename(columns={"altas": "altas_interiores", "bajas": "bajas_interiores", "saldo": "saldo_interior"})
    # celdas pequeñas: con < 10 altas o < 10 bajas en la celda municipio × periodo × edad × nacionalidad se vacían las tres
    malo = (t.altas_interiores < 10) | (t.bajas_interiores < 10)
    t.loc[malo, ["altas_interiores", "bajas_interiores", "saldo_interior"]] = np.nan
    t["suprimido"] = malo
    return t


# ------------------------------------------------------------------------------------------------ precios y alquileres
def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z]", "", s)


# provincia del MIVAU (texto, a veces truncado) → código INE; solo se usa para desambiguar nombres repetidos
PROV = {"alava": "01", "araba": "01", "albacete": "02", "alicante": "03", "almeria": "04", "avila": "05", "badajoz": "06",
        "illesbalears": "07", "baleares": "07", "barcelona": "08", "burgos": "09", "caceres": "10", "cadiz": "11",
        "castellon": "12", "ciudadreal": "13", "cordoba": "14", "coruna": "15", "acoruna": "15", "cuenca": "16", "girona": "17",
        "granada": "18", "guadalajara": "19", "gipuzkoa": "20", "guipuzcoa": "20", "huelva": "21", "huesca": "22", "jaen": "23",
        "leon": "24", "lleida": "25", "rioja": "26", "larioja": "26", "lugo": "27", "madrid": "28", "malaga": "29", "murcia": "30",
        "navarra": "31", "ourense": "32", "asturias": "33", "palencia": "34", "laspalmas": "35", "palmaslas": "35",
        "pontevedra": "36", "salamanca": "37", "santacruzde": "38", "tenerife": "38", "segovia": "40", "sevilla": "41",
        "soria": "42", "tarragona": "43", "teruel": "44", "toledo": "45", "valencia": "46", "valladolid": "47", "bizkaia": "48",
        "vizcaya": "48", "zamora": "49", "zaragoza": "50", "ceuta": "51", "melilla": "52"}
# nombres del MIVAU sin equivalente literal en el nomenclátor del INE (se apuntan al nombre INE, nunca a un código)
ALIAS = {"palmademallorca": "Palma", "vitoria": "Vitoria-Gasteiz", "sancristoballaguna": "San Cristóbal de La Laguna",
         "santacolomagramanet": "Santa Coloma de Gramenet", "puertodesantamaria": "Puerto de Santa María, El",
         "santaeulaliadelrio": "Santa Eulària des Riu", "mahon": "Maó"}


def _prov(texto: str) -> str | None:
    t = norm(texto)
    return next((c for k, c in PROV.items() if t.startswith(k) or k.startswith(t)), None) if t else None


def concordancia_mivau() -> pd.DataFrame:
    """Nombre del MIVAU → código INE: coincidencia exacta normalizada con alguna variante del nombre INE (partes separadas
    por «/», artículo pospuesto) y, si hay varias, la de la provincia indicada. Sin coincidencia única → sin código."""
    mv = pd.read_csv(RAW / "mivau_valor_tasado_municipios.csv", usecols=["territorio", "provincia", "nivel"], dtype=str)
    mv = mv[mv.nivel == "municipio"].drop_duplicates(["territorio", "provincia"])
    mu = pd.read_parquet(RAIZ / "data/base/geo/municipios.parquet", columns=["cod_municipio", "nombre_municipio"])
    variantes = []
    for cod, nom in zip(mu.cod_municipio, mu.nombre_municipio):
        for parte in [nom] + re.split(r"/", nom):
            parte = parte.strip()
            m = re.match(r"^(.*), *(el|la|los|las|l'|els|les|o|a|os|as|es|sa|ses)$", parte, flags=re.I)
            variantes += [(cod, norm(parte))] + ([(cod, norm(m.group(1))), (cod, norm(f"{m.group(2)} {m.group(1)}"))] if m else [])
    v = pd.DataFrame(variantes, columns=["cod_municipio", "clave"]).drop_duplicates()
    filas = []
    for t, p in zip(mv.territorio, mv.provincia):
        partes = [t] + [re.sub(r"\s*\(.*\)$", "", x).strip() for x in t.split("/")]
        claves = {norm(x) for x in partes} | ({norm(ALIAS[norm(t)])} if norm(t) in ALIAS else set())
        cand = sorted(set(v[v.clave.isin(claves)].cod_municipio))
        cp = _prov(p)
        if len(cand) > 1 and cp:
            cand = [c for c in cand if c[:2] == cp]
        filas.append({"territorio_mivau": t, "provincia_mivau": p, "cod_municipio": cand[0] if len(cand) == 1 else "",
                      "candidatos": len(cand), "alias": norm(t) in ALIAS})
    return pd.DataFrame(filas)


def precios() -> pd.DataFrame:
    import pyarrow.parquet as pq
    t = pq.read_table(RAIZ / "data/base/publica/hechos.parquet", columns=["territorio_codigo", "nivel", "periodo", "variable", "desagregacion", "valor"],
                      filters=[("nivel", "=", "municipio"), ("variable", "=", "serpavi_alquiler_m2_mediana"),
                               ("desagregacion", "=", "tipologia=VC")]).to_pandas()
    alq = t.assign(anio=t.periodo.astype(int)).rename(columns={"territorio_codigo": "cod_municipio", "valor": "alquiler_m2"})[["cod_municipio", "anio", "alquiler_m2"]]
    k = concordancia_mivau()
    OUT.mkdir(parents=True, exist_ok=True)
    k.to_csv(OUT / "concordancia_mivau_municipios.csv", index=False)
    mv = pd.read_csv(RAW / "mivau_valor_tasado_municipios.csv", usecols=["periodo", "valor", "territorio", "provincia", "nivel"], dtype=str)
    # la concordancia (nombre → código, versionada) se aplica una vez; a partir de aquí todo cruce es por código INE
    conc = {(t, p): c for t, p, c in zip(k.territorio_mivau, k.provincia_mivau, k.cod_municipio) if c}
    mv = mv[mv.nivel == "municipio"].copy()
    mv["cod_municipio"] = [conc.get((t, p)) for t, p in zip(mv.territorio, mv.provincia)]
    mv = mv.dropna(subset=["cod_municipio"])
    mv["anio"], mv["valor"] = mv.periodo.str[:4].astype(int), pd.to_numeric(mv.valor, errors="coerce")
    com = mv.groupby(["cod_municipio", "anio"], as_index=False).valor.mean().rename(columns={"valor": "valor_tasado_m2"})
    return alq.merge(com, how="outer", on=["cod_municipio", "anio"])


def spearman_ic(x: np.ndarray, y: np.ndarray, rng: np.random.Generator, B: int = 1000) -> tuple[float, float, float, float]:
    r, p = stats.spearmanr(x, y)
    bs = []
    for _ in range(B):
        i = rng.integers(0, len(x), len(x))
        bs.append(stats.spearmanr(x[i], y[i])[0])
    lo, hi = np.nanpercentile(bs, [2.5, 97.5])
    return float(r), float(p), float(lo), float(hi)


def relacion_precios(P: pd.DataFrame, x: pd.DataFrame, cor: dict[str, set[str]], reg: Registry) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Asociación (Spearman, IC bootstrap) entre la tasa de saldo interior de un periodo y el nivel y el cambio de
    alquiler/precio en el mismo periodo, en municipios ≥ 10.000 hab. con dato; y ratio de alquiler destino/origen de
    quienes salen de las capitales."""
    b1 = pd.read_csv(RAIZ / "output/v12/b1/contabilidad_periodos_municipio.csv.gz", dtype={"cod_territorio": str})
    b1 = b1[b1.nac == "TOTAL"][["periodo", "cod_territorio", "poblacion_inicio", "tasa_saldo_interior_por_mil_anual", "tasa_saldo_exterior_por_mil_anual"]]
    rng = np.random.default_rng(SEED)
    filas = []
    for per, ini, fin in (("2014-2019", 2014, 2019), ("2022-2024", 2022, 2024)):
        for var in ("alquiler_m2", "valor_tasado_m2"):
            q = P.dropna(subset=[var]).pivot_table(index="cod_municipio", columns="anio", values=var)
            if ini not in q or fin not in q:
                continue
            nivel = q[ini].rename("nivel_inicio")
            cambio = (100 * (q[fin] / q[ini] - 1)).rename("cambio_pct")
            d = b1[b1.periodo == per].set_index("cod_territorio").join(nivel).join(cambio)
            for ambito, sub in (("España", d), ("cinco áreas", d[d.index.isin(set().union(*cor.values()) | set(CAPITALES.values()))])):
                for saldo in ("tasa_saldo_interior_por_mil_anual", "tasa_saldo_exterior_por_mil_anual"):
                    for medida in ("nivel_inicio", "cambio_pct"):
                        z = sub[[saldo, medida]].dropna()
                        if len(z) < 10:
                            continue
                        r, p, lo, hi = spearman_ic(z[saldo].to_numpy(), z[medida].to_numpy(), rng)
                        mid = f"b2_{per}_{ambito}_{saldo}_{var}_{medida}"
                        reg.log("V12-B2", mid, f"spearman({saldo}, {var}:{medida})", ini, fin, len(z), np.nan, np.nan, np.nan,
                                coef_interes=r, p_interes=p, notas=f"descriptivo C4; ámbito {ambito}")
                        filas.append({"periodo": per, "ambito": ambito, "saldo": saldo, "medida": f"{var}:{medida}", "N": len(z),
                                      "spearman": round(r, 3), "ic95": [round(lo, 3), round(hi, 3)], "p": p})
    R = pd.DataFrame(filas)
    if len(R):
        from statsmodels.stats.multitest import multipletests
        R["p_holm"] = multipletests(R.p, method="holm")[1]
        R["ic95_inf"], R["ic95_sup"] = R.ic95.str[0], R.ic95.str[1]
        R = R.drop(columns="ic95")
    # pares: alquiler en destino / alquiler en la capital para quienes salen de ella (ponderado por el flujo)
    pares = []
    alq = P.dropna(subset=["alquiler_m2"]).set_index(["cod_municipio", "anio"]).alquiler_m2
    for a, cap in CAPITALES.items():
        for anio in range(2011, 2025):
            y = x[(x.origen == cap) & (x.anio == anio)].groupby(["destino", "nac"], as_index=False).n.sum()
            y["alq_dest"] = [alq.get((m, anio), np.nan) for m in y.destino]
            a0 = alq.get((cap, anio), np.nan)
            for nac, g in list(y.groupby("nac")) + [("TOTAL", y)]:
                g = g.dropna(subset=["alq_dest"])
                if g.empty or np.isnan(a0):
                    continue
                for zona, h in (("corona", g[g.destino.isin(cor[a])]), ("todos con dato", g)):
                    if h.n.sum() == 0:
                        continue
                    pares.append({"area": a, "anio": anio, "nac": nac, "destinos": zona, "personas_con_dato": int(h.n.sum()),
                                  "alquiler_capital": round(a0, 2), "alquiler_destino_ponderado": round(float(np.average(h.alq_dest, weights=h.n)), 2),
                                  "ratio_destino_capital": round(float(np.average(h.alq_dest, weights=h.n) / a0), 3)})
    return R, pd.DataFrame(pares)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    reg = Registry(OUT / "registry.csv")
    ar = areas()
    x = od(ar)
    cor = coronas(x, ar)
    pd.DataFrame([{"area": a, "capital": CAPITALES[a], "municipios_area": len(ar[a]), "municipios_corona_fija": len(cor[a]),
                   "definicion": "PATEVAL (GVA)" if a == "valencia" else f"centroide a ≤ {RADIO_KM[a]} km",
                   "corona": " ".join(sorted(cor[a]))} for a in CAPITALES]).to_csv(OUT / "areas.csv", index=False)
    f = flujos_area(x, cor)
    w = resumen_area(f)
    w.to_csv(OUT / "flujos_area_anual.csv", index=False)
    wt = w.groupby(["area", "anio"], as_index=False)[[c for c in w.columns if c not in ("area", "anio", "nac", "edad_g")]].sum()
    wt.to_csv(OUT / "flujos_area_anual_total.csv", index=False)
    per = por_periodo(w, ["area", "nac", "edad_g"])
    per.to_csv(OUT / "flujos_area_periodos.csv", index=False)
    destinos(x).to_csv(OUT / "destinos_capitales_2022_2024.csv", index=False)
    saldos_edad_nac().to_csv(OUT / "saldos_interiores_edad_nac_municipio.csv.gz", index=False, compression=GZ_PANDAS)
    P = precios()
    R, pares = relacion_precios(P, x, cor, reg)
    R.to_csv(OUT / "asociacion_saldos_precios.csv", index=False)
    pares.to_csv(OUT / "alquiler_destino_salidas_capital.csv", index=False)
    reg.flush()
    tp = per.groupby(["area", "periodo"])[["capital_a_corona", "corona_a_capital", "saldo_capital_con_corona", "saldo_capital_con_resto"]].sum()
    edad = per[per.periodo == "2022-2024"].groupby(["area", "edad_g"]).saldo_capital_con_corona.sum().unstack()
    nacs = per[per.periodo == "2022-2024"].groupby(["area", "nac"]).saldo_capital_con_corona.sum().unstack()
    k = pd.read_csv(OUT / "concordancia_mivau_municipios.csv", dtype=str, keep_default_na=False)
    res = {"rama": "V12-B2", "pregunta": "¿A dónde va y quién se desplaza?", "capa": "C4", "metodo": "flujos OD y asociación de rangos (descriptivo)",
           "datos": "EVR 2002-2020 y EMCR 2021-2024 (microdatos OD, INE); SERPAVI; MIVAU valor tasado", "N": int(len(x)),
           "saldo_capital_con_corona_por_periodo": {f"{a}|{p}": int(v) for (a, p), v in tp.saldo_capital_con_corona.items()},
           "saldo_capital_con_corona_2022_2024_por_edad": {a: {e: int(v) for e, v in r.items()} for a, r in edad.iterrows()},
           "saldo_capital_con_corona_2022_2024_por_nac": {a: {e: int(v) for e, v in r.items()} for a, r in nacs.iterrows()},
           "concordancia_mivau": {"nombres": len(k), "con_codigo": int((k.cod_municipio != "").sum())},
           "asociaciones_p_holm_menor_005": int((R.p_holm < 0.05).sum()) if len(R) else 0, "asociaciones": int(len(R)),
           "notas": ["corona de composición fija (municipios identificados en todos los años)",
                     "saldo exterior municipal sin edad (los microdatos no la traen)",
                     "asociaciones de rangos: no implican causalidad"]}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

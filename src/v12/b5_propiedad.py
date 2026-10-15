"""V12-B5 · Quién es propietario (descriptivo, C4/C1; sin modelos ni lenguaje causal).

1. Catastro, titularidad 2024-2026 (sujetos pasivos del IBI por tramo de nº de inmuebles y tipo de persona), uso
   RESIDENCIAL (ficheros _V): por ámbito, cuota de viviendas en manos de sujetos pasivos con > 5 inmuebles (tramos
   6-10, 11-25, 26-100, > 100), con > 10, de personas jurídicas privadas (PJ) y de entidades públicas (PE).
   El tramo se cuenta DENTRO del ámbito (V12-F0): la cuota municipal es una COTA INFERIOR de la concentración (un titular
   con 200 viviendas repartidas en 40 municipios cuenta en cada municipio en su tramo local). Se publican los cuatro
   ámbitos (España, CCAA, provincia, municipio). Los ficheros de CCAA y provincia solo traen nombres: el código INE se
   toma del propio fichero municipal (CODINE y nombre de provincia en la misma fila). País Vasco y Navarra no están
   (catastros forales). Por tipo fino (ficheros _TPF, España y provincia): personas físicas de nacionalidad española o
   extranjera, sociedades, entidades extranjeras, administraciones públicas.
2. Ranking municipal (municipios ≥ 10.000 hab.) y asociación descriptiva (Spearman con IC bootstrap y Holm; Registry)
   entre las cuotas de 2025 y: alquiler (SERPAVI 2024 y su variación 2019-2024), IPVA (variación 2019-2024), valor tasado
   (MIVAU, con la concordancia de B2), viviendas turísticas (INE, % del parque, mayo de 2025, suma de secciones),
   llegada de población (B1, saldos exterior e interior 2022-2024) y renta (ADRH 2023, media de secciones ponderada por
   población). Asociación entre territorios: no dice qué causa qué.
3. 2012-2023 (JAXI): titulares catastrales urbanos frente a unidades urbanas (Catastro): titulares por unidad. NO se
   encadena con 2024-2026 (otra definición).
4. AEAT (Comunitat Valenciana, 2016-2024): declarantes aproximados con rentas de bienes inmuebles (V12-F0; incluye
   alquileres e imputación de inmuebles no alquilados, no mide caseros) y 2013-2015 rendimientos del capital
   inmobiliario (alquileres) declarados.
5. Ficha del verificador que actualiza V02 («fondos y grandes tenedores»): pasa de «NO ANALIZADA: FALTAN DATOS» a
   analizada; la parte causal («responsables de la subida») sigue sin poder contrastarse con datos descriptivos.
Salidas: output/v12/b5/.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.econ_utils import Registry  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
CT = RAIZ / "data/raw/v11/catastro_titularidad"
OUT = RAIZ / "output/v12/b5"
SEED = 20261010
TIPOS = ["PF", "PJ", "PE", "PD"]
TRAMOS = ["HASTA_1", "HASTA_5", "HASTA_10", "HASTA_25", "HASTA_100", "MAYOR_100"]
MAS5, MAS10 = TRAMOS[2:], TRAMOS[3:]


def cuotas(d: pd.DataFrame) -> pd.DataFrame:
    i = lambda t, r: pd.to_numeric(d[f"I_U_{t}_{r}"], errors="coerce").fillna(0)  # noqa: E731
    viv = sum(i(t, r) for t in TIPOS for r in TRAMOS)
    o = pd.DataFrame({"viviendas": viv, "sujetos_pasivos": pd.to_numeric(d.get("NUM_SUJETOS_PASIVOS"), errors="coerce")}, index=d.index)
    o["viv_mas5"] = sum(i(t, r) for t in TIPOS for r in MAS5)
    o["viv_mas10"] = sum(i(t, r) for t in TIPOS for r in MAS10)
    o["viv_mas100"] = sum(i(t, "MAYOR_100") for t in TIPOS)
    for t in ("PJ", "PE", "PF"):
        o[f"viv_{t}"] = sum(i(t, r) for r in TRAMOS)
    o["viv_PJ_mas10"] = sum(i("PJ", r) for r in MAS10)
    o["viv_PF_mas10"] = sum(i("PF", r) for r in MAS10)
    for c in ("mas5", "mas10", "mas100", "PJ", "PE", "PF", "PJ_mas10", "PF_mas10"):
        o[f"pct_{c}"] = 100 * o[f"viv_{c}"] / o.viviendas
    return o


def titularidad() -> pd.DataFrame:
    m = pd.read_csv(CT / "p_spi_mun_v.csv.gz", dtype=str)
    prov_cod = m.assign(c=m.CODINE.str[:2]).groupby("PROVINCIA").c.agg(lambda s: s.mode().iloc[0]).to_dict()
    terr = pd.read_parquet(RAIZ / "data/base/territorios.parquet")
    p_ccaa = terr[terr.nivel == "provincia"].set_index("territorio_codigo").cod_ccaa.to_dict()
    ccaa_cod = m.assign(c=m.CODINE.str[:2].map(p_ccaa)).groupby("CCAANOM").c.agg(lambda s: s.mode().iloc[0]).to_dict()
    partes = []
    for fichero, nivel, cod in (("p_spi_total_v", "nacional", lambda d: pd.Series("00", index=d.index)),
                                # concordancia derivada de los códigos INE (CODINE) del propio fichero municipal
                                ("p_spi_aut_v", "ccaa", lambda d: pd.Series([ccaa_cod.get(x) for x in d["CCAANOM"]], index=d.index)),
                                ("p_spi_prov_v", "provincia", lambda d: pd.Series([prov_cod.get(x) for x in d["PROVINCIA"]], index=d.index)),
                                ("p_spi_mun_v", "municipio", lambda d: d.CODINE)):
        d = pd.read_csv(CT / f"{fichero}.csv.gz", dtype=str)
        o = cuotas(d)
        o.insert(0, "anio", d.anio_fichero.astype(int))
        o.insert(0, "cod_territorio", cod(d))
        o.insert(0, "nivel", nivel)
        partes.append(o)
    x = pd.concat(partes, ignore_index=True)
    assert x.cod_territorio.notna().all(), "ámbito sin código INE"
    return x


def tipo_fino() -> pd.DataFrame:
    filas = []
    for fichero, nivel in (("p_spi_total_v_tpf", "nacional"), ("p_spi_prov_v_tpf", "provincia")):
        d = pd.read_csv(CT / f"{fichero}.csv.gz", dtype=str)
        cols = [c for c in d.columns if c.startswith("I_U_")]
        L = d.melt(id_vars=["anio_fichero"] + (["PROVINCIA"] if "PROVINCIA" in d else []), value_vars=cols, var_name="c", value_name="viviendas")
        L["viviendas"] = pd.to_numeric(L.viviendas, errors="coerce").fillna(0)
        p = L.c.str.extract(r"I_U_(\d+I|MAS100)_(.*)")
        L["tramo_hasta"] = pd.to_numeric(p[0].str.replace("I", "", regex=False).replace("MAS100", "1000"))
        L["tipo"] = p[1]
        L["tramo"] = np.where(L.tramo_hasta <= 5, "≤ 5", np.where(L.tramo_hasta <= 10, "6-10", "> 10"))
        claves = ["anio_fichero"] + (["PROVINCIA"] if "PROVINCIA" in d else [])
        g = L.groupby(claves + ["tipo", "tramo"], as_index=False).viviendas.sum()
        g["pct"] = 100 * g.viviendas / g.groupby(claves).viviendas.transform("sum")
        g.insert(0, "nivel", nivel)
        filas.append(g)
    return pd.concat(filas, ignore_index=True)


def covariables() -> pd.DataFrame:
    import pyarrow.parquet as pq
    h = RAIZ / "data/base/publica/hechos.parquet"
    rd = lambda filtros, cols=("territorio_codigo", "nivel", "periodo", "variable", "desagregacion", "valor"): pq.read_table(  # noqa: E731
        h, columns=list(cols), filters=filtros).to_pandas()
    s = rd([("nivel", "=", "municipio"), ("variable", "=", "serpavi_alquiler_m2_mediana"), ("desagregacion", "=", "tipologia=VC")])
    s = s.pivot_table(index="territorio_codigo", columns="periodo", values="valor")
    c = pd.DataFrame({"alquiler_m2_2024": s["2024"], "alquiler_var_2019_2024": 100 * (s["2024"] / s["2019"] - 1)})
    ip = rd([("nivel", "=", "municipio"), ("variable", "=", "ipva_tam_indice")]).pivot_table(index="territorio_codigo", columns="periodo", values="valor")
    c = c.join((100 * (ip["2024"] / ip["2019"] - 1)).rename("ipva_var_2019_2024"), how="outer")
    vt = pd.read_csv(RAIZ / "output/v12/b2/concordancia_mivau_municipios.csv", dtype=str, keep_default_na=False)
    conc = {(t, p): k for t, p, k in zip(vt.territorio_mivau, vt.provincia_mivau, vt.cod_municipio) if k}
    mv = pd.read_csv(RAIZ / "data/raw/mivau_valor_tasado_municipios.csv", usecols=["periodo", "valor", "territorio", "provincia", "nivel"], dtype=str)
    mv = mv[mv.nivel == "municipio"].copy()
    mv["cod"] = [conc.get((t, p)) for t, p in zip(mv.territorio, mv.provincia)]
    mv = mv.dropna(subset=["cod"]).assign(anio=lambda d: d.periodo.str[:4], v=lambda d: pd.to_numeric(d.valor, errors="coerce"))
    mv = mv.groupby(["cod", "anio"]).v.mean().unstack()
    c = c.join(pd.DataFrame({"valor_tasado_2024": mv["2024"], "valor_tasado_var_2019_2024": 100 * (mv["2024"] / mv["2019"] - 1)}), how="outer")
    vut = rd([("nivel", "=", "seccion"), ("variable", "in", ["ine_vut_vivienda_turistica", "ine_vut_porcentaje_vivienda_turistica"]), ("periodo", "=", "2025-05")])
    w = vut.pivot_table(index="territorio_codigo", columns="variable", values="valor")
    w["parque"] = w.ine_vut_vivienda_turistica / (w.ine_vut_porcentaje_vivienda_turistica / 100)
    w = w.replace([np.inf, -np.inf], np.nan).groupby(w.index.str[:5])[["ine_vut_vivienda_turistica", "parque"]].sum(min_count=1)
    c = c.join((100 * w.ine_vut_vivienda_turistica / w.parque).rename("vut_pct_2025"), how="outer")
    b1 = pd.read_csv(RAIZ / "output/v12/b1/contabilidad_periodos_municipio.csv.gz", dtype={"cod_territorio": str})
    b1 = b1[(b1.nac == "TOTAL") & (b1.periodo == "2022-2024")].set_index("cod_territorio")
    c = c.join(b1[["tasa_saldo_exterior_por_mil_anual", "tasa_saldo_interior_por_mil_anual"]], how="outer")
    r = rd([("nivel", "=", "seccion"), ("variable", "=", "adrh_renta_neta_hogar"), ("periodo", "=", "2023")])
    pob = rd([("nivel", "=", "seccion"), ("variable", "=", "pob_censo_anual"), ("periodo", "=", "2023"), ("desagregacion", "=", "nacionalidad=Total")])
    r = r.set_index("territorio_codigo").valor.rename("renta").to_frame().join(pob.set_index("territorio_codigo").valor.rename("pob")).dropna()
    r = r.groupby(r.index.str[:5]).apply(lambda g: np.average(g.renta, weights=g.pob) if g.pob.sum() > 0 else np.nan)
    c = c.join(r.rename("renta_neta_hogar_2023"), how="outer")
    return c.rename_axis("cod_municipio")


def asociaciones(t: pd.DataFrame, cov: pd.DataFrame, reg: Registry) -> pd.DataFrame:
    from statsmodels.stats.multitest import multipletests
    cen = pd.read_csv(RAIZ / "data/raw/v9/ine_censo_anual/censo_seccion_pais.csv.gz", dtype=str)
    cen = cen[(cen.nivel == "municipio") & (cen.pais_nacionalidad == "Total") & (cen.edicion == "2025")]
    grandes = set(cen[pd.to_numeric(cen.poblacion) >= 10000].cod_municipio)
    m = t[(t.nivel == "municipio") & (t.anio == 2025) & t.cod_territorio.isin(grandes)].set_index("cod_territorio")
    d = m[["pct_mas10", "pct_PJ"]].join(cov)
    rng = np.random.default_rng(SEED)
    filas = []
    for cuota in ("pct_mas10", "pct_PJ"):
        for v in [c for c in cov.columns]:
            z = d[[cuota, v]].dropna()
            if len(z) < 10:
                continue
            x, y = z[cuota].to_numpy(), z[v].to_numpy()
            r, p = stats.spearmanr(x, y)
            bs = []
            for _ in range(1000):
                i = rng.integers(0, len(x), len(x))
                bs.append(stats.spearmanr(x[i], y[i])[0])
            lo, hi = np.nanpercentile(bs, [2.5, 97.5])
            reg.log("V12-B5", f"b5_{cuota}_{v}", f"spearman({cuota}, {v})", 2025, 2025, len(z), np.nan, np.nan, np.nan,
                    coef_interes=r, p_interes=p, notas="descriptivo C4; municipios ≥ 10.000 hab.")
            filas.append({"cuota": cuota, "variable": v, "N": len(z), "spearman": round(float(r), 3), "ic95_inf": round(float(lo), 3),
                          "ic95_sup": round(float(hi), 3), "p": float(p)})
    R = pd.DataFrame(filas)
    R["p_holm"] = multipletests(R.p, method="holm")[1]
    return R


def titulares_2012_2023() -> pd.DataFrame:
    h = pd.read_csv(CT / "titulares_municipio_2006_2023.csv.gz", dtype={"cod_municipio": str})
    u = pd.read_csv(RAIZ / "data/raw/catastro_urbana_municipios.csv.gz", dtype={"codigo": str, "periodo": str})
    u = u[u.unidad == "unidades_urbanas_total"].assign(anio=lambda d: d.periodo.astype(int) - 1)   # fichero t = stock a 31-12-(t−1)
    u = u.groupby(["codigo", "anio"], as_index=False).valor.sum().rename(columns={"codigo": "cod_municipio", "valor": "unidades_urbanas"})
    x = h[h.anio.between(2012, 2023)].merge(u, how="inner", on=["cod_municipio", "anio"])
    n = x.groupby("anio")[["titulares_urbano", "unidades_urbanas"]].sum()
    n["titulares_por_unidad"] = n.titulares_urbano / n.unidades_urbanas
    n["municipios"] = x.groupby("anio").cod_municipio.nunique()
    return n.reset_index()


def aeat() -> tuple[pd.DataFrame, pd.DataFrame]:
    a = pd.read_csv(RAIZ / "output/v12/f0/aeat_declarantes_inmuebles_aprox.csv", dtype={"cod_municipio": str})
    a = a[a.marca.isna() | (a.marca == "")]
    cv = a.groupby("ejercicio")[["declaraciones", "declarantes_rentas_inmuebles_aprox"]].sum()
    cv["cuota_pct"] = 100 * cv.declarantes_rentas_inmuebles_aprox / cv.declaraciones
    v = pd.read_csv(RAIZ / "output/v12/f0/aeat_inmuebles_2013_2015.csv", dtype={"cod_municipio": str})
    return cv.reset_index(), v.groupby("ejercicio").sum(numeric_only=True).reset_index()


def _es(x: float) -> str:
    return f"{x:.1f}".replace(".", ",")


def ficha(t: pd.DataFrame, R: pd.DataFrame, grandes: set) -> dict:
    n = t[(t.nivel == "nacional")].set_index("anio")
    u = int(n.index.max())
    r = n.loc[u]
    m = t[(t.nivel == "municipio") & (t.anio == u) & t.cod_territorio.isin(grandes)]
    sig = R[R.p_holm < 0.05]
    return {"id": "V12-V02", "sustituye": "V02", "tema": "Grandes tenedores",
            "enunciado": "Los fondos de inversión y los grandes tenedores son los responsables de la subida de precios y alquileres.",
            "capa": "C4",
            "magnitud": (f"Catastro {u} (uso residencial, España sin País Vasco ni Navarra): {_es(r.pct_mas10)} % de las viviendas son de sujetos "
                         f"pasivos con más de 10 inmuebles residenciales en España, {_es(r.pct_mas100)} % de los que tienen más de 100 y "
                         f"{_es(r.pct_PJ)} % de personas jurídicas privadas; {_es(r.pct_PF)} % de personas físicas."),
            "intervalo": f"municipios ≥ 10.000 hab. (cota inferior): mediana {_es(m.pct_mas10.median())} % (p10-p90 {_es(m.pct_mas10.quantile(.1))}-{_es(m.pct_mas10.quantile(.9))} %) con > 10",
            "cota": "—",
            "literatura": "Sin trabajo replicado para España con estos datos.",
            "veredicto": "ANALIZADA, NO CONCLUYENTE",
            "regla": ("Hay ya cifra del peso de los grandes titulares (C4, fuente única: Catastro). La afirmación es causal («responsables de la subida») "
                      "y no hay diseño que la contraste: entre municipios, las asociaciones con alquiler y precio son descriptivas "
                      f"({len(sig)} de {len(R)} con p de Holm < 0,05) y no permiten separar si la concentración sigue a los precios o al revés."),
            "limites": ("Los tramos se cuentan dentro de cada ámbito (la cuota municipal es una cota inferior); un sujeto pasivo por inmueble "
                        "(no cuenta cotitulares); no distingue viviendas en alquiler; no identifica fondos frente a otras sociedades."),
            "evidencia": ["output/v12/b5/titularidad_cuotas.csv", "output/v12/b5/asociaciones_titularidad.csv", "docs/v12/decisiones.md"],
            "veredicto_previo": "NO ANALIZADA: FALTAN DATOS"}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    reg = Registry(OUT / "registry.csv")
    t = titularidad()
    t.to_csv(OUT / "titularidad_cuotas.csv", index=False, float_format="%.10g")
    tipo_fino().to_csv(OUT / "titularidad_tipo_fino.csv", index=False, float_format="%.10g")
    cov = covariables()
    R = asociaciones(t, cov, reg)
    R.to_csv(OUT / "asociaciones_titularidad.csv", index=False)
    reg.flush()
    cen = pd.read_csv(RAIZ / "data/raw/v9/ine_censo_anual/censo_seccion_pais.csv.gz", dtype=str)
    cen = cen[(cen.nivel == "municipio") & (cen.pais_nacionalidad == "Total") & (cen.edicion == "2025")]
    grandes = set(cen[pd.to_numeric(cen.poblacion) >= 10000].cod_municipio)
    nom = pd.read_parquet(RAIZ / "data/base/geo/municipios.parquet", columns=["cod_municipio", "nombre_municipio"]).set_index("cod_municipio").nombre_municipio
    rk = t[(t.nivel == "municipio") & (t.anio == t.anio.max()) & t.cod_territorio.isin(grandes)].copy()
    rk["nombre"] = rk.cod_territorio.map(nom)
    rk["rango_mas10"] = rk.pct_mas10.rank(ascending=False, method="min").astype(int)
    rk["rango_PJ"] = rk.pct_PJ.rank(ascending=False, method="min").astype(int)
    rk.sort_values("rango_mas10").to_csv(OUT / "ranking_municipios.csv", index=False, float_format="%.6g")
    tt = titulares_2012_2023()
    tt.to_csv(OUT / "titulares_2012_2023.csv", index=False, float_format="%.10g")
    cv, v15 = aeat()
    cv.to_csv(OUT / "aeat_cv_declarantes_inmuebles.csv", index=False, float_format="%.10g")
    v15.to_csv(OUT / "aeat_cv_2013_2015.csv", index=False, float_format="%.10g")
    f = ficha(t, R, grandes)
    (OUT / "fichas_verificador_v12.json").write_text(json.dumps([f], ensure_ascii=False, indent=1), encoding="utf-8")
    n = t[t.nivel == "nacional"].set_index("anio")
    res = {"rama": "V12-B5", "pregunta": "¿Quién es propietario?", "capa": "C4", "metodo": "descriptivo (cuotas) y asociación de rangos",
           "datos": "Catastro titularidad 2024-2026 y JAXI 2012-2023; SERPAVI, IPVA, MIVAU, INE VUT, ADRH, B1; AEAT", "N": int(len(t)),
           "nacional": {int(a): {c: round(float(r[c]), 2) for c in ("viviendas", "pct_mas5", "pct_mas10", "pct_mas100", "pct_PJ", "pct_PE", "pct_PF")}
                        for a, r in n.iterrows()},
           "municipio_10k_2025_mediana_pct_mas10": round(float(t[(t.nivel == "municipio") & (t.anio == 2025) & t.cod_territorio.isin(grandes)].pct_mas10.median()), 2),
           "titulares_por_unidad_2012_2023": [round(float(tt.titulares_por_unidad.iloc[0]), 3), round(float(tt.titulares_por_unidad.iloc[-1]), 3)],
           "aeat_cv_cuota_pct": {int(a): round(float(c), 1) for a, c in zip(cv.ejercicio, cv.cuota_pct)},
           "asociaciones": R[["cuota", "variable", "N", "spearman", "ic95_inf", "ic95_sup", "p_holm"]].to_dict(orient="records"),
           "ficha_verificador": {"id": f["id"], "veredicto": f["veredicto"], "sustituye": f["sustituye"]},
           "notas": ["cuota municipal = cota inferior (tramos dentro del ámbito)", "sin País Vasco ni Navarra",
                     "asociaciones descriptivas entre municipios; no causales"]}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "asociaciones"}, ensure_ascii=False, indent=1))
    print(R.to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())

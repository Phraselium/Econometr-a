"""V12-B4 · Respuesta de la oferta: dónde se construye y dónde no (descriptivo, C4; sin modelos ni lenguaje causal).

1. Obra nueva NETA del Catastro: variación anual de unidades urbanas de uso residencial por municipio (estadística
   URBANA; fichero «año t» = stock a 31-12-(t−1)). Es neta de bajas e incluye altas administrativas: el procedimiento de
   regularización catastral (2013-2017, Ley 16/2012) incorporó construcciones no declaradas que no son obra nueva del año.
2. Contraste provincial con el MIVAU: viviendas LIBRES terminadas (certificados de fin de obra) + calificaciones
   definitivas de vivienda PROTEGIDA (concordancia nombre → código versionada). Σ municipal del Catastro de la variación
   del año t (ficheros t+1 − t) frente a terminadas del año t. Si las dos fuentes difieren menos de un 25 %
   en un periodo se marca «coinciden» (C1 solo si coinciden; si no, se reportan ambas).
3. INSPIRE (94 municipios de València, su área y las capitales): viviendas por año de construcción (stock superviviente,
   cota inferior de lo construido) frente al Catastro estadístico en los mismos años.
4. Presión: hogares nuevos frente a obra nueva por municipio y periodo.
   - 2021-2025 (todos los municipios ≥ 10.000 hab.): hogares nuevos estimados = Δ población (censo anual, 1-1-2021 →
     1-1-2025) ÷ personas por hogar del municipio en el Censo 2021 (muestra); obra nueva = Catastro ficheros 2022-2025
     (stock 31-12-2020 → 31-12-2024, mismo intervalo). Estimación marcada: supone el tamaño medio de hogar de 2021.
   - 2011-2021 (municipios > 20.000 hab., identificados en los dos censos): hogares de los censos (B3) frente a Catastro
     ficheros 2012-2021 (stock 31-12-2011 → 31-12-2020; ventana de 9 años frente a 10: robustez, marcado).
   - Ratio obra nueva / hogares nuevos y categorías: «obra ≥ hogares», «obra 50-100 %», «obra < 50 %», «hogares no crecen».
   Provincia 2021-2025: hogares observados de la ECP frente a Catastro y MIVAU.
Salidas: output/v12/b4/.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output/v12/b4"
UMBRAL_COINCIDE = 0.25


def catastro() -> pd.DataFrame:
    u = pd.read_csv(RAIZ / "data/raw/catastro_urbana_municipios.csv.gz", dtype={"codigo": str, "periodo": str})
    u = u[(u.unidad == "unidades_urbanas_residenciales") & (u.nivel == "municipio")]
    u = u.assign(fichero=u.periodo.astype(int)).groupby(["codigo", "fichero"], as_index=False).valor.sum()
    u = u.rename(columns={"codigo": "cod_municipio", "valor": "uu_residenciales"}).sort_values(["cod_municipio", "fichero"])
    u["obra_neta"] = u.groupby("cod_municipio").uu_residenciales.diff()
    u.loc[u.groupby("cod_municipio").fichero.diff() != 1, "obra_neta"] = np.nan
    u["anio_obra"] = u.fichero - 1   # el fichero t recoge el stock a 31-12-(t−1): la variación es del año t−1
    return u


def mivau_terminadas() -> pd.DataFrame:
    import pyarrow.parquet as pq
    t = pq.read_table(RAIZ / "data/base/publica/hechos.parquet", columns=["territorio_codigo", "nivel", "periodo", "variable", "frecuencia", "valor"],
                      filters=[("variable", "=", "terminadas"), ("nivel", "in", ["provincia", "ccaa"]), ("frecuencia", "=", "T")]).to_pandas()
    # CCAA uniprovinciales: la serie solo se publica como CCAA → se asigna a su única provincia (código INE)
    terr = pd.read_parquet(RAIZ / "data/base/territorios.parquet")
    prov = terr[terr.nivel == "provincia"].groupby("cod_ccaa").territorio_codigo.agg(list)
    uni = {c: v[0] for c, v in prov.items() if len(v) == 1}
    cc = t[(t.nivel == "ccaa") & t.territorio_codigo.isin(uni)].copy()
    cc["territorio_codigo"] = [uni[c] for c in cc.territorio_codigo]
    t = t[t.nivel == "provincia"]
    t = pd.concat([t, cc[~cc.territorio_codigo.isin(set(t.territorio_codigo))]], ignore_index=True)
    t["anio"] = t.periodo.str[:4].astype(int)
    OUT.mkdir(parents=True, exist_ok=True)
    n = t.groupby(["territorio_codigo", "anio"]).periodo.nunique()
    a = t.groupby(["territorio_codigo", "anio"], as_index=False).valor.sum()
    a["trimestres"] = a.set_index(["territorio_codigo", "anio"]).index.map(n)
    a = a[a.trimestres == 4].rename(columns={"territorio_codigo": "cpro", "valor": "terminadas_mivau"}).drop(columns="trimestres")
    return a.merge(protegida(), how="left", on=["cpro", "anio"])


def _norm(x: str) -> str:
    x = unicodedata.normalize("NFKD", str(x)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z]", "", x)


def protegida() -> pd.DataFrame:
    """Calificaciones definitivas de vivienda protegida (MIVAU, anual). El fichero solo trae nombres: concordancia
    nombre → código INE de provincia (partes separadas por «/», artículo entre paréntesis) y, para las CCAA
    uniprovinciales, CCAA → su única provincia. Se guarda la concordancia; las filas con nota «(1)» se descartan."""
    d = pd.read_csv(RAIZ / "data/raw/mivau_v2_protegida.csv", dtype=str)
    d = d[d.serie.str.startswith("prot_definitiva_anual") & d.nivel.isin(["provincia", "ccaa", "ciudad_autonoma"])]
    t = pd.read_parquet(RAIZ / "data/base/territorios.parquet")
    prov = t[t.nivel == "provincia"]
    claves = {}
    for cod, nom in zip(prov.territorio_codigo, prov.nombre):
        for parte in [nom] + nom.split("/"):
            m = re.match(r"^(.*), *(\w+)$", parte.strip())
            claves.setdefault(_norm(parte), set()).add(cod)
            if m:
                claves.setdefault(_norm(m.group(1)), set()).add(cod)
    uni = prov.groupby("cod_ccaa").territorio_codigo.agg(list)
    uni = {c: v[0] for c, v in uni.items() if len(v) == 1}
    ccaa = t[t.nivel == "ccaa"]
    for cod, nom in zip(ccaa.territorio_codigo, ccaa.nombre):
        if cod in uni:
            for parte in [nom] + nom.split(","):
                claves.setdefault(_norm(parte), set()).add(uni[cod])
    filas = []
    for nom in sorted(d.territorio.unique()):
        if "(1)" in nom or "(*)" in nom:
            filas.append({"territorio_mivau": nom, "cpro": ""})
            continue
        sin = re.sub(r"\s*\((\w+)\)$", r" \1", nom)
        cand = set().union(*[claves.get(_norm(x), set()) for x in [nom, sin, re.sub(r"\s*\(.*\)$", "", nom)] + nom.split("/")])
        filas.append({"territorio_mivau": nom, "cpro": next(iter(cand)) if len(cand) == 1 else ""})
    k = pd.DataFrame(filas)
    k.to_csv(OUT / "concordancia_mivau_protegida_provincias.csv", index=False)
    conc = dict(zip(k.territorio_mivau, k.cpro))
    d["cpro"] = [conc.get(x, "") for x in d.territorio]
    d = d[(d.cpro != "") & d.periodo.str.fullmatch(r"\d{4}")]
    d["anio"], d["valor"] = d.periodo.astype(int), pd.to_numeric(d.valor, errors="coerce")
    return d.groupby(["cpro", "anio"], as_index=False).valor.sum().rename(columns={"valor": "protegida_definitivas"})


def contraste_provincial(u: pd.DataFrame, m: pd.DataFrame) -> pd.DataFrame:
    c = u.dropna(subset=["obra_neta"]).assign(cpro=lambda d: d.cod_municipio.str[:2]).groupby(["cpro", "anio_obra"], as_index=False).obra_neta.sum()
    c = c.rename(columns={"anio_obra": "anio", "obra_neta": "obra_neta_catastro"}).merge(m, how="outer", on=["cpro", "anio"])
    c["terminadas_mivau_total"] = c.terminadas_mivau + c.protegida_definitivas.fillna(0)
    c["ratio_catastro_mivau"] = c.obra_neta_catastro / c.terminadas_mivau_total
    return c.sort_values(["cpro", "anio"])


def inspire(u: pd.DataFrame) -> pd.DataFrame:
    v = pd.read_csv(RAIZ / "data/raw/v11/catastro_inspire/viviendas_por_anio_construccion_municipio.csv.gz", dtype={"cod_municipio": str})
    v = v.rename(columns={"anio_construccion": "anio", "viviendas": "viviendas_inspire"})[["cod_municipio", "anio", "viviendas_inspire"]]
    c = u.rename(columns={"anio_obra": "anio"})[["cod_municipio", "anio", "obra_neta"]]
    x = v[v.anio.between(2011, 2025)].merge(c, how="left", on=["cod_municipio", "anio"])
    return x.sort_values(["cod_municipio", "anio"])


def categoria(r: pd.Series) -> pd.Series:
    return pd.Series(np.select([r.isna(), r < 0, r >= 1, r >= 0.5], ["hogares no crecen", "hogares no crecen", "obra ≥ hogares", "obra 50-100 %"],
                               "obra < 50 %"), index=r.index)


def presion(u: pd.DataFrame) -> pd.DataFrame:
    c = pd.read_csv(RAIZ / "data/raw/v9/ine_censo_anual/censo_seccion_pais.csv.gz", dtype=str)
    c = c[(c.nivel == "municipio") & (c.pais_nacionalidad == "Total")]
    pob = c.assign(p=pd.to_numeric(c.poblacion), a=c.edicion.astype(int)).pivot_table(index="cod_municipio", columns="a", values="p", aggfunc="sum")
    j = pd.read_csv(RAIZ / "data/raw/v11/ine_censos_microdatos/jefatura_2021.csv.gz", dtype={"cpro": str, "cmun": str})
    j = j[~j.cmun.isin(["991", "992", "993"])]
    pph = j.assign(cod=j.cpro + j.cmun).groupby("cod")[["personas_muestra", "referencias_muestra"]].sum()
    pph = (pph.personas_muestra / pph.referencias_muestra).rename("personas_por_hogar_2021")
    ob = u.pivot_table(index="cod_municipio", columns="fichero", values="uu_residenciales")
    filas = []
    d = pd.DataFrame({"poblacion_2021": pob[2021], "poblacion_2025": pob[2025]}).join(pph, how="inner")
    d["hogares_nuevos_estimados"] = (d.poblacion_2025 - d.poblacion_2021) / d.personas_por_hogar_2021
    d["obra_neta"] = ob[2025].reindex(d.index) - ob[2021].reindex(d.index)
    d["periodo"], d["metodo_hogares"] = "2021-2025", "Δ población censo anual ÷ personas por hogar 2021 (estimación)"
    filas.append(d)
    b3 = pd.read_csv(RAIZ / "output/v12/b3/descomposicion_2011_2021_municipio.csv", dtype={"cod_municipio": str}).set_index("cod_municipio")
    e = pd.DataFrame({"hogares_nuevos_estimados": b3.crecimiento})
    e["obra_neta"] = ob[2021].reindex(e.index) - ob[2012].reindex(e.index)
    e["periodo"], e["metodo_hogares"] = "2011-2021", "censos 2011 y 2021 (obra: ficheros 2012-2021, 9 años; robustez)"
    filas.append(e)
    x = pd.concat(filas).rename_axis("cod_municipio").reset_index()
    x["ratio_obra_hogares"] = np.where(x.hogares_nuevos_estimados > 0, x.obra_neta / x.hogares_nuevos_estimados, np.nan)
    x["categoria"] = categoria(x.ratio_obra_hogares)
    return x


def provincial_reciente(u: pd.DataFrame, m: pd.DataFrame) -> pd.DataFrame:
    h = pd.read_csv(RAIZ / "data/raw/ine_v2_hogares_prov.csv", dtype={"codigo": str})
    h = h[(h.nivel == "provincia") & (h.desglose == "tamaño=Total") & h.periodo.isin(["2021T1", "2025T1"])]
    h = h.assign(cpro=h.codigo.str.zfill(2)).pivot_table(index="cpro", columns="periodo", values="valor")
    d = pd.DataFrame({"hogares_nuevos_ecp": h["2025T1"] - h["2021T1"]})
    cat = u[u.anio_obra.between(2021, 2024)].assign(cpro=lambda z: z.cod_municipio.str[:2]).groupby("cpro").obra_neta.sum(min_count=1)
    d["obra_neta_catastro"] = cat
    mm = m[m.anio.between(2021, 2024)]
    d["terminadas_mivau"] = (mm.terminadas_mivau + mm.protegida_definitivas.fillna(0)).groupby(mm.cpro).sum()
    d["ratio_catastro_hogares"] = d.obra_neta_catastro / d.hogares_nuevos_ecp
    d["ratio_mivau_hogares"] = d.terminadas_mivau / d.hogares_nuevos_ecp
    d["fuentes_oferta_coinciden"] = (d.obra_neta_catastro / d.terminadas_mivau - 1).abs() < UMBRAL_COINCIDE
    d["capa"] = np.where(d.fuentes_oferta_coinciden, "C1 (oferta: dos fuentes coinciden)", "C4 (fuentes de oferta discrepan: se reportan ambas)")
    return d.rename_axis("cpro").reset_index()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    u = catastro()
    m = mivau_terminadas()
    u[["cod_municipio", "fichero", "anio_obra", "uu_residenciales", "obra_neta"]].to_csv(OUT / "obra_neta_catastro_municipio.csv.gz", index=False,
                                                                                         compression={"method": "gzip", "mtime": 0})
    cp = contraste_provincial(u, m)
    cp.to_csv(OUT / "contraste_catastro_mivau_provincia.csv", index=False, float_format="%.10g")
    ins = inspire(u)
    ins.to_csv(OUT / "inspire_frente_catastro.csv", index=False)
    pr = presion(u)
    pr.to_csv(OUT / "presion_hogares_obra_municipio.csv", index=False, float_format="%.10g")
    pv = provincial_reciente(u, m)
    pv.to_csv(OUT / "presion_provincia_2021_2025.csv", index=False, float_format="%.10g")
    nac = cp.groupby("anio")[["obra_neta_catastro", "terminadas_mivau", "protegida_definitivas", "terminadas_mivau_total"]].sum(min_count=1)
    reg = nac.loc[2013:2017]
    res = {"rama": "V12-B4", "pregunta": "¿Dónde se construye y dónde no?", "capa": "C4", "metodo": "contable y descriptivo",
           "datos": "Catastro URBANA e INSPIRE; MIVAU terminadas; censo anual; Censos 2011/2021; ECP hogares", "N": int(len(pr)),
           "nacional_catastro_vs_mivau": {int(a): {k: (None if pd.isna(v) else int(v)) for k, v in r.items()} for a, r in nac.iterrows()},
           "regularizacion_2013_2017_catastro_menos_mivau": int((reg.obra_neta_catastro - reg.terminadas_mivau_total).sum()),
           "municipios_2021_2025_por_categoria": pr[pr.periodo == "2021-2025"].categoria.value_counts().to_dict(),
           "municipios_2011_2021_por_categoria": pr[pr.periodo == "2011-2021"].categoria.value_counts().to_dict(),
           # misma muestra para las tres magnitudes: provincias con Catastro y MIVAU (sin País Vasco, Navarra, Ceuta ni Melilla)
           "provincia_2021_2025": {"provincias": int(pv.dropna(subset=["obra_neta_catastro", "terminadas_mivau"]).shape[0]),
                                   **{k: int(pv.dropna(subset=["obra_neta_catastro", "terminadas_mivau"])[k].sum())
                                      for k in ("hogares_nuevos_ecp", "obra_neta_catastro", "terminadas_mivau")},
                                   "provincias_fuentes_coinciden": int(pv.fuentes_oferta_coinciden.sum())},
           "inspire_municipios": int(ins.cod_municipio.nunique()),
           "notas": ["obra nueva neta del Catastro incluye regularizaciones administrativas (2013-2017)",
                     "hogares nuevos 2021-2025 municipales estimados con el tamaño de hogar de 2021",
                     "ratio obra/hogares descriptivo: no mide necesidad ni déficit (ver v7.1)"]}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

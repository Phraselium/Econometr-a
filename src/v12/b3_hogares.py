"""V12-B3 · Hogares y presión (descriptivo y contable, C4; sin modelos).

1. Tasas de jefatura (hogares / personas en viviendas familiares) por grupo quinquenal de edad y nacionalidad, de los
   microdatos de los Censos 2011 y 2021 (data/raw/v11/ine_censos_microdatos, extraídos por
   src/v11/fetch_ine_censos_microdatos.py). «Persona de referencia» = persona de MAYOR edad del hogar (regla común a los
   dos censos); 2011 con el factor de elevación del INE; 2021 sin factor (muestra del 10 % de los hogares): se calibra a
   los hogares de la ECP a 1-1-2021 de cada provincia (factor uniforme por provincia).
2. Descomposición del crecimiento de hogares 2011 → 2021 (H = P · Σ s_a · h_a):
     población  = (P1 − P0) · Σ s0 h0
     estructura = P1 · Σ (s1 − s0) h0
     jefatura   = P1 · Σ s1 (h1 − h0)
   y en el orden inverso (jefatura primero); se publican los dos órdenes (la suma es idéntica, el reparto no).
   Niveles: España, CCAA, provincia y municipio (solo los > 20.000 hab., los identificados en ambos censos).
3. 2021 → último 1 de enero con ECP (provincia): hogares esperados con la jefatura por edad del Censo 2021 y la
   población por edad de la ECP; la diferencia con los hogares observados de la ECP es el cambio implícito de jefatura.
4. Hogares por nacionalidad de la primera persona (Censo 2021, muestra): cuota con IC95 (muestreo aleatorio de hogares,
   corrección por población finita f = 0,1). No se publican celdas con < 10 hogares en la muestra ni con error relativo
   del recuento > 30 %.
Salidas: output/v12/b3/.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import GZ_PANDAS  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
CM = RAIZ / "data/raw/v11/ine_censos_microdatos"
OUT = RAIZ / "output/v12/b3"
F_MUESTRA = 0.10
MIN_CASOS, RSE_MAX = 10, 0.30
EDADES = ["0-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69",
          "70-74", "75-79", "80-84", "85+"]


def ccaa_de_provincia() -> dict:
    t = pd.read_parquet(RAIZ / "data/base/territorios.parquet")
    return t[t.nivel == "provincia"].set_index("territorio_codigo").cod_ccaa.to_dict()


def hogares_ecp() -> pd.DataFrame:
    h = pd.read_csv(RAIZ / "data/raw/ine_v2_hogares_prov.csv", dtype={"codigo": str})
    h = h[(h.nivel == "provincia") & (h.desglose == "tamaño=Total") & h.periodo.str.endswith("T1")]
    return h.assign(anio=h.periodo.str[:4].astype(int), cpro=h.codigo.str.zfill(2))[["cpro", "anio", "valor"]].rename(columns={"valor": "hogares"})


def jefatura() -> pd.DataFrame:
    j11 = pd.read_csv(CM / "jefatura_2011.csv.gz", dtype={"cpro": str, "cmun": str}).assign(anio=2011)
    j21 = pd.read_csv(CM / "jefatura_2021.csv.gz", dtype={"cpro": str, "cmun": str}).assign(anio=2021)
    # calibración 2021: hogares de la muestra × factor provincial = hogares ECP 1-1-2021
    he = hogares_ecp()
    he = he[he.anio == 2021].set_index("cpro").hogares
    fac = he / j21.groupby("cpro").referencias.sum()
    j21["factor"] = j21.cpro.map(fac)
    for c in ("personas", "referencias"):
        j21[c] = j21[c] * j21.factor
    return pd.concat([j11, j21.drop(columns="factor")], ignore_index=True)


def tasas(j: pd.DataFrame, claves: list[str]) -> pd.DataFrame:
    g = j.groupby(claves + ["anio", "grupo_edad"], as_index=False)[["personas", "referencias", "personas_muestra", "referencias_muestra"]].sum()
    g["jefatura"] = g.referencias / g.personas
    return g


def descomponer(g: pd.DataFrame, claves: list[str]) -> pd.DataFrame:
    filas = []
    for k, x in g.groupby(claves) if claves else [((), g)]:
        w = x.pivot_table(index="grupo_edad", columns="anio", values=["personas", "jefatura"]).reindex(EDADES).fillna(0)
        if (2011 not in w["personas"]) or (2021 not in w["personas"]):
            continue
        P0, P1 = w["personas"][2011].sum(), w["personas"][2021].sum()
        s0, s1 = w["personas"][2011] / P0, w["personas"][2021] / P1
        h0, h1 = w["jefatura"][2011], w["jefatura"][2021]
        H0, H1 = (P0 * s0 * h0).sum(), (P1 * s1 * h1).sum()
        # orden A: población → estructura → jefatura; orden B: jefatura → estructura → población
        a = {"poblacion": (P1 - P0) * (s0 * h0).sum(), "estructura": P1 * ((s1 - s0) * h0).sum(), "jefatura": P1 * (s1 * (h1 - h0)).sum()}
        b = {"jefatura": P0 * (s0 * (h1 - h0)).sum(), "estructura": P0 * ((s1 - s0) * h1).sum(), "poblacion": (P1 - P0) * (s1 * h1).sum()}
        f = dict(zip(claves, k if isinstance(k, tuple) else (k,)))
        f.update({"hogares_2011": H0, "hogares_2021": H1, "crecimiento": H1 - H0, "personas_2011": P0, "personas_2021": P1,
                  "personas_por_hogar_2011": P0 / H0, "personas_por_hogar_2021": P1 / H1,
                  "referencias_muestra_2011": x.loc[x.anio == 2011, "referencias_muestra"].sum(),
                  "referencias_muestra_2021": x.loc[x.anio == 2021, "referencias_muestra"].sum()})
        for o, d in (("A", a), ("B", b)):
            for c, v in d.items():
                f[f"{c}_{o}"] = v
        filas.append(f)
    r = pd.DataFrame(filas)
    for c in ("poblacion", "estructura", "jefatura"):
        r[f"pct_{c}_media"] = 100 * (r[f"{c}_A"] + r[f"{c}_B"]) / 2 / r.crecimiento.abs()
    return r


def ecp_edad() -> pd.DataFrame:
    """Población ECP por provincia × grupo de edad × 1 de enero (2021-último), todas las nacionalidades."""
    e = pd.read_csv(RAIZ / "data/raw/v11/ine_ecp/ecp_t60129.csv.gz", dtype=str)
    e = e[(e.Nacionalidad == "Total") & e.Periodo.str.startswith("1 de enero")]
    e["cpro"] = e.Provincias.str[:2]
    e = e[e.cpro.str.fullmatch(r"\d{2}")]
    ini = e["Grupo quinquenal de edad"].str.extract(r"(\d+)")[0].astype(float)
    e["grupo_edad"] = pd.cut(ini, [-1, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 84, 200], labels=EDADES).astype(str)
    e = e[ini.notna()]
    e["anio"] = e.fecha.str[:4].astype(int)
    e["poblacion"] = pd.to_numeric(e.Total.str.replace(".", "", regex=False), errors="coerce")
    return e.groupby(["cpro", "anio", "grupo_edad"], as_index=False).poblacion.sum()


def reciente(g21: pd.DataFrame) -> pd.DataFrame:
    """2021 → último año: hogares esperados con la jefatura del Censo 2021 frente a hogares ECP observados."""
    e, he = ecp_edad(), hogares_ecp()
    ult = int(min(e.anio.max(), he.anio.max()))
    filas = []
    for cpro, x in g21.groupby("cpro"):
        x = x.set_index("grupo_edad").reindex(EDADES).fillna(0)
        p = e[e.cpro == cpro].pivot_table(index="grupo_edad", columns="anio", values="poblacion").reindex(EDADES)
        if 2021 not in p or ult not in p:
            continue
        r = (p[ult] / p[2021]).fillna(1.0)
        hh21 = x.personas
        H21 = (hh21 * x.jefatura).sum()
        Hpob = H21 * p[ult].sum() / p[2021].sum()
        Hesp = (hh21 * r * x.jefatura).sum()
        Hobs21 = float(he[(he.cpro == cpro) & (he.anio == 2021)].hogares.iloc[0])
        Hobs = float(he[(he.cpro == cpro) & (he.anio == ult)].hogares.iloc[0])
        filas.append({"cpro": cpro, "periodo": f"2021-{ult}", "hogares_2021": Hobs21, f"hogares_{ult}": Hobs, "crecimiento_observado": Hobs - Hobs21,
                      "efecto_poblacion": Hpob - H21, "efecto_estructura_edad": Hesp - Hpob,
                      "cambio_jefatura_implicito": (Hobs - Hobs21) - (Hesp - H21)})
    return pd.DataFrame(filas)


def nacionalidad_hogares() -> pd.DataFrame:
    """Cuota de hogares cuya primera persona tiene nacionalidad extranjera (Censo 2021, muestra), con IC95."""
    h = pd.read_csv(RAIZ / "data/raw/v11/ine_censo2021/hogares_muestra_municipio_nacionalidad.csv.gz", dtype={"cod_municipio": str})
    pc = ccaa_de_provincia()
    filas = []
    niveles = {"municipio": h.cod_municipio, "provincia": h.cod_municipio.str[:2], "ccaa": h.cod_municipio.str[:2].map(pc),
               "nacional": pd.Series("00", index=h.index)}
    for nivel, k in niveles.items():
        g = h.assign(k=k).groupby(["k", "nac_primera_persona"]).hogares_muestra.sum().unstack(fill_value=0)
        for cod, r in g.iterrows():
            if nivel == "municipio" and cod[2:] in ("991", "992", "993"):
                continue
            n, x = int(r.sum()), int(r.get("EXT", 0))
            p = x / n if n else np.nan
            se = np.sqrt(p * (1 - p) / n * (1 - F_MUESTRA)) if n else np.nan
            rse = se / p if p else np.inf
            ok = x >= MIN_CASOS and rse <= RSE_MAX
            filas.append({"nivel": nivel, "cod_territorio": cod, "hogares_muestra": n, "hogares_ext_muestra": x if ok else np.nan,
                          "cuota_ext_pct": round(100 * p, 2) if ok else np.nan, "ic95_inf": round(100 * max(p - 1.96 * se, 0), 2) if ok else np.nan,
                          "ic95_sup": round(100 * (p + 1.96 * se), 2) if ok else np.nan, "error_relativo": round(rse, 3) if np.isfinite(rse) else np.nan,
                          "publicable": ok})
    return pd.DataFrame(filas)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    j = jefatura()
    pc = ccaa_de_provincia()
    j["ccaa"] = j.cpro.map(pc)
    j["cod_municipio"] = j.cpro + j.cmun
    # municipios identificados en ambos censos (> 20.000 hab. en 2011; los grupos 991-994 son tamaños de municipio)
    ident = set(j[(j.anio == 2011) & ~j.cmun.isin(["991", "992", "993", "994"])].cod_municipio) & \
        set(j[(j.anio == 2021) & ~j.cmun.isin(["991", "992", "993"])].cod_municipio)
    salidas = {}
    for nivel, claves, sub in (("nacional", [], j), ("ccaa", ["ccaa"], j), ("provincia", ["cpro"], j),
                               ("municipio", ["cod_municipio"], j[j.cod_municipio.isin(ident)])):
        t = tasas(sub, claves)
        t.to_csv(OUT / f"jefatura_{nivel}.csv{'.gz' if nivel == 'municipio' else ''}", index=False, float_format="%.10g",
                 compression=GZ_PANDAS if nivel == "municipio" else None)
        d = descomponer(t, claves)
        d.insert(0, "nivel", nivel)
        d.to_csv(OUT / f"descomposicion_2011_2021_{nivel}.csv", index=False, float_format="%.10g")
        salidas[nivel] = d
    rec = reciente(tasas(j[j.anio == 2021], ["cpro"]))
    rec.to_csv(OUT / "hogares_reciente_provincia.csv", index=False, float_format="%.10g")
    nh = nacionalidad_hogares()
    nh.to_csv(OUT / "hogares_nacionalidad_censo2021.csv", index=False)
    n = salidas["nacional"].iloc[0]
    rt = rec.sum(numeric_only=True)
    res = {"rama": "V12-B3", "pregunta": "¿Por qué crece el número de hogares?", "capa": "C4", "metodo": "descomposición contable (dos órdenes)",
           "datos": "Censos 2011 y 2021 (microdatos), ECP (hogares y población por edad)", "N": int(len(j)),
           "nacional_2011_2021": {k: round(float(n[k])) for k in ("hogares_2011", "hogares_2021", "crecimiento", "poblacion_A", "estructura_A",
                                                                   "jefatura_A", "poblacion_B", "estructura_B", "jefatura_B")},
           "personas_por_hogar": [round(float(n.personas_por_hogar_2011), 3), round(float(n.personas_por_hogar_2021), 3)],
           "reciente_suma_provincias": {k: round(float(rt[k])) for k in ("crecimiento_observado", "efecto_poblacion", "efecto_estructura_edad", "cambio_jefatura_implicito")},
           "periodo_reciente": rec.periodo.iloc[0] if len(rec) else None,
           "hogares_nacionalidad": {"municipios_publicables": int(nh[(nh.nivel == "municipio") & nh.publicable].shape[0]),
                                    "municipios_suprimidos": int(nh[(nh.nivel == "municipio") & ~nh.publicable].shape[0]),
                                    "nacional_cuota_ext": nh[nh.nivel == "nacional"][["cuota_ext_pct", "ic95_inf", "ic95_sup"]].iloc[0].to_dict()},
           "notas": ["persona de referencia = persona de mayor edad del hogar (común a 2011 y 2021)", "2021 calibrado a hogares ECP por provincia",
                     "los dos órdenes de la descomposición se publican porque el reparto depende del orden"]}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1, default=float))
    return 0


if __name__ == "__main__":
    sys.exit(main())

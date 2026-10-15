"""V12-B1 · De dónde viene la población: contabilidad demográfica (descriptivo, C4; identidad contable con residuo).

Para cada territorio y año t (flujos del año natural t; población a 1 de enero de t y t+1):
    ΔP = (nacimientos − defunciones) + (inmigración exterior − emigración exterior) + (altas − bajas interiores) + residuo
Fuentes (data/raw/v11, cruce por código INE):
- vegetativo: MNP microdatos (municipio de residencia; nacionalidad desde 1996/1999);
- exterior: EVR hasta 2020 (altas desde el extranjero; bajas al extranjero registradas desde 2002) y EMCR desde 2021;
- interior: EVR hasta 2020 y EMCR desde 2021 (saldo de movimientos entre municipios de España);
- población: padrón continuo municipal a 1 de enero 2003-2022 (v9) y censo anual 2021-2025 (v9). Para ΔP de 2003-2021 se
  usa el padrón; para 2022-2024 el censo anual (empalme en 2022; ambas fuentes coinciden en 2021-2022 → C1 si la
  diferencia es < 1 %; se publica la diferencia).
- Empalme EVR → EMCR en 2021: se usa la EMCR (metodología vigente; incluye correcciones por omisión que la EVR no tenía).
  La EVR de 2021 se guarda para comparar (empalme_2021.csv).
Niveles: municipio ≥ 10.000 hab. (los menores están agregados como PP999 en los microdatos: sus flujos solo se suman a
provincia), provincia, CCAA y España. Nacionalidad: total, ES, EXT (la población por nacionalidad cambia también por
adquisiciones de nacionalidad, que no son flujos: van al residuo de cada grupo y se documenta).
Periodos: 2002-2007 (municipal y provincial desde 2003 por la población municipal), 2008-2013, 2014-2019, 2020-2021,
2022-2024 (último año con flujos completos).
Salidas en output/v12/b1/: contabilidad_anual_<nivel>.csv, contabilidad_periodos_<nivel>.csv, empalme_2021.csv,
resultado.json, hechos.json.
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
RAW11, RAW9 = RAIZ / "data/raw/v11", RAIZ / "data/raw/v9"
OUT = RAIZ / "output/v12/b1"
PERIODOS = {"2003-2007": (2003, 2007), "2008-2013": (2008, 2013), "2014-2019": (2014, 2019), "2020-2021": (2020, 2021),
            "2022-2024": (2022, 2024)}


def ccaa_de_provincia() -> dict:
    t = pd.read_parquet(RAIZ / "data/base/territorios.parquet")
    return t[t.nivel == "provincia"].set_index("territorio_codigo").cod_ccaa.to_dict()


def flujos() -> pd.DataFrame:
    """Flujos anuales por municipio (incluye PP999) × nacionalidad (ES, EXT, NC)."""
    m = pd.read_csv(RAW11 / "ine_mnp/mnp_municipio.csv.gz", dtype={"cod_municipio": str})
    m = m[m.cod_municipio != "EXTR"].rename(columns={"saldo_vegetativo": "vegetativo"})[["anio", "cod_municipio", "nac", "nacimientos", "defunciones", "vegetativo"]]
    partes = []
    for fuente, ini, fin in (("ine_evr", 2002, 2020), ("ine_emcr", 2021, 2024)):
        s = pd.read_csv(RAW11 / f"{fuente}/saldos_internos_municipio.csv.gz", dtype={"cod_municipio": str})
        s = s[s.anio.between(ini, fin)].groupby(["anio", "cod_municipio", "nac"], as_index=False)[["altas", "bajas"]].sum()
        s = s.rename(columns={"altas": "altas_interiores", "bajas": "bajas_interiores"})
        e = pd.read_csv(RAW11 / f"{fuente}/flujos_exterior_municipio.csv.gz", dtype=str)
        pais = "cnac" if "cnac" in e else "pais_nacionalidad"
        e["nac"] = np.where(e[pais].str.strip() == "108", "ES", "EXT")
        e["anio"] = e.anio.astype(int)
        e = e[e.anio.between(ini, fin) & ~e.cod_municipio.str.startswith("66")]
        cin, cout = ("altas_desde_extranjero", "bajas_al_extranjero") if fuente == "ine_evr" else ("inmigracion_exterior", "emigracion_exterior")
        for c in (cin, cout):
            e[c] = pd.to_numeric(e[c])
        e = e.groupby(["anio", "cod_municipio", "nac"], as_index=False)[[cin, cout]].sum().rename(columns={cin: "inmigracion_exterior", cout: "emigracion_exterior"})
        x = s.merge(e, how="outer", on=["anio", "cod_municipio", "nac"])
        x["fuente_migraciones"] = "EVR" if fuente == "ine_evr" else "EMCR"
        partes.append(x)
    f = pd.concat(partes, ignore_index=True).merge(m, how="outer", on=["anio", "cod_municipio", "nac"])
    f = f[f.anio.between(2002, 2024)]
    num = ["nacimientos", "defunciones", "vegetativo", "inmigracion_exterior", "emigracion_exterior", "altas_interiores", "bajas_interiores"]
    f[num] = f[num].fillna(0)
    f["fuente_migraciones"] = np.where(f.anio <= 2020, "EVR", "EMCR")
    f["saldo_exterior"] = f.inmigracion_exterior - f.emigracion_exterior
    f["saldo_interior"] = f.altas_interiores - f.bajas_interiores
    return f


def poblacion() -> pd.DataFrame:
    """Población a 1 de enero por municipio y nacionalidad (Total, ES, EXT): padrón 2003-2022 y censo anual 2021-2025."""
    p = pd.read_csv(RAW9 / "ine_padron_nacionalidad/padron_nacionalidad_2003_2022.csv.gz", dtype={"cod_municipio": str})
    p = p[p.cod_municipio.notna() & p.nacionalidad.isin(["Total", "Española", "Extranjera"])]
    p["nac"] = p.nacionalidad.map({"Total": "TOTAL", "Española": "ES", "Extranjera": "EXT"})
    p = p.groupby(["anio", "cod_municipio", "nac"], as_index=False).poblacion.sum().assign(fuente_poblacion="padron")
    c = pd.read_csv(RAW9 / "ine_censo_anual/censo_seccion_pais.csv.gz", dtype=str)
    c = c[c.nivel == "municipio"]
    c["poblacion"] = pd.to_numeric(c.poblacion)
    tot = c[c.pais_nacionalidad == "Total"].groupby(["edicion", "cod_municipio"], as_index=False).poblacion.sum().assign(nac="TOTAL")
    es = c[c.pais_nacionalidad == "España"].groupby(["edicion", "cod_municipio"], as_index=False).poblacion.sum().assign(nac="ES")
    ex = tot.merge(es, on=["edicion", "cod_municipio"], suffixes=("", "_es"))
    ex = ex.assign(poblacion=ex.poblacion - ex.poblacion_es, nac="EXT")[["edicion", "cod_municipio", "poblacion", "nac"]]
    c = pd.concat([tot, es, ex]).rename(columns={"edicion": "anio"})
    c["anio"] = c.anio.astype(int)
    c = c.assign(fuente_poblacion="censo_anual")
    return pd.concat([p, c], ignore_index=True)


def agregar(f: pd.DataFrame, P: pd.DataFrame, nivel: str, prov_ccaa: dict) -> pd.DataFrame:
    def clave(cod: pd.Series) -> pd.Series:
        if nivel == "municipio":
            return cod
        if nivel == "provincia":
            return cod.str[:2]
        if nivel == "ccaa":
            return cod.str[:2].map(prov_ccaa)
        return pd.Series("00", index=cod.index)
    num = ["nacimientos", "defunciones", "vegetativo", "inmigracion_exterior", "emigracion_exterior", "saldo_exterior",
           "altas_interiores", "bajas_interiores", "saldo_interior"]
    f = f.copy()
    if nivel == "municipio":
        f = f[~f.cod_municipio.str[2:].isin(["999"])]
    f["territorio"] = clave(f.cod_municipio)
    fl = f.groupby(["territorio", "anio", "nac"], as_index=False)[num].sum()
    flt = fl.groupby(["territorio", "anio"], as_index=False)[num].sum().assign(nac="TOTAL")
    fl = pd.concat([fl[fl.nac.isin(["ES", "EXT"])], flt], ignore_index=True)
    P = P.copy()
    P["territorio"] = clave(P.cod_municipio)
    pp = P.groupby(["territorio", "anio", "nac", "fuente_poblacion"], as_index=False).poblacion.sum()
    # ΔP con la misma fuente en t y t+1: padrón para t ≤ 2021, censo anual para t ≥ 2022
    filas = []
    for fuente, rango in (("padron", range(2003, 2022)), ("censo_anual", range(2022, 2025))):
        q = pp[pp.fuente_poblacion == fuente].set_index(["territorio", "nac", "anio"]).poblacion
        for t in rango:
            if (t + 1) not in q.index.get_level_values("anio") or t not in q.index.get_level_values("anio"):
                continue
            a, b = q.xs(t, level="anio"), q.xs(t + 1, level="anio")
            d = pd.concat([a.rename("poblacion_inicio"), b.rename("poblacion_fin")], axis=1).dropna().reset_index()
            d["anio"], d["fuente_poblacion"] = t, fuente
            filas.append(d)
    dp = pd.concat(filas, ignore_index=True)
    dp["crecimiento"] = dp.poblacion_fin - dp.poblacion_inicio
    out = dp.merge(fl, how="left", on=["territorio", "anio", "nac"])
    out[num] = out[num].fillna(0)
    out["residuo"] = out.crecimiento - out.vegetativo - out.saldo_exterior - out.saldo_interior
    out["nivel"] = nivel
    return out


def periodos(a: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for nombre, (i, j) in PERIODOS.items():
        x = a[a.anio.between(i, j)]
        g = x.groupby(["nivel", "territorio", "nac"])
        r = g[["crecimiento", "vegetativo", "saldo_exterior", "saldo_interior", "residuo", "inmigracion_exterior",
               "emigracion_exterior", "altas_interiores", "bajas_interiores"]].sum()
        r["anios"] = g.anio.nunique()
        r["poblacion_inicio"] = x[x.anio == i].set_index(["nivel", "territorio", "nac"]).poblacion_inicio
        r = r.reset_index()
        r["periodo"] = nombre
        r = r[r.anios == (j - i + 1)]
        for c in ("vegetativo", "saldo_exterior", "saldo_interior", "residuo"):
            r[f"pct_{c}"] = np.where(r.crecimiento != 0, 100 * r[c] / r.crecimiento.abs(), np.nan)
            r[f"tasa_{c}_por_mil_anual"] = 1000 * r[c] / r.poblacion_inicio / r.anios
        r["tasa_crecimiento_por_mil_anual"] = 1000 * r.crecimiento / r.poblacion_inicio / r.anios
        filas.append(r)
    return pd.concat(filas, ignore_index=True)


def valencia() -> dict:
    """València por sección y barrio, 2021-2025 (censo anual por sección × nacionalidad; INE 2021-2025).

    No hay flujos (nacimientos, migraciones) por sección: solo la variación de población por nacionalidad (stock), sin
    descomposición contable. Sección → barrio: si la sección cae en un solo barrio (≥ 95 % de su área) se asigna entera;
    si no, se reparte por área (aproximación: supone densidad uniforme; se publica la población repartida). Las secciones
    sin correspondencia van a «sin asignar». Celdas < 10 personas por país se suprimen al publicar (se conservan Total,
    España y EXT). El padrón por barrio con nacionalidad del Ajuntament no está en data/raw (ver decisiones).
    Cambios de seccionado 2021-2025: solo hay cartografía (y correspondencia con barrios) del seccionado vigente, y
    varias secciones se dividen o desaparecen. La variación 2021→2025 es exacta por distrito (las secciones no cambian
    de distrito) y por barrio solo se publica si su distrito no tuvo cambios de seccionado («comparable»)."""
    c = pd.read_csv(RAW9 / "ine_censo_anual/censo_seccion_pais.csv.gz", dtype=str)
    s = c[(c.nivel == "seccion") & (c.cod_municipio == "46250")].copy()
    s["poblacion"] = pd.to_numeric(s.poblacion)
    s["anio"] = s.edicion.astype(int)
    w = s.pivot_table(index=["cod_seccion", "anio"], columns="pais_nacionalidad", values="poblacion", aggfunc="sum").fillna(0)
    w["EXT"] = w["Total"] - w["España"]
    tot_w = s[s.pais_nacionalidad == "Total"].pivot(index="cod_seccion", columns="anio", values="poblacion")   # NaN = no existe
    k0 = pd.read_csv(RAIZ / "data/base/geo/correspondencia_seccion_barrio_valencia.csv", dtype={"cod_seccion": str})
    cambia = tot_w.index[tot_w.isna().any(axis=1) | ~tot_w.index.isin(k0.cod_seccion)]
    dist_afectados = sorted(set(cambia.str[5:7]))
    existe = tot_w.stack().index   # (cod_seccion, anio) con la sección vigente ese año
    sec = w[w.index.isin(existe)].reset_index()
    k = pd.read_csv(RAIZ / "data/base/geo/correspondencia_seccion_barrio_valencia.csv", dtype={"cod_seccion": str, "cod_barrio": str})
    unico = k[k.seccion_en_un_barrio].sort_values("peso_area").groupby("cod_seccion").tail(1).assign(peso=1.0)
    rep = k[~k.seccion_en_un_barrio].assign(peso=lambda d: d.peso_area / d.groupby("cod_seccion").peso_area.transform("sum"))
    corr = pd.concat([unico, rep])[["cod_seccion", "cod_barrio", "peso", "seccion_en_un_barrio"]]
    x = sec.merge(corr, how="left", on="cod_seccion")
    x["cod_barrio"] = x.cod_barrio.fillna("sin_asignar")
    x["peso"] = x.peso.fillna(1.0)
    paises = [p for p in w.columns if p not in ("Total", "España", "EXT")]
    cols = ["Total", "España", "EXT"] + paises
    x[cols] = x[cols].mul(x.peso, axis=0)
    x["repartido_por_area"] = np.where(x.seccion_en_un_barrio.eq(False), x.Total, 0.0)
    b = x.groupby(["cod_barrio", "anio"], as_index=False)[cols + ["repartido_por_area"]].sum()
    nombres = pd.read_parquet(RAIZ / "data/base/geo/barrios_valencia.parquet", columns=["cod_barrio", "cod_distrito", "nombre"])
    b = b.merge(nombres, how="left", on="cod_barrio")

    def largo(d: pd.DataFrame, clave: str) -> pd.DataFrame:
        L = d.melt(id_vars=[clave, "anio"], value_vars=cols, var_name="nacionalidad", value_name="poblacion")
        L["poblacion"] = L.poblacion.round(0)
        L["suprimido_menor_10"] = ~L.nacionalidad.isin(["Total", "España", "EXT"]) & (L.poblacion < 10)
        L.loc[L.suprimido_menor_10, "poblacion"] = np.nan
        return L

    ls, lb = largo(sec, "cod_seccion"), largo(b, "cod_barrio")
    ls.to_csv(OUT / "valencia_seccion_nacionalidad.csv.gz", index=False, compression=GZ_PANDAS)
    lb.to_csv(OUT / "valencia_barrio_nacionalidad.csv", index=False)
    # variación 2021 → 2025 por barrio (Total, España, EXT)
    v = b.set_index(["cod_barrio", "anio"])[["Total", "España", "EXT"]].unstack("anio")
    d = pd.DataFrame({f"{g}_{a}": v[(g, a)] for g in ("Total", "España", "EXT") for a in (2021, 2025)})
    for g in ("Total", "España", "EXT"):
        d[f"var_{g}_2021_2025"] = d[f"{g}_2025"] - d[f"{g}_2021"]
    d["cuota_EXT_2021"], d["cuota_EXT_2025"] = 100 * d.EXT_2021 / d.Total_2021, 100 * d.EXT_2025 / d.Total_2025
    d["pct_var_explicada_por_EXT"] = np.where(d.var_Total_2021_2025 != 0, 100 * d.var_EXT_2021_2025 / d.var_Total_2021_2025.abs(), np.nan)
    d = d.round(1).join(nombres.set_index("cod_barrio")).reset_index()
    d = d[d.cod_barrio != "sin_asignar"]
    d["comparable"] = ~d.cod_barrio.str[5:7].isin(dist_afectados)
    var = [c for c in d.columns if c.startswith(("var_", "pct_var"))]
    d.loc[~d.comparable, var] = np.nan   # cambio de seccionado en el distrito: la variación por barrio no es comparable
    d.to_csv(OUT / "valencia_barrio_variacion_2021_2025.csv", index=False)
    di = sec.assign(cod_distrito=sec.cod_seccion.str[:7]).groupby(["cod_distrito", "anio"])[["Total", "España", "EXT"]].sum().unstack("anio")
    dd = pd.DataFrame({f"{g}_{a}": di[(g, a)] for g in ("Total", "España", "EXT") for a in range(2021, 2026)})
    for g in ("Total", "España", "EXT"):
        dd[f"var_{g}_2021_2025"] = dd[f"{g}_2025"] - dd[f"{g}_2021"]
    dd["cuota_EXT_2021"], dd["cuota_EXT_2025"] = (100 * dd.EXT_2021 / dd.Total_2021).round(1), (100 * dd.EXT_2025 / dd.Total_2025).round(1)
    dd["cambio_seccionado"] = dd.index.str[5:7].isin(dist_afectados)
    dd.reset_index().to_csv(OUT / "valencia_distrito_variacion_2021_2025.csv", index=False)
    tot = sec.groupby("anio")[["Total", "España", "EXT"]].sum()
    sin = b[b.cod_barrio == "sin_asignar"].set_index("anio").Total.reindex(range(2021, 2026)).fillna(0)
    return {"secciones": int(sec.cod_seccion.nunique()), "barrios": int((d.cod_barrio != "sin_asignar").sum()),
            "secciones_sin_correspondencia": int(sec.loc[~sec.cod_seccion.isin(k.cod_seccion), "cod_seccion"].nunique()),
            "poblacion_repartida_por_area_2025_pct": round(float(100 * x[x.anio == 2025].repartido_por_area.sum() / tot.loc[2025, "Total"]), 1),
            "total_2021": int(tot.loc[2021, "Total"]), "total_2025": int(tot.loc[2025, "Total"]),
            "var_total": int(tot.loc[2025, "Total"] - tot.loc[2021, "Total"]),
            "var_espanola": int(tot.loc[2025, "España"] - tot.loc[2021, "España"]),
            "var_extranjera": int(tot.loc[2025, "EXT"] - tot.loc[2021, "EXT"]),
            "distritos_con_cambio_de_seccionado": dist_afectados, "barrios_comparables_2021_2025": int(d.comparable.sum()),
            "poblacion_sin_asignar_a_barrio": {int(a): int(v) for a, v in sin.items()},
            "barrios_comparables_que_pierden_poblacion": int((d.var_Total_2021_2025 < 0).sum()),
            "nota": "variación de stocks por nacionalidad; la población española también cambia por adquisiciones de nacionalidad"}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    pc = ccaa_de_provincia()
    f, P = flujos(), poblacion()
    anual = pd.concat([agregar(f, P, n, pc) for n in ("municipio", "provincia", "ccaa", "nacional")], ignore_index=True)
    for n, g in anual.groupby("nivel"):
        gz = n == "municipio"   # el municipal pesa ~35 MB sin comprimir
        g.sort_values(["territorio", "nac", "anio"]).to_csv(OUT / f"contabilidad_anual_{n}.csv{'.gz' if gz else ''}", index=False,
                                                            float_format="%.6g", compression=GZ_PANDAS if gz else None)
    per = periodos(anual)
    for n, g in per.groupby("nivel"):
        gz = n == "municipio"
        g.sort_values(["territorio", "nac", "periodo"]).to_csv(OUT / f"contabilidad_periodos_{n}.csv{'.gz' if gz else ''}", index=False,
                                                               float_format="%.6g", compression=GZ_PANDAS if gz else None)
    # empalme 2021 (EVR frente a EMCR, nacional) y población padrón frente a censo anual (2021 y 2022)
    emp = []
    for fuente in ("ine_evr", "ine_emcr"):
        e = pd.read_csv(RAW11 / f"{fuente}/flujos_exterior_municipio.csv.gz", dtype=str)
        e = e[(e.anio == "2021") & ~e.cod_municipio.str.startswith("66")]
        cin, cout = ("altas_desde_extranjero", "bajas_al_extranjero") if fuente == "ine_evr" else ("inmigracion_exterior", "emigracion_exterior")
        s = pd.read_csv(RAW11 / f"{fuente}/saldos_internos_municipio.csv.gz", dtype={"cod_municipio": str})
        emp.append({"fuente": fuente, "anio": 2021, "inmigracion_exterior": pd.to_numeric(e[cin]).sum(),
                    "emigracion_exterior": pd.to_numeric(e[cout]).sum(), "movimientos_interiores": int(s[s.anio == 2021].altas.sum())})
    pc_ = P[P.nac == "TOTAL"].groupby(["anio", "fuente_poblacion"]).poblacion.sum().unstack()
    for a in (2021, 2022):
        if a in pc_.index:
            emp.append({"fuente": "poblacion_1_enero", "anio": a, "padron": pc_.loc[a].get("padron"), "censo_anual": pc_.loc[a].get("censo_anual"),
                        "dif_pct": 100 * (pc_.loc[a].get("censo_anual") / pc_.loc[a].get("padron") - 1)})
    pd.DataFrame(emp).to_csv(OUT / "empalme_2021.csv", index=False)
    nac = per[(per.nivel == "nacional") & (per.nac == "TOTAL")].set_index("periodo")
    res = {"rama": "V12-B1", "pregunta": "¿De dónde viene el crecimiento de la población?", "capa": "C4", "metodo": "identidad contable",
           "datos": "MNP, EVR, EMCR, padrón continuo, censo anual (INE)", "N": int(len(anual)),
           "nacional_por_periodo": nac[["crecimiento", "vegetativo", "saldo_exterior", "saldo_interior", "residuo"]].round(0).to_dict(orient="index"),
           "empalme_2021": emp,
           "notas": ["Municipios < 10.000 hab. solo en provincia/CCAA/España", "residuo por nacionalidad incluye adquisiciones de nacionalidad",
                     "EVR sin bajas al extranjero antes de 2002 (no se usa antes de 2002)"]}
    res["valencia"] = valencia()
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    hechos = [{"id": f"b1_nacional_{p}_{c}", "valor": float(nac.loc[p, c]), "unidad": "personas", "periodo": p, "territorio": "España",
               "capa": "C4", "fuente": "INE: padrón/censo anual (población), MNP, EVR/EMCR",
               "nota": "identidad contable; el residuo recoge revisiones del padrón y bajas por caducidad no registradas como flujo"}
              for p in nac.index for c in ("crecimiento", "vegetativo", "saldo_exterior", "residuo")]
    hechos += [{"id": f"b1_valencia_{k}", "valor": v, "unidad": "personas", "periodo": "2021-2025", "territorio": "València",
                "capa": "C4", "fuente": "INE censo anual por sección"} for k, v in res["valencia"].items() if k.startswith("var_")]
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res["nacional_por_periodo"], ensure_ascii=False, indent=1, default=float))
    print(pd.DataFrame(emp))
    return 0


if __name__ == "__main__":
    sys.exit(main())

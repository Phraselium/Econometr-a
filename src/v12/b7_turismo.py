"""V12-B7 · Turismo y presión residencial (descriptivo, C4/C1; sin modelos ni lenguaje causal).

Ámbito: Comunitat Valenciana (municipios), València (distritos y barrios) y, como contraste, Cataluña y Barcelona.
Fuentes (todas en la base o en data/raw, cruce por código INE):
- INE, viviendas turísticas (experimental: anuncios en plataformas, semestral 2021-02 → último), por sección; se suman
  a municipio, distrito y barrio (sección → barrio con la correspondencia por área de B1);
- GVA, registro de viviendas turísticas: dos cortes observados (2025-01-26 y 2026-10-14) y la serie reconstruida
  2015-2025 a partir de las fechas de alta de las viviendas que siguen inscritas (cota inferior del stock pasado:
  no incluye las bajas; marcada «reconstruido», solo robustez);
- INE, medición del turismo con teléfonos móviles: turistas (internos + receptores) por municipio de destino;
- Idescat, HUT por municipio (2015-2025) y Ajuntament de Barcelona, HUT por barrio y año del expediente;
- contraste: población (censo anual), alquiler (SERPAVI; distrito en València), titularidad (B5), saldo B1.
Dos fuentes de stock (INE y registro): si difieren < 25 % en un municipio se marca «coinciden» (C1 del orden de
magnitud); si no, se reportan ambas (miden cosas distintas: anuncios frente a inscripciones).
Asociaciones (Spearman, IC bootstrap, Holm, Registry) entre municipios de la Comunitat Valenciana: descriptivas.
Salidas: output/v12/b7/.
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
OUT = RAIZ / "output/v12/b7"
SEED = 20261010
CV = ("03", "12", "46")
UMBRAL = 0.25


def hechos(filtros: list) -> pd.DataFrame:
    import pyarrow.parquet as pq
    return pq.read_table(RAIZ / "data/base/publica/hechos.parquet", columns=["territorio_codigo", "nivel", "periodo", "variable", "desagregacion", "valor"],
                         filters=filtros).to_pandas()


def vut_ine() -> pd.DataFrame:
    """Viviendas turísticas INE por sección → parque implícito (vut / %) para poder agregar el porcentaje."""
    v = hechos([("nivel", "=", "seccion"), ("variable", "in", ["ine_vut_vivienda_turistica", "ine_vut_porcentaje_vivienda_turistica", "ine_vut_plazas"])])
    w = v.pivot_table(index=["territorio_codigo", "periodo"], columns="variable", values="valor").reset_index()
    w["parque"] = (w.ine_vut_vivienda_turistica / (w.ine_vut_porcentaje_vivienda_turistica / 100)).replace([np.inf, -np.inf], np.nan)
    return w.rename(columns={"territorio_codigo": "cod_seccion", "ine_vut_vivienda_turistica": "vut", "ine_vut_plazas": "plazas"})


def agregar(w: pd.DataFrame, clave: pd.Series, peso: pd.Series | None = None) -> pd.DataFrame:
    x = w.assign(k=clave.values, p=1.0 if peso is None else peso.values)
    for c in ("vut", "plazas", "parque"):
        x[c] = x[c] * x.p
    g = x.groupby(["k", "periodo"], as_index=False)[["vut", "plazas", "parque"]].sum(min_count=1)
    g["pct_vut"] = 100 * g.vut / g.parque
    return g


def municipios_cv(w: pd.DataFrame) -> pd.DataFrame:
    m = agregar(w, w.cod_seccion.str[:5])
    m = m[m.k.str[:2].isin(CV)].rename(columns={"k": "cod_municipio"})
    r = hechos([("nivel", "=", "municipio"), ("variable", "in", ["vut_registro_gva", "vut_registro_gva_reconstruido"])])
    reg = r[r.variable == "vut_registro_gva"].pivot_table(index="territorio_codigo", columns="periodo", values="valor")
    rec = r[r.variable == "vut_registro_gva_reconstruido"].pivot_table(index="territorio_codigo", columns="periodo", values="valor")
    # INE más cercano a cada corte del registro: 2024-11 ↔ 2025-01-26; 2026-05 ↔ 2026-10-14
    ult = m.periodo.max()
    base = m[m.periodo.isin(["2024-11", ult])].pivot_table(index="cod_municipio", columns="periodo", values=["vut", "pct_vut", "parque"])
    d = pd.DataFrame({"vut_ine_2024_11": base[("vut", "2024-11")], f"vut_ine_{ult}": base[("vut", ult)],
                      f"pct_vut_ine_{ult}": base[("pct_vut", ult)], "parque_ine": base[("parque", ult)]})
    d = d.join(reg.rename(columns=lambda c: f"registro_gva_{c}"), how="outer")
    d["ratio_registro_ine_2025"] = d["registro_gva_2025-01-26"] / d.vut_ine_2024_11
    d["ratio_registro_ine_ultimo"] = d["registro_gva_2026-10-14"] / d[f"vut_ine_{ult}"]
    d["fuentes_coinciden"] = (d.ratio_registro_ine_ultimo - 1).abs() < UMBRAL
    for a in ("2015-01", "2019-01", "2025-01"):
        if a in rec:
            d[f"registro_reconstruido_{a}"] = rec[a]
    return d.rename_axis("cod_municipio").reset_index()


def turistas() -> pd.DataFrame:
    t = hechos([("nivel", "=", "municipio"), ("variable", "in", ["ine_tmov_interno_turistas", "ine_tmov_receptor_turistas"])])
    t["anio"] = t.periodo.str[:4]
    meses = t.groupby(["territorio_codigo", "variable", "anio"]).periodo.nunique()
    a = t.groupby(["territorio_codigo", "variable", "anio"]).valor.sum().to_frame().assign(meses=meses).reset_index()
    a = a[a.meses == 12].pivot_table(index=["territorio_codigo", "anio"], columns="variable", values="valor").reset_index()
    a["turistas"] = a[["ine_tmov_interno_turistas", "ine_tmov_receptor_turistas"]].sum(axis=1, min_count=1)
    return a.rename(columns={"territorio_codigo": "cod_municipio"})


def contraste_cv(d: pd.DataFrame, tu: pd.DataFrame, reg: Registry) -> tuple[pd.DataFrame, pd.DataFrame]:
    from statsmodels.stats.multitest import multipletests
    pob = hechos([("nivel", "=", "municipio"), ("variable", "=", "pob_censo_anual"), ("desagregacion", "=", "nacionalidad=Total")])
    pob = pob.pivot_table(index="territorio_codigo", columns="periodo", values="valor")
    s = hechos([("nivel", "=", "municipio"), ("variable", "=", "serpavi_alquiler_m2_mediana"), ("desagregacion", "=", "tipologia=VC")])
    s = s.pivot_table(index="territorio_codigo", columns="periodo", values="valor")
    b5 = pd.read_csv(RAIZ / "output/v12/b5/titularidad_cuotas.csv", dtype={"cod_territorio": str})
    b5 = b5[(b5.nivel == "municipio") & (b5.anio == 2025)].set_index("cod_territorio")
    ult = [c for c in d.columns if c.startswith("pct_vut_ine_")][0]
    t24 = tu[tu.anio == "2024"].set_index("cod_municipio").turistas
    x = d.set_index("cod_municipio")[[ult, "registro_gva_2026-10-14"]].join(pob[["2021", "2025"]])
    x["vut_registro_por_1000_hab"] = 1000 * x["registro_gva_2026-10-14"] / x["2025"]
    x["turistas_2024_por_hab"] = t24.reindex(x.index) / x["2025"]
    x["crec_pob_2021_2025_pct"] = 100 * (x["2025"] / x["2021"] - 1)
    x["alquiler_m2_2024"] = s.get("2024")
    x["alquiler_var_2019_2024"] = 100 * (s.get("2024") / s.get("2019") - 1)
    x["pct_PJ_2025"], x["pct_mas10_2025"] = b5.pct_PJ, b5.pct_mas10
    x = x[x["2025"] >= 10000]
    rng = np.random.default_rng(SEED)
    filas = []
    for tur in (ult, "vut_registro_por_1000_hab", "turistas_2024_por_hab"):
        for v in ("crec_pob_2021_2025_pct", "alquiler_m2_2024", "alquiler_var_2019_2024", "pct_PJ_2025", "pct_mas10_2025"):
            z = x[[tur, v]].dropna()
            if len(z) < 10:
                continue
            a, b = z[tur].to_numpy(), z[v].to_numpy()
            r, p = stats.spearmanr(a, b)
            bs = [stats.spearmanr(a[i], b[i])[0] for i in (rng.integers(0, len(a), len(a)) for _ in range(1000))]
            lo, hi = np.nanpercentile(bs, [2.5, 97.5])
            reg.log("V12-B7", f"b7_{tur}_{v}", f"spearman({tur}, {v})", 2021, 2025, len(z), np.nan, np.nan, np.nan, coef_interes=r, p_interes=p,
                    notas="descriptivo C4; municipios CV ≥ 10.000 hab.")
            filas.append({"turismo": tur, "variable": v, "N": len(z), "spearman": round(float(r), 3), "ic95_inf": round(float(lo), 3),
                          "ic95_sup": round(float(hi), 3), "p": float(p)})
    R = pd.DataFrame(filas)
    R["p_holm"] = multipletests(R.p, method="holm")[1]
    return x.rename_axis("cod_municipio").reset_index(), R


def valencia(w: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    v = w[w.cod_seccion.str.startswith("46250")]
    dist = agregar(v, v.cod_seccion.str[:7]).rename(columns={"k": "cod_distrito"})
    k = pd.read_csv(RAIZ / "data/base/geo/correspondencia_seccion_barrio_valencia.csv", dtype={"cod_seccion": str, "cod_barrio": str})
    unico = k[k.seccion_en_un_barrio].sort_values("peso_area").groupby("cod_seccion").tail(1).assign(peso=1.0)
    rep = k[~k.seccion_en_un_barrio].assign(peso=lambda d: d.peso_area / d.groupby("cod_seccion").peso_area.transform("sum"))
    c = pd.concat([unico, rep])[["cod_seccion", "cod_barrio", "peso"]]
    vb = v.merge(c, on="cod_seccion", how="inner")
    bar = agregar(vb, vb.cod_barrio, vb.peso).rename(columns={"k": "cod_barrio"})
    nom = pd.read_parquet(RAIZ / "data/base/geo/barrios_valencia.parquet", columns=["cod_barrio", "nombre"])
    bar = bar.merge(nom, how="left", on="cod_barrio")
    # distrito: población (B1), alquiler SERPAVI e IPVA
    b1 = pd.read_csv(RAIZ / "output/v12/b1/valencia_distrito_variacion_2021_2025.csv", dtype={"cod_distrito": str}).set_index("cod_distrito")
    s = hechos([("nivel", "=", "distrito"), ("variable", "=", "serpavi_alquiler_m2_mediana"), ("desagregacion", "=", "tipologia=VC")])
    s = s[s.territorio_codigo.str.startswith("46250")].pivot_table(index="territorio_codigo", columns="periodo", values="valor")
    ult = dist.periodo.max()
    dd = dist[dist.periodo.isin(["2021-08", ult])].pivot_table(index="cod_distrito", columns="periodo", values=["vut", "pct_vut"])
    r = pd.DataFrame({"vut_2021_08": dd[("vut", "2021-08")], f"vut_{ult}": dd[("vut", ult)], f"pct_vut_{ult}": dd[("pct_vut", ult)]})
    r = r.join(b1[["Total_2021", "Total_2025", "var_Total_2021_2025", "cuota_EXT_2025"]])
    if "2024" in s and "2019" in s:
        r["alquiler_m2_2024"], r["alquiler_var_2019_2024"] = s["2024"], 100 * (s["2024"] / s["2019"] - 1)
    return r.rename_axis("cod_distrito").reset_index(), bar


def cataluna(w: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    h = hechos([("nivel", "=", "municipio"), ("variable", "=", "idescat_hut_n")]).pivot_table(index="territorio_codigo", columns="periodo", values="valor")
    m = agregar(w, w.cod_seccion.str[:5])
    m = m[m.k.str[:2].isin(["08", "17", "25", "43"]) & m.periodo.str.startswith("2025")].groupby("k").vut.mean()
    c = pd.DataFrame({"hut_idescat_2025": h.get("2025"), "vut_ine_2025_media": m}).dropna(how="all")
    c["ratio_idescat_ine"] = c.hut_idescat_2025 / c.vut_ine_2025_media
    c["fuentes_coinciden"] = (c.ratio_idescat_ine - 1).abs() < UMBRAL
    b = pd.read_csv(RAIZ / "data/raw/v9/bcn_hut/bcn_hut_barrio_anio_expediente.csv.gz", dtype={"cod_municipio": str, "codi_barri": str})
    b = b.groupby("anio_expediente", as_index=False)[["n_hut", "places"]].sum()
    return c.rename_axis("cod_municipio").reset_index(), b


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    reg = Registry(OUT / "registry.csv")
    w = vut_ine()
    d = municipios_cv(w)
    d.to_csv(OUT / "cv_municipios_vut_ine_registro.csv", index=False, float_format="%.10g")
    tu = turistas()
    tu[tu.cod_municipio.str[:2].isin(CV)].to_csv(OUT / "cv_turistas_moviles_anual.csv", index=False, float_format="%.10g")
    x, R = contraste_cv(d, tu, reg)
    x.to_csv(OUT / "cv_contraste_municipios.csv", index=False, float_format="%.10g")
    R.to_csv(OUT / "cv_asociaciones.csv", index=False)
    reg.flush()
    dist, bar = valencia(w)
    dist.to_csv(OUT / "valencia_distritos.csv", index=False, float_format="%.10g")
    bar.to_csv(OUT / "valencia_barrios_vut_serie.csv", index=False, float_format="%.10g")
    cat, bcn = cataluna(w)
    cat.to_csv(OUT / "cataluna_hut_idescat_frente_ine.csv", index=False, float_format="%.10g")
    bcn.to_csv(OUT / "barcelona_hut_por_anio_expediente.csv", index=False)
    ultp = w.periodo.max()
    cvt = agregar(w[w.cod_seccion.str[:2].isin(CV)], pd.Series("CV", index=w[w.cod_seccion.str[:2].isin(CV)].index))
    vlc = agregar(w[w.cod_seccion.str.startswith("46250")], pd.Series("València", index=w[w.cod_seccion.str.startswith("46250")].index))
    serie = pd.concat([cvt, vlc]).rename(columns={"k": "ambito"})
    serie.to_csv(OUT / "serie_vut_cv_valencia.csv", index=False, float_format="%.10g")
    g = lambda s, p, c: float(s[(s.periodo == p)][c].iloc[0])  # noqa: E731
    res = {"rama": "V12-B7", "pregunta": "¿Dónde se concentra la vivienda turística y qué la acompaña?", "capa": "C4",
           "metodo": "descriptivo; dos fuentes de stock; asociación de rangos", "datos": "INE VUT, registro GVA, INE móviles, Idescat, Ajuntament de Barcelona",
           "N": int(len(d)),
           "cv": {"vut_ine_2021_08": g(cvt, "2021-08", "vut"), f"vut_ine_{ultp}": g(cvt, ultp, "vut"), f"pct_{ultp}": round(g(cvt, ultp, "pct_vut"), 2),
                  "registro_gva_2026_10_14": float(d["registro_gva_2026-10-14"].sum()),
                  "municipios_fuentes_coinciden": int(d.fuentes_coinciden.sum()), "municipios_con_ambas": int(d.ratio_registro_ine_ultimo.notna().sum())},
           "valencia": {"vut_ine_2021_08": g(vlc, "2021-08", "vut"), f"vut_ine_{ultp}": g(vlc, ultp, "vut"), f"pct_{ultp}": round(g(vlc, ultp, "pct_vut"), 2),
                        "registro_gva_2026_10_14": float(d.loc[d.cod_municipio == "46250", "registro_gva_2026-10-14"].iloc[0])},
           "cataluna_municipios_fuentes_coinciden": int(cat.fuentes_coinciden.sum()), "cataluna_municipios_con_ambas": int(cat.ratio_idescat_ine.notna().sum()),
           "asociaciones": R[["turismo", "variable", "N", "spearman", "ic95_inf", "ic95_sup", "p_holm"]].to_dict(orient="records"),
           "notas": ["INE VUT = anuncios en plataformas (experimental); registro GVA = inscripciones", "serie reconstruida del registro: cota inferior, solo robustez",
                     "asociaciones descriptivas entre municipios"]}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "asociaciones"}, ensure_ascii=False, indent=1))
    print(R.to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())

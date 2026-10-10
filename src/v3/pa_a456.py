"""A4 (esfuerzo de acceso), A5 (tenencia por edad) y A6 (precio/alquiler y coste de uso)."""
from __future__ import annotations

import numpy as np
import pandas as pd

import pa_data as pdat

M2 = 80.0
PLAZO = 25
LTV = 0.8
ANIO_A4 = 2023


def cuota(precio: float, tipo_pct: float) -> float:
    """Cuota mensual de un préstamo del 80 % del precio, a 25 años, sistema francés."""
    i = tipo_pct / 100 / 12
    n = PLAZO * 12
    p = LTV * precio
    return p * i / (1 - (1 + i) ** -n) if i > 0 else p / n


def _renta_agregada(nivel: int, anio: int) -> pd.DataFrame:
    """Renta neta media por hogar (ADRH) agregada a municipio (5) o provincia (2), ponderada por hogares del Censo 2021."""
    r = pdat.adrh_hogar()
    r = r[r.anio == anio].set_index("codigo").renta_hogar
    sec = pdat.censo2021_secciones()
    x = pd.concat([r, sec.hogares], axis=1, join="inner").dropna()
    x = x[x.hogares > 0]
    x["cod"] = x.index.str[:nivel]
    g = x.groupby("cod").apply(lambda t: pd.Series({"renta_hogar": np.average(t.renta_hogar, weights=t.hogares),
                                                    "hogares": t.hogares.sum(), "n_secciones": len(t)}), include_groups=False)
    return g


def a4(reg) -> dict[str, pd.DataFrame]:
    pp = pdat.panel("panel_prov_a")
    nq = pdat.nacional_q()
    mp = pdat.mapa_prov(pp)
    reg_p = pdat.registradores_prov()
    reg_p = reg_p[reg_p.periodo == ANIO_A4].set_index("clave").reg_pm2
    tipo = float(nq.loc[[q for q in nq.index if q.startswith(str(ANIO_A4))], "tipo_hip"].mean())
    ren = _renta_agregada(2, ANIO_A4)
    inc = pdat.incasol_renta(ANIO_A4)
    inc["cod_prov"] = inc.index.str[:2]
    incp = inc.groupby("cod_prov").apply(lambda t: np.average(t.renta_mes, weights=t.n_contratos), include_groups=False)
    p = pp[pp.anio == ANIO_A4].set_index("cod_prov")
    filas = []
    for cod, r in p.iterrows():
        k = next((kk for kk, vv in mp.items() if vv == cod), None)
        renta = ren.renta_hogar.get(cod, np.nan)
        pr_t = r.p_tasado
        pr_r = reg_p.get(k, np.nan)
        alq_s = r.serpavi_mediana_vc * M2 if pd.notna(r.serpavi_mediana_vc) else np.nan
        alq_i = incp.get(cod, np.nan)
        fila = {"cod_prov": cod, "provincia": r.provincia, "anio": ANIO_A4, "renta_hogar_adrh": renta,
                "precio_m2_tasado": pr_t, "precio_m2_registradores": pr_r,
                "alquiler_mes_serpavi": alq_s, "alquiler_mes_incasol": alq_i, "tipo_hipotecario_pct": tipo}
        for nom, pr in (("tasado", pr_t), ("registradores", pr_r)):
            fila[f"precio_{nom}_{int(M2)}m2"] = pr * M2
            fila[f"precio_renta_{nom}"] = pr * M2 / renta if pd.notna(pr) else np.nan
            c = cuota(pr * M2, tipo) if pd.notna(pr) else np.nan
            fila[f"cuota_mes_{nom}"] = c
            fila[f"cuota_pct_renta_{nom}"] = 100 * c / (renta / 12) if pd.notna(c) else np.nan
        fila["alquiler_pct_renta_serpavi"] = 100 * alq_s * 12 / renta if pd.notna(alq_s) else np.nan
        fila["alquiler_pct_renta_incasol"] = 100 * alq_i * 12 / renta if pd.notna(alq_i) else np.nan
        filas.append(fila)
        reg.log("A4_provincia", f"A4_{cod}_{ANIO_A4}", "precio·80m²/renta; cuota 25a LTV80; alquiler·12/renta", ANIO_A4, ANIO_A4, 1,
                np.nan, np.nan, np.nan, np.nan, fila["precio_renta_tasado"], np.nan, r.provincia)
    prov = pd.DataFrame(filas)
    # nacional por año: renta ADRH (todas las secciones) frente a renta de la contabilidad nacional por hogar
    nac = []
    sec = pdat.censo2021_secciones()
    ad = pdat.adrh_hogar()
    for y in sorted(ad.anio.unique()):
        y = int(y)
        a = ad[ad.anio == y].set_index("codigo").renta_hogar
        x = pd.concat([a, sec.hogares], axis=1, join="inner").dropna()
        renta_adrh = np.average(x.renta_hogar, weights=x.hogares)
        qs = [q for q in nq.index if q.startswith(str(y))]
        if len(qs) < 4:
            continue
        rhog = nq.loc[qs, "renta_hog"].sum() * 1e6
        hog = nq.loc[qs, "hogares_epa"].mean() * 1000
        precio = nq.loc[qs, "p_tasado"].mean()
        t = nq.loc[qs, "tipo_hip"].mean()
        for nom, renta in (("ADRH (renta neta media por hogar)", renta_adrh), ("Cuentas nacionales (renta disponible hogares/hogares EPA)", rhog / hog)):
            c = cuota(precio * M2, t)
            nac.append({"anio": y, "renta_fuente": nom, "renta_hogar_anual": renta, "precio_m2_tasado": precio,
                        "precio_renta": precio * M2 / renta, "tipo_hipotecario_pct": t, "cuota_mes": c,
                        "cuota_pct_renta": 100 * c / (renta / 12)})
            reg.log("A4_nacional", f"A4nac_{y}_{nom[:6]}", "esfuerzo nacional", y, y, 1, np.nan, np.nan, np.nan, np.nan,
                    precio * M2 / renta, np.nan, nom)
    # municipal: municipios con valor tasado
    pm = pdat.panel("panel_muni_a")
    pm["cod"] = pm.cod_muni.astype(int).astype(str).str.zfill(5)
    pm = pm[pm.anio == ANIO_A4].drop_duplicates("cod").set_index("cod")
    rm = _renta_agregada(5, ANIO_A4)
    mu = pm[["municipio", "p_tasado", "serpavi_mediana_vc"]].join(rm, how="inner").dropna(subset=["p_tasado"])
    mu["precio_renta_tasado"] = mu.p_tasado * M2 / mu.renta_hogar
    mu["cuota_pct_renta"] = [100 * cuota(p_ * M2, tipo) / (r_ / 12) for p_, r_ in zip(mu.p_tasado, mu.renta_hogar, strict=True)]
    mu["alquiler_pct_renta_serpavi"] = 100 * mu.serpavi_mediana_vc * M2 * 12 / mu.renta_hogar
    return {"A4_provincias": prov, "A4_nacional": pd.DataFrame(nac), "A4_municipios": mu.reset_index().rename(columns={"index": "cod"})}


def a5(reg) -> pd.DataFrame:
    f = pd.read_csv(pdat.V3 / "eff_tenencia_edad_v3.csv")
    f = f[f.serie.str.contains("eff_pct_hogares_vivienda_principal")].copy()
    f["edad"] = f.serie.str.extract(r"edad=([^|]+)")[0]
    eff = f.groupby(["periodo", "edad"]).valor.agg(["min", "max"]).reset_index()
    filas = []
    for r in eff.itertuples():
        filas.append({"fuente": "EFF (tablas del BdE; mín-máx entre ediciones)", "anio": int(r.periodo), "edad": r.edad,
                      "categoria": "propietario de vivienda principal", "pct_min": r.min, "pct_max": r.max})
    v = pd.read_csv(pdat.V3 / "ine_ecv_tenencia_edad_v3.csv")
    v = v[v.serie.str.contains("sexo=Ambos sexos")].copy()
    v["cat"] = v.serie.str.replace("ecv_pct_hogares_tenencia|", "", regex=False).str.split("|").str[0]
    v["edad"] = v.serie.str.extract(r"edad_persona_referencia=([^|]+)")[0]
    pv = v.pivot_table(index=["periodo", "edad"], columns="cat", values="valor").reset_index()
    for r in pv.itertuples():
        d = r._asdict()
        prop = d["Propiedad"]
        for cat, val in (("propietario", prop), ("propiedad con hipoteca", d["_6"] if False else r[pv.columns.get_loc("Propiedad con hipoteca") + 1]),
                         ("alquiler a precio de mercado", r[pv.columns.get_loc("Alquiler a precio de mercado") + 1]),
                         ("alquiler inferior al mercado", r[pv.columns.get_loc("Alquiler inferior al precio de mercado") + 1]),
                         ("cesión", r[pv.columns.get_loc("Cesión") + 1])):
            filas.append({"fuente": "INE ECV (tabla 9994)", "anio": int(r.periodo), "edad": r.edad, "categoria": cat,
                          "pct_min": val, "pct_max": val})
    e = pd.read_csv(pdat.V3 / "eurostat_emancipacion_tenencia_v3.csv")
    e = e[e.fuente.str.contains("lvho02") & (e.codigo == "ES")]
    e = e[e.serie.str.contains(r"_A1_(?:LT65|GE65)_(?:OWN|RENT|TOTAL)$")].copy()
    e["grupo"] = e.serie.str.extract(r"_A1_(LT65|GE65)_")[0]
    e["cat"] = e.serie.str.extract(r"_(OWN|RENT|TOTAL)$")[0]
    pe = e.pivot_table(index=["periodo", "grupo"], columns="cat", values="valor").reset_index()
    for r in pe.itertuples():
        for cat, num in (("propietario", r.OWN), ("alquiler", r.RENT)):
            v_ = 100 * num / r.TOTAL
            filas.append({"fuente": "Eurostat ilc_lvho02 (adulto solo, % del grupo)", "anio": int(r.periodo),
                          "edad": "<65" if r.grupo == "LT65" else "65+", "categoria": cat, "pct_min": v_, "pct_max": v_})
    # Censo 2021: total (todas las edades), a partir de los indicadores por sección
    sec = pd.read_csv(pdat.V3 / "ine_v3_censo2021_seccion_indicadores.csv.gz", dtype={"codigo": str}, usecols=["codigo", "serie", "valor"])
    s = sec[sec.serie.isin(["t19_1", "t20_1", "t20_2", "t20_3"])].pivot(index="codigo", columns="serie", values="valor").dropna()
    tot = s.sum()
    filas.append({"fuente": "Censo 2021 (secciones; total, sin edad)", "anio": 2021, "edad": "total",
                  "categoria": "propietario", "pct_min": 100 * tot.t20_1 / tot.t19_1, "pct_max": 100 * tot.t20_1 / tot.t19_1})
    filas.append({"fuente": "Censo 2021 (secciones; total, sin edad)", "anio": 2021, "edad": "total",
                  "categoria": "alquiler", "pct_min": 100 * tot.t20_2 / tot.t19_1, "pct_max": 100 * tot.t20_2 / tot.t19_1})
    out = pd.DataFrame(filas)
    for r in out[out.anio.isin([2008, 2014, 2020, 2022])].itertuples():
        reg.log("A5", f"A5_{r.fuente[:6]}_{r.anio}_{r.edad}_{r.categoria[:8]}", "porcentaje de hogares por tenencia y edad",
                r.anio, r.anio, 1, np.nan, np.nan, np.nan, np.nan, r.pct_min, np.nan, r.fuente)
    return out


def a6(reg) -> dict[str, pd.DataFrame]:
    nq = pdat.nacional_q()
    nq = nq.copy()
    nq["anio"] = [int(i[:4]) for i in nq.index]
    ann = nq.groupby("anio").agg(ipv=("ipv", "mean"), ipc_alq=("ipc_alquiler", "mean"), p_tasado=("p_tasado", "mean"),
                                 tipo_hip=("tipo_hip", "mean"), infl=("inflacion_deflactor", "mean"),
                                 ratio_idx=("ratio_precio_alquiler_idx", "mean"))
    cnt = nq.groupby("anio").tipo_hip.count()
    ann = ann[cnt >= 4]
    ecb = pd.read_csv(pdat.RAW / "ecb_tipo_hipotecario_es.csv")
    ecb["anio"] = ecb.periodo.str[:4].astype(int)
    ann["tipo_hip_bce"] = ecb.groupby("anio").valor.mean()
    ann["ratio_ipv_ipc_base2015"] = 100 * (ann.ipv / ann.ipc_alq) / (ann.loc[2015, "ipv"] / ann.loc[2015, "ipc_alq"])
    sp = nq.groupby("anio").serpavi_esp_constante.mean()
    ann["serpavi_eur_m2_mes"] = sp
    ann["ratio_niveles_tasado_serpavi"] = ann.p_tasado / (ann.serpavi_eur_m2_mes * 12)
    r15 = ann.loc[2015, "ratio_niveles_tasado_serpavi"] if 2015 in ann.index and pd.notna(ann.loc[2015, "ratio_niveles_tasado_serpavi"]) else np.nan
    ann["ratio_niveles_base2015"] = 100 * ann.ratio_niveles_tasado_serpavi / r15
    # Poterba: uc = i + tau_p + delta - g   (% anual del precio); sin deducción fiscal
    tau = 0.5
    ipv_g4 = 100 * (np.log(ann.ipv) - np.log(ann.ipv.shift(4))) / 4
    filas = []
    for y, r in ann.iterrows():
        if pd.isna(r.tipo_hip):
            continue
        for fuente_i, i in (("v2 (agregado de tipo hipotecario)", r.tipo_hip), ("BCE (tipo de nuevos préstamos)", r.tipo_hip_bce)):
            if pd.isna(i):
                continue
            for dep in (1.0, 2.0, 3.0):
                for gn, g in (("g=0", 0.0), ("g=inflación", r.infl), ("g=IPV media 4 años", ipv_g4.get(y, np.nan))):
                    if pd.isna(g):
                        continue
                    uc = i + tau + dep - g
                    filas.append({"anio": y, "tipo_fuente": fuente_i, "tipo_hip_pct": i, "depreciacion_pct": dep, "ganancia_esperada": gn,
                                  "ganancia_pct": g, "coste_uso_pct": uc, "coste_uso_mes_80m2": uc / 100 * r.p_tasado * M2 / 12,
                                  "alquiler_mes_serpavi_80m2": r.serpavi_eur_m2_mes * M2})
    uc = pd.DataFrame(filas)
    uc["coste_uso_sobre_alquiler"] = uc.coste_uso_mes_80m2 / uc.alquiler_mes_serpavi_80m2
    for y, g in uc.groupby("anio"):
        reg.log("A6", f"A6_uc_{y}", "uc = i + τ + δ − g", y, y, len(g), np.nan, np.nan, np.nan, np.nan, g.coste_uso_pct.median(), np.nan,
                f"rango {g.coste_uso_pct.min():.2f} a {g.coste_uso_pct.max():.2f}")
    # ratio por provincia (niveles), último año con dato
    pp = pdat.panel("panel_prov_a")
    pr = pp[pp.anio == 2023][["cod_prov", "provincia", "p_tasado", "serpavi_mediana_vc", "precio_alquiler_ratio_nivel"]].copy()
    pr["ratio_niveles_tasado_serpavi"] = pr.p_tasado / (pr.serpavi_mediana_vc * 12)
    return {"A6_ratio_nacional": ann.reset_index(), "A6_coste_uso": uc, "A6_ratio_provincias_2023": pr}

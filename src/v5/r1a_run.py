"""R1a · Cierre de la rama BT de v2 (v5): no residentes por provincia (BK-002), VUT INE frente a GVA (BK-052)
y alquiler de temporada/por habitaciones (BK-014). Determinista, sin red, un solo hilo, SEED=20261010.

Entradas (solo lectura): data/raw/mivau_transacciones_residencia.csv, mivau_valor_tasado_nacional_ccaa_prov.csv,
ine_v2_padron_prov_edad_nac.csv, ine_v2_cre.csv, pdf/notariado_cgn_extranjeros_semestral.csv,
gva_vut_municipio.csv.gz, ine_v2_vut.csv, v3/ine_v3_vut_seccion.csv.gz, v3/airbnb_insideairbnb_agregados_v3.csv.gz.
Salidas: output/v5/R1A/ (tablas, registro.csv, resultado.json, hechos.json, fichas_verificador.json).
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
from econ_utils import Registry, holm  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
RAW = RAIZ / "data" / "raw"
OUT = RAIZ / "output" / "v5" / "R1A"
TAB = OUT / "tablas"
TAB.mkdir(parents=True, exist_ok=True)
FECHA_DATO = "2026-08 (descarga 2026-10-09/10; MIVAU hasta 2026T2)"


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return "".join(ch for ch in s if ch.isalnum())


# Unidades: 43 provincias de MIVAU + 7 comunidades uniprovinciales (MIVAU las da solo como CCAA)
UNI = {"Asturias": "Asturias (Principado de)", "Balears, Illes": "Balears (Illes)", "Cantabria": "Cantabria",
       "Madrid": "Madrid (Comunidad de)", "Murcia": "Murcia (Región de)", "Navarra": "Navarra (Comunidad Foral de)",
       "Rioja, La": "Rioja (La)"}
COSTA = {"Alicante/Alacant", "Almería", "Cádiz", "Castellón/Castelló", "Girona", "Granada", "Huelva", "Málaga",
         "Tarragona", "Valencia/València", "Barcelona", "Pontevedra", "Coruña, A", "Murcia", "Asturias", "Cantabria",
         "Bizkaia", "Gipuzkoa", "Balears, Illes", "Palmas, Las", "Santa Cruz de Tenerife"}
ISLAS = {"Balears, Illes", "Palmas, Las", "Santa Cruz de Tenerife"}
# Costa mediterránea y sur-atlántica con alta presencia residencial de extranjeros (sensibilidad)
COSTA_SOL = {"Alicante/Alacant", "Almería", "Cádiz", "Castellón/Castelló", "Girona", "Granada", "Huelva", "Málaga",
             "Tarragona", "Valencia/València", "Murcia", "Balears, Illes", "Palmas, Las", "Santa Cruz de Tenerife"}


def cargar_tx() -> pd.DataFrame:
    d = pd.read_csv(RAW / "mivau_transacciones_residencia.csv")
    d["anio"] = d.periodo.str[:4].astype(int)
    d["tipo"] = d.serie.str.extract(r"^(tx_residencia_(?:total|no_residentes_total|no_residentes_extranjeros|"
                                    r"residentes_extranjeros|residentes_total))_(?:ccaa|provincia|nacional)")[0]
    d = d[d.tipo.notna() & d.nivel.isin(["provincia", "ccaa", "nacional"])]
    g = d.groupby(["nivel", "territorio", "anio", "tipo"]).valor.agg(["sum", "count"]).reset_index()
    g = g[g["count"] == 4]  # años completos
    return g.pivot_table(index=["nivel", "territorio", "anio"], columns="tipo", values="sum").reset_index()


def cargar_precio() -> pd.DataFrame:
    v = pd.read_csv(RAW / "mivau_valor_tasado_nacional_ccaa_prov.csv")
    v["anio"] = v.periodo.str[:4].astype(int)
    # Navarra cambia de nombre en el Boletín (2015-2018 «Com. Foral de»): se unifican
    v["territorio"] = v.territorio.replace({"Navarra (Com. Foral de)": "Navarra (Comunidad Foral de)"})
    g = v[v.serie.str.startswith("valor_tasado_libre") & v.nivel.isin(["provincia", "ccaa"])]
    g = g.groupby(["nivel", "territorio", "anio"]).valor.agg(["mean", "count"]).reset_index()
    return g[g["count"] == 4].rename(columns={"mean": "p"})


def panel() -> pd.DataFrame:
    tx, pr = cargar_tx(), cargar_precio()
    pad = pd.read_csv(RAW / "ine_v2_padron_prov_edad_nac.csv")
    pad = pad[(pad.nivel == "provincia") & (pad.desglose == "nacionalidad=Total; edad=Todas")].copy()
    pad["anio"] = pad.periodo.str[:4].astype(int)
    cre = pd.read_csv(RAW / "ine_v2_cre.csv")
    cre = cre[cre.nivel == "provincia"].copy()
    cre["anio"] = cre.periodo.astype(int)
    pnorm = {norm(t): t for t in pad.territorio.unique()}
    cnorm = {norm(t): t for t in cre.territorio.unique()}
    filas = []
    provs_m = sorted(tx[tx.nivel == "provincia"].territorio.unique())
    unidades = [(p, "provincia", p) for p in provs_m] + [(k, "ccaa", v) for k, v in UNI.items()]

    def ine_name(n):
        k = norm(n)
        alias = {"alicantealacant": "alicantealacant", "araba alava": "arabaalava", "coruna(a)": "corunaa",
                 "palmas(las)": "palmaslas", "valenciavalencia": "valenciavalencia", "araba/alava": "arabaalava"}
        k = alias.get(k, k)
        return pnorm.get(k)

    for ine_n, nivel, mivau_n in unidades:
        # nombre INE de la unidad
        nm = ine_name(ine_n) or ine_name(mivau_n)
        if nm is None:
            nm = next((v for k, v in pnorm.items() if k.startswith(norm(ine_n.split(",")[0].split("/")[0])[:5])), None)
        if nm is None:
            continue
        filas.append((nm, ine_n, nivel, mivau_n))
    u = pd.DataFrame(filas, columns=["ine", "unidad", "nivel", "mivau"])
    out = []
    for _, r in u.iterrows():
        t = tx[(tx.nivel == r.nivel) & (tx.territorio == r.mivau)].set_index("anio")
        # precio: mismo nivel; los nombres de provincia de valor tasado difieren (p. ej. «Coruña (A)»)
        pp = pr[pr.nivel == r.nivel]
        cand = pp[pp.territorio.map(norm) == norm(r.mivau)]
        if cand.empty:
            cand = pp[pp.territorio.map(norm).str[:6] == norm(r.mivau)[:6]]
        p = cand.set_index("anio").p
        pa = pad[pad.territorio == r.ine].set_index("anio").valor
        cr = cre[cre.territorio == r.ine]
        cr = cr.set_index("anio").valor
        try:
            a0, a1 = 2015, 2025
            d = dict(unidad=r.unidad, nivel=r.nivel, ine=r.ine)
            for a in (2015, 2016, 2025):
                tot = t.loc[a, "tx_residencia_total"]
                d[f"tot{a}"] = tot
                d[f"nr{a}"] = t.loc[a, "tx_residencia_no_residentes_extranjeros"] / tot
                d[f"nrt{a}"] = t.loc[a, "tx_residencia_no_residentes_total"] / tot
                d[f"re{a}"] = t.loc[a, "tx_residencia_residentes_extranjeros"] / tot
            d["dlnp"] = np.log(p.loc[a1]) - np.log(p.loc[a0])
            d["lnp0"] = np.log(p.loc[a0])
            d["dlnpob"] = np.log(pa.loc[a1]) - np.log(pa.loc[a0])
            d["lnpib_pc0"] = np.log(cr.loc[a0] * 1000 / pa.loc[a0])
            d["lnpob0"] = np.log(pa.loc[a0])
            d["costa"] = int(r.unidad in COSTA)
            d["isla"] = int(r.unidad in ISLAS)
            d["costa_sol"] = int(r.unidad in COSTA_SOL)
            out.append(d)
        except (KeyError, ValueError, IndexError):
            continue
    return pd.DataFrame(out)


def tarea_bk002(reg: Registry) -> dict:
    d = panel()
    d.to_csv(TAB / "no_residentes_panel_provincias.csv", index=False)
    d["nr_ini"] = (d.nr2015 + d.nr2016) / 2  # peso inicial = media 2015-2016 (pre-ventana de la subida 2015-2025)
    d["nr_ini"] = d.nr_ini * 100
    d["nrt_ini"] = (d.nrt2015 + d.nrt2016) / 2 * 100
    d["re_ini"] = (d.re2015 + d.re2016) / 2 * 100
    d["d_nr"] = (d.nr2025 - d.nr2015) * 100
    # Evolución (pp)
    ev = d[["unidad", "nivel", "nr2015", "nr2025", "re2015", "re2025"]].copy()
    for c in ["nr2015", "nr2025", "re2015", "re2025"]:
        ev[c] = (ev[c] * 100).round(2)
    ev["cambio_nr_pp"] = (ev.nr2025 - ev.nr2015).round(2)
    ev.sort_values("nr2025", ascending=False).to_csv(TAB / "no_residentes_peso_2015_2025.csv", index=False)
    # Nacional (MIVAU)
    tx = cargar_tx()
    nac = tx[tx.nivel == "nacional"].set_index("anio")
    nac_nr = {a: nac.loc[a, "tx_residencia_no_residentes_extranjeros"] / nac.loc[a, "tx_residencia_total"] * 100
              for a in (2015, 2025)}
    nac_re = {a: nac.loc[a, "tx_residencia_residentes_extranjeros"] / nac.loc[a, "tx_residencia_total"] * 100
              for a in (2015, 2025)}
    # Notariado frente a MIVAU (CCAA, 2025): operaciones de compradores extranjeros (Notariado T2: vivienda libre;
    # MIVAU: residentes + no residentes extranjeros, todas las viviendas). Notariado no publica el total por CCAA.
    notar = pd.read_csv(RAW / "pdf" / "notariado_cgn_extranjeros_semestral.csv")
    nt = notar[(notar.tabla == "T2") & notar.periodo.str.startswith("2025")].groupby("territorio").valor.sum()
    ccaa_map = {"Andalucía": "Andalucía", "Aragón": "Aragón", "Asturias": "Asturias (Principado de)",
                "Islas Baleares": "Balears (Illes)", "Islas Canarias": "Canarias", "Cantabria": "Cantabria",
                "Castilla y León": "Castilla y León", "Castilla-La Mancha": "Castilla-La Mancha",
                "Cataluña": "Cataluña", "Comunidad Valenciana": "Comunitat Valenciana", "Extremadura": "Extremadura",
                "Galicia": "Galicia", "Comunidad de Madrid": "Madrid (Comunidad de)",
                "Región de Murcia": "Murcia (Región de)", "Navarra": "Navarra (Comunidad Foral de)",
                "País Vasco": "País Vasco", "La Rioja": "Rioja (La)"}
    filas = []
    for k, v in ccaa_map.items():
        r = tx[(tx.nivel == "ccaa") & (tx.territorio == v) & (tx.anio == 2025)]
        if k in nt.index and not r.empty:
            m = r.iloc[0]
            filas.append((v, float(nt[k]), float(m.tx_residencia_residentes_extranjeros
                                                 + m.tx_residencia_no_residentes_extranjeros)))
    cc = pd.DataFrame(filas, columns=["ccaa", "ops_extranjeros_notariado_libre", "ops_extranjeros_mivau"])
    cc["cociente_notariado_mivau"] = cc.ops_extranjeros_notariado_libre / cc.ops_extranjeros_mivau
    cc.round(3).to_csv(TAB / "extranjeros_notariado_vs_mivau_ccaa_2025.csv", index=False)
    corr_cc = float(cc[["ops_extranjeros_notariado_libre", "ops_extranjeros_mivau"]].corr(method="spearman").iloc[0, 1])
    dif_media = float(cc.cociente_notariado_mivau.mean())
    # Especificaciones
    esp = {
        "E1_bivariada": "dlnp ~ nr_ini",
        "E2_controles": "dlnp ~ nr_ini + lnpib_pc0 + dlnpob + costa + isla",
        "E3_conv_precio0": "dlnp ~ nr_ini + lnpib_pc0 + dlnpob + costa + isla + lnp0",
        "E4_residentes_extr": "dlnp ~ re_ini + lnpib_pc0 + dlnpob + costa + isla",
        "E5_nr_total": "dlnp ~ nrt_ini + lnpib_pc0 + dlnpob + costa + isla",
        "E6_costa_sol": "dlnp ~ nr_ini + lnpib_pc0 + dlnpob + costa_sol + isla",
        "E7_cambio_contemporaneo": "dlnp ~ d_nr + lnpib_pc0 + dlnpob + costa + isla",
    }
    res, pv, ests = {}, {}, {}
    for k, f in esp.items():
        m = smf.ols(f, data=d).fit(cov_type="HC3")
        var = f.split("~")[1].split("+")[0].strip()
        res[k] = m
        pv[k] = float(m.pvalues[var])
        ests[k] = (var, float(m.params[var]), [float(x) for x in m.conf_int().loc[var]])
        reg.log_res("R1A_BK002", k, f, m, interes=var, notas="HC3; N=%d unidades; coef en log-puntos por pp" % int(m.nobs))
    # Sensibilidades que cambian la muestra (E2 sin outliers de costa; sin islas)
    sub = d[(d.isla == 0)]
    f8 = "dlnp ~ nr_ini + lnpib_pc0 + dlnpob + costa"
    m = smf.ols(f8, data=sub).fit(cov_type="HC3")
    reg.log_res("R1A_BK002", "E8_sin_islas", f8, m, interes="nr_ini", notas="HC3; sin islas")
    pv["E8_sin_islas"] = float(m.pvalues["nr_ini"])
    ests["E8_sin_islas"] = ("nr_ini", float(m.params["nr_ini"]), [float(x) for x in m.conf_int().loc["nr_ini"]])
    # Bootstrap por provincias de E2 (semilla fija) para un IC alternativo
    rng = np.random.default_rng(SEED)
    bs = []
    for _ in range(2000):
        s = d.iloc[rng.integers(0, len(d), len(d))]
        if s.isla.nunique() < 2 or s.costa.nunique() < 2:
            continue
        bs.append(smf.ols(esp["E2_controles"], data=s).fit().params["nr_ini"])
    ic_bs = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    ph = holm(pv)
    tab = pd.DataFrame([{"especificacion": k, "variable": ests[k][0], "coef": ests[k][1], "ic95_lo": ests[k][2][0],
                         "ic95_hi": ests[k][2][1], "p_hc3": pv[k], "p_holm": ph[k]} for k in pv])
    tab.to_csv(TAB / "no_residentes_regresiones.csv", index=False)
    reg.log("R1A_BK002", "E2_bootstrap", esp["E2_controles"], 2015, 2025, len(d), np.nan, np.nan, np.nan,
            coef_interes=float(np.mean(bs)), notas=f"bootstrap 2000 rem. IC95 [{ic_bs[0]:.4f}; {ic_bs[1]:.4f}]")
    # Hechos de peso inicial por unidad
    top = d.sort_values("nr2025", ascending=False).head(5)
    d_stats = dict(n=len(d), prov=int((d.nivel == "provincia").sum()),
                   nr_ini_min=float(d.nr_ini.min()), nr_ini_max=float(d.nr_ini.max()),
                   nr2025_min=float(d.nr2025.min() * 100), nr2025_max=float(d.nr2025.max() * 100),
                   top=[(r.unidad, round(r.nr2025 * 100, 1)) for r in top.itertuples()],
                   dlnp_min=float(d.dlnp.min()), dlnp_max=float(d.dlnp.max()),
                   pearson_dlnp_nr=float(d[["dlnp", "nr_ini"]].corr().iloc[0, 1]),
                   spearman_dlnp_nr=float(d[["dlnp", "nr_ini"]].corr(method="spearman").iloc[0, 1]))
    return dict(n=len(d), tab=tab, nac_nr=nac_nr, nac_re=nac_re, corr_cc=corr_cc, dif_media=dif_media,
                ic_bs=ic_bs, stats=d_stats, e2=ests["E2_controles"], e1=ests["E1_bivariada"],
                n_cc=len(cc), r2=float(res["E2_controles"].rsquared_adj), d=d)


# ---------------------------------------------------------------------------------------------------- BK-052
def tarea_bk052() -> dict:
    g = pd.read_csv(RAW / "gva_vut_municipio.csv.gz", low_memory=False)
    ine = pd.read_csv(RAW / "ine_v2_vut.csv")
    ine = ine[(ine.medida == "viviendas_turisticas") & (ine.nivel == "provincia")]
    codigos = {"03": "Alicante/Alacant", "12": "Castellón/Castelló", "46": "Valencia/València"}
    stock = g[g.serie.str.startswith("vut_stock_prov_")].copy()
    stock["cod"] = stock.serie.str[-2:]
    stock["fecha"] = pd.to_datetime(stock.fecha)
    filas = []
    for f in sorted(ine.fecha.unique()):
        fd = pd.Timestamp(f)
        if fd > pd.Timestamp("2024-12-01"):
            continue
        fm = fd.replace(day=1)
        for cod, nom in codigos.items():
            s = stock[(stock.cod == cod) & (stock.fecha == fm)].valor
            i = ine[(ine.fecha == f) & (ine.territorio == nom)].valor
            if len(s) and len(i):
                filas.append(dict(fecha=str(fm.date()), provincia=nom, gva_stock=float(s.iloc[0]), ine=float(i.iloc[0])))
    c = pd.DataFrame(filas)
    c["ratio"] = c.gva_stock / c.ine
    c.round(3).to_csv(TAB / "vut_ine_vs_gva_provincias.csv", index=False)
    tot = c.groupby("fecha")[["gva_stock", "ine"]].sum()
    tot["ratio"] = tot.gva_stock / tot.ine
    tot.round(3).to_csv(TAB / "vut_ine_vs_gva_total3prov.csv")
    # Factor 1: fecha/estacionalidad INE (rango máx/mín de INE en 2023-2024 vs estable de GVA)
    ine3 = ine[ine.territorio.isin(codigos.values())].pivot_table(index="fecha", columns="territorio", values="valor").sum(axis=1)
    ine3 = ine3[(ine3.index >= "2023-02-01") & (ine3.index <= "2024-12-01")]
    # Cota de desfase de fecha: mayor variación del INE entre dos observaciones consecutivas separadas <=3 meses
    ine3 = ine3.sort_index()
    idx = pd.to_datetime(ine3.index)
    dif = [max(ine3.iloc[k + 1] / ine3.iloc[k], ine3.iloc[k] / ine3.iloc[k + 1]) for k in range(len(ine3) - 1)
           if (idx[k + 1] - idx[k]).days <= 95]
    f_fecha_max = float(max(dif))
    # Ratio de referencia 2024-11 (INE) frente a stock GVA 2024-11 y 2024-12
    ref = tot.loc["2024-11-01"]
    r_ref = float(ref.ratio)
    # Factor 2: bajas no depuradas. GVA: stock (2024-12) frente a la foto del registro vigente (2026-10-09)
    foto = g[g.serie.str.startswith("vut_foto_prov_")].valor.sum()
    st24 = float(stock[stock.fecha == "2024-12-01"].valor.sum())
    f_bajas = st24 / float(foto)  # >1: parte del stock ya no figura vigente 22 meses después (cota inferior del efecto; fechas distintas)
    # Factor 3: cobertura. INE provincia (total) frente a suma de secciones; se mide en las 3 provincias y a escala nacional
    s = pd.read_csv(RAW / "v3" / "ine_v3_vut_seccion.csv.gz", dtype={"codigo": str, "territorio": str})
    s = s[(s.nivel == "seccion") & (s.medida == "vivienda_turistica")].copy()
    s["prov"] = s.codigo.str.zfill(10).str[:2]
    suma = s.groupby(["periodo", "prov"]).valor.sum().unstack()
    nac = ine[ine.territorio.notna()].groupby(["periodo", "territorio"]).valor.sum().unstack()  # por provincia
    cov = []
    for per in ["2024M11", "2025M11", "2026M05"]:
        ip = ine[ine.periodo == per].set_index("territorio").valor
        for cod, nom in codigos.items():
            if per in suma.index and cod in suma.columns and nom in ip.index:
                cov.append(dict(periodo=per, ambito=nom, ine_prov=float(ip[nom]), suma_secciones=float(suma.loc[per, cod]),
                                cobertura=float(suma.loc[per, cod] / ip[nom])))
        todas = ip.sum()
        sn = suma.loc[per].sum() if per in suma.index else np.nan
        cov.append(dict(periodo=per, ambito="52 provincias (suma)", ine_prov=float(todas), suma_secciones=float(sn),
                        cobertura=float(sn / todas)))
    cov = pd.DataFrame(cov)
    cov.round(3).to_csv(TAB / "vut_ine_cobertura_secciones.csv", index=False)
    cob_nac = cov[cov.ambito == "52 provincias (suma)"].cobertura.tolist()
    cob_cv = cov[cov.ambito != "52 provincias (suma)"].cobertura
    # Cota de cobertura: la discrepancia GVA/INE usa INE provincial (cobertura completa por construcción); la
    # secciones secretas (<umbral) pierden viviendas. Cota: 1/cobertura_min aplicada solo si se usan secciones.
    f_cober_sec = float(1 / cov[cov.ambito == "52 provincias (suma)"].cobertura.min())
    # Ratio contemporáneo: registro vigente de la GVA (2026-10-09) frente a INE 2026-05 (mismo orden de fecha)
    ine26 = ine[(ine.periodo == "2026M05") & ine.territorio.isin(codigos.values())].set_index("territorio").valor
    fp = g[g.serie.str.startswith("vut_foto_prov_")].assign(cod=lambda x: x.serie.str[-2:]).set_index("cod").valor
    ratio_foto = {nom: float(fp[cod] / ine26[nom]) for cod, nom in codigos.items()}
    ratio_foto_tot = float(fp.sum() / ine26.sum())
    # Residual: definición (anuncios activos en plataformas frente a registro de altas con bajas no depuradas)
    r_total = r_ref
    ln = np.log
    res = dict(
        r_total=r_total, f_fecha_max=f_fecha_max, f_bajas=f_bajas,
        resto=r_total / f_bajas, resto_con_fecha=r_total / (f_bajas * f_fecha_max),
    )
    # Intervalo del ratio observado en todo el periodo 2020-2024 (rango entre fechas y provincias)
    rango = (float(c.ratio.min()), float(c.ratio.max()))
    rango_tot = (float(tot.ratio.min()), float(tot.ratio.max()))
    # Cuota explicada (en logs) por factor, como cota: min..max
    sh = {
        "fecha_estacionalidad_INE (cota superior)": (0.0, ln(f_fecha_max) / ln(r_total)),
        "bajas_no_depuradas (solo cota inferior; fechas distintas)": (ln(f_bajas) / ln(r_total), float("nan")),
        "cobertura (INE provincial ya completa)": (0.0, 0.0),
    }
    # revisión R (B2): las bajas solo tienen cota inferior, así que el residual solo tiene cota SUPERIOR (no identificado por abajo)
    hi_res = 1 - sum(v[0] for v in sh.values())
    sh["residual_definicion (anuncios activos vs registro; solo cota superior)"] = (float("nan"), hi_res)
    pd.DataFrame([{"factor": k, "cuota_ln_min": v[0], "cuota_ln_max": v[1]} for k, v in sh.items()]).round(3).to_csv(
        TAB / "vut_discrepancia_descomposicion.csv", index=False)
    return dict(c=c, tot=tot, ratio_foto=ratio_foto, ratio_foto_tot=ratio_foto_tot, r_ref=r_ref, rango=rango, rango_tot=rango_tot, f_fecha=f_fecha_max, f_bajas=f_bajas,
                foto=float(foto), st24=st24, cob=cob_nac, cob_cv=[float(cob_cv.min()), float(cob_cv.max())], sh=sh,
                res=res, f_cober_sec=f_cober_sec)


# ---------------------------------------------------------------------------------------------------- BK-014
def tarea_bk014() -> dict:
    a = pd.read_csv(RAW / "v3" / "airbnb_insideairbnb_agregados_v3.csv.gz")
    cols = a.columns.tolist()
    ia = dict(cols=cols, n=len(a), series=sorted(a.serie.unique())[:12] if "serie" in a.columns else None)
    # Qué existe en el repositorio
    disp = {
        "INE estadística experimental de alojamiento": "VUT sin duración de estancia (data/raw/ine_v2_vut.csv): sin alquiler de temporada",
        "SERPAVI": "contratos de alquiler declarados en IRPF; sin duración ni habitación (data/raw/pdf/serpavi_*)",
        "fianzas autonómicas (Incasòl)": "data/raw/v3/incasol_fianzas_municipio_v3.csv.gz: fianzas de contratos de alquiler de vivienda; sin duración",
        "Inside Airbnb": "agregados v3 con room_type/minimum_nights solo para ciudades concretas (C4, fuente única)",
    }
    return dict(ia=ia, disp=disp)


def escribir(r2: dict, r52: dict, r14: dict) -> None:
    t = r2["tab"].set_index("especificacion")
    e1, e2 = t.loc["E1_bivariada"], t.loc["E2_controles"]
    st = r2["stats"]
    sh = r52["sh"]
    nota_fuentes = ("MIVAU (Boletín, tabla 1.6, residencia del comprador) y Notariado (CCAA) no son independientes; "
                    "Registradores no separa residentes de no residentes ni publica la residencia por provincia: una sola fuente "
                    "efectiva para el peso provincial, por lo que no se alcanza C1.")
    resultado = {
        "rama": "R1A",
        "pregunta": "¿Se asocia el peso inicial de los compradores extranjeros no residentes con la subida de precios provincial "
                    "2015-2025? Además: conciliación VUT INE frente a GVA (BK-052) y alquiler de temporada/por habitaciones (BK-014).",
        "capa": "C4",
        "datos": "MIVAU Boletín (transacciones por residencia del comprador, valor tasado libre €/m2; hasta 2026T2); INE padrón "
                 "(1 enero) y CRE (PIB provincial 2015); Notariado CCAA 2025; INE VUT (provincia, sección) y GVA Registre de Turisme (stock a 2024-12, registro vigente 2026-10-09)",
        "N": {"unidades_BK002": r2["n"], "provincias": st["prov"], "uniprovinciales_como_CCAA": r2["n"] - st["prov"],
              "fechas_BK052": int(len(r52["tot"])), "provincias_BK052": 3},
        "metodo": "BK-002: corte transversal MCO con errores HC3, 8 especificaciones registradas (Holm) y bootstrap de 2000 "
                  "remuestreos; BK-052: conciliación multiplicativa (cotas por factor); BK-014: inventario de fuentes.",
        "estimacion": {
            "BK002_E1_bivariada_dlnP_por_pp_nr": float(e1.coef),
            "BK002_E2_con_controles_dlnP_por_pp_nr": float(e2.coef),
            "BK052_ratio_GVA_INE_2024_11": r52["r_ref"], "BK052_ratio_foto_2026": r52["ratio_foto_tot"]},
        "ic95": {"BK002_E1": [float(e1.ic95_lo), float(e1.ic95_hi)], "BK002_E2": [float(e2.ic95_lo), float(e2.ic95_hi)],
                 "BK002_E2_bootstrap": r2["ic_bs"]},
        "p_ajustado": {k: float(v) for k, v in t.p_holm.items()},
        "nivel_evidencia": "EXPLORATORIO (C4): asociación transversal con ~50 unidades; sin identificación causal",
        "diagnosticos": {"R2_aj_E2": r2["r2"], "pearson_dlnp_nr": st["pearson_dlnp_nr"], "spearman_dlnp_nr": st["spearman_dlnp_nr"],
                         "spec_curve": "con renta, población y costa/islas (E2-E8) el coeficiente no se distingue de cero (p_Holm=1); el IC95 de E2 [-0,55; 0,59] es compatible con cero y con hasta un 60 % del coeficiente bivariado (E1): no se puede atribuir la asociación bivariada a ningún factor",
                         "fuentes_BK002": nota_fuentes,
                         "BK014": "NO ANALIZADA: FALTAN DATOS (ver docs/v5/fuentes_fallidas.md)"},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": [
            "Peso de no residentes extranjeros = compraventas de no residentes extranjeros / total (MIVAU, años completos); peso inicial = media 2015-2016.",
            "Precio = valor tasado medio de vivienda libre (MIVAU, €/m2), logaritmo de la media 2025 menos la media 2015.",
            "Costa e islas: lista del analista (21 unidades costeras, 3 insulares), sensibilidad E6 y E8.",
            "Ceuta y Melilla excluidas; 7 comunidades uniprovinciales entran con datos de CCAA.",
            "Sin lenguaje causal: con controles el coeficiente no se distingue de cero, pero el IC95 no excluye una asociación de hasta el 60 % de la bivariada; no se atribuye a costa e islas ni a un efecto.",
            f"BK-052: el cociente GVA/INE cae entre {r52['rango_tot'][0]:.2f} y {r52['rango_tot'][1]:.2f} (3 provincias) y por provincia/fecha entre {r52['rango'][0]:.2f} y {r52['rango'][1]:.2f}. GVA solo cubre 3 provincias.",
        ]}
    json.dump(resultado, open(OUT / "resultado.json", "w"), ensure_ascii=False, indent=1)
    H = lambda i, ind, v, lo, hi, u, per, cob, fu, capa: {"id": i, "indicador": ind, "valor": v, "min": lo, "max": hi, "unidad": u,  # noqa: E731
                                                          "periodo": per, "cobertura": cob, "fuentes": fu, "capa": capa,
                                                          "fecha_dato": FECHA_DATO}
    n = r2["nac_nr"]
    hechos = [
        H("R1A-H1", "Peso de compradores extranjeros no residentes en las compraventas, España 2025", round(n[2025], 2),
          round(n[2025], 2), round(n[2025], 2), "%", "2025", "España", ["MIVAU Boletín tabla 1.6"], "C4"),
        H("R1A-H2", "Peso de compradores extranjeros no residentes, España 2015", round(n[2015], 2), round(n[2015], 2),
          round(n[2015], 2), "%", "2015", "España", ["MIVAU Boletín tabla 1.6"], "C4"),
        H("R1A-H3", "Peso de no residentes extranjeros por provincia 2025 (rango entre unidades)", round(st["nr2025_max"], 1),
          round(st["nr2025_min"], 2), round(st["nr2025_max"], 1), "%", "2025", f"{r2['n']} unidades",
          ["MIVAU Boletín tabla 1.6"], "C4"),
        H("R1A-H4", "Asociación bivariada precio 2015-2025 y peso inicial de no residentes (coef.)", round(100 * float(e1.coef), 2),
          round(100 * float(e1.ic95_lo), 2), round(100 * float(e1.ic95_hi), 2), "% de precio por punto de peso inicial",
          "2015-2025", f"{r2['n']} unidades", ["MIVAU Boletín"], "C4"),
        H("R1A-H5", "Misma asociación con renta, población, costa e islas (coef.)", round(100 * float(e2.coef), 2),
          round(100 * float(e2.ic95_lo), 2), round(100 * float(e2.ic95_hi), 2), "% de precio por punto de peso inicial",
          "2015-2025", f"{r2['n']} unidades", ["MIVAU Boletín", "INE padrón", "INE CRE"], "C4"),
        H("R1A-H6", "Cociente VUT registro GVA (stock) / INE, 3 provincias valencianas, 2024-11", round(r52["r_ref"], 2),
          round(r52["rango_tot"][0], 2), round(r52["rango_tot"][1], 2), "veces", "2020-08 a 2024-11", "Alicante, Castellón, Valencia",
          ["INE VUT (experimental)", "GVA Registre de Turisme"], "C4"),
        H("R1A-H7", "Cociente VUT registro vigente GVA (2026-10-09) / INE (2026-05)", round(r52["ratio_foto_tot"], 2),
          round(min(r52["ratio_foto"].values()), 2), round(max(r52["ratio_foto"].values()), 2), "veces", "2026", "3 provincias",
          ["INE VUT (experimental)", "GVA Registre de Turisme"], "C4"),
        H("R1A-H8", "Cobertura de la suma de secciones INE VUT frente al total provincial (52 provincias)", round(100 * float(np.mean(r52["cob"])), 1),
          round(100 * min(r52["cob"]), 1), round(100 * max(r52["cob"]), 1), "%", "2024-11 a 2026-05", "España", ["INE VUT (experimental)"], "C4"),
    ]
    json.dump(hechos, open(OUT / "hechos.json", "w"), ensure_ascii=False, indent=1)
    ficha = [{
        "id": "R1A-V1", "tema": "Compradores extranjeros y precio por provincia",
        "enunciado": "Los compradores extranjeros encarecen la vivienda.", "capa": "C4",
        "magnitud": (f"Peso de no residentes extranjeros en las compraventas: España {n[2015]:.1f} % (2015) y {n[2025]:.1f} % (2025); "
                     f"por unidad en 2025 entre {st['nr2025_min']:.2f} % y {st['nr2025_max']:.1f} % (Alicante, Málaga, Baleares y Tenerife en cabeza). "
                     f"Sin controles, cada punto de peso inicial se asocia con {100*float(e1.coef):.2f} % más de subida de precio 2015-2025 "
                     f"(IC95 {100*float(e1.ic95_lo):.2f} a {100*float(e1.ic95_hi):.2f}); con renta, población, costa e islas, "
                     f"{100*float(e2.coef):.2f} % (IC95 {100*float(e2.ic95_lo):.2f} a {100*float(e2.ic95_hi):.2f}; p Holm = 1)."),
        "intervalo": f"[{100*float(e2.ic95_lo):.2f}; {100*float(e2.ic95_hi):.2f}] % por punto de peso (con controles, C4)",
        "cota": "— (sin cota C2 de precio)",
        "literatura": "NO VERIFICADA (sin DOI Crossref en esta pasada; cuartil no verificado). El resultado es una asociación transversal, no un efecto.",
        "veredicto": "ANALIZADA, NO CONCLUYENTE",
        "regla": "Capa C4 (menor de sus componentes): una sola fuente efectiva por provincia (MIVAU/Notariado no independientes; Registradores sin residencia por provincia) y sin diseño de identificación; el máximo con C4 es ANALIZADA, NO CONCLUYENTE.",
        "limites": ("~50 unidades, 1 corte transversal; costa e islas concentran a la vez peso de no residentes y subida de precio; con controles el coeficiente no se distingue de cero (IC95 compatible con cero y con hasta un 60 % de la bivariada); no se identifica un efecto; "
                    "valor tasado ≠ precio de transacción; MIVAU cubre todas las viviendas y el Notariado solo vivienda libre (cociente Notariado/MIVAU de extranjeros por CCAA 1,04-1,24, correlación de rangos "
                    f"{r2['corr_cc']:.2f}); errores robustos HC3 con pocas unidades pueden subestimar la varianza; peso de residentes extranjeros (E4) tampoco se asocia con controles."),
        "evidencia": ["output/v5/R1A/tablas/no_residentes_regresiones.csv", "output/v5/R1A/tablas/no_residentes_peso_2015_2025.csv",
                      "output/v5/R1A/tablas/extranjeros_notariado_vs_mivau_ccaa_2025.csv", "output/v5/R1A/registro.csv"]}]
    json.dump(ficha, open(OUT / "fichas_verificador.json", "w"), ensure_ascii=False, indent=1)
    (OUT / "bk052_bk014.json").write_text(json.dumps({
        "BK052": {"ratio_2024_11": r52["r_ref"], "ratio_rango_total": r52["rango_tot"], "ratio_rango_prov_fecha": r52["rango"],
                  "ratio_foto_2026": r52["ratio_foto"], "cuotas_ln": r52["sh"], "cobertura_secciones": r52["cob"],
                  "cobertura_CV": r52["cob_cv"], "capa": "C4"},
        "BK014": {"estado": "NO ANALIZADA: FALTAN DATOS", "inventario": r14["disp"]}}, ensure_ascii=False, indent=1))


def main() -> None:
    reg = Registry(OUT / "registro.csv")
    r2 = tarea_bk002(reg)
    r52 = tarea_bk052()
    r14 = tarea_bk014()
    reg.flush()
    escribir(r2, r52, r14)
    print(json.dumps(dict(r2={k: v for k, v in r2.items() if k not in ("tab", "d")}), ensure_ascii=False, default=str, indent=1))
    print(r2["tab"].round(4).to_string())
    print(json.dumps({k: v for k, v in r52.items() if k not in ("c", "tot")}, ensure_ascii=False, default=str, indent=1))
    print(json.dumps(r14, ensure_ascii=False, default=str, indent=1))


if __name__ == "__main__":
    main()

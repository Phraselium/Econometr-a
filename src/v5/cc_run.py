"""CC · C7 (desigualdad: esfuerzo por quintil/tenencia y ayuda familiar) y C2 (salida de vivienda protegida).

Determinista, sin red. Lee data/raw/v5/cc_*, data/raw/mivau_v2_protegida.csv y data/raw/v3/*.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261010
np.random.seed(SEED)
R = Path(__file__).resolve().parents[2]
RAW, OUT = R / "data" / "raw", R / "output" / "v5" / "CC"
(OUT / "tablas").mkdir(parents=True, exist_ok=True)
REG: list[dict] = []
HECHOS: list[dict] = []


def reg(fase, modelo, formula, ini, fin, n, notas, coef=None):
    REG.append(dict(fase=fase, modelo_id=modelo, formula=formula, muestra_ini=ini, muestra_fin=fin, n=n,
                    r2_adj=None, aic=None, bic=None, rmse_oos=None, coef_interes=coef, p_interes=None, notas=notas))


def hecho(id_, ind, val, mn, mx, uni, per, cob, fu, capa, fecha):
    HECHOS.append(dict(id=id_, indicador=ind, valor=val, min=mn, max=mx, unidad=uni, periodo=per,
                       cobertura=cob, fuentes=fu, capa=capa, fecha_dato=fecha))


# ---------------------------------------------------------------- C7 (a)
def c7a():
    q = pd.read_csv(RAW / "v5" / "cc_eurostat_ilc_lvho07b.csv")
    t = pd.read_csv(RAW / "v5" / "cc_eurostat_ilc_lvho07c.csv")
    upd = q["actualizado"].iloc[0][:10]
    qt = q.pivot_table(index=["geo", "quant_inc"], columns="time", values="valor")
    tt = t.pivot_table(index=["geo", "tenure"], columns="time", values="valor")
    ult = int(q["time"].max())
    out = []
    for nom, tab in (("quintil", qt), ("tenencia", tt)):
        for (g, k), r in tab.iterrows():
            out.append(dict(dimension=nom, geo=g, grupo=k, y2015=r.get(2015), ultimo=r.get(ult), anio_ultimo=ult,
                            cambio_pp=round(r.get(ult) - r.get(2015), 1), min_2015_ult=r.loc[2015:ult].min(),
                            max_2015_ult=r.loc[2015:ult].max()))
            reg("C7a", f"{nom}|{g}|{k}", "sobrecarga% 2015 vs ultimo (descriptivo, sin SE publicado)", 2015, ult, ult - 2014,
                f"Eurostat ilc_lvho07{'b' if nom == 'quintil' else 'c'}, act. {upd}; sin p-valor: la fuente no publica errores tipicos", out[-1]["cambio_pp"])
    df = pd.DataFrame(out)
    df.to_csv(OUT / "tablas" / "sobrecarga_quintil_tenencia_2015_ultimo.csv", index=False)
    g = lambda d, geo, k: df[(df.dimension == d) & (df.geo == geo) & (df.grupo == k)].iloc[0]
    for k, nom in (("QU1", "primer quintil"), ("QU5", "quinto quintil")):
        r = g("quintil", "ES", k)
        hecho(f"CC-C7a-qu-{k}", f"Tasa de sobrecarga de coste de vivienda, {nom} de renta, España", r.ultimo, r.min_2015_ult,
              r.max_2015_ult, "% de personas", f"{ult} (2015: {r.y2015} %)", "España; rango = mín-máx 2015-" + str(ult),
              "Eurostat ilc_lvho07b (= ECV del INE; una sola fuente)", "C4", upd)
    for k, nom in (("RENT_MKT", "inquilinos a precio de mercado"), ("OWN_L", "propietarios con hipoteca")):
        r = g("tenencia", "ES", k)
        hecho(f"CC-C7a-ten-{k}", f"Tasa de sobrecarga de coste de vivienda, {nom}, España", r.ultimo, r.min_2015_ult,
              r.max_2015_ult, "% de personas", f"{ult} (2015: {r.y2015} %)", "España; rango = mín-máx 2015-" + str(ult),
              "Eurostat ilc_lvho07c (= ECV del INE; una sola fuente)", "C4", upd)
    return df, ult


# ---------------------------------------------------------------- C7 (b)
def c7b():
    j = json.load(open(RAW / "v5" / "cc_ine_t59953.json"))
    rows = []
    for x in j:
        p = x["Nombre"].split(". ")
        d = max(x["Data"], key=lambda z: z["Anyo"])
        rows.append(dict(tenencia=p[1], decil=p[2], anio=d["Anyo"], pct_de_la_tenencia=d["Valor"]))
    dec = pd.DataFrame(rows)
    dec.to_csv(OUT / "tablas" / "ine_ecv_decil_por_tenencia.csv", index=False)
    mk = dec[dec.tenencia == "Alquiler a precio de mercado"].set_index("decil").pct_de_la_tenencia
    bajos = float(mk[["Primer decil", "Segundo decil", "Tercer decil"]].sum())
    reg("C7b", "ecv59953|alquiler_mercado|deciles1-3", "suma % de inquilinos a precio de mercado en deciles 1-3", 2025, 2025, 3,
        "INE ECV t.59953 (distribucion por decil dentro de cada tenencia, no tasa por decil)", bajos)
    hecho("CC-C7b-alq-d123", "Inquilinos a precio de mercado situados en los deciles 1-3 de renta por UC", round(bajos, 1), None, None,
          "% de personas inquilinas", "2025", "España", "INE ECV t.59953", "C4", "2025")
    e = pd.read_csv(RAW / "v3" / "ine_ecv_tenencia_edad_v3.csv")
    e = e[e.serie.str.contains("Ambos")]
    e = e.assign(t=e.serie.str.split("|").str[1], ed=e.serie.str.split("|").str[2].str.replace("edad_persona_referencia=", ""))
    jov = e[(e.ed == "De 16 a 29 años") & e.periodo.isin([2015, 2025])].pivot_table(index="t", columns="periodo", values="valor")
    jov.to_csv(OUT / "tablas" / "ecv_tenencia_16_29.csv")
    prop, sin, ces = jov.loc["Propiedad", 2025], jov.loc["Propiedad sin hipoteca", 2025], jov.loc["Cesión", 2025]
    reg("C7b", "ecv9994|16-29|prop_sin_hipoteca/prop", "propiedad sin hipoteca / propiedad, hogares 16-29", 2025, 2025, 1,
        "Aproximacion: sin hipoteca no equivale a herencia/donacion; cota de lectura, no medida", round(sin / prop, 3))
    hecho("CC-C7b-jov-prop", "Hogares con persona de referencia de 16-29 años en propiedad", prop, jov.loc["Propiedad", 2015], prop,
          "% de hogares", "2025 (2015 en min)", "España", "INE ECV t.9994", "C4", "2025")
    hecho("CC-C7b-jov-sinhip", "Hogares de 16-29 años en propiedad sin hipoteca (proxy NO medida de herencia/donación)", sin, None, None,
          "% de hogares", "2025", "España", "INE ECV t.9994", "C4", "2025")
    hecho("CC-C7b-jov-cesion", "Hogares de 16-29 años en vivienda cedida (gratis o precio inferior)", ces, jov.loc["Cesión", 2015], ces,
          "% de hogares", "2025 (2015 en min)", "España", "INE ECV t.9994", "C4", "2025")
    f = pd.read_csv(RAW / "v3" / "eff_tenencia_edad_v3.csv")
    f = f[f.serie.str.startswith("eff_pct_hogares_vivienda_principal|edad=<35")][["periodo", "serie", "valor"]]
    f.to_csv(OUT / "tablas" / "eff_pct_vivprincipal_menor35.csv", index=False)
    return jov, f


# ---------------------------------------------------------------- C2
def c2():
    p = pd.read_csv(RAW / "mivau_v2_protegida.csv")
    p = p[pd.to_numeric(p.periodo, errors="coerce").notna()].assign(periodo=lambda d: d.periodo.astype(float).astype(int))
    nac = p[p.serie == "prot_definitiva_anual_nacional"].set_index("periodo").valor
    cc = p[p.serie.str.startswith("prot_definitiva_anual_ccaa_") | p.serie.str.contains("ciudad_autonoma")]
    cca = cc.pivot_table(index="periodo", columns="ccaa", values="valor")
    ult = int(nac.index.max())
    cuadre = float((cca.sum(axis=1) - nac).abs().max())
    # Escenarios de plazo L (anios desde la calificacion definitiva). Ver docs en plazos_planes.csv.
    # base: 30 anios para todo; bajo: 30 solo para calificaciones <=2004 (desde 2005 el RD 801/2005 permite ampliar y el de 2026 es permanente);
    # alto: base + 15 anios para calificaciones 2013-2020 (RD sin plazo en el texto; plazo fijado por la CCAA, supuesto).
    def salidas(serie, esc):
        r = {}
        for t in range(2026, 2036):
            if esc == "bajo":
                v = serie.get(t - 30, np.nan) if t - 30 <= 2004 else 0.0
            elif esc == "base":
                v = serie.get(t - 30, np.nan)
            else:
                v = serie.get(t - 30, np.nan) + (serie.get(t - 15, 0.0) if 2013 <= t - 15 <= 2020 else 0.0)
            r[t] = v
        return pd.Series(r)
    tab = pd.DataFrame({e: salidas(nac, e) for e in ("bajo", "base", "alto")})
    tab.index.name = "anio_salida"
    nuevas5 = float(nac.loc[ult - 4:ult].mean())
    tab["calificaciones_nuevas_media_5a"] = nuevas5
    tab["ratio_base"] = (tab["base"] / nuevas5).round(2)
    tab.to_csv(OUT / "tablas" / "salidas_nacional_2026_2035.csv")
    tot = tab[["bajo", "base", "alto"]].sum()
    reg_rows = {e: float(tot[e]) for e in tot.index}
    for e, v in reg_rows.items():
        reg("C2", f"salidas_2026_2035|{e}", "sum_t cal(t-L)", 2026, 2035, 10, "ver plazos_planes.csv; cota con supuestos, sin descalificacion anticipada", v)
    base_ccaa = pd.DataFrame({t: cca.loc[t - 30] if (t - 30) in cca.index else np.nan for t in range(2026, 2036)}).T
    base_ccaa.index.name = "anio_salida"
    base_ccaa.to_csv(OUT / "tablas" / "salidas_base_por_ccaa_2026_2035.csv")
    ccaa_tot = base_ccaa.sum().sort_values(ascending=False)
    ccaa_tot.to_csv(OUT / "tablas" / "salidas_base_total_por_ccaa.csv", header=["viviendas"])
    plazos = [
        ("Plan 1992-1995", "RD 1932/1991", "BOE-A-1992-604", "1991-12-21", "sin plazo de régimen en el texto (solo tanteo/retracto 10 años, 5 años sin transmitir)", "15-30 (supuesto)"),
        ("Plan 1996-1999", "RD 2190/1995", "BOE-A-1995-27970", "1996-01-06", "uso arrendamiento 25 (especial) / 10 (general); sin plazo de régimen de venta; tanteo 10 años", "15-30 (supuesto)"),
        ("Plan 1998-2001", "RD 1186/1998", "BOE-A-1998-15136", "1998-06-24", "sin plazo de régimen de venta; alquiler 10 o 25 años", "15-30 (supuesto)"),
        ("Plan 2002-2005", "RD 1/2002", "BOE-A-2002-689", "2002-01-18", "sin descalificación voluntaria hasta 15 años desde la calificación (art. 10.4); alquiler 25 años", "15-30 (supuesto)"),
        ("Plan 2005-2008", "RD 801/2005", "BOE-A-2005-12049", "2005-07-13", "30 años desde la calificación definitiva, sin descalificación voluntaria; CCAA pueden ampliar", "30 a permanente"),
        ("Plan 2009-2012", "RD 2066/2008", "BOE-A-2008-20751", "2008-12-24", "permanente mientras dure el régimen del suelo (y no menos de 30 años) o 30 años como mínimo", "30 a permanente"),
        ("Plan 2013-2016", "RD 233/2013", "BOE-A-2013-3780", "2013-04-10", "sin plazo general; DA 4ª: descalificación excepcional 3 años; régimen fijado por la CCAA", "15-30 (supuesto)"),
        ("Plan 2018-2021", "RD 106/2018", "BOE-A-2018-3358", "2018-03-10", "alquiler/cesión 25 años mínimo; sin plazo de régimen de venta", "15-30 (supuesto)"),
        ("Plan 2022-2025", "RD 42/2022", "BOE-A-2022-802", "2022-01-19", "alquiler 50 años (públicas) / 20 años (otras); sin plazo de régimen de venta", "15-30 (supuesto)"),
        ("Plan 2026-2030", "RD 326/2026", "BOE-A-2026-8872", "2026-04-23", "permanencia indefinida como condición de financiación", "permanente"),
    ]
    pd.DataFrame(plazos, columns=["plan", "norma", "boe", "fecha_publicacion", "plazo_en_el_texto", "L_usado_anios"]).to_csv(
        OUT / "tablas" / "plazos_planes.csv", index=False)
    f = "2026-10-10"
    for e in ("bajo", "base", "alto"):
        hecho(f"CC-C2-salidas-{e}", f"Viviendas protegidas que salen del régimen 2026-2035 (escenario {e})", float(tot[e]),
              float(tot["bajo"]), float(tot["alto"]), "viviendas", "2026-2035", "España (calificaciones definitivas, planes estatales y autonómicos)",
              "MIVAU Boletín Online tabla 1.6 + BOE (RD de los planes)", "C2", f)
    hecho("CC-C2-nuevas5a", "Calificaciones definitivas de vivienda protegida, media anual", round(nuevas5), None, None, "viviendas/año",
          f"{ult-4}-{ult}", "España", "MIVAU Boletín Online tabla 1.6", "C1" if False else "C4", f"{ult}")
    hecho("CC-C2-ratio", "Salidas anuales medias 2026-2035 (base) / calificaciones nuevas anuales medias 5 años",
          round(float(tot["base"]) / 10 / nuevas5, 2), round(float(tot["bajo"]) / 10 / nuevas5, 2), round(float(tot["alto"]) / 10 / nuevas5, 2),
          "ratio", "2026-2035", "España", "MIVAU + BOE", "C2", f)
    return tab, tot, nuevas5, cuadre, ult, ccaa_tot


def main():
    qt, ult = c7a()
    jov, eff = c7b()
    tab, tot, nuevas5, cuadre, ultp, ccaa_tot = c2()
    pd.DataFrame(REG).to_csv(OUT / "registro.csv", index=False)
    json.dump(HECHOS, open(OUT / "hechos.json", "w"), ensure_ascii=False, indent=1)
    es = lambda d, k: float(qt[(qt.dimension == d) & (qt.geo == "ES") & (qt.grupo == k)].iloc[0].cambio_pp)
    estim = {
        "C7a_cambio_pp_2015_a_%d" % ult: {k: es("quintil", k) for k in ("QU1", "QU2", "QU3", "QU4", "QU5")} | {k: es("tenencia", k) for k in ("RENT_MKT", "OWN_L", "OWN_NL", "RENT_FR")},
        "C2_salidas_2026_2035": {k: float(v) for k, v in tot.items()},
        "C2_calificaciones_nuevas_media_5a": nuevas5,
    }
    res = dict(
        rama="CC", pregunta="C7: esfuerzo de vivienda por renta y tenencia y papel de la ayuda familiar; C2: viviendas protegidas que dejan el régimen 2026-2035",
        capa="C4 (C7, fuente única: Eurostat-SILC es la ECV) · C2 (salidas de vivienda protegida, cota con supuestos de plazo)",
        datos="Eurostat ilc_lvho07b/07c; INE ECV t.9994 y t.59953; BdE EFF (cuadros publicados en repo); MIVAU tabla 1.6; BOE (10 RD)",
        N={"sobrecarga_anios": ult - 2014, "calificaciones_anios": int(ultp - 1990)}, metodo="descriptivo por grupo; cota por convolución plazo-calificación en 3 escenarios",
        estimacion=estim, ic95=None, p_ajustado=None, nivel_evidencia="DESCRIPTIVO (C7) · COTA C2 (C2)",
        diagnosticos={"cuadre_suma_CCAA_nacional_max_abs": cuadre, "p_valores": "no aplican: sin errores tipicos publicados", "holm_bh": "n/a (0 contrastes)"},
        fuera_muestra={"modelo": None, "rmse": None, "dm_vs_ar4": None},
        notas="Eurostat ilc_lvho07 es la ECV: ECV y Eurostat NO son independientes, luego no hay C1. INE no publica sobrecarga por decil: solo quintil y tenencia (Eurostat); la tasa quintil x tenencia no esta publicada. EFF: ningun documento accesible del BdE publica herencia/donacion ni ayuda para la entrada (SIN DATO). Plazos de 1992-1998 y 2013-2022 no constan en el RD: supuesto 15-30 años. No se incluye descalificacion anticipada. Los tres escenarios son un rango de supuestos, no cotas estrictas: la cota inferior logica es 0 (si el regimen fuese permanente) y el escenario alto no cubre plazos <15 años. La suma de CCAA difiere de la serie nacional hasta 6024 viviendas/año en algun año (ver diagnosticos). Rango por CCAA no estimable: el plazo autonomico no esta recogido.")
    json.dump(res, open(OUT / "resultado.json", "w"), ensure_ascii=False, indent=1, default=float)
    fichas = [
        dict(id="CC-V1", tema="Desigualdad y ayuda familiar", enunciado="Sin ayuda familiar los jóvenes no pueden comprar vivienda.", capa="C4",
             magnitud="No medible con los datos accesibles: la EFF publicada en el repositorio no recoge herencia, donación ni ayuda para la entrada. Contexto descriptivo: 30,6 % de los hogares de 16-29 años están en propiedad (34,2 % en 2015), de ellos 14,1 puntos sin hipoteca (la ECV no distingue su origen).",
             intervalo="n/d", cota="n/d", literatura="NO VERIFICADA (no se consultó literatura en este módulo)",
             veredicto="ANALIZADA, NO CONCLUYENTE", regla="Con capa C4 el máximo es «ANALIZADA, NO CONCLUYENTE»; la afirmación exige un contrafactual (compra sin ayuda) que ningún dato accesible identifica.",
             limites="Propiedad sin hipoteca no equivale a herencia o donación. Sin cuadro EFF de ayuda familiar. ECV y Eurostat no son fuentes independientes.",
             evidencia=["output/v5/CC/tablas/ecv_tenencia_16_29.csv", "output/v5/CC/tablas/sobrecarga_quintil_tenencia_2015_ultimo.csv"], convenciones={}),
        dict(id="CC-V2", tema="Vivienda protegida", enunciado="Las viviendas protegidas se pierden por descalificación y el parque protegido se erosiona.", capa="C2",
             magnitud=f"Salidas 2026-2035: {tot['bajo']:.0f} (bajo) a {tot['alto']:.0f} (alto) viviendas, base {tot['base']:.0f}, frente a {nuevas5:.0f} calificaciones nuevas al año de media en los últimos 5 años ({ultp-4}-{ultp}).",
             intervalo=f"{tot['bajo']:.0f}-{tot['alto']:.0f} viviendas", cota="C2: plazos como supuesto; sin descalificación anticipada; el stock real y las descalificaciones efectivas no se observan",
             literatura="NO VERIFICADA (el texto introductorio del RD 326/2026 afirma la dinámica de descalificación; no hay contraste independiente)",
             veredicto="PARCIALMENTE", regla="Cota C2 de la salida por fin de plazo; la descalificación efectiva no se observa.",
             limites="Los plazos autonómicos no se han recogido; las salidas son por fin de plazo, no descalificaciones observadas.",
             evidencia=["output/v5/CC/tablas/salidas_nacional_2026_2035.csv", "output/v5/CC/tablas/plazos_planes.csv"], convenciones={}),
    ]
    json.dump(fichas, open(OUT / "fichas_verificador.json", "w"), ensure_ascii=False, indent=1)
    print(tab.round(2).to_string()); print(tot, nuevas5, cuadre, ultp)
    print(ccaa_tot.head(5))


if __name__ == "__main__":
    main()

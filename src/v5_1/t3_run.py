"""T3 · Rangos de necesidad y déficit con las bajas de T1 y la sensibilidad de las liberadas de T2. Determinista, sin red.

1) Déficit 2021-2024 y 2021-2025: fuentes de M0/M1 (sin bajas, C1) + bajas de T1 (C4).
2) Necesidad 2026-2035 = A + R + V + F - M - K + X (X = liberadas que no llegan al mercado; las liberadas NUNCA se restan).
3) Descomposición de la amplitud, un supuesto cada vez. 4) Frase frente a las terminadas actuales. 5) Control de sumas.
Uso: python3 src/v5_1/t3_run.py [--smoke]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
for p in ("src", "src/v3", "src/v4", "src/v5"):
    sys.path.insert(0, str(RAIZ / p))
import b1_run as b1  # noqa: E402
import econ_utils  # noqa: E402
import m1_run as m1  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
RAW = RAIZ / "data" / "raw"
OUT = RAIZ / "output" / "v5_1" / "T3"
SMOKE = "--smoke" in sys.argv
S3 = ("min", "central", "max")
FECHA_DATO = "2025 (ECP y MIVAU); proyección INE 54562 de 2026-06-17"


# ------------------------------------------------------------------ insumos compartidos con T4
def parque_provincial(nombres: dict, cods: list) -> pd.DataFrame:
    """Parque MIVAU a 31-dic por provincia (misma construcción que T1)."""
    cm = b1.pdat.censo2021_municipios().copy()
    cm["cod_prov"] = cm.index.str[:2]
    c21 = cm.groupby("cod_prov").V_TOTAL.sum()
    mp = pd.read_csv(RAW / "mivau_parque.csv")
    park = b1.serie_prov(mp.assign(serie=mp.serie.str.replace("parque_total_viviendas", "parque")), "parque", nombres,
                         {c: m1.UNIPROV_PROT.get(c) for c in cods})
    park = park.reindex(cods)
    park.columns = park.columns.astype(int)
    pall = mp[mp.nivel.isin(["provincia", "ccaa", "ciudad_autonoma"])].pivot_table(index="territorio", columns="periodo",
                                                                                 values="valor", aggfunc="first")
    pall.columns = pall.columns.astype(int)
    for c, nm in (("33", "Asturias (Principado de )"), ("33", "Asturias (Principado de)")):
        if c in cods and park.loc[c].isna().all() and nm in pall.index:
            park.loc[c] = pall.loc[nm]
    cym = [t for t in pall.index if "Ceuta" in t]
    if cym and "51" in cods and "52" in cods and park.loc["51"].isna().all():
        sh51 = c21["51"] / (c21["51"] + c21["52"])
        park.loc["51"] = pall.loc[cym[0]] * sh51
        park.loc["52"] = pall.loc[cym[0]] * (1 - sh51)
    return park


def bajas_pasadas(rate: pd.Series, park: pd.DataFrame, yrs) -> pd.Series:
    """Bajas del periodo pasado: tasa x parque a 31-dic del año anterior (igual que T1)."""
    out = pd.Series(0.0, index=rate.index)
    for y in yrs:
        col = y - 1 if (y - 1) in park.columns else park.columns.max()
        out = out + rate * park[col].reindex(rate.index)
    return out


def muertes_anuales(cods: list, kcod: dict) -> pd.DataFrame:
    """Defunciones anuales de 75+ por provincia 2026-2040 (proyección INE x riesgo de muerte 2024, como B1/T2)."""
    pp, _ = b1.lee_proy_pob()
    mort = b1.lee_mortalidad()
    qk5 = mort.pivot(index="k", columns="e0", values="valor") / 1000.0
    qk = 1.0 - (1.0 - qk5.clip(upper=0.999)) ** 0.2
    qk[95] = qk[90]
    out = {}
    for c in cods:
        k = kcod[c]
        sub = pp[(pp.k == k) & (pp.e >= 75)]
        pv = sub.pivot(index="e", columns="anyo", values="valor")
        band = pv.index.map(lambda e: min(95, 75 + 5 * ((e - 75) // 5)))
        qb = np.array([qk.loc[k, b] for b in band])
        out[c] = pv.mul(qb, axis=0).sum()
    return pd.DataFrame(out).T


def insumos(cods: list, nombres: dict) -> dict:
    kcod = {c: b1.kn(nombres[c]) for c in cods}
    b = pd.read_csv(RAIZ / "output/v5/B1/tablas/B1_provincias.csv", dtype={"cod_prov": str}).set_index("cod_prov").reindex(cods)
    bj = pd.read_csv(RAIZ / "output/v5_1/T1/tablas/bajas_provincia.csv", dtype={"cod_prov": str}).set_index("cod_prov").reindex(cods)
    lib = pd.read_csv(RAIZ / "output/v5_1/T2/tablas/liberadas_detalle.csv", dtype={"cod_prov": str})
    lib = lib[lib.periodo == "2026-2035"].groupby("cod_prov")[["liberadas_min", "liberadas_central", "liberadas_max",
                                                              "no_llega_min", "no_llega_central", "no_llega_max"]].sum().reindex(cods)
    a4 = pd.read_csv(RAIZ / "output/v5/A4/tablas/A4_deficit_provincial_ECP_MIVAU.csv", dtype={"cod_prov": str})
    d_con = a4[a4.periodo == "2021-2025"].set_index("cod_prov").deficit_bajas0.reindex(cods)
    d_con24 = a4[a4.periodo == "2021-2024"].set_index("cod_prov").deficit_bajas0.reindex(cods)
    mc = pd.read_csv(RAIZ / "output/v4/M1/tablas/M1_provincias_combinaciones.csv", dtype={"cod_prov": str})

    def fuente(per, prot):
        x = mc[(mc.periodo == per) & (mc.ruta_hogares == "ECP") & (mc.bajas_pct == 0) & (mc.ambito == "principal")
               & mc.fuente_altas.str.startswith("MIVAU") & (mc.protegida == prot)]
        return x.set_index("cod_prov").deficit.reindex(cods)
    d_sin = fuente("2021-2025", "sin")
    park = parque_provincial(nombres, cods)
    return dict(kcod=kcod, b=b, bj=bj, lib=lib, d_con=d_con, d_sin=d_sin, d_con24=d_con24, park=park,
                muertes=muertes_anuales(cods, kcod))


def componentes(cods: list, ins: dict) -> pd.DataFrame:
    """Tabla provincial 2026-2035 con los componentes en viviendas (10 años), mínimo / central / máximo."""
    b, bj, lib, park = ins["b"], ins["bj"], ins["lib"], ins["park"]
    f = pd.DataFrame({"provincia": b.provincia, "presion": b.presion}, index=cods)
    rate = {s: bj[f"tasa_{s}"].astype(float) for s in S3}
    baj25 = {s: bajas_pasadas(rate[s], park, range(2021, 2026)) for s in S3}
    f["A1_min"] = (ins["d_con"] + baj25["min"]).clip(lower=0)
    f["A1_central"] = ((ins["d_con"] + ins["d_sin"]) / 2 + baj25["central"]).clip(lower=0)
    f["A1_max"] = (ins["d_sin"] + baj25["max"]).clip(lower=0)
    for s in S3:
        f[f"A2_{s}"] = b[f"A2_{s}"]
        f[f"A_{s}"] = f[f"A1_{s}"] + f[f"A2_{s}"]
        f[f"R_{s}"] = 10 * rate[s] * park[park.columns.max()].reindex(cods)
        for k in ("V", "F", "M", "K", "L"):
            f[f"{k}_{s}"] = b[f"{k}_{s}"]
        f[f"X_{s}"] = lib[f"no_llega_{s}"]
    f["N10_min"] = f.A_min + f.R_min + f.V_min + f.F_min - f.M_max - f.K_max + f.X_min
    f["N10_central"] = f.A_central + f.R_central + f.V_central + f.F_central - f.M_central - f.K_central + f.X_central
    f["N10_max"] = f.A_max + f.R_max + f.V_max + f.F_max - f.M_min - f.K_min + f.X_max
    for s in S3:
        f[f"N_anual_{s}"] = f[f"N10_{s}"] / 10
    return f


def deficit_12(ins: dict, cods: list) -> tuple[pd.DataFrame, pd.DataFrame]:
    """12 combinaciones: 4 de fuentes de M0 (2021-2024) x 3 niveles de bajas de T1; y 2021-2025 (2 fuentes ECP x 3)."""
    park, bj = ins["park"], ins["bj"]
    m0 = pd.read_csv(RAIZ / "output/v4/M0/deficit_2021_2024.csv")
    m0 = m0[m0.bajas_pct == 0]
    rate = {s: bj[f"tasa_{s}"].astype(float) for s in S3}
    b24 = {s: float(bajas_pasadas(rate[s], park, range(2021, 2025)).sum()) for s in S3}
    b25 = {s: float(bajas_pasadas(rate[s], park, range(2021, 2026)).sum()) for s in S3}
    f24 = [dict(periodo="2021-2024", hogares=r.hogares, protegida=r.protegida, tasa_bajas=s, deficit_sin_bajas=float(r.deficit),
                bajas=b24[s], deficit=float(r.deficit) + b24[s], capa="C1" if s == "min" else "C4")
           for r in m0.itertuples() for s in S3]
    f25 = [dict(periodo="2021-2025", hogares="ECP", protegida=p, tasa_bajas=s, deficit_sin_bajas=float(d.sum()), bajas=b25[s],
                deficit=float(d.sum()) + b25[s], capa="C1" if s == "min" else "C4")
           for p, d in (("con", ins["d_con"]), ("sin", ins["d_sin"])) for s in S3]
    return pd.DataFrame(f24), pd.DataFrame(f25)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "tablas").mkdir(exist_ok=True)
    (OUT / "figuras").mkdir(exist_ok=True)
    reg = econ_utils.Registry(OUT / "registro.csv")
    _, nombres = m1.provincias_ecp()
    cods = sorted(nombres)
    if SMOKE:
        cods = ["46", "28", "52", "31"]
    ins = insumos(cods, nombres)
    f = componentes(cods, ins)
    D24, D25 = deficit_12(ins, cods)
    D24.to_csv(OUT / "tablas" / "deficit_2021_2024_12_combinaciones.csv", index=False, float_format="%.1f")
    D25.to_csv(OUT / "tablas" / "deficit_2021_2025_combinaciones.csv", index=False, float_format="%.1f")
    for r in pd.concat([D24, D25]).itertuples():
        reg.log("T3", f"T3_def_{r.periodo}_{r.hogares}_{r.protegida}_{r.tasa_bajas}",
                "deficit = deficit sin bajas (M0/M1) + bajas T1 (tasa x parque)", 2021, int(r.periodo[-4:]), 1, np.nan, np.nan,
                np.nan, coef_interes=r.deficit, notas=f"capa {r.capa}")
    if SMOKE:
        print(D24.round(0).to_string())
        print(f[["provincia", "A_central", "R_central", "F_central", "X_central", "N10_central"]].round(0))
        return

    # ---------------- cifras del déficit
    d24 = D24.deficit
    sin24 = D24[D24.tasa_bajas == "min"].deficit
    d24_c = float(D24[D24.tasa_bajas == "central"].deficit.median())
    d25 = D25.deficit
    sin25 = D25[D25.tasa_bajas == "min"].deficit
    d25_c = float(D25[D25.tasa_bajas == "central"].deficit.median())
    old_max = 902808.0

    # ---------------- necesidad nacional por componente
    nac = {}
    for k in ("A1", "A2", "A", "R", "V", "F", "M", "K", "L", "X", "N10"):
        nac[k] = {s: float(f[f"{k}_{s}"].sum()) for s in S3}
    b1_n = {s: float(ins["b"][f"N10_{s}"].sum()) for s in S3}
    # efecto sobre N de cada componente (signo): mínimo = efecto más bajo posible
    efecto = {
        "atraso (A1+A2)": ("A", +1), "reposición (R)": ("R", +1), "flujo futuro (F)": ("F", +1),
        "vacancia friccional (V)": ("V", +1), "movilizables (M)": ("M", -1), "cartera (K)": ("K", -1),
        "liberadas que no llegan al mercado (X)": ("X", +1),
    }
    filas = []
    N_cen = nac["N10"]["central"]
    for nm, (k, sg) in efecto.items():
        lo = sg * nac[k]["min"] if sg > 0 else sg * nac[k]["max"]
        hi = sg * nac[k]["max"] if sg > 0 else sg * nac[k]["min"]
        cen = sg * nac[k]["central"]
        filas.append(dict(componente=nm, efecto_en_N_min=lo, efecto_en_N_central=cen, efecto_en_N_max=hi,
                          N10_si_solo_varia_min=N_cen - cen + lo, N10_si_solo_varia_max=N_cen - cen + hi,
                          amplitud_10a=hi - lo, amplitud_anual=(hi - lo) / 10))
    dec = pd.DataFrame(filas)
    amp_conj = nac["N10"]["max"] - nac["N10"]["min"]
    dec["peso_pct_amplitud_conjunta"] = 100 * dec.amplitud_10a / amp_conj
    dec = dec.sort_values("amplitud_10a", ascending=False).reset_index(drop=True)
    dec["orden"] = np.arange(1, len(dec) + 1)
    dec.to_csv(OUT / "tablas" / "descomposicion_amplitud.csv", index=False, float_format="%.1f")
    # sub-descomposición del atraso (A1: fuentes y bajas; A2: emancipación retrasada)
    sub = pd.DataFrame([
        dict(parte="A1 déficit 2021-2025 (fuentes y bajas)", amplitud_10a=nac["A1"]["max"] - nac["A1"]["min"]),
        dict(parte="A2 emancipación retrasada", amplitud_10a=nac["A2"]["max"] - nac["A2"]["min"]),
        dict(parte="de A1: solo bajas T1 (0 a máx.)", amplitud_10a=float(sum(
            bajas_pasadas(ins["bj"]["tasa_max"].astype(float), ins["park"], range(2021, 2026)))))])
    sub.to_csv(OUT / "tablas" / "descomposicion_atraso.csv", index=False, float_format="%.1f")

    # ---------------- tabla provincial y nacional
    cols = ["provincia", "presion"] + [f"{k}_{s}" for k in ("A1", "A2", "A", "R", "V", "F", "M", "K", "X", "L", "N10") for s in S3] \
        + [f"N_anual_{s}" for s in S3]
    f[cols].round(0).to_csv(OUT / "tablas" / "necesidad_provincial.csv", index_label="cod_prov")
    pd.DataFrame([{"componente": k, **v} for k, v in nac.items()]).to_csv(OUT / "tablas" / "necesidad_nacional.csv", index=False,
                                                                           float_format="%.1f")
    recon = pd.DataFrame([
        dict(paso="B1 (v5): R acotado a 0, A1 con bajas 0-0,2 %, sin X", **{f"N_anual_{s}": b1_n[s] / 10 for s in S3}),
        dict(paso="T3 sin X (R y A1 con bajas T1)", **{f"N_anual_{s}": (nac["N10"][s] - nac["X"][s]) / 10 for s in S3}),
        dict(paso="T3 con X (liberadas que no llegan, suma)", **{f"N_anual_{s}": nac["N10"][s] / 10 for s in S3}),
    ])
    recon.to_csv(OUT / "tablas" / "reconciliacion_con_B1.csv", index=False, float_format="%.0f")

    # ---------------- control de liberadas: necesidad == suma de componentes sin L
    ctrl_l = []
    comp_sum = {s: 0.0 for s in S3}
    for s, inv in (("min", "max"), ("central", "central"), ("max", "min")):
        comp_sum[s] = (nac["A"][s] + nac["R"][s] + nac["V"][s] + nac["F"][s] - nac["M"][inv] - nac["K"][inv] + nac["X"][s])
        ctrl_l.append(dict(tabla=f"necesidad_nacional_10a_{s}", necesidad=nac["N10"][s], suma_componentes_sin_L=comp_sum[s]))
        ctrl_l.append(dict(tabla=f"necesidad_provincial_suma_10a_{s}", necesidad=float(f[f"N10_{s}"].sum()),
                           suma_componentes_sin_L=float((f[f"A_{s}"] + f[f"R_{s}"] + f[f"V_{s}"] + f[f"F_{s}"]
                                                         - f[f"M_{inv}"] - f[f"K_{inv}"] + f[f"X_{s}"]).sum())))
    (OUT / "control_liberadas.json").write_text(json.dumps(ctrl_l, ensure_ascii=False, indent=1))

    # ---------------- frase frente a las terminadas actuales
    tt = pd.read_csv(RAIZ / "output/v4/M0/terminadas_triangulacion.csv")
    tt = tt[tt.anio.between(2019, 2024)]
    p_com = (float(tt.comun_mivau_bruto_sin_PV_NA.min()), float(tt.comun_mivau_bruto_sin_PV_NA.max()))
    p_nac = (float(tt.mivau_bruto_libres_mas_prot.min()), float(tt.mivau_bruto_libres_mas_prot.max()))
    filas = []
    for nm, (lo, hi) in (("territorio común (cifras_clave terminadas_1924)", p_com), ("nacional con País Vasco y Navarra (MIVAU bruto)", p_nac)):
        mid = (lo + hi) / 2
        for s in S3:
            n_a = nac["N10"][s] / 10
            filas.append(dict(serie=nm, produccion_min=lo, produccion_media=mid, produccion_max=hi, necesidad_anual=n_a,
                              necesidad_escenario=s, veces_cabe_con_prod_media=n_a / mid, veces_cabe_con_prod_max=n_a / hi,
                              veces_cabe_con_prod_min=n_a / lo, produccion_cubre_pct=100 * mid / n_a))
    fr = pd.DataFrame(filas)
    fr.to_csv(OUT / "tablas" / "produccion_vs_necesidad.csv", index=False, float_format="%.3f")

    # ---------------- control de sumas provincial = nacional
    m0 = pd.read_csv(RAIZ / "output/v4/M0/deficit_2021_2024.csv")
    a4n = pd.read_csv(RAIZ / "output/v5/A4/tablas/A4_reconciliacion_prov_nacional.csv")
    t1d = pd.read_csv(RAIZ / "output/v5_1/T1/tablas/deficit_con_bajas_estimadas.csv")
    t1 = {(r.periodo, r.escenario): r.bajas for r in t1d.itertuples()}
    t2n = json.loads((RAIZ / "output/v5_1/T2/tablas/agregados.json").read_text())["resumen"]["2026-2035"]
    hp, hnac = b1.lee_proy_hogares()
    cs = []

    def chk(nm, parts, tot, tol=1e-6):
        cs.append(dict(tabla=nm, suma_provincial=float(parts), nacional=float(tot), tolerancia_rel=tol))
    chk("A1_fuente_ECP_con_protegida_2021_2025", ins["d_con"].sum(), a4n[a4n.periodo == "2021-2025"].deficit_nac.iloc[0])
    chk("deficit_2021_2024_fuente_ECP_con_M0", ins["d_con24"].sum(), m0[(m0.hogares == "ECP") & (m0.protegida == "con") & (m0.bajas_pct == 0)].deficit.iloc[0])
    for s in ("central", "max"):
        chk(f"bajas_2021_2024_{s}_T1", D24[(D24.tasa_bajas == s)].bajas.iloc[0], t1[("2021-2024", f"estimada_tasa_{s}")], 1e-6)
        chk(f"bajas_2021_2025_{s}_T1", D25[(D25.tasa_bajas == s)].bajas.iloc[0], t1[("2021-2025", f"estimada_tasa_{s}")], 1e-6)
    chk("X_no_llega_central_10a_T2", f.X_central.sum(), t2n["no_llega_central"], 1e-6)
    chk("X_no_llega_min_10a_T2", f.X_min.sum(), t2n["no_llega_min"], 1e-6)
    chk("X_no_llega_max_10a_T2", f.X_max.sum(), t2n["no_llega_max"], 1e-6)
    chk("F_hogares_2026_2036", f.F_central.sum(), float(hnac[2036] - hnac[2026]), 1e-2)
    chk("necesidad_10a_central", f.N10_central.sum(), nac["N10"]["central"], 1e-9)
    chk("necesidad_10a_min", f.N10_min.sum(), nac["N10"]["min"], 1e-9)
    chk("necesidad_10a_max", f.N10_max.sum(), nac["N10"]["max"], 1e-9)
    for c in cs:
        c["ok"] = abs(c["suma_provincial"] - c["nacional"]) <= c["tolerancia_rel"] * max(1.0, abs(c["nacional"]))
    (OUT / "control_sumas.json").write_text(json.dumps(cs, ensure_ascii=False, indent=1))
    fallos = [c["tabla"] for c in cs if not c["ok"]]
    print("control_sumas fallos:", fallos)

    figura(dec, nac)
    escribe(f, nac, dec, sub, D24, D25, sin24, d24, d24_c, sin25, d25, d25_c, old_max, p_com, p_nac, fr, ctrl_l, fallos, recon)
    reg.flush()


def figura(dec: pd.DataFrame, nac: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 4.8))
    d = dec.iloc[::-1]
    ax.barh(d.componente, d.amplitud_anual / 1000, color="#4575b4")
    for i, r in enumerate(d.itertuples()):
        ax.text(r.amplitud_anual / 1000 + 0.5, i, f"{r.peso_pct_amplitud_conjunta:.0f} %", va="center", fontsize=8)
    ax.set_xlabel("Amplitud (máx. - mín.) de la necesidad, miles de viviendas/año, un supuesto cada vez")
    ax.set_title("T3 · Aporte de cada componente a la amplitud de la necesidad 2026-2035 (C4)\n"
                 f"amplitud conjunta {(nac['N10']['max'] - nac['N10']['min']) / 10000:.0f} mil/año", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "figuras" / "T3_descomposicion_amplitud.png", dpi=110, metadata={"Software": None})
    plt.close(fig)


def esc(x) -> str:
    return f"{x:,.0f}".replace(",", ".")


def escribe(f, nac, dec, sub, D24, D25, sin24, d24, d24_c, sin25, d25, d25_c, old_max, p_com, p_nac, fr, ctrl_l, fallos, recon) -> None:
    N = {s: nac["N10"][s] / 10 for s in S3}
    fd = FECHA_DATO

    def H(i, ind, v, lo, hi, ud, per, cob, fu, capa, fecha=fd):
        return dict(id=i, indicador=ind, valor=None if v is None else round(float(v), 1), min=None if lo is None else round(float(lo), 1),
                    max=None if hi is None else round(float(hi), 1), unidad=ud, periodo=per, cobertura=cob, fuentes=fu, capa=capa,
                    fecha_dato=fecha)
    nb = ["T1", "M0"]
    top = dec.iloc[0]
    # revisión v5.1 (B1): misma cobertura que la necesidad (52 provincias) -> serie nacional con País Vasco y Navarra
    fr_com = fr[fr.serie.str.startswith("nacional")]
    hechos = [
        H("T3-H1", "Déficit acumulado sin bajas (12 combinaciones de M0: 4 de fuentes; las bajas a 0)", None, sin24.min(), sin24.max(),
          "viviendas", "2021-2024", "España", ["M0", "INE ECP/EPA", "Ministerio, Catastro"], "C1", "2024"),
        H("T3-H2", "Déficit acumulado con las bajas estimadas de T1 (4 fuentes x tasa 0 / central / máx.)", d24_c, d24.min(), d24.max(),
          "viviendas", "2021-2024", "España", nb + ["Licencias de demolición MIVAU"], "C4", "2024"),
        H("T3-H3", "Nuevo máximo del déficit 2021-2024 frente al máximo del supuesto antiguo de bajas 0,1-0,2 % (902.808)",
          d24.max(), d24.max(), old_max, "viviendas", "2021-2024", "España", nb, "C4", "2024"),
        H("T3-H4", "Déficit 2021-2025 con las bajas estimadas de T1 (ECP, con y sin protegida)", d25_c, d25.min(), d25.max(), "viviendas",
          "2021-2025", "España", ["A4", "T1"], "C4", "2025"),
        H("T3-H5", "Necesidad anual de vivienda 2026-2035 recalculada (A+R+V+F-M-K+X; no resta liberadas)", N["central"], N["min"], N["max"],
          "viviendas/año", "2026-2035", "España (52 provincias)", ["B1", "T1", "T2", "A4"], "C4"),
        H("T3-H5b", "Necesidad anual de vivienda 2026-2035, base sin la sensibilidad X (A+R+V+F-M-K; no resta liberadas)",
          (nac["N10"]["central"] - nac["X"]["central"]) / 10, (nac["N10"]["min"] - nac["X"]["min"]) / 10, (nac["N10"]["max"] - nac["X"]["max"]) / 10,
          "viviendas/año", "2026-2035", "España (52 provincias)", ["B1", "T1"], "C4"),
        H("T3-H6", "Liberadas por envejecimiento que no llegan al mercado (componente que suma), por año", nac["X"]["central"] / 10,
          nac["X"]["min"] / 10, nac["X"]["max"] / 10, "viviendas/año", "2026-2035", "España", ["T2"], "C4"),
        H("T3-H7", "Reposición con las bajas de T1 (10 años)", nac["R"]["central"], nac["R"]["min"], nac["R"]["max"], "viviendas",
          "2026-2035", "España", ["T1"], "C4"),
        H("T3-H8", f"Amplitud conjunta (máx. - mín.) de la necesidad; mayor aporte: {top.componente}", amp := (N["max"] - N["min"]),
          top.amplitud_anual, top.amplitud_anual, "viviendas/año", "2026-2035", "España", ["T3"], "C4"),
        H("T3-H9", "Veces que cabe la producción actual (terminadas nacionales con País Vasco y Navarra, media 2019-2024) en la necesidad anual con sensibilidad X (mínimo, central, máximo)",
          fr_com[fr_com.necesidad_escenario == "central"].veces_cabe_con_prod_media.iloc[0],
          fr_com[fr_com.necesidad_escenario == "min"].veces_cabe_con_prod_media.iloc[0],
          fr_com[fr_com.necesidad_escenario == "max"].veces_cabe_con_prod_media.iloc[0], "veces", "2019-2024 (producción)", "España (52 provincias)",
          ["M0", "T3"], "C4", "2024"),
    ]
    assert amp > 0
    res = {
        "rama": "v5_1/T3",
        "pregunta": "¿Qué rango tienen el déficit 2021-2025 y la necesidad 2026-2035 con las bajas estimadas (T1) y las liberadas que no llegan al mercado (T2), y qué supuesto pesa más en la amplitud?",
        "capa": "C1 (déficit sin bajas) / C4 (con bajas y necesidad)",
        "datos": ["output/v4/M0", "output/v4/M1", "output/v5/A4", "output/v5/B1", "output/v5_1/T1", "output/v5_1/T2"],
        "N": {"provincias": int(len(f)), "combinaciones_deficit_2021_2024": int(len(D24)), "combinaciones_deficit_2021_2025": int(len(D25))},
        "metodo": "Déficit = fuentes (M0/M1) + bajas T1 (tasa x parque MIVAU); necesidad = A+R+V+F-M-K+X con R y A1 a partir de las bajas de T1 y X = "
                  "liberadas que no llegan al mercado (T2); las liberadas NO se restan; descomposición un supuesto cada vez (aditiva).",
        "estimacion": {
            "deficit_2021_2024": {"sin_bajas_C1": [float(sin24.min()), float(sin24.max())], "con_bajas_T1_C4": {"central": d24_c,
                                  "min": float(d24.min()), "max": float(d24.max())}, "maximo_antiguo": old_max},
            "deficit_2021_2025": {"sin_bajas_C1": [float(sin25.min()), float(sin25.max())], "con_bajas_T1_C4": {"central": d25_c,
                                  "min": float(d25.min()), "max": float(d25.max())}},
            "necesidad_anual": N, "necesidad_10a": nac["N10"],
            "componentes_10a": {k: nac[k] for k in ("A1", "A2", "A", "R", "V", "F", "M", "K", "X")},
            "L_informativa_no_suma_ni_resta_10a": nac["L"],
            "descomposicion_amplitud_anual": {r.componente: {"amplitud": r.amplitud_anual, "peso_pct": r.peso_pct_amplitud_conjunta}
                                              for r in dec.itertuples()},
            "producciones_serie": {"territorio_comun_2019_2024": p_com, "nacional_con_PV_NA_2019_2024": p_nac},
        },
        "ic95": None, "p_ajustado": None,
        "nivel_evidencia": "EXPLORATORIO (C4); el déficit sin bajas es C1 (descriptivo)",
        "diagnosticos": {"control_sumas_fallos": fallos, "control_liberadas": "output/v5_1/T3/control_liberadas.json",
                         "reconciliacion_B1": recon.to_dict("records")},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": [
            "Contabilidad con rangos, no modelo predictivo: AR(4) y ECM v1 no aplican (fuera_muestra null); Holm/BH no aplica (sin contrastes).",
            "Los rangos combinan los extremos de todos los supuestos a la vez: son cotas, no intervalos de confianza.",
            "Déficit 2021-2024: 4 combinaciones de fuentes de M0 (hogares ECP / EPA corregida; con y sin protegida) x 3 niveles de bajas de T1 (0, central, máx.). Sin bajas sigue siendo C1.",
            "Déficit 2021-2025 y A1: solo la ruta ECP provincial (con y sin protegida), porque EPA corregida no existe por provincia ni M0 llega a 2025.",
            "R = 10 x tasa de bajas de T1 x parque MIVAU de 2024 (B1 usaba el parque del Censo 2021 y tasas de identidad acotadas a 0); L se informa pero NO entra: la proyección de hogares del INE ya la descuenta.",
            "X (liberadas que no llegan al mercado) viene de T2 (fuente única, parámetros de residencias sin dato verificado) y SUMA a la necesidad.",
            "Descomposición aditiva: la suma de amplitudes por componente iguala la amplitud conjunta.",
            "Producción actual: se usa la serie del territorio común (cifras_clave terminadas_1924, C1: 72.264-94.426) y, como sensibilidad, la serie nacional con País Vasco y Navarra (78.810-100.980, MIVAU bruto). Como la necesidad cubre 52 provincias, la serie común sobrestima ligeramente las veces.",
            "Sin lenguaje causal; asociaciones y magnitudes descriptivas.",
        ],
    }
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float))
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1, default=float))
    fr_c = fr_com.set_index("necesidad_escenario")
    frase = (f"La producción actual de terminadas ({esc(p_nac[0])}-{esc(p_nac[1])} al año, España con País Vasco y Navarra, 2019-2024) cabe "
             f"{fr_c.loc['min', 'veces_cabe_con_prod_media']:.1f} veces en el mínimo de la necesidad anual ({esc(N['min'])}), "
             f"{fr_c.loc['central', 'veces_cabe_con_prod_media']:.1f} en el central ({esc(N['central'])}) y "
             f"{fr_c.loc['max', 'veces_cabe_con_prod_media']:.1f} en el máximo ({esc(N['max'])}), con la producción media de {esc((p_nac[0] + p_nac[1]) / 2)}; "
             f"con los extremos de la producción el rango es {fr_c.loc['min', 'veces_cabe_con_prod_max']:.1f}-{fr_c.loc['max', 'veces_cabe_con_prod_min']:.1f}.")
    frase = re.sub(r"(\d)\.(\d) ", r"\1,\2 ", frase).replace(".1f}", "")   # decimales con coma
    frase = re.sub(r"(\d)\.(\d)(-|\b)", lambda m: m.group(1) + "," + m.group(2) + m.group(3) if len(m.group(2)) == 1 else m.group(0), frase)
    (OUT / "frase_verificable.txt").write_text(frase + "\n")
    lin = "\n".join(f"| {r.orden} | {r.componente} | {esc(r.amplitud_anual)} | {r.peso_pct_amplitud_conjunta:.1f} % |" for r in dec.itertuples())
    (OUT / "metodo.md").write_text(
        "# T3 · método\n\n"
        "Necesidad 2026-2035 = A + R + V + F − M − K + X, en viviendas (10 años). X = liberadas por envejecimiento que no llegan al mercado (T2), que suma. "
        "Las liberadas no se restan: la proyección de hogares del INE ya las descuenta.\n\n"
        "Déficit con bajas = déficit de las fuentes (M0 para 2021-2024; ECP con y sin protegida para 2021-2025) + bajas de T1 "
        "(tasa 0 / central 0,026 % / máxima 0,052 % por parque).\n\n"
        "Descomposición: cada supuesto entre su mínimo y su máximo con los demás en el central; la amplitud es aditiva.\n\n"
        "| orden | componente | amplitud (viviendas/año) | peso |\n|---|---|---|---|\n" + lin + "\n\n"
        f"Frase: {frase}\n\n"
        "Capa: sin bajas C1 (562.692-688.692); con bajas y necesidad C4. Fechas de datos: " + FECHA_DATO + ".\n")
    print(frase)
    print(dec[["componente", "amplitud_anual", "peso_pct_amplitud_conjunta"]].round(1).to_string())
    print(D24.round(0).to_string())


if __name__ == "__main__":
    main()

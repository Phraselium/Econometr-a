"""V7.1-S1 · Dosis, coste fiscal y normalización de los instrumentos de R6 (v7). Capa C4. SIN análisis nuevo.

Reproduce EXACTAMENTE las extracciones de Monte Carlo de R6 (misma semilla, mismo orden de extracción, rejilla de
elasticidades; la regional no es utilizable en ninguna CCAA) y anota, por extracción:
  - dosis: viviendas añadidas (a-d), compraventas beneficiarias por año (e, f1) o viviendas nuevas por año (f2);
  - coste fiscal anual aproximado (M€/año) cuando hay base versionada; si no, «coste no estimable» con el motivo;
  - efecto por 10.000 viviendas (instrumentos de cantidad) y por 100 M€ anuales (instrumentos con coste);
  - coste por punto de reducción (M€ anuales por punto porcentual), con rango p5-p95.
No se calcula un «umbral de equivalencia» frente a f2: la eficiencia por euro de f2 está inflada por construcción (R6 aplica
el desplazamiento de costes al precio de todo el mercado y el coste fiscal solo a la obra nueva; decisión W3).
Comprueba que la variación de precio reproducida coincide con output/v7/R6/impactos.csv (si no, se detiene).

El signo de los instrumentos de oferta (−) y de demanda (+ en precio de mercado) lo fija en gran parte la fórmula de
incidencia; lo informativo son las magnitudes relativas, y siguen siendo C4.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "v7"))
import r6_propuestas as R6  # noqa: E402

SEED = 20261010
OUT = ROOT / "output" / "v7_1" / "S1"
FECHA = "2026-10-12"
NOMBRE_INSTR = {"a_construccion": "construcción adicional", "b_vacias": "movilización de vacías",
                "c_vivienda_publica": "vivienda pública o asequible", "d_turisticos": "regulación local de turísticos",
                "e_ayuda_demanda": "ayudas a la demanda", "f1_rebaja_ITP_IVA_vivienda_nueva": "rebaja de ITP/IVA (vivienda nueva)",
                "f2_impuestos_construccion": "rebaja de impuestos y costes de construcción (no difundible)"}   # v7.2
DOSIS_DEF = {"a_construccion": "viviendas adicionales acumuladas (llegan tras 1 año); 50-100 % del mínimo entre la necesidad anual T3 y la capacidad observada (máximo anual de visados 2007-2025 menos visados 2025; v7.2)",
             "b_vacias": "viviendas vacías movilizadas acumuladas; triangular(M_min, M_central, M_max) de T3 / 10 por año",
             "c_vivienda_publica": "viviendas públicas o asequibles netas de desplazamiento, acumuladas; 20 % × U(0,5; 1,5) de la necesidad anual, desplazamiento 0-50 %",
             "d_turisticos": "viviendas turísticas que vuelven al uso residencial (una vez); 5-30 % del stock VUT 2025T4",
             "e_ayuda_demanda": "compraventas beneficiarias por año (todas las de 2025) con ayuda del 5-15 % del precio",
             "f1_rebaja_ITP_IVA_vivienda_nueva": "compraventas beneficiarias por año (todas las de 2025; cota superior: el escenario es de vivienda nueva) con rebaja de 1-4 puntos",
             "f2_impuestos_construccion": "viviendas nuevas por año (visados 2025) con rebaja del coste del 2-6 % y cuota del coste en el precio del 40-70 %"}
SIN_BASE = {"a_construccion": "coste no estimable: no hay coste unitario por vivienda (suelo, obra, financiación pública) verificado ni versionado; el escenario no fija quién paga",
            "b_vacias": "coste no estimable: no hay coste unitario verificado de movilización (incentivo, rehabilitación, recargo del IBI) ni reparto entre recaudación y gasto",
            "c_vivienda_publica": "coste no estimable: no hay coste unitario verificado por vivienda pública (v5 D1: «coste unitario sin dato verificado»)",
            "d_turisticos": "coste no estimable: regulación sin coste fiscal directo verificable (inspección y compensaciones sin base)",
            "e_alquiler": "coste no estimable: el panel v7 no tiene renta media del alquiler en euros por CCAA ni número de hogares beneficiarios"}


def simular_s1(cc, b, rej, rng):
    """Copia de R6.simular (fuente «rejilla») con el MISMO orden de extracciones; devuelve vectores por (inst, mer, h)."""
    n = R6.NMC
    ed = rng.uniform(R6.ED_LO, R6.ED_HI, n)
    es = rng.uniform(rej.rej_lo, max(rej.rej_hi, rej.rej_lo + 1e-9), n)
    adj = R6.sendas(rng, n)
    Q = b.parque
    alq = rng.uniform(0.15, 0.20, n) * Q
    inc = ed / (es + ed)
    # v7.2: dosis de construcción adicional NO nula. Capacidad observada = máximo anual de visados 2007-2025 menos visados de 2025
    # (en R6 el máximo de 2016-2025 dejaba la dosis en 0 en 14 CCAA); dosis = 50-100 % del mínimo entre necesidad anual T3 y esa capacidad.
    cap = max(b.vis_max_0725 - b.vis_2025, 0.0)
    a_anual = min(b.N_anual_central, cap) * rng.uniform(0.5, 1.0, n)
    b_anual = rng.triangular(b.M_min, b.M_central, b.M_max, n) / 10 if b.M_max > 0 else np.zeros(n)
    c_anual = 0.2 * b.N_anual_central * rng.uniform(0.5, 1.5, n) * (1 - rng.uniform(0, 0.5, n))
    d_unico = b.vut * rng.uniform(0.05, 0.30, n)
    ofer = {"a_construccion": (a_anual, "anual", rng.uniform(0.1, 0.3, n)), "b_vacias": (b_anual, "anual", rng.uniform(0.3, 0.7, n)),
            "c_vivienda_publica": (c_anual, "anual", rng.uniform(0.8, 1.0, n)), "d_turisticos": (d_unico, "unico", np.ones(n))}
    v = {}
    for inst, (dq, modo, om) in ofer.items():
        for mer in ("precio", "alquiler"):
            for h in R6.HOR:
                acum = dq * (max(h - 1, 0) if modo == "anual" else 1.0)
                base = Q if mer == "precio" else alq
                frac = acum * (1.0 if mer == "precio" else om) / base
                dp = -100 * frac / (es + ed) * adj[h]
                with np.errstate(divide="ignore", invalid="ignore"):
                    e10k = np.where(acum > 0, dp * 1e4 / acum, np.nan)
                v[(inst, mer, h)] = dict(dp=dp, neto=dp, dosis=acum, coste=np.full(n, np.nan), e10k=e10k)
    s_ay = rng.uniform(0.05, 0.15, n)
    s_itp = rng.uniform(0.01, 0.04, n)
    for inst, s, mers in (("e_ayuda_demanda", s_ay, ("precio", "alquiler")), ("f1_rebaja_ITP_IVA_vivienda_nueva", s_itp, ("precio",))):
        for mer in mers:
            for h in R6.HOR:
                dp = 100 * s * inc * adj[h]
                neto = 100 * ((1 + dp / 100) * (1 - s * adj[h]) - 1)
                coste = s * b.valor_compras_meur if mer == "precio" else np.full(n, np.nan)
                v[(inst, mer, h)] = dict(dp=dp, neto=neto, dosis=np.full(n, float(b.compraventas_2025)), coste=coste, e10k=np.full(n, np.nan))
    c_red = rng.uniform(0.02, 0.06, n)
    cuota = rng.uniform(0.4, 0.7, n)
    for mer in ("precio", "alquiler"):
        for h in R6.HOR:
            dp = -100 * c_red * cuota * es / (es + ed) * adj[h]
            coste = c_red * cuota * b.valor_nuevas_meur if mer == "precio" else np.full(n, np.nan)
            v[("f2_impuestos_construccion", mer, h)] = dict(dp=dp, neto=dp, dosis=np.full(n, float(b.vis_2025)), coste=coste, e10k=np.full(n, np.nan))
    return v


def q(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if not len(x):
        return (np.nan, np.nan, np.nan)
    return (float(np.median(x)), float(np.percentile(x, 5)), float(np.percentile(x, 95)))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    R6.SV = R6.semivida_r4()
    d = R6.leer_panel()
    rej = R6.rejilla_a4().set_index("cc")
    bs = R6.base_regional(d)
    cv = d[d.anio == 2025].groupby("cc").compraventas.sum()
    pt = d[d.trimestre == "2025Q4"].set_index("cc").p_tasado
    bs["compraventas_2025"] = cv
    bs["valor_nuevas_meur"] = bs.vis_2025 * R6.M2 * pt / 1e6   # valor de mercado de la obra nueva anual (proxy: visados 2025)
    bs["vis_max_0725"] = d[(d.anio >= 2007) & (d.anio <= 2025)].groupby(["cc", "anio"]).visados.sum().unstack().max(axis=1)   # v7.2
    rob_a = []
    rng0 = np.random.default_rng(SEED)
    filas = []
    for cc in sorted(rej.index):
        seed = int(rng0.integers(1, 2**31))
        v = simular_s1(cc, bs.loc[cc], rej.loc[cc], np.random.default_rng(seed))
        rob_a += robustez_construccion(cc, v, bs.loc[cc])
        for (inst, mer, h), x in v.items():
            con_coste = np.isfinite(x["coste"]).any()
            red = -x["neto"]   # reducción del precio neto pagado (puntos); en oferta = reducción del precio de mercado
            with np.errstate(divide="ignore", invalid="ignore"):
                e100 = x["dp"] * 100 / x["coste"] if con_coste else np.full(R6.NMC, np.nan)
                e100n = x["neto"] * 100 / x["coste"] if con_coste else np.full(R6.NMC, np.nan)
                cpp = np.where(red > 0, x["coste"] / red, np.nan) if con_coste else np.full(R6.NMC, np.nan)
            e10 = q(x["e10k"])
            if con_coste:
                estado = "estimado (C4)"
            elif inst == "e_ayuda_demanda":
                estado = SIN_BASE["e_alquiler"]
            elif inst == "f2_impuestos_construccion":
                estado = "coste anual igual al de compra (la rebaja es una sola); el efecto en alquiler es indirecto"
            else:
                estado = SIN_BASE[inst]
            dz, cz = q(x["dosis"]), q(x["coste"])
            filas.append(dict(cc=cc, ccaa=R6.NOMBRE[cc], instrumento=inst, nombre=NOMBRE_INSTR[inst], mercado=mer, horizonte=h,
                              dosis_def=DOSIS_DEF[inst], dosis_med=dz[0], dosis_p5=dz[1], dosis_p95=dz[2],
                              dprecio_med=q(x["dp"])[0], dprecio_p5=q(x["dp"])[1], dprecio_p95=q(x["dp"])[2],
                              dneto_med=q(x["neto"])[0], coste_anual_meur_med=cz[0], coste_anual_meur_p5=cz[1], coste_anual_meur_p95=cz[2],
                              coste_10a_meur_med=cz[0] * 10 if con_coste else np.nan, estado_coste=estado,
                              efecto_10k_med=e10[0], efecto_10k_p5=e10[1], efecto_10k_p95=e10[2],
                              efecto_100meur_mercado_med=q(e100)[0], efecto_100meur_mercado_p5=q(e100)[1], efecto_100meur_mercado_p95=q(e100)[2],
                              efecto_100meur_neto_med=q(e100n)[0], efecto_100meur_neto_p5=q(e100n)[1], efecto_100meur_neto_p95=q(e100n)[2],
                              coste_por_punto_meur_med=q(cpp)[0], coste_por_punto_meur_p5=q(cpp)[1], coste_por_punto_meur_p95=q(cpp)[2]))
    t = pd.DataFrame(filas)
    comprobar(t)
    escribir_construccion(pd.DataFrame(rob_a))
    t.round(4).to_csv(OUT / "dosis_coste.csv", index=False)
    escribir(t)


def comprobar(t: pd.DataFrame) -> None:
    im = pd.read_csv(ROOT / "output/v7/R6/impactos.csv", dtype={"cc": str})
    im = im[im.fuente_es == "rejilla"][["cc", "instrumento", "mercado", "horizonte", "dprecio_med", "coste_meur_med"]]
    t = t[t.instrumento != "a_construccion"]   # v7.2: la construcción adicional se reestima con dosis nueva (no reproduce R6)
    im = im[im.instrumento != "a_construccion"]
    m = t.merge(im, on=["cc", "instrumento", "mercado", "horizonte"], suffixes=("", "_r6"))
    assert len(m) == len(t) == len(im), (len(m), len(t), len(im))
    dif = (m.dprecio_med - m.dprecio_med_r6).abs().max()
    difc = (m.coste_anual_meur_med - m.coste_meur_med).abs().max()
    if not (dif < 1e-3 and (np.isnan(difc) or difc < 1e-2)):
        raise SystemExit(f"S1: la reproducción de R6 no coincide (precio {dif}, coste {difc})")


def robustez_construccion(cc, v, b) -> list[dict]:
    """v7.2: mismo criterio que R6 (V18) para la construcción adicional con la dosis nueva: el esfuerzo (= precio en oferta) baja en
    TODAS las extracciones y horizontes, el p95 y el máximo a 10 años son < -0,1 % y el precio de mercado no sube (p95 <= 0)."""
    out = []
    for mer in ("precio", "alquiler"):
        x = {h: v[("a_construccion", mer, h)]["dp"] for h in R6.HOR}
        ok = (all(float(np.max(x[h])) < 0 for h in R6.HOR) and float(np.percentile(x[10], 95)) < R6.UMBRAL
              and float(np.max(x[10])) < R6.UMBRAL and all(float(np.percentile(x[h], 95)) <= 1e-9 for h in R6.HOR))
        for h in R6.HOR:
            d = v[("a_construccion", mer, h)]
            out.append(dict(cc=cc, ccaa=R6.NOMBRE[cc], instrumento="a_construccion", mercado=mer, horizonte=h, fuente_es="rejilla",
                            visados_2025=float(b.vis_2025), visados_max_2007_2025=float(b.vis_max_0725),
                            dosis_anual_max=float(min(b.N_anual_central, max(b.vis_max_0725 - b.vis_2025, 0.0))),
                            necesidad_anual_T3=float(b.N_anual_central), capacidad_observada=float(max(b.vis_max_0725 - b.vis_2025, 0.0)),
                            dosis_med=float(np.median(d["dosis"])), dprecio_med=float(np.median(d["dp"])),
                            dprecio_p5=float(np.percentile(d["dp"], 5)), dprecio_p95=float(np.percentile(d["dp"], 95)),
                            esfuerzo_max=float(np.max(d["dp"])), robusto=bool(ok)))
    return out


def escribir_construccion(r: pd.DataFrame) -> None:
    o = ROOT / "output" / "v7_2" / "construccion"
    o.mkdir(parents=True, exist_ok=True)
    r.round(4).to_csv(o / "impactos_construccion.csv", index=False)
    r10 = r[r.horizonte == 10]
    L = ["# V7.2 · Construcción adicional con dosis no nula (escenario condicional, C4)", "",
         "Misma fórmula, semilla, extracciones y rejilla de elasticidades que R6. Solo cambia la dosis: 50-100 % del mínimo entre la necesidad "
         "anual central de T3 (v5.1) y la capacidad observada de construcción (máximo anual de visados 2007-2025 menos visados de 2025). En R6 la "
         "capacidad se medía con el máximo de 2016-2025 y la dosis era 0 en 14 de 17 CCAA. El máximo de 2007-2025 incluye el auge de 2007-2008: "
         "es una capacidad generosa, que acota por arriba.", "",
         "| CCAA | necesidad anual T3 | capacidad observada | dosis anual máx. | mercado | Δ precio 10 años: mediana [p5, p95] | robusto |",
         "|---|---|---|---|---|---|---|"]
    for x in r10.itertuples():
        L.append(f"| {x.ccaa} | {x.necesidad_anual_T3:,.0f} | {x.capacidad_observada:,.0f} | {x.dosis_anual_max:,.0f} | "
                 f"{'compra' if x.mercado == 'precio' else 'alquiler'} | {x.dprecio_med:.2f} % [{x.dprecio_p5:.2f}; {x.dprecio_p95:.2f}] | {'sí' if x.robusto else 'no'} |"
                 .replace(",", "X").replace(".", ",").replace("X", "."))
    L += ["", f"Robusta en compra en {int(r10[r10.mercado == 'precio'].robusto.sum())} de 17 CCAA y en alquiler en "
          f"{int(r10[r10.mercado == 'alquiler'].robusto.sum())} de 17 (criterio V18 de R6). Escenario condicional: no es un efecto estimado.", ""]
    (o / "resumen.md").write_text("\n".join(L), encoding="utf-8")


def nac(t, inst, mer, col, h=10):
    x = t[(t.instrumento == inst) & (t.mercado == mer) & (t.horizonte == h)][col].dropna()
    return (float(x.median()), float(x.min()), float(x.max())) if len(x) else (np.nan, np.nan, np.nan)


def escribir(t: pd.DataFrame) -> None:
    t10 = t[t.horizonte == 10]
    L = ["# V7.1-S1 · Dosis, coste fiscal y normalización de los instrumentos de R6 (capa C4)", "",
         "Escenarios condicionales («si se hiciera X, con estos supuestos…»), no efectos identificados. Se reproducen las extracciones de "
         "Monte Carlo de R6 (v7) con la misma semilla; la variación de precio coincide con output/v7/R6/impactos.csv (comprobado en el script). "
         "Se evalúan instrumentos, no actores.", "",
         "**Nota de lectura (C4).** El signo lo fija en gran parte la fórmula de incidencia: los instrumentos de cantidad bajan el precio "
         "(Δp/p = −(ΔQ/Q)/(εs+|εd|)) y las ayudas a la demanda lo suben (Δp/p = s·|εd|/(εs+|εd|)). Lo informativo son las magnitudes "
         "relativas entre instrumentos y CCAA, condicionadas a la rejilla de elasticidades de v5 (la regional no es utilizable en ninguna CCAA).", "",
         "## Definiciones", "",
         "- **Dosis**: cantidad a la que se aplica el instrumento (ver tabla). Horizonte: 2, 5 y 10 años; los titulares son a 10 años.",
         "- **Coste fiscal anual** (M€/año, sin efectos inducidos ni descuento): e y f1 = s × compraventas 2025 × 90 m² × valor tasado 2025T4 (como en R6); "
         "f2 = rebaja del coste × cuota del coste × visados 2025 × 90 m² × valor tasado. Coste a 10 años = 10 × anual.",
         "- **Efecto por 10.000 viviendas** (instrumentos de cantidad): variación del precio (puntos %) por cada 10.000 viviendas de dosis acumulada.",
         "- **Efecto por 100 M€ anuales** (instrumentos con coste): variación del precio de mercado y del precio neto pagado por el beneficiario por cada 100 M€/año.",
         "- **Coste por punto**: M€ anuales por punto porcentual de reducción del precio neto pagado (en f2, del precio de mercado). En e y f1 el precio "
         "de mercado SUBE: el coste por punto se refiere solo al beneficiario.",
         "- **Regla de lectura para los instrumentos de cantidad** (sin coste estimable): si el coste por vivienda fuera u euros, el efecto por "
         "100 M€ sería «efecto por 10.000 viviendas × 10.000 / u». No se publica ningún u: no hay base verificada.", "",
         "## Resumen nacional (mediana entre CCAA y rango entre CCAA, 10 años, rejilla)", "",
         "| Instrumento | Mercado | Dosis (mediana CCAA) | Δ precio de mercado (%) | Coste anual (M€) | Efecto por 10.000 viv. (pp) | Efecto por 100 M€/año en precio de mercado (pp) | Coste por punto (M€/año) |",
         "|---|---|---|---|---|---|---|---|"]
    for inst in NOMBRE_INSTR:
        for mer in ("precio", "alquiler"):
            g = t10[(t10.instrumento == inst) & (t10.mercado == mer)]
            if g.empty:
                continue
            dp, cs, e10, e100, cpp = (nac(t, inst, mer, c) for c in ("dprecio_med", "coste_anual_meur_med", "efecto_10k_med",
                                                                     "efecto_100meur_mercado_med", "coste_por_punto_meur_med"))
            f = (lambda x, k=2: "—" if np.isnan(x[0]) else f"{x[0]:.{k}f} [{x[1]:.{k}f}; {x[2]:.{k}f}]")
            cst = f(cs, 0) if not np.isnan(cs[0]) else ("no estimable" if not g.estado_coste.iloc[0].startswith("coste anual") else "(el de compra)")
            L.append(f"| {NOMBRE_INSTR[inst]} | {'compra' if mer == 'precio' else 'alquiler'} | {g.dosis_med.median():,.0f} | {f(dp)} | {cst} | "
                     f"{f(e10, 3)} | {f(e100, 3)} | {f(cpp, 0)} |".replace(",", "X").replace(".", ",").replace("X", "."))
    L += ["", "Rango entre corchetes: mínimo y máximo de las medianas de las 17 CCAA. El rango p5-p95 de cada CCAA está en dosis_coste.csv.", "",
          "## Dosis por instrumento", "", "| Instrumento | Dosis | Coste |", "|---|---|---|"]
    for inst in NOMBRE_INSTR:
        g = t10[(t10.instrumento == inst) & (t10.mercado == "precio")]
        est = g.estado_coste.iloc[0] + ("; en alquiler, " + SIN_BASE["e_alquiler"] if inst == "e_ayuda_demanda" else "")
        L.append(f"| {NOMBRE_INSTR[inst]} | {DOSIS_DEF[inst]} | {est} |")
    L += ["", "## Lectura", "",
          "- Los instrumentos de cantidad no tienen coste fiscal estimable con base versionada: se comparan por su dosis y su efecto por "
          "10.000 viviendas, no por euro.",
          "- En compra, el efecto por 10.000 viviendas es el MISMO para vacías, vivienda pública y turísticos en cada CCAA (la fórmula solo depende del "
          "parque y de las elasticidades). Lo que los distingue es la dosis y, en alquiler, la fracción que llega al alquiler. Del mismo modo, el efecto "
          "por 100 M€ en el precio de mercado es idéntico para las ayudas a la demanda y la rebaja de ITP/IVA: ambos son una intensidad s sobre el mismo "
          "valor de compras. Son propiedades de la fórmula, no hallazgos.",
          "- Las ayudas a la demanda y la rebaja de ITP/IVA reducen el precio neto del beneficiario, pero suben el precio de mercado para el resto. "
          "Su coste por punto es de reducción del precio neto, no del precio de mercado.",
          "- La rebaja de impuestos y costes de construcción es NO DIFUNDIBLE (v7.2): su escenario sobrestima el efecto por diseño (R6 traslada la "
          "rebaja al precio de todo el mercado, mientras que el coste fiscal solo cubre la obra nueva). Sus filas se conservan para trazabilidad.",
          "- Construcción adicional (v7.2): la dosis de R6 era 0 en la mayoría de las CCAA porque medía la capacidad con el máximo de visados de "
          "2016-2025. Desde v7.2 la dosis es el mínimo entre la necesidad anual de T3 y la capacidad observada con el máximo de 2007-2025 "
          "(output/v7_2/construccion/resumen.md); es una capacidad generosa, que incluye el auge de 2007-2008.",
          "- Todo es C4: los parámetros son supuestos de la rejilla. No se recomienda ningún instrumento; se comparan magnitudes condicionales.", ""]
    (OUT / "resumen.md").write_text("\n".join(L), encoding="utf-8")
    hechos = []
    for inst in NOMBRE_INSTR:
        for mer in ("precio", "alquiler"):
            if t10[(t10.instrumento == inst) & (t10.mercado == mer)].empty:
                continue
            mlab = "compra" if mer == "precio" else "alquiler"
            for col, ind, uni in (("efecto_10k_med", "Variación del precio por cada 10.000 viviendas", "puntos %"),
                                  ("efecto_100meur_mercado_med", "Variación del precio de mercado por cada 100 M€ anuales", "puntos %"),
                                  ("coste_anual_meur_med", "Coste fiscal anual aproximado", "M€/año"),
                                  ("coste_por_punto_meur_med", "Coste anual por punto de reducción del precio neto pagado", "M€/año por punto")):
                v = nac(t, inst, mer, col)
                if np.isnan(v[0]):
                    continue
                hechos.append(dict(id=f"V71-S1-{inst}-{mlab}-{col.replace('_med', '')}",
                                   indicador=f"{ind}, {NOMBRE_INSTR[inst]}, {mlab}, 10 años (mediana entre CCAA; rango entre CCAA)",
                                   valor=v[0], min=v[1], max=v[2], unidad=uni, periodo="2026-2036 (escenario)", cobertura="17 CCAA",
                                   fuentes="R6 v7 (rejilla A4 v5; T3 v5.1; R4 v7); panel_ccaa_q_v7", capa="C4", fecha_dato=FECHA,
                                   sentido_min_max="mínimo y máximo de las medianas de las 17 CCAA"))
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1), encoding="utf-8")
    res = dict(rama="V7.1-S1", pregunta="Dosis, coste y efecto normalizado de los instrumentos de R6", capa="C4",
               datos="output/v7/R6 (reproducido); panel_ccaa_q_v7", N=17, metodo="contabilidad sobre las extracciones de Monte Carlo de R6 (4.000 por CCAA)",
               estimacion=None, ic95=None, p_ajustado=None, nivel_evidencia="EXPLORATORIO", diagnosticos="reproducción de impactos.csv < 1e-3",
               fuera_muestra=dict(modelo=None, rmse=None, dm_vs_ar4=None),
               notas="Sin análisis nuevo; costes de oferta no estimables sin base; signos dados por la fórmula de incidencia.")
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()

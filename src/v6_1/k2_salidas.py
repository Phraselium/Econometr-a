"""K2 (v6.1): salidas. Tablas en markdown, registro con Holm/BH, resultado.json, hechos.json y texto para entregables."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

import k2_lib as kl

FECHA = "2026-10-11"


def _f(x, d=2):
    return "n/d" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{d}f}".replace(".", ",")


def _md(df):
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(out)


def _ic(r):
    return f"{_f(r['coef'])} [{_f(r['lo'])}; {_f(r['hi'])}]"


def escribir(U, meta, CTX, FILAS, cadena, col, dem, bma, REG, OUT, smoke):
    df = pd.DataFrame(FILAS)
    df["p_holm"] = np.nan
    df["p_bh"] = np.nan
    for bl, g in df.groupby("bloque"):
        pp = {r["id"]: r["p"] for _, r in g.iterrows() if pd.notna(r["p"])}
        df.loc[g.index, "p_holm"] = g["id"].map(kl.holm_dict(pp))
        df.loc[g.index, "p_bh"] = g["id"].map(kl.bh_dict(pp))
    pg = {r["id"]: r["p"] for _, r in df.iterrows() if pd.notna(r["p"])}
    df["p_holm_global"] = df["id"].map(kl.holm_dict(pg))
    df.to_csv(OUT / "registro_holm.csv", index=False)
    df[df["bloque"] == "inmigracion"].to_csv(OUT / "pasos_inmigracion.csv", index=False)
    inm = df[df["bloque"] == "inmigracion"]
    n_spec = len(df)

    def g(paso, mk, via=None, col_="coef"):
        s = df[(df["paso"] == paso) & (df["mercado"] == mk)]
        if via:
            s = s[s["via"] == via]
        return s.iloc[0] if len(s) else None

    # ------------------------------------------------------------ inmigracion.md
    ac = inm[inm["via"] == "acumulado"].copy()
    ac["cambio_por_paso"] = ac["coef"] - ac["coef_anterior_misma_muestra"]
    t1 = ac.assign(coef_ic95=ac.apply(_ic, axis=1), p=ac["p"].map(lambda v: _f(v, 3)),
                   anterior=ac["coef_anterior_misma_muestra"].map(_f), cambio=ac["cambio_por_paso"].map(_f),
                   F1=ac["F1"].map(lambda v: _f(v, 1)), p_holm=ac["p_holm"].map(lambda v: _f(v, 3)))[
        ["paso", "mercado", "medida", "periodo", "N", "coef_ic95", "p", "p_holm", "anterior", "cambio", "F1"]]
    ud = inm[inm["via"] == "una_dimension"].copy()
    ud["cambio"] = (ud["coef"] - ud["coef_anterior_misma_muestra"]).map(_f)
    t2 = ud.assign(coef_ic95=ud.apply(_ic, axis=1), p=ud["p"].map(lambda v: _f(v, 3)),
                   base_misma_muestra=ud["coef_anterior_misma_muestra"].map(_f),
                   p_holm=ud["p_holm"].map(lambda v: _f(v, 3)))[
        ["dimension", "paso", "mercado", "medida", "nivel", "periodo", "N", "coef_ic95", "p", "p_holm", "base_misma_muestra", "cambio"]]
    cor = [("cuota (t-1) y ln poblacion (t-1), panel v6, conjunta", col["v6_share_vs_ln_pob"]["pooled"]),
           ("idem, entre provincias", col["v6_share_vs_ln_pob"]["entre"]),
           ("idem, dentro de provincia (EF dobles)", col["v6_share_vs_ln_pob"]["dentro"]),
           ("VIF cuota y ln poblacion (EF dobles)", col["v6_vif_share_pob"]["l1_share_ext_pob"]),
           ("VIF cuota con el nucleo de M2", col["v6_vif_nucleo"]["l1_share_ext_pob"]),
           ("VIF ln poblacion con el nucleo de M2", col["v6_vif_nucleo"]["l1_ln_pob"]),
           ("flujo/poblacion (base v2) y ln poblacion, dentro", col["v2_flujo_vs_ln_pob"]["dentro"]),
           ("variacion del stock y ln poblacion, dentro", col["v2_dstock_vs_ln_pob"]["dentro"]),
           ("cuota y compras de extranjeros residentes (MIVAU), conjunta / entre / dentro",
            f"{_f(col['corr_cuota_compra_ext_residentes']['pooled'])} / {_f(col['corr_cuota_compra_ext_residentes']['entre'])} / {_f(col['corr_cuota_compra_ext_residentes']['dentro'])}"),
           ("cuota y costa (entre, 38 provincias)", col["corr_cuota_costa"]["entre"]),
           ("cuota y vivienda no principal 2021 (Censo, entre)", col["corr_cuota_no_principal"]["entre"]),
           ("cuota y no residentes 2015-2016 (R1A, entre)", col["corr_cuota_no_residentes_1516"]["entre"])]
    t3 = pd.DataFrame([(a, _f(b) if not isinstance(b, str) else b) for a, b in cor], columns=["medida", "valor"])
    de = inm[inm["via"] == "demanda_externa"].copy()
    de["k"] = de["paso"].str.split("|")
    de["medida_"] = de["k"].str[0]
    de["controles_base"] = de["k"].str[1]
    de["externa"] = de["k"].str[2]
    de["coef_ic95"] = de.apply(_ic, axis=1)
    de["p"] = de["p"].map(lambda v: _f(v, 3))
    de["p_holm"] = de["p_holm"].map(lambda v: _f(v, 3))
    de["abs"] = de.apply(lambda r: f"{_f(r['coef_abs'], 1)} {r['unidad_abs']}", axis=1)
    t4 = de[["medida_", "controles_base", "externa", "N", "coef_ic95", "abs", "p", "p_holm"]]
    tb = pd.DataFrame([(f"{k[0]} | {k[1]}", _f(v["pip"], 3), _f(v["media"], 2), _f(v["pip_pob"], 2), v["N"], v["modelos"])
                       for k, v in bma.items()], columns=["mercado | conjunto", "PIP cuota (BIC)", "media posterior %/pp",
                                                        "PIP poblacion", "N", "modelos"])

    c_comp = g("P8", "compra")
    c_comp_sin = c_comp["coef_anterior_misma_muestra"]
    c_alq = g("P8", "alquiler")
    sd = lambda m, c, e: de[(de["medida_"] == m) & (de["controles_base"] == c) & (de["externa"] == e)].iloc[0]  # noqa: E731
    cs0, cs1 = sd("valor tasado MIVAU", "sin_controles", "sin_externa"), sd("valor tasado MIVAU", "sin_controles", "costa+no_principal+compras_ext")
    cp0, cp1 = sd("valor tasado MIVAU", "con_nucleo", "sin_externa"), sd("valor tasado MIVAU", "con_nucleo", "costa+no_principal+compras_ext")
    as0, as1 = sd("SERPAVI VC (stock)", "sin_controles", "sin_externa"), sd("SERPAVI VC (stock)", "sin_controles", "costa+no_principal+compras_ext")
    ap0, ap1 = sd("SERPAVI VC (stock)", "con_nucleo", "sin_externa"), sd("SERPAVI VC (stock)", "con_nucleo", "costa+no_principal+compras_ext")
    p0a, p0c = g("P0", "alquiler"), g("P0", "compra")
    p1a, p1c = g("P1", "alquiler"), g("P1", "compra")
    p6a = g("P6", "alquiler")
    ser = g("medida_alq_SERPAVI_muestra_comun", "alquiler")
    ipc = g("medida_alq_IPC_muestra_comun", "alquiler")
    reg = g("medida_precio_registradores", "compra")
    tas = g("medida_precio_tasado_real", "compra")
    ipv = g("medida_precio_ipv_ine", "compra")
    co = col
    concl = (
        f"Con los datos de entrenamiento (provincias de entrenamiento de v6; {meta['n_v2']} con datos de v2) la asociación de la inmigración con el "
        f"precio de compra y con el alquiler de stock **no tiene un signo ni un orden entre mercados estables**: cambia con el método, con la "
        f"medida de alquiler y con el control por población (que puede ser mediador o término mecánico de la inmigración y estima otra magnitud). "
        f"(1) Método: la base de v2 (flujo/población, 2SLS shift-share, 2009-2021) da {_ic(p0a)} %/pp en alquiler (IPC) y {_ic(p0c)} en valor "
        f"tasado; con MCO y los mismos EF da {_ic(p1a)} y {_ic(p1c)}: el orden alquiler > compra de v2 corresponde al 2SLS y el orden compra > alquiler de v6 al MCO "
        f"(ya presente en la columna MCO de v2). La primera etapa en estas provincias es débil (F = {_f(p0a['F1'], 1)} frente a 14,4 en las 49 provincias de v2; "
        f"las 11 provincias selladas de v6 no se usan). "
        f"(2) Población (sensibilidad, en pie de igualdad con la lectura sin población; no prueba que la cuota no importe): la cuota de extranjeros (t-1) y el ln de la población (t-1) se correlacionan {_f(co['v6_share_vs_ln_pob']['dentro'])} dentro de provincia "
        f"({_f(co['v6_share_vs_ln_pob']['pooled'])} en conjunta); al añadir la población, el coeficiente sobre el valor tasado pasa de {_f(c_comp_sin)} a "
        f"{_f(c_comp['coef'])} %/pp (IC95 [{_f(c_comp['lo'])}; {_f(c_comp['hi'])}]) y el de SERPAVI de {_f(c_alq['coef_anterior_misma_muestra'])} a {_f(c_alq['coef'])}. "
        f"(3) Medida de alquiler: en la muestra común 2012-2021 el coeficiente es {_ic(ser)} con SERPAVI y {_ic(ipc)} con IPC. "
        f"(4) Demanda externa: sin población, los controles costa×año, vivienda no principal×año y compras de extranjeros residentes (MIVAU) reducen el coeficiente "
        f"de {_f(cs0['coef'])} a {_f(cs1['coef'])} %/pp (valor tasado) y de {_f(as0['coef'])} a {_f(as1['coef'])} (SERPAVI), compatible con que la cuota recoja en parte "
        f"provincias de costa; con población (o con el núcleo de M2) el coeficiente apenas cambia ({_f(cp0['coef'])} a {_f(cp1['coef'])} en valor tasado; {_f(ap0['coef'])} a {_f(ap1['coef'])} en SERPAVI). "
        f"Las tres provincias insulares están en la parte sellada de v6, así que las islas no se pueden contrastar. "
        f"Con el BMA aproximado (BIC) la probabilidad de inclusión de la cuota es {_f(bma[('compra', 'nucleo_M2')]['pip'], 2)} en compra y {_f(bma[('alquiler', 'nucleo_M2')]['pip'], 2)} en alquiler "
        f"(v6/M2: 0,77 y 0,06), pero la media posterior en compra es {_f(bma[('compra', 'nucleo_M2')]['media'], 2)} %/pp: una inclusión alta no implica signo positivo. "
        f"**Capa C4; veredicto «ANALIZADA, NO CONCLUYENTE»; asociación, sin lectura causal.**")
    CTX["concl"] = concl
    FSEC = f'''## F. Qué dimensión mueve el resultado entre v1-v3 y v6
Aviso sobre la población: la inmigración aumenta la población (es componente del flujo y denominador de la cuota), de modo que la población puede ser mediadora o un término mecánico. Controlar por ella estima otra magnitud y puede absorber el canal; no prueba que la cuota no importe. Las lecturas sin y con población se presentan en pie de igualdad (paso P8 y tabla D).
Dimensiones que se pueden afirmar sin esa salvedad:
1. **Método** (2SLS frente a MCO): invierte el orden entre mercados (paso P1: cambio {_f(p1a['coef'] - p0a['coef'])} en alquiler y {_f(p1c['coef'] - p0c['coef'])} en compra).
2. **Medida de alquiler** (IPC frente a SERPAVI): multiplica el coeficiente en alquiler por {_f(ser['coef'] / ipc['coef'], 1)} en la muestra común.
3. Definición (flujo, stock, cuota), periodo, nivel y fuente de datos (v2/v6, idénticas: r≈1) mueven la magnitud pero no explican el cambio de orden. Medida de precio en 2016-2021: valor tasado {_ic(tas)}, Registradores {_ic(reg)}, IPV {_ic(ipv)} (intervalos solapados).
Sensibilidad (otra magnitud, no «la dimensión principal»): al añadir la población el coeficiente sobre el valor tasado pasa de {_f(c_comp_sin)} a {_f(c_comp['coef'])} y el de SERPAVI se anula; ambas lecturas son compatibles con los datos.

'''
    txt = f"""# K2 · Inmigración: análisis de especificación «una dimensión cada vez» (v6.1)

Fecha del dato: {FECHA}. Capa **C4** (exploratorio, asociación; nada causal). Script: `src/v6_1/k2_inmigracion.py` (SEED 20261010, un hilo, sin red).
medida_precio: valor tasado MIVAU por defecto; las demás se declaran en cada fila. Alquiler: stock (IPC, SERPAVI); los contratos nuevos (fianzas) no entran (N≈15 en entrenamiento). {n_spec} especificaciones registradas en `registro.csv`; Holm y BH dentro de cada bloque en `registro_holm.csv`.

## Datos y supuestos
- Muestra: las 41 provincias de entrenamiento de v6 (output/v6/M0/paneles) y, para los datos de v2, las 38 que coinciden con el entrenamiento de v2 (2002-2023). Las 11 provincias selladas de v6 no se usan, así que **no se reproduce exactamente la muestra de 49 provincias de v2** (BI publicado: alquiler 3,06 [1,14; 4,98], compra −1,04 [−6,08; 4,00], F 14,4).
- CCAA y nacional son series publicadas (v1) que agregan todas las provincias; se usan solo descriptivamente. No hay dato municipal de extranjeros en data/processed: en municipio se une la variable provincial (pseudo-replicación; cluster provincia).
- Unidades: % de variación (o de nivel) de la medida por +1 pp del regresor; en €/mes y €/m² con el alquiler medio SERPAVI ({_f(meta['renta_media'], 0)} €/mes) y el precio medio tasado ({_f(meta['precio_medio'], 0)} €/m²) del panel. IC95 con t(G−1), errores agrupados por provincia (por CCAA con IPV).
- Notariado: solo hay panel de la Comunitat Valenciana (3 provincias) en data/processed, sin panel provincial: no entra. IPV del INE es de CCAA.
- La probabilidad de inclusión (PIP) es una aproximación con BIC sobre datos con EF; reproduce la de v6/M2 (núcleo) pero no es idéntica (g-prior).

## A. Camino acumulado: de la base de v2 (BI) a la especificación de v6 (M2)
Cada fila cambia una dimensión respecto de la anterior; «anterior» es el coeficiente del paso previo estimado en la misma muestra (salvo cuando cambia el periodo).

{_md(t1)}

## B. Una dimensión cada vez desde la base MCO (EF provincia y año, flujo, IPC / valor tasado real, 2009-2021)
«base_misma_muestra» es la base estimada en las filas válidas para ambas especificaciones.

{_md(t2)}

## C. Colinealidad con la población y con la demanda externa
{_md(t3)}

## D. ¿La cuota capta provincias de demanda externa? Cuota (t-1) en niveles, EF dobles (v6)
`controles_base`: sin controles, con ln población o con el núcleo de M2. `externa`: costa×año, vivienda no principal 2021×año (Censo), compras de extranjeros residentes (MIVAU, t-1), no residentes 2015-2016 (R1A) y combinaciones. Islas: 0 provincias insulares en entrenamiento (07, 35 y 38 están selladas). Filas `pooled` (sin EF de provincia, EF de año) y `FD` (primeras diferencias) al final.

{_md(t4)}

## E. BMA aproximado (BIC)
{_md(tb)}

{FSEC}## G. Conclusión única (C4)
{concl}
"""
    (OUT / "inmigracion.md").write_text(txt)

    # ------------------------------------------------------------ otros_cambios.md
    ot = df[df["bloque"] == "otros"].copy()
    ot["coef_ic95"] = ot.apply(_ic, axis=1)
    ot["p"] = ot["p"].map(lambda v: _f(v, 3))
    ot["anterior"] = ot["coef_anterior_misma_muestra"].map(_f)
    ot["p_holm"] = ot["p_holm"].map(lambda v: _f(v, 3))
    sec = ["# K2 · Otras conclusiones que cambiaron de signo o de mercado (v6.1)", "",
           f"Fecha del dato: {FECHA}. C4 en todas las filas; «ANALIZADA, NO CONCLUYENTE»; asociación, sin lectura causal. Cadenas ligeras, una dimensión cada vez, "
           "paso anterior en la misma muestra. Unidad: % de la medida por +10 % (niveles) o +10 pp de crecimiento anual (diferencias) de la variable; "
           "turísticos: +10 % de viviendas turísticas (t-1). Muestra: provincias de entrenamiento de v6. Holm por bloque.", ""]
    guia = {"empleo": "Empleo (ocupados). v1: DOLS con empleo +1,48 (nacional, precio real, output/informe.md); v2/BV: crecimiento de ocupados +0,044 en compra (output/v2/BV); v6/M1b: efectos fijos −1,23 % (p WCB 0,49) y v6/M2: PDS +4,16 % (output/v6/M1B, M2).",
            "renta": "Renta (PIB por habitante). v6/M1b: +1,34 % (p 0,13); v6/M2: PIP compra 0,84 y alquiler 0,10; mediana del multiverso −0,05 % (output/v6/M2).",
            "iniciadas": "Iniciadas libres en alquiler. v6/M1a: −0,17 €/mes por 1.000 (2021-2023) y +2,21 (2016-2023); v6/M2: PIP en alquiler 0,97 (núcleo) y 0,09 (completo) (output/v6/M1A, M2).",
            "turisticos": "Turísticos (VUT). v3/C1: +0,0003 por 100 viviendas (sección, no concluyente); v3/GL: −0,0042 (Barcelona); v6/M1a: −1,58 €/mes por 1.000 (provincia, 2021-2023) (output/v3/C1, GL; v6/M1A)."}
    for nom in ["empleo", "renta", "iniciadas", "turisticos"]:
        o = ot[ot["via"] == nom][["paso", "dimension", "mercado", "medida", "nivel", "periodo", "N", "coef_ic95", "p", "p_holm", "anterior"]]
        sec += [f"## {nom.capitalize()}", "", guia[nom], "", _md(o), ""]
    bo = CTX["bma_otros"]
    filas_b = []
    for mk in ("compra", "alquiler"):
        for v, d in bo[mk]["res"].items():
            filas_b.append((mk, v, _f(d["pip"], 2), _f(d["media"], 2)))
    sec += ["## BMA aproximado (BIC), núcleo de M2", "", _md(pd.DataFrame(filas_b, columns=["mercado", "variable", "PIP", "media posterior"])), "",
            "## Lectura", "",
            "- Los signos de empleo, renta e iniciadas cambian al pasar de diferencias a niveles con EF y al añadir el núcleo de controles (población incluida): ninguno es estable entre pasos con IC95 que excluya 0 en la especificación final.",
            "- Turísticos: ningún paso tiene IC95 que excluya 0; el signo cambia entre medida de alquiler, método y nivel.",
            "- El cambio de mercado (alquiler frente a compra) y de signo entre versiones coincide con cambios de medida (IPC, SERPAVI; valor tasado), de método y de controles, no con un resultado estable."]
    (OUT / "otros_cambios.md").write_text("\n".join(sec) + "\n")

    # ------------------------------------------------------------ que_cambio.md
    qc = f"""## Qué cambió entre versiones y por qué

Las versiones v1-v3 y v6 no estiman la misma asociación de la inmigración con la vivienda. Esta sección compara las especificaciones, una dimensión cada vez, sobre las provincias de entrenamiento (C4; datos de 2009-2023; fecha {FECHA}).

**Inmigración.** En v2 el flujo de inmigración, instrumentado con cuotas de 2002, se asociaba más con el alquiler (IPC) que con el precio de compra. En v6 la cuota de extranjeros tiene probabilidad de inclusión alta en compra (0,77) y baja en alquiler (0,06). Al repetir la comparación, el orden depende del método: con 2SLS el coeficiente es {_f(p0a['coef'])} %/pp en alquiler y {_f(p0c['coef'])} en valor tasado; con MCO, {_f(p1a['coef'])} y {_f(p1c['coef'])}. Como sensibilidad, la población (puede ser mediadora o término mecánico de la inmigración, así que estima otra magnitud y no prueba que la cuota no importe; ambas lecturas son compatibles con los datos), correlacionada {_f(co['v6_share_vs_ln_pob']['dentro'])} con la cuota dentro de cada provincia, cambia el signo del coeficiente en compra ({_f(c_comp_sin)} a {_f(c_comp['coef'])} %/pp) y lo anula en alquiler. La medida de alquiler también importa: en la misma muestra, {_f(ser['coef'])} con SERPAVI y {_f(ipc['coef'])} con IPC. Los controles de costa, vivienda no principal y compras de extranjeros residentes reducen el coeficiente sin población ({_f(cs0['coef'])} a {_f(cs1['coef'])} en compra), compatible con que la cuota recoja en parte provincias de costa; las islas no se pueden contrastar porque están en la muestra sellada. Una probabilidad de inclusión alta no implica signo positivo: la media posterior en compra es {_f(bma[('compra', 'nucleo_M2')]['media'], 2)} %/pp.

**Otros cambios.** Empleo, renta, iniciadas y turísticos cambian de signo o de mercado según la medida de alquiler, el método y los controles; ningún intervalo de la especificación final excluye el cero.

**Conclusión (C4, «ANALIZADA, NO CONCLUYENTE»).** Las diferencias entre versiones se explican por cambios de método, de controles y de medida, no por un resultado estable que se haya invertido. No se puede afirmar un efecto de la inmigración sobre el precio o el alquiler. Limitación: no se reproduce la muestra de 49 provincias de v2 (primera etapa débil en las provincias de entrenamiento).
"""
    (OUT / "que_cambio.md").write_text(qc)

    # ------------------------------------------------------------ hechos.json y resultado.json
    per = "2016-2024 (compra), 2016-2023 (alquiler)"

    def hecho(i, ind, r, unidad, cob, extra_src=None):
        return dict(id=i, indicador=ind, valor=round(float(r["coef"]), 3), min=round(float(r["lo"]), 3), max=round(float(r["hi"]), 3),
                    unidad=unidad, periodo=per, cobertura=f"{int(r['N'])} observaciones provincia-año; {cob}",
                    fuentes=["output/v6_1/K2/registro_holm.csv", "output/v6/M0/paneles/prov_compra_anual_train.csv.gz"],
                    capa="C4", fecha_dato=FECHA)
    u = "% por pp"  # v6.2: unidad corta (por +1 punto porcentual de cuota de extranjeros en t-1)
    hechos = [
        hecho("K2-CUOTA-COMPRA-SIN", "Cuota de extranjeros (t-1) y valor tasado MIVAU, EF dobles, con nucleo de controles (poblacion incluida), sin controles de demanda externa", cp0, u, "medida_precio: valor tasado MIVAU"),
        hecho("K2-CUOTA-COMPRA-EXT", "Idem con controles de demanda externa (costa x anio, vivienda no principal x anio, compras de extranjeros residentes)", cp1, u, "medida_precio: valor tasado MIVAU"),
        hecho("K2-CUOTA-COMPRA-SINPOB-SIN", "Cuota de extranjeros (t-1) y valor tasado MIVAU, EF dobles, sin controles (sin poblacion) y sin demanda externa", cs0, u, "medida_precio: valor tasado MIVAU"),
        hecho("K2-CUOTA-COMPRA-SINPOB-EXT", "Idem sin poblacion, con controles de demanda externa", cs1, u, "medida_precio: valor tasado MIVAU"),
        hecho("K2-CUOTA-ALQ-SINPOB-SIN", "Cuota de extranjeros (t-1) y alquiler de stock SERPAVI, EF dobles, sin controles y sin demanda externa", as0, u, "alquiler de stock SERPAVI"),
        hecho("K2-CUOTA-ALQ-SINPOB-EXT", "Idem con controles de demanda externa", as1, u, "alquiler de stock SERPAVI"),
        hecho("K2-CUOTA-ALQ-NUCLEO-SIN", "Cuota de extranjeros (t-1) y alquiler SERPAVI, EF dobles, con nucleo (poblacion incluida), sin demanda externa", ap0, u, "alquiler de stock SERPAVI"),
        hecho("K2-CUOTA-ALQ-NUCLEO-EXT", "Idem con controles de demanda externa", ap1, u, "alquiler de stock SERPAVI"),
    ]
    for i, ind, v in [("K2-CORR-POB-DENTRO", "Correlacion dentro de provincia (EF dobles) entre la cuota de extranjeros (t-1) y el ln de la poblacion (t-1)", co["v6_share_vs_ln_pob"]["dentro"]),
                      ("K2-CORR-POB-CONJUNTA", "Correlacion conjunta entre la cuota de extranjeros (t-1) y el ln de la poblacion (t-1)", co["v6_share_vs_ln_pob"]["pooled"])]:
        hechos.append(dict(id=i, indicador=ind, valor=round(float(v), 3), min=None, max=None, unidad="correlacion", periodo="2016-2024",
                           cobertura=f"{co['v6_share_vs_ln_pob']['N']} observaciones provincia-año; 41 provincias de entrenamiento",
                           fuentes=["output/v6_1/K2/diag.json"], capa="C4", fecha_dato=FECHA))
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1))
    (OUT / "diag.json").write_text(json.dumps(dict(col=col, bma={f"{k[0]}|{k[1]}": v for k, v in bma.items()}), indent=1, default=str))
    res = dict(
        rama="K2", pregunta="¿Qué dimensión de la especificación explica que la asociación de la inmigración con el precio y el alquiler difiera entre v1-v3 y v6?",
        capa="C4", medida_precio="valor tasado MIVAU (por defecto; Registradores, IPV INE y valor tasado real se contrastan en la tabla B)",
        datos="Provincias de entrenamiento v6 (41; 38 con datos de v2), 2002-2024, output/v6/M0/paneles y data/processed/v2/train; sin data/sealed",
        N=dict(provincia_anio_compra=int(c_comp["N"]), provincia_anio_alquiler=int(c_alq["N"]), especificaciones=int(n_spec)),
        metodo="MCO/2SLS con EF de provincia y año, errores agrupados, una dimensión cada vez; BMA aproximado con BIC; Holm y BH por bloque",
        estimacion=dict(cuota_compra_sin_poblacion=round(float(cs0["coef"]), 3), cuota_compra_con_nucleo=round(float(cp0["coef"]), 3),
                        cuota_compra_con_nucleo_y_demanda_externa=round(float(cp1["coef"]), 3), unidad="% por +1 pp de cuota (t-1)",
                        corr_poblacion_dentro=round(float(co["v6_share_vs_ln_pob"]["dentro"]), 3)),
        ic95=dict(cuota_compra_con_nucleo=[round(float(cp0["lo"]), 3), round(float(cp0["hi"]), 3)],
                  cuota_compra_con_nucleo_y_demanda_externa=[round(float(cp1["lo"]), 3), round(float(cp1["hi"]), 3)]),
        p_ajustado=dict(cuota_compra_con_nucleo_holm=round(float(df.loc[df["id"] == cp0["id"], "p_holm"].iloc[0]), 3), familia=f"{int((df['bloque'] == 'inmigracion').sum())} especificaciones de inmigración"),
        nivel_evidencia="EXPLORATORIO (C4); ANALIZADA, NO CONCLUYENTE; sin lenguaje causal",
        diagnosticos=dict(primera_etapa_F_base_38_provincias=round(float(p0a["F1"]), 2), vif_cuota_poblacion=round(float(co["v6_vif_share_pob"]["l1_share_ext_pob"]), 2),
                          pip_bic_compra=round(float(bma[("compra", "nucleo_M2")]["pip"]), 3), pip_bic_alquiler=round(float(bma[("alquiler", "nucleo_M2")]["pip"]), 3),
                          islas_en_entrenamiento=meta["islas_en_train"], dimension_que_mueve="método (2SLS/MCO) y control por población; medida de alquiler"),
        fuera_muestra=dict(modelo=None, rmse=None, dm_vs_ar4=None),
        notas=["K2 no usa evaluación sellada ni predicción: fuera_muestra no aplica.",
               "No se reproduce la muestra de 49 provincias de v2 (las 11 provincias selladas de v6 no se usan); primera etapa débil en las provincias de entrenamiento.",
               "Notariado sin panel provincial; IPV solo CCAA; municipio con regresor provincial unido.",
               "Conclusión: " + concl.replace("**", "")])
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    (OUT / "registro.csv").parent.mkdir(exist_ok=True, parents=True)
    REG.flush()

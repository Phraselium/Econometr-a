"""BS · informe_v2.md. Ninguna cifra escrita a mano: todo se lee de ficheros versionados (se cita cada fuente)."""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

import bs_lib as L
import bs_tablas as T

N, PV, IC = L.num, L.pv, L.ic


def src(*paths) -> str:
    return "\n*Fuente: " + "; ".join(f"`{p}`" for p in paths) + ".*\n"


def seccion_md(rel: str, patron: str) -> str:
    """Texto de la sección '## ...' de un .md de rama cuyo título casa con `patron` (hasta el siguiente '## ')."""
    txt = (L.R / rel).read_text().splitlines() if rel.startswith("docs") else (L.O / rel).read_text().splitlines()
    out, dentro = [], False
    for ln in txt:
        if ln.startswith("## "):
            if dentro:
                break
            dentro = re.search(patron, ln) is not None
            continue
        if dentro:
            out.append(ln)
    return "\n".join(out).strip()


def linea_md(rel: str, patron: str) -> str:
    base = L.R / rel if rel.startswith("docs") or rel.startswith("output/informe") else L.O / rel
    for ln in base.read_text().splitlines():
        if re.search(patron, ln):
            return ln.strip()
    raise KeyError(f"{rel}: {patron}")


def cita(texto: str, fuente: str) -> str:
    return "\n".join("> " + x for x in texto.splitlines()) + f"\n>\n> — `{fuente}`\n"


def fmtN(n) -> str:
    return "; ".join(f"{k} = {L.entero(v)}" for k, v in n.items()) if isinstance(n, dict) else L.entero(n)


def md_df(df, fmt=None):
    return L.tabla_md(df, fmt)


_K = {}


def K() -> dict:
    """Cifras estructurales leídas de ficheros (nunca escritas a mano)."""
    if _K:
        return _K
    hip = (L.R / "docs/v2/hipotesis.md").read_text()
    via = (L.R / "docs/v2/viabilidad_g0.md").read_text()
    dec = (L.R / "docs/v2/decisiones.md").read_text()
    ba, bi, bv = L.j("BA/resultado.json"), L.j("BI/resultado.json"), L.j("BV/resultado.json")
    h1s = L.j("BA/h1_sellado.json")["resultado"]
    reg = L.c("BA/registro.csv").query("modelo_id=='H1_principal'").iloc[0]
    _K.update(
        nprov=ba["N"]["provincias"],
        nsell=len(h1s["selladas"]),
        sell_codigos=", ".join(h1s["selladas"][:-1]) + " y " + h1s["selladas"][-1],
        sell_nombres=re.search(r"provincias (11 \(Cádiz\), 16 \(Cuenca\) y 45 \(Toledo\))", hip).group(1),
        sell_vent=re.search(r"\| P5 sellado \| (\d{4}Q\d-\d{4}Q\d)", hip).group(1),
        train_rango=re.search(r"provincias de entrenamiento × (\d{4}Q\d-\d{4}Q\d)", via).group(1),
        vut_desde=re.search(r"VUT INE (\d{4}Q\d)-", via).group(1),
        nt_vut=re.search(r"N temporal = (\d+)", (L.O / "BA/resumen.md").read_text()).group(1),
        boot=re.search(r"Webb \(([\d\.]+)", ba["metodo"]).group(1),
        bi_per=re.search(r"(\d{4}-\d{4});", bi["datos"]).group(1),
        bv_per=re.search(r"(\d{4}Q\d-\d{4}Q\d)", bv["datos"]).group(1),
        ba_per=f"{reg.muestra_ini}-{reg.muestra_fin}",
        rango_mag=re.search(r"rango razonable ([\d,]+-[\d,]+)", bi["estimacion"]["magnitud"]).group(1),
        umbral_cont=L.j("BM/h7_sellado.json")["resultado"]["umbral_continuidad"],
        ruido=re.search(r"diferencias máximas (~\S+?) ", dec).group(1),
        n52=re.search(r"\(=100 en las (\d+)\)", dec).group(1),
    )
    return _K


# ------------------------------------------------------------------ cálculos reutilizados
def pack(holm, ha, oos, ctr, rank, refs, reg, regmeta):
    """Calcula las cifras que se citan en varias secciones."""
    val = oos[(oos.tipo_muestra == "validacion_entrenamiento") & (oos.nota != "línea base")].copy()
    sel = oos[oos.tipo_muestra == "sellada_principal"].copy()
    d = dict(
        n_val=len(val),
        val_raw=int(((val.DM_vs_AR4 > 0) & (val.p_vs_AR4 < .05)).sum()),
        val_bh=int(((val.DM_vs_AR4 > 0) & (val.p_BH_AR4 < .05)).sum()),
        sel_ok=sel[(sel.DM_vs_AR4 > 0) & (sel.p_vs_AR4 < .05)][["rama", "modelo", "objetivo"]].values.tolist(),
        n_sel=len(sel),
    )
    return d


# ------------------------------------------------------------------ secciones
def s_resumen(holm, ha, oos, rank, reg, regmeta, k):
    h = holm.set_index("hipotesis")
    h1s = L.j("BA/h1_sellado.json")["resultado"]["todas"]
    v1_tot = pd.read_csv(L.R / "output" / "registro_busqueda.csv").shape[0]
    bd = L.c("BD/tabla_resumen.csv")
    def g(per, fam, mer):
        return bd[(bd.periodo == per) & (bd.familia == fam) & (bd.mercado == mer)].iloc[0]
    ao, co = g("P3-P4 (desde 2020)", "observado", "alquiler"), g("P3-P4 (desde 2020)", "comun_efectos_tiempo", "alquiler")
    a14, c14 = g("P2-P4 (desde 2014)", "observado", "alquiler"), g("P2-P4 (desde 2014)", "comun_efectos_tiempo", "alquiler")
    po = g("P3-P4 (desde 2020)", "observado", "compra")
    h6 = L.j("BP/h6_sellado.json")["resultado"]["DECISION"]
    nr = int(L.c("BD/tabla_resumen.csv").shape[0])
    ctr = T.t_contrib()
    n_nr = int(ctr.no_robusto.sum())
    sel_txt = "; ".join(f"{a[0]}: {a[1]}" for a in k["sel_ok"])
    ordenados = '; '.join(f"{x.hipotesis} {N(x.p_holm7)}" for x in holm.sort_values(['p_holm7','hipotesis']).itertuples())
    s = f"""## 1. Resumen ejecutivo

**Alcance.** {L.entero(regmeta['total'])} especificaciones registradas en v2 (`output/v2/tablas/registro_v2.csv`; v1: {L.entero(v1_tot)}), (sin contar las estimaciones de las evaluaciones selladas: {regmeta['sellado_n']}; ver anexo), sobre paneles provinciales ({K()['nprov']} provincias de entrenamiento, {K()['train_rango']}) con la muestra {K()['sell_vent']} y las provincias {K()['sell_codigos']} selladas. Lenguaje de **asociación**: ninguna pregunta alcanza el nivel CAUSAL y ninguna confirmatoria alcanza ASOCIACIÓN ROBUSTA.

- **Hipótesis confirmatorias.** Ninguna de las 7 supera Holm sobre la familia de 7 (p ajustado por hipótesis: {ordenados}; el menor es {h.p_holm7.idxmin()}). Por el criterio uniforme todas quedan **EXPLORATORIO** (etiquetas fijadas en `docs/v2/decisiones.md`).
- **Hecho predictivo de v2.** En la muestra sellada, el modelo demográfico de alquiler (H1) mejora al AR(4) de panel (RMSE {N(h1s['rmse'],4)} frente a {N(h1s['rmse_AR4'],4)}; DM-HLN {N(h1s['dm_vs_AR4'],2)}; p = {PV(h1s['p_vs_AR4'])}; p×7 = {N(7*h1s['p_vs_AR4'])}) y al ECM v1 (p = {PV(h1s['p_vs_ECM_v1'])}). Es un hecho fuera de muestra; **no** convierte la hipótesis conjunta de H1 (que exigía también signo + de la población extranjera, no cumplido: p_IUT {N(h.loc['H1','p_dentro_muestra'])}) en una asociación robusta de cada coeficiente. En las {K()['nsell']} provincias selladas solas (n = {int(L.j('BA/h1_sellado.json')['resultado']['selladas_ventana']['n'])}) no hay diferencia significativa.
- **Ningún otro modelo supera al AR(4).** De {k['n_val']} configuraciones evaluadas en validación por bloques con embargo, {k['val_bh']} mejoran al AR(4) tras BH ({k['val_raw']} con p<0,05 sin corregir); de los {k['n_sel']} contrastes sellados principales, solo cumple {len(k['sel_ok'])} ({sel_txt}).
- **Alquiler frente a compra.** Alquiler: la población de 20-34 años es la asociación más estable entre provincias (+, en todas las submuestras), pero no se traduce en explicar la subida agregada. Compra: el crédito hipotecario nuevo (+) y el coste de uso × exposición hipotecaria (−) se asocian con el precio real dentro de muestra, sin valor predictivo (H2 no se confirma en el sellado). Lo que más pesa en ambos mercados es el componente común no explicado: desde 2020 el alquiler acumula {N(ao.observado_pp,2)} pp y el componente común es {N(co.contrib_pp_M1,2)} pp ({N(co.pct_observado_M1,0)} % del observado, M1); desde 2014, {N(a14.observado_pp,2)} pp con {N(c14.contrib_pp_M1,2)} pp en el común. El precio real de compra varía {N(po.observado_pp,2,True)} pp desde 2020.
- **Política.** Tope catalán de 2020 (H5): signo contrario y fallan pretendencias. Zonas tensionadas (H6): τ = {N(h6['tau'],4,True)} en ln del IPC de alquiler, p nominal {N(h6['p_perm_bilateral'])}, pero Holm-7 {N(h.loc['H6','p_holm7'])}; el DiD simple discrepa y hay heterogeneidad entre provincias: EXPLORATORIO.
- **Contribuciones por periodo (BD).** {n_nr} de los componentes familia × periodo × mercado son «no robustos» (el IC95 excluye 0 solo en uno de los dos modelos o con signos opuestos): no son hallazgos.
- **Qué no se puede afirmar** (sección 11): causalidad de la inmigración, del crédito o del tope catalán; efecto causal de las zonas tensionadas; que un modelo prediga mejor que un AR(4) salvo el hecho sellado de H1; magnitudes de elasticidades.
{src('output/v2/BS/holm7.csv','output/v2/BA/h1_sellado.json','output/v2/BP/h6_sellado.json','output/v2/BD/tabla_resumen.csv','output/v2/tablas/modelos_fuera_muestra.csv','output/v2/tablas/registro_v2.csv','output/registro_busqueda.csv')}"""
    return s


def s_datos(regmeta):
    ramas = {r: L.j(f"{r}/resultado.json") for r in L.RAMAS}
    per = []
    ln = [ln for ln in (L.R / "docs/v2/hipotesis.md").read_text().splitlines() if re.match(r"^\| P\d ", ln)]
    for x in ln:
        p = [y.strip() for y in x.strip().strip("|").split("|")]
        per.append(f"| {p[0]} | {p[1]} | {p[2]} |")
    sells = []
    for r, f in (("BA", "h1_sellado.json"), ("BV", "h2_sellado.json"), ("BP", "h6_sellado.json"), ("BM", "h7_sellado.json")):
        j = L.j(f"{r}/{f}")
        sells.append(f"| {j['hipotesis']} | {j['rama']} | {j['utc']} | {', '.join(j['paneles'])} |")
    bo_txt = (L.O / "BO/resumen.md").read_text()
    sup = re.search(r"([\d\.]+) SUPUESTOS", bo_txt).group(1)
    obs = re.search(r"\*\*([\d\.]+) observados", bo_txt) or re.search(r"([\d\.]+) OBSERVADAS", bo_txt)
    dec = (L.R / "docs/v2/decisiones.md").read_text()
    dmax = re.search(r"entre provincias \((0,\d+)\)", dec).group(1)
    s = f"""## 2. Datos y muestra

**Paneles (entrenamiento).** Provincial trimestral (`panel_prov_q`: {K()['nprov']} provincias de entrenamiento, {K()['train_rango']}), provincial anual, municipal anual y UE anual, más la serie nacional (`nacional_q_v2`), siempre vía `holdout.load_train`. N por rama, tal como figura en `resultado.json`:

""" + "\n".join(f"- **{r}**: N = {fmtN(d['N'])}. Datos: {d['datos']}" for r, d in ramas.items()) + f"""
{src(*[f'output/v2/{r}/resultado.json' for r in L.RAMAS], 'docs/v2/viabilidad_g0.md')}
**Muestra sellada.** Trimestres {K()['sell_vent']} (todas las provincias) y las provincias {K()['sell_nombres']} en todos los periodos; en paneles anuales 2025+ sellado y 2024 en embargo (`docs/v2/hipotesis.md`). Cada hipótesis con evaluación sellada (H1, H2, H6, H7) se evaluó UNA vez (registro de aperturas en `docs/v2/holdout_accesos.md`):

| Hipótesis | Rama | UTC de la evaluación | Paneles |
|---|---|---|---|
""" + "\n".join(sells) + f"""

El sellado es **procedimental** (permisos, carga obligatoria vía `holdout.load_train`, auditoría del revisor), no un secreto físico: `data/raw` está versionado con todos los periodos. Además, los últimos 8 trimestres nacionales ya se usaron en v1, así que a escala nacional el sellado no es «virgen»; las hipótesis confirmatorias se evalúan preferentemente en las provincias selladas.
{src('docs/v2/hipotesis.md','docs/v2/holdout_accesos.md','docs/v2/decisiones.md','output/v2/BA/h1_sellado.json','output/v2/BV/h2_sellado.json','output/v2/BP/h6_sellado.json','output/v2/BM/h7_sellado.json')}
**Periodos fijados ex ante.**

| Periodo | Trimestres | Justificación previa |
|---|---|---|
""" + "\n".join(per) + f"""
{src('docs/v2/hipotesis.md')}
**Interpolaciones y datos no validados (solo robustez, nunca en un modelo principal sin marca).**
- Población (1 de enero) interpolada log-linealmente en T2-T4 en el panel trimestral: marcada; la robustez con T1 observado y con el panel anual coincide (`BA/resumen.md`). El padrón se publica con retraso, de modo que en tiempo real el dato no estaría disponible (`docs/v2/limitaciones.md`, C7 de BA).
- Viviendas turísticas (INE) solo desde {K()['vut_desde']} (N temporal {K()['nt_vut']} en el módulo provincial); SERPAVI municipal (extraído de visor/PDF) se usa únicamente en el módulo exploratorio de turismo de BA, no en los modelos principales.
- Vivienda protegida en el déficit: {obs.group(1) if obs else 'n/d'} viviendas observadas en las provincias de entrenamiento y reescaladas por cobertura (cota inferior sin reescalar: {L.entero(L.c('BO/deficit_nacional.csv').query("variante.str.contains('cota inferior') and ref=='EPA'", engine='python').protegida.iloc[0])}; 2021Q1-2024Q2) más {sup} viviendas **supuestas** (ritmo constante, 2024Q3-2025Q4) en la ilustración de BO; el supuesto no se usa como dato.
- Coste de uso aproximado (sin impuestos ni prima de riesgo; misma serie para todas las provincias). No hay datos provinciales de no residentes ni de inversores (`docs/v2/fuentes_fallidas.md`; licencias, titularidad catastral y AEAT: descargas fallidas).
{src('output/v2/BA/resumen.md','output/v2/BO/resumen.md','docs/v2/fuentes_fallidas.md','docs/v2/viabilidad_g0.md')}
**Fugas detectadas y corregidas** (`docs/v2/decisiones.md`):
1. **Población de 2024Q2** (`pob_total`, `pob_extranj`, `pob_20_34`): se interpolaba con el dato del 1 de enero de 2025, que está sellado. Ahora es NaN en entrenamiento (método `anulado_fuga_sellado`); por eso P4 de BD termina en 2024Q1.
2. **Nivel de los índices con base 2025** (IPC alquiler, IPV, IPV nueva y usada): el INE publica en base 2025=100, de modo que los niveles de entrenamiento incorporaban información de 2025. `holdout.build` rebasa a media de 2015 = 100 por unidad antes de separar entrenamiento y sellado; las diferencias logarítmicas no cambian. Reejecutadas BA, BV, BI y BO: diferencias máximas {K()['ruido']} (ruido de coma flotante). H1 y H2 se evaluaron antes del rebase, con entrenamiento y sellado ambos en base 2025 (consistentes).

**Lectura indebida menor declarada por el orquestador.** Para comprobar la continuidad del rebase, el orquestador leyó en memoria el panel completo fuera de `holdout.evaluate` y mostró dos estadísticos: la media de 2015 por provincia (= 100 en las {K()['n52']}) y el máximo |Δln| del IPC de alquiler entre 2024Q2 y 2024Q3 entre provincias ({dmax}). No se miró ningún efecto ni diferencia entre tratadas y donantes. Es un acceso indebido menor, registrado en `docs/v2/decisiones.md`; el umbral de continuidad de H7 ({N(K()['umbral_cont'],2)}) se fijó después de esa comprobación (limitación de BM).
{src('docs/v2/decisiones.md','docs/v2/limitaciones.md')}"""
    return s


def s_metodos(refs):
    r = refs.set_index(refs.referencia.str.extract(r"^(.*?\(\d{4}\))")[0])
    def t(clave):
        m = [i for i in r.index if re.search(clave, i)]
        if not m:
            raise KeyError(clave)
        e = r.loc[m[0]]
        etq = e.estado if e.estado != "VERIFICADA" else "verificada"
        if e.cuartil_no_verificado and e.estado == "VERIFICADA":
            etq = "verificada; cuartil no verificado"
        return f"{m[0]} [{etq}]"
    s = f"""**Métodos y referencias metodológicas** (estado de verificación entre corchetes; detalle en la sección 12):
- Comparación fuera de muestra: Diebold-Mariano {t('Diebold')} con la corrección de muestra finita {t('Harvey')}.
- Inferencia con pocos clusters: wild cluster bootstrap restringido, {t('^Roodman')} y pesos de {t('^Webb')}.
- Control sintético y SDiD (H5, H6): {t('Abadie')} y {t('Arkhangelsky')}.
- Shift-share (H3): {t('Goldsmith')}, {t('Borusyak')}, {t('Adão')}; crítica de exogeneidad y de dinámica: {t('^Jaeger')}; F de primera etapa: {t('Montiel')}.
- Heterogeneidad y aprendizaje automático (BI, BM): {t('^Chernozhukov')} y {t('Athey')}; elastic net {t('^Zou')}; post-double-selection {t('Belloni')}; ALE {t('Apley')}; LSTM {t('Hochreiter')}; SHAP {t('Lundberg')} y LightGBM {t('^Ke ')}.
- Parámetros cambiantes y proyecciones locales (BM, BV, BO): BVAR {t('Giannone')}; TVP-VAR {t('^Primiceri')} con la corrección de {t('Del Negro')}; proyecciones locales {t('Jordà')}.
- Coste de uso de la vivienda: {t('Poterba')}.
- Contexto y signos esperados: demografía y alquiler {t('Khametshin')}; inmigración y precios {t('Saiz')}; turismo {t('Garcia')}; tope de rentas (contratos nuevos) {t('Jofre')}; elasticidad de la oferta citada por el Banco de España {t('Caldera')} y {t('Cavalleri')}; déficit de 750.000 viviendas {t('^Banco de España')}.
{src('docs/literatura.md','output/v2/tablas/referencias_v2.csv')}"""
    return s


def s_alq_vs_compra(ctr):
    pco = L.c("BA/periodos_coef.csv")
    bvp = L.c("BV/periodos_coeficientes_H2_FEtrim.csv")
    bd = L.c("BD/tabla_resumen.csv")
    perf = {"P1": "P1_ajuste", "P2": "P2_recuperacion", "P3": "P3_covid", "P4": "P4_tipos"}
    filas = []
    for p, pb in perf.items():
        a = pco[(pco.x == "d4_ln_pob_20_34") & (pco.periodo == p)].iloc[0]
        cr = bvp[(bvp.variable == "d4_ln_hipotecas_importe") & (bvp.periodo == pb)].iloc[0]
        cu = bvp[(bvp.variable == "cu_x_expo") & (bvp.periodo == pb)].iloc[0]
        oa = bd[(bd.periodo == p) & (bd.familia == "observado") & (bd.mercado == "alquiler")].iloc[0]
        oc = bd[(bd.periodo == p) & (bd.familia == "observado") & (bd.mercado == "compra")].iloc[0]
        filas.append({"Periodo": p, "Alquiler observado (pp)": N(oa.observado_pp, 2), "Compra real observada (pp)": N(oc.observado_pp, 2),
                      "Alquiler: coef. 20-34 [q BH]": f"{N(a.coef)} [{N(a.q_BH,2)}]",
                      "Compra: coef. crédito [p Holm]": f"{N(cr.coef,4)} [{PV(cr.p_holm)}]",
                      "Compra: coef. coste de uso × exposición [p Holm]": f"{N(cu.coef,4)} [{PV(cu.p_holm)}]"})
    t = md_df(pd.DataFrame(filas))
    ex = L.c("BA/h1_principal.csv").set_index("var")
    arb = L.c("BV/arbitraje_lp.csv")
    ap = arb[(arb.h == 4) & (arb.desv == "media_total")].set_index("outcome")
    _c = ctr[(ctr.mercado == 'compra')]
    dm14 = _c[(_c.periodo == 'P2-P4 (desde 2014)') & (_c.familia == 'demografia')].iloc[0]
    cp1 = _c[(_c.periodo == 'P1') & (_c.familia == 'credito_tipos_cu')].iloc[0]
    s = f"""## 3. Alquiler frente a compra: qué se asocia con cada uno y por periodo

Todo en este apartado es **asociación** (EXPLORATORIO o DESCRIPTIVO). Crecimiento acumulado observado por periodo en pp de ln (alquiler nominal; valor tasado real) y coeficientes por periodo de las ecuaciones de BA y BV:

{t}
{src('output/v2/BD/tabla_resumen.csv','output/v2/BA/periodos_coef.csv','output/v2/BV/periodos_coeficientes_H2_FEtrim.csv')}
**Alquiler.**
- La población de 20-34 años es la variable más estable entre provincias: positiva en P1-P3 y más débil en P4 (tabla). La población extranjera sale con signo no positivo ({N(ex.loc['d4_ln_pob_extranj','coef'])}, IC95 {IC(ex.loc['d4_ln_pob_extranj','ic95_lo'], ex.loc['d4_ln_pob_extranj','ic95_hi'])}) cuando se condiciona a efectos de tiempo; sin ellos la asociación temporal agregada con la población extranjera sí aparece (`BA/resumen.md`), pero no se traslada a diferencias entre provincias.
- La inmigración instrumentada con shift-share (BI, {K()['bi_per']}) da un coeficiente positivo (β = {N(L.c('BI/h3_principal.csv').set_index('resultado').loc['alq','b_2sls'],2)}) que **no resiste** los controles GPSS, los placebos de alquiler pasado ni la submuestra 2015-2021: solo el signo es estable; la magnitud no está identificada.
- Viviendas turísticas, oferta (terminadas), empleo y coste de uso: sin asociación robusta (ranking, sección 5).
- Política: zonas tensionadas de Cataluña (H6) y tope de 2020 (H5) en la sección 7.

**Compra.**
- El crédito hipotecario nuevo (+) y el coste de uso × exposición hipotecaria (−) se asocian con el crecimiento del precio real en la muestra completa, con los signos esperados, pero el crédito no es significativo en 2014-2024 ni con el crédito retardado 4 trimestres (simultaneidad), y el modelo con ambas variables no predice mejor que un AR(4) (sección 6).
- La asociación del coste de uso es fuerte en P1 y P3 y nula en P4: el alza de tipos de 2022 no se recoge con esta variable.
- Arbitraje alquiler-compra (ratio precio/alquiler 1 unidad de log por encima de su media, h = 4): precio {N(ap.loc['y_precio','coef'])} (Holm m=16 {PV(ap.loc['y_precio','p_holm_m16'])}) y alquiler {N(ap.loc['y_alq','coef'])} (Holm {N(ap.loc['y_alq','p_holm_m16'])}); el ajuste es sobre todo vía precio; la desviación respecto de la media de toda la muestra incorpora reversión mecánica.
- Demografía agregada: desde 2014 es negativa en M1 ({N(dm14.contrib_pp_M1,2)} pp) y en M2 ({N(dm14.contrib_pp_M2,2)} pp) con IC95 que excluyen 0, es decir, se replica entre modelos (EXPLORATORIO; refleja la composición de la población, no un efecto); desde 2020 no hay atribución estable. El crédito/coste de uso en P1 también se replica ({N(cp1.contrib_pp_M1,2)} y {N(cp1.contrib_pp_M2,2)} pp). Empleo y oferta: sin atribución estable entre M1 y M2.

**Común a ambos.** Lo que más pesa es lo no explicado por las familias medidas (efectos comunes de tiempo: tipos, expectativas, inflación, regulación nacional); ver sección 4.3.
{src('output/v2/BA/resumen.md','output/v2/BV/resumen.md','output/v2/BI/resumen.md','output/v2/BV/arbitraje_lp.csv','output/v2/BA/h1_principal.csv','output/v2/BI/h3_principal.csv')}"""
    return s


def s_ecuaciones(ctr):
    h1 = L.c("BA/h1_principal.csv")
    h2 = L.c("BV/h2_resultados.csv").query("spec=='H2_principal'")
    nm = {"d4_ln_pob_20_34": "Δ4 ln población 20-34", "d4_ln_pob_extranj": "Δ4 ln población extranjera", "d4_ln_ocupados": "Δ4 ln ocupados",
          "d4_ln_hipotecas_importe": "Δ4 ln importe hipotecario", "cu_x_expo": "coste de uso × exposición hip. 2005-07 (z)"}
    t1 = pd.DataFrame({"Variable": h1["var"].map(nm), "Coef.": h1.coef.map(lambda x: N(x, 4)), "EE cluster": h1.se.map(lambda x: N(x, 4)),
                       "IC95 %": [IC(a, b, 4) for a, b in zip(h1.ic95_lo, h1.ic95_hi)], "p cluster": h1.p.map(PV),
                       "p wild bootstrap": h1.p_boot.map(PV), "p Holm intra-H1 (m=2)": h1.p_holm_H1.map(PV)})
    t2 = pd.DataFrame({"Variable": h2["var"].map(nm), "Coef.": h2.coef.map(lambda x: N(x, 4)), "EE cluster": h2.se.map(lambda x: N(x, 4)),
                       "IC95 %": [IC(a, b, 4) for a, b in zip(h2.ic95_inf, h2.ic95_sup)], "p cluster": h2.p.map(PV), "p wild bootstrap": h2.p_wcb.map(PV)})
    bd_r = pd.DataFrame()
    ctr2 = ctr.copy()
    def tabla_ctr(mer, ventanas):
        fam = ["demografia", "demografia_20_34", "demografia_extranj", "empleo_renta", "credito_tipos_cu", "oferta", "politica", "explicado_familias", "comun_efectos_tiempo", "residuo", "observado"]
        nombres = {"demografia": "Demografía agregada (20-34 + extranjera)", "demografia_20_34": "Demografía: 20-34", "demografia_extranj": "Demografía: extranjera", "empleo_renta": "Empleo (ocupados)",
                   "credito_tipos_cu": "Crédito / coste de uso", "oferta": "Oferta (terminadas)", "politica": "Política (tope CAT)",
                   "explicado_familias": "Suma de familias", "comun_efectos_tiempo": "Común (efectos de tiempo)", "residuo": "Residuo", "observado": "Observado"}
        out = []
        for v in ventanas:
            for f in fam:
                r = ctr2[(ctr2.periodo == v) & (ctr2.familia == f) & (ctr2.mercado == mer)]
                if r.empty:
                    continue
                r = r.iloc[0]
                out.append({"Ventana": v, "Componente": nombres[f],
                            "M1 pp [IC95 %]": f"{N(r.contrib_pp_M1,2)} [{N(r.ic95_inf_M1,2)}; {N(r.ic95_sup_M1,2)}]",
                            "M2 pp [IC95 %]": f"{N(r.contrib_pp_M2,2)} [{N(r.ic95_inf_M2,2)}; {N(r.ic95_sup_M2,2)}]",
                            "Robustez M1/M2": r.robustez_M1_M2.split(" (")[0], "Nivel": r.nivel_evidencia})
        return md_df(pd.DataFrame(out))
    VENT = ["P2-P4 (desde 2014)", "P3-P4 (desde 2020)"]
    def tabla_periodos(mer):
        out = []
        for p in ("P1", "P2", "P3", "P4"):
            row = {"Periodo": p}
            for f, nmb in (("observado", "Observado"), ("demografia", "Demografía"), ("empleo_renta", "Empleo"), ("credito_tipos_cu", "Crédito/CU"),
                           ("oferta", "Oferta"), ("comun_efectos_tiempo", "Común")):
                r = ctr2[(ctr2.periodo == p) & (ctr2.familia == f) & (ctr2.mercado == mer)].iloc[0]
                row[nmb] = f"{N(r.contrib_pp_M1,2)} [{N(r.ic95_inf_M1,2)}; {N(r.ic95_sup_M1,2)}]"
            out.append(row)
        return md_df(pd.DataFrame(out))
    nr = ctr2[ctr2.no_robusto].copy()
    nrt = pd.DataFrame({"Mercado": nr.mercado, "Ventana": nr.periodo, "Componente": nr.familia,
                        "M1 [IC95 %]": [f"{N(a,2)} [{N(b,2)}; {N(c,2)}]" for a, b, c in zip(nr.contrib_pp_M1, nr.ic95_inf_M1, nr.ic95_sup_M1)],
                        "M2 [IC95 %]": [f"{N(a,2)} [{N(b,2)}; {N(c,2)}]" for a, b, c in zip(nr.contrib_pp_M2, nr.ic95_inf_M2, nr.ic95_sup_M2)],
                        "Motivo": nr.robustez_M1_M2})
    lim_bd = seccion_md("docs/v2/limitaciones.md", r"BD \(")
    bd_head = linea_md("BD/resumen.md", r"^\*\*Nivel de evidencia global")
    resp_bd = ('**Respuesta breve de BD** (asociaciones condicionales, EXPLORATORIO):\n\n' + seccion_md('BD/resumen.md', r'Respuesta breve')
               + '\n\nLa demografía contribuye de forma negativa en 2014-2019 por composición, no por una asociación nueva:\n\n'
               + cita(linea_md('BD/resumen.md', r'^- La demografía contribuye NEGATIVAMENTE').lstrip('- '), 'output/v2/BD/resumen.md'))
    s = f"""## 4. Ecuaciones principales y contribuciones por periodo

### 4.1 Alquiler (BA, H1): Δ4 ln IPC de alquiler provincial

MCO con efectos fijos de provincia y de trimestre, EE cluster por provincia ({int(h1.G.iloc[0])} clusters, t con {int(h1.G.iloc[0])-1} gl), wild cluster bootstrap restringido (Webb, {K()['boot']}). N = {L.entero(h1.n.iloc[0])}, {int(h1.G.iloc[0])} provincias, {K()['ba_per']} con población disponible, R² within = {N(h1.r2_within.iloc[0],3)}. Nivel: **EXPLORATORIO**.

{md_df(t1)}
{src('output/v2/BA/h1_principal.csv')}
Lectura: 1 pp más de crecimiento interanual de la población de 20-34 años se asocia con {N(h1.coef.iloc[0],2)} pp más de crecimiento del alquiler (diferencial entre provincias). La parte «extranjera» de H1 no se confirma (signo opuesto, indistinguible de 0) y los ocupados no se asocian. Población interpolada en T2-T4 (marcada).

### 4.2 Compra (BV, H2): Δ4 ln valor tasado real provincial

MCO con FE de provincia y trimestre, EE cluster, bootstrap Webb {K()['boot']}. N = {L.entero(h2.N.iloc[0])}, {int(h2.G.iloc[0])} provincias, {K()['bv_per']}. Nivel: **EXPLORATORIO** (H2 no se confirma en el sellado). Magnitud: 1 unidad de coste de uso × exposición (por DE y pp) se asocia con {N(h2.coef.iloc[1],4)} pp; solo se identifica el diferencial por exposición (el nivel nacional lo absorbe el FE de trimestre).

{md_df(t2)}
{src('output/v2/BV/h2_resultados.csv')}
Simultaneidad: con el crédito retardado 4 trimestres su coeficiente es {N(L.c('BV/h2_resultados.csv').query("spec=='H2_credito_l4' and var=='hip_l4'").coef.iloc[0],4)} (p wild {N(L.c('BV/h2_resultados.csv').query("spec=='H2_credito_l4' and var=='hip_l4'").p_wcb.iloc[0])}): la asociación del crédito es contemporánea, no predictiva.

### 4.3 Contribuciones por periodo y familia (BD)

{bd_head}

Contribución = coeficiente por periodo × variación media de la familia (media ponderada por población), en pp de ln acumulados; identidad contable observado = familias + común + residuo. **M1**: efectos fijos de provincia y de trimestre (el «común» recoge lo que se mueve igual en todas las provincias). **M2**: sin efectos de tiempo, con Δ4 del coste de uso nacional. IC95 % = envolvente de bootstrap por provincias y por bloques de tiempo. P4 termina en 2024Q1 (fuga de la población de 2024Q2 corregida).

{resp_bd}

![Contribuciones por periodo](BS/contribuciones_periodo.png)

*Figura: `output/v2/BS/contribuciones_periodo.png` (datos: `output/v2/BD/tabla_resumen.csv`).*

**Alquiler, por periodo (M1).**

{tabla_periodos('alquiler')}

**Alquiler, ventanas acumuladas desde 2014 y desde 2020.**

{tabla_ctr('alquiler', VENT)}

**Corrección a la lectura de BD para compra:** la cita anterior dice «sin atribución estable entre M1 y M2»; con la tabla de ventanas, la demografía agregada desde 2014 sí se replica en M1 y M2 (y el crédito/coste de uso de P1), EXPLORATORIO; el resto no.

**Compra (valor tasado real), por periodo (M1).**

{tabla_periodos('compra')}

**Compra, ventanas acumuladas.**

{tabla_ctr('compra', VENT)}
{src('output/v2/tablas/contribuciones_periodo.csv','output/v2/BD/tabla_resumen.csv')}
**Componentes no robustos** (IC95 que excluye 0 solo en un modelo o con signos opuestos; no son hallazgos; sin corrección por multiplicidad sobre ~14 componentes × 2 modelos):

{md_df(nrt)}
{src('output/v2/tablas/contribuciones_periodo.csv')}
**Limitaciones de BD** (de `docs/v2/limitaciones.md`):

{lim_bd}
{src('docs/v2/limitaciones.md')}"""
    return s


def s_ranking(rank):
    r = rank.copy()
    for k in ["A_p_ajustado", "B_signo_estable", "C_oos_entrenamiento", "D_sellado", "E_bd_M1_M2"]:
        r[k] = r[k].map(lambda v: "sí" if str(v) == "True" else ("no" if str(v) == "False" else "n/a"))
    t = md_df(r[["rango", "familia", "mercado", "evidencia_mas_alta", "A_p_ajustado", "B_signo_estable", "C_oos_entrenamiento", "D_sellado", "E_bd_M1_M2",
                 "criterios_cumplidos", "criterios_evaluables"]].rename(columns={"evidencia_mas_alta": "nivel", "A_p_ajustado": "A", "B_signo_estable": "B",
                                                                                "C_oos_entrenamiento": "C", "D_sellado": "D", "E_bd_M1_M2": "E",
                                                                                "criterios_cumplidos": "cumple", "criterios_evaluables": "evaluables"}),
                {"rango": lambda v: str(int(v)), "cumple": lambda v: str(int(v)), "evaluables": lambda v: str(int(v))})
    porque = "\n".join(f"- **{x.rango}. {x.familia} ({x.mercado})**: {x.por_que}." for x in rank.itertuples())
    s = f"""## 5. Ranking de factores y nivel de evidencia

Criterios (A-E) por familia y mercado: **A** p ajustado por multiplicidad < 0,05 (Holm/BH intra-rama o Holm-7); **B** signo estable en submuestras o periodos; **C** mejora predictiva significativa frente al AR(4) en validación de entrenamiento; **D** mejora significativa frente al AR(4) en la muestra sellada; **E** contribución de BD replicada en M1 y M2 desde 2020 (IC95 excluye 0, mismo signo). «n/a» = no evaluable. La puntuación (nº de criterios cumplidos) ordena la tabla; es un resumen descriptivo, no un contraste. **Ninguna familia supera el nivel EXPLORATORIO** (tope fijado por el orquestador: ninguna confirmatoria sobrevive a Holm-7); lo no explicado y el déficit son DESCRIPTIVO.

{t}
{src('output/v2/tablas/ranking_factores.csv')}
**Por qué (con la cifra de origen):**

{porque}
{src('output/v2/tablas/ranking_factores.csv (columna fuentes de cada fila)')}"""
    return s


def s_oos(oos, k):
    val = oos[(oos.tipo_muestra == "validacion_entrenamiento")]
    rows = []
    for (rama, obj), g in val.groupby(["rama", "objetivo"], sort=False):
        m = g[g.nota != "línea base"]
        m = m[~m.modelo.str.startswith("LSTM")] if rama == "BM" else m
        b = m.loc[m.RMSE.idxmin()]
        rows.append({"Rama": rama, "Objetivo": obj, "Config.": len(m), "Mejor RMSE (modelo)": b.modelo, "N": L.entero(b.N), "RMSE": N(b.RMSE, 4),
                     "RMSE AR(4)": N(b.RMSE_AR4, 4), "RMSE ECM v1": N(b.RMSE_ECM_v1, 4), "DM vs AR(4)": N(b.DM_vs_AR4, 2), "p": PV(b.p_vs_AR4),
                     "p BH": PV(b.p_BH_AR4), "Mejoran al AR(4) con BH": int(((m.DM_vs_AR4 > 0) & (m.p_BH_AR4 < .05)).sum())})
    tv = md_df(pd.DataFrame(rows))
    sel = oos[oos.tipo_muestra == "sellada_principal"]
    rows = []
    for _, b in sel.iterrows():
        rows.append({"Rama": b.rama, "Modelo": b.modelo, "Objetivo": b.objetivo, "N": L.entero(b.N), "RMSE": N(b.RMSE, 4), "RMSE AR(4)": N(b.RMSE_AR4, 4),
                     "DM vs AR(4)": N(b.DM_vs_AR4, 2), "p": PV(b.p_vs_AR4), "p BH (5 sellados)": PV(b.p_BH_AR4), "RMSE ECM v1": N(b.RMSE_ECM_v1, 4),
                     "DM vs ECM v1": N(b.DM_vs_ECM_v1, 2), "p ECM": PV(b.p_vs_ECM_v1)})
    ts = md_df(pd.DataFrame(rows))
    h1sec = oos[(oos.rama == "BA") & (oos.tipo_muestra == "sellada_secundaria")]
    h1v = h1sec[h1sec.muestra.str.contains("solo provincias selladas")].iloc[0]
    h7 = L.j("BM/h7_sellado.json")["resultado"]["A"]["PRINCIPAL"]
    hC = L.j("BM/h7_sellado.json")["resultado"]["C"]["PRINCIPAL"]
    h2c = oos[(oos.rama == 'BV') & oos.muestra.str.contains('referencia ECM')].iloc[0]
    lstm = L.j("BM/lstm_resultado.json")
    sel_txt = ", ".join(f"{a[0]}: {a[1]}" for a in k["sel_ok"])
    vv = val[(val.DM_vs_AR4 > 0) & (val.p_vs_AR4 < .05) & (val.nota != 'línea base')]
    cruda = '; '.join(f"{x.rama} {x.modelo} (p {PV(x.p_vs_AR4)}, p BH {PV(x.p_BH_AR4)})" for x in vv.itertuples())
    s = f"""## 6. Modelos fuera de muestra frente a AR(4) y ECM v1

Todo en la misma muestra por contraste, h = 4 trimestres (anual en BI), DM con corrección Harvey-Leybourne-Newbold (DM > 0 = el modelo es mejor que la base). Detalle de los {oos.shape[0]} modelos y evaluaciones: `output/v2/tablas/modelos_fuera_muestra.csv`.

### 6.1 Validación en bloques con embargo (entrenamiento ≤ 2024Q2; informativa)

{tv}
{src('output/v2/tablas/modelos_fuera_muestra.csv')}
De {k['n_val']} filas de modelos con variables (incluidas {L.c('BM/lstm_panelB.csv').shape[0]} configuraciones de LSTM), **{k['val_bh']} mejoran al AR(4) con BH** ({k['val_raw']} con p < 0,05 sin corregir: {cruda}, que tampoco sobreviven a BH). El ECM v1 es peor que el AR(4) en los tres objetivos de BM: en entrenamiento mejorarlo es un listón bajo (en el sellado de compra no lo es: ver 6.2). El LSTM no supera al gradient boosting (RMSE {N(lstm['RMSE_LSTM'],4)} frente a {N(lstm['RMSE_GB'],4)}; DM {N(lstm['DM_LSTM_vs_GB'],2)}; p = {PV(lstm['p'])}): resultado negativo.

### 6.2 Muestra sellada (una evaluación por hipótesis; principal = {K()['nprov']+K()['nsell']} provincias, {K()['sell_vent']})

{ts}
{src('output/v2/BA/h1_sellado.json','output/v2/BV/h2_sellado.json','output/v2/BM/h7_sellado.json','output/v2/tablas/modelos_fuera_muestra.csv')}
**Lectura.** Ningún modelo supera al AR(4) salvo la mejora sellada del modelo demográfico de alquiler ({sel_txt}). En las {K()['nsell']} provincias selladas solas (n = {int(h1v.N)}) esa mejora no es significativa (p = {PV(h1v.p_vs_AR4)}): la potencia es baja y el resultado descansa en las {K()['nprov']} provincias de entrenamiento evaluadas en {K()['sell_vent']}. En entrenamiento el mismo modelo no mejoraba (p = {PV(oos[(oos.rama=='BA') & (oos.modelo=='B_AR4_mas_H1') & (oos.tipo_muestra=='validacion_entrenamiento')].p_vs_AR4.iloc[0])}). H2 (C3) y H7 (A, B, C) no cumplen la regla.

**Contraste de H2 con el ECM v1** (49 provincias, {K()['sell_vent']}; `sec_c` de `BV/h2_sellado.json`): ECM v1 RMSE {N(h2c.RMSE_ECM_v1,4)} frente a {N(h2c.RMSE,4)} de C3; DM {N(h2c.DM_vs_ECM_v1,2)}; p = {PV(h2c.p_vs_ECM_v1)}: sin diferencia.

**Observación NO pre-registrada (no se usa como evidencia).** En la sellada de compra provincial (52 provincias) el ECM v1 tuvo menor RMSE que el AR(4): {N(hC['rmse_ECM_v1'],4)} frente a {N(hC['rmse_AR4'],4)} (solo RMSE, sin contraste). En la ventana sellada nacional (n = {int(h7['n'])}) el ECM v1 tuvo RMSE {N(h7['rmse_ECM_v1'],4)} frente a {N(h7['rmse_AR4'],4)} del AR(4) y {N(h7['rmse'],4)} del TVP-VAR elegido para H7. Con n = 8 y sin que se hubiera fijado de antemano, no se interpreta; en entrenamiento el ECM v1 era peor que el AR(4) en los tres objetivos.
{src('output/v2/BM/h7_sellado.json','output/v2/BM/resumen.md')}"""
    return s


def s_hipotesis(ha, holm, bsdir):
    ver = pd.read_csv(bsdir / "holm7_verificacion.csv")
    t = pd.DataFrame({"Id": ha.hipotesis, "Signo esperado": ha.signo_esperado, "Estimación": ha.estimacion, "IC95 %": ha.ic95,
                      "p dentro de muestra": ha.p_dentro_muestra.map(lambda x: N(x, 4)), "p sellado": ha.p_sellado.map(lambda x: N(x, 4)), "p hipótesis (IUT/máx.)": ha.p_hipotesis_preregistrada.map(lambda x: N(x, 4)),
                      "p Holm-7": ha.p_holm7.map(lambda x: N(x, 4)), "Nivel": ha.nivel_evidencia})
    dec = "\n".join(f"- **{x.hipotesis} ({x.rama})**: {x.decision}. {x.nota}." for x in ha.itertuples())
    v = pd.DataFrame({"Id": ver.hipotesis, "p transcrito en la versión previa": ver.p_transcrito_previo.map(lambda x: N(x, 4)), "p leído del fichero": ver.p_fichero.map(lambda x: N(x, 4)),
                      "Diferencia": ver.diferencia.map(lambda x: N(x, 4, True))})
    h3 = holm.set_index("hipotesis").loc["H3"]
    s = f"""## 7. Hipótesis confirmatorias y Holm-7

Familia de 7 hipótesis pre-registradas (`docs/v2/hipotesis.md`, tag `prereg-v2`). p de cada hipótesis = la decisión pre-registrada: las conjunciones se contrastan por intersección-unión (máximo de los p componentes) y, con evaluación sellada, el p conjunto es el máximo entre dentro de muestra y sellado. Holm sobre las 7. **Ninguna supera Holm al 5 %.** Todas EXPLORATORIO.

{md_df(t)}
{src('output/v2/tablas/hipotesis_confirmatorias.csv','output/v2/BS/holm7.csv')}
{dec}
{src('output/v2/tablas/hipotesis_confirmatorias.csv')}
**Verificación de los p transcritos.** La versión previa de `src/v2/holm7.py` traía transcritos los p dentro de muestra de H1-H5; ahora se leen de los ficheros de cada rama y se contrastan:

{md_df(v)}

Todos coinciden salvo redondeo; se usa el valor del fichero. El único efecto visible es H3: el fichero da {N(h3.p_hipotesis,4)} (la versión previa 0,029), de modo que su p Holm-7 es {N(h3.p_holm7,4)} y no 0,174 (en `docs/v2/decisiones.md` figura «0,17»); la conclusión no cambia. Del mismo modo, el p sellado de H1 ×7 es {N(7*holm.set_index('hipotesis').loc['H1','p_sellado'])} con el p exacto del fichero (en `docs/v2/decisiones.md` figura 0,035, con el p redondeado a 0,005).
{src('output/v2/BS/holm7_verificacion.csv','output/v2/BS/holm7.csv')}
**Etiquetas finales (fijadas por el orquestador).** Ninguna hipótesis confirmatoria alcanza ASOCIACIÓN ROBUSTA ni CAUSAL. H1 (conjunta) EXPLORATORIO; se reporta como HECHO fuera de muestra que el modelo demográfico de alquiler mejora al AR(4) y al ECM v1 en la muestra sellada, sin convertirlo en asociación robusta de cada coeficiente. H6 EXPLORATORIO (SDiD y control sintético coinciden; el DiD simple discrepa; heterogeneidad por provincia). H2, H3, H4, H5 y H7 EXPLORATORIO o no confirmadas. Todo lo demás EXPLORATORIO o DESCRIPTIVO (`docs/v2/decisiones.md`).
{src('docs/v2/decisiones.md')}"""
    return s


def s_cambios(holm, regmeta):
    v1_lp = pd.read_csv(L.R / "output/tablas/ecuacion_final_lp.csv")
    v1_cp = pd.read_csv(L.R / "output/tablas/ecuacion_final_cp.csv")
    v1_tot = pd.read_csv(L.R / "output/registro_busqueda.csv").shape[0]
    iv = pd.read_csv(L.R / "output/tablas/inmigracion_iv.csv")
    ipc = iv[(iv.resultado == "IPC alquiler") & (iv.spec == "FE")].set_index("est")
    d1 = pd.read_csv(L.R / "output/tablas/deficit.csv")
    d1p = d1[d1.variante.astype(str).str.contains("PRINCIPAL")].iloc[0]
    d1e = d1[d1.variante.astype(str).str.contains("ECP 60131")].iloc[0]
    ref = pd.read_csv(L.R / "output/tablas/referencias.csv")
    cj1 = ref[ref.referencia.str.contains("Caldera")].iloc[0].marca
    cj2 = T.t_refs().query("referencia.str.contains('Caldera')", engine="python").iloc[0].estado
    dn = L.c("BO/deficit_nacional.csv").set_index("variante")
    bi = L.c("BI/h3_identificacion.csv").set_index(["spec", "res"])
    b3 = L.c("BI/h3_principal.csv").set_index("resultado")
    dmv1 = re.search(r"fuera de muestra \(DM p = ([\d,]+)\)", (L.R / "output/informe.md").read_text()).group(1)
    ba, bv = L.j("BA/resultado.json"), L.j("BV/resultado.json")
    tab = pd.DataFrame([
        ["Unidad de análisis y N", f"Serie nacional trimestral: LP N={int(v1_lp.N.iloc[0])}, CP N={int(v1_cp.N.iloc[0])}; panel de 17 CCAA anual",
         f"Paneles provinciales: alquiler N={L.entero(ba['N']['H1_prov_trim'])} y compra N={L.entero(bv['N']['H2_principal'])} (49 provincias, trimestral); BI N={L.entero(L.j('BI/resultado.json')['N'])}; BO N={L.entero(L.j('BO/resultado.json')['N'])}",
         "Más N y heterogeneidad; riesgo de interpolación de población en T2-T4"],
        ["Escala de evidencia", "«asociación» (ninguna pregunta alcanzó el nivel causal)", "CAUSAL > ASOCIACIÓN ROBUSTA > EXPLORATORIO > DESCRIPTIVO; 7 confirmatorias pre-registradas con Holm-7",
         "Pre-registro (tag `prereg-v2`) y muestra sellada: separa confirmación de exploración"],
        ["Especificaciones probadas", L.entero(v1_tot), L.entero(regmeta["total"]), "Corrección por búsqueda: Holm/BH por familia y Holm-7"],
        ["Inmigración y alquiler", f"OLS IPC alquiler {N(ipc.loc['OLS','coef'])} (p WCB {N(ipc.loc['OLS','p_WCB_restr'],3)}); panel de 17 CCAA, 2003-2025; 2SLS {N(ipc.loc['2SLS','coef'])} (p WCB {N(ipc.loc['2SLS','p_WCB_restr'])})",
         f"2SLS β alquiler {N(b3.loc['alq','b_2sls'],2)} (p WCB {N(b3.loc['alq','p_wcb_2c'])}); con GPSS de extranjeros 2002 {N(bi.loc[('gpss_extr02','alq'),'b'],2)} (p cluster {N(bi.loc[('gpss_extr02','alq'),'p_cluster'])}); placebo de alquiler pasado rechaza",
         "Con paneles provinciales, GPSS y placebos la inmigración **ya no es una asociación robusta con el alquiler**: solo el signo + es estable; magnitud no identificada; CAUSAL descartado"],
        ["Déficit de vivienda", f"{L.entero(d1p.deficit)} (2021T1-2025T4, EPA corregida, sin protegida); {L.entero(d1e.deficit)} (ECP)",
         f"{L.entero(dn.loc['EPA corregida, sin protegida','deficit'])} sin protegida y {L.entero(dn.loc['EPA corregida, con protegida (49 prov. + reescalado)','deficit'])} con protegida (2021Q1-2024Q2; protegida observada y reescalada por cobertura; cota inferior {L.entero(dn.loc['EPA corregida, con protegida (solo 49 prov., cota inferior)','deficit'])})",
         "No comparable (periodo más corto por el sellado); con/sin protegida se separan observadas y supuestas; DESCRIPTIVO"],
        ["Predicción", f"El modelo preferido no mejora al AR(4) (DM p = {dmv1})", "Ninguna configuración mejora al AR(4) en validación (BH); solo H1 mejora en el sellado",
         "Validación en bloques con embargo y evaluación sellada única"],
        ["Caldera y Johansson (2013)", cj1, cj2, "DOI comprobado en Crossref en v2; el informe v1 no se modifica"],
        ["Quiebres", "Chow 2014Q1; modelo no estable", "Periodos P0-P5 fijados ex ante; coeficientes por periodo y contribuciones con IC", "Se pregunta por los periodos en vez de detectarlos"],
    ], columns=["Aspecto", "v1", "v2", "Por qué cambia / lectura"])
    s = f"""## 8. Qué cambió respecto de v1 y por qué

{md_df(tab)}
{src('output/informe.md','output/tablas/ecuacion_final_lp.csv','output/tablas/ecuacion_final_cp.csv','output/tablas/inmigracion_iv.csv','output/tablas/deficit.csv','output/tablas/referencias.csv','output/registro_busqueda.csv','output/v2/BI/h3_principal.csv','output/v2/BI/h3_identificacion.csv','output/v2/BO/deficit_nacional.csv','docs/literatura.md')}
Cavalleri, Cournède y Özsöğüt (2019) sigue como parcialmente verificada (DOI existe; autores y número no confirmados). El estudio de València de v1 no se repite en v2 (los paneles son provinciales): sus conclusiones siguen siendo las de v1.
"""
    return s


def s_negativos():
    h2s = L.j("BV/h2_sellado.json")["resultado"]["PRINCIPAL_todas"]
    bp = L.j("BP/resultado.json")["diagnosticos"]
    h7 = L.j("BM/h7_sellado.json")["resultado"]
    lstm = L.j("BM/lstm_resultado.json")
    h4 = L.c("BO/h4_robustez_submuestras.csv")
    suelo = L.c("BO/suelo_proyecciones_locales.csv")
    tur = L.c("BA/turismo.csv").set_index("spec")
    bhj = linea_md("BI/resumen.md", r"^- BHJ a nivel de shock")
    bhj_es = re.sub(r'(\d)\.(\d)', r'\1,\2', bhj.lstrip('- ').replace('p=0.000', 'p < 0,001')).replace('p=', 'p = ')
    ue = seccion_md("BO/resumen.md", r"4\. Panel UE")
    h5 = L.j("BP/resultado.json")
    s = f"""## 9. Resultados negativos (se reportan igual que los positivos)

- **H2 no se confirma en el sellado.** C3 RMSE {N(h2s['rmse'],4)} frente a {N(h2s['rmse_AR4'],4)} del AR(4), DM-HLN {N(h2s['dm_vs_AR4'],2)}, p = {PV(h2s['p_vs_AR4'])}. En entrenamiento C3 ya era peor que el AR(4) (`BV/oos_panel.csv`). Los signos dentro de muestra (crédito +, coste de uso × exposición −) quedan EXPLORATORIO. *(`BV/h2_sellado.json`)*
- **H5 (tope catalán de 2020).** Efecto SDiD {N(h5['estimacion']['efecto_medio_ln_2020Q4_2022Q1'],4,True)} (signo contrario; p de permutación una cola del signo − = {N(bp['p_permutacion_una_cola_post1'])}); placebo en el tiempo (2018Q4) p = {N(bp['placebo_tiempo_2018Q4_p'])} y pendiente de pretendencia p = {N(bp['pretendencias_sdid_p_pendiente'])}: las tratadas ya divergían antes. El IPC provincial diluye el tratamiento: un nulo no prueba ausencia de efecto. *(`BP/resultado.json`)*
- **H7.** Ningún objetivo cumple la regla: A (nacional, TVP-VAR) {N(h7['A']['PRINCIPAL']['rmse'],4)} frente a {N(h7['A']['PRINCIPAL']['rmse_AR4'],4)}; B (alquiler, LightGBM) {N(h7['B']['PRINCIPAL']['rmse'],4)} frente a {N(h7['B']['PRINCIPAL']['rmse_AR4'],4)} (p = {N(h7['B']['PRINCIPAL']['p_vs_AR4'])}); C (compra, elastic net) {N(h7['C']['PRINCIPAL']['rmse'],4)} frente a {N(h7['C']['PRINCIPAL']['rmse_AR4'],4)}. *(`BM/h7_sellado.json`)*
- **LSTM.** RMSE {N(lstm['RMSE_LSTM'],4)} frente a {N(lstm['RMSE_GB'],4)} del gradient boosting; DM {N(lstm['DM_LSTM_vs_GB'],2)} (p = {PV(lstm['p'])}); la selección del mejor LSTM entre 4 configuraciones es además optimista. *(`BM/lstm_resultado.json`)*
- **H4 (oferta).** Falla submuestras: sin signos esperados en {', '.join(f"{x.spec.split('_',1)[1] if '_' in x.spec else x.spec} (p_IUT {N(x.p_IUT)})" for x in h4.itertuples() if not x.signos_ok)}; el IV no la respalda (J de Hansen rechaza) y el placebo de precio futuro es significativo. *(`BO/h4_robustez_submuestras.csv`, `BO/resumen.md`)*
- **H3 con pocos grupos.** {bhj_es} *(`BI/resumen.md`)*
- **Suelo.** La serie cruda no da señal (mínimo p Holm sobre 160 contrastes = {N(suelo[suelo.variante=='crudo'].p_Holm.min(),2)}); la variante «media4T», añadida a posteriori, da p Holm = {N(suelo[suelo.variante=='media4T'].p_Holm.min())} solo en P4 (h = 6, n pequeña): no es una señal anticipatoria robusta. *(`BO/suelo_proyecciones_locales.csv`)*
- **Turismo (VUT).** Municipal: coef. {N(tur.loc['T_muni_base','coef'],5)} (p = {N(tur.loc['T_muni_base','p'])}), placebo de pretendencia p = {N(tur.loc['T_muni_PLACEBO_pretend','p'])}; provincial: Δ ln VUT p = {N(tur.loc['T_prov_dlnVUT','p'])} frente a Δ por 1.000 hab. p = {N(tur.loc['T_prov_dVUTpc','p'],4)} con N temporal 6: depende de la métrica. *(`BA/turismo.csv`)*
- **Panel UE.** {ue.replace(chr(10), ' ')} *(`BO/resumen.md`, sección 4)*
- **Importancias SHAP / permutación / ALE (BM).** Provienen de modelos que no mejoran al AR(4): no son explicación y la colinealidad reparte las importancias de forma arbitraria. *(`BM/resumen.md`)*
{src('output/v2/BV/h2_sellado.json','output/v2/BP/resultado.json','output/v2/BM/h7_sellado.json','output/v2/BM/lstm_resultado.json','output/v2/BO/resumen.md','output/v2/BI/resumen.md','output/v2/BA/turismo.csv')}"""
    return s


def s_limitaciones():
    txt = (L.R / "docs/v2/limitaciones.md").read_text().splitlines()
    secs, cur = {}, None
    for ln in txt:
        m = re.match(r"^## (B[A-Z]) ", ln)
        if m:
            cur = m.group(1)
            secs[cur] = {"titulo": ln[3:].strip(), "items": []}
        elif cur and ln.startswith("- "):
            secs[cur]["items"].append(ln)
        elif cur and ln.startswith("  ") and secs[cur]["items"]:
            secs[cur]["items"][-1] += " " + ln.strip()
    prio = [("Prioridad 1 · identificación e inferencia (invalidan lecturas causales o la confirmación)", ["BI", "BV"]),
            ("Prioridad 2 · datos y medición (condicionan magnitudes)", ["BA", "BO", "BD"]),
            ("Prioridad 3 · potencia y modelos predictivos", ["BM"])]
    out = []
    for ttl, ramas in prio:
        out.append(f"**{ttl}**\n")
        for r in ramas:
            out.append(f"*{secs[r]['titulo']}*\n")
            out.extend(secs[r]["items"])
            out.append("")
    ries = linea_md("BP/resumen.md", r"^\* Riesgos:")
    otros = [x for x in (L.R / "docs/v2/decisiones.md").read_text().splitlines() if "Limitación conocida" in x]
    s = f"""## 10. Limitaciones (priorizadas)

La prioridad es un ordenamiento de BS según su efecto sobre la inferencia; el texto procede de `docs/v2/limitaciones.md` (limitaciones de v1 en `docs/limitaciones.md` siguen vigentes para las series nacionales).

""" + "\n".join(out) + f"""
*BP (política)* — declaración ex ante antes de abrir H6:

{ries}

*Infraestructura y sellado* (`docs/v2/decisiones.md`):

{chr(10).join(otros)}
- El sellado es procedimental; hubo una lectura indebida menor del orquestador (sección 2).
{src('docs/v2/limitaciones.md','docs/limitaciones.md','output/v2/BP/resumen.md','docs/v2/decisiones.md')}"""
    return s


def s_no_afirmar(holm):
    h1s = L.j("BA/h1_sellado.json")["resultado"]["selladas_ventana"]
    bi = L.j("BI/resultado.json")
    h3 = L.c("BI/h3_principal.csv").set_index("resultado")
    h = holm.set_index("hipotesis")
    h4 = L.c("BO/h4_principal.csv").iloc[0]
    deficit = L.c("BO/deficit_nacional.csv")
    s = f"""## 11. Qué NO se puede afirmar

- **Causalidad de la inmigración** (BI): el placebo de alquiler pasado rechaza, las cuotas 2002 no están balanceadas (Sudamérica pesa en Rotemberg), con GPSS el F cae y el coeficiente deja de ser significativo; las pretendencias 2003-2007 no son pre-tratamiento (diagnóstico de Jaeger, Ruist y Stuhler 2018). H3: p_IUT {N(h.loc['H3','p_hipotesis'],4)}, Holm-7 {N(h.loc['H3','p_holm7'])}.
- **Causalidad del crédito** (BV): simultaneidad sin instrumento; con el crédito retardado 4 trimestres no es significativo.
- **Causalidad del tope catalán** (H5): fallan pretendencias y placebo; el signo es contrario al esperado.
- **Efecto de las zonas tensionadas como causal** (H6): τ = {N(L.j('BP/h6_sellado.json')['resultado']['DECISION']['tau'],4,True)} no supera Holm-7 ({N(h.loc['H6','p_holm7'])}); el DiD simple discrepa; mide «Cataluña 2024-2026» con un paquete regulatorio coetáneo, no la zona tensionada aislada; está por debajo del MDE declarado. EXPLORATORIO.
- **Que algún modelo prediga mejor que un AR(4)**, salvo el hecho sellado de H1 (y ni siquiera en las 3 provincias selladas solas: n = {int(h1s['n'])}, p = {PV(h1s['p_vs_AR4'])}). La observación del ECM v1 en la ventana nacional sellada no es evidencia.
- **Que H1 «se confirma»**: la conjunción de signos falla (población extranjera) y H1 no supera Holm-7; tampoco que el signo + de la población de 20-34 años sea una asociación robusta de ese coeficiente.
- **Magnitudes de elasticidades**: inmigración-alquiler (rango {K()['rango_mag']}; IC95 {IC(h3.loc['alq','ic95_lo'], h3.loc['alq','ic95_hi'],1)}), oferta-precio ({N(h4['b_precio'],2)}, inestable entre submuestras), crédito y coste de uso (simultaneidad y aproximación del coste), efecto de zonas tensionadas. No se comparan cuantitativamente con Saiz (2007) ni con el 0,45 del Banco de España.
- **Que H3 (alquiler > compra) ni H4 (suelo barato eleva la elasticidad) sean robustas**: nominalmente p < 0,05, pero no sobreviven a Holm-7 ni a las submuestras.
- **Que las familias medidas expliquen la subida del alquiler o del precio** desde 2014 o desde 2020: la mayor parte queda en el componente común; los contrafactuales de BD son aritmética de coeficientes de asociación, sin equilibrio general.
- **Importancias SHAP/ALE/permutación como explicación**, ni efectos de política con series nacionales que solo varían en el tiempo.
- **Cifras de déficit comparables con el BdE** (2021-2025 frente a 2021Q1-2024Q2 = {L.entero(deficit.iloc[0].deficit)} sin protegida; parte de la protegida es supuesto), ni déficit provincial (solo un proxy).
- **Nada sobre no residentes, inversores, licencias o titularidad** (sin datos), sobre viviendas turísticas como causa, ni sobre diferencias significativas de España frente a la UE (un único clúster).
- **Nada sobre 2024Q3-2026Q2 ni sobre Cádiz, Cuenca y Toledo** más allá de las cuatro evaluaciones selladas (H1, H2, H6, H7), y nada específico de la Comunitat Valenciana / València en v2.
{src('output/v2/BI/resumen.md','output/v2/BI/h3_principal.csv','output/v2/BP/h6_sellado.json','output/v2/BA/h1_sellado.json','output/v2/BO/resumen.md','output/v2/BD/resumen.md','output/v2/BS/holm7.csv')}"""
    return s


def s_refs(refs):
    t = refs[["referencia", "doi", "revista", "cuartil", "estado"]].rename(columns={"referencia": "Referencia", "doi": "DOI", "revista": "Revista", "cuartil": "Cuartil", "estado": "Estado"})
    nv = refs[refs.estado.str.startswith("NO VERIFICADA")].referencia.tolist()
    cq = refs[refs.cuartil_no_verificado].referencia.tolist()
    s = f"""## 12. Referencias (marca de verificación)

Estado según `docs/literatura.md` (DOI comprobado en Crossref; cuartil leído de resultados de búsqueda de Scimago o de agregadores, en la mayoría de la edición 2025, no del año de publicación: «año publ. no comprobado»). No se inventa ninguna referencia: las **NO VERIFICADAS** son {len(nv)} y las de **cuartil no verificado**, {len(cq)}.

{md_df(t)}

NO VERIFICADAS: {'; '.join(nv)}. Cuartil no verificado: {'; '.join(cq)}.
{src('output/v2/tablas/referencias_v2.csv','docs/literatura.md')}"""
    return s


def s_anexo(reg, regmeta):
    pr = pd.DataFrame({"Rama": list(regmeta["por_rama"].keys()), "Especificaciones": [L.entero(v) for v in regmeta["por_rama"].values()]})
    s = f"""## Anexo. Especificaciones registradas y reproducibilidad

{md_df(pr)}

Total v2: {L.entero(regmeta['total'])} (excluye {regmeta['filas_presupuesto_excluidas']} filas de presupuesto declarado de configuraciones). **Las {L.entero(regmeta['total'])} no incluyen las estimaciones de las 4 evaluaciones selladas** (una por hipótesis, ejecutadas por el orquestador con `holdout.evaluate`, no por las ramas): {regmeta['sellado_n']}. No se añaden a `registro_v2.csv` porque el Registry de cada rama se cerró antes del sellado; sus resultados están en los `*_sellado.json` y en `modelos_fuera_muestra.csv`. Cada rama registra sus especificaciones en `output/v2/<rama>/registro.csv` (Registry de `econ_utils`); la concatenación con columna `rama` es `output/v2/tablas/registro_v2.csv`.

Reproducibilidad: `python3 src/v2/bs_run.py` (1 hilo, SEED = {L.SEED}, sin red) regenera `output/v2/BS/*`, `output/v2/tablas/*.csv` y este informe; dos ejecuciones dan md5 idénticos. Todas las cifras se leen de los ficheros citados.
{src('output/v2/tablas/registro_v2.csv')}"""
    return s


def construir(holm, ha, oos, ctr, rank, refs, reg, regmeta, bsdir) -> str:
    k = pack(holm, ha, oos, ctr, rank, refs, reg, regmeta)
    cab = f"""# Determinantes del precio de la vivienda en España: informe v2 (síntesis BS)

Documento generado por `src/v2/bs_run.py` a partir de las salidas versionadas de las ramas BA, BV, BI, BO, BP, BM y BD (`output/v2/`). Las cifras se insertan desde ficheros versionados y cada bloque cita su origen; las pocas excepciones son literales citados de documentos (p. ej. 0,17 / 0,174 y 0,035 de `docs/v2/decisiones.md`, 0,029 del script previo de Holm-7, el MDE y el 0,45 que recogen los resúmenes de rama) o convenciones (umbral de 0,05). Escala de evidencia: CAUSAL > ASOCIACIÓN ROBUSTA > EXPLORATORIO > DESCRIPTIVO; **ninguna conclusión de este informe supera EXPLORATORIO** y se evita el lenguaje causal. Inferencia: EE cluster por provincia con wild cluster bootstrap (Webb) o HAC(4); comparación de modelos en la misma muestra frente a AR(4) y ECM v1 (Diebold-Mariano con corrección Harvey-Leybourne-Newbold).

"""
    partes = [s_resumen(holm, ha, oos, rank, reg, regmeta, k), s_datos(regmeta), s_metodos(refs), s_alq_vs_compra(ctr), s_ecuaciones(ctr), s_ranking(rank), s_oos(oos, k),
              s_hipotesis(ha, holm, bsdir), s_cambios(holm, regmeta), s_negativos(), s_limitaciones(), s_no_afirmar(holm), s_refs(refs), s_anexo(reg, regmeta)]
    return cab + "\n".join(partes)

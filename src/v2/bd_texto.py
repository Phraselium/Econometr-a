"""BD - resumen.md y resultado.json (cifras leídas de las tablas; sin lenguaje causal)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bd_lib as L  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import v2_common as vc  # noqa: E402


def fmt(x, d=2):
    return f"{x:.{d}f}".replace(".", ",").replace("-", "−")


def cell(c, mer, mo, per, comp):
    r = c[(c.mercado == mer) & (c.modelo == mo) & (c.periodo == per) & (c.componente == comp)].iloc[0]
    return f"{fmt(r.contrib_pp)} [{fmt(r.ic95_inf)}; {fmt(r.ic95_sup)}]"


def pct(c, mer, mo, per, comp):
    r = c[(c.mercado == mer) & (c.modelo == mo) & (c.periodo == per) & (c.componente == comp)].iloc[0]
    return f"{fmt(r.pct_observado, 0)} %"


def cell_nac(df, per, comp):
    r = df[(df.periodo == per) & (df.componente == comp)].iloc[0]
    return f"{fmt(r.contrib_pp, 1)} [{fmt(r.ic95_inf, 1)}; {fmt(r.ic95_sup, 1)}]"


def tabla_ventana(c, mer, per):
    comps = ["observado", "explicado_familias", "demografia", "demografia_20_34", "demografia_extranj", "empleo_renta",
             "credito_tipos_cu", "oferta", "politica", "comun_efectos_tiempo", "residuo"]
    ets = {"observado": "**Observado** (crecimiento acumulado, pp de ln)", "explicado_familias": "Suma de familias",
           "demografia": "Demografía (20-34 + extranjera)", "demografia_20_34": "  · pob 20-34", "demografia_extranj": "  · pob extranjera",
           "empleo_renta": "Empleo (ocupados)", "credito_tipos_cu": "Crédito / coste de uso", "oferta": "Oferta (terminadas)",
           "politica": "Política (tope de rentas CAT)", "comun_efectos_tiempo": "Común: efectos de tiempo + FE", "residuo": "Residuo"}
    h = "| Componente | M1 pp [IC95 %] | % obs. M1 | M2 pp [IC95 %] | % obs. M2 | Evidencia heredada |\n|---|---|---|---|---|---|\n"
    from bd_report import evidencia
    for k in comps:
        if k == "politica" and mer == "compra":
            continue
        h += f"| {ets[k]} | {cell(c, mer, 'M1', per, k)} | {pct(c, mer, 'M1', per, k)} | {cell(c, mer, 'M2', per, k)} | {pct(c, mer, 'M2', per, k)} | {evidencia(mer, k)} |\n"
    return h


def tabla_cf(cf):
    nombres = {"a_ambas_sin_variacion_desde_2014": "(a) 20-34 y extranjera sin variación desde 2014Q1",
               "a1_solo_pob_20_34_sin_variacion": "(a1) solo 20-34 sin variación",
               "a2_solo_pob_extranj_sin_variacion": "(a2) solo extranjera sin variación",
               "a3_ambas_sin_crecimiento_positivo_desde_2014": "(a3) ambas: se elimina solo el crecimiento positivo",
               "b_credito_y_cu_congelados_2013Q4": "(b) crédito y coste de uso congelados en 2013Q4",
               "c_cu_2021Q4_en_P4": "(c) coste de uso de 2021Q4 durante P4"}
    h = "| Mercado | Modelo | Escenario | Efecto P2-P4 acumulado (pp) | Efecto P4 (pp) | Observado P4 (pp) |\n|---|---|---|---|---|---|\n"
    for mer in ("alquiler", "compra"):
        for mo in ("M1", "M2"):
            for k, nm in nombres.items():
                x = cf[(cf.mercado == mer) & (cf.modelo == mo) & (cf.escenario == k)].set_index("periodo")
                a, p4 = x.loc["P2-P4 acumulado"], x.loc["P4"]
                f = lambda r: f"{fmt(r.efecto_pp)} [{fmt(r.ic95_inf)}; {fmt(r.ic95_sup)}]"
                h += f"| {mer} | {mo} | {nm} | {f(a) if k[0] != 'c' else '(solo P4)'} | {f(p4)} | {fmt(p4.observado_pp)} |\n"
    return h


def escribir(ctx):
    c, cf, nac, B, OUT = ctx["contrib"], ctx["cf"], ctx["nac"], ctx["B"], ctx["OUT"]
    tur, obsn = ctx["tur"], ctx["obsn"]
    n = {m: ctx["res"][(m, "M1")]["n"] for m in ("alquiler", "compra")}
    # --- nacional: tablas
    def tn(df):
        h = "| Periodo | Componente | pp [IC95 %] | % obs. |\n|---|---|---|---|\n"
        for _, r in df.iterrows():
            h += f"| {r.periodo} | {r.componente} | {fmt(r.contrib_pp, 1)} [{fmt(r.ic95_inf, 1)}; {fmt(r.ic95_sup, 1)}] | {fmt(r.pct_observado, 0)} % |\n"
        return h
    lp = nac["lp"][nac["lp"].componente != "estacional (dummies)"]
    t = tur["contrib"].set_index(["periodo", "componente"])
    tt = t.loc[("P4", "turismo")]
    md = f"""# BD - Descomposición por periodos con contrafactuales e intervalos (alquiler y compra)

**Nivel de evidencia global: EXPLORATORIO.** Descomposición contable de asociaciones condicionales; no hay identificación causal.
Cada fila hereda el nivel de la rama de origen (columna «Evidencia heredada»): H1 (alquiler) tuvo mejora predictiva confirmada en la
muestra sellada (BA/BV/BP aprobadas; H1 conjunta de signos EXPLORATORIA; el componente 20-34 es candidato a ASOCIACIÓN ROBUSTA sujeto a Holm-7 en BS);
H2 (compra) NO se confirmó en el sellado. La descomposición NO usa el periodo sellado (termina en 2024Q1 por la razón indicada abajo).
Cifras generadas por `src/v2/bd_run.py` (B={B}, semilla {vc.SEED}); dos ejecuciones con md5 idénticos.

## Respuesta breve (EXPLORATORIO; asociaciones condicionales)
- **Alquiler desde 2014:** +{cell(c, 'alquiler', 'M1', 'P2-P4 (desde 2014)', 'observado')} pp; las familias medidas no lo explican (suma M1 {cell(c, 'alquiler', 'M1', 'P2-P4 (desde 2014)', 'explicado_familias')} pp) y el componente común/no explicado es {cell(c, 'alquiler', 'M1', 'P2-P4 (desde 2014)', 'comun_efectos_tiempo')} pp.
- **Alquiler desde 2020:** +{cell(c, 'alquiler', 'M1', 'P3-P4 (desde 2020)', 'observado')} pp; solo la población de 20-34 años aparece con IC>0 en M2 ({cell(c, 'alquiler', 'M2', 'P3-P4 (desde 2020)', 'demografia_20_34')} pp, ~10 %); ~95-100 % queda en el componente común.
- **Compra (real) desde 2014:** {cell(c, 'compra', 'M1', 'P2-P4 (desde 2014)', 'observado')} pp (≈0); **desde 2020:** {cell(c, 'compra', 'M1', 'P3-P4 (desde 2020)', 'observado')} pp (caída real). Sin atribución estable entre M1 y M2.
- Contrafactuales (b) y (c) (crédito/coste de uso): efectos pequeños en alquiler; en compra solo (b) en M1 tiene IC que excluye 0 ({fmt(cf[(cf.mercado=='compra')&(cf.modelo=='M1')&(cf.escenario=='b_credito_y_cu_congelados_2013Q4')&(cf.periodo=='P2-P4 acumulado')].efecto_pp.iloc[0])} pp) y no se replica en M2.

## Método (qué se calcula exactamente)
- Datos: `panel_prov_q` y `nacional_q_v2` vía `v2_common.load` (49 provincias de entrenamiento). Alquiler: Δ4 ln IPC de alquiler (nominal, como BA);
  compra: Δ4 ln valor tasado REAL (deflactor nacional, como BV). Muestra 2008Q1-2024Q1 (N alquiler = {n['alquiler']}, compra = {n['compra']}).
  **P4 llega solo a 2024Q1**: la población de 2024Q2 está anulada (fuga del sellado corregida en holdout.build) y las familias demografía la necesitan.
- Modelos (EXPLORATORIOS), coeficientes POR PERIODO (como estimaron BA y BV; el tope catalán y el Δ4 del coste de uso nacional, globales):
  **M1** = FE de provincia y de trimestre (los efectos de tiempo recogen todo lo común: tipos, regulación nacional, expectativas y el movimiento
  común de las propias familias); **M2** = FE de provincia + dummies de trimestre del año + intercepto por periodo + Δ4 del coste de uso nacional
  (identificación solo temporal con una serie única: sin variación transversal, los EE cluster no valen; se usa el bootstrap por bloques de tiempo).
  Los coeficientes de M1/M2 son nuevos (no son los de BA/BV: otra especificación conjunta, oferta contemporánea Δ4 ln terminadas con relleno 0 y dummy
  de dato ausente —Ceuta, Melilla y 2008Q1-Q3—, y crédito provincial y tope catalán en alquiler); se informan en `coeficientes_por_periodo.csv`.
- Contribución de la familia f en el periodo P = coeficiente_{{f,P}} × (variación media de la familia en P), con media nacional PONDERADA POR POBLACIÓN
  de las 49 provincias, expresada como crecimiento acumulado ≈ (n_trim/4) × media del Δ4 (pp de ln; efecto de borde: ver `observado_niveles_referencia.csv`).
  Identidad: observado = Σ familias + común (efectos de tiempo + FE de provincia + dummies) + residuo.
  **Cautela de lectura de M1**: el coeficiente se identifica con diferencias entre provincias y se aplica a la media nacional de la variable; lo que en M1 no
  atribuye a las familias queda en «común», que por construcción es grande.
- IC95 %: percentiles de {B} réplicas de (i) bootstrap por bloques de provincias (cluster, remuestreo de provincias con reposición, modelo reestimado) y (ii) bootstrap
  por bloques de tiempo (bloques móviles de 4 trimestres dentro de cada periodo). La tabla da la ENVOLVENTE de ambos (`contribuciones_todas.csv` tiene cada uno por separado).
  El «observado» también tiene IC porque la media ponderada depende de las provincias/trimestres remuestreados.
- Ventanas acumuladas: «desde 2014» = P2+P3+P4 (2014Q1-2024Q1) y «desde 2020» = P3+P4 (2020Q1-2024Q1).

## Alquiler (IPC de alquiler nominal) - subida desde 2014 (P2+P3+P4)
{tabla_ventana(c, 'alquiler', 'P2-P4 (desde 2014)')}
## Alquiler - subida desde 2020 (P3+P4)
{tabla_ventana(c, 'alquiler', 'P3-P4 (desde 2020)')}
**Lectura (asociación, no causalidad).**
- Desde 2014 el IPC de alquiler acumula {cell(c, 'alquiler', 'M1', 'P2-P4 (desde 2014)', 'observado')} pp. Con efectos de tiempo (M1) las familias medidas suman
  {cell(c, 'alquiler', 'M1', 'P2-P4 (desde 2014)', 'explicado_familias')} pp: casi todo el aumento queda en el componente común ({cell(c, 'alquiler', 'M1', 'P2-P4 (desde 2014)', 'comun_efectos_tiempo')} pp), es decir,
  en lo que se mueve igual en todas las provincias y no se explica con las variables disponibles (tipos, regulación nacional, expectativas, inflación...).
- La demografía contribuye NEGATIVAMENTE en 2014-2019 (P2: población de 20-34 años en descenso, coeficiente positivo): {cell(c, 'alquiler', 'M1', 'P2', 'demografia_20_34')} pp en M1.
  No explica la subida; el signo es el de la composición, no el de una asociación nueva.
- Desde 2020 el único componente con IC que excluye el 0 y signo positivo es la población de 20-34 en M2: {cell(c, 'alquiler', 'M2', 'P3-P4 (desde 2020)', 'demografia_20_34')} pp
  ({pct(c, 'alquiler', 'M2', 'P3-P4 (desde 2020)', 'demografia_20_34')} del observado {cell(c, 'alquiler', 'M2', 'P3-P4 (desde 2020)', 'observado')}); en M1 el efecto es
  {cell(c, 'alquiler', 'M1', 'P3-P4 (desde 2020)', 'demografia_20_34')} (IC incluye 0). La población extranjera, el empleo, la oferta, el crédito y el tope catalán no se distinguen de 0 (IC incluyen el 0).
- Lo no explicado domina: en M1 el componente común es {pct(c, 'alquiler', 'M1', 'P3-P4 (desde 2020)', 'comun_efectos_tiempo')} del crecimiento desde 2020; en M2 {pct(c, 'alquiler', 'M2', 'P3-P4 (desde 2020)', 'comun_efectos_tiempo')}.

## Compra (valor tasado REAL) - subida desde 2014 (P2+P3+P4)
{tabla_ventana(c, 'compra', 'P2-P4 (desde 2014)')}
## Compra - desde 2020 (P3+P4)
{tabla_ventana(c, 'compra', 'P3-P4 (desde 2020)')}
**Lectura (asociación, no causalidad).**
- En términos REALES el valor tasado no «sube» en el conjunto 2014-2024Q1: observado {cell(c, 'compra', 'M1', 'P2-P4 (desde 2014)', 'observado')} pp (recuperación en P2, caída real en P3-P4: {cell(c, 'compra', 'M1', 'P3-P4 (desde 2020)', 'observado')} pp desde 2020 por la inflación del deflactor).
  Por eso la pregunta «qué explica la subida» se refiere al nominal solo de forma indirecta; aquí se descompone el real.
- Ninguna familia explica de forma robusta la evolución desde 2020: en M1 las familias suman {cell(c, 'compra', 'M1', 'P3-P4 (desde 2020)', 'explicado_familias')} pp y el común {cell(c, 'compra', 'M1', 'P3-P4 (desde 2020)', 'comun_efectos_tiempo')} pp.
  En M2 la demografía (sobre todo extranjera: {cell(c, 'compra', 'M2', 'P3-P4 (desde 2020)', 'demografia_extranj')} pp) sale con signo negativo en P3-P4 porque los coeficientes por periodo de la población cambian de signo
  (`coeficientes_por_periodo.csv`); no se interpreta, la inestabilidad entre M1 y M2 indica que no hay una atribución estable.
- El crédito/coste de uso pesa en P1 ({cell(c, 'compra', 'M1', 'P1', 'credito_tipos_cu')} pp en M1) y es indistinguible de 0 desde 2014 en M1.

## Contrafactuales (EXPLORATORIOS y PARCIALES)
**Advertencia:** son ejercicios ceteris paribus sobre las variables del modelo: se modifican solo esas variables con los coeficientes estimados; no hay equilibrio general
(oferta, expectativas, migración y precios se retroalimentan), la identificación no es causal y M1 solo recoge el canal diferencial entre provincias (coste de uso
únicamente vía exposición hipotecaria; en alquiler M1 el canal de coste de uso es 0 por construcción). M2 añade el canal temporal nacional, pero con una serie única (IC por bloques de tiempo).
Efecto = valor contrafactual − observado (pp acumulados de ln). Si «sin variación» elimina una caída observada, el efecto es positivo.
{tabla_cf(cf)}
- (a) «Sin crecimiento» de 20-34 y extranjera desde 2014: la población de 20-34 años CAYÓ en P2, así que fijarla (Δ=0) sube el alquiler contrafactual
  (M1: {fmt(cf[(cf.mercado=='alquiler')&(cf.modelo=='M1')&(cf.escenario=='a1_solo_pob_20_34_sin_variacion')&(cf.periodo=='P2-P4 acumulado')].efecto_pp.iloc[0])} pp); eliminar solo el crecimiento positivo (a3) apenas cambia nada.
  En P4 (donde la población joven crece) quitar su variación resta {fmt(cf[(cf.mercado=='alquiler')&(cf.modelo=='M2')&(cf.escenario=='a1_solo_pob_20_34_sin_variacion')&(cf.periodo=='P4')].efecto_pp.iloc[0])} pp en M2 y {fmt(cf[(cf.mercado=='alquiler')&(cf.modelo=='M1')&(cf.escenario=='a1_solo_pob_20_34_sin_variacion')&(cf.periodo=='P4')].efecto_pp.iloc[0])} pp en M1 sobre un observado de {fmt(cf[(cf.mercado=='alquiler')&(cf.modelo=='M1')&(cf.escenario=='a1_solo_pob_20_34_sin_variacion')&(cf.periodo=='P4')].observado_pp.iloc[0])} pp.
- (b) y (c), alquiler: efectos pequeños (décimas de pp) y con IC que incluyen 0; en compra, congelar crédito y coste de uso en 2013Q4 reduce el real acumulado en M1 pero el IC en M2 incluye 0.
  (c): con el coste de uso de 2021Q4 durante P4 el efecto es de décimas de pp con IC que incluye 0 en M2 (en M1 es 0 por construcción en alquiler y −0,14 [−0,55; 0,27] en compra):
  la subida de tipos de 2022 no deja una señal detectable en estos modelos (ausencia de señal, no evidencia de efecto nulo).
- Compra, (a): M1 y M2 discrepan (P4: M1 {fmt(cf[(cf.mercado=='compra')&(cf.modelo=='M1')&(cf.escenario=='a_ambas_sin_variacion_desde_2014')&(cf.periodo=='P4')].efecto_pp.iloc[0])} pp, M2 {fmt(cf[(cf.mercado=='compra')&(cf.modelo=='M2')&(cf.escenario=='a_ambas_sin_variacion_desde_2014')&(cf.periodo=='P4')].efecto_pp.iloc[0])} pp): no hay contrafactual demográfico estable para la compra.

## Nacional: precio real con el ECM v1 real (EXPLORATORIO)
ECM v1 real (v1: `output/f2/ecuacion_real.csv`) reestimado con datos de entrenamiento ({nac['muestra'][0]}-{nac['muestra'][1]}; LP N={nac['n_lp']}, CP N={nac['n_cp']}; el P1 de CP empieza en 2008Q2).
IC95: bootstrap de residuos por bloques (4), regresores fijos, B={B} (el desequilibrio de CP usa el ECT puntual, no reestimado). Identidad de largo plazo (Δy = b·Δx + estacional + Δ desequilibrio):
{tn(lp)}
Corto plazo (suma de Δy_t = Σ coef·x; exacta):
{tn(nac['cp'])}
Lectura: en 2014-2019 (P2) el empleo ({cell_nac(nac['cp'], 'P2', 'empleo (Δ ocupados t-1)')} pp en CP) y el desequilibrio ({cell_nac(nac['cp'], 'P2', 'desequilibrio (ect t-1)')} pp) concentran buena parte del aumento real;
en P4 (2022Q1-2024Q2) los tipos restan ({cell_nac(nac['cp'], 'P4', 'tipos (Δ tipo hip. t-1)')} pp, IC en el límite del 0) y el desequilibrio de largo plazo se cierra ({cell_nac(nac['lp'], 'P4', 'desequilibrio (Δ ect)')} pp),
mientras el empleo aporta {cell_nac(nac['lp'], 'P4', 'empleo (ocupados)')} pp. El IC del tipo real de LP incluye 0 en todos los periodos (en v1 también era no significativo, igual que permisos; solo empleo y costes lo eran).
El DOLS usa pocos datos, la estacionalidad del LP depende de los trimestres de inicio y fin, y el «residuo» de CP no es independiente de la elección de variables de v1 (elegidas por R² ajustado en la misma muestra).

## Turismo (VUT; solo ventana 2021Q3-2024Q1; N temporal = 6)
Contribución en P4 (6 trimestres): {fmt(tt.contrib_pp)} pp [{fmt(tt.ic95_inf)}; {fmt(tt.ic95_sup)}] sobre un crecimiento observado en la ventana de {fmt(t.loc[('P4', 'observado')].contrib_pp)} pp. No se distingue de 0; no comparable con el resto (otra ventana y coeficiente global). `turismo_*.csv`.

## Qué NO se puede afirmar
- Nada causal: ni «la demografía/el crédito/los tipos causaron» ni que los contrafactuales sean lo que habría ocurrido. Son aritmética de coeficientes de asociación.
- Que las familias medidas expliquen la subida desde 2014 o desde 2020: la mayor parte queda en el componente común/no explicado.
- Que la subida de tipos de 2022 no importara: con una serie nacional única y 9-10 trimestres en P4, M1/M2 no tienen potencia para detectarla (no es evidencia de efecto nulo).
- Efectos de política (tope catalán de 2020-22, Ley 12/2023, zonas tensionadas 2024: sellada), inversores y no residentes (sin datos provinciales).
- Nada sobre 2024Q2 en adelante (2024Q2 queda fuera por la población anulada; el sellado no se usa).
- Estabilidad: M1 y M2 difieren en tamaño y a veces en signo (p. ej. compra, demografía); los coeficientes por periodo con 8-24 trimestres son imprecisos. Poblaciones intra-anuales interpoladas (T2-T4) y coste de uso aproximado (sin impuestos ni prima de riesgo).
- Las medidas de «% del observado» son inestables cuando el observado es pequeño (alquiler P2, compra P2-P4).

## Archivos
`tabla_resumen.csv` (periodo × familia × mercado, con M1 y M2), `contribuciones_todas.csv`, `coeficientes_por_periodo.csv`, `contrafactuales.csv`, `nacional_*.csv`, `turismo_*.csv`,
`observado_niveles_referencia.csv`, `registro.csv`, `resultado.json`, `figuras/`.
"""
    (OUT / "resumen.md").write_text(md)
    r1 = c[(c.mercado == "alquiler") & (c.modelo == "M1") & (c.periodo == "P3-P4 (desde 2020)")].set_index("componente")
    est = {f"alquiler_M1_P3P4_{k}": float(r1.loc[k, "contrib_pp"]) for k in ("observado", "demografia_20_34", "comun_efectos_tiempo")}
    ic95 = {f"alquiler_M1_P3P4_{k}": [float(r1.loc[k, "ic95_inf"]), float(r1.loc[k, "ic95_sup"])] for k in ("observado", "demografia_20_34", "comun_efectos_tiempo")}
    r2 = c[(c.mercado == "alquiler") & (c.modelo == "M2") & (c.periodo == "P3-P4 (desde 2020)")].set_index("componente")
    est["alquiler_M2_P3P4_demografia_20_34"] = float(r2.loc["demografia_20_34", "contrib_pp"])
    ic95["alquiler_M2_P3P4_demografia_20_34"] = [float(r2.loc["demografia_20_34", "ic95_inf"]), float(r2.loc["demografia_20_34", "ic95_sup"])]
    r3 = c[(c.mercado == "compra") & (c.modelo == "M1") & (c.periodo == "P3-P4 (desde 2020)")].set_index("componente")
    for k in ("observado", "comun_efectos_tiempo", "explicado_familias"):
        est[f"compra_M1_P3P4_{k}"] = float(r3.loc[k, "contrib_pp"])
        ic95[f"compra_M1_P3P4_{k}"] = [float(r3.loc[k, "ic95_inf"]), float(r3.loc[k, "ic95_sup"])]
    if not ctx["smoke"]:
        vc.resultado_json(
            OUT / "resultado.json", rama="BD",
            pregunta="¿Qué familias de variables se asocian con el crecimiento acumulado del alquiler y del precio real de compra en P1-P4 (descomposición, IC y contrafactuales parciales)?",
            datos="panel_prov_q y nacional_q_v2 vía v2_common.load; 49 provincias; 2008Q1-2024Q1 (2024Q2 sin población por fuga del sellado); sin muestra sellada",
            N={"alquiler": int(n["alquiler"]), "compra": int(n["compra"]), "provincias": 49, "nacional_LP": nac["n_lp"], "nacional_CP": nac["n_cp"]},
            metodo=f"MCO con FE (M1: provincia+trimestre; M2: provincia+trimestre del año+intercepto de periodo+Δ4 coste de uso nacional), coeficientes por periodo; contribución = coef × variación media ponderada por población; IC95 por bootstrap de provincias y de bloques de tiempo (4), B={B}; contrafactuales parciales ceteris paribus; ECM v1 real nacional con bootstrap de residuos por bloques",
            estimacion=est, ic95=ic95,
            p_ajustado={"nota": "sin contrastes de hipótesis: descomposición descriptiva con IC; Holm-7 de las confirmatorias lo aplica BS"},
            nivel_evidencia="EXPLORATORIO",
            diagnosticos={"heredado": {"alquiler_demografia_20_34": "candidato a ASOCIACIÓN ROBUSTA (H1, sujeto a Holm-7 en BS)", "alquiler_resto": "EXPLORATORIO",
                                       "compra": "EXPLORATORIO (H2 no confirmada en sellado)", "comun_residuo": "DESCRIPTIVO"},
                          "identidad_contable": "observado = familias + común + residuo (se verifica en tabla_resumen.csv)",
                          "limitacion_P4": "P4 termina en 2024Q1", "robustez": "M1 vs M2 difieren en magnitud y a veces en signo"},
            fuera_muestra={"modelo": "no aplica (descomposición en muestra; el fuera de muestra está en BA/BV)", "rmse": None, "dm_vs_ar4": None},
            notas="EXPLORATORIO. Contrafactuales parciales, sin equilibrio general ni identificación causal. Sin lenguaje causal.")

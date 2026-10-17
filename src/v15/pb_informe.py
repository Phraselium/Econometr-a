"""V15-B · genera output/v15/{p4,p9,p2,p7,p10}/informe.md a partir de resultado.json y multiverso.csv (sin lenguaje causal; todo C4).
Uso: python3 src/v15/pb_informe.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v15.pb_comun import OUT  # noqa: E402

PIE = ("\n## Límites\nC4 (entrenamiento), `pendiente_sellada`: true. Lenguaje de asociación. Multiplicidad (Holm en H, BH/BY en E) la aplica el orquestador con "
       "`p_valores_para_BY` de resultado.json. Desviaciones: docs/v15/desviaciones.md (DV15-B). Semilla 20261010.\n")


def g(x, n=3):
    return "n/d" if x is None else (f"{x:.{n}g}" if isinstance(x, (int, float)) else str(x))


def h4(r, mv):
    d, e = r["diagnosticos"], r["estimacion"]
    rot = ", ".join(f"{t['origen']} ({t['peso']:.2f})" for t in d["rotemberg"]["top8"][:4])
    return f"""# H4 · Inmigración y alquiler (shift-share municipal) · informe
**Resultado (puntual, sin p ni IC: AKM y AKM0 NO APTOS).** La población extranjera predicha por cuotas de origen de 2003 se asocia con un alquiler SERPAVI (VC) {g(e['beta_pp_alquiler_por_pp_poblacion_extranjera'])} % mayor por punto porcentual (OLS: {g(e['ols_pp'])} %), N = {r['N']} observaciones municipio-año, {e['n_municipios']} municipios, 2012-2022, efectos provincia × año. Instrumento sin UE-14 residenciales. Capa C4; pendiente de evaluación sellada (2022→2025).

## Ficha reproducible {{#beta}}
`python3 src/v15/p4_inmigracion.py`. Δlog alquiler(t) sobre 100·ΔPobExt(t)/Pob(t−1); instrumento Σ_k cuota_k,2003 · g_kt (leave-one-out), 28 países menos Alemania, Francia, Italia, Portugal y Reino Unido. Multiverso (64): β entre {g(mv.beta_pp.min()*100)} y {g(mv.beta_pp.max()*100)} % por p.p., mediana {g(mv.beta_pp.median()*100)}; signo positivo en {g(100*(mv.beta_pp>0).mean(),3)} % de las especificaciones.

## Primera etapa {{#F}}
F robusto HC1 (descriptivo): {g(e['F_robusto'])} (rango en el multiverso {g(mv.F_robusto.min())}–{g(mv.F_robusto.max())}). El procedimiento MOP/AR/AKM no es APTO; no se declara instrumento fuerte ni débil por inferencia. V9-D4 (provincial, IPC/valor tasado) tuvo F 2,8–4,6: no es comparable (otro nivel y otra medida).

## Rotemberg {{#rotemberg}}
Orígenes de mayor peso: {rot}. Número efectivo de choques (1/HHI): {g(d['rotemberg']['n_efectivo_choques_1_sobre_HHI'])}.

## Diagnósticos (descriptivos)
- Pretendencias SERPAVI 2011-2013 frente al instrumento medio: pendiente {g(d['pretendencias_2011_2013']['pendiente_dlog_por_pp_z'])}, correlación {g(d['pretendencias_2011_2013']['correlacion'])}.
- Balance 2003: corr con log población {g(d['balance_2003']['corr_z_logpob03'])}, con cuota extranjera {g(d['balance_2003']['corr_z_cuota_ext03'])}.
- Instrumento retardado (JRS): β {g(d['jaeger_ruist_stuhler_control_z_retardado']['beta_pp']*100)} %; sin 5 orígenes de mayor peso: {g(d['excluye_5_origenes_Rotemberg']['beta_pp']*100)} %; desbordamiento 15 km: {g(d['desbordamiento_15km']['beta_propio_pp']*100)} %; sin Barcelona y València: {g(d['excluye_Barcelona_Valencia']['beta_pp']*100)} %; sin 1 % superior de exposición: {g(d['excluye_1pct_superior_exposicion']['beta_pp']*100)} %; 28 orígenes: {g(d['instrumento_28_origenes']['beta_pp']*100)} %.
- Fallidas/no evaluables: AKM, AKM0 y agrupación por provincia (NO APTOS); evaluación sellada (pendiente); TOST (sin inferencia).
{PIE}"""


def h5(r, mv):
    d = r["diagnosticos"]
    t = d["ECM_por_modelo"]
    fila = "\n".join(f"| {m} | {v['rmse']:.5f} | {v['razon_ecm_vs_AR4']:.2f} |" for m, v in t.items())
    dm = d["DM_HLN_vs_AR4_unilateral"]["Combinacion"]
    return f"""# H5 · Predicción frente al AR(4) y al ECM v1 · informe
**Resultado.** Con {d['muestra_errores']['P']} errores de entrenamiento ({d['muestra_errores']['primer_origen_objetivo']}–{d['muestra_errores']['ultimo']}, h = 1), la combinación tiene una razón de ECM de {g(t['Combinacion']['razon_ecm_vs_AR4'])} frente al AR(4); DM-HLN unilateral: DM = {g(dm['dm'])}, p = {g(dm['p_unilateral'])}. Ningún modelo de la lista supera al AR(4); la línea base K1 de menor ECM es {d['linea_base_K1']['base']}. Predicción, sin lectura causal. Evaluación sellada: octubre de 2027.

## Ficha reproducible {{#razon}}
`python3 src/v15/p9_prediccion.py`. Ventana expansiva; AR(4), ECM v1 reconstruido (DV15-B-2), paseo con deriva, DFM, BVAR, LASSO y ARDL sobre la misma muestra.

| modelo | RMSE | razón ECM / AR(4) |
|---|---|---|
{fila}

## DM-HLN {{#dm}}
Combinación frente a AR(4): p unilateral {g(dm['p_unilateral'])}; frente al ECM v1: p {g(d['DM_HLN_vs_ECMv1_unilateral']['Combinacion']['p_unilateral'])}; frente a la base K1: p {g(d['linea_base_K1']['dm_combinacion_vs_base']['p_unilateral'])}. Sin 2020T2-T3: p {g(d['robustez_sin_2020T2_T3']['p_unilateral'])}.

## MCS y otros contrastes (descriptivos)
MCS 10 %: {', '.join(d['MCS']['al_10pct_descriptivo'])}. Clark-West y GW: no se calculan (NO APTOS). Multiverso (60): {g(100*d['multiverso_60']['frac_ecm_menor_que_AR4'],3)} % de las especificaciones con ECM menor que el AR(4); razón entre {g(d['multiverso_60']['razon_min'])} y {g(d['multiverso_60']['razon_max'])}. Potencia: {d['potencia']}.
{PIE}"""


def e1(r, mv):
    d, e = r["diagnosticos"], r["estimacion"]
    cs = mv[(mv.estimador == "CS-ARDL") & (mv.medida == "tasado")]
    return f"""# E1 · Precio frente a alquiler y coste de uso (panel provincial) · informe
**Resultado (puntual; Westerlund, CIPS y CS-ARDL NO APTOS).** Elasticidad de largo plazo valor tasado–alquiler: CS-ARDL (p = 1, sin coste de uso) {g(e['theta_precio_alquiler_CS_ARDL'])}; MG y PMG dan valores distintos y de signo variable (multiverso.csv). La velocidad de ajuste del CS-ARDL ({g(e['velocidad_media'])} trimestral) no es fiable: cobertura 0,003 en el Monte Carlo. No se contrasta cointegración. Capa C4, descriptivo.

## Ficha reproducible {{#theta}}
`python3 src/v15/p2_fundamentales.py`. 36 especificaciones: {{MG, CS-ARDL, PMG}} × {{0,1,2 rezagos}} × {{con/sin coste de uso}} × {{valor tasado provincial, IPV CCAA}}. CS-ARDL tasado: θ entre {g(cs.theta_precio_alquiler_media.min())} y {g(cs.theta_precio_alquiler_media.max())}.

## Semivida {{#semivida}}
MG y PMG sin coste de uso (valor tasado): semivida mediana ≈ 3,6–4,2 años (puntual). PMG con coste de uso: no identificado (θ en el límite).

## Diagnósticos
CD de Pesaran (Δlog valor tasado): {g(d['tasado_estructura']['CD_Pesaran_dlog_precio'])} (correlación media {g(d['tasado_estructura']['correlacion_media'])}) → fuerte dependencia transversal. CIPS (estadístico, descriptivo): precio {g(d['tasado_estructura']['CIPS_log_precio_p1'])}, alquiler {g(d['tasado_estructura']['CIPS_log_alquiler_p1'])}. Fallidas: Westerlund, CIPS y CS-ARDL (NO APTOS); potencia de Westerlund frente a −0,04 no alcanzada.
{PIE}"""


def e2(r, mv):
    d = r["diagnosticos"]
    return f"""# E2 · Presión demográfica frente a obra nueva · informe
**Resultado (descriptivo, sin p ni IC).** Correlación entre el exceso de presión ((hogares nuevos − obra)/población inicial) y el Δlog del alquiler: Pearson entre {g(d['pearson_min_max'][0])} y {g(d['pearson_min_max'][1])} en {d['con_dato']} de {d['especificaciones']} especificaciones; positivas en el {g(100*d['frac_pearson_positivo'],3)} %. Caso de referencia (provincial, terminadas, hogares, SERPAVI, 2018-2024): r = {g(r['estimacion']['pearson_provincial_terminadas_hogares_SERPAVI'])}. Es una asociación entre territorios dominada por el término de demanda; no es un efecto.

## Ficha reproducible {{#pearson}}
`python3 src/v15/p7_demografia.py`. Obra neta del Catastro con el desfase de un año (obra de t = Δ unidades en t+1); hogar medio 2,5 (DV15-B-8). 8 especificaciones municipales con MIVAU no disponibles. En el nivel provincial, hogares y población coinciden salvo escala.

## Limitaciones
{'; '.join(d['limitaciones'])}.
{PIE}"""


def e3(r, mv):
    det = r["detalle"]
    fila = "\n".join(f"| {x['id']} | {x['rho_o_lambda']:.3f} | {x['se']:.3f} | {g(x['p_wald'])} | {x['n']} |" for x in det)
    return f"""# E3 · Dependencia espacial del alquiler municipal · informe
**Resultado (SAR/SEM/SDM APTO).** Hay autocorrelación espacial positiva y fuerte en el Δlog SERPAVI VC: ρ (SAR, contigüidad, 2015-2024) = {g(r['estimacion']['rho_SAR_contiguidad_2015_2024'])} (IC95 Wald {g(r['ic95'][0])}–{g(r['ic95'][1])}), N = {r['N']}. Los 12 contrastes de Wald rechazan ρ = 0 antes de ajustar (el ajuste BY lo aplica el orquestador). Asociación espacial, no mecanismo.

## Ficha reproducible {{#rho}}
`python3 src/v15/p10_espacial.py`. Regresores: constante, log alquiler inicial, log contratos iniciales.

| especificación | ρ/λ | EE | p Wald | N |
|---|---|---|---|---|
{fila}

Efectos directo e indirecto (simulación LeSage-Pace, 1.000 réplicas): en resultado.json (`detalle`). Moran de los residuos MCO y exclusión de Barcelona/València: en `diagnosticos`. Sin errores de Conley (no figura en las tablas).
{PIE}"""


def main():
    for carp, f in (("p4", h4), ("p9", h5), ("p2", e1), ("p7", e2), ("p10", e3)):
        r = json.loads((OUT / carp / "resultado.json").read_text(encoding="utf-8"))
        mv = pd.read_csv(OUT / carp / "multiverso.csv")
        (OUT / carp / "informe.md").write_text(f(r, mv), encoding="utf-8")


if __name__ == "__main__":
    main()

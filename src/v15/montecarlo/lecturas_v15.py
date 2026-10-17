"""V15 fase 4.1 · Añade a cada docs/v15/validacion_montecarlo/<herramienta>.md la sección «Lectura» (interpretación posterior a los resultados).

Las cifras salen de output/v15/montecarlo/<herramienta>/{resultado.json,tabla.csv}; el texto interpretativo se escribe después de ver los resultados y
no forma parte del proceso generador declarado antes de simular. Idempotente. Uso: python src/v15/montecarlo/lecturas_v15.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v15.montecarlo import _comun_v15 as C  # noqa: E402

M2 = "<!-- LECTURA -->"


def carga(h):
    d = C.OUT / h
    return json.loads((d / "resultado.json").read_text(encoding="utf-8")), pd.read_csv(d / "tabla.csv")


def f(x, n=3):
    return f"{x:.{n}f}".replace(".", ",")


def sdid():
    r, t = carga("sdid_placebo_h1h2")
    g = lambda e, i, ef, c: float(t[(t.escenario == e) & (t.inferencia == i) & (t.efecto == ef)][c].iloc[0])
    s1, s2, s3, s4 = "S1_H1_74donantes", "S2_H1_14donantes_10km", "S3_H2_74donantes", "S4_IPVA_provincias"
    rm = lambda e: g(e, "webb_cluster", "ref", "rmse")
    return f"""## Lectura (posterior a los resultados)
- **Veredicto por escenario:** {'; '.join(f'{e}: {v}' for e, v in r['diagnosticos']['veredicto_por_escenario'].items())}. Condición que falla: el error típico por placebo, tal como lo fija el pre-registro (N_tr = 124 placebo-tratados), **no es computable**: exige más donantes (74 o 14) que tratados (124). Con la inferencia alternativa de la adenda (wild cluster bootstrap de Webb por municipio) el tamaño es {f(g(s1,'webb_cluster','nulo','rechazo'))} (S1), {f(g(s2,'webb_cluster','nulo','rechazo'))} (S2) y {f(g(s3,'webb_cluster','nulo','rechazo'))} (S3), y la cobertura {f(g(s1,'webb_cluster','ref','cobertura'))}, {f(g(s2,'webb_cluster','ref','cobertura'))} y {f(g(s3,'webb_cluster','ref','cobertura'))}. En la variante R-IPVA (clusters = provincia, ≈ 5 provincias tratadas) el tamaño es {f(g(s4,'webb_cluster','nulo','rechazo'))} y la cobertura {f(g(s4,'webb_cluster','ref','cobertura'))}.
- **Por qué:** el SDID puntual es insesgado en el proceso (sesgo ≈ 0; RMSE {f(rm(s1),4)} en S1), pero el error típico por municipio subestima la dispersión real (en S1 la anchura media del IC95 de Webb es {f(g(s1,'webb_cluster','ref','ancho_medio_ic'),4)}, es decir, un SE de ≈ {f(g(s1,'webb_cluster','ref','ancho_medio_ic')/3.92,4)} frente a un RMSE de {f(rm(s1),4)}) porque ignora la correlación espacial entre municipios próximos y las cargas factoriales espaciales (campos de 25 y 60 km del proceso generador). Ningún remuestreo por municipio recupera esa dependencia: haría falta agrupar por zona o por distancia.
- **Variantes de diagnóstico del placebo (no cumplen el pre-registro):** con m = N_co/2 placebo-tratados sin reescalar el tamaño es {f(g(s1,'placebo_m_sin_escalar','nulo','rechazo'),4)} en S1 (dentro del criterio solo por coincidencia: sobrestima el SE en S2 y S3, con {f(g(s2,'placebo_m_sin_escalar','nulo','rechazo'),4)} y {f(g(s3,'placebo_m_sin_escalar','nulo','rechazo'),4)}); reescalado por √(m/N_tr) el tamaño sube a {f(g(s1,'placebo_m_escalado','nulo','rechazo'))}. Ninguna variante es robusta a los tres escenarios.
- **Consecuencia para H1/H2 (adenda 1, puntos 2 y 13):** con esta inferencia el SDID no puede sostener C3; el estimador puntual sigue siendo válido como descriptivo. Condicionado a los niveles de ruido declarados (supuestos del proceso, no medidos), el MDE80 que implica el RMSE del estimador es ≈ {f(2.8*rm(s1)*100,1)} % en renta con 74 donantes (S1), ≈ {f(2.8*rm(s2)*100,1)} % con los 14 donantes a ≥ 10 km (S2; supera el 5 % de la regla de paso a exploratoria de la adenda) y ≈ {f(2.8*rm(s3)*100,1)} % en log(1 + contratos) (S3; por debajo del 13 %).
"""


def honest():
    r, t = carga("honest_did")
    a, b = t.iloc[0], t.iloc[1]
    return f"""## Lectura (posterior a los resultados)
- **Veredicto: {r['diagnosticos']['veredicto']}.** La implementación de V9 se revalida con R = 2.000 y con tendencias paralelas exactas en el proceso:
  - **M̄ = 0 (escenario A):** con la covarianza que usará H1 (estimada por municipio) el tamaño es {f(a.tamano_5pct)} y la cobertura {f(a.cobertura_95)}: **no** pasa. Con la covarianza verdadera el mismo contraste da tamaño {f(a.tamano_Sigma_verdadera)} y cobertura {f(a.cobertura_Sigma_verdadera)}: el contraste ARP condicional de V9 es correcto (el 7,3 % de V9, con 400 réplicas y covarianza conocida, es compatible con este valor dentro del error de Monte Carlo de ±1,3 pp) y el sobre-rechazo viene de la covarianza clusterizada por municipio, que ignora la correlación espacial.
  - **M̄ = 1 (escenario B, tendencia lineal frontera):** tamaño {f(b.tamano_5pct)} (conservador extremo, NO APTO) y **potencia {f(b['potencia_tau_-0.05'])}** incluso frente a un efecto de −5 %: con el ruido declarado (SE de cada coeficiente ≈ 0,012) el IC con M̄ = 1 mide ≈ ±0,2 y nunca excluye el 0. Con la covarianza verdadera ocurre lo mismo.
- **Consecuencia:** el criterio «M̄ de ruptura ≥ 1» de H1 es inalcanzable con este nivel de ruido y no puede sostener C3, aunque haya una segunda implementación (la adenda la exige además y no está disponible aquí: sin red para instalar HonestDiD). Informativo: con tendencias propias y cargas factoriales heterogéneas (E y F) el comportamiento es el mismo (tamaño {f(t.iloc[4].tamano_5pct)} con M̄ = 0; 0,000 con M̄ = 1).
"""


def sc():
    r, t = carga("control_sintetico")
    h, i, p = t.iloc[0], t.iloc[1], t.iloc[2]
    return f"""## Lectura (posterior a los resultados)
- **Veredicto: {r['diagnosticos']['veredicto']}** (escenario P7_heterogeneo, el del pre-registro con la adenda).
- **Tamaño** de la permutación en el espacio por municipio: {f(h.tamano_perm_tau,4)} cuando los 10 tratados mayores son menos ruidosos que los donantes (conservador extremo), {f(i.tamano_perm_tau,4)} cuando son intercambiables (dentro del criterio, y es el máximo exacto posible con 75 unidades: 3/75 = 0,04) y {f(p.tamano_perm_tau,4)} con 20 trimestres previos. Con el cociente RMSPE el tamaño es {f(h.tamano_perm_rmspe,3)} (heterogéneo) y {f(i.tamano_perm_rmspe,3)} (intercambiable). La cobertura del IC por inversión es {f(h.cobertura_ic_perm,3)} (heterogéneo): demasiado ancho.
- **Potencia** frente a −5 %: {f(h.potencia_ref_tau,3)} con la permutación por |τ| y {f(i.potencia_ref_tau,3)} en el caso intercambiable; el RMSE de τ por municipio es {f(h.rmse,4)} (7 trimestres previos, 74 donantes) frente a un efecto de referencia de −0,05.
- **Consecuencia:** el control sintético por municipio es descriptivo; la prueba (vi) de H1 no puede usarse como criterio de C3. La desigualdad de ruido entre grandes municipios y donantes es el mecanismo, no una anomalía del código.
"""


def akm():
    r, t = carga("akm_municipal")
    g = lambda e, i, c: float(t[(t.escenario == e) & (t.inferencia == i)][c].iloc[0])
    e1, e3 = "M1_28_origenes_F_alta", "M3_instr_sin_residenciales_F_alta"
    return f"""## Lectura (posterior a los resultados)
- **Veredicto:** {'; '.join(f'{e}: {v}' for e, v in r['diagnosticos']['veredicto_por_escenario'].items())}.
- **AKM** (28 orígenes, N_efectivo de choques = {f(g(e1,'AKM','n_ef_choques'),1)}): tamaño {f(g(e1,'AKM','tamano_5pct'))}, cobertura {f(g(e1,'AKM','cobertura_95'))}; con el instrumento sin orígenes residenciales (23 orígenes, N_efectivo = {f(g(e3,'AKM','n_ef_choques'),1)}) el tamaño es {f(g(e3,'AKM','tamano_5pct'))}. La varianza AKM se apoya en pocos choques dominantes y los subestima; el error agrupado por provincia es peor ({f(g(e1,'agrupado provincia t(40)','tamano_5pct'))}: no capta la dependencia por cuotas).
- **AKM0 / Anderson-Rubin** (la alternativa de la adenda, punto 5): tamaño {f(g(e1,'AKM0 (AR)','tamano_5pct'),4)}, cobertura {f(g(e1,'AKM0 (AR)','cobertura_95'))}: conservador (fuera de [0,04; 0,06]) y con potencia {f(g(e1,'AKM0 (AR)','potencia_beta_ref'))} frente a β = 0,01 (Saiz). El IC invertido es no acotado en el {f(100*(1-g(e1,'AKM0 (AR)','acotado_AKM0')),0)} % de las réplicas.
- **F efectivo:** con la primera etapa calibrada para una mediana de ≈ 24 el F de cada réplica es muy variable (percentil 10 ≈ 4); el tamaño condicional a F ≥ 10 es {f(g(e1,'AKM','tamano_si_F>=10'))}: el umbral F ≥ 10 no corrige el sobre-rechazo.
- **Consecuencia:** H4 no puede alcanzar C3 con AKM ni con AKM0 con 28 orígenes (≈ 10 choques efectivos); queda como descriptivo/C4. Los pesos de Rotemberg y los intervalos AR (sin criterio de C3) pueden publicarse como diagnóstico.
"""


def dfm():
    r, t = carga("dfm_bvar_mcs")
    e = r["estimacion"]
    return f"""## Lectura (posterior a los resultados)
- **Veredicto DM/CW:** {r['diagnosticos']['veredicto_DM']}. Con el nulo de igual ECM esperado (δ* = {f(r['diagnosticos']['delta_estrella'])}), el DM-HLN unilateral con 73 errores tiene tamaño {f(e['tamano_DM_HLN'],4)} (dentro de [0,04; 0,06]) y potencia {f(e['potencia_DM_HLN_ECM_-20'],3)} frente a una reducción del 20 % del ECM (el MDE del pre-registro es del 18-30 %: la potencia es moderada, no alta). Con el AR(4) como proceso verdadero (δ = 0) la combinación es peor en media y el DM unilateral casi nunca rechaza (tamaño {f(t.iloc[0].rechazo_DM_HLN,4)}), como corresponde.
- **Clark-West no es utilizable** para la combinación frente al AR(4): rechaza el {f(e['tamano_CW_delta0'],3)} de las veces cuando el AR(4) es el proceso verdadero (la combinación de modelos no anidados con parámetros estimados no cumple la teoría de modelos anidados). **GW** condicional: tamaño {f(e['tamano_GW'],3)} bajo igualdad incondicional; solo diagnóstico (su nulo es condicional).
- **MCS** (6 modelos, P = 73, igualdad de precisión por construcción): tamaño {f(e['tamano_mcs_10pct'],4)} al 10 % (banda declarada [0,08; 0,12]; supera el límite por 0,003, dentro de un error de Monte Carlo de ≈ 0,007: **NO APTO en el límite**) y {f(e['tamano_mcs_5pct'],4)} al 5 % (dentro de [0,04; 0,06]). El veredicto del MCS es {r['diagnosticos']['veredicto_MCS']}; la decisión depende de la banda declarada para el 10 %, y por eso H5 debe leerse con el MCS al 5 % como comprobación.
- **Alcance:** esta validación cubre el tamaño de las pruebas con los modelos sustituidos por proxies declarados (λ de Minnesota fijo en lugar de GLP; BIC en lugar de validación temporal con embargo) y ventana expansiva; no valida la elección de la línea base de K1.
"""


def west():
    r, t = carga("westerlund_csardl")
    g = lambda h, c: float(t[t.herramienta == h][c].iloc[0])
    return f"""## Lectura (posterior a los resultados)
- **Umbral de V15:** la potencia de Westerlund (Gτ, bootstrap, B = 99) frente a una velocidad de ajuste de −0,04 trimestral es **{f(g('Westerlund Gtau','potencia_alpha_-0.04'))}** (Gα {f(g('Westerlund Galpha','potencia_alpha_-0.04'))}, Pτ {f(g('Westerlund Ptau','potencia_alpha_-0.04'))}, Pα {f(g('Westerlund Palpha','potencia_alpha_-0.04'))}), menor que 0,5 en los cuatro estadísticos: **E1 se reporta solo como descriptiva**, con independencia del tamaño.
- **Tamaño:** Gτ {f(g('Westerlund Gtau','tamano_5pct'))}, Gα {f(g('Westerlund Galpha','tamano_5pct'))}, Pτ {f(g('Westerlund Ptau','tamano_5pct'))}, Pα {f(g('Westerlund Palpha','tamano_5pct'))}: el bootstrap (VAR(1) por unidad, remuestreo temporal conjunto) sobre-rechaza con N = 40, T = 98 y raíces cercanas a la unidad; la potencia queda inflada por ese sobre-rechazo. **CIPS** con bootstrap de bloques es conservador ({f(g('CIPS (serie I(1))','tamano_5pct'),4)}) y con potencia {f(g('CIPS (serie I(1))','potencia_alpha_-0.04'))} frente a φ ≈ 0,96.
- **CS-ARDL:** la elasticidad de largo plazo tiene RMSE {f(g('CS-ARDL elasticidad de largo plazo','rmse'))} (frente a una elasticidad de 0,8: el cociente (b0+b1)/(1−φ) es inestable por unidad) y cobertura {f(g('CS-ARDL elasticidad de largo plazo','cobertura_95'))} (IC enormes); la **velocidad de ajuste** media sale sesgada en {f(g('CS-ARDL velocidad de ajuste media','sesgo'))} (verdad −0,04) con cobertura {f(g('CS-ARDL velocidad de ajuste media','cobertura_95'),4)}: el ARDL(1,1) con las medias transversales de y y x y sus 4 rezagos (14 regresores con 94 observaciones) probablemente absorbe la tendencia común (ȳ y x̄ están casi colineales) y estima la reversión de la desviación respecto a la media, no la del nivel; no se ha contrastado esta explicación.
- **Veredictos:** ver lista anterior: ninguna herramienta pasa. La adenda no nombra alternativa para estas herramientas.
"""


def sar():
    r, t = carga("sar_sdm")
    h = t[t.errores == "hetero"]
    return f"""## Lectura (posterior a los resultados)
- **Veredicto: {r['diagnosticos']['veredicto']}** en las seis combinaciones modelo × W del escenario heterocedástico (R = 3.000 por celda, N = {r['diagnosticos']['N']}).
- Tamaño del Wald sobre ρ (λ) entre {f(h.tamano_wald_rho.min(),3)} y {f(h.tamano_wald_rho.max(),3)}; razón de verosimilitudes entre {f(h.tamano_lr_rho.min(),3)} y {f(h.tamano_lr_rho.max(),3)}; Moran de los residuos entre {f(h.tamano_moran.min(),3)} y {f(h.tamano_moran.max(),3)}. Cobertura del IC de ρ entre {f(h.cobertura_rho.min(),3)} y {f(h.cobertura_rho.max(),3)}; del efecto indirecto entre {f(h.cobertura_indirecto.min(),3)} y {f(h.cobertura_indirecto.max(),3)}; del directo entre {f(h.cobertura_directo.min(),3)} y {f(h.cobertura_directo.max(),3)}; tamaño del efecto indirecto bajo el nulo entre {f(h.tamano_indirecto.min(),3)} y {f(h.tamano_indirecto.max(),3)}. Sesgo de ρ ≤ {f(h.sesgo_rho.abs().max(),3)} en valor absoluto.
- **Límites de la validación:** el proceso generador es el modelo bien especificado con la W verdadera, errores normales con heterocedasticidad moderada y X fija; no cubre una W equivocada ni una dependencia no espacial (factor común, tendencia regional), que es la amenaza más probable en datos reales. El resultado habilita las herramientas bajo esos supuestos; la sensibilidad a la elección de W queda para la fase de estimación (los dos W del pre-registro).
"""


def webb():
    r, t = carga("wild_webb_v15")
    g = lambda e, i, c: float(t[(t.escenario == e) & (t.inferencia == i)][c].iloc[0])
    w1, w2, w3 = "W1_H1H2_198municipios", "W2_H4_38provincias", "W3_RIPVA_36provincias_pocos_tratados"
    i = "Webb WCR/WCU B=9999"
    return f"""## Lectura (posterior a los resultados)
- **Veredicto:** {'; '.join(f'{e}: {v}' for e, v in r['diagnosticos']['veredicto_por_escenario'].items())}.
- El bootstrap de Webb es algebraicamente correcto (comprobado contra la regresión bootstrap explícita en tests/v15/test_mc_v15.py) y B = 9.999 no cambia nada frente a B = 999 (tamaño {f(g(w1,i,'tamano_5pct'),4)} frente a {f(g(w1,'Webb B=999','tamano_5pct'),4)} en W1). Lo que falla es el supuesto de cluster: con 198 municipios (W1) el tamaño es {f(g(w1,i,'tamano_5pct'))} (el error agrupado CR1 da {f(g(w1,'CR1 t(G-1)','tamano_5pct'))}); con 38 provincias y dependencia por cuotas (W2) {f(g(w2,i,'tamano_5pct'))} (CR1: {f(g(w2,'CR1 t(G-1)','tamano_5pct'))}); con ≈ 5 provincias tratadas de 36 (W3) {f(g(w3,i,'tamano_5pct'))} (CR1: {f(g(w3,'CR1 t(G-1)','tamano_5pct'))}).
- **Interpretación:** Webb mejora a CR1 cuando hay pocos clusters (W3: de {f(g(w3,'CR1 t(G-1)','tamano_5pct'))} a {f(g(w3,i,'tamano_5pct'))}) pero no corrige la dependencia entre clusters (correlación espacial y por cuotas del proceso generador). Para H1/H2 y H4 no puede ser la inferencia que sostenga C3 si la dependencia entre clusters es del orden del proceso declarado.
"""


FUN = {"sdid_placebo_h1h2": sdid, "honest_did": honest, "control_sintetico": sc, "akm_municipal": akm, "dfm_bvar_mcs": dfm,
       "westerlund_csardl": west, "sar_sdm": sar, "wild_webb_v15": webb}


def main():
    for h, fn in FUN.items():
        md = C.DOCS / f"{h}.md"
        base = md.read_text(encoding="utf-8").split(M2)[0].rstrip() + "\n\n"
        md.write_text(base + M2 + "\n" + fn().strip() + "\n", encoding="utf-8")
        print("lectura", h)


if __name__ == "__main__":
    main()

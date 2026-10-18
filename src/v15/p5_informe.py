"""V15-A · H3: escribe resultado.json, informe.md y hechos.json desde output/v15/p5/estimacion_bruta.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pa_comun import FECHA, OUT, volcar  # noqa: E402

S = OUT / "p5"


def f(x, d=3):
    return "n.d." if x is None or not np.isfinite(x) else f"{x:.{d}f}".replace(".", ",")


def main():
    r = json.loads((S / "estimacion_bruta.json").read_text(encoding="utf-8"))
    pr, pl, rm = r["principal"], r["placebo_adelanto"], r["resumen_multiverso"]
    sg, s1, ip, cm = r["sin_grandes_ciudades"], r["sin_1pct_superior"], r["ipva_distrito"], r["comprobacion_medida"]
    b = pr["pct_por_DT"]
    placebo_ok = None  # sin inferencia válida (Conley NO APTO tras K16): el placebo solo se lee como coeficiente puntual
    diag = {
        "inferencia": "principal pre-registrada (agrupada por municipio): sin validación Monte Carlo en panel T = 4 -> descriptiva; alternativa Conley 2 km: NO APTO tras corregir el núcleo (decisión K16 de docs/v16/decisiones.md) -> solo estimación puntual; los errores típicos se dan como referencia, sin IC ni p",
        "placebo_adelanto": {"beta_lead_pct_por_DT": 100 * pl["beta_lead"], "superado": placebo_ok, "nota": "sin inferencia válida: coeficiente puntual"},
        "exclusion_grandes_ciudades": {"beta_pct_por_DT": 100 * sg["beta_log_por_DT"], "se_conley_pct": 100 * sg["se_conley"], "mismo_signo": bool(np.sign(sg["beta_log_por_DT"]) == np.sign(pr["beta_log_por_DT"])), "excluidas": sg["excluidas"]},
        "exclusion_1pct_superior": {"beta_pct_por_DT": 100 * s1["beta_log_por_DT"], "se_conley_pct": 100 * s1["se_conley"]},
        "resultado_alternativo_IPVA_distrito": {k: {"beta_pct_por_DT": 100 * v["beta_log_por_DT"], "se_municipio_pct": 100 * v["se_municipio"], "n_obs": v["n_obs"]} for k, v in ip.items()},
        "exclusion_saltos_factor_10": "ver multiverso (muestra «sin_saltos», 12 de 24 especificaciones)",
        "moran_residuos": {"I_media_anual": pr["moran_I_residuos"], "I_por_anio": pr["moran_I_por_anio"], "nota": pr["moran_nota"]},
        "cinelli_hazlett_RV_q1": pr["cinelli_hazlett_RV_q1"], "oster": {"delta": pr["oster_delta"], "R2_corto": pr["oster_R2_corto"], "R2_largo": pr["oster_R2_largo"], "Rmax": pr["oster_Rmax"], "beta_corto_pct": 100 * pr["oster_beta_corto"]},
        "e_value": "no aplica (resultado continuo, efecto prácticamente nulo)",
        "MDE80_pct_por_DT": {"conley": pr["MDE80_conley_pct_por_DT"], "municipio": pr["MDE80_municipio_pct_por_DT"], "umbral_adenda_exploratoria": 1.0, "supera_umbral": bool(pr["MDE80_conley_pct_por_DT"] > 1.0)},
        "comprobacion_medida": cm,
        "raices_unitarias_cointegracion_rupturas": "no aplica (T = 4)",
        "no_validadas": ["error agrupado por municipio en panel T = 4", "Conley 2 km (NO APTO tras corregir el núcleo, K16)"],
    }
    est = {"beta_pct_por_DT": b, "se_conley_pct_referencia_no_valida": 100 * pr["se_conley2km"], "se_municipio_pct_referencia_no_valida": 100 * pr["se_municipio"],
           "rango_multiverso_pct_por_DT": rm["rango_pct_por_DT"], "referencia_literatura_pct_por_DT": "2-6 (preregistro §3 H3, no verificada aquí)"}
    out = {"rama": "v15/p5", "pregunta": "H3: asociación, dentro de cada sección, entre el porcentaje de viviendas turísticas (INE) y el alquiler declarado (SERPAVI VC, €/m², stock de contratos)",
           "capa": "C4", "datos": "data/processed/v15/p5_turismo_seccion.parquet (INE VUT 2021-2024 y SERPAVI 2021-2024; entrenamiento)",
           "N": {"observaciones": pr["n_obs"], "secciones": pr["n_secciones"], "municipios": pr["n_municipios"]},
           "metodo": "MCO con efectos fijos de sección y de municipio × año; exposición estandarizada por la DT intra-sección; solo estimación puntual (Conley 2 km NO APTO tras K16; agrupado por municipio sin validar)",
           "estimacion": est, "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO", "diagnosticos": diag,
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None}, "pendiente_sellada": True,
           "p_valores_para_BY": [{"hipotesis": "H3", "p": None, "inferencia": "Conley 2 km NO APTO tras K16; agrupado por municipio sin validar", "familia": "asociación pre-registrada, fuera de Holm"}],
           "notas": "Asociación C4, sin lenguaje causal. SERPAVI = stock de contratos declarados (no contratos nuevos); la evaluación con SERPAVI 2025 y el bloque espacial son réplicas posteriores no hechas. Desviaciones: DV15-A, A5.",
           "multiverso_n": rm["n_especificaciones"] * 2, "multiverso_registro": "output/v15/p5/registro.csv"}
    volcar(S / "resultado.json", out)

    inf = [f"# V15-A · H3: vivienda turística (INE) y alquiler por sección (SERPAVI), 2021-2024", "",
           "Capa C4 (asociación pre-registrada, entrenamiento). Sin lenguaje causal. `pendiente_sellada: true`: las réplicas con SERPAVI 2025 y el bloque espacial no se han hecho.", "",
           "## Datos y diseño",
           f"- Resultado: log de la mediana SERPAVI de alquiler en €/m² de vivienda colectiva (**stock de contratos declarados en el IRPF, no contratos nuevos**). Exposición: media anual de las ediciones INE del porcentaje de viviendas turísticas, estandarizada por la DT intra-sección ({f(pr['dt_intra_seccion_pct'], 2)} puntos porcentuales). Efectos fijos de sección y de municipio × año.",
           f"- Muestra: {pr['n_obs']} observaciones, {pr['n_secciones']} secciones en {pr['n_municipios']} municipios (sección con el mismo código en las ediciones INE de 2021 y 2024; {r['n_secciones_codigo_estable']} secciones cumplen el criterio, {r['n_secciones_panel']} tienen alquiler y exposición). Madrid, Illes Balears y Canarias están fuera (sellado v6).",
           "- Inferencia: ninguna validada. El error agrupado por municipio (principal pre-registrado) no tiene validación en un panel de T = 4, y Conley a 2 km es NO APTO tras corregir su núcleo (decisión K16 de docs/v16/decisiones.md). H3 se publica solo como estimación puntual; los errores típicos se dan como referencia, sin IC ni p.", "",
           "## Resultado principal",
           f"- Coeficiente: **{f(b, 4)} % por DT intra-sección** (estimación puntual; EE de referencia, no válidos: Conley {f(100*pr['se_conley2km'], 4)}, agrupado por municipio {f(100*pr['se_municipio'], 4)}).",
           f"- Potencia (referencia, con el EE de Conley no validado): MDE80 = {f(pr['MDE80_conley_pct_por_DT'], 3)} % por DT, por debajo de los 0,5 % del pre-registro y de los 2-6 % que el pre-registro atribuye a la literatura (cifra del pre-registro, no verificada aquí). El umbral de paso a exploratoria (1 % por DT) no se supera.",
           f"- Multiverso de 48 (24 especificaciones × 2 agrupaciones): coeficientes entre {f(rm['rango_pct_por_DT'][0], 3)} % y {f(rm['rango_pct_por_DT'][1], 3)} % por DT, mediana {f(rm['mediana_pct_por_DT'], 3)}; {f(100*rm['pct_positivos'], 0)} % positivos (puntuales; los p de registro.csv son de referencia y no válidos tras K16).", "",
           "## Pruebas",
           f"- **Placebo de adelanto** (exposición en t+1 con la de t controlada): {f(100*pl['beta_lead'], 4)} % por DT (puntual; sin inferencia válida, no se declara superado ni fallido).",
           f"- **Sin Barcelona ni València** (las grandes ciudades en entrenamiento): {f(100*sg['beta_log_por_DT'], 4)} % por DT: {'mismo signo' if diag['exclusion_grandes_ciudades']['mismo_signo'] else 'signo distinto'}. Sin el 1 % superior de exposición: {f(100*s1['beta_log_por_DT'], 4)} %.",
           f"- **IPVA por distrito** (resultado alternativo; EE agrupado por municipio, descriptivo): {f(100*ip['anio']['beta_log_por_DT'], 3)} % por DT con efecto de año y {f(100*ip['mun_anio']['beta_log_por_DT'], 3)} % con municipio × año ({ip['mun_anio']['n_distritos']} distritos).",
           f"- **Moran de residuos** (distancia inversa, 2 km; solo estadístico): I medio anual {f(pr['moran_I_residuos'], 3)}. **Cinelli-Hazlett** RV = {f(pr['cinelli_hazlett_RV_q1'], 5)}; **Oster** δ = {f(pr['oster_delta'], 3)} (con efecto casi nulo no informativo).",
           f"- **Comprobación de la medida** (pre-registro: se aplica a cualquier resultado): {f(100*cm['obs_con_exposicion_cero'], 1)} % de las observaciones tiene exposición 0; {f(100*cm['secciones_sin_variacion_intra'], 1)} % de las secciones no varía; en las {cm['n_secciones_media_pct_ge_1']} secciones con media ≥ 1 % el coeficiente es {f(100*cm['beta_log_por_DT_secciones_expuestas'], 4)} % por DT (EE de Conley {f(100*cm['se_conley_expuestas'], 4)}). Las exposiciones por número y por plazas correlacionan con el porcentaje en {f(cm['corr_pct_n'], 2)} y {f(cm['corr_pct_plazas'], 2)}. La exposición «viviendas por 100 hogares» no se pudo construir (DV15-A, A5).",
           "- Raíces unitarias, cointegración y rupturas: no aplican (T = 4).", "",
           "## Lectura frente a lo ya publicado",
           "- La 1.0 dice «turísticos: no concluyente» (v3, v6, V8, V9). Un coeficiente puntual pequeño por sección, sin inferencia válida y en el extremo inferior de su multiverso (que debe citarse con su mediana y su rango), no contradice esa conclusión ni la precisa: H3 queda «no concluyente», no «nula»; V9-D2 usa otra exposición (viviendas de uso turístico en 2019 × periodos) y otra unidad (municipio, renta de contratos nuevos): no es comparable cifra a cifra.",
           "- Todo es asociación C4: el alquiler SERPAVI es un stock y se mueve despacio (DT residual del log: " + f(cm['desv_tipica_residual_log_alquiler'], 3) + "), de modo que un efecto sobre contratos nuevos no se descarta con este resultado.", "",
           "## Fichas reproducibles",
           "Todas: `python3 src/v15/p5_turismo.py && python3 src/v15/p5_informe.py` (SEED 20261010); cifras en output/v15/p5/estimacion_bruta.json y registro.csv.",
           "- <a id=\"ficha-h3-principal\"></a>**ficha-h3-principal:** `principal.pct_por_DT` = 100 × β de log(SERPAVI VC) sobre z = pct/DT intra-sección, con FE de sección y de municipio × año (src/v15/pa_panel.py:ols_fe); EE de Conley con núcleo de Bartlett a 2 km y puntuaciones sumadas por sección.",
           "- <a id=\"ficha-h3-rango\"></a>**ficha-h3-rango:** `resumen_multiverso.rango_pct_por_DT` (24 especificaciones × 2 agrupaciones).",
           "- <a id=\"ficha-h3-placebo\"></a>**ficha-h3-placebo:** `placebo_adelanto.beta_lead` (modelo con z_t y z_{t+1}, años 2021-2023).",
           "- <a id=\"ficha-h3-mde\"></a>**ficha-h3-mde:** `principal.MDE80_conley_pct_por_DT` = 2,8 × EE de Conley × 100.",
           "- <a id=\"ficha-h3-ipva\"></a>**ficha-h3-ipva:** `ipva_distrito.mun_anio`.",
           "- <a id=\"ficha-h3-n\"></a>**ficha-h3-n:** `principal.n_secciones`."]
    (S / "informe.md").write_text("\n".join(inf) + "\n", encoding="utf-8")

    base = dict(periodo="2021-2024", cobertura="secciones con alquiler SERPAVI VC y código estable; entrenamiento", fuentes=["INE (viviendas turísticas, experimental)", "MIVAU SERPAVI"], capa="C4", fecha_dato=FECHA)
    hechos = [
        dict(id="V15-H3-beta", indicador="H3: variación del alquiler SERPAVI VC (stock) por 1 DT intra-sección del porcentaje de viviendas turísticas (estimación puntual; sin IC válido, K16)", valor=round(b, 6), min=None, max=None, unidad="% por DT", ficha="output/v15/p5/informe.md#ficha-h3-principal", **base),
        dict(id="V15-H3-rango", indicador="H3: mediana de los coeficientes del multiverso (min/max = rango de las especificaciones; no es IC)", valor=round(rm["mediana_pct_por_DT"], 6), min=round(rm["rango_pct_por_DT"][0], 6), max=round(rm["rango_pct_por_DT"][1], 6), unidad="% por DT", ficha="output/v15/p5/informe.md#ficha-h3-rango", **base),
        dict(id="V15-H3-placebo", indicador="H3: coeficiente del placebo de adelanto (exposición en t+1)", valor=round(100 * pl["beta_lead"], 4), min=None, max=None, unidad="% por DT", ficha="output/v15/p5/informe.md#ficha-h3-placebo", **base),
        dict(id="V15-H3-mde", indicador="H3: efecto mínimo detectable con 80 % de potencia (2,8 × EE de Conley; referencia, EE no validado tras K16)", valor=round(pr["MDE80_conley_pct_por_DT"], 4), min=None, max=None, unidad="% por DT", ficha="output/v15/p5/informe.md#ficha-h3-mde", **base),
        dict(id="V15-H3-ipva", indicador="H3: coeficiente con el IPVA por distrito como resultado (efectos de municipio × año; EE agrupado, descriptivo)", valor=round(100 * ip["mun_anio"]["beta_log_por_DT"], 4), min=None, max=None, unidad="% por DT", ficha="output/v15/p5/informe.md#ficha-h3-ipva", **base),
        dict(id="V15-H3-n", indicador="H3: secciones del panel principal", valor=pr["n_secciones"], min=None, max=None, unidad="secciones", ficha="output/v15/p5/informe.md#ficha-h3-n", **base),
    ]
    volcar(S / "hechos.json", hechos)


if __name__ == "__main__":
    main()

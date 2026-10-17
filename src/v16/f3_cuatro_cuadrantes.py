"""V16-F3 · Marco de stock y flujo de cuatro cuadrantes (DiPasquale y Wheaton) calibrado para España: qué respuesta cabe esperar de
cada shock y si los datos nacionales la muestran (docs/v16/plan.md, fase 3). Contabilidad teórica, no estimación: capa C4.

Modelo log-lineal en estado estacionario:
- Alquiler (cuadrante 1): stock ocupado S = A · Y^ey · R^(−ed)  →  ln R = (ln A + ey ln Y − ln S) / ed
- Activo (cuadrante 2): P = R / i (i: rentabilidad bruta o tasa de capitalización)
- Construcción (cuadrante 3): C = B · (P / K)^es (K: coste de reposición)
- Stock (cuadrante 4): en estado estacionario C = φ S (φ: obra nueva sobre el parque = crecimiento + bajas)
Multiplicadores de largo plazo: dlnR/dlnY = dlnP/dlnY = ey/(ed+es); dlnS/dlnY = es·ey/(ed+es);
dlnP/dln i = dlnP/dlnK = −ed/(ed+es); dlnR/dln i = es/(ed+es). Corto plazo (stock fijo): dlnR/dlnY = ey/ed; dlnP/dln i = −1.
Velocidad de ajuste del stock: λ = φ (1 + es/ed); semivida = ln 2 / λ.

Parámetros: de output/v5/cifras_clave.csv por id cuando existen; de la literatura de docs/v16/literatura con su ficha; y si no hay
fuente leída, «supuesto del autor» con rango amplio y explícito. Monte Carlo uniforme en los rangos (SEED=20261010, 20.000 extracciones).
Comprobación con datos: signos de las variaciones nacionales observadas en el episodio de subida de tipos (medias anuales de 2024 frente a 2022), de data/base
(capa pública, filas no marcadas como muestra_sellada_v6), frente a los signos que predice el marco con y sin shock de demanda simultáneo.
Salidas: output/v16/f3/cuatro_cuadrantes.md, cuatro_cuadrantes_parametros.csv, cuatro_cuadrantes_multiplicadores.csv y
cuatro_cuadrantes_resultado.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
SAL = RAIZ / "output" / "v16" / "f3"
SEED = 20261010
N = 20_000


def _ck() -> pd.DataFrame:
    return pd.read_csv(RAIZ / "output/v5/cifras_clave.csv", dtype=str).set_index("id")


def parametros() -> pd.DataFrame:
    ck = _ck()
    ratio_min, ratio_max = float(ck.at["K3-RATIO-2023", "min"]), float(ck.at["K3-RATIO-2023", "max"])
    filas = [
        # parámetro, mínimo, máximo, tipo, fuente
        ("es", 0.8, 1.3, "literatura", "elasticidad de la nueva oferta a precio, 17 CCAA 1990-2012: Taltavull (2014), "
                                        "docs/v16/literatura/L3_oferta_elasticidad.md (leída en resumen)"),
        ("ed", 0.3, 1.0, "supuesto del autor", "elasticidad-precio de la demanda de servicios de vivienda: sin estimación española leída "
                                                "en V16 (L3, «Parámetros de calibración»); rango amplio"),
        ("ey", 0.5, 1.5, "supuesto del autor", "elasticidad-renta de la demanda de vivienda: sin estimación española leída en V16; rango amplio"),
        ("i", 1 / ratio_max, 1 / ratio_min, "cifra_clave", "inversa del ratio precio/alquiler 2023 (K3-RATIO-2023, mínimo y máximo de las medidas)"),
        ("phi", 0.002, 0.006, "supuesto del autor", "obra nueva sobre el parque al año (crecimiento del parque + bajas); orden de magnitud de "
                                                   "E-T7-prod sobre el parque censal; las bajas por licencia (T1-H8) son < 0,06 %"),
        ("retardo", float(ck.at["B2-H5", "min"]), float(ck.at["B2-H5", "max"]), "cifra_clave",
         "retardo medio iniciadas-terminadas en años (B2-H5); solo informativo: el estado estacionario no depende de él"),
    ]
    return pd.DataFrame(filas, columns=["parametro", "minimo", "maximo", "tipo", "fuente"])


def multiplicadores(p: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    d = {r.parametro: rng.uniform(r.minimo, r.maximo, N) for r in p.itertuples()}
    es, ed, ey, i, phi = d["es"], d["ed"], d["ey"], d["i"], d["phi"]
    dlni_1pp = 0.01 / i                                              # +1 p.p. en la rentabilidad exigida, en log
    m = {
        ("demanda +1 % (renta u hogares)", "alquiler", "largo"): ey / (ed + es),
        ("demanda +1 % (renta u hogares)", "precio", "largo"): ey / (ed + es),
        ("demanda +1 % (renta u hogares)", "stock", "largo"): es * ey / (ed + es),
        ("demanda +1 % (renta u hogares)", "alquiler", "corto (stock fijo)"): ey / ed,
        ("demanda +1 % (renta u hogares)", "obra nueva", "corto (stock fijo)"): es * ey / ed,
        ("tipo exigido +1 p.p.", "precio", "corto (stock fijo)"): -dlni_1pp,
        ("tipo exigido +1 p.p.", "obra nueva", "corto (stock fijo)"): -es * dlni_1pp,
        ("tipo exigido +1 p.p.", "alquiler", "corto (stock fijo)"): 0 * es,
        ("tipo exigido +1 p.p.", "precio", "largo"): -ed / (ed + es) * dlni_1pp,
        ("tipo exigido +1 p.p.", "alquiler", "largo"): es / (ed + es) * dlni_1pp,
        ("tipo exigido +1 p.p.", "stock", "largo"): -es * ed / (ed + es) * dlni_1pp,
        ("coste de construcción +1 %", "precio", "largo"): es / (ed + es),
        ("coste de construcción +1 %", "alquiler", "largo"): es / (ed + es),
        ("coste de construcción +1 %", "stock", "largo"): -es * ed / (ed + es),
        ("oferta menos elástica (es/2), demanda +1 %", "precio", "largo"): ey / (ed + es / 2),
        ("oferta menos elástica (es/2), demanda +1 %", "stock", "largo"): (es / 2) * ey / (ed + es / 2),
    }
    filas = []
    for (shock, var, plazo), v in m.items():
        # shocks de +1 %: la elasticidad ya es el % de respuesta; shock de tipos: variación logarítmica → × 100
        k = 100.0 if shock.startswith("tipo exigido") else 1.0
        filas.append({"shock": shock, "variable": var, "plazo": plazo, "mediana_pct": k * float(np.median(v)),
                      "p05_pct": k * float(np.quantile(v, 0.05)), "p95_pct": k * float(np.quantile(v, 0.95))})
    sem = np.log(2) / (phi * (1 + es / ed))
    filas.append({"shock": "ajuste del stock", "variable": "semivida (años)", "plazo": "—", "mediana_pct": float(np.median(sem)),
                  "p05_pct": float(np.quantile(sem, 0.05)), "p95_pct": float(np.quantile(sem, 0.95))})
    return pd.DataFrame(filas)


def observado() -> pd.DataFrame:
    vars_ = {"tipo_hip": "tipo hipotecario (p.p.)", "ipv": "precio de compra, IPV (%)", "ipc_alquiler": "alquiler, IPC (%)",
             "compraventas_ine": "compraventas (%)", "visados": "visados de obra nueva (%)", "renta_hog_real": "renta real de los hogares (%)",
             "hogares_epa": "hogares, EPA (%)"}
    lista = ", ".join(f"'{v}'" for v in vars_)
    # medias anuales de los cuatro trimestres: evitan la estacionalidad de comparar trimestres sueltos
    q = f"""SELECT variable, substr(periodo, 1, 4) AS anio, avg(valor) AS valor FROM read_parquet('{RAIZ / "data/base/publica/hechos.parquet"}')
            WHERE nivel = 'nacional' AND NOT muestra_sellada_v6 AND variable IN ({lista}) AND frecuencia = 'T'
              AND substr(periodo, 1, 4) IN ('2022', '2024')
            GROUP BY 1, 2 HAVING count(DISTINCT periodo) = 4"""
    d = duckdb.sql(q).df().pivot(index="variable", columns="anio", values="valor")
    filas = []
    for v, nombre in vars_.items():
        if v not in d.index or d.loc[v].isna().any():
            filas.append({"serie": nombre, "variable": v, "variacion": None, "signo": "sin dato"})
            continue
        a, b = float(d.at[v, "2022"]), float(d.at[v, "2024"])
        x = b - a if v == "tipo_hip" else 100 * (b / a - 1)
        filas.append({"serie": nombre, "variable": v, "variacion": x, "signo": "+" if x > 0 else "−" if x < 0 else "0"})
    return pd.DataFrame(filas)


def main() -> int:
    SAL.mkdir(parents=True, exist_ok=True)
    p = parametros()
    m = multiplicadores(p)
    o = observado()
    p.to_csv(SAL / "cuatro_cuadrantes_parametros.csv", index=False, lineterminator="\n", float_format="%.6g")
    m.to_csv(SAL / "cuatro_cuadrantes_multiplicadores.csv", index=False, lineterminator="\n", float_format="%.6g")
    sg = dict(zip(o.variable, o.signo))
    solo_tipos = {"ipv": "−", "visados": "−", "ipc_alquiler": "0 o +"}
    coherente_solo_tipos = sg.get("ipv") == "−" and sg.get("visados") == "−"
    f = lambda x: f"{x:.2f}".replace(".", ",")
    L = ["# V16 · Marco de cuatro cuadrantes (DiPasquale y Wheaton) calibrado para España", "",
         "Generado por `python3 src/v16/f3_cuatro_cuadrantes.py`. Es un marco teórico calibrado, no una estimación: dice qué respuesta "
         "cabe esperar de cada shock si el mercado funcionara como el modelo, con los parámetros y rangos declarados. Capa C4.", "",
         "## Parámetros", "", "| Parámetro | Mínimo | Máximo | Tipo | Fuente |", "|---|---|---|---|---|"]
    for r in p.itertuples():
        L.append(f"| {r.parametro} | {r.minimo:.4g} | {r.maximo:.4g} | {r.tipo} | {r.fuente} |")
    L += ["", "Tres de los cinco parámetros que mueven los multiplicadores son supuestos del autor: no hay estimación española leída de "
          "las elasticidades de la demanda ni de la tasa de obra nueva sobre el parque. Los rangos son amplios a propósito.", "",
          "## Respuestas esperadas (Monte Carlo sobre los rangos): % de variación por shock de +1 % o de +1 p.p.; la semivida en años", "",
          "| Shock | Variable | Plazo | Mediana | P5 | P95 |", "|---|---|---|---|---|---|"]
    for r in m.itertuples():
        L.append(f"| {r.shock} | {r.variable} | {r.plazo} | {f(r.mediana_pct)} | {f(r.p05_pct)} | {f(r.p95_pct)} |")
    L += ["", "El «tipo exigido» es la rentabilidad que pide el comprador (coste de uso: tipo, depreciación, fiscalidad y revalorización "
          "esperada), no el tipo hipotecario: una subida de 1 p.p. del hipotecario no se traslada por fuerza uno a uno.",
          "", "Lectura: con una obra nueva del orden del 0,2-0,6 % del parque al año, el stock tarda décadas en ajustarse; a corto plazo "
          "los shocks de demanda van sobre todo al alquiler y al precio, y los de tipos al precio y a la obra nueva.", "",
          "## ¿Lo muestran los datos? Episodio de subida de tipos: medias de 2024 frente a 2022 (descriptivo)", "",
          "| Serie | Variación | Signo |", "|---|---|---|"]
    for r in o.itertuples():
        L.append(f"| {r.serie} | {'' if r.variacion is None or pd.isna(r.variacion) else f(r.variacion)} | {r.signo} |")
    L += ["", f"Signos que predice el marco si solo cambiaran los tipos: precio {solo_tipos['ipv']}, obra nueva {solo_tipos['visados']}, "
          f"alquiler {solo_tipos['ipc_alquiler']}. Con los datos observados, ese patrón {'se cumple' if coherente_solo_tipos else 'no se cumple'}. "
          "Si no se cumple, el marco es compatible con un shock de demanda simultáneo (hogares, renta) que compensa la subida de tipos; "
          "con estos datos no se puede separar un shock del otro: es una pregunta de la fase 6 (Q5), no una conclusión de este marco.", ""]
    (SAL / "cuatro_cuadrantes.md").write_text("\n".join(L), encoding="utf-8")
    res = {"rama": "v16-f3-cuatro-cuadrantes", "pregunta": "Respuestas esperadas a cada shock en un marco de stock y flujo calibrado",
           "capa": "C4", "datos": ["output/v5/cifras_clave.csv", "data/base/publica/hechos.parquet", "docs/v16/literatura/L3_oferta_elasticidad.md"],
           "N": N, "metodo": "DiPasquale-Wheaton log-lineal en estado estacionario; Monte Carlo uniforme sobre rangos", "estimacion": None,
           "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO",
           "diagnosticos": {"supuestos_del_autor": int((p.tipo == "supuesto del autor").sum()), "patron_solo_tipos_en_datos": coherente_solo_tipos,
                            "signos_observados_2022_2024": sg},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "notas": "Marco teórico calibrado; no identifica efectos. Tres parámetros son supuestos con rango amplio."}
    (SAL / "cuatro_cuadrantes_resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"f3_cuatro_cuadrantes: {len(m)} respuestas; patrón solo-tipos en datos: {coherente_solo_tipos}; signos {sg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

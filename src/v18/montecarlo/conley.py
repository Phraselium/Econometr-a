"""V18 · Monte Carlo de Conley a 1, 2, 10 y 25 km en sección y municipio (geometría sintética de Barcelona). Simulación; sin datos reales.

Ejecución: python src/v18/montecarlo/conley.py [--R 2000]   (SEED 20261010)

Por qué falló en V16 (conley_seccion, tamaño 0,0963, cobertura 0,9038; núcleo de Bartlett a 2 km): el proceso generador de V16 situaba el alcance de la
correlación del producto x_i e_i justo en el corte (soporte = 2 km). El núcleo triangular pondera cada covarianza a distancia d por (1 - d/corte), de modo
que cuando hay correlación hasta el borde subestima la varianza (sesgo a la baja que crece con el cociente soporte/corte); con soporte la mitad del corte
(radio 0,5 km) V16 daba tamaño 0,0555, y con soporte mayor que el corte (1,5 km), 0,1245. Es un sesgo del estimador, no del código (el HC1 daba 0,236).
Este Monte Carlo lo mide por cociente soporte/corte y lo declara como condición.

Proceso generador (declarado antes de simular)
- Geometría sintética (src/v18/herramientas/conley.py): sección = 800 secciones en 48 barrios de la ciudad (densidad 10,6 secciones/km2) + 3.200
  secciones en 310 municipios de la corona metropolitana (N = 4.000; unos 39 vecinos a menos de 2 km, similar al ~46 de V16 con datos de secciones);
  municipio = 311 centros municipales (Barcelona en el origen y 310 con ley radial). Coordenadas planas en km.
- Sección: MCO de y sobre x con efectos fijos de barrio o municipio (358 grupos; grupos de unos 11 secciones); 48 clusters de barrio en la ciudad.
  Municipio: MCO con constante, sin grupos.
- x_i = m^x_g + a_i; y_i = beta x_i + h_g (m^e_g + b_i), con a, b campos gaussianos independientes de covarianza 0,6 W_theta(d) + 0,4 I (W = correlación de
  Wendland de soporte theta, definida positiva en 2D) y m ~ N(0,1) (absorbidos por los efectos fijos de grupo); h_g = exp(0,5 N(0,1)) por grupo
  (heterogeneidad); en municipio h_i por unidad y sin efectos de grupo.
- Cociente soporte/corte: theta = r x corte con r en {0,5; 1; 2}. Escenario principal por corte: r = 1 (la correlación llega al corte, como en V16).
- Nulo beta = 0; no nulo beta = 0,1 por equivariancia a la traslación: potencia = rechazo de H0: beta = -0,1 con los datos de beta = 0; cobertura = 1 - tamaño.
- Inferencia: Conley con núcleo de Bartlett (cada observación una sola vez en la diagonal), normal. Varianza no positiva: no rechazo, se cuenta.
  Referencias: HC1 y (sección) agrupado por grupo (CR1).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
SEED = 20261010
ALCANCE_TERRITORIAL = "sin lectura de datos"
HERR = "conley"
ROTULO = "simulación; sin datos reales"
DELTA = 0.1
Z95 = 1.959964
SALIDA = RAIZ / "output" / "v18" / "montecarlo" / HERR
CORTES = (1.0, 2.0, 10.0, 25.0)
RATIOS = (0.5, 1.0, 2.0)
LOTE = 250


def _herr():
    """Carga la herramienta por ruta (mismo nombre de fichero que este script: no se puede importar por nombre)."""
    m = sys.modules.get("herr_conley")
    if m is None:
        spec = importlib.util.spec_from_file_location("herr_conley", RAIZ / "src" / "v18" / "herramientas" / "conley.py")
        m = importlib.util.module_from_spec(spec)
        sys.modules["herr_conley"] = m
        spec.loader.exec_module(m)
    return m


def veredicto(tam, cob, R):
    fallos = []
    if R < 1000:
        fallos.append(f"R={R} < 1.000")
    if not (0.03 <= tam <= 0.08):
        fallos.append(f"tamaño {tam:.4f} fuera de [0,03; 0,08]")
    if not (0.92 <= cob <= 0.97):
        fallos.append(f"cobertura {cob:.4f} fuera de [0,92; 0,97]")
    return ("APTO" if not fallos else "NO APTO"), fallos


def banda_adenda(tam, cob):
    if tam > 0.15 or tam < 0.02:
        return "no fiable"
    if 0.04 <= tam <= 0.06 and 0.93 <= cob <= 0.97:
        return "apta"
    return "con valor crítico corregido"


def ic_bin(p, n):
    e = 1.96 * math.sqrt(max(p * (1 - p), 1e-12) / n)
    return [round(max(p - e, 0.0), 4), round(min(p + e, 1.0), 4)]


def geometria(nivel):
    C = _herr()
    rng = np.random.default_rng([SEED, 99, 0 if nivel == "seccion" else 1])
    if nivel == "seccion":
        coords, grupo, _ = C.geometria_secciones(rng)
        h_unidad = False
    else:
        coords, grupo, h_unidad = C.geometria_municipios(rng), None, True
    return coords, grupo, h_unidad


def simular(nivel, corte, ratio, k, R, coords, grupo, h_unidad, D):
    C = _herr()
    N = len(coords)
    theta = ratio * corte
    S = 0.6 * C.wendland(D, theta) + 0.4 * np.eye(N)
    L = np.linalg.cholesky(S + 1e-9 * np.eye(N))
    K = np.maximum(0.0, 1.0 - D / corte)
    vec_medios = float(((D < corte).sum()) / N)
    if grupo is not None:
        cnt = np.bincount(grupo).astype(float)
        ini = np.r_[0, np.cumsum(cnt)[:-1]].astype(int)
        Gn = len(cnt)

        def dm(a):
            return a - (np.add.reduceat(a, ini, axis=0) / cnt[:, None])[grupo]
    else:
        Gn = 0

        def dm(a):
            return a - a.mean(axis=0, keepdims=True)
    cols = []
    hecho = 0
    lote_i = 0
    while hecho < R:
        b = min(LOTE, R - hecho)
        rng = np.random.default_rng([SEED, k, lote_i])
        x = L @ rng.standard_normal((N, b))
        e = L @ rng.standard_normal((N, b))
        if grupo is not None:
            h = np.exp(0.5 * rng.standard_normal((Gn, b)))[grupo]
            x = x + rng.standard_normal((Gn, b))[grupo]
            e = h * (e + rng.standard_normal((Gn, b))[grupo])
        elif h_unidad:
            e = np.exp(0.5 * rng.standard_normal((N, b))) * e
        xt, yt = dm(x), dm(e)
        sxx = (xt ** 2).sum(0)
        bh = (xt * yt).sum(0) / sxx
        s = xt * (yt - bh * xt)
        vc = (s * (K @ s)).sum(0)
        vh = (s ** 2).sum(0) * N / (N - 1.0)
        if grupo is not None:
            cs = np.add.reduceat(s, ini, axis=0)
            vg = (cs ** 2).sum(0) * Gn / (Gn - 1.0)
        else:
            vg = np.full(b, np.nan)
        cols.append(np.column_stack([bh, sxx, vc, vh, vg]))
        hecho += b
        lote_i += 1
    M = np.vstack(cols)
    return M, vec_medios


def resumir(M, nivel, corte, ratio, R, vec_medios, principal):
    bh, sxx, vc, vh, vg = (M[:, j] for j in range(5))
    var_emp = float(np.var(bh))
    filas = []
    infs = [("Conley (Bartlett)", vc), ("HC1 (referencia)", vh)]
    if not np.isnan(vg).all():
        infs.append(("agrupado por barrio o municipio (referencia)", vg))
    for nom, v in infs:
        pos = v > 0
        se = np.sqrt(np.where(pos, v, 1.0)) / sxx
        rech0 = pos & (np.abs(bh) / se > Z95)
        rechA = pos & (np.abs(bh + DELTA) / se > Z95)
        tam = float(rech0.mean())
        d = {"nivel": nivel, "corte_km": corte, "razon_soporte_corte": ratio, "soporte_km": ratio * corte, "inferencia": nom, "R": R,
             "tamano_5pct": tam, "tamano_ic95": str(ic_bin(tam, R)), "cobertura_95": 1 - tam, "potencia": float(rechA.mean()),
             "razon_var_est_sobre_emp": float(np.mean(v / sxx ** 2) / var_emp), "var_no_positiva": float((~pos).mean()),
             "vecinos_medios_corte": vec_medios, "sesgo": float(bh.mean()), "rmse": float(np.sqrt(np.mean(bh ** 2))), "principal": principal}
        d["veredicto"] = veredicto(tam, 1 - tam, R)[0]
        d["banda_adenda_1_12"] = banda_adenda(tam, 1 - tam)
        filas.append(d)
    return filas


def main(R=2000, salida=SALIDA, niveles=("seccion", "municipio"), cortes=CORTES):
    C = _herr()
    filas = []
    k = 0
    for nivel in niveles:
        coords, grupo, h_unidad = geometria(nivel)
        D = C.distancias(coords)
        for corte in cortes:
            for ratio in RATIOS:
                M, vm = simular(nivel, corte, ratio, k, R, coords, grupo, h_unidad, D)
                filas += resumir(M, nivel, corte, ratio, len(M), vm, ratio == 1.0)
                print(nivel, corte, ratio, flush=True)
                k += 1
    tab = pd.DataFrame(filas)
    escribir(tab, salida)
    return tab


def escribir(tab, salida):
    salida.mkdir(parents=True, exist_ok=True)
    tab.to_csv(salida / "tabla.csv", index=False)
    vg = {}
    cc = tab[tab.inferencia == "Conley (Bartlett)"]
    for (nivel, corte), g in cc.groupby(["nivel", "corte_km"]):
        g = g.set_index("razon_soporte_corte")
        p1 = g.loc[1.0, "veredicto"] == "APTO"
        p05 = g.loc[0.5, "veredicto"] == "APTO"
        if p1 and p05:
            v = "APTO"
        elif p05:
            v = "APTO solo si el alcance de la dependencia es de a lo sumo la mitad del corte; NO APTO si llega al corte"
        else:
            v = "NO APTO"
        vg[f"{nivel} · {corte:g} km"] = {"veredicto": v, "tamano_por_razon": {str(r): round(float(g.loc[r, 'tamano_5pct']), 4) for r in g.index},
                                          "cobertura_por_razon": {str(r): round(float(g.loc[r, 'cobertura_95']), 4) for r in g.index}}
    res = {"rama": "v18/montecarlo", "pregunta": "validación de Conley a 1, 2, 10 y 25 km en sección y municipio (E1, E5-A3, E6-R1, E10-A1)",
           "capa": "validación de herramienta (sin capa de evidencia)", "datos": ROTULO, "N": "sección: 4.000 secciones (800 en la ciudad); municipio: 311",
           "metodo": "MCO (con efectos fijos de grupo en sección) y errores de Conley con núcleo de Bartlett",
           "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "no aplica (validación Monte Carlo)",
           "diagnosticos": {"veredicto_por_nivel_y_corte": vg, "R": int(tab.R.min()), "semilla": SEED,
                            "criterio": "tamaño [0,03; 0,08], cobertura [0,92; 0,97], R >= 2.000; principal = soporte igual al corte",
                            "bandas_adenda_1_12": {f"{r.nivel} {r.corte_km:g} km r={r.razon_soporte_corte:g} · {r.inferencia}": r.banda_adenda_1_12 for r in tab.itertuples()},
                            "alcance_territorial": ALCANCE_TERRITORIAL},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "notas": [ROTULO, "Causa del NO APTO de V16: el núcleo de Bartlett subestima la varianza cuando la correlación llega al corte (ver razon_var_est_sobre_emp)."]}
    (salida / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    cols = ["nivel", "corte_km", "razon_soporte_corte", "inferencia", "R", "tamano_5pct", "cobertura_95", "potencia", "razon_var_est_sobre_emp",
            "var_no_positiva", "vecinos_medios_corte", "veredicto", "banda_adenda_1_12"]
    md = ["# Conley en sección y municipio · Monte Carlo V18", "", f"**{ROTULO}.** SEED {SEED}.", "",
          "Proceso generador y causa del NO APTO de V16: ver el docstring de src/v18/montecarlo/conley.py.", "", "## Resultados", "",
          tab[cols].round(4).to_markdown(index=False), "", "## Veredicto por nivel y corte", ""]
    for k, v in vg.items():
        md.append(f"- **{k}: {v['veredicto']}.** Tamaño por cociente soporte/corte: {v['tamano_por_razon']}.")
    (salida / "informe.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    main(ap.parse_args().R)

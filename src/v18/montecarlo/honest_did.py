"""V18 · Monte Carlo de Honest DiD (Rambachan-Roth, magnitudes relativas, M̄ hasta 1) en los diseños de estudio de eventos de V18
(plan de replicación 1.13: E1-R3, R4, A2; E2; E6-R1; E8).

Uso: python3 src/v18/montecarlo/honest_did.py [--R 2000] [--jobs 4]
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):   # BLAS de un hilo: antes de importar numpy
    os.environ.setdefault(_v, "1")

import functools
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v18.herr18 import honest_did as H  # noqa: E402
from src.v18.montecarlo import _comun as C  # noqa: E402
from src.v18.montecarlo import _dgp_did as D  # noqa: E402
from src.v18.montecarlo import _informe as I  # noqa: E402
from src.v18.montecarlo._resumen import filas_por_p  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"
HERR = "honest_did"
K1 = 22
PEND = 0.004          # pendiente de la tendencia diferencial por periodo (log), V15
TAU_ALT = -0.05
# nombre: (diseño, Mbar del contraste, multiplicador m de la pendiente posterior, pendiente previa s, ¿entra en el veredicto?)
ESC = {
    "cat_M_M0_PTexacta": ("cat_trim_M", 0.0, 0.0, 0.0, True),
    "cat_M_M05_frontera": ("cat_trim_M", 0.5, 0.5, PEND, True),
    "cat_M_M1_frontera": ("cat_trim_M", 1.0, 1.0, PEND, True),
    "cat_S_M0_PTexacta": ("cat_trim_S", 0.0, 0.0, 0.0, True),
    "cat_S_M1_frontera": ("cat_trim_S", 1.0, 1.0, PEND, True),
    "cat_L_M0_PTexacta": ("cat_trim_L", 0.0, 0.0, 0.0, True),
    "cat_L_M1_frontera": ("cat_trim_L", 1.0, 1.0, PEND, True),
    "cat_M_M1_sin_tendencia (info)": ("cat_trim_M", 1.0, 0.0, 0.0, False),
    "itp_8ccaa_M0 (info)": ("itp_honest", 0.0, 0.0, 0.0, False),
    "itp_8ccaa_M1_frontera (info)": ("itp_honest", 1.0, 1.0, PEND, False),
}

DGP = """
Estructura (declarada; ningún dato real). Cataluña municipio-trimestre, 2019T1-2022T1 (T = 13): ref = 2020T2 (índice 5), previos = índices 0-4 (5 coeficientes),
posteriores = índices 6-12 (7 coeficientes; el efecto empieza en el índice 7 = 2020T4 y el 6 = 2020T3 es el trimestre parcial); tratados 50/100/150 y controles 100/200/300
(S/M/L); 42 comarcas. ITP (E8): 36 provincias en 8 CCAA, una cohorte de 15 provincias (3 CCAA, índice 8), 21 controles, cluster = CCAA, ref = índice 7, 6 previos, 7 posteriores.
Resultado: el de _dgp_did.py (factores comunes con cargas heterogéneas AR(1), choque de comarca/CCAA, ruido AR(1) heterocedástico, tendencias propias d_i ~ N(0; 0,001);
efecto τ_i = τ(1 + 0,5 z_i) con rampa 1 − exp(−(e+1)/2)). Las tendencias paralelas se cumplen en esperanza.
Sesgo de tendencias diferencial (solo tratados): δ_t = s·(t − ref) para t <= ref y δ_t = m·s·(t − ref) para t > ref, con s = 0,004 por trimestre. El valor m es el de la
frontera de Δ^RM(M̄ = m): la pendiente posterior iguala m veces la previa (M̄ = 1: igual; M̄ = 0,5: la mitad; M̄ = 0: sin sesgo posterior).
Estimación dentro de cada réplica: estudio de eventos b_t = media tratados − media controles de (Y_t − Y_ref), covarianza AGRUPADA estimada (cluster = municipio, que es el nivel del
tratamiento en E2, o CCAA en E8) con factor G/(G − 1); contraste condicional ARP por piezas (src/v9) para θ = media de los 7 coeficientes posteriores.
Medidas: tamaño = rechazo de θ = 0 con τ = 0 (al borde de Δ^RM(M̄)); cobertura = 1 − rechazo de θ = θ verdadero (media de los efectos τ_i de los 7 posteriores) con τ = −0,05
(inversión del contraste) y bajo el nulo (θ = 0); potencia = rechazo de θ = 0 con τ = −0,05. Variantes de covarianza: (a) cluster del tratamiento (principal); (b) cluster = comarca
(solo en diseños municipales); (c) (a) con factor de Hotelling (G−1)/(G−k) sobre la covarianza (k coeficientes) cuando G > k + 1.
Verdad con covarianza conocida (diagnóstico): covarianza empírica de los coeficientes entre réplicas bajo el nulo.
"""

V16 = """
V15 (honest_did, NO APTO): tamaño 0,144 con M̄ = 0 y covarianza estimada por unidad (0,052 con la covarianza verdadera: el fallo no era el contraste ARP sino la covarianza),
cobertura 0,8745 en el caso frontera y tamaño 0,0 (conservador extremo) en el caso M̄ = 1 sin tendencia. V9 tuvo 7,3 % en 400 réplicas. Aquí: (1) la covarianza se agrupa por cluster del tratamiento
y se compara con la comarcal y con una versión con corrección de grados de libertad; (2) el criterio se aplica a los casos frontera de Δ^RM (M̄ = 0 con paralelismo exacto, M̄ = 0,5 y M̄ = 1 con la
pendiente posterior igual a m veces la previa); el caso M̄ = 1 sin tendencia es información (conservador por construcción: el contraste admite un sesgo que no existe); (3) se mide en tres tamaños
(50/100/150 tratados) y en el diseño de 8 CCAA, donde la covarianza agrupada tiene rango <= 7 y se espera que el método no sea válido.
"""


@functools.lru_cache(maxsize=None)
def _diseno(nombre: str):
    if nombre == "itp_honest":
        d = D.diseno("itp_8ccaa")
        coh = np.where(d.cohorte == 8, 8, -1)
        d = D.Diseno("itp_honest", d.T, coh, d.cl_fino, d.cl_grueso, d.params, d.cluster_principal)
        return d, 7, list(range(1, 7)), list(range(8, 15))
    d = D.diseno(nombre)
    return d, 5, list(range(0, 5)), list(range(6, 13))


def _drift(T: int, ref: int, s: float, m: float) -> np.ndarray:
    t = np.arange(T) - ref
    return np.where(t <= 0, s * t, m * s * t)


def datos(rng: np.random.Generator, nombre_esc: str, tau: float):
    nom, Mbar, m, s, _ = ESC[nombre_esc]
    d, ref, pre, post = _diseno(nom)
    Y, efecto = D.simular(d, rng, tau)
    tr = d.cohorte >= 0
    Y = Y.copy()
    Y[tr] += _drift(d.T, ref, s, m)[None, :]
    theta = float(efecto[tr][:, post].mean(0).mean())
    return d, Y, tr, ref, pre, post, theta


def rep(rng: np.random.Generator, nombre_esc: str, tau: float) -> list[float]:
    nom, Mbar, m, s, _ = ESC[nombre_esc]
    d, Y, tr, ref, pre, post, theta = datos(rng, nombre_esc, tau)
    npre, npost = len(pre), len(post)
    b, V, info = H.evento_agrupado(Y, tr, d.cl_fino, ref, pre, post)
    est = float(b[npre:].mean())
    thetas = [0.0] if tau == 0 else [0.0, theta]
    fila = [theta, est]
    # (a) principal
    ra = [H.contrasta(b, V, npre, npost, Mbar, t) for t in thetas]
    # (b) cluster comarca (municipal) ; para itp = igual que (a)
    if d.cluster_principal == "municipio":
        bb, Vb, _ = H.evento_agrupado(Y, tr, d.cl_grueso, ref, pre, post)
        rb = [H.contrasta(bb, Vb, npre, npost, Mbar, t) for t in thetas]
    else:
        rb = ra
    # (c) Hotelling
    G, k = info["G"], info["k"]
    f = (G - 1) / (G - k) if G > k + 1 else np.nan
    rc = [H.contrasta(b, V * f, npre, npost, Mbar, t) for t in thetas] if np.isfinite(f) else [np.nan] * len(thetas)
    out = []
    for r in (ra, rb, rc):
        r = list(r)
        if tau == 0:
            r = r + r
        out += [float(x) if x == x else np.nan for x in r]      # [rechaza_0, rechaza_verdad]
    return fila + out + [float(info["rango_V"]), float(G), float(k)]


def _a_p(M: np.ndarray, cols: list[int]) -> np.ndarray:
    """Convierte indicadores de rechazo (0/1) en pseudo p-valores (0,01 si rechaza, 1 si no) para reutilizar filas_por_p."""
    P = M.copy()
    for c in cols:
        P[:, c] = np.where(np.isnan(M[:, c]), np.nan, np.where(M[:, c] > 0.5, 0.01, 1.0))
    return P


def main(R: int = 2000, jobs: int = 4, escenarios: list[str] | None = None, salida: Path | None = None) -> pd.DataFrame:
    filas = []
    t_ini = time.time()
    for i, esc in enumerate(escenarios or list(ESC)):
        t0 = time.time()
        Mn = C.ejecutar(rep, (esc, 0.0), R, K1, i * 10 + 1, jobs)
        Ma = C.ejecutar(rep, (esc, TAU_ALT), R, K1, i * 10 + 2, jobs)
        cols = list(range(2, 8))
        Mn, Ma = _a_p(Mn, cols), _a_p(Ma, cols)
        var = {"cluster_tratamiento": (2, 3), "cluster_comarca": (4, 5), "cluster_tratamiento + Hotelling": (6, 7)}
        nom, Mbar, m, s, veredicta = ESC[esc]
        ex = {"Mbar": Mbar, "pendiente_posterior_m": m, "entra_en_veredicto": veredicta, "rango_V_medio": float(Mn[:, 8].mean()), "G": float(Mn[:, 9].mean()),
              "k": float(Mn[:, 10].mean()), "seg": round(time.time() - t0, 1)}
        filas += filas_por_p(esc, var, Mn, Ma, extra=ex)
        print(esc, [(f["variante"], round(f["tamano_5pct"], 4), round(f["cobertura_alt"], 4)) for f in filas[-3:]], ex["seg"], flush=True)
    tabla = pd.DataFrame(filas)
    prin = tabla[(tabla.variante == "cluster_tratamiento") & (tabla.entra_en_veredicto)]
    mal = prin[prin.veredicto != "APTO"]
    ok = prin[prin.veredicto == "APTO"].escenario.tolist()
    if len(mal) == 0:
        veredicto, cond = "APTO", ""
    else:
        cond = "; ".join(f"{r.escenario} ({r.fallos})" for r in mal.itertuples())
        veredicto = ("APTO CONDICIONADO (solo en: " + ", ".join(ok) + ")") if ok else "NO APTO"
    res = C.resultado_base(HERR, "¿Es válido el IC robusto de Honest DiD (magnitudes relativas, M̄ hasta 1) en los estudios de eventos de V18?",
                           "simulados (sin datos reales ni muestra sellada)", f"Cataluña 150-450 municipios x 13 trimestres; 36 provincias x 24 trimestres; R = {R}",
                           "Honest DiD (Rambachan-Roth, Δ^RM) con contraste condicional ARP por piezas; covarianza agrupada")
    r1 = (tabla[tabla.escenario == "cat_M_M1_frontera"] if (tabla.escenario == "cat_M_M1_frontera").any() else tabla).iloc[0]
    res["estimacion"] = {"tamano_M1_frontera": float(r1.tamano_5pct), "cobertura_M1_frontera": float(r1.cobertura_alt),
                         "potencia_M1": float(r1.potencia), "sesgo": float(r1.sesgo), "rmse": float(r1.rmse)}
    res["diagnosticos"] = {"veredicto": veredicto, "condicion_en_que_falla": cond, "variante_principal": "cluster_tratamiento (escenarios que entran en el veredicto)",
                           "por_escenario": {r.escenario: r.veredicto for r in prin.itertuples()}, "R": R, "segundos": round(time.time() - t_ini, 1)}
    informe = I.construir("Honest DiD (Rambachan-Roth, magnitudes relativas)", DGP, tabla, veredicto, cond,
                          ["El veredicto lo deciden los escenarios en frontera de Δ^RM con la covarianza agrupada del tratamiento; las variantes de covarianza y los escenarios marcados (info) son diagnóstico.",
                           "Con M̄ = 1 y sin tendencia el contraste es conservador por construcción (admite un sesgo que no existe).",
                           'En los casos frontera con M̄ > 0 el tamaño es 0 y la potencia contra τ = −0,05 es ≈ 0 en los tres tamaños: el IC es válido (no sobre-rechaza) pero no es nominal ni informativo con este ruido. Ancho medio del IC95 (log, 8 réplicas, 100 tratados/200 controles): 0,027 con M̄ = 0, 0,105 con M̄ = 0,5 y 0,201 con M̄ = 1 (0,168 con 150/300); es decir, con M̄ = 1 el IC solo excluye el cero si el efecto supera ≈ 0,10 en log, el doble de la magnitud de la literatura de E2 (−0,044). Por qué: la restricción relativa acota el sesgo posterior por M̄ veces el mayor salto previo, y el mayor salto previo se estima con un error del orden de 0,01 (frente a una pendiente verdadera de 0,004). Con M̄ = 0 el método es un contraste de tendencias paralelas posteriores y sí tiene potencia (0,85-1,00).'], V16,
                          ["escenario", "variante", "R", "tamano_5pct", "cobertura_nulo", "cobertura_alt", "potencia", "veredicto", "banda_112", "Mbar", "rango_V_medio"])
    C.escribir(HERR, res, tabla, informe, salida)
    return tabla


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    print(main(a.R, a.jobs).to_string())
